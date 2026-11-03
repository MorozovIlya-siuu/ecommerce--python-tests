import pytest
from src.product import Product
from src.cart import ShoppingCart

@pytest.fixture
def product():
    return Product("prod_1", "Ноутбук", 10000.0, 10)

@pytest.fixture
def cart_with_item(product):
    cart = ShoppingCart()
    cart.register_product(product)
    cart.add_item("prod_1", 2)  # 2 ноутбука по 10000 = 20000
    return cart

def test_apply_valid_promo_sale10(cart_with_item):
    cart_with_item.apply_promo_code("SALE10")
    # 20000 - 10% = 18000
    assert cart_with_item.get_total_cost() == 18000.0

def test_apply_valid_promo_sale20(cart_with_item):
    cart_with_item.apply_promo_code("SALE20")
    # 20000 - 20% = 16000
    assert cart_with_item.get_total_cost() == 16000.0

def test_apply_valid_promo_half(cart_with_item):
    cart_with_item.apply_promo_code("HALF")
    # 20000 - 50% = 10000
    assert cart_with_item.get_total_cost() == 10000.0

def test_apply_promo_case_insensitive(cart_with_item):
    # Промокод должен работать независимо от регистра
    cart_with_item.apply_promo_code("sale10")
    assert cart_with_item.get_total_cost() == 18000.0

def test_apply_promo_with_spaces(cart_with_item):
    # Пробелы по краям должны игнорироваться
    cart_with_item.apply_promo_code("  SALE10  ")
    assert cart_with_item.get_total_cost() == 18000.0

def test_apply_invalid_promo(cart_with_item):
    with pytest.raises(ValueError, match="Недействительный промокод"):
        cart_with_item.apply_promo_code("INVALID")

def test_apply_empty_promo(cart_with_item):
    with pytest.raises(ValueError, match="Промокод должен быть непустой строкой"):
        cart_with_item.apply_promo_code("")

def test_apply_none_promo(cart_with_item):
    with pytest.raises(ValueError, match="Промокод должен быть непустой строкой"):
        cart_with_item.apply_promo_code(None)

def test_apply_multiple_promos(cart_with_item):
    cart_with_item.apply_promo_code("SALE10")
    with pytest.raises(ValueError, match="Промокод уже применён"):
        cart_with_item.apply_promo_code("SALE20")

def test_reset_promo_code(cart_with_item):
    cart_with_item.apply_promo_code("SALE10")
    assert cart_with_item.get_total_cost() == 18000.0
    
    cart_with_item.reset_promo_code()
    # После сброса скидка должна исчезнуть
    assert cart_with_item.get_total_cost() == 20000.0
    assert cart_with_item.discount_percent == 0.0

def test_get_total_cost_without_promo(cart_with_item):
    # Без промокода скидка не применяется
    assert cart_with_item.get_total_cost() == 20000.0