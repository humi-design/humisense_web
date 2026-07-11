import os
import json
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

from config import config
from extensions import db, init_extensions
from models import Contact, Newsletter, CourseEnrollment, ResearchSubmission, User, Admin
from forms import ContactForm, NewsletterForm, EnrollmentForm, ResearchSubmissionForm, DemoRequestForm


# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


def save_json_data(filename, data):
    """Save data to JSON file."""
    with open(os.path.join('data', f'{filename}.json'), 'w') as f:
        json.dump(data, f, indent=2)

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
    return render_template('about.html', team=team_data)


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


# =====================================================
# ADMIN ROUTES
# =====================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            admin.last_login = datetime.now(timezone.utc)
            db.session.commit()
            flash('Welcome to the admin panel!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard."""
    # Get counts
    products_count = len(products_data)
    services_count = len(services_data)
    courses_count = len(courses_data)
    research_count = len(research_data)
    testimonials_count = len(testimonials_data)
    contacts_count = Contact.query.count()
    newsletter_count = Newsletter.query.count()
    enrollments_count = CourseEnrollment.query.count()
    research_submissions_count = ResearchSubmission.query.count()
    
    # Get recent contacts
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         products_count=products_count,
                         services_count=services_count,
                         courses_count=courses_count,
                         research_count=research_count,
                         testimonials_count=testimonials_count,
                         contacts_count=contacts_count,
                         newsletter_count=newsletter_count,
                         enrollments_count=enrollments_count,
                         research_submissions_count=research_submissions_count,
                         recent_contacts=recent_contacts)


# =====================================================
# ADMIN: PRODUCTS MANAGEMENT
# =====================================================

@app.route('/admin/products')
@admin_required
def admin_products():
    """List all products."""
    return render_template('admin/products.html', products=products_data)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_product_add():
    """Add new product."""
    if request.method == 'POST':
        new_product = {
            'id': request.form.get('id'),
            'name': request.form.get('name'),
            'tagline': request.form.get('tagline'),
            'description': request.form.get('description'),
            'category': request.form.get('category'),
            'icon': request.form.get('icon', 'box'),
            'color': request.form.get('color', '#6366F1'),
            'features': [f.strip() for f in request.form.get('features', '').split('\n') if f.strip()],
            'benefits': [b.strip() for b in request.form.get('benefits', '').split('\n') if b.strip()],
            'use_cases': [],
            'api_example': {
                'endpoint': request.form.get('api_endpoint', ''),
                'method': 'POST',
                'code': request.form.get('api_code', '')
            },
            'pricing': request.form.get('pricing')
        }
        
        # Parse use cases
        use_case_titles = request.form.getlist('use_case_title')
        use_case_descs = request.form.getlist('use_case_desc')
        for i, title in enumerate(use_case_titles):
            if title.strip():
                new_product['use_cases'].append({
                    'title': title.strip(),
                    'description': use_case_descs[i].strip() if i < len(use_case_descs) else ''
                })
        
        products_data.append(new_product)
        save_json_data('products', products_data)
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_edit.html', product=None, action='Add')


@app.route('/admin/products/edit/<product_id>', methods=['GET', 'POST'])
@admin_required
def admin_product_edit(product_id):
    """Edit product."""
    product = next((p for p in products_data if p['id'] == product_id), None)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        product['name'] = request.form.get('name')
        product['tagline'] = request.form.get('tagline')
        product['description'] = request.form.get('description')
        product['category'] = request.form.get('category')
        product['icon'] = request.form.get('icon', 'box')
        product['color'] = request.form.get('color', '#6366F1')
        product['features'] = [f.strip() for f in request.form.get('features', '').split('\n') if f.strip()]
        product['benefits'] = [b.strip() for b in request.form.get('benefits', '').split('\n') if b.strip()]
        product['pricing'] = request.form.get('pricing')
        product['api_example'] = {
            'endpoint': request.form.get('api_endpoint', ''),
            'method': 'POST',
            'code': request.form.get('api_code', '')
        }
        
        # Parse use cases
        use_cases = []
        use_case_titles = request.form.getlist('use_case_title')
        use_case_descs = request.form.getlist('use_case_desc')
        for i, title in enumerate(use_case_titles):
            if title.strip():
                use_cases.append({
                    'title': title.strip(),
                    'description': use_case_descs[i].strip() if i < len(use_case_descs) else ''
                })
        product['use_cases'] = use_cases
        
        save_json_data('products', products_data)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_edit.html', product=product, action='Edit')


@app.route('/admin/products/delete/<product_id>', methods=['POST'])
@admin_required
def admin_product_delete(product_id):
    """Delete product."""
    global products_data
    products_data = [p for p in products_data if p['id'] != product_id]
    save_json_data('products', products_data)
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))


# =====================================================
# ADMIN: SERVICES MANAGEMENT
# =====================================================

@app.route('/admin/services')
@admin_required
def admin_services():
    """List all services."""
    return render_template('admin/services.html', services=services_data)


@app.route('/admin/services/add', methods=['GET', 'POST'])
@admin_required
def admin_service_add():
    """Add new service."""
    if request.method == 'POST':
        new_service = {
            'id': request.form.get('id'),
            'name': request.form.get('name'),
            'icon': request.form.get('icon', 'settings'),
            'color': request.form.get('color', '#6366F1'),
            'short_description': request.form.get('short_description'),
            'description': request.form.get('description'),
            'features': [f.strip() for f in request.form.get('features', '').split('\n') if f.strip()],
            'technologies': [t.strip() for t in request.form.get('technologies', '').split(',') if t.strip()],
            'starting_price': request.form.get('starting_price')
        }
        
        services_data.append(new_service)
        save_json_data('services', services_data)
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/service_edit.html', service=None, action='Add')


@app.route('/admin/services/edit/<service_id>', methods=['GET', 'POST'])
@admin_required
def admin_service_edit(service_id):
    """Edit service."""
    service = next((s for s in services_data if s['id'] == service_id), None)
    if not service:
        flash('Service not found', 'error')
        return redirect(url_for('admin_services'))
    
    if request.method == 'POST':
        service['name'] = request.form.get('name')
        service['icon'] = request.form.get('icon', 'settings')
        service['color'] = request.form.get('color', '#6366F1')
        service['short_description'] = request.form.get('short_description')
        service['description'] = request.form.get('description')
        service['features'] = [f.strip() for f in request.form.get('features', '').split('\n') if f.strip()]
        service['technologies'] = [t.strip() for t in request.form.get('technologies', '').split(',') if t.strip()]
        service['starting_price'] = request.form.get('starting_price')
        
        save_json_data('services', services_data)
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/service_edit.html', service=service, action='Edit')


@app.route('/admin/services/delete/<service_id>', methods=['POST'])
@admin_required
def admin_service_delete(service_id):
    """Delete service."""
    global services_data
    services_data = [s for s in services_data if s['id'] != service_id]
    save_json_data('services', services_data)
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_services'))


# =====================================================
# ADMIN: COURSES MANAGEMENT
# =====================================================

@app.route('/admin/courses')
@admin_required
def admin_courses():
    """List all courses."""
    return render_template('admin/courses.html', courses=courses_data)


@app.route('/admin/courses/add', methods=['GET', 'POST'])
@admin_required
def admin_course_add():
    """Add new course."""
    if request.method == 'POST':
        new_course = {
            'id': request.form.get('id'),
            'name': request.form.get('name'),
            'icon': request.form.get('icon', 'book'),
            'color': request.form.get('color', '#6366F1'),
            'level': request.form.get('level'),
            'duration': request.form.get('duration'),
            'modules': int(request.form.get('modules', 1)),
            'description': request.form.get('description'),
            'outcomes': [o.strip() for o in request.form.get('outcomes', '').split('\n') if o.strip()],
            'curriculum': []
        }
        
        # Parse curriculum
        module_nums = request.form.getlist('module_num')
        module_titles = request.form.getlist('module_title')
        module_topics_list = request.form.getlist('module_topics')
        
        for i, num in enumerate(module_nums):
            if module_titles[i].strip():
                topics = [t.strip() for t in module_topics_list[i].split('\n') if t.strip()] if i < len(module_topics_list) else []
                new_course['curriculum'].append({
                    'module': int(num) if num else i + 1,
                    'title': module_titles[i].strip(),
                    'topics': topics
                })
        
        courses_data.append(new_course)
        save_json_data('courses', courses_data)
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    return render_template('admin/course_edit.html', course=None, action='Add')


@app.route('/admin/courses/edit/<course_id>', methods=['GET', 'POST'])
@admin_required
def admin_course_edit(course_id):
    """Edit course."""
    course = next((c for c in courses_data if c['id'] == course_id), None)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('admin_courses'))
    
    if request.method == 'POST':
        course['name'] = request.form.get('name')
        course['icon'] = request.form.get('icon', 'book')
        course['color'] = request.form.get('color', '#6366F1')
        course['level'] = request.form.get('level')
        course['duration'] = request.form.get('duration')
        course['modules'] = int(request.form.get('modules', len(course.get('curriculum', []))))
        course['description'] = request.form.get('description')
        course['outcomes'] = [o.strip() for o in request.form.get('outcomes', '').split('\n') if o.strip()]
        
        # Parse curriculum
        curriculum = []
        module_nums = request.form.getlist('module_num')
        module_titles = request.form.getlist('module_title')
        module_topics_list = request.form.getlist('module_topics')
        
        for i, num in enumerate(module_nums):
            if module_titles[i].strip():
                topics = [t.strip() for t in module_topics_list[i].split('\n') if t.strip()] if i < len(module_topics_list) else []
                curriculum.append({
                    'module': int(num) if num else i + 1,
                    'title': module_titles[i].strip(),
                    'topics': topics
                })
        course['curriculum'] = curriculum
        
        save_json_data('courses', courses_data)
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin_courses'))
    
    return render_template('admin/course_edit.html', course=course, action='Edit')


@app.route('/admin/courses/delete/<course_id>', methods=['POST'])
@admin_required
def admin_course_delete(course_id):
    """Delete course."""
    global courses_data
    courses_data = [c for c in courses_data if c['id'] != course_id]
    save_json_data('courses', courses_data)
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin_courses'))


# =====================================================
# ADMIN: RESEARCH MANAGEMENT
# =====================================================

@app.route('/admin/research')
@admin_required
def admin_research():
    """List all research papers."""
    return render_template('admin/research.html', research=research_data)


@app.route('/admin/research/add', methods=['GET', 'POST'])
@admin_required
def admin_research_add():
    """Add new research paper."""
    if request.method == 'POST':
        authors_list = [a.strip() for a in request.form.get('authors', '').split(',') if a.strip()]
        new_research = {
            'id': request.form.get('id'),
            'title': request.form.get('title'),
            'authors': authors_list,
            'institution': request.form.get('institution'),
            'year': int(request.form.get('year')),
            'abstract': request.form.get('abstract'),
            'keywords': [k.strip() for k in request.form.get('keywords', '').split(',') if k.strip()],
            'research_area': request.form.get('research_area'),
            'pdf_url': request.form.get('pdf_url', '#'),
            'citation': request.form.get('citation')
        }
        
        research_data.append(new_research)
        save_json_data('research', research_data)
        flash('Research paper added successfully!', 'success')
        return redirect(url_for('admin_research'))
    
    return render_template('admin/research_edit.html', paper=None, action='Add')


@app.route('/admin/research/edit/<paper_id>', methods=['GET', 'POST'])
@admin_required
def admin_research_edit(paper_id):
    """Edit research paper."""
    paper = next((r for r in research_data if r['id'] == paper_id), None)
    if not paper:
        flash('Research paper not found', 'error')
        return redirect(url_for('admin_research'))
    
    if request.method == 'POST':
        paper['title'] = request.form.get('title')
        paper['authors'] = [a.strip() for a in request.form.get('authors', '').split(',') if a.strip()]
        paper['institution'] = request.form.get('institution')
        paper['year'] = int(request.form.get('year'))
        paper['abstract'] = request.form.get('abstract')
        paper['keywords'] = [k.strip() for k in request.form.get('keywords', '').split(',') if k.strip()]
        paper['research_area'] = request.form.get('research_area')
        paper['pdf_url'] = request.form.get('pdf_url', '#')
        paper['citation'] = request.form.get('citation')
        
        save_json_data('research', research_data)
        flash('Research paper updated successfully!', 'success')
        return redirect(url_for('admin_research'))
    
    return render_template('admin/research_edit.html', paper=paper, action='Edit')


@app.route('/admin/research/delete/<paper_id>', methods=['POST'])
@admin_required
def admin_research_delete(paper_id):
    """Delete research paper."""
    global research_data
    research_data = [r for r in research_data if r['id'] != paper_id]
    save_json_data('research', research_data)
    flash('Research paper deleted successfully!', 'success')
    return redirect(url_for('admin_research'))


# =====================================================
# ADMIN: TESTIMONIALS MANAGEMENT
# =====================================================

@app.route('/admin/testimonials')
@admin_required
def admin_testimonials():
    """List all testimonials."""
    return render_template('admin/testimonials.html', testimonials=testimonials_data)


@app.route('/admin/testimonials/add', methods=['GET', 'POST'])
@admin_required
def admin_testimonial_add():
    """Add new testimonial."""
    if request.method == 'POST':
        max_id = max([t.get('id', 0) for t in testimonials_data], default=0)
        new_testimonial = {
            'id': max_id + 1,
            'name': request.form.get('name'),
            'role': request.form.get('role'),
            'company': request.form.get('company'),
            'avatar': ''.join([n[0] for n in request.form.get('name', 'AB').split()]).upper()[:2],
            'quote': request.form.get('quote'),
            'rating': int(request.form.get('rating', 5))
        }
        
        testimonials_data.append(new_testimonial)
        save_json_data('testimonials', testimonials_data)
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('admin_testimonials'))
    
    return render_template('admin/testimonial_edit.html', testimonial=None, action='Add')


@app.route('/admin/testimonials/edit/<int:testimonial_id>', methods=['GET', 'POST'])
@admin_required
def admin_testimonial_edit(testimonial_id):
    """Edit testimonial."""
    testimonial = next((t for t in testimonials_data if t.get('id') == testimonial_id), None)
    if not testimonial:
        flash('Testimonial not found', 'error')
        return redirect(url_for('admin_testimonials'))
    
    if request.method == 'POST':
        testimonial['name'] = request.form.get('name')
        testimonial['role'] = request.form.get('role')
        testimonial['company'] = request.form.get('company')
        testimonial['avatar'] = ''.join([n[0] for n in request.form.get('name', 'AB').split()]).upper()[:2]
        testimonial['quote'] = request.form.get('quote')
        testimonial['rating'] = int(request.form.get('rating', 5))
        
        save_json_data('testimonials', testimonials_data)
        flash('Testimonial updated successfully!', 'success')
        return redirect(url_for('admin_testimonials'))
    
    return render_template('admin/testimonial_edit.html', testimonial=testimonial, action='Edit')


@app.route('/admin/testimonials/delete/<int:testimonial_id>', methods=['POST'])
@admin_required
def admin_testimonial_delete(testimonial_id):
    """Delete testimonial."""
    global testimonials_data
    testimonials_data = [t for t in testimonials_data if t.get('id') != testimonial_id]
    save_json_data('testimonials', testimonials_data)
    flash('Testimonial deleted successfully!', 'success')
    return redirect(url_for('admin_testimonials'))


# =====================================================
# ADMIN: TEAM MANAGEMENT
# =====================================================

# Load team data (hardcoded in about page, we'll create a JSON file)
def load_team_data():
    try:
        with open('data/team.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [
            {'name': 'Dr. Sarah Chen', 'role': 'CEO & Co-Founder', 'bio': 'Former AI Research Lead at Google with 15+ years experience in machine learning and natural language processing.'},
            {'name': 'Michael Rodriguez', 'role': 'CTO & Co-Founder', 'bio': 'Ex-Stanford ML researcher specializing in multi-agent systems and autonomous AI agents.'},
            {'name': 'Dr. Emily Watson', 'role': 'Chief Scientist', 'bio': 'Leading expert in generative AI and neural architecture design with numerous publications.'},
            {'name': 'James Kim', 'role': 'VP of Engineering', 'bio': 'Built AI infrastructure at scale for Fortune 500 companies for over a decade.'},
            {'name': 'Dr. Priya Patel', 'role': 'Head of Research', 'bio': 'Published researcher in explainable AI and AI safety with PhD from MIT.'},
            {'name': 'Alex Thompson', 'role': 'VP of Product', 'bio': 'Product leader with experience launching AI products used by millions.'}
        ]

team_data = load_team_data()

@app.route('/admin/team')
@admin_required
def admin_team():
    """List all team members."""
    return render_template('admin/team.html', team=team_data)


@app.route('/admin/team/add', methods=['GET', 'POST'])
@admin_required
def admin_team_add():
    """Add new team member."""
    global team_data
    if request.method == 'POST':
        new_member = {
            'name': request.form.get('name'),
            'role': request.form.get('role'),
            'bio': request.form.get('bio')
        }
        
        team_data.append(new_member)
        save_json_data('team', team_data)
        flash('Team member added successfully!', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/team_edit.html', member=None, action='Add')


@app.route('/admin/team/edit/<int:member_index>', methods=['GET', 'POST'])
@admin_required
def admin_team_edit(member_index):
    """Edit team member."""
    global team_data
    if member_index < 0 or member_index >= len(team_data):
        flash('Team member not found', 'error')
        return redirect(url_for('admin_team'))
    
    if request.method == 'POST':
        team_data[member_index]['name'] = request.form.get('name')
        team_data[member_index]['role'] = request.form.get('role')
        team_data[member_index]['bio'] = request.form.get('bio')
        
        save_json_data('team', team_data)
        flash('Team member updated successfully!', 'success')
        return redirect(url_for('admin_team'))
    
    return render_template('admin/team_edit.html', member=team_data[member_index], member_index=member_index, action='Edit')


@app.route('/admin/team/delete/<int:member_index>', methods=['POST'])
@admin_required
def admin_team_delete(member_index):
    """Delete team member."""
    global team_data
    if 0 <= member_index < len(team_data):
        team_data.pop(member_index)
        save_json_data('team', team_data)
        flash('Team member deleted successfully!', 'success')
    return redirect(url_for('admin_team'))


# =====================================================
# ADMIN: CONTACTS MANAGEMENT
# =====================================================

@app.route('/admin/contacts')
@admin_required
def admin_contacts():
    """List all contact submissions."""
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)


@app.route('/admin/contacts/<int:contact_id>/status', methods=['POST'])
@admin_required
def admin_contact_status(contact_id):
    """Update contact status."""
    contact = Contact.query.get_or_404(contact_id)
    contact.status = request.form.get('status', 'new')
    db.session.commit()
    flash('Contact status updated!', 'success')
    return redirect(url_for('admin_contacts'))


@app.route('/admin/contacts/delete/<int:contact_id>', methods=['POST'])
@admin_required
def admin_contact_delete(contact_id):
    """Delete contact."""
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted!', 'success')
    return redirect(url_for('admin_contacts'))


# =====================================================
# ADMIN: NEWSLETTER MANAGEMENT
# =====================================================

@app.route('/admin/newsletter')
@admin_required
def admin_newsletter():
    """List all newsletter subscribers."""
    subscribers = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    return render_template('admin/newsletter.html', subscribers=subscribers)


@app.route('/admin/newsletter/toggle/<int:subscriber_id>', methods=['POST'])
@admin_required
def admin_newsletter_toggle(subscriber_id):
    """Toggle newsletter subscription status."""
    subscriber = Newsletter.query.get_or_404(subscriber_id)
    subscriber.is_active = not subscriber.is_active
    db.session.commit()
    flash(f"Subscription {'activated' if subscriber.is_active else 'deactivated'}!", 'success')
    return redirect(url_for('admin_newsletter'))


@app.route('/admin/newsletter/delete/<int:subscriber_id>', methods=['POST'])
@admin_required
def admin_newsletter_delete(subscriber_id):
    """Delete newsletter subscriber."""
    subscriber = Newsletter.query.get_or_404(subscriber_id)
    db.session.delete(subscriber)
    db.session.commit()
    flash('Subscriber deleted!', 'success')
    return redirect(url_for('admin_newsletter'))


# =====================================================
# ADMIN: ENROLLMENTS MANAGEMENT
# =====================================================

@app.route('/admin/enrollments')
@admin_required
def admin_enrollments():
    """List all course enrollments."""
    enrollments = CourseEnrollment.query.order_by(CourseEnrollment.enrolled_at.desc()).all()
    return render_template('admin/enrollments.html', enrollments=enrollments, courses=courses_data)


@app.route('/admin/enrollments/<int:enrollment_id>/status', methods=['POST'])
@admin_required
def admin_enrollment_status(enrollment_id):
    """Update enrollment status."""
    enrollment = CourseEnrollment.query.get_or_404(enrollment_id)
    enrollment.status = request.form.get('status', 'pending')
    db.session.commit()
    flash('Enrollment status updated!', 'success')
    return redirect(url_for('admin_enrollments'))


@app.route('/admin/enrollments/delete/<int:enrollment_id>', methods=['POST'])
@admin_required
def admin_enrollment_delete(enrollment_id):
    """Delete enrollment."""
    enrollment = CourseEnrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    flash('Enrollment deleted!', 'success')
    return redirect(url_for('admin_enrollments'))


# =====================================================
# ADMIN: RESEARCH SUBMISSIONS MANAGEMENT
# =====================================================

@app.route('/admin/research-submissions')
@admin_required
def admin_research_submissions():
    """List all research submissions."""
    submissions = ResearchSubmission.query.order_by(ResearchSubmission.submitted_at.desc()).all()
    return render_template('admin/research_submissions.html', submissions=submissions)


@app.route('/admin/research-submissions/<int:submission_id>/status', methods=['POST'])
@admin_required
def admin_research_submission_status(submission_id):
    """Update research submission status."""
    submission = ResearchSubmission.query.get_or_404(submission_id)
    submission.status = request.form.get('status', 'submitted')
    db.session.commit()
    flash('Submission status updated!', 'success')
    return redirect(url_for('admin_research_submissions'))


@app.route('/admin/research-submissions/delete/<int:submission_id>', methods=['POST'])
@admin_required
def admin_research_submission_delete(submission_id):
    """Delete research submission."""
    submission = ResearchSubmission.query.get_or_404(submission_id)
    db.session.delete(submission)
    db.session.commit()
    flash('Submission deleted!', 'success')
    return redirect(url_for('admin_research_submissions'))


# =====================================================
# ADMIN: SETTINGS
# =====================================================

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    """Admin settings."""
    admin = Admin.query.get(session['admin_id'])
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not admin.check_password(current_password):
                flash('Current password is incorrect', 'error')
            elif new_password != confirm_password:
                flash('New passwords do not match', 'error')
            elif len(new_password) < 6:
                flash('Password must be at least 6 characters', 'error')
            else:
                admin.set_password(new_password)
                db.session.commit()
                flash('Password changed successfully!', 'success')
        
        elif action == 'update_profile':
            admin.email = request.form.get('email')
            db.session.commit()
            flash('Profile updated successfully!', 'success')
    
    return render_template('admin/settings.html', admin=admin)


@app.route('/admin/create-user', methods=['GET', 'POST'])
@admin_required
def admin_create_user():
    """Create new admin user."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if Admin.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        else:
            new_admin = Admin(username=username, email=email)
            new_admin.set_password(password)
            db.session.add(new_admin)
            db.session.commit()
            flash(f'Admin user "{username}" created successfully!', 'success')
            return redirect(url_for('admin_settings'))
    
    return render_template('admin/create_user.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin', email='admin@humisense.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('Default admin created: admin / admin123')
    app.run(host='0.0.0.0', port=5000, debug=True)