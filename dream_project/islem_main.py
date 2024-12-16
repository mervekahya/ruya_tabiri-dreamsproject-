def kelimeduzenleme(metin):
    turkce_to_ascii = {
        'ç': 'c', 'Ç': 'c',
        'ğ': 'g', 'Ğ': 'g',
        'ı': 'i', 'İ': 'i',
        'ö': 'o', 'Ö': 'o',
        'ş': 's', 'Ş': 's',
        'ü': 'u', 'Ü': 'u'
    }
    
    # Çoğul ve türemiş kelimelerin köklerini bulmak için
    cogul_ekler = {
        'ler': '', 'lar': '',
        'lerle': '', 'larla': '',
        'leri': '', 'ları': ''
    }
    
    # Ek temizleme kuralları
    ek_kurallar = {
        'nin': '', 'nın': '', 'nun': '', 'nün': '',
        'in': '', 'ın': '', 'un': '', 'ün': '',
        'da': '', 'de': '', 'ta': '', 'te': '',
        'den': '', 'dan': '', 'ten': '', 'tan': '',
        'i': '', 'ı': '', 'u': '', 'ü': ''
    }
    
    # Metni küçük harfe çevir ve kelimelere ayır
    kelimeler = metin.lower().split()
    temiz_kelimeler = []
    
    for kelime in kelimeler:
        # Türkçe karakterleri dönüştür
        kelime = ''.join(turkce_to_ascii.get(karakter, karakter) for karakter in kelime)
        
        # Önce çoğul ekleri temizle
        for ek in sorted(cogul_ekler.keys(), key=len, reverse=True):
            if kelime.endswith(ek) and len(kelime) > len(ek) + 2:  # En az 2 harf kök olsun
                kelime = kelime[:-len(ek)]
                break
        
        # Sonra diğer ekleri temizle
        for ek in sorted(ek_kurallar.keys(), key=len, reverse=True):
            if kelime.endswith(ek) and len(kelime) > len(ek) + 2:
                kelime = kelime[:-len(ek)]
                break
        
        # Türemiş kelimeleri kontrol et
        if kelime.endswith('lik') or kelime.endswith('lik'):
            kelime = kelime[:-3]
        
        temiz_kelimeler.append(kelime)
    
    return ' '.join(temiz_kelimeler)
