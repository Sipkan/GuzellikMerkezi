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
        "slug": "lazer-epilasyon",
        "title": "Lazer Epilasyon",
        "card_image": "lazer-epilasyon.png",
        "card_image_url": "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80",
        "short": "Kalıcı ve etkili lazer epilasyon ile pürüzsüz bir cilde kavuşun.",
        "description": (
            "Son teknoloji lazer cihazlarımız ile tüm vücut bölgelerinde kalıcı "
            "epilasyon hizmeti sunuyoruz. Her cilt tipine uygun, güvenli ve ağrısız "
            "uygulamalar ile istenmeyen tüylerden kalıcı olarak kurtulmanızı sağlıyoruz. "
            "Uzman ekibimiz kişiye özel tedavi planı oluşturarak en etkili sonuçları garanti eder."
        ),
        "highlights": [
            "Son teknoloji lazer cihazları",
            "Tüm vücut bölgelerine uygulama",
            "Ağrısız & konforlu seanslar",
            "Kişiye özel tedavi planı",
        ],
        "before_after": [
            # {"before": "before_1.jpg", "after": "after_1.jpg", "caption": "Lazer epilasyon sonuçları"},
        ],
    },
    {
        "slug": "cilt-bakimi",
        "title": "Cilt bakımı & Leke Protokolü",
        "card_image": "cilt-bakimi.png",
        "card_image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=800&q=80",
        "short": "Canlandırıcı yüz bakımları ve gelişmiş cilt tedavileri.",
        "description": (
            "Derin temizlik yüz bakımından anti-aging peeling ve nemlendirme "
            "tedavilerine kadar geniş bir cilt bakım menüsü sunuyoruz. "
            "Premium ürünler ve en son tekniklerle cildinizin doğal "
            "parlaklığını ortaya çıkarıyoruz."
        ),
        "highlights": [
            "Derin temizlik & nemlendirici yüz bakımı",
            "Kimyasal peeling & mikrodermabrazyon",
            "Anti-aging & kolajen tedavileri",
            "Akne & pigmentasyon çözümleri",
        ],
        "before_after": [],
    },
    {
        "slug": "Altın-oran-kaş",
        "title": "Altın Oran Kaş Tasarım",
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
        "slug": "kilo-verme",
        "title": "Bölgesel İncelme",
        "card_image": "kilo-verme.png",
        "card_image_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=800&q=80",
        "short": "Etkili ve sağlıklı yöntemlerle kilo vermenize yardımcı oluyoruz.",
        "description": (
            "Profesyonel ekibimiz ile kişiye özel kilo verme programları sunuyoruz. "
            "Bölgesel incelme, lipoliz, lenf drenaj ve diyet danışmanlığı gibi "
            "kapsamlı hizmetlerimiz ile sağlıklı ve kalıcı sonuçlar elde etmenizi sağlıyoruz. "
            "Her tedavi planı bireysel ihtiyaçlarınıza göre özelleştirilir."
        ),
        "highlights": [
            "Bölgesel incelme uygulamaları",
            "Lipoliz & kavitasyon",
            "Lenf drenaj masajı",
            "Kişiye özel diyet danışmanlığı",
        ],
        "before_after": [],
    },
    {
        "slug": "kalici-makyaj",
        "title": "Kalıcı Makyaj",
        "card_image": "kalici-makyaj.png",
        "card_image_url": "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?auto=format&fit=crop&w=800&q=80",
        "short": "Doğal görünümlü kalıcı makyaj ile her an kusursuz olun.",
        "description": (
            "Kalıcı makyaj hizmetimiz ile kaş, dudak ve eyeliner uygulamaları yapıyoruz. "
            "Uzman ekibimiz yüz hatlarınıza en uygun renk ve şekli belirleyerek "
            "doğal ve kusursuz bir görünüm elde etmenizi sağlar. Kalıcı makyaj ile "
            "her sabah makyaja harcadığınız zamanı kazanın."
        ),
        "highlights": [
            "Kalıcı kaş kontürü",
            "Dudak renklendirme",
            "Kalıcı eyeliner",
            "Doğal & kişiye özel renk seçimi",
        ],
        "before_after": [],
    },
]

# Quick lookup by slug
SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}
