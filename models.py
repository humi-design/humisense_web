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