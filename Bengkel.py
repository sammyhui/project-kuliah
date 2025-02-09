from tkinter import *

def ganti_ke_frame2():
    frame1.grid_forget()  # Menyembunyikan frame1
    frame2.grid(row=0, column=0, padx=10, pady=10)  # Menampilkan frame2

def ganti_ke_frame3():
    frame2.grid_forget()  # Menyembunyikan frame2
    frame3.grid(row=0, column=0, padx=10, pady=10)  # Menampilkan frame3

def ganti_ke_frame1():
    frame3.grid_forget()  # Menyembunyikan frame3
    frame1.grid(row=0, column=0, padx=10, pady=10)  # Menampilkan frame1

# Membuat jendela utama
main = Tk()
main.title("Ganti Frame Contoh - 3 Frame")
main.geometry('500x400')

# Frame pertama (frame1)
frame1 = Frame(main, bg='lightblue', width=500, height=400)
frame1.grid(row=0, column=0, padx=10, pady=10)

label1 = Label(frame1, text="Ini adalah Frame 1", font='times 12 bold', bg='lightblue')
label1.grid(row=0, column=0, padx=10, pady=10)

# Tombol untuk mengganti ke frame2
button_ganti2 = Button(frame1, text="Ke Frame 2", font="times 12 bold", bg="lightgreen", command=ganti_ke_frame2)
button_ganti2.grid(row=1, column=0, pady=10)

# Frame kedua (frame2)
frame2 = Frame(main, bg='lightgreen', width=500, height=400)
# Frame2 disembunyikan terlebih dahulu
label2 = Label(frame2, text="Ini adalah Frame 2", font='times 12 bold', bg='lightgreen')
label2.grid(row=0, column=0, padx=10, pady=10)

# Tombol untuk mengganti ke frame3
button_ganti3 = Button(frame2, text="Ke Frame 3", font="times 12 bold", bg="lightcoral", command=ganti_ke_frame3)
button_ganti3.grid(row=1, column=0, pady=10)

# Frame ketiga (frame3)
frame3 = Frame(main, bg='lightcoral', width=500, height=400)
# Frame3 disembunyikan terlebih dahulu
label3 = Label(frame3, text="Ini adalah Frame 3", font='times 12 bold', bg='lightcoral')
label3.grid(row=0, column=0, padx=10, pady=10)

# Tombol untuk kembali ke frame1
button_kembali1 = Button(frame3, text="Ke Frame 1", font="times 12 bold", bg="lightblue", command=ganti_ke_frame1)
button_kembali1.grid(row=1, column=0, pady=10)

# Menjalankan aplikasi Tkinter
main.mainloop()
