from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # استخدم مفتاح سري قوي
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# نموذج المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# الصفحة الرئيسية
@app.route('/')
def home():
    return redirect(url_for('login'))


# صفحة التسجيل
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username,
                                    password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')


# الصفحة الشخصية للمستخدم
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))


# صفحة البحث عن الأصدقاء
@app.route('/search', methods=['GET', 'POST'])
def search():
    users = User.query.all()
    if request.method == 'POST':
        query = request.form['query']
        users = User.query.filter(User.username.like(f'%{query}%')).all()
    return render_template('search.html', users=users)


# تشغيل التطبيق
if __name__ == '__main__':
    db.create_all()  # إنشاء قاعدة البيانات إذا لم تكن موجودة
    app.run(host='0.0.0.0', port=3000)
