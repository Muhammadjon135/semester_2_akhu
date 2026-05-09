from abc import ABC, abstractmethod

class Seat(ABC):
    def __init__(self, viewer):
        self.viewer = viewer
    @abstractmethod
    def ticket_price(self):
        pass
class Standard(Seat):
    def ticket_price(self):
        return 35_000
class Premium(Seat):
    def ticket_price(self):
        return 70_000
class Vip(Seat):
    def ticket_price(self):
        return 120_000
class TicketSystem:
    def __init__(self):
        self.bookings = []   # list of (viewer, seat_class)

    def add(self, seat: Seat):
        self.bookings.append(seat)
    def run(self, ticket, qr_sender):
            # [print(i) for i in self.bookings]
            ticket.print_ticket(self.bookings)
            qr_sender.send(self.bookings)

class Ticket(ABC):
    @abstractmethod
    def print_ticket(self, bookings):
        pass
class PaperTicket(Ticket):
    def print_ticket(self, bookings):
        for booking in bookings:
            print(f"TICKET <{booking.viewer}> price={booking.ticket_price()}")
class QrSender(ABC):
    @abstractmethod
    def send(self, bookings):
        pass
class TelegramQrSender(QrSender):
    def send(self, bookings):
        for booking in bookings:
            print(f"[QR → {booking.viewer}] Show this at entrance. Paid {booking.ticket_price()} so'm")


cinema = TicketSystem()
cinema.add(Standard("Anakin"))
cinema.add(Premium("Obi-Wan"))
cinema.add(Vip("Yoda"))

cinema.run(PaperTicket(), TelegramQrSender())
'''
TICKET <Anakin> price=35000
TICKET <Obi-Wan> price=70000
TICKET <Yoda> price=120000
[QR → Anakin] Show this at entrance. Paid 35000 so'm
[QR → Obi-Wan] Show this at entrance. Paid 70000 so'm
[QR → Yoda] Show this at entrance. Paid 120000 so'm
'''
