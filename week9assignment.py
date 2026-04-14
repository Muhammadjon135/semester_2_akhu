from dataclasses import dataclass, field
@dataclass
class Component:
    name: str
    units: float
    price_per_unit : float

    def total_price(self) -> float:
        return self.units * self.price_per_unit

@dataclass
class Assembly:
    title: str
    batch_size: int
    components: list = field(default_factory=lambda: [])
    total_price: float = field(init=False)

    def __post_init__(self):
        self.total_price = 0
        for c in self.components:
            self.total_price += c.total_price()
            # print(i.total_price(), "bear13")
    def add_component(self, component: Component):
        self.components.append(component)
        self.__post_init__()
    def price_per_item(self) -> float:
        return self.total_price / self.batch_size
    def scale(self, new_batch_size: int):
        for c in self.components:
            c.units *= new_batch_size / self.batch_size
        self.batch_size = new_batch_size
        self.__post_init__()
    def display(self) -> str:
        lines = [f"{self.title} ({self.batch_size} items):"]
        for c in self.components:
            lines.append(f"  {c.name}: {c.units} units (${c.total_price()})")
        lines.append(f"Per item: ${self.price_per_item()}\n")
        return "\n".join(lines)
a = Assembly("Drone", 8)
a.add_component(Component("Motor", 32.0, 15.0))
a.add_component(Component("Frame", 8.0, 45.0))
a.add_component(Component("Battery", 16.0, 25.0))

print(a.total_price)
print(a.price_per_item())
print(a.display())

a.scale(4)
print(a.display())

'''
1240.0
155.0
Drone (8 items):
  Motor: 32.0 units ($480.0)
  Frame: 8.0 units ($360.0)
  Battery: 16.0 units ($400.0)
Per item: $155.0

Drone (4 items):
  Motor: 16.0 units ($240.0)
  Frame: 4.0 units ($180.0)
  Battery: 8.0 units ($200.0)
Per item: $155.0

'''
