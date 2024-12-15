def kelimeduzenleme(metin):
    turkce_to_ascii = {
        'ç': 'c', 'Ç': 'c',
        'ğ': 'g', 'Ğ': 'g',
        'ı': 'i', 'İ': 'i',
        'ö': 'o', 'Ö': 'o',
        'ş': 's', 'Ş': 's',
        'ü': 'u', 'Ü': 'u'
    }
    return ''.join(turkce_to_ascii.get(karakter, karakter) for karakter in metin).lower()
