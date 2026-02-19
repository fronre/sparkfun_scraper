from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: str
    stock: str
    link: str
    category: str
