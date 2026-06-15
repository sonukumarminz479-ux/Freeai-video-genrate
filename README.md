# Freeai Video Generator

AI-powered Video, Image, and 3D Model Generator - Free with Login

## Features

✨ **Video Generation** - Create AI-generated videos from text prompts

🖼️ **Image Generation** - Generate high-quality images using AI

🎭 **3D Model Generation** - Create 3D models from descriptions

🔐 **Free with Login** - Free access with user authentication

🚀 **Fast Processing** - Optimized for quick generation times

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API keys for AI services (OpenAI, Stability AI, etc.)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sonukumarminz479-ux/Freeai-video-genrate.git
cd Freeai-video-genrate
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key_here
STABILITY_API_KEY=your_stability_key_here
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your_secret_key_here
```

### 6. Run the application

```bash
python main.py
```

The application will start on `http://localhost:5000`

## Quick Setup Script

```bash
bash setup.sh
```

## Project Structure

```
Freeai-video-genrate/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── setup.sh
├── README.md
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── generators/
│   │   ├── __init__.py
│   │   ├── video_generator.py
│   │   ├── image_generator.py
│   │   └── model_3d_generator.py
│   └── routes/
│       ├── __init__.py
│       └── api.py
├── templates/
│   ├── index.html
│   ├── login.html
│   └── dashboard.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## Usage

### 1. Create an account

Visit `http://localhost:5000/register` and create a new account

### 2. Login

Login with your credentials at `http://localhost:5000/login`

### 3. Generate Content

- **Video**: Go to Video tab, enter prompt, click Generate
- **Image**: Go to Image tab, enter prompt, click Generate
- **3D Model**: Go to 3D Model tab, enter description, click Generate

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Generation
- `POST /api/generate/video` - Generate video
- `POST /api/generate/image` - Generate image
- `POST /api/generate/model3d` - Generate 3D model
- `GET /api/history` - Get generation history

## Configuration

Edit `config.py` to customize:

- Database settings
- API timeouts
- Generation parameters
- Model selection

## Troubleshooting

### Port already in use
```bash
python main.py --port 8000
```

### Missing dependencies
```bash
pip install --upgrade -r requirements.txt
```

### API key errors
Verify your `.env` file has correct API keys

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

- [ ] Add video editing features
- [ ] Support for multiple AI models
- [ ] Batch generation
- [ ] WebUI improvements
- [ ] Mobile app
- [ ] Cloud deployment

---

**Made with ❤️ by Sonu Kumar**
