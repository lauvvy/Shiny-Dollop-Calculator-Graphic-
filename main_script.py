# Import library GUI dan modul pendukung
import tkinter
import turtle
import GraphGen
import FuncParser
import history_parser

# Mengambil canvas turtle dan root Tkinter
canvas = turtle.getcanvas()
root = canvas.master
# Membaca riwayat fungsi dari file (history)
OPTIONS = history_parser.read_from()

# TAMPILAN UTAMA
title = tkinter.Label(root, text="Shiny Dollop Graphic Calculator", font="Arial, 16") # judul aplikasi 
title.pack(before=canvas)

# Frame utama di sisi kiri canvas
main_frame = tkinter.Frame(root, width=300)
main_frame.pack(after=canvas, side="left", fill="both", padx=10)

# TOMBOL RIEMANN SUM
r_sum_btn = tkinter.Button(main_frame, text="Riemann Sum", font="Arial, 12",
                           width=15)
r_sum_btn.grid(row=1, column=0, sticky="W")

# INPUT FUNGSI f(x)
# Varibel teks untuk entry fungsi
e_txt = tkinter.StringVar()
# Entry tempat user menulis fungsi f(x)
fx_input = tkinter.Entry(main_frame, font="Arial, 12", textvariable=e_txt)
fx_input.grid(row=0, column=2)


# History
def callback(selection):  # command untuk opsi pilihan 
    global e_txt
    e_txt.set("")
    e_txt.set(selection) # mengisi entry dengan pilihan history

# Variabel untuk option menu
var = tkinter.StringVar()
var.set("History")

# Dropdown history fungsi
fx_options = tkinter.OptionMenu(main_frame, var, *OPTIONS, command=callback)
fx_options.grid(row=0, column=3)

# Fungsi untuk membantu setiap item history tetap memanggil callback
def handle_option_select(v):  # adds the callback command to every options
    var.set(v)
    callback(v)

# Memperbarui isi OptionMenu setelah history berubah
def update_options():
    global fx_options, OPTIONS
    OPTIONS = history_parser.read_from() # mebmaca ulang file history
    fx_options['menu'].delete(0, tkinter.END)
    for item in OPTIONS:
        fx_options['menu'].add_command(
            label=item,
            command=lambda v=item: handle_option_select(v)
        )

# FUNGSI RIEMANN SUM
# Menghitung dan menggambar Riemann Sum
def gen_riemann(n, l_lim, u_lim, area_label):
    GraphGen.turt3.clear() # menghapus gambar Riemann sebelumnya
    GraphGen.riemann_called = True

  # mengkonversi input ke tipe numerik
    n = int(n)
    l_lim = float(l_lim)
    u_lim = float(u_lim)
  # Menyimpan parameter ke GraphGen
    GraphGen.pl_n = n
    GraphGen.pl_ll = l_lim
    GraphGen.pl_ul = u_lim
  # Menghitung luas Riemann
    area = GraphGen.riemann_sum(n, l_lim, u_lim)
  # Koreksi tanda jika batas terbalik
    if u_lim < l_lim:
        area *= -1
      # Tampilkan hasil
    area_label.config(text=f"Hasil = {area:.4f}")
    GraphGen.turt3.screen.update()

# POPUP RIEMANN SUM
# Riemann Entries
popped_up = False
r_s_popup = None

 #Membuat input popup riemann sum
def riemann_popup():
    global popped_up, r_s_popup
    if popped_up: # Jika popup sudah ada, tutup
        r_s_popup.destroy()
        popped_up = False
        return
    else:
        r_s_popup = tkinter.Toplevel(main_frame)
    r_s_popup.overrideredirect(True)
    r_s_popup.attributes('-topmost', True)

    input_frame = tkinter.Frame(r_s_popup, bd=3, relief="sunken")
    input_frame.pack()

    # Posisi popup relatif terhadap tombol
    r_s_popup_x = main_frame.winfo_x() + r_sum_btn.winfo_x()
    r_s_popup_y = main_frame.winfo_y() + r_sum_btn.winfo_y()
    r_s_popup.geometry(f"{190}x{200}+{r_s_popup_x+125}+{r_s_popup_y-50}")
    # Input jumlah partisi
    n_txt = tkinter.Label(input_frame, text="n (amount of subdivisions)",
                          font="Arial, 12")
    n_entry = tkinter.Entry(input_frame, font="Arial, 12")
    n_txt.grid(row=1, column=0)
    n_entry.grid(row=2, column=0)

    # Input batas bawah
    low_lim_txt = tkinter.Label(input_frame, text="lower limit",
                                font="Arial, 12")
    low_lim_entry = tkinter.Entry(input_frame, font="Arial, 12")
    low_lim_txt.grid(row=3, column=0)
    low_lim_entry.grid(row=4, column=0)

    # Input batas atas
    upper_lim_txt = tkinter.Label(input_frame, text="upper limit",
                                  font="Arial, 12")
    upper_lim_entry = tkinter.Entry(input_frame, font="Arial, 12")
    upper_lim_txt.grid(row=5, column=0)
    upper_lim_entry.grid(row=6, column=0)
    popped_up = True

    # Tombol generate riemann
    r_gen_btn = tkinter.Button(input_frame, font="Arial, 12", text=
                               "Generate!", command=lambda: gen_riemann(n_entry.get(),
                                low_lim_entry.get(), upper_lim_entry.get(), area_label))
    r_gen_btn.grid(row=7, padx=50)
    # Label Hasil Luas
    area_label = tkinter.Label(input_frame, font="Arial, 12", text="Hasil = 0")
    area_label.grid(row=8, column=0, padx=50)
# = = = = = = = = =
# GENERATE GRAFIK ||
# = = = = = = = = =
def run():
    global OPTIONS
    check = False
    # baca ulang history
    OPTIONS = history_parser.read_from()
    # Bersihkan canvas
    GraphGen.turt2.clear()
    GraphGen.turt3.clear()
    GraphGen.riemann_called = False
    # Parsing fungsi dari input user
    fx = FuncParser.parse(list(fx_input.get()))
    # Simpan titik fungsi ke GraphGen
    GraphGen.points = fx
    # Gambar Grafik
    GraphGen.gen_graph(fx, GraphGen.zoom_amount)
    GraphGen.turt2.screen.update()
    GraphGen.screen.listen()
    # Validasi fungsi
    if len(fx) > 1000:  # length of the whole (x, y) cords should be more than 1k
        for l in range(10):
            if fx[l][1] is not None:
                # Jika Valid, simpan ke history
                check = True    # if within 10 y values there is a non-None, it's valid
        if check:
            history_parser.check_and_write(fx_input.get())
            update_options()

# Koneksi tombol & start
r_sum_btn.config(command=riemann_popup)
run_btn = tkinter.Button(main_frame, text="Generate Graph", font="Arial, 12",
                         width=15, command=run)

run_btn.grid(row=0, column=0, columnspan=2, sticky="W")

# Gambar grafik awal 
GraphGen.starting_graph()
#Jalankan loop Tkinter
root.mainloop()
