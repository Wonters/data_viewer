from .models import Formula


def test_formula():
    formula = Formula(content="a^2 + b^2 = c^2")
    assert formula.content == b"a^2 + b^2 = c^2"