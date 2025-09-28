import asyncio
import uuid

from dotenv import load_dotenv
from geoalchemy2 import WKTElement
from sqlalchemy import text

from app.database import asyncSessionLocal
from app.merchants.enums import MerchantCategoryEnum
from app.merchants.models import Item, Merchant

load_dotenv()

MERCHANTS = [
    # (uuid, name, category, image, lat, lon)
    (
        "11111111-1111-1111-1111-111111111111",
        "Warung Kayleen",
        MerchantCategoryEnum.SmallRestaurant,
        "https://cdn.example.com/images/warung_kayleen.jpg",
        -6.200000,
        106.816666,
    ),
    (
        "22222222-2222-2222-2222-222222222222",
        "Bakmi Gading",
        MerchantCategoryEnum.MediumRestaurant,
        "https://cdn.example.com/images/bakmi_gading.png",
        -6.201800,
        106.818600,
    ),
    (
        "33333333-3333-3333-3333-333333333333",
        "Depot Nusantara",
        MerchantCategoryEnum.LargeRestaurant,
        "https://cdn.example.com/images/depot_nusantara.jpg",
        -6.196000,
        106.820000,
    ),
    (
        "44444444-4444-4444-4444-444444444444",
        "Kios Mart",
        MerchantCategoryEnum.ConvenienceStore,
        "https://cdn.example.com/images/kios_mart.png",
        -6.202500,
        106.812300,
    ),
    (
        "55555555-5555-5555-5555-555555555555",
        "Booth Soto Kujang",
        MerchantCategoryEnum.BoothKiosk,
        "https://cdn.example.com/images/booth_soto.jpg",
        -6.205000,
        106.817500,
    ),
    (
        "66666666-6666-6666-6666-666666666666",
        "Merchandise Corner",
        MerchantCategoryEnum.MerchandiseRestaurant,
        "https://cdn.example.com/images/merch_corner.jpg",
        -6.198500,
        106.819200,
    ),
    (
        "77777777-7777-7777-7777-777777777777",
        "Cafe Pelangi",
        MerchantCategoryEnum.MediumRestaurant,
        "https://cdn.example.com/images/cafe_pelangi.jpg",
        -6.203200,
        106.815400,
    ),
    (
        "88888888-8888-8888-8888-888888888888",
        "Nasi Goreng Bu Rini",
        MerchantCategoryEnum.SmallRestaurant,
        "https://cdn.example.com/images/nasi_goreng_rini.jpg",
        -6.199900,
        106.814800,
    ),
    (
        "99999999-9999-9999-9999-999999999999",
        "Roti Bakar 88",
        MerchantCategoryEnum.BoothKiosk,
        "https://cdn.example.com/images/roti_bakar88.jpg",
        -6.200900,
        106.817000,
    ),
    (
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "24/7 Convenience",
        MerchantCategoryEnum.ConvenienceStore,
        "https://cdn.example.com/images/247_convenience.jpg",
        -6.197700,
        106.816100,
    ),
]

ITEMS = {
    "11111111-1111-1111-1111-111111111111": [("Nasi Campur", 18000), ("Es Teh", 5000)],
    "22222222-2222-2222-2222-222222222222": [
        ("Bakmi Special", 25000),
        ("Pangsit", 8000),
    ],
    "33333333-3333-3333-3333-333333333333": [
        ("Ayam Bakar", 35000),
        ("Sayur Asem", 15000),
    ],
    "44444444-4444-4444-4444-444444444444": [("Air Mineral", 3000), ("Roti", 7000)],
    "55555555-5555-5555-5555-555555555555": [("Soto", 20000), ("Kerupuk", 3000)],
    "66666666-6666-6666-6666-666666666666": [("T-Shirt", 90000), ("Sticker", 15000)],
    "77777777-7777-7777-7777-777777777777": [
        ("Americano", 25000),
        ("Cappuccino", 30000),
    ],
    "88888888-8888-8888-8888-888888888888": [
        ("Nasi Goreng", 20000),
        ("Teh Manis", 5000),
    ],
    "99999999-9999-9999-9999-999999999999": [("Roti Bakar Coklat", 12000)],
    "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa": [("Indomie Goreng", 12000)],
}


async def seed():
    async with asyncSessionLocal() as session:
        # Clean deterministic data
        ids = [uuid.UUID(x[0]) for x in MERCHANTS]
        await session.execute(
            text("DELETE FROM items WHERE merchant_id = ANY(:ids)"), {"ids": ids}
        )
        await session.execute(
            text("DELETE FROM merchants WHERE id = ANY(:ids)"), {"ids": ids}
        )

        # Insert merchants
        for id, name, category, image, lat, lon in MERCHANTS:
            m = Merchant(
                id=uuid.UUID(id),
                name=name,
                merchant_category=category,
                image_url=image,
                latitude=lat,
                longitude=lon,
                geog=WKTElement(f"POINT({lon} {lat})", srid=4326),
            )
            session.add(m)
        await session.commit()

        # Insert items
        for mid, arr in ITEMS.items():
            for name, price in arr:
                it = Item(
                    id=uuid.uuid4(),
                    merchant_id=uuid.UUID(mid),
                    name=name,
                    price=price,
                )
                session.add(it)
        await session.commit()

        print("Seeding merchants and items completed.")


if __name__ == "__main__":
    asyncio.run(seed())
