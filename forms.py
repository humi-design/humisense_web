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


# =====================================================
# MASTERCLASS FORMS
# =====================================================

class MasterclassForm(FlaskForm):
    """Form for creating/editing masterclasses."""
    # General Info
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    slug = StringField('Slug', validators=[Length(max=220)])
    short_description = StringField('Short Description', validators=[Length(max=500)])
    detailed_description = TextAreaField('Detailed Description')
    
    # Images
    banner_image = StringField('Banner Image URL')
    thumbnail = StringField('Thumbnail URL')
    featured_image = StringField('Featured Image URL')
    
    # Schedule
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    timezone = SelectField('Timezone', choices=[
        ('UTC', 'UTC'),
        ('US/Eastern', 'US/Eastern'),
        ('US/Pacific', 'US/Pacific'),
        ('Europe/London', 'Europe/London'),
        ('Europe/Paris', 'Europe/Paris'),
        ('Asia/Tokyo', 'Asia/Tokyo'),
        ('Asia/Shanghai', 'Asia/Shanghai'),
        ('Asia/Kolkata', 'Asia/Kolkata'),
        ('Australia/Sydney', 'Australia/Sydney'),
    ], default='UTC')
    duration = StringField('Duration (minutes)')
    registration_opens = StringField('Registration Opens')
    registration_closes = StringField('Registration Closes')
    
    # Instructor
    instructor_name = StringField('Instructor Name', validators=[Length(max=100)])
    instructor_photo = StringField('Instructor Photo URL')
    instructor_designation = StringField('Designation', validators=[Length(max=100)])
    instructor_company = StringField('Company', validators=[Length(max=100)])
    instructor_bio = TextAreaField('Bio')
    instructor_linkedin = StringField('LinkedIn URL')
    instructor_twitter = StringField('Twitter URL')
    instructor_website = StringField('Website URL')
    
    # Seats
    max_seats = StringField('Maximum Seats', validators=[DataRequired()])
    
    # Status & Visibility
    status = SelectField('Status', choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('registration_open', 'Registration Open'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='draft')
    is_featured = BooleanField('Featured')
    show_floating_button = BooleanField('Show Floating Button')
    show_popup = BooleanField('Show Popup')
    show_sticky_banner = BooleanField('Show Sticky Banner')
    show_homepage_promotion = BooleanField('Show Homepage Promotion')
    
    # SEO
    meta_title = StringField('Meta Title', validators=[Length(max=200)])
    meta_description = StringField('Meta Description', validators=[Length(max=500)])
    meta_keywords = StringField('Meta Keywords', validators=[Length(max=500)])
    og_image = StringField('Open Graph Image URL')
    canonical_url = StringField('Canonical URL')
    
    # Content
    about_content = TextAreaField('About Content')
    language = SelectField('Language', choices=[
        ('English', 'English'),
        ('Spanish', 'Spanish'),
        ('French', 'French'),
        ('German', 'German'),
        ('Chinese', 'Chinese'),
        ('Japanese', 'Japanese'),
        ('Hindi', 'Hindi'),
    ], default='English')
    mode = SelectField('Mode', choices=[
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ], default='online')


class MasterclassRegistrationForm(FlaskForm):
    """Registration form for masterclasses."""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    
    # Professional Info
    country = SelectField('Country', choices=[
        ('', 'Select your country'),
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IN', 'India'),
        ('JP', 'Japan'),
        ('CN', 'China'),
        ('BR', 'Brazil'),
        ('Other', 'Other'),
    ])
    company = StringField('Company Name', validators=[Optional(), Length(max=100)])
    job_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    experience = SelectField('Experience Level', choices=[
        ('', 'Select your experience'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ])
    industry = StringField('Industry', validators=[Optional(), Length(max=100)])
    linkedin = StringField('LinkedIn Profile (optional)', validators=[Optional(), Length(max=500)])
    
    receive_updates = BooleanField('I agree to receive updates about this masterclass and related events')


class MasterclassSettingsForm(FlaskForm):
    """Settings form for masterclass module."""
    enable_module = BooleanField('Enable Masterclass Module')
    enable_homepage_promotion = BooleanField('Enable Homepage Promotion')
    enable_floating_cta = BooleanField('Enable Floating CTA')
    enable_popup = BooleanField('Enable Exit Intent Popup')
    enable_sticky_banner = BooleanField('Enable Sticky Banner')
    enable_countdown = BooleanField('Enable Countdown Timer')
    enable_seat_counter = BooleanField('Enable Seat Counter')
    enable_reminder_emails = BooleanField('Enable Reminder Emails')
    enable_calendar_integration = BooleanField('Enable Calendar Integration')
    enable_waitlist = BooleanField('Enable Waitlist')
    enable_certificates = BooleanField('Enable Certificates')
    enable_analytics = BooleanField('Enable Analytics')
    admin_email = StringField('Admin Notification Email', validators=[Optional(), Email()])