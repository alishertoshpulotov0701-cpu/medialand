# templates.py fayli

INDEX_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="geFdhlqFqWC7cdKBlYr_ncuSIwJ6R0DFoz-c6xsGAzA" />
    <title>Bizning Dokon - Bosh sahifa</title>
    <style>
        /* Asosiy sozlamalar va sahifa yuklanish animatsiyasi */
        body {
            font-family: sans-serif;
            background-color: #1e81b0;
            margin: 0;
            padding: 0;
            animation: fadeInSahifa 0.8s ease-out;
        }

        .navbar { background-color: #eeeee4; padding: 15px; text-align: center; }
        .navbar a { color: blue; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #007bff; }
        h1 { text-align: center; margin-top: 30px; color: #333; animation: tepadatushish 0.6s ease-out; }
        .konteyner { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; padding: 30px; }
        
        /* TUZATILDI: Kartalarni va tugmalarni standart simmetrik holatga keltirish */
        .karta { 
            background: white; 
            padding: 20px; 
            border-radius: 12px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.08); 
            text-align: center; 
            width: 280px; 
            
            display: flex;
            flex-direction: column;
            min-height: 420px; 
            box-sizing: border-box; 
            
            transition: transform 0.3s ease, box-shadow 0.3s ease; 
            animation: pastdanChiqish 0.6s ease-out backwards;
        }
        .karta:hover { transform: translateY(-10px); box-shadow: 0 12px 24px rgba(0,0,0,0.15); }
        .karta img { width: 100%; height: 180px; object-fit: contain; border-radius: 6px; transition: transform 0.5s ease; }
        .karta:hover img { transform: scale(1.05); }
        .narx { color: #28a745; font-size: 1.3rem; font-weight: bold; display: block; margin: 15px 0; }
        
        /* YANGI: Matndan keyingi joyni egallab, tugmani eng pastga bir xil qatorga tekislaydi */
        .karta p {
            flex-grow: 1;
            margin-bottom: 15px;
        }

        /* TUZATILDI: Ikki tomondan va pastdan aniq 20px standart masofa qoldirish */
        .tugma { 
            background-color: #007bff; 
            color: white; 
            border: none; 
            padding: 12px 20px; 
            border-radius: 6px; 
            width: 100%; 
            cursor: pointer; 
            font-size: 1rem; 
            font-weight: bold;
            text-decoration: none;
            display: block;
            box-sizing: border-box;
            margin-top: auto;
            
            transition: background-color 0.2s, transform 0.1s;
        }
        .tugma:hover { background-color: #0056b3; }
        .tugma:active { transform: scale(0.95); }

        @keyframes fadeInSahifa { from { opacity: 0; } to { opacity: 1; } }
        @keyframes tepadatushish { from { transform: translateY(-30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @keyframes pastdanChiqish { from { transform: translateY(40px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
    </div>
    <h1>Bizning do'konimizga xush kelibsiz!</h1>
    <div class="konteyner">
        {% for mahsulot in mahsulotlar %}
        <div class="karta" style="animation-delay: {{ loop.index * 0.15 }}s;">
            <img src="{{ mahsulot.rasm }}" alt="{{ mahsulot.nomi }}">
            <h3>{{ mahsulot.nomi }}</h3>
            <p>{{ mahsulot.tavsifi }}</p>
            <span class="narx">{{ mahsulot.narxi }}</span>
            <a href="/mahsulot/{{ mahsulot.id }}" class="tugma" style="text-decoration: none; display: block;">Sotib olish</a>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

ABOUT_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Biz haqimizda - Bizning Do'kon</title>
    <style>
        body { 
            font-family: sans-serif; 
            background-color: #1e81b0; 
            margin: 0;
            padding: 0; 
            text-align: center; 
        }
        .navbar { background-color: #eeeee4; padding: 15px; text-align: center; }
        .navbar a { color: blue; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #007bff; }
        
        .kontent { 
            background: white; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 40px; 
            border-radius: 12px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            text-align: center; /* Kontent markazga tekislandi */
            box-sizing: border-box;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .matn { line-height: 1.6; color: #555; font-size: 1.1rem; text-align: justify; margin-bottom: 30px; }
        
        /* TUZATILDI: Afzallik kartalarini bir qatorga chiroyli joylashtirish */
        .afzalliklar { 
            display: flex; 
            gap: 20px; 
            margin-top: 30px; 
            flex-wrap: wrap; 
            justify-content: center;
        }
        .afzallik-karta { 
            flex: 1; 
            min-width: 200px; 
            background: #f4f6f9; 
            padding: 20px; 
            border-radius: 8px; 
            text-align: center; 
            box-shadow: 0 2px 6px rgba(0,0,0,0.05); 
            box-sizing: border-box;
        }
        .afzallik-karta h3 { color: #007bff; margin-top: 0; margin-bottom: 10px; }
        .afzallik-karta p { color: #666; font-size: 0.95rem; margin: 0; line-height: 1.4; }
        
        .ortga-tugma { 
            display: inline-block; 
            margin-top: 40px; 
            padding: 12px 30px; 
            background-color: #6c757d; 
            color: white; 
            text-decoration: none; 
            border-radius: 6px; 
            font-weight: bold; 
            transition: background-color 0.2s;
        }
        .ortga-tugma:hover { background-color: #5a6268; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
    </div>
    
    <div class="kontent">
        <h1>Biz haqimizda</h1>
        <div class="matn">
            Bizning internet do'konimiz 2026-yilda xaridorlarga eng sifatli va zamonaviy mahsulotlarni tez hamda qulay usullarda yetkazib berish maqsadida tashkil etilgan. Biz mijozlarimizning vaqti va ishonchini qadrlaymiz, shuning uchun faqat kafolatlangan mahsulotlarni taqdim etamiz. Hozirgi kunda do'konimiz orqali kitoblar, kompyuter jihozlari va boshqa kundalik ehtiyoj uchun zarur bo'lgan ashyolarni hamyonbop narxlarda xarid qilishingiz mumkin.
        </div>
        
        <div class="afzalliklar">
            <div class="afzallik-karta">
                <h3>⚡ Tezkor Yetkazish</h3>
                <p>O'zbekiston bo'ylab buyurtmalar 24 soat ichida yetkazib beriladi.</p>
            </div>
            <div class="afzallik-karta">
                <h3>🛡️ Sifat Kafolati</h3>
                <p>Barcha mahsulotlarimiz 100% original va sifat nazoratidan o'tgan.</p>
            </div>
            <div class="afzallik-karta">
                <h3>📞 24/7 Qo'llab-quvvatlash</h3>
                <p>Savollaringizga istalgan vaqtda tezkor javob olasiz.</p>
            </div>
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
    <title>Aloqa - Bizning Do'kon</title>
    <style>
        body { font-family: sans-serif; background-color: #1e81b0; margin: 0; padding: 0; text-align: center; }
        .navbar { background-color: #eeeee4; padding: 15px; }
        .navbar a { color: blue; margin: 0 15px; text-decoration: none; font-weight: bold; transition: color 0.3s; }
        .navbar a:hover { color: #007bff; }
        
        .kontent { background: white; max-width: 800px; margin: 50px auto; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: left; display: flex; gap: 30px; flex-wrap: wrap; }
        h1 { width: 100%; text-align: center; color: #333; margin-top: 0; }
        
        .aloqa-info { flex: 1; min-width: 280px; }
        .aloqa-forma { flex: 1; min-width: 280px; background: #f4f6f9; padding: 20px; border-radius: 8px; }
        
        .info-blok { margin-bottom: 20px; }
        .info-blok strong { color: #007bff; display: block; font-size: 1.1rem; margin-bottom: 5px; }
        
        .forma-guruh { margin-bottom: 15px; }
        .forma-guruh label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        .forma-guruh input, .forma-guruh textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-family: sans-serif; }
        
        .yuborish-tugma { background-color: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 6px; width: 100%; cursor: pointer; font-size: 1rem; font-weight: bold; transition: background-color 0.2s; }
        .yuborish-tugma:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
    </div>
    
    <div class="kontent">
        <h1>Biz bilan bog'lanish</h1>
        
        <div class="aloqa-info">
            <p>Savollar, takliflar yoki buyurtmalar bo'yicha muammolar yuzaga kelsa, istalgan vaqtda bizga murojaat qilishingiz mumkin. Biz sizga yordam berishdan mamnunmiz!</p>
            
            <div class="info-blok">
                <strong>📧 Elektron pochta:</strong>
                <a href="mailto:alishertoshpulotov0701@gmail.com" style="color: #333;">alishertoshpulotov0701@gmail.com</a>
            </div>
            
            <div class="info-blok">
                <strong>📞 Telefon raqam:</strong>
                <span>+998 (99) 654-21-57</span>
            </div>
            
            <div class="info-blok">
                <strong>📍 Asosiy manzil:</strong>
                <span>Buxoro viloyati, Olot tumani, Xalifa MFY, 100-uy </span>
            </div>
            
            <div class="info-blok">
                <strong>⏰ Ish vaqti:</strong>
                <span>Dushanba - Shanba: 09:00 - 20:00<br>Yakshanba: Dam olish kuni</span>
            </div>
        </div>
        
        <div class="aloqa-forma">
            <h3 style="margin-top: 0; text-align: center; color: #333;">Xabar qoldiring</h3>
            
            {# YANGI: Muvaffaqiyatli yuborilgandagi yashil xabar #}
            {% if success %}
            <div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 6px; margin-bottom: 15px; text-align: center;">
                <b>Rahmat!</b> Xabaringiz pochtaga real vaqtda muvaffaqiyatli yuborildi.
            </div>
            {% endif %}

            {# YANGI: Noto'g'ri kiritilgandagi qizil xabar (Xato sababi backenddan keladi) #}
            {% if error %}
            <div style="background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 6px; margin-bottom: 15px; text-align: center;">
                <b>Xatolik!</b> {{ xato_sababi }}
            </div>
            {% endif %}

            <form action="/contact" method="POST">
                <div class="forma-guruh">
                    <label>Ismingiz:</label>
                    <input type="text" name="ism" placeholder="Ismingizni kiriting" required>
                </div>
                <div class="forma-guruh">
                    <label>Email yoki Telefon:</label>
                    <input type="text" name="aloqa" placeholder="Bog'lanish ma'lumotini kiriting" required>
                </div>
                <div class="forma-guruh">
                    <label>Xabaringiz:</label>
                    <textarea rows="4" name="xabar" placeholder="Xabar matnini yozing..." required></textarea>
                </div>
                <button type="submit" class="yuborish-tugma">Xabarni yuborish</button>
            </form>  
        </div>
    </div>
</body>
</html>
"""

MAHSULOT_DETAL_HTML = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>{{ mahsulot.nomi }}</title>
    <style>
        body { font-family: sans-serif; background-color: #1e81b0; margin: 0; padding: 0; text-align: center; }
        .navbar { background-color: #eeeee4; padding: 15px; }
        .navbar a { color: blue; margin: 0 15px; text-decoration: none; font-weight: bold; }
        .kontent { background: white; max-width: 500px; margin: 50px auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .kontent img { max-width: 100%; height: 250px; object-fit: contain; border-radius: 8px; margin-bottom: 20px; }
        .narx { color: #28a745; font-size: 1.5rem; font-weight: bold; display: block; margin: 15px 0; }
        .ortga-tugma { 
            display: inline-block; 
            margin-top: 20px; 
            padding: 10px 20px; 
            background-color: #6c757d; 
            color: white; 
            text-decoration: none; 
            border-radius: 6px; 
            font-weight: bold; 
        }
        .ortga-tugma:hover { background-color: #5a6268; }
    </style>
</head>
<body>
    <div class="navbar">
        <a href="/">Bosh sahifa</a>
        <a href="/about">Biz haqimizda</a>
        <a href="/contact">Aloqa</a>
    </div>
    <div class="kontent">
        {% if mahsulot.rasm %}
        <img src="{{ mahsulot.rasm }}" alt="{{ mahsulot.nomi }}">
        {% endif %}
        <h1>{{ mahsulot.nomi }}</h1>
        <p><strong>Tavsifi:</strong> {{ mahsulot.tavsifi }}</p>
        <span class="narx">{{ mahsulot.narxi }}</span>
        
        <hr>
        <a href="/" class="ortga-tugma">⬅ Bosh sahifaga qaytish</a>
    </div>
</body>
</html>
"""

