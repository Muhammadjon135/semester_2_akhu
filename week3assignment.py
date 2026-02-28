class MaterialBatch:
    def __init__(self, material_name: str, cost_per_unit: float, unit_count: int):
        self.material_name = material_name
        self.cost_per_unit = cost_per_unit
        self.unit_count = unit_count

    def __str__(self):    
        return f"{self.material_name}: {self.unit_count} unit(s) at ${self.cost_per_unit}"
    
    def __repr__(self):
        return f"MaterialBatch('{self.material_name}', {self.cost_per_unit}, {self.unit_count})"
    
    def __add__(self, other):
        if isinstance(other, MaterialBatch):
            if self.material_name == other.material_name:
                return MaterialBatch(self.material_name, self.cost_per_unit, self.unit_count + other.unit_count)
            return NotImplemented
        elif isinstance(other, int):
            return MaterialBatch(self.material_name, self.cost_per_unit, self.unit_count + other)        
        return NotImplemented
    
    def __eq__(self, value):
        if isinstance(value, MaterialBatch):
            return (self.material_name, self.cost_per_unit) == (value.material_name, value.cost_per_unit)
        return NotImplemented
    def __bool__(self):
        return self.unit_count > 0

batch1 = MaterialBatch("Bricks", 0.5, 100)
batch2 = MaterialBatch("Bricks", 0.5, 50)
batch3 = MaterialBatch("Cement", 8.0, 0)

print(str(batch1))
print(repr(batch1))
print(batch1 + batch2)
print(batch1 + 200)
print(batch1 == batch2)
print(bool(batch1))
print(bool(batch3))

'''
Bricks: 100 unit(s) at $0.5
MaterialBatch('Bricks', 0.5, 100)
Bricks: 150 unit(s) at $0.5
Bricks: 300 unit(s) at $0.5
True
True
False
'''