from typing import Dict, Optional
from .product import Product

class ShoppingCart:
    def __init__(self):
        self.items: Dict[str, int] = {}
        self.products_catalog: Dict[str, Product] = {}
        self.discount_percent: float = 0.0  # Скидка в процентах (0 = нет скидки)

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
        
        # Применяем скидку, если она есть
        if self.discount_percent > 0:
            total = total * (100 - self.discount_percent) / 100
            
        return total

    def apply_promo_code(self, promo_code: str):
        """Применяет промокод к корзине. 
        Доступные промокоды:
        - 'SALE10' - скидка 10%
        - 'SALE20' - скидка 20%
        - 'HALF' - скидка 50%
        """
        promo_codes = {
            'SALE10': 10.0,
            'SALE20': 20.0,
            'HALF': 50.0,
        }
        
        if not promo_code or not isinstance(promo_code, str):
            raise ValueError("Промокод должен быть непустой строкой")
            
        promo_code = promo_code.upper().strip()
        
        if promo_code not in promo_codes:
            raise ValueError(f"Недействительный промокод: {promo_code}")
            
        if self.discount_percent > 0:
            raise ValueError("Промокод уже применён. Нельзя использовать несколько промокодов")
            
        self.discount_percent = promo_codes[promo_code]

    def reset_promo_code(self):
        """Сбрасывает применённый промокод"""
        self.discount_percent = 0.0