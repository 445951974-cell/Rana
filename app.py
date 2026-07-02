from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# إعداد قاعدة البيانات (SQLite)
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # إنشاء جدول لحفظ تقارير العقود المرفوعة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            summary TEXT,
            suggestion TEXT,
            draft TEXT
        )
    ''')
    conn.commit()
    conn.close()

# الصفحة الرئيسية (تعرض واجهة HTML)
@app.route('/')
def home():
    return render_template('index.html')

# الـ API المسؤول عن استقبال الملف وتحليله وحفظه في قاعدة البيانات
@app.route('/analyze', methods=['POST'])
def analyze_contract():
    if 'contract_file' not in request.files:
        return jsonify({'error': 'لم يتم رفع أي ملف'}), 400
        
    file = request.files['contract_file']
    if file.filename == '':
        return jsonify({'error': 'اسم الملف فارغ'}), 400

    # هنا في المستقبل يتم دمج وكيل الذكاء الاصطناعي لقراءة الـ PDF، حالياً نضع بيانات محاكاة (Mock Data) للهاكاثون
    filename = file.filename
    risk_score = 55
    risk_level = "🟡 مخاطرة متوسطة"
    summary = "تم اكتشاف شرط إلغاء غير مرن (90 يوماً)، وتجديد تلقائي مجحف للأسعار المستحقة."
    suggestion = "نقترح التفاوض لتقليل مدة الالتزام من 3 سنوات إلى سنة واحدة، وتقليص فترة الإشعار إلى 30 يوماً."
    draft = f"السلام عليكم، بخصوص عقد {filename} المطروح، نود مناقشة بند الإلغاء الوارد في المادة رقم (7) واقتراح تعديل فترة الإشعار لتصبح 30 يوماً بدلاً من 90 يوماً."

    # حفظ البيانات في قاعدة البيانات باستخدام SQL
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contracts (filename, risk_score, risk_level, summary, suggestion, draft)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (filename, risk_score, risk_level, summary, suggestion, draft))
    conn.commit()
    conn.close()

    # إرسال النتيجة للـ Front-end لعرضها فوراً
    return jsonify({
        'filename': filename,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'summary': summary,
        'suggestion': suggestion,
        'draft': draft
    })
    print("تم الوصول لنهاية الملف ")
    if __name__=='__main__':
     init_db()  # تشغيل قاعدة البيانات عند بدء السيرفر
     app.run(debug=True, port=5000)