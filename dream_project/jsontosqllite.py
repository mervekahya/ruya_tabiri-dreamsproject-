import json
import sqlite3

# JSON dosyasından verileri çekitm 
with open('ruyalarkayit.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# SQLite veri tabanını oluşturdumç.
conn = sqlite3.connect('ruyaanlamalari.db')
cursor = conn.cursor()

# "ruyalar" tablosunu yaptım
cursor.execute('''
CREATE TABLE IF NOT EXISTS ruyalar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kelime TEXT,
    tabir TEXT,
    detay TEXT
)
''')

# json --> sqllite veri aktarımı
for item in data['ruyalar']:
    cursor.execute('''
    INSERT INTO ruyalar (kelime, tabir, detay)
    VALUES (?, ?, ?)
    ''', (item['kelime'], item['tabir'], item['detay']))

# kayıt ettim ve bağlantıyı kapattım
conn.commit()
conn.close()

print("Veriler başarıyla SQLite veritabanına aktarıldı.")
 

#merve kahya