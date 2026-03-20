def track_change(func):
    def wrapper(*args, **kwargs):
        smth = func(*args, **kwargs)
        print(f"[STOCK] {smth}")
        return smth
    return wrapper
class Supply:
    _all_supplies = []
    def __init__(self, name, unit_price, stock):
        self.name = name
        self.unit_price = float(unit_price)
        self.stock = int(stock)
        Supply._all_supplies.append(self)
    @track_change
    def add_stock(self, amount):
        self.stock += amount
        return f"{self.name}: added {amount}, now {self.stock}"
    @track_change
    def distribute(self, amount):
        if amount > self.stock:
            return f"Not enough {self.name} in storage"
        else:
            self.stock -= amount
            return f"{self.name}: distributed {amount}, now {self.stock}"
    def total_cost(self):
        return round(self.unit_price * self.stock, 1)
    @classmethod
    def from_purchase_order(cls, entry):
        name, price, stock = entry.split(":")
        return cls(name, float(price), int(stock))
    @staticmethod
    def is_valid_code(code):
        return code[0:4] == "SUP-" and code[4:].isdigit()
    @classmethod
    def office_value(cls):
        total = sum(item.total_cost() for item in cls._all_supplies)
        return float(round(total, 1))
s1 = Supply("Notebooks", 4.50, 40)
s2 = Supply.from_purchase_order("Markers:2.80:25")

s1.add_stock(10)
s1.distribute(35)
s1.distribute(100)
s2.distribute(5)

print(f"{s1.name}: cost = ${s1.total_cost()}")
print(f"{s2.name}: cost = ${s2.total_cost()}")

print(f"Valid code 'SUP-007': {Supply.is_valid_code('SUP-007')}")
print(f"Valid code 'OFF-010': {Supply.is_valid_code('OFF-010')}")
print(f"Office total: ${Supply.office_value()}")

'''
[STOCK] Notebooks: added 10, now 50
[STOCK] Notebooks: distributed 35, now 15
[STOCK] Not enough Notebooks in storage
[STOCK] Markers: distributed 5, now 20
Notebooks: cost = $67.5
Markers: cost = $56.0
Valid code 'SUP-007': True
Valid code 'OFF-010': False
Office total: $123.5
'''