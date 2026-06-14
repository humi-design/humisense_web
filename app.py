import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

from config import config
from extensions import init_extensions
from models import db, Contact, Newsletter, CourseEnrollment, ResearchSubmission, User
from forms import ContactForm, NewsletterForm, EnrollmentForm, ResearchSubmissionForm, DemoRequestForm

# Create Flask application
app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_ENV', 'default')])

# Initialize extensions
db = init_extensions(app)

# Load data files
def load_data(filename):
    """Load JSON data from data directory."""
    try:
        with open(os.path.join('data', f'{filename}.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Data for pages
products_data = load_data('products')
services_data = load_data('services')
courses_data = load_data('courses')
research_data = load_data('research')
testimonials_data = load_data('testimonials')


# Page Routes
@app.route('/')
def home():
    """Home page."""
    stats = [
        {'value': 500, 'suffix': '+', 'label': 'AI Models Deployed'},
        {'value': 98, 'suffix': '%', 'label': 'Customer Satisfaction'},
        {'value': 50, 'suffix': '+', 'label': 'Enterprise Clients'},
        {'value': 10, 'suffix': 'M+', 'label': 'API Calls Monthly'}
    ]
    return render_template('home.html', 
                         products=products_data[:3],
                         stats=stats,
                         testimonials=testimonials_data[:6])


@app.route('/products')
def products():
    """Products listing page."""
    return render_template('products.html', products=products_data)


@app.route('/products/<product_id>')
def product_detail(product_id):
    """Individual product detail page."""
    product = next((p for p in products_data if p['id'] == product_id), None)
    if not product:
        return render_template('404.html'), 404
    return render_template('product_detail.html', product=product)


@app.route('/services')
def services():
    """Services listing page."""
    return render_template('services.html', services=services_data)


@app.route('/courses')
def courses():
    """Courses listing page."""
    return render_template('courses.html', courses=courses_data)


@app.route('/courses/<course_id>')
def course_detail(course_id):
    """Individual course detail page."""
    course = next((c for c in courses_data if c['id'] == course_id), None)
    if not course:
        return render_template('404.html'), 404
    return render_template('course_detail.html', course=course)


@app.route('/research')
def research():
    """Research center page."""
    return render_template('research.html', 
                         research=research_data,
                         research_areas=[
                             {'id': 'agentic_ai', 'name': 'Agentic AI', 'description': 'Developing autonomous AI agents that can reason, plan, and execute tasks independently.'},
                             {'id': 'multi_agent', 'name': 'Multi-Agent Systems', 'description': 'Studying coordination and collaboration between multiple AI agents.'},
                             {'id': 'generative_ai', 'name': 'Generative AI', 'description': 'Creating AI systems capable of producing original content across modalities.'},
                             {'id': 'explainable_ai', 'name': 'Explainable AI', 'description': 'Making AI decisions transparent and interpretable.'},
                             {'id': 'healthcare_ai', 'name': 'Healthcare AI', 'description': 'Applying AI to improve healthcare outcomes and diagnostics.'},
                             {'id': 'nlp', 'name': 'Natural Language Processing', 'description': 'Advancing understanding and generation of human language.'},
                             {'id': 'computer_vision', 'name': 'Computer Vision', 'description': 'Teaching machines to interpret and understand visual information.'},
                             {'id': 'ai_accessibility', 'name': 'AI Accessibility', 'description': 'Ensuring AI technologies are accessible to all users.'}
                         ])


@app.route('/about')
def about():
    """About page."""
    team = [
        {'name': 'Dr. Sarah Chen', 'role': 'CEO & Co-Founder', 'bio': 'Former AI Research Lead at Google with 15+ years experience in machine learning and natural language processing.'},
        {'name': 'Michael Rodriguez', 'role': 'CTO & Co-Founder', 'bio': 'Ex-Stanford ML researcher specializing in multi-agent systems and autonomous AI agents.'},
        {'name': 'Dr. Emily Watson', 'role': 'Chief Scientist', 'bio': 'Leading expert in generative AI and neural architecture design with numerous publications.'},
        {'name': 'James Kim', 'role': 'VP of Engineering', 'bio': 'Built AI infrastructure at scale for Fortune 500 companies for over a decade.'},
        {'name': 'Dr. Priya Patel', 'role': 'Head of Research', 'bio': 'Published researcher in explainable AI and AI safety with PhD from MIT.'},
        {'name': 'Alex Thompson', 'role': 'VP of Product', 'bio': 'Product leader with experience launching AI products used by millions.'}
    ]
    return render_template('about.html', team=team)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form."""
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Thank you for your message! We will get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


# API Routes
@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    """Newsletter subscription endpoint."""
    form = NewsletterForm()
    if form.validate_on_submit():
        existing = Newsletter.query.filter_by(email=form.email.data).first()
        if existing:
            if existing.is_active:
                return jsonify({'success': True, 'message': 'Already subscribed!'})
            existing.is_active = True
            db.session.commit()
        else:
            subscriber = Newsletter(email=form.email.data)
            db.session.add(subscriber)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Successfully subscribed!'})
    return jsonify({'success': False, 'message': 'Invalid email address'}), 400


@app.route('/api/enroll', methods=['POST'])
def enroll_course():
    """Course enrollment endpoint."""
    form = EnrollmentForm()
    if form.validate_on_submit():
        enrollment = CourseEnrollment(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            course_id=request.json.get('course_id') if request.is_json else None,
            experience_level=form.experience_level.data,
            goals=form.goals.data
        )
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Enrollment submitted! We will contact you shortly.'})
    return jsonify({'success': False, 'message': 'Please check your information and try again'}), 400


@app.route('/api/research', methods=['POST'])
def submit_research():
    """Research submission endpoint."""
    form = ResearchSubmissionForm()
    if form.validate_on_submit():
        submission = ResearchSubmission(
            title=form.title.data,
            authors=form.authors.data,
            email=form.email.data,
            institution=form.institution.data,
            research_area=form.research_area.data,
            abstract=form.abstract.data,
            keywords=form.keywords.data
        )
        db.session.add(submission)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Research submitted successfully!'})
    return jsonify({'success': False, 'message': 'Please check your information and try again'}), 400


@app.route('/api/demo', methods=['POST'])
def request_demo():
    """Demo request endpoint."""
    form = DemoRequestForm()
    if form.validate_on_submit():
        # Store demo request
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            company=form.company.data,
            phone=form.phone.data,
            subject=f'Demo Request: {form.product.data}',
            message=f"Use Case: {form.use_case.data}\nPreferred Time: {form.preferred_time.data}"
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Demo request received! Our team will contact you soon.'})
    return jsonify({'success': False, 'message': 'Please check your information and try again'}), 400


# Sitemap and SEO
@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml."""
    from flask import Response
    pages = [
        {'loc': url_for('home', _external=True), 'priority': '1.0'},
        {'loc': url_for('products', _external=True), 'priority': '0.9'},
        {'loc': url_for('services', _external=True), 'priority': '0.9'},
        {'loc': url_for('courses', _external=True), 'priority': '0.9'},
        {'loc': url_for('research', _external=True), 'priority': '0.8'},
        {'loc': url_for('about', _external=True), 'priority': '0.7'},
        {'loc': url_for('contact', _external=True), 'priority': '0.8'},
    ]
    for product in products_data:
        pages.append({'loc': url_for('product_detail', product_id=product['id'], _external=True), 'priority': '0.8'})
    for course in courses_data:
        pages.append({'loc': url_for('course_detail', course_id=course['id'], _external=True), 'priority': '0.8'})
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += f'  <url>\n    <loc>{page["loc"]}</loc>\n    <priority>{page["priority"]}</priority>\n    <changefreq>weekly</changefreq>\n  </url>\n'
    xml += '</urlset>'
    
    return Response(xml, mimetype='application/xml')


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# Shell context
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Contact': Contact,
        'Newsletter': Newsletter,
        'CourseEnrollment': CourseEnrollment,
        'ResearchSubmission': ResearchSubmission
    }


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)