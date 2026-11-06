# ========================================================
# 1-BOʻLIM: KUTUBXONALAR VA MODULLARNI IMPORT QILISH
# ========================================================
import os
import re
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

# Ma'lumotlar bazasi va HTML shablonlarini import qilamiz
# Diqqat: ai_model funksiyalari (Ollama) server xotirasini tejash uchun bu yerda o'chirildi!
from database import get_db_connection, baza_tizimini_yaratish
from templates import (
    INDEX_HTML, ABOUT_HTML, CONTACT_HTML, MAHSULOT_DETAL_HTML,
    KINOTEATR_HTML, YAZAR_EDITOR_HTML, MUALLIFLAR_HTML, MUTOLAA_HTML,
    KORZINKA_HTML, REGISTER_HTML, LOGIN_HTML
)

# ========================================================
# 2-BOʻLIM: FLASK ILOVASI VA FLASK-MAIL SOZLAMALARI
# ========================================================
# Tizim xotirasiga .env faylidagi elektron pochta maxfiy kalitlarini yuklaymiz
load_dotenv('API_KEY.env')

app = Flask(__name__)

# Ichki xavfsizlik kaliti (Sessiyalar xavfsizligi va xabarlar (flash) uchun shart)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'mening_flask_maxfiy_kalitim_123')

# Flask-Mail tizimi sozlamalari (Faqat xavfsiz va aniq SMTP parametrlari)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'alishertoshpulotov0701@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'epgjocpbofwfxeic')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
app.config['MAIL_SUPPRESS_SEND'] = False  

# Mail obyektini ilovaga bog'lab faollashtiramiz
mail = Mail(app)

# --- ASINXRON EMAIL YUBORISH TIZIMI ---
def asinxron_xat_yuborish(ilova_konteksti, msg):
    """ Xatni asosiy serverni qotirmasdan, orqa fonda yuborish funksiyasi """
    with ilova_konteksti:
        try:
            mail.send(msg)
        except Exception as e:
            print(f" Fondagi xat yuborishda xatolik: {str(e)}")

def xat_yubor(mavzu, qabul_qiluvchi, matn_html):
    """ Kod ichida xat yuborish uchun chaqiriladigan asosiy yengil funksiya """
    msg = Message(mavzu, recipients=[qabul_qiluvchi])
    msg.html = matn_html
    
    # Flask ilovasi kontekstini nusxalab, yangi oqim (Thread) ichiga uzatamiz
    ilova_konteksti = app.app_context()
    Thread(target=asinxron_xat_yuborish, args=(ilova_konteksti, msg)).start()

# ========================================================
# 3-BOʻLIM: BAZANI INICIALIZATSIYA QILISH VA VALIDATORLAR
# ========================================================
# Dastur yoqilishidan oldin ma'lumotlar bazasini avtomatik tekshirib yaratamiz
baza_tizimini_yaratish()

def telefon_to_grimi(nomer):
    """ 
    O'zbekiston telefon raqamlari formatini mukammal tekshirish.
    "+998 (90) 123-45-67" yoki "90 123 45 67" kabi har qanday formatni tozalaydi.
    """
    if not nomer:
        return False
    # Barcha bo'shliqlar, chiziqchalar va qavslarni tozalab tashlaymiz
    tozalangan_nomer = re.sub(r"[\s\-\(\)]", "", nomer.strip())
    # Tozalangan matn faqat to'g'ri raqamlardan iboratligini tekshiramiz
    return bool(re.match(r"^(\+?998)?\d{9}$", tozalangan_nomer))

def pochta_to_grimi(email):
    """ 
    Elektron pochta manzili formatini tekshirish.
    Kiritilgan matndagi ortiqcha bo'shliqlarni avtomatik tozalaydi.
    """
    if not email:
        return False
    tozalangan_email = email.strip().lower()
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", tozalangan_email))

# ========================================================
# 4-BOʻLIM: FOYDALANUVCHILAR TIZIMI (AUTH ROUTERLARI)
# ========================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ism = request.form.get('ism')
        email = request.form.get('email', '').strip().lower()
        parol = request.form.get('parol')
        
        if not pochta_to_grimi(email):
            flash("⚠️ Elektron pochta formati noto'g'ri!")
            return render_template_string(REGISTER_HTML)
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Kelajak uchun optimallashtirish: * o'rniga faqat 1 belgisini tekshiramiz (Tezkor qidiruv)
        cursor.execute("SELECT 1 FROM foydalanuvchilar WHERE email = ? LIMIT 1", (email,))
        if cursor.fetchone():
            conn.close()
            flash("⚠️ Bu elektron pochta allaqachon ro'yxatdan o'tgan!")
            return render_template_string(REGISTER_HTML)
            
        shifrlangan_parol = generate_password_hash(parol)
        cursor.execute("INSERT INTO foydalanuvchilar (ism, email, parol) VALUES (?, ?, ?)", (ism, email, shifrlangan_parol))
        conn.commit()
        conn.close()
        
        flash("🎉 Ro'yxatdan muvaffaqiyatli o'tdingiz! Tizimga kiring.")
        return redirect(url_for('login'))
    return render_template_string(REGISTER_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        parol = request.form.get('parol')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Faqat tekshirish va sessiya uchun kerakli bo'lgan ustunlarni olamiz
        cursor.execute("SELECT id, ism, parol FROM foydalanuvchilar WHERE email = ? LIMIT 1", (email,))
        foydalanuvchi = cursor.fetchone()
        conn.close()
        
        if foydalanuvchi and check_password_hash(foydalanuvchi['parol'], parol):
            session['user_id'] = foydalanuvchi['id']
            session['user_name'] = foydalanuvchi['ism']
            
            # Agar foydalanuvchi tizimga kirmasdan oldin savatga mahsulot qo'shgan bo'lsa, ularni saqlab qolamiz
            if 'korzinka' not in session:
                session['korzinka'] = []
                
            flash(f"👋 Xush kelibsiz, {foydalanuvchi['ism']}!", "success")
            return redirect(url_for('home'))
            
        flash("⚠️ Pochta yoki parol noto'g'ri!")
        return render_template_string(LOGIN_HTML)
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    # Faqat foydalanuvchi ma'lumotlarini o'chiramiz, session.clear() qilib savatni butunlay yo'qotmaymiz
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash("🔒 Tizimdan muvaffaqiyatli chiqdingiz.", "info")
    return redirect(url_for('home'))

# ========================================================
# 5-BOʻLIM: UMUMIY SAHIFALAR VA RESURSLAR KANALLARI
# ========================================================
@app.route('/')
def home():
    # URL'dan joriy sahifa raqamini olamiz (standart holatda 1-sahifa)
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Bitta sahifada ko'rinadigan maksimal mahsulotlar soni
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Jami mahsulotlar sonini aniqlaymiz (Pagination tugmalari uchun kerak)
    cursor.execute("SELECT COUNT(id) FROM mahsulotlar")
    total_products = cursor.fetchone()[0]
    total_pages = (total_products + per_page - 1) // per_page

    # Kelajak uchun optimallashtirish: '*' o'rniga faqat katalog sahifasida ko'rinadigan ustunlarni olamiz
    # LIMIT va OFFSET yordamida bazadan butun jadval emas, faqat kerakli 12 ta qator yuklanadi
    cursor.execute(
        "SELECT id, nomi, narxi, rasm, tur FROM mahsulotlar LIMIT ? OFFSET ?", 
        (per_page, offset)
    )
    baza_mahsulotlari = cursor.fetchall()
    conn.close()
    
    return render_template_string(
        INDEX_HTML, 
        mahsulotlar=baza_mahsulotlari, 
        current_page=page, 
        total_pages=total_pages
    )

@app.route('/about')
def about():
    return render_template_string(ABOUT_HTML)

@app.route('/kinoteatr')
def kinoteatr():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Faqat 'kino' turidagi mahsulotlar sonini aniqlaymiz
    cursor.execute("SELECT COUNT(id) FROM mahsulotlar WHERE tur = 'kino'")
    total_kinolar = cursor.fetchone()[0]
    total_pages = (total_kinolar + per_page - 1) // per_page

    # Kinolarni ham bo'lib-bo'lib, faqat kerakli ustunlar bilan yuklaymiz
    cursor.execute(
        "SELECT id, nomi, narxi, rasm, tur FROM mahsulotlar WHERE tur = 'kino' LIMIT ? OFFSET ?", 
        (per_page, offset)
    )
    kino_mahsulotlari = cursor.fetchall()
    conn.close()
    
    return render_template_string(
        KINOTEATR_HTML, 
        kinolar=kino_mahsulotlari, 
        current_page=page, 
        total_pages=total_pages
    )

@app.route('/mahsulot/<int:m_id>')
def mahsulot_sahifasi(m_id):
    if 'user_id' not in session:
        flash("⚠️ Platformadagi kontentlardan foydalanish uchun avval tizimga kirishingiz shart!")
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    # Detal sahifasida mahsulotning barcha ma'lumotlari (tavsifi, fayl yo'li) kerakligi uchun '*' saqlanadi
    # Ortiqcha yuklamaning oldini olish va tezlik uchun LIMIT 1 qo'shildi
    cursor.execute("SELECT * FROM mahsulotlar WHERE id = ? LIMIT 1", (m_id,))
    tanlangan_mahsulot = cursor.fetchone()
    conn.close()
    
    if tanlangan_mahsulot:
        return render_template_string(MAHSULOT_DETAL_HTML, mahsulot=tanlangan_mahsulot)
    return "<h1>Fayl topilmadi!</h1>", 404

# ========================================================
# 6-BOʻLIM: SAVATCHA TIZIMI (KORZINKA ROUTERLARI)
# ========================================================
@app.route('/korzinka')
def korzinka():
    if 'user_id' not in session:
        flash("⚠️ Savatni ko'rish uchun avval tizimga kiring!")
        return redirect(url_for('login'))
        
    savat_idlar = session.get('korzinka', [])
    mahsulotlar = []
    
    if savat_idlar:
        conn = get_db_connection()
        cursor = conn.cursor()
        # SQL Injection xavfidan himoyalangan dinamik IN operatori
        formatlangan_idlar = ','.join(['?'] * len(savat_idlar))
        
        # Kelajak uchun optimallashtirish: * o'rniga faqat savatchada kerakli ustunlarni yuklaymiz
        cursor.execute(
            f"SELECT id, nomi, narxi, rasm, tur FROM mahsulotlar WHERE id IN ({formatlangan_idlar})", 
            savat_idlar
        )
        mahsulotlar = cursor.fetchall()
        conn.close()
        
    return render_template_string(KORZINKA_HTML, mahsulotlar=mahsulotlar)

@app.route('/savat/qoshish/<int:m_id>')
def savat_qoshish(m_id):
    if 'user_id' not in session:
        flash("⚠️ Savatdan foydalanish uchun avval tizimga kiring!")
        return redirect(url_for('login'))
        
    if 'korzinka' not in session:
        session['korzinka'] = []
        
    korzinka = session['korzinka']
    if m_id not in korzinka:
        korzinka.append(m_id)
        session['korzinka'] = korzinka
        # Flask ro'yxat ichidagi o'zgarishni xotirada aniq saqlashi uchun modified bayrog'ini yoqamiz
        session.modified = True
        flash("🎉 Mahsulot savatchaga qo'shildi!")
        
    # Foydalanuvchi qaysi sahifadan turib qo'shgan bo'lsa, o'sha sahifaning o'zida qoldiramiz
    return redirect(request.referrer or url_for('home'))

@app.route('/savat/ochirish/<int:m_id>')
def savat_ochirish(m_id):
    korzinka = session.get('korzinka', [])
    if m_id in korzinka:
        korzinka.remove(m_id)
        session['korzinka'] = korzinka
        session.modified = True
        flash("🗑️ Mahsulot savatdan olib tashlandi.")
    return redirect(url_for('korzinka'))

# ========================================================
# 7-BOʻLIM: INTERFAOL XIZMATLAR (ALOQA VA IJODXONA)
# ========================================================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        ism = request.form.get('ism')
        aloqa = request.form.get('aloqa', '').strip()
        xabar_matni = request.form.get('xabar')
        
        yaroqli = False
        turi = ""
        
        try:
            if "@" in aloqa:
                turi = "Elektron pochta"
                if pochta_to_grimi(aloqa): 
                    yaroqli = True
            else:
                turi = "Telefon raqam"
                if telefon_to_grimi(aloqa): # validatorimiz ichida avtomatik tozalanadi
                    yaroqli = True
        except Exception as e_validation:
            return render_template_string(CONTACT_HTML, error=True, xato_sababi=f"Tekshirishda xato: {str(e_validation)}")

        if not yaroqli:
            xato_matni = f"Kiritilgan {turi} haqiqiy emas! Qayta tekshiring."
            return render_template_string(CONTACT_HTML, error=True, xato_sababi=xato_matni)
        
        try:
            # 2-bo'limdagi asinxron xat_yubor funksiyasini chaqiramiz (Asosiy oqim qotmaydi)
            xat_body = f"Yuboruvchi: {ism}<br>Aloqa: {aloqa} ({turi})<br>Xabar:<br>{xabar_matni}"
            xat_yubor(f"MediaLend - Yangi Aloqa Xabari: {ism}", app.config['MAIL_USERNAME'], xat_body)
            
            return render_template_string(CONTACT_HTML, success=True)
        except Exception as e_mail:
            return render_template_string(CONTACT_HTML, error=True, xato_sababi=f"Email xatosi: {str(e_mail)}")
            
    return render_template_string(CONTACT_HTML)

@app.route('/yozish', methods=['GET', 'POST'])
def yozish():
    if 'user_id' not in session:
        flash("⚠️ Yangi asar yuklash uchun avval tizimga kirishingiz shart!")
        return redirect(url_for('login'))

    if request.method == 'POST':
        nomi = request.form.get('nomi')
        matn = request.form.get('matn')
        amal = request.form.get('amal')
        muallif = session.get('user_name')
        
        holat = 'qoralama' if amal == 'qoralama' else 'chop_etildi'
        
        # 1-bo'limda o'chirilgan AI funksiyasini faqat kerak bo'lganda (Lazy Import) chaqiramiz
        from ai_model import matn_janrini_bashorat_qil
        
        # Ollama AI so'rovi vaqt olishi mumkin, shuning uchun xatoliklar ushlanadi
        try:
            aniqlangan_janr = matn_janrini_bashorat_qil(matn) or "Noma'lum"
        except Exception:
            aniqlangan_janr = "Nasr" # Ollama o'chib qolsa, standart janr yoziladi

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO muallif_kitoblari (nomi, muallif, matn, tur, holat) VALUES (?, ?, ?, ?, ?)", 
            (nomi, muallif, matn, aniqlangan_janr, holat)
        )
        conn.commit()
        conn.close()
        
        flash(f"🚀 Asaringiz '{aniqlangan_janr}' janri bilan muvaffaqiyatli saqlandi!")
        return redirect(url_for('mualliflar'))
    return render_template_string(YAZAR_EDITOR_HTML)

@app.route('/mualliflar')
def mualliflar():
    # Sahifalash (Pagination) kelajakda mualliflar ko'payganda saytni qutqaradi
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Umumiy chop etilgan mualliflik kitoblari soni
    cursor.execute("SELECT COUNT(id) FROM muallif_kitoblari WHERE holat = 'chop_etildi'")
    total_books = cursor.fetchone()[0]
    total_pages = (total_books + per_page - 1) // per_page

    # 2. Xotirani tejash: 'matn' (ulkan tekst) ustunini bu yerda yuklamaymiz!
    cursor.execute(
        "SELECT id, nomi, muallif, tur FROM muallif_kitoblari WHERE holat = 'chop_etildi' ORDER BY id DESC LIMIT ? OFFSET ?", 
        (per_page, offset)
    )
    muallif_kitoblari = cursor.fetchall()
    conn.close()
    
    return render_template_string(
        MUALLIFLAR_HTML, 
        kitoblar=muallif_kitoblari, 
        current_page=page, 
        total_pages=total_pages
    )

@app.route('/mutolaa/<int:k_id>')
def mutolaa(k_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Kitob matni faqat foydalanuvchi aynan shu asarni o'qish tugmasini bosgandagina yuklanadi
    cursor.execute("SELECT * FROM muallif_kitoblari WHERE id = ? LIMIT 1", (k_id,))
    kitob = cursor.fetchone()
    conn.close()
    
    if kitob: 
        return render_template_string(MUTOLAA_HTML, kitob=kitob)
    return "<h1>Asar topilmadi!</h1>", 404

# ========================================================
# 8-BOʻLIM: ASINXRON OLLAMA AI ROUTE VA ILOVANI ISHGA TUSHIRISH
# ========================================================
# AI so'rovlari Flask asosiy oqimini muzlatib qo'ymasligi uchun alohida ishchi hovuz ochamiz
# max_workers=4 bir vaqtning o'zida 4 ta og'ir AI so'rovini fonga joylashtirish imkonini beradi
ai_executor = ThreadPoolExecutor(max_workers=4)

@app.route('/ai_yordamchi', methods=['POST'])
def ai_yordamchi_route():
    data = request.get_json() or {}
    matn = data.get('matn')
    tur = data.get('tur') # 'polishing' yoki 'outline'
    
    if not matn:
        return jsonify({"natija": "⚠️ Matn maydoni bo'sh!"}), 400
        
    # Og'ir AI funksiyalarini faqat kerak bo'lganda (Lazy Import) xotiraga chaqiramiz
    from ai_model import imlo_va_uslubni_tekshir, syujet_davomiyligini_yarat

    # Fondagi oqim ichida xavfsiz bajariladigan yordamchi ichki funksiya
    def ai_vazifasini_bajar(sorov_turi, matn_kontenti):
        try:
            if sorov_turi == 'polishing':
                return imlo_va_uslubni_tekshir(matn_kontenti)
            elif sorov_turi == 'outline':
                return syujet_davomiyligini_yarat(matn_kontenti)
            return "Xato: Noma'lum so'rov turi."
        except Exception as e_ai:
            return f"⚠️ Ollama AI bilan bog'lanishda kutilmagan xatolik: {str(e_ai)}"

    # Og'ir AI so'rovini hovuzga topshiramiz. Flask oqimi esa darhol bo'shab, boshqa mijozlarga xizmat qiladi
    kelajakdagi_javob = ai_executor.submit(ai_vazifasini_bajar, tur, matn)
    
    try:
        # Maksimal 45 soniya kutamiz. Agar Ollama javob bermasa, serverni qulashdan asrab timeout beradi
        javob = kelajakdagi_javob.result(timeout=45.0)
    except Exception:
        return jsonify({
            "natija": "⚠️ Sun'iy intellekt javob berish muddati tugadi. Iltimos, qisqaroq matn yozib, qayta urinib ko'ring."
        }), 504
        
    return jsonify({"natija": javob})

if __name__ == '__main__':
    # Tizim port konfiguratsiyasi va serverni ishga tushirish bloki
    # debug=True faqat lokal ishlab chiqish (development) uchun xizmat qiladi
    port = int(os.environ.get("PORT", 5002))
    app.run(debug=True, host='0.0.0.0', port=port) 

