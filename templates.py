INDEX_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <!-- Google Search Console tasdiqlash kodi -->
    <meta name="google-site-verification" content="geFdhlqFqWC7cdKBlYr_ncuSIwJ6R0DFoz-c6xsGAzA" />
    <title>MediaLend - Bosh sahifa</title>
    <style> 
        body { font-family: sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        h1 { text-align: center; margin-top: 30px; color: #fff; }
        .konteyner { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; padding: 30px; }
        .karta { background: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); text-align: center; width: 280px; display: flex; flex-direction: column; min-height: 420px; box-sizing: border-box; border: 1px solid #334155; position: relative; }
        .karta img { width: 100%; height: 180px; object-fit: contain; background-color: #1e293b; border-radius: 6px; }
        .narx { color: #38bdf8; font-size: 1.3rem; font-weight: bold; display: block; margin: 15px 0; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; background: #334155; color: #cbd5e1; margin-top: 10px; align-self: center; }
        .tugma { background-color: #0284c7; color: white; border: none; padding: 12px 20px; border-radius: 6px; width: 100%; cursor: pointer; font-size: 1rem; font-weight: bold; text-decoration: none; display: block; box-sizing: border-box; margin-top: auto; text-align: center; transition: background 0.2s; }
        .tugma:hover { background-color: #0369a1; }
        
        /* Sahifalash (Pagination) Dizayni */
        .pagination { display: flex; justify-content: center; align-items: center; gap: 10px; margin: 40px 0; padding-bottom: 20px; }
        .page-link { background-color: #1e293b; color: #94a3b8; border: 1px solid #334155; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: bold; transition: all 0.3s; }
        .page-link:hover { background-color: #334155; color: #38bdf8; border-color: #38bdf8; }
        .page-active { background-color: #0284c7; color: white; border-color: #0284c7; padding: 10px 18px; border-radius: 6px; font-weight: bold; }
        .page-disabled { background-color: #0f172a; color: #475569; border: 1px solid #1e293b; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    
    <h1>Kutubxona va Hordiq Platformasiga xush kelibsiz!</h1>
    
    <div class="konteyner">
        {% for mahsulot in mahsulotlar %}
        <div class="karta">
            <img src="{{ mahsulot.rasm }}" alt="{{ mahsulot.nomi }}" loading="lazy" onerror="this.src='https://placehold.co'">
            <h3>{{ mahsulot.nomi }}</h3>
            <div class="badge">
                {% if mahsulot.tur == 'kino' %} 🎬 Film 
                {% else %} 📖 Kitob / Asar 
                {% endif %}
            </div>
            <span class="narx">{{ mahsulot.narxi }}</span>
            <a href="/mahsulot/{{ mahsulot.id }}" class="tugma">
                {% if mahsulot.tur == 'kino' %} 🎬 Tomosha qilish 
                {% else %} 📖 Batafsil ko'rish 
                {% endif %}
            </a>
        </div>
        {% endfor %}
    </div>

    <!-- DINAMIK SAHIFALASH TIZIMI -->
    {% if total_pages > 1 %}
    <div class="pagination">
        {% if current_page > 1 %}
            <a href="/?page={{ current_page - 1 }}" class="page-link">⬅️ Oldingi</a>
        {% else %}
            <span class="page-disabled">⬅️ Oldingi</span>
        {% endif %}

        {% for p in range(1, total_pages + 1) %}
            {% if p == current_page %}
                <span class="page-active">{{ p }}</span>
            {% else %}
                <a href="/?page={{ p }}" class="page-link">{{ p }}</a>
            {% endif %}
        {% endfor %}

        {% if current_page < total_pages %}
            <a href="/?page={{ current_page + 1 }}" class="page-link">Keyingi ➡️</a>
        {% else %}
            <span class="page-disabled">Keyingi ➡️</span>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""


ABOUT_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Biz haqimizda - MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 0; text-align: center; }
        .navbar { background-color: #1e293b; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .kontent { background: #1e293b; max-width: 800px; margin: 50px auto; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1px solid #334155; }
        .afzalliklar { display: flex; gap: 20px; margin-top: 30px; flex-wrap: wrap; justify-content: center; }
        .afzallik-karta { flex: 1; min-width: 200px; background: #111827; padding: 20px; border-radius: 8px; border: 1px solid #334155; text-align: left; }
        .afzallik-karta h3 { margin-top: 0; color: #38bdf8; }
        .afzallik-karta p { color: #94a3b8; margin-bottom: 0; }
        .ortga-tugma { display: inline-block; margin-top: 40px; padding: 12px 30px; background-color: #0284c7; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; transition: background 0.2s; }
        .ortga-tugma:hover { background-color: #0369a1; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="kontent">
        <h1>Biz haqimizda</h1>
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">Biz raqamli madaniyat ekotizimimiz. Bu yerda siz do'kon xizmatlaridan foydalanishingiz, kino ko'rib dam olishingiz va o'z asaringizni yaratishingiz mumkin.</p>
        <div class="afzalliklar">
            <div class="afzallik-karta"><h3>⚡ Tezkor</h3><p>Hordiq va mutolaa bir xil tezlikda, bitta joyda.</p></div>
            <div class="afzallik-karta"><h3>📝 Erkinlik</h3><p>Hech qanday cheklovlarsiz o'z kitoblaringizni yozing!</p></div>
        </div>
        <a href="/" class="ortga-tugma">⬅ Bosh sahifaga qaytish</a>
    </div>
</body>
</html>
"""

CONTACT_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Aloqa - MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .kontent { background: #1e293b; max-width: 650px; margin: 50px auto; padding: 40px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        input, textarea { width: 100%; padding: 12px; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 6px; box-sizing: border-box; margin: 5px 0 15px 0; transition: border-color 0.3s; }
        input:focus, textarea:focus { border-color: #38bdf8; outline: none; }
        .yuborish-tugma { background-color: #0284c7; color: white; padding: 14px; width: 100%; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 1rem; transition: background 0.2s; }
        .yuborish-tugma:hover { background-color: #0369a1; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="kontent">
        <h1>Biz bilan bog'lanish</h1>
        {% if success %}
        <div style="background: rgba(34, 197, 94, 0.2); color: #22c55e; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 15px; border: 1px solid #22c55e;">🎉 Xabaringiz muvaffayatli yuborildi!</div>
        {% endif %}
        {% if error %}
        <div style="background: rgba(244, 63, 94, 0.2); color: #f43f5e; padding: 12px; border-radius: 6px; text-align: center; font-weight: bold; margin-bottom: 15px; border: 1px solid #f43f5e;">⚠️ Xatolik! {{ xato_sababi }}</div>
        {% endif %}
        <form action="/contact" method="POST">
            <label>Ismingiz:</label>
            <input type="text" name="ism" value="{{ session.get('user_name', '') }}" required>
            <label>Email yoki Telefon:</label>
            <input type="text" name="aloqa" placeholder="example@mail.com yoki +998901234567" required>
            <label>Xabaringiz:</label>
            <textarea rows="4" name="xabar" placeholder="Xabaringiz matnini shu yerga yozing..." required></textarea>
            <button type="submit" class="yuborish-tugma">Xabarni yuborish</button>
        </form>
    </div>
</body>
</html>
"""

KINOTEATR_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Kinoteatr - MediaLend</title>
    <style> 
        body { font-family: sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .konteyner { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; padding: 30px; }
        .karta { background: #1e293b; padding: 20px; border-radius: 12px; text-align: center; width: 280px; display: flex; flex-direction: column; min-height: 360px; box-sizing: border-box; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .karta img { width: 100%; height: 180px; object-fit: contain; background-color: #0f172a; border-radius: 6px; }
        .karta h3 { margin: 15px 0 10px 0; font-size: 1.2rem; color: #ffffff; }
        .tugma { background-color: #a855f7; color: white; border: none; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; display: block; margin-top: auto; text-align: center; transition: background 0.2s; }
        .tugma:hover { background-color: #9333ea; }
        
        /* Sahifalash (Pagination) Dizayni */
        .pagination { display: flex; justify-content: center; align-items: center; gap: 10px; margin: 40px 0; padding-bottom: 20px; }
        .page-link { background-color: #1e293b; color: #94a3b8; border: 1px solid #334155; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: bold; transition: all 0.3s; }
        .page-link:hover { background-color: #334155; color: #38bdf8; border-color: #38bdf8; }
        .page-active { background-color: #0284c7; color: white; border-color: #0284c7; padding: 10px 18px; border-radius: 6px; font-weight: bold; }
        .page-disabled { background-color: #0f172a; color: #475569; border: 1px solid #1e293b; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    
    <h1 style="text-align: center; color: white; margin-top: 30px;">🎬 Onlayn Kinoteatr</h1>
    
    <div class="konteyner">
        {% for kino in kinolar %}
        <div class="karta">
            <img src="{{ kino.rasm }}" alt="{{ kino.nomi }}" loading="lazy" onerror="this.src='https://placehold.co'">
            <h3>{{ kino.nomi }}</h3>
            <a href="/mahsulot/{{ kino.id }}" class="tugma">🍿 Tomosha qilish</a>
        </div>
        {% endfor %}
    </div>

    <!-- DINAMIK SAHIFALASH TIZIMI -->
    {% if total_pages > 1 %}
    <div class="pagination">
        {% if current_page > 1 %}
            <a href="/kinoteatr?page={{ current_page - 1 }}" class="page-link">⬅️ Oldingi</a>
        {% else %}
            <span class="page-disabled">⬅️ Oldingi</span>
        {% endif %}

        {% for p in range(1, total_pages + 1) %}
            {% if p == current_page %}
                <span class="page-active">{{ p }}</span>
            {% else %}
                <a href="/kinoteatr?page={{ p }}" class="page-link">{{ p }}</a>
            {% endif %}
        {% endfor %}

        {% if current_page < total_pages %}
            <a href="/kinoteatr?page={{ current_page + 1 }}" class="page-link">Keyingi ➡️</a>
        {% else %}
            <span class="page-disabled">Keyingi ➡️</span>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""

MAHSULOT_DETAL_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>{{ mahsulot.nomi }} - MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 0; text-align: center; }
        .navbar { background-color: #1e293b; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .detal-quti { background: #1e293b; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        img { max-width: 100%; height: 300px; object-fit: contain; border-radius: 8px; background-color: #0f172a; padding: 10px; box-sizing: border-box; }
        .sotib-olish-t { background-color: #22c55e; color: white; border: none; padding: 12px 25px; border-radius: 6px; cursor: pointer; font-size: 1.1rem; font-weight: bold; width: 100%; display: block; margin-bottom: 12px; text-decoration: none; box-sizing: border-box; transition: background 0.2s; }
        .sotib-olish-t:hover { background-color: #16a34a; }
        .oqish-t { background-color: #0284c7; color: white; text-decoration: none; padding: 12px 25px; border-radius: 6px; font-size: 1.1rem; font-weight: bold; width: 100%; display: block; text-align: center; box-sizing: border-box; transition: background 0.2s; }
        .oqish-t:hover { background-color: #0369a1; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="detal-quti">
        <img src="{{ mahsulot.rasm }}" alt="{{ mahsulot.nomi }}" onerror="this.src='https://placehold.co'">
        <h2>{{ mahsulot.nomi }}</h2>
        <p style="color: #94a3b8; line-height: 1.6;">{{ mahsulot.tavsifi }}</p>
        <span style="font-size: 1.5rem; color: #38bdf8; font-weight: bold; display: block; margin: 25px 0;">{{ mahsulot.narxi }}</span>
        <a href="{{ mahsulot.fayl }}" target="_blank" class="oqish-t">
            {% if mahsulot.tur == 'kino' %} 🎬 Filmni to'g'ridan-to'g'ri tomosha qilish (MP4)
            {% else %} 📖 Kitobni to'g'ridan-to'g'ri mutolaa qilish (PDF)
            {% endif %}
        </a>
        <a href="/savat/qoshish/{{ mahsulot.id }}" id="sotib-olish-btn" class="sotib-olish-t" style="margin-top: 15px;">🛍️ Savatga qo'shish</a>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const m = { id: {{ mahsulot.id | tojson }}, nomi: {{ mahsulot.nomi | tojson }}, narxi: {{ mahsulot.narxi | tojson }}, rasm: {{ mahsulot.rasm | tojson }}, tur: {{ mahsulot.tur | tojson }} };
            let t = JSON.parse(localStorage.getItem('tarix')) || [];
            if (!t.some(i => String(i.id) === String(m.id))) { 
                t.unshift(m); 
                if (t.length > 10) t.pop(); 
                localStorage.setItem('tarix', JSON.stringify(t)); 
            }
            document.getElementById('sotib-olish-btn').addEventListener('click', function() {
                let s = JSON.parse(localStorage.getItem('savat')) || [];
                if (!s.some(i => String(i.id) === String(m.id))) { 
                    s.unshift(m); 
                    localStorage.setItem('savat', JSON.stringify(s)); 
                }
            });
        });
    </script>
</body>
</html>
"""

KORZINKA_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Savat va Tarix - MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .kontent { max-width: 900px; margin: 40px auto; padding: 0 20px; box-sizing: border-box; }
        .blok { background: #1e293b; padding: 25px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .blok h2 { margin-top: 0; margin-bottom: 20px; color: #fff; font-size: 1.5rem; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        .tarix-element { display: flex; justify-content: space-between; align-items: center; background: #0f172a; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #334155; transition: transform 0.2s; }
        .tarix-element:hover { transform: translateY(-2px); }
        .tarix-element img { width: 60px; height: 60px; object-fit: contain; background: #1e293b; border-radius: 6px; padding: 5px; }
        .ochirish-t { background: #ef4444; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: background 0.2s; display: inline-block; text-decoration: none; font-size: 0.9rem; }
        .ochirish-t:hover { background-color: #dc2626; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="kontent">
        <div class="blok">
            <h2>🛍️ Savatdagi Xaridlar</h2>
            <div id="savat-ruyxat"></div>
        </div>
        <div class="blok">
            <h2>👁️ Yaqinda Ko'rilganlar Tarixi</h2>
            <div id="tarix-ruyxat"></div>
        </div>
    </div>
    <script>
        function ruyxatniChikar() {
            const s = JSON.parse(localStorage.getItem('savat')) || [];
            const t = JSON.parse(localStorage.getItem('tarix')) || [];
            const sd = document.getElementById('savat-ruyxat');
            const td = document.getElementById('tarix-ruyxat');
            
            sd.innerHTML = s.length === 0 ? 
                '<p style="color:#94a3b8;font-style:italic;margin:0;">Savat bo\\'sh.</p>' : 
                s.map((m, i) => `
                    <div class="tarix-element">
                        <div style="display:flex;align-items:center;gap:15px;">
                            <img src="${m.rasm}" onerror="this.src='https://placehold.co'">
                            <div>
                                <h4 style="margin:0;font-size:1.1rem;color:#fff;">${m.nomi}</h4>
                                <span style="color:#38bdf8;font-weight:bold;margin-top:5px;display:inline-block;">${m.narxi || m.narx}</span>
                            </div>
                        </div>
                        <div style="display:flex;gap:10px;align-items:center;">
                            <a href="/savat/ochirish/${m.id}" class="ochirish-t" onclick="savatdanOchirish(event, ${i}, ${m.id})">O'chirish</a>
                        </div>
                    </div>
                `).join('');
                
            td.innerHTML = t.length === 0 ? 
                '<p style="color:#94a3b8;font-style:italic;margin:0;">Tarix bo\\'sh.</p>' : 
                t.map((m, i) => `
                    <div class="tarix-element">
                        <div style="display:flex;align-items:center;gap:15px;">
                            <img src="${m.rasm}" onerror="this.src='https://placehold.co'">
                            <div>
                                <h4 style="margin:0;font-size:1.1rem;color:#fff;">${m.nomi}</h4>
                                <span style="color:#94a3b8;font-size:0.9rem;margin-top:5px;display:inline-block;">Turi: ${(m.tur || 'Asar').toUpperCase()}</span>
                            </div>
                        </div>
                        <button class="ochirish-t" onclick="tarixdanOchirish(${i})">O'chirish</button>
                    </div>
                `).join('');
        }
        function savatdanOchirish(event, index, id) {
            event.preventDefault();
            let s = JSON.parse(localStorage.getItem('savat')) || []; 
            s.splice(index, 1); 
            localStorage.setItem('savat', JSON.stringify(s));
            window.location.href = `/savat/ochirish/${id}`;
        }
        function tarixdanOchirish(index) { 
            let r = JSON.parse(localStorage.getItem('tarix')) || []; 
            r.splice(index, 1); 
            localStorage.setItem('tarix', JSON.stringify(r)); 
            ruyxatniChikar(); 
        }
        document.addEventListener('DOMContentLoaded', ruyxatniChikar);
    </script>
</body>
</html>
"""

YAZAR_EDITOR_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Ijodxona - MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; margin:0; padding:0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .konteyner { display: flex; max-width: 1250px; margin: 30px auto; padding: 0 20px; gap: 25px; box-sizing: border-box; }
        .quti { flex: 3; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .ai-panel { flex: 1; background: #1e293b; padding: 25px; border-radius: 12px; border: 1px solid #334155; height: fit-content; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .ai-t { background-color: #6b21a8; color: white; border: none; padding: 14px; border-radius: 6px; font-weight: bold; cursor: pointer; text-align: left; transition: all 0.2s; }
        .ai-t:hover:not(:disabled) { background-color: #581c87; }
        .ai-t:disabled { background-color: #4c1d95; color: #94a3b8; cursor: not-allowed; opacity: 0.6; }
        .ai-natija-quti { background: #0f172a; border: 1px solid #334155; border-radius: 6px; padding: 15px; min-height: 160px; color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; word-wrap: break-word; white-space: pre-wrap; }
        input[type="text"] { width: 100%; padding: 12px; margin: 8px 0 15px 0; background: #0f172a; border: 1px solid #334155; color: white; border-radius: 6px; box-sizing: border-box; font-size: 1rem; }
        textarea { width: 100%; min-height: 400px; background-color: #0f172a; color: white; border-radius: 6px; border: 1px solid #334155; font-size: 16px; padding: 15px; box-sizing: border-box; resize: vertical; }
        textarea:focus { border-color: #38bdf8; outline: none; }
        .tugma-guruh { display: flex; gap: 15px; margin-top: 25px; }
        .tugma-chop { background-color: #22c55e; color: white; border: none; padding: 14px; flex: 1; border-radius: 6px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        .tugma-chop:hover { background-color: #16a34a; }
        .tugma-qoralama { background-color: #f59e0b; color: white; border: none; padding: 14px; flex: 1; border-radius: 6px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        .tugma-qoralama:hover { background-color: #d97706; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="konteyner">
        <div class="quti">
            <h2>✍️ O'z asaringizni yozing</h2>
            <form method="POST" action="/yozish" id="yozish-form">
                <label>Asar sarlavhasi:</label>
                <input type="text" name="nomi" placeholder="Kitob nomini kiriting..." required>
                <label>Matn:</label>
                <textarea name="matn" id="editor-matn" placeholder="Bu yerga o'z asaringizni yozing..." required></textarea>
                <div class="tugma-guruh">
                    <button type="submit" name="amal" value="qoralama" id="btn-qoralama" class="tugma-qoralama">💾 Qoralama sifatida saqlash</button>
                    <button type="submit" name="amal" value="chop_etish" id="btn-chop" class="tugma-chop">🚀 Tugatish va chop etish</button>
                </div>
            </form>
        </div>
        <div class="ai-panel">
            <h3 style="color:#a855f7; margin:0;">🤖 AI Muharrir Ko'makchisi</h3>
            <button type="button" class="ai-t" id="btn-polishing" onclick="aiSorovYubor('polishing')">✨ Imlo va uslubni tekshirish</button>
            <button type="button" class="ai-t" id="btn-outline" onclick="aiSorovYubor('outline')">📝 Keyingi boblar uchun reja/g'oya</button>
            <div id="ai-natija" class="ai-natija-quti"><span style="color:#64748b; font-style:italic;">Tugmalardan birini bosing...</span></div>
        </div>
    </div>  
    <script>
    document.getElementById('yozish-form').addEventListener('submit', function(e) {
        document.getElementById('btn-chop').disabled = true;
        document.getElementById('btn-qoralama').disabled = true;
        document.getElementById('btn-chop').innerHTML = "⏳ AI janrni aniqlamoqda...";
    });
    function aiSorovYubor(tur) {
        const matnMaydoni = document.getElementById('editor-matn');
        const natijaKutish = document.getElementById('ai-natija');
        const btnPolishing = document.getElementById('btn-polishing');
        const btnOutline = document.getElementById('btn-outline');
        if (!matnMaydoni || !matnMaydoni.value.trim()) { alert("⚠️ Avval matn maydoniga biror narsa yozing!"); return; }
        const matn = matnMaydoni.value.trim();
        btnPolishing.disabled = true; btnOutline.disabled = true; matnMaydoni.disabled = true;
        natijaKutish.innerHTML = "⏳ <b>Ollama fondagi ishchi oqimda tahlil qilmoqda... Iltimos, kuting...</b>";
        fetch('/ai_yordamchi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matn: matn, tur: tur })
        })
        .then(response => { if (!response.ok) throw new Error('Xatolik'); return response.json(); })
        .then(data => { natijaKutish.innerHTML = data.natija || "⚠️ Bo'sh javob."; })
        .catch(error => { natijaKutish.innerHTML = "❌ <b>Taymaut yoki aloqa xatoligi!</b>"; })
        .finally(() => { btnPolishing.disabled = false; btnOutline.disabled = false; matnMaydoni.disabled = false; });
    }
    </script>
</body>
</html>
"""

# 8. MUALLIFLAR ASARLARI RO'YXATI (MUALLIFLAR_HTML)
MUALLIFLAR_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Mualliflar Ijodi - MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .kontent { max-width: 800px; margin: 40px auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        .kontent h1 { margin-top: 0; margin-bottom: 25px; font-size: 1.8rem; color: #fff; border-bottom: 1px solid #334155; padding-bottom: 12px; }
        .kitob-turi { background: #0f172a; padding: 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; transition: transform 0.2s; }
        .kitob-turi:hover { transform: translateY(-2px); }
        .mutolaa-tugma { background-color: #0284c7; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; transition: background 0.2s; }
        .mutolaa-tugma:hover { background-color: #0369a1; }
        .janr-badge { font-size: 0.75rem; background-color: #6b21a8; color: #f3e8ff; padding: 3px 8px; border-radius: 12px; margin-left: 10px; font-weight: bold; display: inline-block; vertical-align: middle; }
        .pagination { display: flex; justify-content: center; align-items: center; gap: 10px; margin: 30px 0; }
        .page-link { background-color: #0f172a; color: #94a3b8; border: 1px solid #334155; padding: 10px 18px; border-radius: 6px; text-decoration: none; font-weight: bold; transition: all 0.3s; }
        .page-link:hover { background-color: #334155; color: #38bdf8; border-color: #38bdf8; }
        .page-active { background-color: #0284c7; color: white; border-color: #0284c7; padding: 10px 18px; border-radius: 6px; font-weight: bold; }
        .page-disabled { background-color: #1e293b; color: #475569; border: 1px solid #0f172a; padding: 10px 18px; border-radius: 6px; font-weight: bold; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="kontent">
        <h1>📚 Mualliflar tomonidan yozilgan kitoblar</h1>
        {% for kitob in kitoblar %}
        <div class="kitob-turi">
            <div>
                <span style="font-weight:bold; color:#38bdf8; font-size:1.1rem;">{{ kitob.nomi }}</span>
                <span style="color:#94a3b8; font-style:italic;"> — {{ kitob.muallif }}</span>
                <span class="janr-badge">{{ kitob.tur }}</span>
            </div>
            <a href="/mutolaa/{{ kitob.id }}" class="mutolaa-tugma">📖 O'qish</a>
        </div>
        {% else %}
        <p style="color:#94a3b8; font-style:italic; text-align:center; margin: 20px 0;">Hozircha asarlar mavjud emas.</p>
        {% endfor %}
        {% if total_pages > 1 %}
        <div class="pagination" style="margin-top: 30px;">
            {% if current_page > 1 %} <a href="/mualliflar?page={{ current_page - 1 }}" class="page-link">⬅️ Oldingi</a>
            {% else %} <span class="page-disabled">⬅️ Oldingi</span> {% endif %}
            {% for p in range(1, total_pages + 1) %}
                {% if p == current_page %} <span class="page-active">{{ p }}</span>
                {% else %} <a href="/mualliflar?page={{ p }}" class="page-link">{{ p }}</a> {% endif %}
            {% endfor %}
            {% if current_page < total_pages %} <a href="/mualliflar?page={{ current_page + 1 }}" class="page-link">Keyingi ➡️</a>
            {% else %} <span class="page-disabled">Keyingi ➡️</span> {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head> 
    <meta charset="UTF-8">
    <title>Tizimga kirish va Ro'yxatdan o'tish - MediaLend</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .kontent { max-width: 400px; margin: 60px auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        h2 { text-align: center; color: #ffffff; margin-top: 0; margin-bottom: 20px; font-size: 1.6rem; }
        form { display: flex; flex-direction: column; gap: 15px; }
        .parol-konteyner { position: relative; width: 100%; }
        input[type="text"], input[type="email"], input[type="password"] { width: 100%; padding: 12px; background-color: #0f172a; border: 1px solid #334155; color: white; border-radius: 6px; box-sizing: border-box; font-size: 1rem; transition: border-color 0.2s; }
        .parol-konteyner input { padding-right: 40px; }
        input:focus { border-color: #38bdf8; outline: none; }
        button { background-color: #38bdf8; color: white; border: none; padding: 14px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 1rem; transition: background 0.2s; }
        button:hover { background-color: #0284c7; }
        .toggle-link { text-align: center; margin-top: 15px; color: #94a3b8; font-size: 0.9rem; cursor: pointer; transition: color 0.2s; }
        .toggle-link:hover { color: #38bdf8; }
        .alert-box { padding: 12px; border-radius: 6px; margin-bottom: 15px; text-align: center; font-weight: bold; font-size: 0.9rem; }
        .alert-error { background-color: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }
        .alert-success { background-color: rgba(34, 197, 94, 0.2); color: #22c55e; border: 1px solid #22c55e; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
    </div>
    <div class="kontent">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert-box {% if category == 'success' %}alert-success{% else %}alert-error{% endif %}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <h2 id="form-title">Kirish</h2>
        <form id="auth-form" method="POST" action="/login">
            <div id="ism-guruh" style="display: none;"><input type="text" id="input-ism" name="ism" placeholder="To'liq ismingiz"></div>
            <input type="email" name="email" placeholder="Elektron pochta (Email)" required>
            <div class="parol-konteyner">
                <input type="password" id="input-parol" name="parol" placeholder="Parol" required>
                <i class="fa-solid fa-eye" id="shov-hide-btn" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; cursor: pointer;"></i>
            </div>
            <button type="submit" id="submit-button">Kirish</button>
        </form>
        <div class="toggle-link" id="toggle-link">Yangi akkaunt ochish (Ro'yxatdan o'tish)</div>
    </div>
    <script>
        const toggleLink = document.getElementById('toggle-link'); const formTitle = document.getElementById('form-title');
        const submitButton = document.getElementById('submit-button'); const authForm = document.getElementById('auth-form');
        const ismGuruh = document.getElementById('ism-guruh'); const inputIsm = document.getElementById('input-ism');
        const parolInput = document.getElementById('input-parol'); const shovHideBtn = document.getElementById('shov-hide-btn');

        shovHideBtn.addEventListener('click', () => {
            if (parolInput.type === 'password') { parolInput.type = 'text'; shovHideBtn.classList.replace('fa-eye', 'fa-eye-slash'); }
            else { parolInput.type = 'password'; shovHideBtn.classList.replace('fa-eye-slash', 'fa-eye'); }
        });
        toggleLink.addEventListener('click', () => {
            if (formTitle.textContent === 'Kirish') {
                formTitle.textContent = "Ro'yxatdan o'tish"; submitButton.textContent = "Ro'yxatdan o'tish";
                toggleLink.textContent = "Sizda akkaunt bormi? Kirish oynasi"; authForm.action = "/register"; ismGuruh.style.display = "block"; inputIsm.required = true;
            } else {
                formTitle.textContent = "Kirish"; submitButton.textContent = "Kirish";
                toggleLink.textContent = "Yangi akkaunt ochish (Ro'yxatdan o'tish)"; authForm.action = "/login"; ismGuruh.style.display = "none"; inputIsm.required = false;
            }
        });
        {% if request.path == '/register' %}
            formTitle.textContent = "Ro'yxatdan o'tish"; submitButton.textContent = "Ro'yxatdan o'tish"; toggleLink.textContent = "Sizda akkaunt bormi? Kirish oynasi"; authForm.action = "/register"; ismGuruh.style.display = "block"; inputIsm.required = true;
        {% endif %}
    </script>
</body>
</html>
"""

# LOGIN SAHIFASI HAM SHU SHABLONDAN FOYDALANADI
LOGIN_HTML = REGISTER_HTML

# ========================================================
# 11-BOʻLIM: KITOB O'QISH/MUTOLAA SAHIFASI (MUTOLAA_HTML)
# ========================================================
MUTOLAA_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>{{ kitob.nomi }} - Mutolaa | MediaLend</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; }
        .navbar { background-color: #1e293b; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar a { color: #94a3b8; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #38bdf8; }
        .oqi-quti { max-width: 800px; margin: 40px auto; background: #1e293b; padding: 40px; border-radius: 12px; border: 1px solid #334155; line-height: 1.8; box-shadow: 0 4px 12px rgba(0,0,0,0.3); box-sizing: border-box; }
        .janr-belgi { background: #6b21a8; padding: 5px 12px; border-radius: 6px; font-size: 0.85rem; font-weight: bold; color: white; display: inline-block; }
        
        /* white-space: pre-wrap; yordamida matndagi barcha enterlar va abzaslar HTMLda saqlanib qoladi */
        .matn-maydoni { font-size: 1.2rem; color: #cbd5e1; margin-top: 30px; text-align: justify; white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/kinoteatr">🎬 Kinoteatr</a>
        <a href="/yozish">Kitob Yozish</a>
        <a href="/mualliflar">📚 Mualliflar Ijodi</a>
        <a href="/korzinka">🛒 Savat / Tarix</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
        {% if session.get('user_id') %}
            <span style="color: #38bdf8; font-weight: bold; margin-left: 20px;">👤 {{ session.get('user_name') }}</span>
            <a href="/logout" style="color: #ef4444; margin-left: 10px;">Chiqish 🔒</a>
        {% else %}
            <a href="/login" style="color: #38bdf8; margin-left: 20px;">Kirish 🔑</a>
        {% endif %}
    </div>
    <div class="oqi-quti">
        <span class="janr-belgi">🎭 Janr: {{ kitob.tur }}</span>
        <h1 style="color: #ffffff; margin-top: 15px; margin-bottom: 5px;">{{ kitob.nomi }}</h1>
        <h3 style="color: #38bdf8; font-style: italic; margin-top: 0; font-weight: normal;">Muallif: {{ kitob.muallif }}</h3>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 25px 0;">
        <div class="matn-maydoni">{{ kitob.matn | safe }}</div>
    </div>
</body>
</html>
"""
