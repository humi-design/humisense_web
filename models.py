from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import extensions

db = extensions.db

def utc_now():
    """Return current UTC time."""
    return datetime.now(timezone.utc)


class Admin(db.Model):
    """Admin user model for admin panel authentication."""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'


class User(db.Model):
    """User model for authentication and contact."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utc_now)
    is_subscribed = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Lead(db.Model):
    """Unified Lead model for all form submissions."""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(50), nullable=False, index=True)  # contact, newsletter, enrollment, demo, research
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    message = db.Column(db.Text)
    
    # Form-specific fields stored as JSON
    form_data = db.Column(db.Text)  # JSON string for additional fields
    
    # Source tracking
    source_page = db.Column(db.String(200))  # URL where form was submitted
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(500))
    
    # Status tracking
    status = db.Column(db.String(20), default='new')  # new, read, in_progress, resolved, archived
    is_read = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    # Email tracking
    email_sent = db.Column(db.Boolean, default=False)
    auto_reply_sent = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    
    def __repr__(self):
        return f'<Lead {self.form_type} - {self.email}>'
    
    def get_form_data_dict(self):
        """Parse form_data JSON to dictionary."""
        import json
        if self.form_data:
            try:
                return json.loads(self.form_data)
            except:
                return {}
        return {}


class Contact(db.Model):
    """Contact form submissions - DEPRECATED, use Lead instead."""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, responded
    created_at = db.Column(db.DateTime, default=utc_now)
    
    def __repr__(self):
        return f'<Contact {self.subject}>'


class Newsletter(db.Model):
    """Newsletter subscriptions."""
    __tablename__ = 'newsletter'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    subscribed_at = db.Column(db.DateTime, default=utc_now)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Newsletter {self.email}>'


class CourseEnrollment(db.Model):
    """Course enrollment tracking - DEPRECATED, use Lead instead."""
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    course_id = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    experience_level = db.Column(db.String(50))
    goals = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed
    enrolled_at = db.Column(db.DateTime, default=utc_now)
    
    def __repr__(self):
        return f'<CourseEnrollment {self.course_id}>'


class ResearchSubmission(db.Model):
    """Research paper submissions - DEPRECATED, use Lead instead."""
    __tablename__ = 'research_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    authors = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(200))
    research_area = db.Column(db.String(100))
    abstract = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(500))
    status = db.Column(db.String(20), default='submitted')  # submitted, reviewing, accepted, rejected
    submitted_at = db.Column(db.DateTime, default=utc_now)
    
    def __repr__(self):
        return f'<ResearchSubmission {self.title[:50]}>'


class FormLog(db.Model):
    """Log for form submissions and errors."""
    __tablename__ = 'form_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(50), nullable=False, index=True)
    action = db.Column(db.String(50), nullable=False)  # submitted, email_sent, email_failed, validated, error
    message = db.Column(db.Text)
    details = db.Column(db.Text)  # JSON string for additional details
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    
    def __repr__(self):
        return f'<FormLog {self.form_type} - {self.action}>'


class SiteSettings(db.Model):
    """Site settings stored in database."""
    __tablename__ = 'site_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    value_type = db.Column(db.String(20), default='string')  # string, int, bool, json
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    
    def __repr__(self):
        return f'<SiteSettings {self.key}>'
    
    def get_value(self):
        """Get typed value."""
        if self.value_type == 'int':
            return int(self.value) if self.value else 0
        elif self.value_type == 'bool':
            return self.value == 'true'
        elif self.value_type == 'json':
            import json
            return json.loads(self.value) if self.value else {}
        return self.value
    
    def set_value(self, value):
        """Set typed value."""
        if self.value_type == 'int':
            self.value = str(value)
        elif self.value_type == 'bool':
            self.value = 'true' if value else 'false'
        elif self.value_type == 'json':
            import json
            self.value = json.dumps(value)
        else:
            self.value = str(value)


# =====================================================
# MASTERCLASS MODELS
# =====================================================

class Masterclass(db.Model):
    """Masterclass model for managing online masterclasses."""
    __tablename__ = 'masterclasses'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # General Info
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False, index=True)
    short_description = db.Column(db.String(500))
    detailed_description = db.Column(db.Text)
    
    # Images
    banner_image = db.Column(db.String(500))
    thumbnail = db.Column(db.String(500))
    featured_image = db.Column(db.String(500))
    
    # Schedule
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    timezone = db.Column(db.String(50), default='UTC')
    duration = db.Column(db.Integer, default=60)  # minutes
    registration_opens = db.Column(db.DateTime)
    registration_closes = db.Column(db.DateTime)
    
    # Instructor
    instructor_name = db.Column(db.String(100))
    instructor_photo = db.Column(db.String(500))
    instructor_designation = db.Column(db.String(100))
    instructor_company = db.Column(db.String(100))
    instructor_bio = db.Column(db.Text)
    instructor_linkedin = db.Column(db.String(500))
    instructor_twitter = db.Column(db.String(500))
    instructor_website = db.Column(db.String(500))
    
    # Seats
    max_seats = db.Column(db.Integer, default=500)
    
    # Status & Visibility
    status = db.Column(db.String(20), default='draft')  # draft, published, registration_open, live, completed, cancelled
    is_featured = db.Column(db.Boolean, default=False)
    show_floating_button = db.Column(db.Boolean, default=True)
    show_popup = db.Column(db.Boolean, default=False)
    show_sticky_banner = db.Column(db.Boolean, default=False)
    show_homepage_promotion = db.Column(db.Boolean, default=False)
    
    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    meta_keywords = db.Column(db.String(500))
    og_image = db.Column(db.String(500))
    canonical_url = db.Column(db.String(500))
    
    # Rich Content (JSON fields)
    about_content = db.Column(db.Text)  # Rich text HTML
    what_you_learn = db.Column(db.Text)  # JSON array
    who_should_attend = db.Column(db.Text)  # JSON array
    prerequisites = db.Column(db.Text)  # JSON array
    benefits = db.Column(db.Text)  # JSON array
    agenda = db.Column(db.Text)  # JSON array of timeline items
    faqs = db.Column(db.Text)  # JSON array of {question, answer}
    testimonials = db.Column(db.Text)  # JSON array of {name, role, company, quote, photo}
    
    # Settings
    language = db.Column(db.String(20), default='English')
    mode = db.Column(db.String(20), default='online')  # online, offline, hybrid
    
    # Reminder Settings (JSON)
    reminder_settings = db.Column(db.Text)  # JSON: {send_24h: true, send_3h: true, send_30m: true}
    
    # Analytics
    view_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    
    # Relationships
    registrations = db.relationship('MasterclassRegistration', backref='masterclass', lazy='dynamic')
    
    def __repr__(self):
        return f'<Masterclass {self.title}>'
    
    @property
    def registered_count(self):
        """Get number of confirmed registrations."""
        return self.registrations.filter_by(status='confirmed').count()
    
    @property
    def available_seats(self):
        """Calculate available seats."""
        return max(0, self.max_seats - self.registered_count)
    
    @property
    def seats_percentage(self):
        """Calculate seats filled percentage."""
        if self.max_seats == 0:
            return 0
        return round((self.registered_count / self.max_seats) * 100, 1)
    
    def get_json_field(self, field_name):
        """Parse JSON field to list."""
        import json
        data = getattr(self, field_name)
        if data:
            try:
                return json.loads(data)
            except:
                return []
        return []
    
    def set_json_field(self, field_name, value):
        """Set JSON field from list."""
        import json
        setattr(self, field_name, json.dumps(value) if value else None)


class MasterclassRegistration(db.Model):
    """Registration for masterclasses."""
    __tablename__ = 'masterclass_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    masterclass_id = db.Column(db.Integer, db.ForeignKey('masterclasses.id'), nullable=False, index=True)
    
    # Personal Info
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20))
    
    # Professional Info
    country = db.Column(db.String(100))
    company = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    experience = db.Column(db.String(50))  # beginner, intermediate, advanced, expert
    industry = db.Column(db.String(100))
    linkedin = db.Column(db.String(500))
    
    # Preferences
    receive_updates = db.Column(db.Boolean, default=True)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, attended
    registration_id = db.Column(db.String(50), unique=True)  # Human-readable ID
    
    # Email tracking
    confirmation_sent = db.Column(db.Boolean, default=False)
    confirmation_sent_at = db.Column(db.DateTime)
    reminder_24h_sent = db.Column(db.Boolean, default=False)
    reminder_3h_sent = db.Column(db.Boolean, default=False)
    reminder_30m_sent = db.Column(db.Boolean, default=False)
    
    # Source tracking
    source_page = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    utm_source = db.Column(db.String(100))
    utm_medium = db.Column(db.String(100))
    utm_campaign = db.Column(db.String(100))
    device = db.Column(db.String(50))  # desktop, mobile, tablet
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    
    def __repr__(self):
        return f'<MasterclassRegistration {self.registration_id}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def masterclass_title(self):
        if self.masterclass:
            return self.masterclass.title
        return "Unknown"


class MasterclassAnalytics(db.Model):
    """Analytics tracking for masterclasses."""
    __tablename__ = 'masterclass_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    masterclass_id = db.Column(db.Integer, db.ForeignKey('masterclasses.id'), nullable=False, index=True)
    
    # Event type
    event_type = db.Column(db.String(50), nullable=False)  # page_view, registration, email_sent, email_opened, email_clicked
    
    # Event data
    event_data = db.Column(db.Text)  # JSON for additional data
    
    # Source info
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    device = db.Column(db.String(50))
    country = db.Column(db.String(100))
    
    # UTM
    utm_source = db.Column(db.String(100))
    utm_medium = db.Column(db.String(100))
    utm_campaign = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=utc_now, index=True)
    
    def __repr__(self):
        return f'<MasterclassAnalytics {self.event_type}>'


class MasterclassEmailLog(db.Model):
    """Email sending logs for masterclasses."""
    __tablename__ = 'masterclass_email_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('masterclass_registrations.id'), nullable=False, index=True)
    
    # Email details
    email_type = db.Column(db.String(50), nullable=False)  # confirmation, reminder_24h, reminder_3h, reminder_30m
    subject = db.Column(db.String(200))
    sent_at = db.Column(db.DateTime, default=utc_now)
    opened_at = db.Column(db.DateTime)
    clicked_at = db.Column(db.DateTime)
    bounced = db.Column(db.Boolean, default=False)
    failed = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<MasterclassEmailLog {self.email_type}>'