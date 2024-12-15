import os
import tkinter as tk
from tkinter import messagebox, Toplevel
from time import sleep
from PIL import Image, ImageTk  # Pillow kütüphanesi
from islem_main import kelimeduzenleme  # islem.py yerine islem_main.py'den import ediyoruz

def bekleme_ekrani():
    bekleme_penceresi = Toplevel()
    bekleme_penceresi.title("Lütfen Bekleyin")
    bekleme_penceresi.geometry("400x200")
    bekleme_penceresi.configure(bg="#4B0082")
    bekleme_penceresi.resizable(False, False)

    bekleme_yazisi = tk.Label(
        bekleme_penceresi,
        text="Rüyanı yorumluyorum... biraz bekle!",
        font=("Arial", 14, "bold"),
        fg="white",
        bg="#4B0082"
    )
    bekleme_yazisi.pack(pady=20)

    kum_saati = tk.Label(bekleme_penceresi, text="⌛", font=("Arial", 50), fg="lightgrey", bg="#4B0082")
    kum_saati.pack(pady=10)

    bekleme_penceresi.update()
    sleep(3)
    bekleme_penceresi.destroy()

def metni_duzenle(event=None):
    gorulen_ruya = metin_girdisi.get("1.0", tk.END).strip()
    if not gorulen_ruya or gorulen_ruya == "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...":
        messagebox.showwarning("Uyarı", "Lütfen bir metin girin.")
        return

    bekleme_ekrani()

    duzenlenmis_ruya = kelimeduzenleme(gorulen_ruya)
    karakter_listesi = list(duzenlenmis_ruya)

    output_file = os.path.join(os.getcwd(), "islenen_metin.txt")
    with open(output_file, "w") as dosya:
        dosya.write(f"Dönüştürülmüş Metin: {duzenlenmis_ruya}\n")
        dosya.write(f"Karakter Listesi: {karakter_listesi}\n")

    messagebox.showinfo("Bilgi", f"Metin başarıyla düzenlendi ve dosyaya kaydedildi.\nDosya: {output_file}")

def temizle_placeholder(event):
    if metin_girdisi.get("1.0", tk.END).strip() == "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...":
        metin_girdisi.delete("1.0", tk.END)
        metin_girdisi.config(fg="white")

def ekle_placeholder(event):
    if not metin_girdisi.get("1.0", tk.END).strip():
        metin_girdisi.insert("1.0", "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...")
        metin_girdisi.config(fg="grey")

def arayuz_baslat():
    pencere = tk.Tk()
    pencere.title("Rüya Yorumlayıcı")
    pencere.geometry("600x400")

    galaksi_resmi = os.path.join(os.getcwd(), "galaksi.png")
    if os.path.exists(galaksi_resmi):
        orijinal_resim = Image.open(galaksi_resmi)
        yeniden_boyutlandirilmis_resim = orijinal_resim.resize((600, 400), Image.Resampling.LANCZOS)
        arkaplan_resmi = ImageTk.PhotoImage(yeniden_boyutlandirilmis_resim)
        arkaplan_label = tk.Label(pencere, image=arkaplan_resmi)
        arkaplan_label.image = arkaplan_resmi  # Referansı kaybetmemek için
        arkaplan_label.place(relwidth=1, relheight=1)
    else:
        pencere.configure(bg="#2E2E2E")

    baslik = tk.Label(pencere, text="Rüya Yorumlayıcı", font=("Arial", 16, "bold"), fg="white", bg="#4B0082")
    baslik.pack(pady=10)

    global metin_girdisi
    metin_girdisi = tk.Text(pencere, height=7, width=50, font=("Arial", 12), fg="grey")
    metin_girdisi.insert("1.0", "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...")
    metin_girdisi.bind("<FocusIn>", temizle_placeholder)
    metin_girdisi.bind("<FocusOut>", ekle_placeholder)
    metin_girdisi.pack(pady=20)

    duzenle_buton = tk.Button(
        pencere,
        text="Metni Düzenle ve Kaydet",
        command=metni_duzenle,
        bg="#800080",
        fg="purple",
        font=("Arial", 12),
        relief=tk.RAISED
    )
    duzenle_buton.pack(pady=10)

    pencere.mainloop()

if __name__ == "__main__":
    arayuz_baslat()
