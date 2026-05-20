"""
Sistem Manajemen Pesanan - Pendekatan Tanpa Design Pattern
File ini mendemonstrasikan bagaimana logika transisi status diatur menggunakan 
percabangan kondisional (if-elif-else) konvensional.
"""

class OrderSystemTanpaPattern:
    def __init__(self):
        # Menggunakan string biasa untuk menandakan status
        self.status = "BARU"

    def next_state(self):
        # Semua logika transisi menumpuk di satu fungsi ini
        if self.status == "BARU":
            print("Pembayaran diterima. Mengubah status ke: DIBAYAR.")
            self.status = "DIBAYAR"
            
        elif self.status == "DIBAYAR":
            print("Pesanan selesai dipacking. Mengubah status ke: DIKIRIM.")
            self.status = "DIKIRIM"
            
        elif self.status == "DIKIRIM":
            print("Kurir telah mengantarkan paket. Mengubah status ke: SELESAI.")
            self.status = "SELESAI"
            
        elif self.status == "SELESAI":
            print("Pesanan sudah selesai. Tidak ada perubahan status berikutnya.")
            
        else:
            print("Status tidak valid!")

    def show_status(self):
        # Logika pembacaan status juga menggunakan percabangan
        if self.status == "BARU":
            print("Status Saat Ini: Pesanan Baru (Belum Dibayar).")
        elif self.status == "DIBAYAR":
            print("Status Saat Ini: Sudah Dibayar (Menunggu Pengiriman).")
        elif self.status == "DIKIRIM":
            print("Status Saat Ini: Pesanan Sedang Dikirim.")
        elif self.status == "SELESAI":
            print("Status Saat Ini: Pesanan Selesai.")


# SIMULASI RUNNING
if __name__ == "__main__":
    print("=== SIMULASI TANPA DESIGN PATTERN ===\n")
    
    pesanan = OrderSystemTanpaPattern()
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
