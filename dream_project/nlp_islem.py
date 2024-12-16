from TurkishStemmer import TurkishStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

stemmer = TurkishStemmer()

def kelime_kokunu_bul(kelime):
    stemmer = TurkishStemmer()
    return stemmer.stem(kelime)

def yorumlari_birlestir(yorumlar):
    """Yorumları anlamlı bir şekilde birleştirir."""
    if not yorumlar:
        return "Rüyanız için yorum bulunamadı."
    
    birlesik_metin = "Rüyanızın genel yorumu:\n\n"
    
    # Yorumlardan kelimeleri ve açıklamaları ayır
    for yorum in yorumlar:
        kelime, aciklama = yorum.split(':', 1)
        birlesik_metin += f"• {aciklama.strip()}\n"
    
    return birlesik_metin
