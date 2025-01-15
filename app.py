from flask import Flask, render_template, request
import sqlite3
import logging

app = Flask(__name__)

# Hata logları için ayar
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# SQLite veritabanı bağlantısı
def get_db_connection():
    try:
        conn = sqlite3.connect('/home/caglarbilgehan/kodland/pythonpro/quiz.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise

# Veritabanı tablosu oluşturma fonksiyonu
def init_db():
    try:
        conn = sqlite3.connect('/home/caglarbilgehan/kodland/pythonpro/quiz.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER
            )
        ''')
        conn.commit()
        conn.close()
        print("Tablo başarıyla oluşturuldu veya zaten mevcut.")
    except Exception as e:
        logging.error(f"Tablo oluşturulurken hata oluştu: {e}")
        raise e


# Ana sayfa (quiz.html) gösterimi
@app.route('/')
def home():
    try:
        return render_template('quiz.html')
    except Exception as e:
        logging.error(f"Error loading home page: {e}")
        return "1) Bir hata oluştu. Lütfen tekrar deneyin.", 500

# Sınavı gönderme ve sonucu kaydetme
@app.route('/submit', methods=['POST'])
def submit():
    try:
        score = 0
        correct_answers = {
            'q1': 'A',  # Elif, Python'daki "else" kısmının kardeşi!
            'q2': 'A',  # print() – Bu komut seni ünlü yapabilir!
            'q3': 'B',  # Veri tipidir, sıralı ve değiştirilebilir.
            'q4': 'A',  # while döngüsü – Sonsuza kadar gidebilir!
            'q5': 'A',  # Fonksiyon tanımlar – Ama unutma, çok eğlenceli!
        }

        # Kullanıcı cevaplarını al
        user_answers = {
            'q1': request.form.get('q1'),
            'q2': request.form.get('q2'),
            'q3': request.form.get('q3'),
            'q4': request.form.get('q4'),
            'q5': request.form.get('q5'),
        }

        # Cevapları kontrol et ve puanı hesapla
        for question, answer in user_answers.items():
            if answer == correct_answers[question]:
                score += 1

        # Veritabanına en yüksek puanı kaydet
        conn = get_db_connection()
        c = conn.cursor()

        # Tabloyu kontrol et (Bu genelde init_db() tarafından yapılır)
        c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="scores";')
        table_exists = c.fetchone()

        if not table_exists:
            init_db()  # Eğer tablo yoksa, tablonun oluşturulmasını sağla
            print("Tablo oluşturuldu.")

        # Veritabanına puanı kaydet
        conn.execute('INSERT INTO scores (score) VALUES (?)', (score,))
        conn.commit()

        # En yüksek puanı veritabanından al
        highest_score = conn.execute('SELECT MAX(score) FROM scores').fetchone()[0]
        conn.close()

        # Sonuç sayfasına yönlendirme
        return render_template('result.html', score=score, highest_score=highest_score)

    except Exception as e:
        logging.error(f"Error during quiz submission: {e}")
        return f"3) Bir hata oluştu: {e}. Lütfen tekrar deneyin.", 500


if __name__ == '__main__':
    # Veritabanını başlat
    init_db()

    # Flask uygulamasını debug modunda çalıştır
    app.run(debug=True)
