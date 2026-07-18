class MethodMeta(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if callable(value) and not key.startswith("_"):
                raise ValueError(f"Method '{key}' must start with '_'")

        return super().__new__(cls, name, bases, attrs)


class ValidClass(metaclass=MethodMeta):
    name = "Elene"

    def _test(self):
        print("Valid")

    def _hello(self):
        print("Hello")


obj = ValidClass()
obj._test()
obj._hello()


class InvalidClass(metaclass=MethodMeta):
    def test(self):
        print("Invalid")