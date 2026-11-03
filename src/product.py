class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if price < 0 or stock < 0:
            raise ValueError("Цена и количество на складе не могут быть отрицательными")
        self.id = product_id
        self.name = name
        self.price = price
        self.stock = stock