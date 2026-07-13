"""
Form Submission Service
Handles all form submissions with unified lead storage, email notifications, and logging.
"""

import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import request
from models import Lead, FormLog, SiteSettings
from extensions import db


class FormService:
    """Unified service for handling all form submissions."""
    
    # Rate limiting storage (in-memory, use Redis for production)
    _rate_limit_store = {}
    RATE_LIMIT_SECONDS = 60  # Minimum seconds between submissions from same IP
    
    @classmethod
    def get_client_ip(cls):
        """Get client IP address from request."""
        if request.environ.get('HTTP_X_FORWARDED_FOR'):
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
        return request.environ.get('REMOTE_ADDR', '0.0.0.0')
    
    @classmethod
    def sanitize_input(cls, text):
        """Sanitize input to prevent XSS."""
        if not text:
            return ''
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', str(text))
        # Remove script content
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
        return text.strip()
    
    @classmethod
    def validate_email(cls, email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @classmethod
    def validate_phone(cls, phone):
        """Validate phone number format."""
        if not phone:
            return True  # Phone is optional
        # Allow various phone formats
        cleaned = re.sub(r'[\s\-\.\(\)]', '', phone)
        return re.match(r'^\+?\d{7,15}$', cleaned) is not None
    
    @classmethod
    def check_rate_limit(cls, ip_address):
        """Check if IP is rate limited."""
        current_time = datetime.utcnow().timestamp()
        if ip_address in cls._rate_limit_store:
            last_submission = cls._rate_limit_store[ip_address]
            if current_time - last_submission < cls.RATE_LIMIT_SECONDS:
                return False
        cls._rate_limit_store[ip_address] = current_time
        return True
    
    @classmethod
    def log_action(cls, form_type, action, message=None, details=None, ip_address=None):
        """Log form action."""
        try:
            log = FormLog(
                form_type=form_type,
                action=action,
                message=message,
                details=json.dumps(details) if details else None,
                ip_address=ip_address or cls.get_client_ip()
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            print(f"Logging error: {e}")
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Get a site setting."""
        try:
            setting = SiteSettings.query.filter_by(key=key).first()
            return setting.get_value() if setting else default
        except:
            return default
    
    @classmethod
    def set_setting(cls, key, value, value_type='string'):
        """Set a site setting."""
        try:
            setting = SiteSettings.query.filter_by(key=key).first()
            if not setting:
                setting = SiteSettings(key=key, value_type=value_type)
                db.session.add(setting)
            setting.set_value(value)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Setting error: {e}")
            return False
    
    @classmethod
    def send_email(cls, to_email, subject, html_content, text_content=None):
        """Send email notification."""
        try:
            # Get SMTP settings
            smtp_host = cls.get_setting('smtp_host', 'localhost')
            smtp_port = cls.get_setting('smtp_port', 587)
            smtp_username = cls.get_setting('smtp_username', '')
            smtp_password = cls.get_setting('smtp_password', '')
            sender_email = cls.get_setting('sender_email', 'noreply@humisense.com')
            sender_name = cls.get_setting('sender_name', 'HUMISENSE')
            
            # Skip if SMTP not configured
            if not smtp_host or smtp_host == 'localhost':
                cls.log_action('system', 'email_skipped', 'SMTP not configured')
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                if smtp_port == 587:
                    server.starttls()
                if smtp_username and smtp_password:
                    server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            cls.log_action('system', 'email_sent', f"To: {to_email}")
            return True
            
        except Exception as e:
            cls.log_action('system', 'email_failed', str(e))
            print(f"Email error: {e}")
            return False
    
    @classmethod
    def send_admin_notification(cls, lead):
        """Send notification email to admin about new lead."""
        try:
            admin_email = cls.get_setting('admin_email', 'admin@humisense.com')
            
            subject = f"New {lead.form_type.title()} Submission - {lead.email}"
            
            # Build email content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #4f46e5, #8b5cf6); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                    .content {{ background: #f9fafb; padding: 20px; border-radius: 0 0 8px 8px; }}
                    .field {{ margin-bottom: 15px; }}
                    .label {{ font-weight: bold; color: #4f46e5; }}
                    .value {{ margin-top: 5px; }}
                    .footer {{ margin-top: 20px; padding-top: 15px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>New {lead.form_type.title()} Submission</h2>
                        <p>Submitted: {lead.created_at.strftime('%Y-%m-%d %H:%M UTC')}</p>
                    </div>
                    <div class="content">
                        <div class="field">
                            <div class="label">Name:</div>
                            <div class="value">{lead.name or 'N/A'}</div>
                        </div>
                        <div class="field">
                            <div class="label">Email:</div>
                            <div class="value"><a href="mailto:{lead.email}">{lead.email}</a></div>
                        </div>
                        <div class="field">
                            <div class="label">Phone:</div>
                            <div class="value">{lead.phone or 'N/A'}</div>
                        </div>
                        <div class="field">
                            <div class="label">Company:</div>
                            <div class="value">{lead.company or 'N/A'}</div>
                        </div>
                        <div class="field">
                            <div class="label">Message:</div>
                            <div class="value">{lead.message or 'N/A'}</div>
                        </div>
            """
            
            # Add form-specific data
            form_data = lead.get_form_data_dict()
            for key, value in form_data.items():
                if key not in ['name', 'email', 'phone', 'company', 'message']:
                    label = key.replace('_', ' ').title()
                    html_content += f"""
                        <div class="field">
                            <div class="label">{label}:</div>
                            <div class="value">{value}</div>
                        </div>
                    """
            
            html_content += f"""
                        <div class="footer">
                            <p><strong>Source Page:</strong> {lead.source_page or 'N/A'}</p>
                            <p><strong>IP Address:</strong> {lead.ip_address or 'N/A'}</p>
                            <p><strong>User Agent:</strong> {lead.user_agent or 'N/A'}</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return cls.send_email(admin_email, subject, html_content)
            
        except Exception as e:
            cls.log_action(lead.form_type, 'admin_notification_failed', str(e))
            return False
    
    @classmethod
    def send_auto_reply(cls, lead):
        """Send auto-reply email to the submitter."""
        try:
            # Check if auto-reply is enabled
            if not cls.get_setting('auto_reply_enabled', True):
                return False
            
            auto_reply_template = cls.get_setting('auto_reply_template', '''Hello {{name}},

Thank you for contacting HUMISENSE.

Our team has received your {{form_type}} submission and will review it shortly. We typically respond within 24 hours.

Here's a summary of what you submitted:
- Type: {{form_type}}
- Email: {{email}}

If you have any urgent questions, please reply to this email.

Best regards,
HUMISENSE Team''')
            
            # Replace placeholders
            content = auto_reply_template.replace('{{name}}', lead.name or 'there')
            content = content.replace('{{form_type}}', lead.form_type.title())
            content = content.replace('{{email}}', lead.email)
            
            subject = f"Thank you for your {lead.form_type} - HUMISENSE"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #4f46e5, #8b5cf6); color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
                    .content {{ background: #f9fafb; padding: 20px; border-radius: 0 0 8px 8px; }}
                    .content p {{ white-space: pre-wrap; }}
                    .footer {{ margin-top: 20px; padding-top: 15px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Thank You!</h2>
                        <p>We appreciate your interest in HUMISENSE</p>
                    </div>
                    <div class="content">
                        <p>{content}</p>
                    </div>
                    <div class="footer">
                        <p>2024 HUMISENSE. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            result = cls.send_email(lead.email, subject, html_content, content)
            
            if result:
                lead.auto_reply_sent = True
                db.session.commit()
            
            return result
            
        except Exception as e:
            cls.log_action(lead.form_type, 'auto_reply_failed', str(e))
            return False
    
    @classmethod
    def create_lead(cls, form_type, data, source_page=None):
        """Create a new lead from form data."""
        try:
            ip_address = cls.get_client_ip()
            
            # Check rate limit
            if not cls.check_rate_limit(ip_address):
                return None, "Please wait before submitting again."
            
            # Extract standard fields
            lead = Lead(
                form_type=form_type,
                name=cls.sanitize_input(data.get('name', '')),
                email=cls.sanitize_input(data.get('email', '')),
                phone=cls.sanitize_input(data.get('phone', '')),
                company=cls.sanitize_input(data.get('company', '')),
                message=cls.sanitize_input(data.get('message', '')),
                source_page=source_page or (request.url if request else None),
                ip_address=ip_address,
                user_agent=request.headers.get('User-Agent', '') if request else None
            )
            
            # Store additional form data
            standard_fields = ['name', 'email', 'phone', 'company', 'message']
            additional_data = {k: v for k, v in data.items() if k not in standard_fields}
            if additional_data:
                lead.form_data = json.dumps(additional_data)
            
            db.session.add(lead)
            db.session.commit()
            
            # Log successful submission
            cls.log_action(form_type, 'submitted', f"New submission from {lead.email}", {
                'lead_id': lead.id,
                'ip': ip_address
            })
            
            # Send admin notification
            if cls.get_setting('email_notifications_enabled', True):
                cls.send_admin_notification(lead)
            
            # Send auto-reply
            if cls.get_setting('auto_reply_enabled', True):
                cls.send_auto_reply(lead)
            
            return lead, None
            
        except Exception as e:
            cls.log_action(form_type, 'error', str(e))
            db.session.rollback()
            return None, str(e)
    
    @classmethod
    def submit_contact(cls, data, source_page=None):
        """Submit contact form."""
        # Validate required fields
        if not data.get('name'):
            return None, "Name is required"
        if not data.get('email'):
            return None, "Email is required"
        if not cls.validate_email(data['email']):
            return None, "Please enter a valid email address"
        if not data.get('message'):
            return None, "Message is required"
        
        # Validate optional phone
        if data.get('phone') and not cls.validate_phone(data['phone']):
            return None, "Please enter a valid phone number"
        
        return cls.create_lead('contact', data, source_page)
    
    @classmethod
    def submit_newsletter(cls, data, source_page=None):
        """Submit newsletter subscription."""
        if not data.get('email'):
            return None, "Email is required"
        if not cls.validate_email(data['email']):
            return None, "Please enter a valid email address"
        
        # Check if already subscribed
        existing = Lead.query.filter_by(
            form_type='newsletter',
            email=data['email']
        ).first()
        
        if existing and existing.is_archived:
            # Reactivate subscription
            existing.is_archived = False
            existing.status = 'new'
            existing.created_at = datetime.utcnow()
            db.session.commit()
            return existing, None
        
        return cls.create_lead('newsletter', data, source_page)
    
    @classmethod
    def submit_enrollment(cls, data, source_page=None):
        """Submit course enrollment."""
        if not data.get('name'):
            return None, "Name is required"
        if not data.get('email'):
            return None, "Email is required"
        if not cls.validate_email(data['email']):
            return None, "Please enter a valid email address"
        if not data.get('course_id'):
            return None, "Course selection is required"
        
        if data.get('phone') and not cls.validate_phone(data['phone']):
            return None, "Please enter a valid phone number"
        
        return cls.create_lead('enrollment', data, source_page)
    
    @classmethod
    def submit_demo(cls, data, source_page=None):
        """Submit demo request."""
        if not data.get('name'):
            return None, "Name is required"
        if not data.get('email'):
            return None, "Email is required"
        if not cls.validate_email(data['email']):
            return None, "Please enter a valid email address"
        if not data.get('product'):
            return None, "Product selection is required"
        
        if data.get('phone') and not cls.validate_phone(data['phone']):
            return None, "Please enter a valid phone number"
        
        return cls.create_lead('demo', data, source_page)
    
    @classmethod
    def submit_research(cls, data, source_page=None):
        """Submit research paper."""
        if not data.get('title'):
            return None, "Paper title is required"
        if not data.get('authors'):
            return None, "Authors are required"
        if not data.get('email'):
            return None, "Email is required"
        if not cls.validate_email(data['email']):
            return None, "Please enter a valid email address"
        if not data.get('abstract'):
            return None, "Abstract is required"
        if len(data.get('abstract', '')) < 100:
            return None, "Abstract must be at least 100 characters"
        
        return cls.create_lead('research', data, source_page)
