import sqlite3

def veritabani_baglantisi():
    return sqlite3.connect('ruyaanlamlari.db')

def tablo_olustur():
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS kelime_detay (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kelime TEXT NOT NULL,
        detay TEXT NOT NULL
    )''')
    
    # Daha fazla örnek veri ekleyelim
    ornek_veriler = [
        ('kedi', 'Rüyada kedi görmek, size zarar vermek isteyen birine işarettir.'),
        ('deniz', 'Rüyada deniz görmek, huzur ve mutluluğa kavuşacağınıza işarettir.'),
        ('sandal', 'Rüyada sandal görmek, yeni bir yolculuğa çıkacağınıza işarettir.'),
        ('yuvarlan', 'Rüyada yuvarlanmak, hayatınızda kontrolü kaybetme korkusuna işarettir.'),
        ('kelebek', 'Rüyada kelebek görmek, güzel haberler alacağınıza işarettir.'),
        ('hazine', 'Rüyada hazine bulmak, yakın zamanda maddi kazanç elde edeceğinizi gösterir.'),
        ('kurt', 'Rüyada kurt görmek, güçlü düşmanlarınız olduğuna işaret eder.'),
        ('kule', 'Rüyada kule görmek, yüksek mevkilere geleceğinize işarettir.'),
        ('deve', 'Rüyada deve görmek, sabır ve dayanıklılık gerektiren bir süreçte olduğunuzu gösterir.'),
        ('orak', 'Rüyada orak görmek, emeklerinizin karşılığını alacağınıza işarettir.')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO kelime_detay (kelime, detay) VALUES (?, ?)', ornek_veriler)
    conn.commit()
    conn.close()

def yorum_bul(kelimeler):
    from nlp_islem import kelime_kokunu_bul
    
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    bulunan_yorumlar = []
    islenen_kelimeler = set()
    
    print("\nVeritabanı sorgusu başlıyor...")
    
    for kelime in kelimeler:
        if kelime.lower() in ['ve', 'ile', 'bir', 'da', 'de', 'den', 'i']:
            continue
            
        kelime = kelime.lower().strip()
        kok = kelime_kokunu_bul(kelime)
        
        print(f"\nAranan kelime: '{kelime}', Kök: '{kok}'")
        
        # Basitleştirilmiş sorgu
        cursor.execute('''
            SELECT * FROM kelime_detay 
            WHERE lower(kelime) IN (?, ?)
            OR ? LIKE lower(kelime) || '%'
            OR ? LIKE lower(kelime) || '%'
        ''', (kelime, kok, kelime, kok))
        
        sonuc = cursor.fetchone()
        
        if sonuc and sonuc[1] not in islenen_kelimeler:
            islenen_kelimeler.add(sonuc[1])
            yorum = f"{sonuc[1]}: {sonuc[2]}"
            bulunan_yorumlar.append(yorum)
            print(f"Eşleşme bulundu: {sonuc[1]}")
        else:
            # İkinci bir deneme - daha esnek eşleştirme
            cursor.execute('''
                SELECT * FROM kelime_detay 
                WHERE lower(kelime) LIKE ?
                OR lower(kelime) LIKE ?
            ''', (f"%{kelime}%", f"%{kok}%"))
            
            sonuc = cursor.fetchone()
            if sonuc and sonuc[1] not in islenen_kelimeler:
                islenen_kelimeler.add(sonuc[1])
                yorum = f"{sonuc[1]}: {sonuc[2]}"
                bulunan_yorumlar.append(yorum)
                print(f"Eşleşme bulundu: {sonuc[1]}")
            else:
                print(f"'{kelime}' için yorum bulunamadı")
    
    conn.close()
    return bulunan_yorumlar

def test_veritabani():
    try:
        conn = veritabani_baglantisi()
        cursor = conn.cursor()
        # Tablo yapısını kontrol et
        cursor.execute("PRAGMA table_info(kelime_detay)")
        columns = cursor.fetchall()
        print("Tablo yapısı:", columns)
        
        # Örnek bir sorgu
        cursor.execute("SELECT * FROM kelime_detay LIMIT 1")
        ornek = cursor.fetchone()
        print("Örnek veri:", ornek)
        
        conn.close()
    except Exception as e:
        print(f"Hata: {e}")

def test_veri_ekle():
    """Test verileri eklemek için yardımcı fonksiyon"""
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    
    # Veritabanını temizle
    cursor.execute('DELETE FROM kelime_detay')
    
    # Test verilerini ekle
    test_veriler = [
        ('kedi', 'Rüyada kedi görmek, size zarar vermek isteyen birine işarettir.'),
        ('deniz', 'Rüyada deniz görmek, huzur ve mutluluğa kavuşacağınıza işarettir.'),
        ('sandal', 'Rüyada sandal görmek, yeni bir yolculuğa çıkacağınıza işarettir.'),
        ('yolculuk', 'Rüyada yolculuk yapmak, hayatınızda yeni başlangıçlar olacağına işarettir.'),
        ('gör', 'Rüyada bir şey görmek, yakında önemli bir olayla karşılaşacağınıza işarettir.')
    ]
    
    cursor.executemany('INSERT INTO kelime_detay (kelime, detay) VALUES (?, ?)', test_veriler)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    tablo_olustur()
    test_veri_ekle()  # Test verilerini ekle
    test_veritabani()
