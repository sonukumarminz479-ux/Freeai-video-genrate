#!/bin/bash

# Freeai Video Generator - Setup Script

echo "========================================"
echo "Freeai Video Generator - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python version: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ "$?" -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

if [ "$?" -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel

if [ "$?" -ne 0 ]; then
    echo "❌ Failed to upgrade pip"
    exit 1
fi

echo "✅ pip upgraded"
echo ""

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

if [ "$?" -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env 2>/dev/null || cat > .env << 'EOF'
# Flask Configuration
FLASK_ENV=development
FLASK_APP=main.py
SECRET_KEY=your-secret-key-change-in-production

# Database
DATABASE_URL=sqlite:///app.db

# API Keys
OPENAI_API_KEY=your_openai_key_here
STABILITY_API_KEY=your_stability_key_here
HUGGING_FACE_API_KEY=your_hugging_face_key_here

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
    echo "✅ .env file created (Please update API keys)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "========================================"
echo "✨ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Run the application with: python main.py"
echo "3. Visit http://localhost:5000"
echo ""
echo "To activate the virtual environment again, run:"
echo "source venv/bin/activate (on macOS/Linux)"
echo "venv\\Scripts\\activate (on Windows)"
echo ""
