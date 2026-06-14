from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and contact."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_subscribed = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Contact(db.Model):
    """Contact form submissions."""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, responded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contact {self.subject}>'


class Newsletter(db.Model):
    """Newsletter subscriptions."""
    __tablename__ = 'newsletter'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Newsletter {self.email}>'


class CourseEnrollment(db.Model):
    """Course enrollment tracking."""
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
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CourseEnrollment {self.course_id}>'


class ResearchSubmission(db.Model):
    """Research paper submissions."""
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
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResearchSubmission {self.title[:50]}>'