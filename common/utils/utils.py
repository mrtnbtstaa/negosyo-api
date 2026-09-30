from apps.product_stock.models import ProductStockStatusChoice


def calculate_stock_status(
    stock_quantity: int,
    low_stock_threshold: int,
) -> str:
    if stock_quantity <= 0:
        return ProductStockStatusChoice.OUT_OF_STOCK.value

    if stock_quantity <= low_stock_threshold:
        return ProductStockStatusChoice.LOW_STOCK.value

    return ProductStockStatusChoice.IN_STOCK.value