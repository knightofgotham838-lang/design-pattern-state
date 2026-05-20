# Tugas: Implementasi State Design Pattern - E-Commerce Order Lifecycle

Repositori ini dibuat untuk memenuhi tugas implementasi Pola Desain Berorientasi Objek (*Object-Oriented Design Patterns*). Proyek ini berfokus pada penyelesaian masalah kode spageti pada manajemen status objek menggunakan **State Design Pattern**.

---

## Dokumentasi Pola Desain (Design Pattern Template)

Berdasarkan standar dokumentasi pola desain, berikut adalah rincian aspek struktur statis, perilaku dinamis, dan implementasi dari solusi yang diterapkan:

### 1. Name
**State Design Pattern** (Pola Desain Status)

### 2. Intent / Problem
Ketika sebuah pesanan bergerak melalui alurnya (`Baru` → `Dibayar` → `Dikirim` → `Selesai`), perilaku sistem akan berubah secara drastis berdasarkan status tersebut—seperti melarang pengiriman jika belum dibayar atau menghentikan transisi setelah pesanan selesai. Jika logika ini dipaksakan masuk ke dalam satu kelas `Order` menggunakan blok `if-else` atau `switch-case` yang panjang, sistem akan mengalami masalah serius berupa kemunculan kode spageti yang membuat kelas menjadi sangat besar (*bloated*) dan sulit dibaca seiring bertambahnya aturan bisnis. Selain itu, pendekatan konvensional ini melanggar *Open/Closed Principle* (OCP) karena penambahan status baru (misalnya status Dibatalkan atau Pengembalian Dana) akan memaksa kita merombak kode inti manajemen pesanan yang sudah ada sehingga berisiko tinggi merusak alur kerja yang sudah berjalan stabil.

### 3. Solution
Solusi yang diterapkan adalah memisahkan tanggung jawab manajemen status dari kelas konteks utama ke dalam kelas-kelas terisolasi yang berdiri sendiri (*Concrete States*). 
* **Struktur Statis:** Membuat sebuah *Abstract Base Class* (interface) bernama `OrderState` yang mendefinisikan metode standar untuk setiap transisi status. Kelas `OrderContext` bertindak sebagai entitas utama yang hanya menyimpan referensi ke objek status yang aktif saat ini.
* **Perilaku Dinamis:** Setiap status konkret (`NewOrderState`, `PaidState`, `ShippedState`, `CompletedState`) mengimplementasikan interface `OrderState` dan bertanggung jawab penuh atas logika transisinya sendiri. Ketika metode `next_state()` dipanggil pada konteks, tugas tersebut didelegasikan langsung ke objek status aktif, yang kemudian akan mengubah status internal konteks secara dinamis ke status berikutnya.

### 4. Sample Code
Implementasi solusi menggunakan bahasa pemrograman Python:

```python
from abc import ABC, abstractmethod

# State Interface
class OrderState(ABC):
    @abstractmethod
    def next(self, order):
        pass
    
    @abstractmethod
    def print_status(self):
        pass

# Concrete States
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

# Context
class OrderContext:
    def __init__(self):
        self._state = NewOrderState()
        
    def set_state(self, state: OrderState):
        self._state = state
        
    def next_state(self):
        self._state.next(self)
        
    def show_status(self):
        self._state.print_status()

# Simulation Execution
if __name__ == "__main__":
    print("=== SIMULASI LIFECYCLE PESANAN ===\n")
    pesanan = OrderContext()
    pesanan.show_status()
    print("-" * 40)
    
    pesanan.next_state() # Baru -> Dibayar
    pesanan.show_status()
    print("-" * 40)
    
    pesanan.next_state() # Dibayar -> Dikirim
    pesanan.show_status()
    print("-" * 40)
    
    pesanan.next_state() # Dikirim -> Selesai
    pesanan.show_status()

| Lines | Code Segment                                    | Explanation                                                                                            |
| ----- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1     | `from abc import ABC, abstractmethod`           | Mengimpor `ABC` dan `abstractmethod` dari modul `abc` untuk membuat abstract class dan method abstrak. |
| 5-15  | `class OrderState(ABC):`                        | Membuat abstract class `OrderState` sebagai interface dasar untuk semua state pesanan.                 |
| 7-10  | `@abstractmethod def next(self, order):`        | Method abstrak untuk berpindah ke state berikutnya. Semua subclass wajib mengimplementasikannya.       |
| 13-15 | `@abstractmethod def print_status(self):`       | Method abstrak untuk menampilkan status pesanan saat ini.                                              |
| 20    | `class NewOrderState(OrderState):`              | State konkret untuk kondisi pesanan baru dan belum dibayar.                                            |
| 21-23 | `def next(self, order): ...`                    | Mengubah status dari `NewOrderState` menjadi `PaidState`.                                              |
| 25-26 | `def print_status(self): ...`                   | Menampilkan status bahwa pesanan masih baru dan belum dibayar.                                         |
| 31    | `class PaidState(OrderState):`                  | State konkret untuk pesanan yang sudah dibayar.                                                        |
| 32-34 | `def next(self, order): ...`                    | Mengubah status dari `PaidState` menjadi `ShippedState`.                                               |
| 36-37 | `def print_status(self): ...`                   | Menampilkan status bahwa pesanan sudah dibayar dan menunggu pengiriman.                                |
| 42    | `class ShippedState(OrderState):`               | State konkret untuk pesanan yang sedang dikirim.                                                       |
| 43-45 | `def next(self, order): ...`                    | Mengubah status dari `ShippedState` menjadi `CompletedState`.                                          |
| 47-48 | `def print_status(self): ...`                   | Menampilkan status bahwa pesanan sedang dalam proses pengiriman.                                       |
| 53    | `class CompletedState(OrderState):`             | State konkret untuk pesanan yang telah selesai.                                                        |
| 54-56 | `def next(self, order): ...`                    | Tidak ada perpindahan state lagi karena pesanan sudah selesai.                                         |
| 58-59 | `def print_status(self): ...`                   | Menampilkan status akhir bahwa pesanan selesai.                                                        |
| 64    | `class OrderContext:`                           | Context class yang menyimpan state aktif dari pesanan.                                                 |
| 65-66 | `def __init__(self): ...`                       | Menginisialisasi pesanan dengan state awal `NewOrderState`.                                            |
| 68-69 | `def set_state(self, state): ...`               | Mengubah state aktif pesanan ke state baru.                                                            |
| 71-72 | `def next_state(self): ...`                     | Memanggil method `next()` pada state aktif untuk berpindah state.                                      |
| 74-75 | `def show_status(self): ...`                    | Memanggil method `print_status()` pada state aktif untuk menampilkan status.                           |
| 80    | `if __name__ == "__main__":`                    | Entry point program agar kode hanya berjalan saat file dieksekusi langsung.                            |
| 81    | `print("=== SIMULASI LIFECYCLE PESANAN ===\n")` | Menampilkan judul simulasi lifecycle pesanan.                                                          |
| 83    | `pesanan = OrderContext()`                      | Membuat objek pesanan baru dengan state awal `NewOrderState`.                                          |
| 84    | `pesanan.show_status()`                         | Menampilkan status awal pesanan.                                                                       |
| 85    | `print("-" * 40)`                               | Menampilkan garis pemisah output agar lebih rapi.                                                      |
| 88    | `pesanan.next_state()`                          | Mengubah state dari `NewOrderState` ke `PaidState`.                                                    |
| 89    | `pesanan.show_status()`                         | Menampilkan status setelah pembayaran diterima.                                                        |
| 90    | `print("-" * 40)`                               | Menampilkan garis pemisah.                                                                             |
| 93    | `pesanan.next_state()`                          | Mengubah state dari `PaidState` ke `ShippedState`.                                                     |
| 94    | `pesanan.show_status()`                         | Menampilkan status setelah pesanan dikirim.                                                            |
| 95    | `print("-" * 40)`                               | Menampilkan garis pemisah.                                                                             |
| 98    | `pesanan.next_state()`                          | Mengubah state dari `ShippedState` ke `CompletedState`.                                                |
| 99    | `pesanan.show_status()`                         | Menampilkan status akhir pesanan selesai.                                                              |
