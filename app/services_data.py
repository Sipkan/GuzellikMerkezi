"""
Service definitions for the Merkez Beauty Center website.
Each service has a slug (URL key), display info, and before/after photo entries.

To add before/after photos:
  1. Create folder: static/images/services/{slug}/
  2. Add image pairs: before_1.jpg + after_1.jpg, before_2.jpg + after_2.jpg, etc.
  3. Update the 'before_after' list below with the file names and a caption.
"""

SERVICES = [
    {
        "slug": "hair-care",
        "title": "Hair Care & Styling",
        "card_image": "card.jpg",
        "card_image_url": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
        "short": "Professional cuts, coloring, and styling for every occasion.",
        "description": (
            "Our expert stylists deliver precision cuts, vibrant coloring, "
            "balayage, keratin treatments, and bridal styling. Whether you want "
            "a subtle refresh or a bold transformation, we tailor every service "
            "to your hair type and personal style."
        ),
        "highlights": [
            "Precision haircuts & layering",
            "Color, highlights & balayage",
            "Keratin smoothing treatments",
            "Bridal & special-occasion updos",
        ],
        "before_after": [
            # {"before": "before_1.jpg", "after": "after_1.jpg", "caption": "Balayage transformation"},
        ],
    },
    {
        "slug": "skin-care",
        "title": "Skin Care & Facials",
        "card_image": "card.jpg",
        "card_image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
        "short": "Rejuvenating facials and advanced skin treatments.",
        "description": (
            "From deep-cleansing facials to anti-aging peels and hydration "
            "therapy, our skin care menu addresses every concern. We use "
            "premium products and the latest techniques to reveal your "
            "skin's natural radiance."
        ),
        "highlights": [
            "Deep-cleansing & hydrating facials",
            "Chemical peels & microdermabrasion",
            "Anti-aging & collagen treatments",
            "Acne & pigmentation solutions",
        ],
        "before_after": [],
    },
    {
        "slug": "Altın-oran-kaş",
        "title": "Altın Oran Kaş",
        "card_image": "ButtonEyebrow.png",
        "card_image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80",
        "short": "Perfectly shaped brows designed with the golden ratio technique.",
        "description": (
            "Achieve the perfect brow shape with our signature Golden Ratio "
            "Eyebrow service. Using precise measurements based on the golden "
            "ratio, our specialists design brows that complement your unique "
            "facial structure, creating natural symmetry and harmony. The result "
            "is beautifully balanced brows that frame your face flawlessly."
        ),
        "highlights": [
            "Golden ratio facial measurement & mapping",
            "Precision brow shaping & sculpting",
            "Tinting & lamination options",
            "Personalized brow design consultation",
        ],
        "before_after": [
            {"before": "b-f(1)b.jpg", "after": "b-f(1)a.jpg", "caption": "Altın Oran Kaş Hizmeti Farkı"},
        ],
    },
    {
        "slug": "massage",
        "title": "Massage & Relaxation",
        "card_image": "card.jpg",
        "card_image_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",
        "short": "Therapeutic massage to melt away stress and tension.",
        "description": (
            "Unwind with our range of massage therapies — from Swedish and "
            "deep tissue to hot stone and aromatherapy. Our trained therapists "
            "customize every session to target your specific needs and restore "
            "your body's balance."
        ),
        "highlights": [
            "Swedish relaxation massage",
            "Deep tissue & sports massage",
            "Hot stone therapy",
            "Aromatherapy sessions",
        ],
        "before_after": [],
    },
    {
        "slug": "makeup",
        "title": "Makeup & Beauty Consultations",
        "card_image": "card.jpg",
        "card_image_url": "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?auto=format&fit=crop&w=800&q=80",
        "short": "Professional makeup and personalized beauty advice.",
        "description": (
            "Whether it's your wedding day, a photoshoot, or an evening out, "
            "our makeup artists create flawless looks tailored to you. We also "
            "offer one-on-one consultations to help you find the perfect "
            "products and routines for your skin."
        ),
        "highlights": [
            "Bridal & event makeup",
            "Photoshoot & editorial looks",
            "Personal beauty consultations",
            "Skincare routine guidance",
        ],
        "before_after": [],
    },
]

# Quick lookup by slug
SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}
