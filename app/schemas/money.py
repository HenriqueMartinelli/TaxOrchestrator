from decimal import Decimal, ROUND_HALF_UP

class Money:
    def __init__(self, amount: Decimal):
        self.amount = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.amount + other.amount)

    def __mul__(self, other):
        if isinstance(other, (int, float, Decimal)):
            return Money(self.amount * Decimal(str(other)))
        return NotImplemented

    def __float__(self):
        return float(self.amount)

    def __repr__(self):
        return f"Money({self.amount})"
