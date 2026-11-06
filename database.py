# ========================================================
# DATABASE.PY - MUKAMMAL optimallashtirilgan BAZA TIZIMI
# ========================================================
import sqlite3

# main.py fayli bilan muvofiqlikni ta'minlash uchun platforma.db qilinadi
DB_FILE = "platforma.db"

def get_db_connection():
    """ Ma'lumotlar bazasi bilan xavfsiz bog'lanish yaratish xizmati """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Natijalarni lug'at (dict) ko'rinishida olish uchun
    return conn

def baza_tizimini_yaratish():
    """ Jadvallarni shakllantirish va boshlang'ich ma'lumotlarni kiritish """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Mahsulotlar (Katalog) jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mahsulotlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomi TEXT NOT NULL,
        tavsifi TEXT,
        narxi TEXT,
        rasm TEXT,
        tur TEXT,
        fayl TEXT
    )""")
    
    # 2. Mualliflar onlayn asarlari jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS muallif_kitoblari (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomi TEXT NOT NULL,
        muallif TEXT NOT NULL,
        matn TEXT NOT NULL,
        tur TEXT DEFAULT 'kitob',
        holat TEXT DEFAULT 'chop_etildi'
    )""")
    
    # 3. Foydalanuvchilar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS foydalanuvchilar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        parol TEXT NOT NULL,
        sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # --- KELAJAK UCHUN RAQAMLI INDEKSLAR (INDEXING) ---
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_foydalanuvchilar_email ON foydalanuvchilar(email);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_muallif_kitoblari_holat ON muallif_kitoblari(holat);")
    
    # === KATALOGNI HAR SAFAR AVTOMATIK YANGILASH STRATEGIYASI ===
    # Eski jadval ma'lumotlarini tozalab, yangi ro'yxatni bazaga yozamiz
    cursor.execute("DELETE FROM mahsulotlar")
    
    boshlangich_mahsulotlar = [
        # === 📚 KITOB TOIFASI ===
        ("Da Vinchi siri (The Da Vinci Code)", "Den Braunning dunyoga mashhur asari. Professor Robert Lengdon Luvr muzeyidagi qotillik sirlari va qadimiy ramzlar ortidan quvadi.", "40,000 so'm", "/static/images/images (1).jpg", "kitob", "/static/books/Davinchisiri.pdf"),
        ("Farishtalar va Shaytonlar (Angels & Demons)", "Illyuminatlar maxfiy jamiyati, Vatikan sirlari og'ushida kechuvchi o'ta hayajonli detektiv sarguzasht.", "38,000 so'm", "/static/images/farishtalar_shatyonlar.jpg", "kitob", "/static/books/Farishtalar va Shaytonlar.pdf"),
        ("Ibtido (Origin)", "Robert Lengdon ishtirokidagi navbatdagi daho asar. Insoniyat qayerdan paydo bo'lgan va qayerga ketyapti degan savollarga kiber-texnologiyalar orqali javob izlanadi.", "45,000 so'm", "/static/images/images (2).jpg", "kitob", "/static/books/Ibtido.pdf"),
        ("Qizil ajdarho (Red Dragon)", "Tomas Harrisning mashhur asari. Mashhur va aqlli manyak Gannibal Lekter hamda uni tutishga urinayotgan FQB agenti Uill Grem qarshiligi.", "35,000 so'm", "/static/images/images (4).jpg", "kitob", "/static/books/Qizil ajdarho.pdf"),
        ("Qo'zichoqlar sukunati (The Silence of the Lambs)", "Psixologik triller durdonasi. Yosh FQB tinglovchisi Klarisa Sterling boshqa bir qotilni topish uchun Gannibal Lekter yordamiga muhtoj bo'ladi.", "37,000 so'm", "/static/images/images.jpg", "kitob", "/static/books/Qo'zichoqlar sukunati.pdf"),
        ("Raqamli qal'a (Digital Fortress)", "Den Braunning ilk romani. Milliy xavfsizlik agentligi, superkompyuterlar va buzib bo'lmas kiber-kod atrofidagi xavfli o'yinlar.", "35,000 so'm", "/static/images/images (13).jpg", "kitob", "/static/books/Raqamli qal'a.pdf"),
        ("Kitob oʻgʻrisi (The book thief)", "Yosh qizning kitoblar orqali o'zini tushuntirish va hayotini tushuntirish uchun yozilgan hikoya.", "50,000 so'm", "/static/images/kitob_ogrisi.jpg", "kitob", "/static/books/kitob_ogrisi.pdf"),
        # === 🎬 KINO TOIFASI ===
        ("Xavfli topshiriq", "Kutilmagan burilishlar va yuqori adrenalinli sahnalarga boy o'tkir syujetli jangari va tarixiy film.", "free!", "/static/images/kino1.jpg", "kino", "/static/movies/kino1.mp4"),
        ("Da Vinchi siri (Film)", "#Detektiv #Sarguzasht. Den Braunning romani asosida ishlangan, Luvr muzeyidagi sirlar va qadimiy ramzlarni ochib beruvchi vizual durdona.", "free!", "/static/images/images (1).jpg", "kino", "/static/movies/Davinchi_Kodi.mp4"),
        ("Sherlok Xolms 2009", "#Mantiq #Kriminal. London ko'chalaridagi eng chalkash va sirli jinoyatlarny aql bovar qilmas deduksiya usuli bilan fosh etuvchi daho izquvar sarguzashtlari.", "free!", "/static/images/10197166.jpg", "kino", "/static/movies/Sherlok_Xolms_720.mp4")
    ]
    
    cursor.executemany("""
        INSERT INTO mahsulotlar (nomi, tavsifi, narxi, rasm, tur, fayl) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, boshlangich_mahsulotlar)

    # Xotira kitoblarini tekshirib boshlang'ich ijod namunasini kiritish
    cursor.execute("SELECT COUNT(*) FROM muallif_kitoblari")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO muallif_kitoblari (nomi, muallif, matn, tur, holat)
            VALUES ('Mening Ilk Romanim', 'Jasur ijodkor', '<p>Bu platformada yozilgan ilk kitob variantidir.</p>', 'Detektiv', 'chop_etildi')
        """)
        
    conn.commit()
    conn.close()
    print("🤖 Baza tizimi muvaffaqiyatli yangilandi va yangi kitob katalogga qo'shildi!")
