from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# SQLite veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanı tablosu oluşturma fonksiyonu
def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Ana sayfa (quiz.html) gösterimi
@app.route('/')
def home():
    return render_template('quiz.html')

@app.route('/reset', methods=['POST'])
def reset_highest_score():
    conn = get_db_connection()
    conn.execute('DELETE FROM scores')
    conn.commit()
    conn.close()
    return render_template('result.html', score=0, highest_score=0)


# Sınavı gönderme ve sonucu kaydetme
@app.route('/submit', methods=['POST'])
def submit():
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
    conn.execute('INSERT INTO scores (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()

    # En yüksek puanı veritabanından al
    conn = get_db_connection()
    highest_score = conn.execute('SELECT MAX(score) FROM scores').fetchone()[0]
    conn.close()

    # Sonuç sayfasına yönlendirme
    return render_template('result.html', score=score, highest_score=highest_score)

if __name__ == '__main__':
    # Veritabanını başlat
    init_db()
    app.run(debug=True)
