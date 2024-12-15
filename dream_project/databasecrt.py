import sqlite3

# verş tabanı ile bağlantı kurdum
conn = sqlite3.connect('ruyaanlamalari.db')
cursor = conn.cursor()

# verileri sorguladım
cursor.execute('SELECT * FROM ruyalar')
rows = cursor.fetchall()

# verilerden çikti aldım
for row in rows:
    print(f" {row[1]}, kelimesinin tabiri: {row[2]}, {row[1]} görmenin manası: {row[3]}")

# veri tabanı ile bağlantıyı kesitm
conn.close()

#merve kahya