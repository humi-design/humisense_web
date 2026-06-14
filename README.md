# HUMISENSE - AI-First Technology Company Website

Building the Future with AI

## Overview

HUMISENSE is a cutting-edge AI technology company specializing in developing intelligent solutions for businesses and individuals. Our platform provides APIs, tools, and services powered by state-of-the-art artificial intelligence.

## Tech Stack

### Backend
- **Flask** - Python web framework
- **Jinja2** - Template engine
- **SQLAlchemy** - ORM for database operations

### Frontend
- **Tailwind CSS** - Utility-first CSS framework
- **GSAP** - Animation library
- **ScrollTrigger** - Scroll-based animations
- **Lenis** - Smooth scrolling
- **Swiper** - Carousel/slider
- **CountUp.js** - Animated counters
- **JustValidate** - Form validation
- **Fancybox** - Lightbox gallery
- **SweetAlert2** - Alert dialogs
- **ApexCharts** - Charts and data visualization
- **Lucide Icons** - Icon library
- **Headroom.js** - Hide/show header on scroll
- **Three.js** - 3D graphics

## Project Structure

```
humisense_web/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── models.py           # Database models
├── forms.py            # WTForms definitions
├── extensions.py       # Flask extensions
├── templates/          # Jinja2 templates
│   ├── base.html
│   ├── home.html
│   ├── products.html
│   ├── services.html
│   ├── courses.html
│   ├── research.html
│   ├── about.html
│   ├── contact.html
│   ├── product_detail.html
│   ├── course_detail.html
│   ├── 404.html
│   ├── 500.html
│   └── components/
├── static/
│   ├── css/
│   └── js/
├── data/               # JSON data files
└── docs/               # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/humi-design/humisense_web.git
cd humisense_web
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Environment Variables

- `SECRET_KEY` - Flask secret key for sessions
- `DATABASE_URL` - PostgreSQL database connection string
- `FLASK_ENV` - Development or production
- `MAIL_SERVER` - SMTP server for emails
- `MAIL_PORT` - SMTP port
- `MAIL_USERNAME` - SMTP username
- `MAIL_PASSWORD` - SMTP password

## Features

### Pages
- **Home** - Landing page with hero, features, and testimonials
- **Products** - AI product showcase
- **Services** - Professional AI services
- **Courses** - Educational courses and training
- **Research** - Research papers and publications
- **About** - Company information
- **Contact** - Contact forms and information

### Products
- HumiSense Voice API
- Sentinel Chat
- HumiSense Agent Studio
- HumiSense Analytics AI
- HumiSense Research Assistant

### Services
- Web Development
- Mobile App Development
- AI Automation
- Agentic AI
- AI Agents
- Machine Learning
- Data Science
- Power BI
- Analytics & Reporting
- AI Consulting
- Cloud Deployment
- MLOps

### Courses
- Python for AI
- Machine Learning
- Deep Learning
- Generative AI
- LLM Engineering
- Prompt Engineering
- AI Agents
- Data Science
- Power BI
- Flask Development
- MLOps

## Development

### Running Locally

```bash
# Development mode
export FLASK_ENV=development
python app.py

# Production mode (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Database Migrations

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Deployment

The application can be deployed to any WSGI-compatible server:

### Docker
```bash
docker build -t humisense_web .
docker run -p 8000:8000 humisense_web
```

### Manual
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## License

This project is proprietary software. All rights reserved.

## Contact

- Website: https://humisense.com
- Email: contact@humisense.com

---

*Building the Future with AI*
