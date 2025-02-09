
#MODUL YANG DIGUNAKAN

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3 

#====================================== BAGIAN OPERASI PROGRAM =======================================#

# Abstraksi: Menyediakan struktur umum untuk kelas turunan
class Service:
    def __init__(self, nama, nomor, alamat):
        self.__nama     = nama
        self.__nomor    = nomor
        self.__alamat   = alamat
        self.__harga    = 0  # Total harga layanan

    # Getter dan Setter untuk enkapsulasi
    def get_nama(self):
        return self.__nama

    def set_nama(self, nama):
        self.__nama = nama

    def get_nomor(self):
        return self.__nomor

    def set_nomor(self, nomor):
        self.__nomor = nomor

    def get_alamat(self):
        return self.__alamat

    def set_alamat(self, alamat):
        self.__alamat = alamat

    def get_harga(self):
        return self.__harga

    def set_harga(self, harga):
        self.__harga = harga

    # Metode abstrak untuk layanan
    def layanan(self):
        pass  # Akan diimplementasikan oleh kelas turunan


# Pewarisan dan Polimorfisme: Kelas Motor mewarisi kelas Service
class Motor(Service):
    def __init__(self, nama, nomor, alamat, jenis_motor):
        super().__init__(nama, nomor, alamat)
        self.__jenis_motor = jenis_motor

    def get_jenis_motor(self):
        return self.__jenis_motor

    def set_jenis_motor(self, jenis_motor):
        self.__jenis_motor = jenis_motor

    def layanan(self):
        return f"Layanan untuk motor jenis {self.__jenis_motor}: Ganti Oli"


# Pewarisan dan Polimorfisme: Kelas Sepeda mewarisi kelas Service
class Sepeda(Service):
    def __init__(self, nama, nomor, alamat, jenis_sepeda):
        super().__init__(nama, nomor, alamat)
        self.__jenis_sepeda = jenis_sepeda

    def get_jenis_sepeda(self):
        return self.__jenis_sepeda

    def set_jenis_sepeda(self, jenis_sepeda):
        self.__jenis_sepeda = jenis_sepeda

    def layanan(self):
        return f"Layanan untuk sepeda jenis {self.__jenis_sepeda}: Cuci Sepeda"


# Fungsi untuk membuat dan menghubungkan ke database
def create_connection():
    conn = sqlite3.connect('riwayat_servis.db')
    return conn

# Fungsi untuk membuat tabel riwayat servis jika belum ada
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS riwayat_servis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        nomor TEXT,
        alamat TEXT,
        jenis_kendaraan TEXT,
        layanan TEXT,
        harga INTEGER,
        kembalian INTEGER
    )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan riwayat servis ke database
def simpan_riwayat_ke_database(nama, nomor, alamat, jenis_kendaraan, layanan, harga, kembalian):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO riwayat_servis (nama, nomor, alamat, jenis_kendaraan, layanan, harga, kembalian)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nama, nomor, alamat, jenis_kendaraan, layanan, harga, kembalian))
    conn.commit()
    conn.close()

# Fungsi untuk menampilkan riwayat dari database
def tampilkan_riwayat_dari_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM riwayat_servis ORDER BY id DESC")
    riwayat_data = cursor.fetchall()
    conn.close()

    riwayat_text = ""
    for riwayat in riwayat_data:
        riwayat_text += f"Nama                      : {riwayat[1]}\n" \
                        f"Nomor                    : {riwayat[2]}\n" \
                        f"Alamat                   : {riwayat[3]}\n" \
                        f"Layanan                : {riwayat[5]}\n" \
                        f"Jenis Kendaraan  : {riwayat[4]}\n" \
                        f"Harga                     : Rp {riwayat[6]}\n" \
                        f"Kembalian             : Rp {riwayat[7]}\n=======================================\n"

    label_riwayat.config(text=riwayat_text)
    
# Menyimpan riwayat servis
riwayat_servis = []

# fungsi hapus form
def bersihkan_form():
    # Menghapus semua entri
    entry_nama.delete(0, tk.END)
    entry_nomor.delete(0, tk.END)
    entry_alamat.delete(0, tk.END)
    entry_uang_dibayar.delete(0, tk.END)
    entry_total_harga.config(state=tk.NORMAL)
    entry_total_harga.delete(0, tk.END)  # Menghapus total harga
    entry_total_harga.config(state=tk.DISABLED)
    entry_kembalian.delete(0, tk.END)
    # Mengembalikan pilihan dropdown ke default
    jenis_kendaraan_var.set("")
    layanan_var.set("")

# Fungsi untuk menghitung harga berdasarkan jenis kendaraan dan layanan (Abstraksi)
def hitung_harga(jenis_kendaraan, layanan_pilihan):
    harga = 0
    if jenis_kendaraan == "Motor":
        if layanan_pilihan == "Ganti Oli Motor":
            harga = 50000
        elif layanan_pilihan == "Ganti Ban Motor":
            harga = 25000
        elif layanan_pilihan == "Cuci Motor Motor":
            harga = 30000
        elif layanan_pilihan == "Perawatan Rantai Motor":
            harga = 40000
        elif layanan_pilihan == "Cek Mesin Motor":
            harga = 60000
    elif jenis_kendaraan == "Sepeda":
        if layanan_pilihan == "Cuci Sepeda":
            harga = 20000
        elif layanan_pilihan == "Ganti Roda Sepeda":
            harga = 35000
        elif layanan_pilihan == "Perawatan Rem Sepeda":
            harga = 25000
        elif layanan_pilihan == "Ganti Rantai Sepeda":
            harga = 30000
        elif layanan_pilihan == "Setel Gear Sepeda":
            harga = 15000
    return harga

# Fungsi untuk memperbarui harga ketika layanan dipilih
def update_harga(*args):
    layanan_pilihan = layanan_var.get()

    harga = hitung_harga(jenis_kendaraan_var.get(), layanan_pilihan)
    
    # Mengupdate harga di entry total harga
    entry_total_harga.config(state=tk.NORMAL)   # Memungkinkan untuk mengubah entry total harga
    entry_total_harga.delete(0, tk.END)         # Menghapus nilai sebelumnya
    entry_total_harga.insert(0, f"Rp {harga}")  # Mengisi entry dengan harga baru
    entry_total_harga.config(state=tk.DISABLED) # Tidak bisa diubah oleh pengguna'



# Fungsi untuk menampilkan data motor atau sepeda
def tampilkan_data():
    try:
        harga        = float(entry_total_harga.get().replace("Rp ", "").replace(",", ""))
        uang_dibayar = float(entry_uang_dibayar.get())
    
        # Validasi uang yang dibayar
        if uang_dibayar < harga:
            messagebox.showerror("Pembayaran Tidak Cukup", "Uang yang dibayar tidak mencukupi.")
            return
        
        kembalian = uang_dibayar - harga
        
        # Memformat kembalian dengan format yang benar
        entry_kembalian.delete(0, tk.END)
        entry_kembalian.insert(0, f"Rp {kembalian:,.0f}")
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan nilai yang valid.")
    # Mengambil data dari entry fields
    nama            = entry_nama.get()
    nomor           = entry_nomor.get()
    alamat          = entry_alamat.get()
    layanan_pilihan = layanan_var.get()
    jenis_kendaraan = jenis_kendaraan_var.get()

    if not nama or not nomor or not alamat or not layanan_pilihan:
        messagebox.showerror("Input Error", "Harap isi semua kolom yang diperlukan!")
        return

    harga = hitung_harga(jenis_kendaraan, layanan_pilihan)

    # Membuat objek Motor atau Sepeda berdasarkan input
    if jenis_kendaraan == "Motor":
        kendaraan = Motor(nama, nomor, alamat, "Matic")
    else:  # Jika jenis kendaraan adalah Sepeda
        kendaraan = Sepeda(nama, nomor, alamat, "MTB")

    kendaraan.set_harga(harga)

    # Menghitung kembalian jika ada uang yang dibayar
    uang_dibayar = float(entry_uang_dibayar.get() or 0)  # Mengambil uang yang dibayar
    kembalian = uang_dibayar - harga

    # Menyimpan riwayat ke database
    simpan_riwayat_ke_database(nama, nomor, alamat, jenis_kendaraan, layanan_pilihan, harga, kembalian if kembalian >= 0 else 0)

    # Menampilkan riwayat lengkap
    tampilkan_riwayat_dari_database()

    # clear form
    bersihkan_form()



#====================================== BAGIAN GUI PROGRAM =======================================#

jendela1 = tk.Tk()
jendela1.title("Layanan Servis Motor dan Sepeda")
jendela1.geometry('950x650')
jendela1.config(background='lightgoldenrod3')


judul     =Label(jendela1, text='SERVICE KENDARAAN', font='times 20 bold',fg='saddlebrown', background='lightgoldenrod3')
judul.place(x=158,y=12)

judul     =Label(jendela1, text=' Bengkel Abadi Selamanya, JL.Teratai, Kalimanah, Purbalingga',
font='times 12 italic',fg='saddlebrown', background='lightgoldenrod3')
judul.place(x=100,y=45)

layer= Canvas(jendela1,bg='slategray3', width=590,height=485)
layer.place(x=13,y=78)

judul     =Label(jendela1, text=' SELAMAT DATANG ',
font='vendana 25 bold',fg='black', background='slategray3')
judul.place(x=150,y=85)

image1 = PhotoImage(file='D:\KULIAH 2023\LOGO\er.png')
display = Label(jendela1,bg='lightgoldenrod3',width=60,heigh=60,image=image1)
display.place(x=35,y=5)

image11 = PhotoImage(file='D:\KULIAH 2023\LOGO\er.png')
display = Label(jendela1,bg='lightgoldenrod3',width=60,heigh=60,image=image11)
display.place(x=523,y=5)
image = PhotoImage(file='D:\KULIAH 2023\LOGO\loggo.png')
display = Label(jendela1,bg='slategray3',width=500,heigh=250,image=image)
display.place(x=50,y=120)
image0 = PhotoImage(file='D:\KULIAH 2023\LOGO\welcome1.png')
display = Label(jendela1,bg='slategray3',width=300,heigh=150,image=image0)
display.place(x=150,y=360)

canvas= Canvas(jendela1,bg='tan2', width=590,height=490)
canvas.place(x=13,y=73)
canvas= Canvas(jendela1,bg='tan2', width=590,height=130)
canvas.place(x=13,y=73)

# Label dan entry untuk nama, nomor, alamat
label_nama      = tk.Label(jendela1, text="Nama",font='roboto 12 bold', background='tan2')
label_nama.place(x=20,y=80)
entry_nama      = tk.Entry(jendela1,width=55, bd=2,relief="solid")
entry_nama.place(x=155,y=80)

label_nomor     = tk.Label(jendela1, text="Nomor Telepon",font='roboto 12 bold', background='tan2')
label_nomor.place(x=20,y=120)
entry_nomor     = tk.Entry(jendela1,width=55, bd=2,relief="solid")
entry_nomor.place(x=155,y=120)

label_alamat    = tk.Label(jendela1, text="Alamat",font='roboto 12 bold', background='tan2')
label_alamat.place(x=20,y=160)
entry_alamat    = tk.Entry(jendela1,width=55, bd=2,relief="solid")
entry_alamat.place(x=155,y=160)

# Dropdown untuk memilih jenis kendaraan
label_jenis_kendaraan = tk.Label(jendela1, text="Jenis Kendaraan",font='roboto 12 bold', background='tan2')
label_jenis_kendaraan.place(x=20,y=220)

jenis_kendaraan_var = tk.StringVar()
jenis_kendaraan_var.set("Motor")  # Default adalah Motor
jenis_kendaraan_dropdown = tk.OptionMenu(jendela1, jenis_kendaraan_var, "Motor", "Sepeda", command=update_harga)
jenis_kendaraan_dropdown.place(x=155,y=220)
jenis_kendaraan_dropdown.config(width=18,height=1,bd=1,relief="groove")

# Dropdown untuk memilih layanan servis
label_layanan = tk.Label(jendela1, text="Layanan Servis",font='roboto 12 bold', background='tan2')
label_layanan.place(x=20,y=270)

layanan_var = tk.StringVar()
layanan_var.set("Ganti Oli Motor")  # Default adalah Ganti Oli
layanan_dropdown = tk.OptionMenu(jendela1, layanan_var, "Ganti Oli Motor", "Ganti Ban Motor", "Cuci Motor Motor", "Perawatan Rantai Motor", "Cek Mesin Motor", 
                                  "Cuci Sepeda", "Ganti Roda Sepeda", "Perawatan Rem Sepeda", "Ganti Rantai Sepeda", "Setel Gear Sepeda", command=update_harga)
layanan_dropdown.place(x=155,y=270)
layanan_dropdown.config(width=18,height=1,bd=1,relief="groove")

# Entry untuk total harga (otomatis terisi berdasarkan layanan)
label_total_harga = tk.Label(jendela1, text="Total Harga",font='roboto 12 bold', background='tan2').place(x=340,y=220)
entry_total_harga = tk.Entry(jendela1,width=20, bd=3,relief="flat")
entry_total_harga.place(x=450,y=220)
entry_total_harga.config(state=tk.DISABLED)  # Tidak bisa diubah oleh pengguna

# Entry untuk uang yang dibayar
label_uang_dibayar = tk.Label(jendela1, text="Bayar",font='roboto 12 bold', background='tan2')
label_uang_dibayar.place(x=340,y=270)
entry_uang_dibayar = tk.Entry(jendela1,width=20, bd=3,relief="flat")
entry_uang_dibayar.place(x=450,y=270)

# Entry untuk kembalian
label_kembalian = tk.Label(jendela1, text="Kembalian",font='roboto 12 bold', background='tan2')
label_kembalian.place(x=260,y=320)
entry_kembalian = tk.Entry(jendela1,width=20, bd=3,relief="flat")
entry_kembalian.place(x=240,y=350)

# Tombol untuk menampilkan data
cetak = PhotoImage(file='D:\cetak1.png')
tombol_tampil = tk.Button(jendela1,image=cetak,font="helvetica 11 bold",text="SAVE",width=75,height=30, bd=3,relief="ridge",compound=LEFT, command=tampilkan_data)
tombol_tampil.place(x=265,y=400)

# Tombol untuk menghitung kembalian
# tombol_hitung_kembalian = tk.Button(jendela1,font="arial 11 bold", text="Hitung",width=10, bd=3,relief="raised", command=hitung_kembalian)
# tombol_hitung_kembalian.place(x=190,y=400)

labelfr = LabelFrame(jendela1, text='\n NOTA SERVIS KENDARAAN\n\n',
background='slategray3',bd=4,font='vendana 15 bold',width=295, height=900)
labelfr.place(x=640,y=20)

labelfr1 =Label(jendela1, text='         ⟪ Bengkel Abadi Selamanya ⟫',
font='times 12 bold', background='slategray3')
labelfr1.place(x=640,y=66)

labelfr2     =Label(jendela1, text='         Jalan S.Parman No.17, Purbalingga',
font='normal 10 italic', background='slategray3')
labelfr2.place(x=640,y=90)

canvas= Canvas(jendela1,bg='white', width=280,height=792)
canvas.place(x=645,y=115)

# Label untuk menampilkan riwayat
label_riwayat = tk.Label(jendela1, text="",bg="white",font="times 10", justify=tk.LEFT)
label_riwayat.place(x=650,y=120)

# Menjalankan aplikasi Tkinter
create_table()  # Membuat tabel riwayat di database saat aplikasi dimulai
jendela1.mainloop()
