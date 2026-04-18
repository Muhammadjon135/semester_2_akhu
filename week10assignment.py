class PaintError(Exception):
    pass
class FormulaNotFoundError(PaintError):
    def __init__(self, formula_name):
        self.formula_name = formula_name
        super().__init__(f"formula not found: {self.formula_name}")
class DuplicateFormulaError(PaintError):
    def __init__(self, formula_name):
        self.formula_name = formula_name
        super().__init__(f"formula already exists: {self.formula_name}")            
class InvalidBatchError(PaintError):
    def __init__(self, batches):
        self.batches = batches
        super().__init__(f"invalid batches: {self.batches}. must be positive")
class MissingPigmentsError(PaintError):
    def __init__(self, formula_name, missing):
        self.formula_name = formula_name
        self.missing = missing
        super().__init__(f"cannot mix {self.formula_name}: missing {self.missing}")

class PaintMixer:
    def __init__(self):
        self.formula_dict = {}

    def add_formula(self, name, batches, pigments):
        if name in self.formula_dict:
            raise DuplicateFormulaError(name)
        if batches <= 0:
            raise InvalidBatchError(batches)
        
        self.formula_dict[name] = {"batches": batches, "pigments": pigments}
    def scale_formula(self, name, desired_batches):
        try:
            formula = self.formula_dict[name]
        except KeyError:
            raise FormulaNotFoundError(name) from None
        if desired_batches < 0:
            raise InvalidBatchError(desired_batches)
        else:
            new_dict = {}
            for color, pigments in formula["pigments"].items():
                new_dict[color] = round(pigments * (desired_batches / formula["batches"]), 2)
            return new_dict
        
    def check_supplies(self, name, supplies):
        try:
            formula = self.formula_dict[name]
        except KeyError:
            raise FormulaNotFoundError(name) from None
        missing_dict = {}
        for pigment_name, amount_needed in formula["pigments"].items():
            amount_available = supplies.get(pigment_name, 0.0)
            if amount_available < amount_needed:
                missing_dict[pigment_name] = round(amount_needed - amount_available, 2)
        if missing_dict:
            raise MissingPigmentsError(name, missing_dict)
        return True

mixer = PaintMixer()

mixer.add_formula("Sunset Orange", 2, {"red": 4.0, "yellow": 3.0, "white": 1.0})
mixer.add_formula("Ocean Blue", 3, {"blue": 6.0, "white": 3.0, "green": 0.75})

scaled = mixer.scale_formula("Sunset Orange", 6)
print(f"sunset orange for 6: {scaled}")

scaled = mixer.scale_formula("Ocean Blue", 1)
print(f"ocean blue for 1: {scaled}")

supplies = {"red": 4.0, "yellow": 1.0, "white": 1.0}
try:
    mixer.check_supplies("Sunset Orange", supplies)
except PaintError as e:
    print(e)

supplies2 = {"blue": 10.0, "white": 5.0, "green": 2.0}
result = mixer.check_supplies("Ocean Blue", supplies2)
print(f"can mix ocean blue: {result}")

tests = [
    lambda: mixer.add_formula("Sunset Orange", 2, {"red": 1.0}),
    lambda: mixer.scale_formula("Forest Green", 3),
    lambda: mixer.scale_formula("Ocean Blue", -4),
]

for test in tests:
    try:
        test()
    except PaintError as e:
        print(e)
