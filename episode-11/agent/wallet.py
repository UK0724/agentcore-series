# A pretend payment session, like an AgentCore PaymentSession:
# it has a spending limit and an expiry, and refuses anything
# beyond them. PRETEND cents only.
import time


class PaymentSession:
    def __init__(self, max_spend, minutes):
        self.max_spend = max_spend
        self.spent = 0
        self.expires = time.time() + minutes * 60
        self.receipts = 0

    def pay(self, price):
        if time.time() > self.expires:
            raise PermissionError("Session expired")
        if self.spent + price["amount"] > self.max_spend:
            raise PermissionError("Spending limit reached")
        self.spent += price["amount"]
        self.receipts += 1
        return f"pretend-proof-{self.receipts}"  # a fake signature
