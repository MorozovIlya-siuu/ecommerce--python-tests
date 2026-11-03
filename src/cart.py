from typing import Dict
from .product import Product

class ShoppingCart:
    def __init__(self):
        self.items: Dict[str, int] = {}
        self.products_catalog: Dict[str, Product] = {}

    def register_product(self, product: Product):
        self.products_catalog[product.id] = product

    def add_item(self, product_id: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Количество товара должно быть больше 0")
        if product_id not in self.products_catalog:
            raise ValueError("Товар не найден в каталоге")
        
        product = self.products_catalog[product_id]
        current_in_cart = self.items.get(product_id, 0)
        
        if current_in_cart + quantity > product.stock:
            raise ValueError(f"Недостаточно товара на складе. Доступно: {product.stock}")
            
        self.items[product_id] = current_in_cart + quantity

    def remove_item(self, product_id: str, quantity: int = None):
        if product_id not in self.items:
            raise ValueError("Товар не найден в корзине")
            
        if quantity is None or quantity >= self.items[product_id]:
            del self.items[product_id]
        else:
            self.items[product_id] -= quantity

    def get_total_cost(self) -> float:
        total = 0.0
        for prod_id, qty in self.items.items():
            total += self.products_catalog[prod_id].price * qty
        return total