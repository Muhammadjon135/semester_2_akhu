from abc import ABC, abstractmethod

class Priceable(ABC):
    @abstractmethod
    def service_fee(self):
        pass
class Formattable(ABC):
    @abstractmethod
    def format_ticket(self):
        pass
class Ticket(Priceable, Formattable):
    def __init__(self, event, price):
        self.event = event
        if price < 0:
            raise ValueError(f"Invalid price: {price}")
        else:
            self.price = price
    def service_fee(self):
        return round(self.price * 0.12, 2)
    def format_ticket(self):
        return f"{self.event}: ${self.price:.2f}"
class EarlyBirdTicket(Ticket):
    def __init__(self, event, price, discount):
        super().__init__(event, price)
        if 0 < discount < 1:
            self.discount = discount
        else:
            raise ValueError("Discount should be between 0 and 1")
    def final_price(self):
        return round(self.price * (1 - self.discount), 2)
    def service_fee(self):
        return round(self.final_price() * 0.12, 2)
    def format_ticket(self):
        return f"{super().format_ticket()} -> ${self.final_price():.2f} (-{int(self.discount*100)}%)"
class PremiumTicket(Ticket):
    def __init__(self, event, price, vip_surcharge):
        super().__init__(event, price)
        self.vip = vip_surcharge
    def service_fee(self):
        return round(self.price * 0.12 + self.price * self.vip, 2)
    def format_ticket(self):
        return f"{super().format_ticket()} (premium, surcharge {int(self.vip*100)}%)"
class CompPass:
    def __init__(self, event, price=0):
        self.event = event
        self.price = price
    def service_fee(self):
        return 0.0
    def format_ticket(self):
        return f"{self.event}: $0.00 (complimentary)"
class Invoice:
    def __init__(self):
        self.lines = []
    def add_line(self, description, fee):
        self.lines.append((description, fee))
    def print_invoice(self):
        for line in self.lines:
            print(f"  {line[0]} | fee: ${line[1]:.2f}")
            
class TicketOrder:
    def __init__(self, buyer_name):
        self.b_name = buyer_name
        self.invoice = Invoice()
        self.tickets = []
    def add_ticket(self, ticket):
        self.tickets.append(ticket)
    def finalize(self):
        print(f"Order for {self.b_name}")
        subtotal = 0
        total_fees = 0
        for ticket in self.tickets:
            self.invoice.add_line(ticket.format_ticket(), ticket.service_fee())
            subtotal += ticket.price
            total_fees += ticket.service_fee() 
        self.invoice.print_invoice()

        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Total Fees: ${total_fees:.2f}")
        print(f"Grand Total: ${(subtotal + total_fees):.2f}")





order = TicketOrder('Nodira')

order.add_ticket(Ticket('Rock Concert', 80))
order.add_ticket(EarlyBirdTicket('Jazz Night', 120, 0.20))
order.add_ticket(PremiumTicket('Opera Gala', 200, 0.30))
order.add_ticket(CompPass('Staff Meeting', 0))

try:
    order.add_ticket(Ticket('Bad Event', -10))
except ValueError as e:
    print(f'Skipped: {e}')

order.finalize()

try:
    p = Priceable()
except TypeError:
    print('Cannot instantiate abstract class')


'''
Skipped: Invalid price: -10
Order for Nodira
  Rock Concert: $80.00 | fee: $9.60
  Jazz Night: $120.00 -> $96.00 (-20%) | fee: $11.52
  Opera Gala: $200.00 (premium, surcharge 30%) | fee: $84.00
  Staff Meeting: $0.00 (complimentary) | fee: $0.00
Subtotal: $400.00
Total Fees: $105.12
Grand Total: $505.12
Cannot instantiate abstract class
'''