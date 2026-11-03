import pytest
from src.product import Product
from src.cart import ShoppingCart

# Фикстура создает тестовый товар перед каждым тестом
@pytest.fixture
def sample_product():
    return Product("prod_1", "Ноутбук", 50000.0, 10)

# Фикстура создает пустую корзину и регистрирует в ней товар
@pytest.fixture
def cart(sample_product):
    c = ShoppingCart()
    c.register_product(sample_product)
    return c

def test_add_item_success(cart):
    cart.add_item("prod_1", 2)
    assert cart.items["prod_1"] == 2

def test_add_item_updates_quantity(cart):
    cart.add_item("prod_1", 2)
    cart.add_item("prod_1", 3) # Должно обновить количество, а не создать новую запись
    assert cart.items["prod_1"] == 5

def test_add_item_exceeds_stock(cart):
    with pytest.raises(ValueError, match="Недостаточно товара на складе"):
        cart.add_item("prod_1", 15) # На складе всего 10

def test_add_item_invalid_quantity_zero(cart):
    with pytest.raises(ValueError, match="Количество товара должно быть больше 0"):
        cart.add_item("prod_1", 0)

def test_add_item_invalid_quantity_negative(cart):
    with pytest.raises(ValueError, match="Количество товара должно быть больше 0"):
        cart.add_item("prod_1", -5)

def test_add_item_not_in_catalog(cart):
    with pytest.raises(ValueError, match="Товар не найден в каталоге"):
        cart.add_item("unknown_id", 1)

def test_remove_item_partial(cart):
    cart.add_item("prod_1", 5)
    cart.remove_item("prod_1", 2) # Уменьшаем на 2
    assert cart.items["prod_1"] == 3

def test_remove_item_full(cart):
    cart.add_item("prod_1", 5)
    cart.remove_item("prod_1") # Удаляем полностью (quantity=None по умолчанию)
    assert "prod_1" not in cart.items

def test_remove_item_exact_amount(cart):
    cart.add_item("prod_1", 5)
    cart.remove_item("prod_1", 5) # Удаляем ровно столько, сколько есть
    assert "prod_1" not in cart.items

def test_remove_item_not_in_cart(cart):
    with pytest.raises(ValueError, match="Товар не найден в корзине"):
        cart.remove_item("prod_1")

def test_get_total_cost_empty(cart):
    assert cart.get_total_cost() == 0.0

def test_get_total_cost_with_items(cart):
    cart.add_item("prod_1", 2)
    assert cart.get_total_cost() == 100000.0