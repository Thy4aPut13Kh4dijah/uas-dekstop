import tkinter as tk
from tkinter import messagebox
import sqlite3

# Koneksi dan setup database SQLite
conn = sqlite3.connect('music_list.db')
cursor = conn.cursor()

# Membuat tabel musik jika belum ada (menghapus kolom price dan stock)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS music (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT NOT NULL,
        genre TEXT NOT NULL
    )
''')
conn.commit()

# Fungsi untuk menambah musik
def add_music():
    title = entry_title.get()
    artist = entry_artist.get()
    genre = entry_genre.get()

    if title and artist and genre:
        cursor.execute('INSERT INTO music (title, artist, genre) VALUES (?, ?, ?)',
                       (title, artist, genre))
        conn.commit()
        refresh_data()
        entry_title.delete(0, tk.END)
        entry_artist.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        messagebox.showinfo("Info", "Lagu berhasil ditambahkan")
    else:
        messagebox.showwarning("Peringatan", "Isi semua kolom")

# Fungsi untuk menampilkan data musik ke dalam listbox
def refresh_data():
    cursor.execute('SELECT * FROM music')
    rows = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

# Fungsi untuk mencari musik berdasarkan judul
def search_music():
    query = entry_search.get()
    cursor.execute('SELECT * FROM music WHERE title LIKE ?', ('%' + query + '%',))
    rows = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

# Fungsi untuk menghapus musik yang dipilih
def delete_music():
    selected_item = listbox.curselection()
    if selected_item:
        item_id = listbox.get(selected_item[0]).split(" | ")[0]
        cursor.execute('DELETE FROM music WHERE id = ?', (item_id,))
        conn.commit()
        refresh_data()
        messagebox.showinfo("Info", "Lagu berhasil dihapus")
    else:
        messagebox.showwarning("Peringatan", "Pilih lagu yang ingin dihapus")

# Fungsi untuk mengedit musik yang dipilih
def edit_music():
    selected_item = listbox.curselection()
    if selected_item:
        item_id = listbox.get(selected_item[0]).split(" | ")[0]
        cursor.execute('SELECT title, artist, genre FROM music WHERE id = ?', (item_id,))
        music = cursor.fetchone()

        entry_title.delete(0, tk.END)
        entry_artist.delete(0, tk.END)
        entry_genre.delete(0, tk.END)

        entry_title.insert(0, music[0])
        entry_artist.insert(0, music[1])
        entry_genre.insert(0, music[2])

        button_add.grid_forget()

        def save_changes():
            new_title = entry_title.get()
            new_artist = entry_artist.get()
            new_genre = entry_genre.get()

            if new_title and new_artist and new_genre:
                cursor.execute('UPDATE music SET title = ?, artist = ?, genre = ? WHERE id = ?',
                               (new_title, new_artist, new_genre, item_id))
                conn.commit()
                refresh_data()
                entry_title.delete(0, tk.END)
                entry_artist.delete(0, tk.END)
                entry_genre.delete(0, tk.END)
                messagebox.showinfo("Info", "Lagu berhasil diubah")

                button_add.grid(row=4, column=0, padx=10, pady=10)
            else:
                messagebox.showwarning("Peringatan", "Isi semua kolom")

        button_save = tk.Button(root, text="Simpan Perubahan", command=save_changes, font=font, width=15)
        button_save.grid(row=4, column=1, padx=10, pady=10)
    else:
        messagebox.showwarning("Peringatan", "Pilih lagu yang ingin diubah")

# Setup UI untuk aplikasi CRUD Music List
root = tk.Tk()
root.title("Aplikasi Music List")
root.geometry("700x400")
root.configure(bg="#f0f0f0")
font = ("Arial", 12)

# Komponen form untuk menambah atau mengedit musik
label_title = tk.Label(root, text="Judul Lagu:", font=font, bg="#f0f0f0")
label_title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_title = tk.Entry(root, font=font)
entry_title.grid(row=0, column=1, padx=10, pady=10)

label_artist = tk.Label(root, text="Penyanyi:", font=font, bg="#f0f0f0")
label_artist.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_artist = tk.Entry(root, font=font)
entry_artist.grid(row=1, column=1, padx=10, pady=10)

label_genre = tk.Label(root, text="Genre:", font=font, bg="#f0f0f0")
label_genre.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_genre = tk.Entry(root, font=font)
entry_genre.grid(row=2, column=1, padx=10, pady=10)

label_search = tk.Label(root, text="Pencarian Lagu:", font=font, bg="#f0f0f0")
label_search.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_search = tk.Entry(root, font=font)
entry_search.grid(row=3, column=1, padx=10, pady=10)

# Tombol-tombol untuk CRUD dan pencarian
button_add = tk.Button(root, text="Tambah Lagu", command=add_music, font=font, width=15)
button_add.grid(row=4, column=0, padx=10, pady=10)

button_search = tk.Button(root, text="Cari", command=search_music, font=font, width=15)
button_search.grid(row=4, column=1, padx=10, pady=10)

button_delete = tk.Button(root, text="Hapus Lagu", command=delete_music, font=font, width=15)
button_delete.grid(row=5, column=0, padx=10, pady=10)

button_edit = tk.Button(root, text="Edit Lagu", command=edit_music, font=font, width=15)
button_edit.grid(row=5, column=1, padx=10, pady=10)

# Listbox untuk menampilkan data musik
listbox = tk.Listbox(root, width=80, height=10, font=font)
listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Tombol untuk menyegarkan data
button_refresh = tk.Button(root, text="Refresh Data", command=refresh_data, font=font, width=15)
button_refresh.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Menampilkan data awal
refresh_data()

# Menjalankan aplikasi
root.mainloop()

# Menutup koneksi ke database saat aplikasi ditutup
conn.close()
