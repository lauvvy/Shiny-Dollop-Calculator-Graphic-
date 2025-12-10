# Membuat list parsed_list dengan 10 elemen awal bernilai "Empty"
# List ini berfungsi sebagai riwayat (history) grafik/fungsi
parsed_list = ["Empty"] * 10
#Variabel
j = 0

# Fungsi untuk MENULIS satu data fx ke file graph_history.txt
def write_into(fx):
    with open("graph_history.txt", "a") as f: # Mode "a" (append) → data ditambahkan di akhir file
        f.write(f"{fx}\n")

# Fungsi untuk MENGHAPUS karakter newline (\n) secara manual
# dari sebuah string baris
def split_manually(line):
    splitted = ""
    for i in line: 
        if i != "\n": #jika bukan new line
            splitted += i #tambahkan string baru
    return splitted

# Fungsi untuk MEMBACA isi file graph_history.txt
# lalu menyimpannya ke dalam parsed_list
def read_from():
    i = 0
    with open("graph_history.txt", "r") as f:
        lines = f.readlines() #membaca semua baris file
        for line in lines:
            if i < len(parsed_list): # agar tidak melebihi ukuran list
                parsed_list[i] = split_manually(line)
                i += 1
    return parsed_list

# Fungsi untuk:
# 1. Menyimpan fx baru
# 2. Menggeser isi parsed_list
# 3. Menulis ulang seluruh riwayat ke file
def check_and_write(fx):
    # Menulis fx ke file
    write_into(fx)
    # Membuka file dengan mode "w" (write)
    # Mode ini MENGHAPUS seluruh isi file
    with open("graph_history.txt", "w"):
        # Menggeser elemen parsed_list ke kanan
        update_elements(parsed_list)
        # Menyimpan fx terbaru di index 0 
        parsed_list[0] = fx
    # Menulis ulang semua isi parsed_list ke file
    for lines in parsed_list:
        if lines != "": # hanya menulis data yang tidak kosong
            write_into(lines)

# Elemen terakhir hilang, elemen sebelumnya bergeser
def update_elements(fx):    # Fungsi untuk MENGGESER elemen list ke kanan
    for i in range(9, 0, -1):  # parsed list len - 1
        fx[i] = fx[i-1]
