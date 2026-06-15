#!/usr/bin/env python
"""Main application entry point"""

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize SQLAlchemy
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== Database Models ====================

from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    generations = db.relationship('Generation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Generation(db.Model):
    """Model for tracking generated content"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    content_type = db.Column(db.String(20), nullable=False)  # video, image, model3d
    prompt = db.Column(db.Text, nullable=False)
    result_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    error_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Generation {self.id} - {self.content_type}>'

# ==================== Login Manager ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            return jsonify({'error': 'All fields are required'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Registration successful'}), 201
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

# ==================== API Routes ====================

@app.route('/api/generate/video', methods=['POST'])
@login_required
def generate_video():
    """Generate video from prompt"""
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    generation = Generation(
        user_id=current_user.id,
        content_type='video',
        prompt=prompt,
        status='pending'
    )
    db.session.add(generation)
    db.session.commit()
    
    # TODO: Integrate with video generation API
    
    return jsonify({
        'message': 'Video generation started',
        'generation_id': generation.id
    }), 202

@app.route('/api/generate/image', methods=['POST'])
@login_required
def generate_image():
    """Generate image from prompt"""
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    generation = Generation(
        user_id=current_user.id,
        content_type='image',
        prompt=prompt,
        status='pending'
    )
    db.session.add(generation)
    db.session.commit()
    
    # TODO: Integrate with image generation API
    
    return jsonify({
        'message': 'Image generation started',
        'generation_id': generation.id
    }), 202

@app.route('/api/generate/model3d', methods=['POST'])
@login_required
def generate_model_3d():
    """Generate 3D model from description"""
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    generation = Generation(
        user_id=current_user.id,
        content_type='model3d',
        prompt=prompt,
        status='pending'
    )
    db.session.add(generation)
    db.session.commit()
    
    # TODO: Integrate with 3D model generation API
    
    return jsonify({
        'message': '3D model generation started',
        'generation_id': generation.id
    }), 202

@app.route('/api/history')
@login_required
def get_history():
    """Get user's generation history"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    generations = Generation.query.filter_by(user_id=current_user.id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    items = [{
        'id': g.id,
        'type': g.content_type,
        'prompt': g.prompt,
        'status': g.status,
        'url': g.result_url,
        'created_at': g.created_at.isoformat()
    } for g in generations.items]
    
    return jsonify({
        'items': items,
        'total': generations.total,
        'pages': generations.pages,
        'current_page': page
    })

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# ==================== App Context ====================

with app.app_context():
    db.create_all()

# ==================== Run ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=app.config['DEBUG'], port=port, host='0.0.0.0')
