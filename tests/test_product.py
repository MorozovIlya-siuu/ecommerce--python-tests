import pytest
from src.product import Product

def test_product_creation_success():
    product = Product("prod_1", "Ноутбук", 50000.0, 10)
    assert product.id == "prod_1"
    assert product.name == "Ноутбук"
    assert product.price == 50000.0
    assert product.stock == 10

def test_product_creation_invalid_price():
    with pytest.raises(ValueError, match="Цена и количество на складе не могут быть отрицательными"):
        Product("prod_2", "Телефон", -100.0, 5)

def test_product_creation_invalid_stock():
    with pytest.raises(ValueError, match="Цена и количество на складе не могут быть отрицательными"):
        Product("prod_3", "Планшет", 20000.0, -1)