import asyncio
import uuid

from dotenv import load_dotenv
from geoalchemy2 import WKTElement
from sqlalchemy import text
from passlib.context import CryptContext

from app.database import asyncSessionLocal
from app.merchants.enums import MerchantCategoryEnum
from app.merchants.models import Item, Merchant
from app.users.models import User

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ===========================
# USERS
# ===========================
USERS = [
    {
        "id": "aaaaaaaa-bbbb-cccc-dddd-111111111111",
        "username": "alice123",
        "email": "alice@example.com",
        "password": "alicepass",
    },
    {
        "id": "aaaaaaaa-bbbb-cccc-dddd-222222222222",
        "username": "bob456",
        "email": "bob@example.com",
        "password": "bobpass",
    },
    {
        "id": "aaaaaaaa-bbbb-cccc-dddd-333333333333",
        "username": "charlie789",
        "email": "charlie@example.com",
        "password": "charliepass",
    },
    {
        "id": "aaaaaaaa-bbbb-cccc-dddd-444444444444",
        "username": "diana999",
        "email": "diana@example.com",
        "password": "dianapass",
    },
    {
        "id": "aaaaaaaa-bbbb-cccc-dddd-555555555555",
        "username": "edward007",
        "email": "edward@example.com",
        "password": "edwardpass",
    },
]

# ===========================
# MERCHANTS & ITEMS
# ===========================
MERCHANTS = [
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
    "11111111-1111-1111-1111-111111111111": [
        (
            "Nasi Campur",
            "Food",
            18000,
            "https://cdn.example.com/images/nasi_campur.jpg",
        ),
        ("Es Teh", "Beverage", 5000, "https://cdn.example.com/images/es_teh.jpg"),
    ],
    "22222222-2222-2222-2222-222222222222": [
        (
            "Bakmi Special",
            "Food",
            25000,
            "https://cdn.example.com/images/bakmi_special.jpg",
        ),
        ("Pangsit", "Food", 8000, "https://cdn.example.com/images/pangsit.jpg"),
    ],
    "33333333-3333-3333-3333-333333333333": [
        ("Ayam Bakar", "Food", 35000, "https://cdn.example.com/images/ayam_bakar.jpg"),
        ("Sayur Asem", "Food", 15000, "https://cdn.example.com/images/sayur_asem.jpg"),
    ],
    "44444444-4444-4444-4444-444444444444": [
        (
            "Air Mineral",
            "Beverage",
            3000,
            "https://cdn.example.com/images/air_mineral.jpg",
        ),
        ("Roti", "Snack", 7000, "https://cdn.example.com/images/roti.jpg"),
    ],
    "55555555-5555-5555-5555-555555555555": [
        ("Soto", "Food", 20000, "https://cdn.example.com/images/soto.jpg"),
        ("Kerupuk", "Snack", 3000, "https://cdn.example.com/images/kerupuk.jpg"),
    ],
    "66666666-6666-6666-6666-666666666666": [
        ("T-Shirt", "Additions", 90000, "https://cdn.example.com/images/tshirt.jpg"),
        ("Sticker", "Additions", 15000, "https://cdn.example.com/images/sticker.jpg"),
    ],
    "77777777-7777-7777-7777-777777777777": [
        (
            "Americano",
            "Beverage",
            25000,
            "https://cdn.example.com/images/americano.jpg",
        ),
        (
            "Cappuccino",
            "Beverage",
            30000,
            "https://cdn.example.com/images/cappuccino.jpg",
        ),
    ],
    "88888888-8888-8888-8888-888888888888": [
        (
            "Nasi Goreng",
            "Food",
            20000,
            "https://cdn.example.com/images/nasi_goreng.jpg",
        ),
        ("Teh Manis", "Beverage", 5000, "https://cdn.example.com/images/teh_manis.jpg"),
    ],
    "99999999-9999-9999-9999-999999999999": [
        (
            "Roti Bakar Coklat",
            "Snack",
            12000,
            "https://cdn.example.com/images/roti_bakar_coklat.jpg",
        )
    ],
    "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa": [
        (
            "Indomie Goreng",
            "Food",
            12000,
            "https://cdn.example.com/images/indomie_goreng.jpg",
        )
    ],
}


async def seed():
    async with asyncSessionLocal() as session:
        # Clean deterministic data (users, merchants, items)
        user_ids = [uuid.UUID(u["id"]) for u in USERS]
        merchant_ids = [uuid.UUID(x[0]) for x in MERCHANTS]

        await session.execute(
            text("DELETE FROM orders WHERE user_id = ANY(:ids)"), {"ids": user_ids}
        )
        await session.execute(
            text("DELETE FROM users WHERE id = ANY(:ids)"), {"ids": user_ids}
        )
        await session.execute(
            text("DELETE FROM items WHERE merchant_id = ANY(:ids)"),
            {"ids": merchant_ids},
        )
        await session.execute(
            text("DELETE FROM merchants WHERE id = ANY(:ids)"), {"ids": merchant_ids}
        )

        # Insert users
        for u in USERS:
            hashed_pw = pwd_context.hash(u["password"])
            user = User(
                id=uuid.UUID(u["id"]),
                username=u["username"],
                email=u["email"],
                password_hash=hashed_pw,
            )
            session.add(user)
        await session.commit()

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
            for name, pc_enum, price, image_url in arr:
                it = Item(
                    id=uuid.uuid4(),
                    merchant_id=uuid.UUID(mid),
                    name=name,
                    product_category=pc_enum,
                    price=price,
                    image_url=image_url,
                )
                session.add(it)
        await session.commit()

        print("✅ Seeding users, merchants, and items completed.")


if __name__ == "__main__":
    asyncio.run(seed())
