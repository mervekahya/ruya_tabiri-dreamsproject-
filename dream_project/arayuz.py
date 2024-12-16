import os
import tkinter as tk
from tkinter import messagebox, Toplevel
from time import sleep
from PIL import Image, ImageTk  # Pillow kütüphanesi
from islem_main import kelimeduzenleme  # islem.py yerine islem_main.py'den import ediyoruz
from veritabani import yorum_bul  # Bu satırı ekleyin
from nlp_islem import yorumlari_birlestir

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
    kelimeler = duzenlenmis_ruya.split()
    
    # Debug logları ekleyelim
    print("Düzenlenmiş kelimeler:", kelimeler)
    
    yorumlar = yorum_bul(kelimeler)
    
    # Yorum sonuçlarını kontrol edelim
    print("Bulunan yorumlar:", yorumlar)
    
    if yorumlar:
        yorum_penceresi = Toplevel()
        yorum_penceresi.title("Rüya Yorumu")
        yorum_penceresi.geometry("600x500")
        yorum_penceresi.configure(bg="#4B0082")
        
        # Başlık ekle
        baslik = tk.Label(
            yorum_penceresi,
            text="Rüyanızın Yorumu",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#4B0082"
        )
        baslik.pack(pady=10)
        
        # Scroll bar ekle
        scroll = tk.Scrollbar(yorum_penceresi)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Yorum metni için text widget'ı
        yorum_text = tk.Text(
            yorum_penceresi,
            height=20,
            width=60,
            font=("Arial", 12),
            bg="white",
            fg="black",
            wrap=tk.WORD,
            yscrollcommand=scroll.set
        )
        yorum_text.pack(pady=20, padx=20)
        
        # Scrollbar'ı text widget'ına bağla
        scroll.config(command=yorum_text.yview)
        
        # NLP ile işlenmiş birleşik yorum
        birlesik_yorum = yorumlari_birlestir(yorumlar)
        
        # Yorumları ekle
        yorum_text.insert(tk.END, "Birleştirilmiş Yorum:\n\n")
        yorum_text.insert(tk.END, f"{birlesik_yorum}\n\n")
        yorum_text.insert(tk.END, "\nDetaylı Yorumlar:\n\n")
        for i, yorum in enumerate(yorumlar, 1):
            yorum_text.insert(tk.END, f"{i}. {yorum}\n\n")
        
        yorum_text.configure(state='disabled')
        
        # Kapat butonu
        kapat_buton = tk.Button(
            yorum_penceresi,
            text="Kapat",
            command=yorum_penceresi.destroy,
            bg="#800080",
            fg="white",
            font=("Arial", 12)
        )
        kapat_buton.pack(pady=10)
    else:
        messagebox.showinfo("Bilgi", "Bu rüya için yorum bulunamadı.")

def temizle_placeholder(event):
    if metin_girdisi.get("1.0", tk.END).strip() == "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...":
        metin_girdisi.delete("1.0", tk.END)
        metin_girdisi.config(fg="black")  # Değişiklik burada: white -> black

def ekle_placeholder(event):
    if not metin_girdisi.get("1.0", tk.END).strip():
        metin_girdisi.insert("1.0", "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...")
        metin_girdisi.config(fg="grey")

def arayuz_baslat():
    pencere = tk.Tk()
    pencere.title("Rüya Yorumlayıcı")
    pencere.geometry("600x400")

    galaksi_resmi = os.path.join(os.getcwd(), "dream_project/galaksi.png")
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
    metin_girdisi = tk.Text(pencere, height=7, width=50, font=("Arial", 12), fg="grey", bg="white")  # bg="white" eklendi
    metin_girdisi.insert("1.0", "Bugün rüyanda ne gördün bana anlat, senin için yorumlayayım...")
    metin_girdisi.bind("<FocusIn>", temizle_placeholder)
    metin_girdisi.bind("<FocusOut>", ekle_placeholder)
    metin_girdisi.pack(pady=20)

    duzenle_buton = tk.Button(
        pencere,
        text="Metni Düzenle ve Kaydet",
        command=metni_duzenle,
        bg="#800080",
        fg="white",
        font=("Arial", 12),
        relief=tk.RAISED
    )
    duzenle_buton.pack(pady=10)

    # Eski on_closing fonksiyonunu basitleştir
    def on_closing():
        pencere.destroy()
    
    pencere.protocol("WM_DELETE_WINDOW", on_closing)
    pencere.mainloop()

if __name__ == "__main__":
    arayuz_baslat()
