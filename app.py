import os
import json
import uuid
import re
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from sqlalchemy import func

from config import config
from extensions import db, init_extensions
from models import (Contact, Newsletter, CourseEnrollment, ResearchSubmission, User, Admin, Lead, SiteSettings, FormLog,
                    Masterclass, MasterclassRegistration, MasterclassAnalytics, MasterclassEmailLog)
from forms import (ContactForm, NewsletterForm, EnrollmentForm, ResearchSubmissionForm, DemoRequestForm,
                   MasterclassForm, MasterclassRegistrationForm, MasterclassSettingsForm)
from services.form_service import FormService
from services.email_service import EmailService


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

# Create all database tables if they don't exist
with app.app_context():
    db.create_all()

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

# Initialize admin user if not exists
def init_admin_user():
    """Create default admin user if not exists."""
    with app.app_context():
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin', email='admin@humisense.com', is_active=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists")

# Call initialization after app is set up
init_admin_user()


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
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'company': request.form.get('company'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message')
        }
        
        lead, error = FormService.submit_contact(data, request.url)
        
        if error:
            flash(error, 'error')
        else:
            flash('Thank you for your message! We will get back to you within 24 hours.', 'success')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)


# API Routes
@app.route('/api/newsletter', methods=['POST'])
def subscribe_newsletter():
    """Newsletter subscription endpoint."""
    email = request.form.get('email') or (request.json.get('email') if request.is_json else None)
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    data = {'email': email}
    lead, error = FormService.submit_newsletter(data, request.url)
    
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    return jsonify({'success': True, 'message': 'Successfully subscribed!'})


@app.route('/api/enroll', methods=['POST'])
def enroll_course():
    """Course enrollment endpoint."""
    data = {}
    
    if request.is_json:
        data = request.json
    else:
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'company': request.form.get('company'),
            'course_id': request.form.get('course_id'),
            'experience_level': request.form.get('experience_level'),
            'goals': request.form.get('goals')
        }
    
    lead, error = FormService.submit_enrollment(data, request.url)
    
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    return jsonify({'success': True, 'message': 'Enrollment submitted! We will contact you shortly.'})


@app.route('/api/research', methods=['POST'])
def submit_research():
    """Research submission endpoint."""
    data = {}
    
    if request.is_json:
        data = request.json
    else:
        data = {
            'title': request.form.get('title'),
            'authors': request.form.get('authors'),
            'email': request.form.get('email'),
            'institution': request.form.get('institution'),
            'research_area': request.form.get('research_area'),
            'abstract': request.form.get('abstract'),
            'keywords': request.form.get('keywords')
        }
    
    lead, error = FormService.submit_research(data, request.url)
    
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    return jsonify({'success': True, 'message': 'Research submitted successfully!'})


@app.route('/api/demo', methods=['POST'])
def request_demo():
    """Demo request endpoint."""
    data = {}
    
    if request.is_json:
        data = request.json
    else:
        data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'company': request.form.get('company'),
            'phone': request.form.get('phone'),
            'product': request.form.get('product'),
            'use_case': request.form.get('use_case'),
            'preferred_time': request.form.get('preferred_time')
        }
    
    lead, error = FormService.submit_demo(data, request.url)
    
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    return jsonify({'success': True, 'message': 'Demo request submitted! We will contact you shortly.'})


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
    unread_leads_count = Lead.query.filter_by(is_archived=False, is_read=False).count()
    
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
                         recent_contacts=recent_contacts,
                         unread_leads_count=unread_leads_count)


# =====================================================
# ADMIN: LEADS MANAGEMENT
# =====================================================

@app.route('/admin/leads')
@admin_required
def admin_leads():
    """List all leads with filtering and search."""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = 20
    form_type = request.args.get('form_type', '')
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    archived = request.args.get('archived', 'false').lower() == 'true'
    
    # Build query
    query = Lead.query
    
    if form_type:
        query = query.filter(Lead.form_type == form_type)
    
    if status:
        query = query.filter(Lead.status == status)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Lead.name.ilike(search_term),
                Lead.email.ilike(search_term),
                Lead.company.ilike(search_term),
                Lead.message.ilike(search_term)
            )
        )
    
    if archived:
        query = query.filter(Lead.is_archived == True)
    else:
        query = query.filter(Lead.is_archived == False)
    
    # Order by newest first
    query = query.order_by(Lead.created_at.desc())
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    leads = pagination.items
    
    # Stats
    total_leads = Lead.query.filter_by(is_archived=False).count()
    unread_leads = Lead.query.filter_by(is_archived=False, is_read=False).count()
    new_leads = Lead.query.filter_by(is_archived=False, status='new').count()
    
    # Count by form type
    contact_count = Lead.query.filter_by(form_type='contact', is_archived=False).count()
    newsletter_count = Lead.query.filter_by(form_type='newsletter', is_archived=False).count()
    enrollment_count = Lead.query.filter_by(form_type='enrollment', is_archived=False).count()
    demo_count = Lead.query.filter_by(form_type='demo', is_archived=False).count()
    research_count = Lead.query.filter_by(form_type='research', is_archived=False).count()
    masterclass_count = Lead.query.filter_by(form_type='masterclass', is_archived=False).count()
    
    return render_template('admin/leads.html',
                         leads=leads,
                         pagination=pagination,
                         total_leads=total_leads,
                         unread_leads=unread_leads,
                         new_leads=new_leads,
                         contact_count=contact_count,
                         newsletter_count=newsletter_count,
                         enrollment_count=enrollment_count,
                         demo_count=demo_count,
                         research_count=research_count,
                         masterclass_count=masterclass_count,
                         current_form_type=form_type,
                         current_status=status,
                         current_search=search,
                         show_archived=archived)


@app.route('/admin/leads/<int:lead_id>')
@admin_required
def admin_lead_detail(lead_id):
    """View lead details."""
    lead = Lead.query.get_or_404(lead_id)
    
    # Mark as read
    if not lead.is_read:
        lead.is_read = True
        db.session.commit()
    
    return render_template('admin/lead_detail.html', lead=lead)


@app.route('/admin/leads/<int:lead_id>/status', methods=['POST'])
@admin_required
def admin_lead_status(lead_id):
    """Update lead status."""
    lead = Lead.query.get_or_404(lead_id)
    lead.status = request.form.get('status', 'new')
    db.session.commit()
    flash('Lead status updated!', 'success')
    return redirect(url_for('admin_lead_detail', lead_id=lead_id))


@app.route('/admin/leads/<int:lead_id>/archive', methods=['POST'])
@admin_required
def admin_lead_archive(lead_id):
    """Archive lead."""
    lead = Lead.query.get_or_404(lead_id)
    lead.is_archived = True
    lead.status = 'archived'
    db.session.commit()
    flash('Lead archived!', 'success')
    return redirect(url_for('admin_leads'))


@app.route('/admin/leads/<int:lead_id>/unarchive', methods=['POST'])
@admin_required
def admin_lead_unarchive(lead_id):
    """Unarchive lead."""
    lead = Lead.query.get_or_404(lead_id)
    lead.is_archived = False
    lead.status = 'new'
    db.session.commit()
    flash('Lead restored!', 'success')
    return redirect(url_for('admin_leads', archived='true'))


@app.route('/admin/leads/<int:lead_id>/delete', methods=['POST'])
@admin_required
def admin_lead_delete(lead_id):
    """Delete lead."""
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    flash('Lead deleted!', 'success')
    return redirect(url_for('admin_leads'))


@app.route('/admin/leads/<int:lead_id>/notes', methods=['POST'])
@admin_required
def admin_lead_notes(lead_id):
    """Update lead notes."""
    lead = Lead.query.get_or_404(lead_id)
    lead.notes = request.form.get('notes', '')
    db.session.commit()
    flash('Notes updated!', 'success')
    return redirect(url_for('admin_lead_detail', lead_id=lead_id))


@app.route('/admin/leads/export')
@admin_required
def admin_leads_export():
    """Export leads to CSV."""
    import csv
    from io import StringIO
    from flask import Response
    
    leads = Lead.query.filter_by(is_archived=False).order_by(Lead.created_at.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Form Type', 'Name', 'Email', 'Phone', 'Company', 'Message', 'Status', 'Created At', 'Source Page', 'IP Address'])
    
    # Data
    for lead in leads:
        writer.writerow([
            lead.id,
            lead.form_type,
            lead.name or '',
            lead.email,
            lead.phone or '',
            lead.company or '',
            lead.message or '',
            lead.status,
            lead.created_at.strftime('%Y-%m-%d %H:%M'),
            lead.source_page or '',
            lead.ip_address or ''
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=leads.csv'}
    )


@app.route('/admin/leads/mark-all-read', methods=['POST'])
@admin_required
def admin_leads_mark_all_read():
    """Mark all leads as read."""
    Lead.query.filter_by(is_archived=False, is_read=False).update({'is_read': True})
    db.session.commit()
    flash('All leads marked as read!', 'success')
    return redirect(url_for('admin_leads'))


# =====================================================
# ADMIN: FORM LOGS
# =====================================================

@app.route('/admin/logs')
@admin_required
def admin_logs():
    """View form submission logs."""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    form_type = request.args.get('form_type', '')
    action = request.args.get('action', '')
    
    query = FormLog.query
    
    if form_type:
        query = query.filter(FormLog.form_type == form_type)
    
    if action:
        query = query.filter(FormLog.action == action)
    
    query = query.order_by(FormLog.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    logs = pagination.items
    
    return render_template('admin/logs.html',
                         logs=logs,
                         pagination=pagination,
                         current_form_type=form_type,
                         current_action=action)


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
        
        elif action == 'update_smtp':
            # Update SMTP settings
            smtp_fields = ['smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'sender_email', 'sender_name']
            for field in smtp_fields:
                value = request.form.get(field, '')
                setting = SiteSettings.query.filter_by(key=field).first()
                if not setting:
                    setting = SiteSettings(key=field, value_type='string')
                    db.session.add(setting)
                setting.set_value(value)
            db.session.commit()
            flash('Email settings saved successfully!', 'success')
        
        elif action == 'test_email':
            test_to = request.form.get('test_email', '')
            if test_to and '@' in test_to:
                from services.email_service import EmailService
                
                # Debug: Check current SMTP settings
                print(f"=== SMTP DEBUG ===")
                for key in ['smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'sender_email', 'sender_name']:
                    setting = SiteSettings.query.filter_by(key=key).first()
                    val = setting.get_value() if setting else None
                    print(f"  {key}: '{val}' (type: {type(val).__name__})")
                print(f"=================")
                
                success = EmailService.test_email(test_to)
                if success:
                    flash(f'Test email sent to {test_to}!', 'success')
                else:
                    flash('Failed to send test email. Check your SMTP settings.', 'error')
            else:
                flash('Please enter a valid email address.', 'error')
    
    # Get SMTP settings for template
    smtp_settings = {}
    for key in ['smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'sender_email', 'sender_name']:
        setting = SiteSettings.query.filter_by(key=key).first()
        smtp_settings[key] = setting.get_value() if setting else ''
    
    return render_template('admin/settings.html', admin=admin, settings=smtp_settings)


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


# =====================================================
# ADMIN: MASTERCLASS MANAGEMENT
# =====================================================

def get_masterclass_setting(key, default=None):
    """Get masterclass module setting from database."""
    setting = SiteSettings.query.filter_by(key=key).first()
    return setting.get_value() if setting else default


def set_masterclass_setting(key, value, value_type='bool'):
    """Set masterclass module setting in database."""
    setting = SiteSettings.query.filter_by(key=key).first()
    if not setting:
        setting = SiteSettings(key=key, value_type=value_type)
        db.session.add(setting)
    setting.set_value(value)
    db.session.commit()


def generate_slug(title):
    """Generate URL-friendly slug from title."""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = slug.strip('-')
    
    # Check for existing slug and make unique if needed
    original_slug = slug
    counter = 1
    while Masterclass.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    return slug


def get_active_masterclass():
    """Get active masterclass for website promotion."""
    if not get_masterclass_setting('masterclass_enable_module', True):
        return None
    
    active_statuses = ['published', 'registration_open', 'live']
    masterclass = Masterclass.query.filter(
        Masterclass.status.in_(active_statuses),
        Masterclass.show_floating_button == True
    ).order_by(Masterclass.date.asc()).first()
    
    return masterclass


@app.context_processor
def inject_masterclass():
    """Inject masterclass data into all templates."""
    active_masterclass = get_active_masterclass()
    return {
        'active_masterclass': active_masterclass,
        'mc_module_enabled': get_masterclass_setting('masterclass_enable_module', True),
        'mc_floating_cta_enabled': get_masterclass_setting('masterclass_enable_floating_cta', True),
        'mc_popup_enabled': get_masterclass_setting('masterclass_enable_popup', True),
        'mc_sticky_banner_enabled': get_masterclass_setting('masterclass_enable_sticky_banner', True),
        'mc_homepage_promotion_enabled': get_masterclass_setting('masterclass_enable_homepage_promotion', True),
    }


@app.route('/admin/masterclasses')
@admin_required
def admin_masterclasses():
    """List all masterclasses."""
    status_filter = request.args.get('status', '')
    
    query = Masterclass.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    masterclasses = query.order_by(Masterclass.date.desc()).all()
    
    # Count by status
    status_counts = {
        'draft': Masterclass.query.filter_by(status='draft').count(),
        'published': Masterclass.query.filter_by(status='published').count(),
        'registration_open': Masterclass.query.filter_by(status='registration_open').count(),
        'live': Masterclass.query.filter_by(status='live').count(),
        'completed': Masterclass.query.filter_by(status='completed').count(),
        'cancelled': Masterclass.query.filter_by(status='cancelled').count(),
    }
    
    return render_template('admin/masterclasses.html', 
                         masterclasses=masterclasses, 
                         status_counts=status_counts,
                         status_filter=status_filter)


@app.route('/admin/masterclasses/create', methods=['GET', 'POST'])
@admin_required
def admin_masterclass_create():
    """Create new masterclass."""
    form = MasterclassForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Generate slug if not provided
            slug = form.slug.data
            if not slug:
                slug = generate_slug(form.title.data)
            
            masterclass = Masterclass(
                title=form.title.data,
                slug=slug,
                short_description=form.short_description.data,
                detailed_description=form.detailed_description.data,
                banner_image=form.banner_image.data,
                thumbnail=form.thumbnail.data,
                featured_image=form.featured_image.data,
                timezone=form.timezone.data,
                duration=int(form.duration.data) if form.duration.data else 60,
                max_seats=int(form.max_seats.data) if form.max_seats.data else 500,
                status=form.status.data,
                is_featured=form.is_featured.data,
                show_floating_button=form.show_floating_button.data,
                show_popup=form.show_popup.data,
                show_sticky_banner=form.show_sticky_banner.data,
                show_homepage_promotion=form.show_homepage_promotion.data,
                meta_title=form.meta_title.data,
                meta_description=form.meta_description.data,
                meta_keywords=form.meta_keywords.data,
                og_image=form.og_image.data,
                canonical_url=form.canonical_url.data,
                about_content=form.about_content.data,
                language=form.language.data,
                mode=form.mode.data,
                instructor_name=form.instructor_name.data,
                instructor_photo=form.instructor_photo.data,
                instructor_designation=form.instructor_designation.data,
                instructor_company=form.instructor_company.data,
                instructor_bio=form.instructor_bio.data,
                instructor_linkedin=form.instructor_linkedin.data,
                instructor_twitter=form.instructor_twitter.data,
                instructor_website=form.instructor_website.data,
            )
            
            # Parse date and time
            try:
                masterclass.date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
                masterclass.time = datetime.strptime(form.time.data, '%H:%M').time()
            except ValueError:
                flash('Invalid date or time format', 'error')
                return render_template('admin/masterclass_edit.html', form=form, masterclass=None)
            
            # Parse registration opens/closes
            if form.registration_opens.data:
                try:
                    masterclass.registration_opens = datetime.strptime(form.registration_opens.data, '%Y-%m-%d %H:%M')
                except ValueError:
                    pass
            
            if form.registration_closes.data:
                try:
                    masterclass.registration_closes = datetime.strptime(form.registration_closes.data, '%Y-%m-%d %H:%M')
                except ValueError:
                    pass
            
            db.session.add(masterclass)
            db.session.commit()
            
            flash(f'Masterclass "{masterclass.title}" created successfully!', 'success')
            return redirect(url_for('admin_masterclass_edit', masterclass_id=masterclass.id))
    
    return render_template('admin/masterclass_edit.html', form=form, masterclass=None)


@app.route('/admin/masterclasses/<int:masterclass_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_masterclass_edit(masterclass_id):
    """Edit existing masterclass."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    form = MasterclassForm(obj=masterclass)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Update fields
            masterclass.title = form.title.data
            masterclass.slug = form.slug.data if form.slug.data else generate_slug(form.title.data)
            masterclass.short_description = form.short_description.data
            masterclass.detailed_description = form.detailed_description.data
            masterclass.banner_image = form.banner_image.data
            masterclass.thumbnail = form.thumbnail.data
            masterclass.featured_image = form.featured_image.data
            masterclass.timezone = form.timezone.data
            masterclass.duration = int(form.duration.data) if form.duration.data else 60
            masterclass.max_seats = int(form.max_seats.data) if form.max_seats.data else 500
            masterclass.status = form.status.data
            masterclass.is_featured = form.is_featured.data
            masterclass.show_floating_button = form.show_floating_button.data
            masterclass.show_popup = form.show_popup.data
            masterclass.show_sticky_banner = form.show_sticky_banner.data
            masterclass.show_homepage_promotion = form.show_homepage_promotion.data
            masterclass.meta_title = form.meta_title.data
            masterclass.meta_description = form.meta_description.data
            masterclass.meta_keywords = form.meta_keywords.data
            masterclass.og_image = form.og_image.data
            masterclass.canonical_url = form.canonical_url.data
            masterclass.about_content = form.about_content.data
            masterclass.language = form.language.data
            masterclass.mode = form.mode.data
            masterclass.confirmation_message = request.form.get('confirmation_message', '').strip()
            masterclass.instructor_name = form.instructor_name.data
            masterclass.instructor_photo = form.instructor_photo.data
            masterclass.instructor_designation = form.instructor_designation.data
            masterclass.instructor_company = form.instructor_company.data
            masterclass.instructor_bio = form.instructor_bio.data
            masterclass.instructor_linkedin = form.instructor_linkedin.data
            masterclass.instructor_twitter = form.instructor_twitter.data
            masterclass.instructor_website = form.instructor_website.data
            
            # Parse date and time
            try:
                masterclass.date = datetime.strptime(form.date.data, '%Y-%m-%d').date()
                masterclass.time = datetime.strptime(form.time.data, '%H:%M').time()
            except ValueError:
                flash('Invalid date or time format', 'error')
                return render_template('admin/masterclass_edit.html', form=form, masterclass=masterclass)
            
            # Parse registration opens/closes
            if form.registration_opens.data:
                try:
                    masterclass.registration_opens = datetime.strptime(form.registration_opens.data, '%Y-%m-%d %H:%M')
                except ValueError:
                    pass
            
            if form.registration_closes.data:
                try:
                    masterclass.registration_closes = datetime.strptime(form.registration_closes.data, '%Y-%m-%d %H:%M')
                except ValueError:
                    pass
            
            db.session.commit()
            flash(f'Masterclass "{masterclass.title}" updated successfully!', 'success')
    
    # Get JSON fields for display
    what_you_learn = masterclass.get_json_field('what_you_learn')
    who_should_attend = masterclass.get_json_field('who_should_attend')
    prerequisites = masterclass.get_json_field('prerequisites')
    benefits = masterclass.get_json_field('benefits')
    agenda = masterclass.get_json_field('agenda')
    faqs = masterclass.get_json_field('faqs')
    testimonials = masterclass.get_json_field('testimonials')
    reminder_settings = masterclass.get_json_field('reminder_settings')
    
    return render_template('admin/masterclass_edit.html', 
                         form=form, 
                         masterclass=masterclass,
                         what_you_learn=what_you_learn,
                         who_should_attend=who_should_attend,
                         prerequisites=prerequisites,
                         benefits=benefits,
                         agenda=agenda,
                         faqs=faqs,
                         testimonials=testimonials,
                         reminder_settings=reminder_settings)


@app.route('/admin/masterclasses/<int:masterclass_id>/content', methods=['POST'])
@admin_required
def admin_masterclass_content(masterclass_id):
    """Update masterclass rich content sections."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    
    # Update JSON fields
    masterclass.set_json_field('what_you_learn', request.json.get('what_you_learn', []))
    masterclass.set_json_field('who_should_attend', request.json.get('who_should_attend', []))
    masterclass.set_json_field('prerequisites', request.json.get('prerequisites', []))
    masterclass.set_json_field('benefits', request.json.get('benefits', []))
    masterclass.set_json_field('agenda', request.json.get('agenda', []))
    masterclass.set_json_field('faqs', request.json.get('faqs', []))
    masterclass.set_json_field('testimonials', request.json.get('testimonials', []))
    masterclass.set_json_field('reminder_settings', request.json.get('reminder_settings', {}))
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Content updated successfully'})


@app.route('/admin/masterclasses/<int:masterclass_id>/delete', methods=['POST'])
@admin_required
def admin_masterclass_delete(masterclass_id):
    """Delete masterclass."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    title = masterclass.title
    db.session.delete(masterclass)
    db.session.commit()
    flash(f'Masterclass "{title}" deleted successfully!', 'success')
    return redirect(url_for('admin_masterclasses'))


@app.route('/admin/masterclasses/<int:masterclass_id>/status', methods=['POST'])
@admin_required
def admin_masterclass_status(masterclass_id):
    """Update masterclass status."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    new_status = request.form.get('status')
    if new_status in ['draft', 'published', 'registration_open', 'live', 'completed', 'cancelled']:
        masterclass.status = new_status
        db.session.commit()
        flash(f'Status updated to "{new_status}"', 'success')
    return redirect(url_for('admin_masterclasses'))


@app.route('/admin/masterclasses/<int:masterclass_id>/registrations')
@admin_required
def admin_masterclass_registrations(masterclass_id):
    """View registrations for a masterclass."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    registrations = masterclass.registrations.order_by(MasterclassRegistration.created_at.desc()).all()
    
    return render_template('admin/masterclass_registrations.html',
                         masterclass=masterclass,
                         registrations=registrations)


@app.route('/admin/masterclasses/<int:masterclass_id>/bulk-email', methods=['POST'])
@admin_required
def admin_masterclass_bulk_email(masterclass_id):
    """Send bulk email to all registrants."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()
    include_masterclass_info = request.form.get('include_masterclass_info') == 'on'
    
    if not subject or not message:
        flash('Subject and message are required.', 'error')
        return redirect(url_for('admin_masterclass_registrations', masterclass_id=masterclass_id))
    
    registrations = masterclass.registrations.filter_by(status='confirmed').all()
    
    if not registrations:
        flash('No confirmed registrations to send emails to.', 'warning')
        return redirect(url_for('admin_masterclass_registrations', masterclass_id=masterclass_id))
    
    # Build email content
    event_datetime = datetime.combine(masterclass.date, masterclass.time)
    event_date_str = event_datetime.strftime('%B %d, %Y')
    event_time_str = masterclass.time.strftime('%I:%M %p')
    
    footer_html = ""
    if include_masterclass_info:
        footer_html = f"""
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
            <h4 style="color: #4f46e5; margin-bottom: 10px;">{masterclass.title}</h4>
            <p style="margin: 5px 0;"><strong>Date:</strong> {event_date_str}</p>
            <p style="margin: 5px 0;"><strong>Time:</strong> {event_time_str}</p>
            {f'<p style="margin: 5px 0;"><strong>Location:</strong> {masterclass.location}</p>' if masterclass.location else ''}
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #4f46e5, #8b5cf6); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-top: none; }}
            .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 8px 8px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>{masterclass.title}</h2>
        </div>
        <div class="content">
            <p>{message.replace('\n', '<br>')}</p>
            {footer_html}
        </div>
        <div class="footer">
            <p>You're receiving this email because you registered for {masterclass.title}.</p>
            <p>Registration ID: {registrations[0].registration_id if registrations else 'N/A'}</p>
        </div>
    </body>
    </html>
    """
    
    location_line = f"Location: {masterclass.location}" if masterclass.location else ""
    
    text_content = f"""
{masterclass.title}

{message}

---
Event Details:
Date: {event_date_str}
Time: {event_time_str}
{location_line}

You're receiving this email because you registered for {masterclass.title}.
    """
    
    # Send emails
    sent_count = 0
    failed_count = 0
    
    for reg in registrations:
        try:
            result = EmailService.send_email(
                reg.email,
                subject,
                html_content,
                text_content
            )
            if result:
                sent_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"Failed to send email to {reg.email}: {e}")
            failed_count += 1
    
    flash(f'Bulk email sent to {sent_count} registrants. {failed_count} failed.', 'success' if failed_count == 0 else 'warning')
    return redirect(url_for('admin_masterclass_registrations', masterclass_id=masterclass_id))


@app.route('/admin/masterclasses/<int:masterclass_id>/analytics')
@admin_required
def admin_masterclass_analytics(masterclass_id):
    """View analytics for a masterclass."""
    masterclass = Masterclass.query.get_or_404(masterclass_id)
    
    # Get analytics data
    page_views = MasterclassAnalytics.query.filter_by(
        masterclass_id=masterclass_id, 
        event_type='page_view'
    ).count()
    
    total_registrations = masterclass.registrations.count()
    confirmed_registrations = masterclass.registrations.filter_by(status='confirmed').count()
    
    # Daily registrations for the last 30 days
    thirty_days_ago = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    daily_stats = db.session.query(
        func.date(MasterclassRegistration.created_at).label('date'),
        func.count(MasterclassRegistration.id).label('count')
    ).filter(
        MasterclassRegistration.masterclass_id == masterclass_id,
        MasterclassRegistration.created_at >= thirty_days_ago
    ).group_by(func.date(MasterclassRegistration.created_at)).all()
    
    # Country distribution
    country_stats = db.session.query(
        MasterclassRegistration.country,
        func.count(MasterclassRegistration.id).label('count')
    ).filter(
        MasterclassRegistration.masterclass_id == masterclass_id
    ).group_by(MasterclassRegistration.country).all()
    
    # Device distribution
    device_stats = db.session.query(
        MasterclassRegistration.device,
        func.count(MasterclassRegistration.id).label('count')
    ).filter(
        MasterclassRegistration.masterclass_id == masterclass_id
    ).group_by(MasterclassRegistration.device).all()
    
    # Recent activity
    recent_analytics = MasterclassAnalytics.query.filter_by(
        masterclass_id=masterclass_id
    ).order_by(MasterclassAnalytics.created_at.desc()).limit(50).all()
    
    return render_template('admin/masterclass_analytics.html',
                         masterclass=masterclass,
                         page_views=page_views,
                         total_registrations=total_registrations,
                         confirmed_registrations=confirmed_registrations,
                         daily_stats=daily_stats,
                         country_stats=country_stats,
                         device_stats=device_stats,
                         recent_analytics=recent_analytics)


# =====================================================
# PUBLIC MASTERCLASS ROUTES
# =====================================================

@app.route('/masterclass/<slug>')
def masterclass_detail(slug):
    """Public masterclass detail page."""
    masterclass = Masterclass.query.filter_by(slug=slug).first_or_404()
    
    # Increment view count
    if masterclass.view_count is None:
        masterclass.view_count = 1
    else:
        masterclass.view_count += 1
    db.session.commit()
    
    # Track analytics
    try:
        analytics = MasterclassAnalytics(
            masterclass_id=masterclass.id,
            event_type='page_view',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            device='mobile' if 'mobile' in request.user_agent.string.lower() else 'desktop',
            utm_source=request.args.get('utm_source'),
            utm_medium=request.args.get('utm_medium'),
            utm_campaign=request.args.get('utm_campaign')
        )
        db.session.add(analytics)
        db.session.commit()
    except Exception:
        pass
    
    # Check if registration is open
    now = datetime.utcnow()
    registration_open = True
    
    if masterclass.registration_closes:
        closes_time = masterclass.registration_closes.replace(tzinfo=None) if masterclass.registration_closes.tzinfo else masterclass.registration_closes
        registration_open = now < closes_time
    
    if masterclass.registration_opens:
        opens_time = masterclass.registration_opens.replace(tzinfo=None) if masterclass.registration_opens.tzinfo else masterclass.registration_opens
        registration_open = registration_open and now >= opens_time
    
    seats_available = masterclass.available_seats > 0
    
    # Get JSON fields
    what_you_learn = masterclass.get_json_field('what_you_learn')
    who_should_attend = masterclass.get_json_field('who_should_attend')
    prerequisites = masterclass.get_json_field('prerequisites')
    benefits = masterclass.get_json_field('benefits')
    agenda = masterclass.get_json_field('agenda')
    faqs = masterclass.get_json_field('faqs')
    testimonials = masterclass.get_json_field('testimonials')
    
    form = MasterclassRegistrationForm()
    
    return render_template('masterclass_detail.html',
                         masterclass=masterclass,
                         form=form,
                         registration_open=registration_open,
                         seats_available=seats_available,
                         what_you_learn=what_you_learn,
                         who_should_attend=who_should_attend,
                         prerequisites=prerequisites,
                         benefits=benefits,
                         agenda=agenda,
                         faqs=faqs,
                         testimonials=testimonials)


@app.route('/masterclass/<slug>/register', methods=['POST'])
def masterclass_register(slug):
    """Handle masterclass registration."""
    masterclass = Masterclass.query.filter_by(slug=slug).first_or_404()
    
    # Get JSON data (same way other forms work)
    if request.is_json:
        data = request.get_json()
    else:
        data = {k: v for k, v in request.form.items()}
    
    # Check if registration is open
    now = datetime.utcnow()
    registration_open = True
    
    if masterclass.registration_closes:
        closes_time = masterclass.registration_closes.replace(tzinfo=None) if masterclass.registration_closes.tzinfo else masterclass.registration_closes
        registration_open = now < closes_time
    
    if masterclass.registration_opens:
        opens_time = masterclass.registration_opens.replace(tzinfo=None) if masterclass.registration_opens.tzinfo else masterclass.registration_opens
        registration_open = registration_open and now >= opens_time
    
    if not registration_open:
        return jsonify({'success': False, 'message': 'Registration is closed'}), 400
    
    # Check seat availability
    if masterclass.available_seats <= 0:
        return jsonify({'success': False, 'message': 'All seats are taken'}), 400
    
    # Validate required fields
    email = data.get('email', '').lower().strip()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    if not first_name:
        return jsonify({'success': False, 'message': 'First name is required'}), 400
    if not last_name:
        return jsonify({'success': False, 'message': 'Last name is required'}), 400
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    # Validate email format
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address'}), 400
    
    # Check for duplicate registration
    existing = MasterclassRegistration.query.filter_by(
        masterclass_id=masterclass.id,
        email=email
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'You have already registered for this masterclass'}), 400
    
    # Generate unique registration ID
    registration_id = f"MC-{masterclass.id}-{uuid.uuid4().hex[:6].upper()}"
    
    # Create registration
    registration = MasterclassRegistration(
        masterclass_id=masterclass.id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=data.get('phone', '').strip() if data.get('phone') else None,
        country=data.get('country', '').strip() if data.get('country') else None,
        company=data.get('company', '').strip() if data.get('company') else None,
        job_title=data.get('job_title', '').strip() if data.get('job_title') else None,
        experience=data.get('experience', '').strip() if data.get('experience') else None,
        industry=data.get('industry', '').strip() if data.get('industry') else None,
        linkedin=data.get('linkedin', '').strip() if data.get('linkedin') else None,
        receive_updates=bool(data.get('receive_updates')),
        registration_id=registration_id,
        status='confirmed',
        source_page=request.referrer,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        device='mobile' if 'mobile' in request.user_agent.string.lower() else 'desktop',
        utm_source=request.args.get('utm_source'),
        utm_medium=request.args.get('utm_medium'),
        utm_campaign=request.args.get('utm_campaign')
    )
    
    db.session.add(registration)
    
    # Also create a Lead entry (same as other forms)
    try:
        lead = Lead(
            name=f"{first_name} {last_name}",
            email=email,
            phone=data.get('phone', '').strip() if data.get('phone') else None,
            company=data.get('company', '').strip() if data.get('company') else None,
            form_type='masterclass',
            status='new',
            ip_address=request.remote_addr
        )
        db.session.add(lead)
    except Exception as e:
        print(f"Failed to create lead: {e}")
    
    # Track analytics
    try:
        analytics = MasterclassAnalytics(
            masterclass_id=masterclass.id,
            event_type='registration',
            event_data=json.dumps({'registration_id': registration_id}),
            ip_address=request.remote_addr,
            device='mobile' if 'mobile' in request.user_agent.string.lower() else 'desktop'
        )
        db.session.add(analytics)
    except Exception:
        pass
    
    db.session.commit()
    
    # Send confirmation email to participant
    try:
        EmailService.send_masterclass_confirmation(registration, masterclass)
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
    
    # Send admin notification
    try:
        admin_email = EmailService.get_setting('masterclass_admin_email', 'admin@humisense.com')
        subject = f"New Masterclass Registration - {masterclass.title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #4f46e5; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9fafb; padding: 20px; border-radius: 0 0 8px 8px; }}
                .field {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; color: #4f46e5; }}
                .value {{ margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>New Masterclass Registration</h2>
                </div>
                <div class="content">
                    <p><strong>Masterclass:</strong> {masterclass.title}</p>
                    <div class="field">
                        <div class="label">Name:</div>
                        <div class="value">{first_name} {last_name}</div>
                    </div>
                    <div class="field">
                        <div class="label">Email:</div>
                        <div class="value"><a href="mailto:{email}">{email}</a></div>
                    </div>
                    <div class="field">
                        <div class="label">Phone:</div>
                        <div class="value">{data.get('phone', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">Company:</div>
                        <div class="value">{data.get('company', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">Job Title:</div>
                        <div class="value">{data.get('job_title', 'N/A')}</div>
                    </div>
                    <div class="field">
                        <div class="label">Registration ID:</div>
                        <div class="value">{registration_id}</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        EmailService.send_email(admin_email, subject, html_content)
    except Exception as e:
        print(f"Failed to send admin notification: {e}")
    
    return jsonify({
        'success': True, 
        'message': 'Registration successful!',
        'registration_id': registration_id
    })


@app.route('/api/masterclass/<slug>/seats')
def api_masterclass_seats(slug):
    """Get real-time seat availability."""
    masterclass = Masterclass.query.filter_by(slug=slug).first_or_404()
    
    return jsonify({
        'available_seats': masterclass.available_seats,
        'max_seats': masterclass.max_seats,
        'registered_count': masterclass.registered_count,
        'seats_percentage': masterclass.seats_percentage
    })


@app.route('/api/masterclass/countdown/<slug>')
def api_masterclass_countdown(slug):
    """Get countdown data for masterclass."""
    masterclass = Masterclass.query.filter_by(slug=slug).first_or_404()
    
    # Calculate target datetime
    target_dt = datetime.combine(masterclass.date, masterclass.time)
    
    return jsonify({
        'target_timestamp': int(target_dt.timestamp()),
        'title': masterclass.title,
        'status': masterclass.status
    })


@app.route('/api/masterclass/active')
def api_masterclass_active():
    """Get active masterclass for website promotion."""
    active_masterclass = get_active_masterclass()
    
    if not active_masterclass:
        return jsonify({'active': False})
    
    return jsonify({
        'active': True,
        'id': active_masterclass.id,
        'title': active_masterclass.title,
        'slug': active_masterclass.slug,
        'short_description': active_masterclass.short_description,
        'date': active_masterclass.date.isoformat(),
        'time': active_masterclass.time.isoformat(),
        'available_seats': active_masterclass.available_seats,
        'show_floating_button': active_masterclass.show_floating_button,
        'show_popup': active_masterclass.show_popup,
        'show_sticky_banner': active_masterclass.show_sticky_banner,
        'show_homepage_promotion': active_masterclass.show_homepage_promotion
    })


# =====================================================
# MASTERCLASS SETTINGS
# =====================================================

@app.route('/admin/masterclass-settings', methods=['GET', 'POST'])
@admin_required
def admin_masterclass_settings():
    """Masterclass module settings."""
    form = MasterclassSettingsForm()
    
    if request.method == 'POST':
        settings_mapping = [
            ('masterclass_enable_module', form.enable_module.data),
            ('masterclass_enable_homepage_promotion', form.enable_homepage_promotion.data),
            ('masterclass_enable_floating_cta', form.enable_floating_cta.data),
            ('masterclass_enable_popup', form.enable_popup.data),
            ('masterclass_enable_sticky_banner', form.enable_sticky_banner.data),
            ('masterclass_enable_reminder_emails', form.enable_reminder_emails.data),
            ('masterclass_enable_calendar_integration', form.enable_calendar_integration.data),
            ('masterclass_enable_waitlist', form.enable_waitlist.data),
            ('masterclass_enable_certificates', form.enable_certificates.data),
            ('masterclass_enable_analytics', form.enable_analytics.data),
        ]
        
        for key, value in settings_mapping:
            set_masterclass_setting(key, value)
        
        if form.admin_email.data:
            set_masterclass_setting('masterclass_admin_email', form.admin_email.data, 'string')
        
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('admin_masterclass_settings'))
    
    # Load current settings
    form.enable_module.data = get_masterclass_setting('masterclass_enable_module', True)
    form.enable_homepage_promotion.data = get_masterclass_setting('masterclass_enable_homepage_promotion', True)
    form.enable_floating_cta.data = get_masterclass_setting('masterclass_enable_floating_cta', True)
    form.enable_popup.data = get_masterclass_setting('masterclass_enable_popup', False)
    form.enable_sticky_banner.data = get_masterclass_setting('masterclass_enable_sticky_banner', False)
    form.enable_reminder_emails.data = get_masterclass_setting('masterclass_enable_reminder_emails', True)
    form.enable_calendar_integration.data = get_masterclass_setting('masterclass_enable_calendar_integration', True)
    form.enable_waitlist.data = get_masterclass_setting('masterclass_enable_waitlist', False)
    form.enable_certificates.data = get_masterclass_setting('masterclass_enable_certificates', False)
    form.enable_analytics.data = get_masterclass_setting('masterclass_enable_analytics', True)
    form.admin_email.data = get_masterclass_setting('masterclass_admin_email', '')
    
    return render_template('admin/masterclass_settings.html', form=form)


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