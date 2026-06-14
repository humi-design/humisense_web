from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo


class ContactForm(FlaskForm):
    """Contact form for general inquiries."""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    subject = SelectField('Subject', choices=[
        ('', 'Select a topic'),
        ('general', 'General Inquiry'),
        ('products', 'Products & Pricing'),
        ('services', 'Services'),
        ('courses', 'Courses & Training'),
        ('partnership', 'Partnership Opportunities'),
        ('support', 'Technical Support'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])


class NewsletterForm(FlaskForm):
    """Newsletter subscription form."""
    email = StringField('Email', validators=[DataRequired(), Email()])


class EnrollmentForm(FlaskForm):
    """Course enrollment form."""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    company = StringField('Company/Organization', validators=[Optional(), Length(max=100)])
    experience_level = SelectField('Experience Level', choices=[
        ('', 'Select your level'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ], validators=[DataRequired()])
    goals = TextAreaField('Learning Goals', validators=[Optional(), Length(max=1000)])
    
    def validate_experience_level(self, field):
        if field.data == '':
            raise ValueError('Please select your experience level')


class ResearchSubmissionForm(FlaskForm):
    """Research paper submission form."""
    title = StringField('Paper Title', validators=[DataRequired(), Length(min=10, max=300)])
    authors = StringField('Authors', validators=[DataRequired(), Length(min=5, max=500)])
    email = StringField('Corresponding Author Email', validators=[DataRequired(), Email()])
    institution = StringField('Institution/Organization', validators=[DataRequired(), Length(max=200)])
    research_area = SelectField('Research Area', choices=[
        ('', 'Select research area'),
        ('agentic_ai', 'Agentic AI'),
        ('multi_agent', 'Multi-Agent Systems'),
        ('generative_ai', 'Generative AI'),
        ('explainable_ai', 'Explainable AI'),
        ('healthcare_ai', 'Healthcare AI'),
        ('nlp', 'Natural Language Processing'),
        ('computer_vision', 'Computer Vision'),
        ('ai_accessibility', 'AI Accessibility'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    abstract = TextAreaField('Abstract', validators=[DataRequired(), Length(min=100, max=2000)])
    keywords = StringField('Keywords', validators=[DataRequired(), Length(max=500)])
    
    def validate_research_area(self, field):
        if field.data == '':
            raise ValueError('Please select a research area')


class LoginForm(FlaskForm):
    """Admin login form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])


class DemoRequestForm(FlaskForm):
    """Demo request form for products."""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    product = StringField('Product', validators=[DataRequired()])
    use_case = TextAreaField('Use Case', validators=[Optional(), Length(max=1000)])
    preferred_time = SelectField('Preferred Contact Time', choices=[
        ('', 'Select preferred time'),
        ('morning', 'Morning (9AM - 12PM)'),
        ('afternoon', 'Afternoon (12PM - 5PM)'),
        ('evening', 'Evening (5PM - 8PM)'),
        ('any', 'Any time')
    ])