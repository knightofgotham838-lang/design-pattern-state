"""
Sistem Manajemen Pesanan - Menggunakan State Design Pattern
File ini mendemonstrasikan bagaimana logika transisi status diisolasi ke dalam 
objek status masing-masing (Concrete State) untuk memenuhi prinsip SOLID.
"""

from abc import ABC, abstractmethod

# 1. STATE INTERFACE 
class OrderState(ABC):
    @abstractmethod
    def next(self, order):
        pass
    
    @abstractmethod
    def print_status(self):
        pass


# 2. CONCRETE STATES
class NewOrderState(OrderState):
    def next(self, order):
        print("Pembayaran diterima. Mengubah status ke: DIBAYAR.")
        order.set_state(PaidState())
        
    def print_status(self):
        print("Status Saat Ini: Pesanan Baru (Belum Dibayar).")


class PaidState(OrderState):
    def next(self, order):
        print("Pesanan selesai dipacking. Mengubah status ke: DIKIRIM.")
        order.set_state(ShippedState())
        
    def print_status(self):
        print("Status Saat Ini: Sudah Dibayar (Menunggu Pengiriman).")


class ShippedState(OrderState):
    def next(self, order):
        print("Kurir telah mengantarkan paket. Mengubah status ke: SELESAI.")
        order.set_state(CompletedState())
        
    def print_status(self):
        print("Status Saat Ini: Pesanan Sedang Dikirim.")


class CompletedState(OrderState):
    def next(self, order):
        print("Pesanan sudah selesai. Tidak ada perubahan status berikutnya.")
        
    def print_status(self):
        print("Status Saat Ini: Pesanan Selesai.")


# 3. CONTEXT
class OrderContext:
    def __init__(self):
        # State awal diatur ke NewOrderState
        self._state = NewOrderState()
        
    def set_state(self, state: OrderState):
        self._state = state
        
    def next_state(self):
        self._state.next(self)
        
    def show_status(self):
        self._state.print_status()


# 4. TESTING (SIMULASI RUNNING)
if __name__ == "__main__":
    print("=== SIMULASI LIFECYCLE PESANAN (STATE PATTERN) ===\n")
    
    # Inisialisasi pesanan baru
    pesanan = OrderContext()
    pesanan.show_status()
    print("-" * 40)
    
    # Transisi 1: Baru -> Dibayar
    pesanan.next_state()
    pesanan.show_status()
    print("-" * 40)
    
    # Transisi 2: Dibayar -> Dikirim
    pesanan.next_state()
    pesanan.show_status()
    print("-" * 40)
    
    # Transisi 3: Dikirim -> Selesai
    pesanan.next_state()
    pesanan.show_status()
    print("-" * 40)
    
    # Mencoba transisi lagi ketika sudah selesai
    pesanan.next_state()
