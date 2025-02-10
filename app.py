from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Veritabanı bağlantısı
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Veritabanı Modelleri
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)  # Kullanıcı Adı
    score = db.Column(db.Integer, nullable=False)

# Ana sayfa (quiz)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['user_name'] = request.form.get('user_name', 'Anonim')  # Kullanıcı adını al ve sakla
        session['user_id'] = session['user_name']  # Kullanıcıyı belirlemek için ID olarak adını kullanıyoruz.
        return redirect('/quiz')

    return render_template('index.html')

# Quiz sayfası
@app.route('/quiz')
def quiz():
    if 'user_name' not in session:
        return redirect('/')

    questions = Question.query.all()
    global_high_score = db.session.query(db.func.max(Score.score)).scalar() or 0
    user_high_score = db.session.query(db.func.max(Score.score)).filter_by(user_id=session['user_id']).scalar() or 0

    return render_template('quiz.html', questions=questions, global_high_score=global_high_score, user_high_score=user_high_score, user_name=session['user_name'])

# Sınav sonucu gönderme
@app.route('/submit', methods=['POST'])
def submit():
    if 'user_name' not in session:
        return redirect('/')

    score = 0
    questions = Question.query.all()

    for question in questions:
        user_answer = request.form.get(f"q{question.id}")
        if user_answer == question.correct_answer:
            score += 1

    new_score = Score(user_id=session['user_id'], user_name=session['user_name'], score=score)
    db.session.add(new_score)
    db.session.commit()

    global_high_score = db.session.query(db.func.max(Score.score)).scalar()
    user_high_score = db.session.query(db.func.max(Score.score)).filter_by(user_id=session['user_id']).scalar()

    return render_template('result.html', score=score, global_high_score=global_high_score, user_high_score=user_high_score, user_name=session['user_name'])

# En yüksek puanı sıfırla
@app.route('/reset', methods=['POST'])
def reset_highest_score():
    db.session.query(Score).delete()
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)