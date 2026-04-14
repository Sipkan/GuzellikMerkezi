from contextlib import asynccontextmanager
from pathlib import Path
import re

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session, init_db
from app.db_models import CallbackRequest as CallbackRequestDB
from app.services_data import SERVICES, SERVICES_BY_SLUG

# Paths
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
# Workaround for a Jinja2 caching key bug on some environments:
# disable template caching to avoid 500s during template loading.
templates.env.cache = None

# Make SERVICES available in every template (used by the footer)
templates.env.globals["all_services"] = SERVICES


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Merkez Beauty Center", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About Us page."""
    return templates.TemplateResponse(request, "about.html")


@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    """Our Services page."""
    return templates.TemplateResponse(request, "services.html", {"services": SERVICES})


@app.get("/services/{slug}", response_class=HTMLResponse)
async def service_detail(request: Request, slug: str):
    """Individual service detail page."""
    service = SERVICES_BY_SLUG.get(slug)
    if not service:
        from fastapi.responses import JSONResponse
        return JSONResponse({"detail": "Service not found"}, status_code=404)
    return templates.TemplateResponse(request, "service_detail.html", {"service": service})

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    """Blog page."""
    return templates.TemplateResponse(request, "blog.html")


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Communication / Contact page."""
    return templates.TemplateResponse(request, "contact.html")


@app.get("/admin/adminDashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Admin dashboard - view callback requests. No links from main site."""
    result = await session.execute(
        select(CallbackRequestDB).order_by(CallbackRequestDB.created_at.desc())
    )
    rows = result.scalars().all()
    # Convert to dicts while session is active (template renders after session closes)
    callbacks = [
        {
            "name": cb.name,
            "phone": cb.phone,
            "email": cb.email or "-",
            "message": cb.message or "-",
            "created_at": cb.created_at.strftime("%Y-%m-%d %H:%M") if cb.created_at else "-",
        }
        for cb in rows
    ]
    return templates.TemplateResponse(request, "admin_dashboard.html", {"callbacks": callbacks})

@app.post("/callback")
async def submit_callback(
    name: str = Form(...),
    phone: str = Form(...),
    email: str | None = Form(None),
    message: str | None = Form(None),
    session: AsyncSession = Depends(get_session),
):
    """Handle callback request form submission."""
    # Normalize phone to digits and validate Turkish GSM (05xx + 9 digits).
    phone_digits = re.sub(r"\D", "", phone or "")
    if phone_digits.startswith("90"):
        phone_digits = "0" + phone_digits[2:]
    if phone_digits.startswith("5"):
        phone_digits = "0" + phone_digits

    if not re.fullmatch(r"05\d{9}", phone_digits):
        return RedirectResponse(url="/contact?phone_error=1", status_code=303)

    callback = CallbackRequestDB(
        name=name,
        phone=phone_digits,
        email=email or None,
        message=message or None,
    )
    session.add(callback)
    await session.flush()
    return RedirectResponse(url="/contact?submitted=1", status_code=303)


# ================= SEO ROUTES =================

@app.get("/robots.txt", response_class=HTMLResponse)
async def robots_txt():
    """Robots.txt for search engine crawlers."""
    content = """User-agent: *
Allow: /
Disallow: /admin/

Sitemap: https://www.pinarsedasayan.com/sitemap.xml
"""
    from fastapi.responses import Response
    return Response(content=content, media_type="text/plain")


@app.get("/sitemap.xml", response_class=HTMLResponse)
async def sitemap_xml():
    """XML Sitemap for search engines."""
    from fastapi.responses import Response
    from datetime import date

    today = date.today().isoformat()
    base_url = "https://www.pinarsedasayan.com"

    # Static pages with priorities
    pages = [
        {"url": "/", "priority": "1.0", "changefreq": "weekly"},
        {"url": "/about", "priority": "0.8", "changefreq": "monthly"},
        {"url": "/services", "priority": "0.9", "changefreq": "weekly"},
        {"url": "/contact", "priority": "0.7", "changefreq": "monthly"},
    ]

    # Add all service detail pages
    for service in SERVICES:
        pages.append({
            "url": f"/services/{service['slug']}",
            "priority": "0.8",
            "changefreq": "monthly",
        })

    xml_entries = []
    for page in pages:
        xml_entries.append(f"""  <url>
    <loc>{base_url}{page['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(xml_entries)}
</urlset>"""

    return Response(content=xml, media_type="application/xml")