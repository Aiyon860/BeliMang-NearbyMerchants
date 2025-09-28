import enum


class MerchantCategoryEnum(str, enum.Enum):
    SmallRestaurant = "SmallRestaurant"
    MediumRestaurant = "MediumRestaurant"
    LargeRestaurant = "LargeRestaurant"
    MerchandiseRestaurant = "MerchandiseRestaurant"
    BoothKiosk = "BoothKiosk"
    ConvenienceStore = "ConvenienceStore"

    __pg_name__ = "merchant_category_enum"
