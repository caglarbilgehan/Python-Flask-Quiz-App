from app import db, Question, app

# Flask uygulama bağlamını kullanarak işlemleri gerçekleştir
with app.app_context():
    db.drop_all()  # Önce eski veritabanını temizle
    db.create_all()  # Yeni tabloları oluştur

    # 📌 Soruları ekleyelim
    sample_questions = [
        Question(text="Python'da koşullu ifadelerde 'elif' ne işe yarar?", 
                 option_a="Koşullu ifadeler için", 
                 option_b="Bir büyü komutu", 
                 option_c="Pizza siparişi vermek için", 
                 correct_answer="A"),
        
        Question(text="Python'da ekrana yazı yazdırmak için hangi komut kullanılır?", 
                 option_a="print()", 
                 option_b="shout()", 
                 option_c="display()", 
                 correct_answer="A"),
        
        Question(text="Python'da 'list' veri tipi ne anlama gelir?", 
                 option_a="Yemek listesi", 
                 option_b="Sıralı ve değiştirilebilir veri tipi", 
                 option_c="Alışveriş sepeti", 
                 correct_answer="B"),
        
        Question(text="Hangi döngü sonsuz döngüye neden olabilir?", 
                 option_a="while döngüsü", 
                 option_b="for döngüsü", 
                 option_c="never-ending-loop()", 
                 correct_answer="A"),
        
        Question(text="Python'da 'def' komutu neyi tanımlar?", 
                 option_a="Bir fonksiyon", 
                 option_b="Gizli bir Python alias'ı", 
                 option_c="Kod yazmanın sırrı", 
                 correct_answer="A"),
        
        Question(text="Python ile bir Discord botu geliştirmek için hangi kütüphane kullanılır?", 
                 option_a="discord.py", 
                 option_b="Flask", 
                 option_c="TensorFlow", 
                 correct_answer="A"),
        
        Question(text="Flask'te HTTP isteğini almak için hangi değişken kullanılır?", 
                 option_a="request", 
                 option_b="response", 
                 option_c="session", 
                 correct_answer="A"),
        
        Question(text="TensorFlow ile yapay zeka modeli eğitirken kullanılan ana metod nedir?", 
                 option_a="model.fit()", 
                 option_b="train_model()", 
                 option_c="ai_learn()", 
                 correct_answer="A"),
        
        Question(text="Computer Vision için en yaygın kullanılan kütüphane hangisidir?", 
                 option_a="OpenCV", 
                 option_b="NLTK", 
                 option_c="Flask", 
                 correct_answer="A"),
        
        Question(text="Doğal Dil İşleme (NLP) için en yaygın kullanılan kütüphane hangisidir?", 
                 option_a="NLTK", 
                 option_b="PyTorch", 
                 option_c="Matplotlib", 
                 correct_answer="A"),
    ]

    # 🔹 Soruları veritabanına ekle
    db.session.add_all(sample_questions)
    db.session.commit()

    print("✅ Veritabanı oluşturuldu ve sorular başarıyla eklendi!")