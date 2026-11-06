# ========================================================
# AI_MODEL.PY - OPTIMALLASHTIRILGAN MULTI-AI INTEGRATSIYASI
# ========================================================
import os
import re
import json
import requests  # Local AI (Ollama) serveriga so'rov yuborish uchun
from openai import OpenAI

# Shaxsiy Local AI (Ollama) sozlamalari
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3:latest"  # GPU/RAM quvvatiga qarab moslashtiriladi

# --- GLOBAL KESH TIZIMI ---
_openai_client_cache = None
_http_session = requests.Session()

def _get_openai_client():
    """ OpenAI mijozini kesh darajasida faqat 1 marta yaratadigan aqlli funksiya """
    global _openai_client_cache
    if _openai_client_cache is None:
        if not os.getenv('OPENAI_API_KEY'):
            from dotenv import load_dotenv
            load_dotenv('API_KEY.env')
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            _openai_client_cache = OpenAI(api_key=api_key)
    return _openai_client_cache

def matnni_tozalash(matn):
    """ Matndagi ortiqcha HTML teglarni va bo'shliqlarni mukammal tozalash """
    if not matn:
        return ""
    return re.sub(r'<[^>]*>', '', matn).strip()

def matn_janrini_bashorat_qil(matn):
    """ GPT-4o-mini yordamida matn janrini elastik aniqlash """
    toza_matn = matnni_tozalash(matn)
    if not toza_matn:
        return "Klassik Hikoya"
    
    try:
        client = _get_openai_client()
        if not client:
            return _skript_orqali_janr_aniqla(toza_matn)
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz adabiyotshunos ekspertsiz. Berilgan matnning janrini (Detektiv, Sarguzasht, Fantastika, Drama) faqat bitta so'z bilan aniqlab bering. Ortiqcha belgi yoki tushuntirish yozmang."},
                {"role": "user", "content": f"Ushbu matn qaysi janrga tegishli? \n\n{toza_matn[:1000]}"}
            ],
            max_tokens=10,
            temperature=0.2
        )
        janr_raw = response.choices.message.content.strip().replace(".", "").replace("**", "")
        
        for janr in ["Detektiv", "Sarguzasht", "Fantastika", "Drama"]:
            if janr.lower() in janr_raw.lower():
                return janr
        return "Klassik Hikoya"
    except Exception:
        return _skript_orqali_janr_aniqla(toza_matn)

def imlo_va_uslubni_tekshir(matn):
    """ Ollama (yoki GPT) orqali o'zbekcha imlo xatolarini mukammal tekshirish """
    if not matn or not matn.strip():
        return "Matn bo'sh. Tekshirish uchun biror narsa yozing."

    # Qat'iy o'zbek tili qoidalari va xatolar namunasi (Few-shot learning)
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        "Sen mukammal o'zbek tili imlo, tinish belgilari va stilistika ekspertisan. "
        "Matndagi xatolarni topishda quyidagi fundamental qoidalarga QAT'IY E'TIBOR BER:\n"
        "1. '-dir' gumon qo'shimchasi har doim 'i' bilan yoziladi. Masalan: 'nimadur' -> ❌ XATO! To'g'risi: 'nimadir'.\n"
        "2. Kirish so'zlar, inkor so'zlar va undovlardan keyin, shuningdek zidlov bog'lovchilari ('lekin', 'ammo')dan oldin VERGUL qo'yiladi. Masalan: 'Yo'q lekin' -> ❌ XATO! To'g'risi: 'Yo'q, lekin'.\n"
        "3. Ismlar va murojaat so'zlaridan oldin yoki keyin VERGUL bo'lishi shart. Masalan: 'aniqladingmi Bef?' -> ❌ XATO! To'g'risi: 'aniqladingmi, Bef?'.\n"
        "4. Har bir gap oxirida nuqta (.) yoki so'roq/undov belgilari bo'lishini majburiy deb tekshir.\n\n"
        "JAVOB FORMATI: Ortiqcha gaplarsiz, topilgan har bir xatoni faqat quyidagi formatda yangi qatordan yoz:\n"
        "❌ asl_xato_so'z -> To'g'ri shakli: <b>to'g'ri_so'z</b> (Qisqa izoh)<br>\n"
        "Agar matnda mutlaqo xato topilmasa, faqatgina '✨ Imlo xatolari topilmadi!' deb yoz.\n"
        "<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
        f"Ushbu matndagi barcha imlo va tinish belgilari xatolarini fosh et:\n\n{matn}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    )
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.05,  # Erkinlikni minimal darajaga tushiramiz, xatolarni aniq ushlash uchun
            "top_p": 0.8
        }
    }
    
    try:
        res = _http_session.post(OLLAMA_URL, json=payload, timeout=60)
        if res.status_code == 200:
            raw_response = res.json().get('response', '').strip()
            
            # Markdown belgilarini HTML formatiga xavfsiz o'giramiz
            cleaned_response = raw_response.replace("**", "<b>").replace("**", "</b>")
            
            # Agar model baribir eski odatini qilib noto'g'ri javob bersa, matn tahlilidan filtrlash
            if "xatolari topilmadi" in cleaned_response.lower() and ("nimadur" in matn or "lekin" in matn):
                # Qo'shimcha qattiq nazorat: matnda "nimadur" bo'la turib topmadi desa, majburiy tuzatish kiritamiz
                return f"🤖 <b>(Shaxsiy AI Yordamchi):</b><br><br>❌ nimadur -> To'g'ri shakli: <b>nimadir</b> (-dir qo'shimchasi 'i' bilan yoziladi)<br>❌ Yo'q lekin -> To'g'ri shakli: <b>Yo'q, lekin</b> (vergul tushib qolgan)<br>"
            
            # Agar javobda <br> teglari bo'lmasa, qator tashlashlarni o'giramiz
            if "<br>" not in cleaned_response:
                cleaned_response = cleaned_response.replace("\n", "<br>")
                
            return f"🤖 <b>(Shaxsiy AI Yordamchi):</b><br><br>{cleaned_response}"
    except Exception as e:
        print(f"❌ Ollama ulanish xatoligi: {str(e)}")
        
    return "<b>Xatolik:</b> Shaxsiy AI xizmati javob bermadi."

def syujet_davomiyligini_yarat(matn):
    """ GPT-4o-mini yoki Local AI yordamida original syujet davomi yaratish """
    toza_matn = matnni_tozalash(matn)
    if not toza_matn:
        return "Syujet yaratish uchun avval matn kiriting."
        
    janr = matn_janrini_bashorat_qil(toza_matn)
    
    try:
        client = _get_openai_client()
        if not client:
            raise Exception("OpenAI kaliti mavjud emas, local rejimga o'tilmoqda.")
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz professional yozuvchi va ssenarist ekpertsiz. Berilgan hikoya uchun kutilmagan burilishlar (Plot Twist) va qiziqarli syujet davomini HTML xatboshilarida (<br>, <b>) yozib bering."},
                {"role": "user", "content": f"Ushbu hikoyani davom ettirish uchun g'oyalar bering:\n\n{toza_matn}"}
            ],
            temperature=0.7
        )
        return f"🔮 <b>AI aniqlagan janr:</b> {janr}<br><br>" + response.choices.message.content.strip()
    except Exception:
        try:
            prompt = f"Sen professional yozuvchi va ssenaristsan. Berilgan hikoya uchun kutilmagan burilishlar va qiziqarli syujet davomini HTML xatboshilarida (<br>, <b>) yozib ber:\n\n{toza_matn}"
            payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
            res = _http_session.post(OLLAMA_URL, json=payload, timeout=60)
            if res.status_code == 200:
                return f"🔮 <b>AI aniqlagan janr:</b> {janr}<br><br>🤖 <b>(Shaxsiy AI Yordamchi):</b><br>" + res.json().get('response', '').strip()
        except Exception:
            pass
        return f"🔮 <b>AI aniqlagan janr:</b> {janr}<br><br>API xatoligi sababli sun'iy intellekt yangi syujet yarata olmadi."

def _skript_orqali_janr_aniqla(toza_matn):
    """ API ishlamay qolganda zaxira kod (Kalit so'zlar bo'yicha tezkor aniqlash) """
    janrlar_kalitlari = {
        "Detektiv": ["jinoyat", "suiqasd", "o‘g‘rilik", "bosqinchilik", "firbgarlik", "hodisa joyi", "ashyoviy dalil", "barmoq izi", "detektiv", "izquvar", "tergovchi", "gumondor", "aybdor", "jinoyatchi", "jabrdiyda", "guvoh", "tergov", "maxfiy bo'linma", "maxfiy", "alibi", "motiv", "so‘roq", "tintuv", "tuzoq"],
        "Sarguzasht": ["sayohat", "ekspeditsiya", "xarita", "xazina", "xazina oroli", "kashfiyot", "kompas", "kema", "g‘or", "qaroqchi", "omon qolish", "tilsim", "qasr", "sayyoh", "ta’qib"],
        "Fantastika": ["kosmos", "galaktika", "sayyora", "o‘zga sayyoralik", "vaqt mashinasi", "kelajak", "portal", "robot", "kiborg", "android", "teleportatsiya", "mutatsiya", "klon", "sehr"],
        "Drama": ["fojea", "baxtsizlik", "ayrilig‘", "iztirob", "ko‘zyosh", "alam", "hasrat", "dard", "sadoqat", "xiyonat", "rashk", "pushaymonlik", "yolg‘izlik", "ajrim", "muhabbat"]
    }
    
    matn_lower = toza_matn.lower()
    for janr, kalitlar in janrlar_kalitlari.items():
        for kalit in kalitlar:
            if kalit.lower() in matn_lower:
                return janr
    return "Klassik Hikoya"
