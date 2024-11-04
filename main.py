from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)

# Модели данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    events = db.relationship('Event', backref='organizer', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    participants = db.relationship('Participant', backref='event', lazy=True)
    tickets = db.relationship('Ticket', backref='event', lazy=True)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

# Представления и маршруты
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка на существование пользователя с таким email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User with this email already exists.', 'danger')
            return redirect(url_for('register'))

        user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        event = Event(name=name, date=datetime.strptime(date, '%Y-%m-%d').date(), organizer=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)

@app.route('/event/<int:event_id>/register', methods=['POST'])
def register_participant(event_id):
    event = Event.query.get_or_404(event_id)
    name = request.form.get('name')
    email = request.form.get('email')
    participant = Participant(name=name, email=email, event=event)
    db.session.add(participant)
    db.session.commit()
    flash('Registration successful!', 'success')
    return redirect(url_for('event_details', event_id=event_id))

@app.route('/event/<int:event_id>/buy_ticket', methods=['POST'])
def buy_ticket(event_id):
    event = Event.query.get_or_404(event_id)
    ticket = Ticket(price=10.0, event=event)  # Здесь можно установить цену билета
    db.session.add(ticket)
    db.session.commit()
    flash('Ticket purchased successfully!', 'success')
    return redirect(url_for('event_details', event_id=event_id))

# Функция для отправки уведомлений (пример)
def send_notification(event, recipient):
    # Здесь можно реализовать логику отправки уведомлений
    print(f'Notification sent for event "{event.name}" to {recipient}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)