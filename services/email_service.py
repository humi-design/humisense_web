"""
Email Service for Masterclasses
Handles all email notifications for masterclass registrations.
"""

import json
import smtplib
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, url_for
from models import SiteSettings, MasterclassEmailLog
from extensions import db


class EmailService:
    """Service for sending masterclass-related emails."""
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Get a site setting."""
        try:
            setting = SiteSettings.query.filter_by(key=key).first()
            return setting.get_value() if setting else default
        except:
            return default
    
    @classmethod
    def send_email(cls, to_email, subject, html_content, text_content=None, email_type='general'):
        """Send email notification."""
        try:
            # Get SMTP settings
            smtp_host = cls.get_setting('smtp_host', '')
            smtp_port = cls.get_setting('smtp_port', '587')
            smtp_username = cls.get_setting('smtp_username', '')
            smtp_password = cls.get_setting('smtp_password', '')
            sender_email = cls.get_setting('sender_email', 'noreply@humisense.com')
            sender_name = cls.get_setting('sender_name', 'HUMISENSE')
            
            # Debug: Print settings (only in test mode)
            print(f"DEBUG SMTP - host: '{smtp_host}', port: '{smtp_port}', user: '{smtp_username}'")
            
            # Ensure port is integer
            try:
                smtp_port = int(smtp_port) if smtp_port else 587
            except (ValueError, TypeError):
                smtp_port = 587
            
            # Skip if SMTP not configured
            if not smtp_host or not smtp_host.strip():
                print(f"Email skipped - SMTP host not set. To: {to_email}")
                print(f"  host='{smtp_host}', password set={bool(smtp_password)}")
                return False
            
            # Check if password is required but not set
            if smtp_host not in ['localhost', '127.0.0.1'] and not smtp_password:
                print(f"Email skipped - SMTP password not set. To: {to_email}")
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
            print(f"Connecting to {smtp_host}:{smtp_port}...")
            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                if smtp_port == 587:
                    server.starttls()
                server.ehlo()
                if smtp_username and smtp_password:
                    print(f"Logging in as {smtp_username}...")
                    server.login(smtp_username, smtp_password)
                print(f"Sending email to {to_email}...")
                server.send_message(msg)
            
            print(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTP Authentication Error: {e}")
            print("  - Check your SMTP username/password")
            print("  - For Gmail, make sure you're using an App Password")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP Error: {e}")
            return False
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    @classmethod
    def test_email(cls, to_email):
        """Test email configuration."""
        subject = "HUMISENSE - Test Email"
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; padding: 30px; text-align: center; border-radius: 8px;">
                <h1>✅ Test Email Successful!</h1>
            </div>
            <div style="padding: 30px; background: #f9fafb; border-radius: 8px; margin-top: 20px;">
                <p>Your SMTP settings are configured correctly.</p>
                <p>This email was sent from the HUMISENSE Admin Panel.</p>
            </div>
        </body>
        </html>
        """
        text_content = "Test email successful! Your SMTP settings are configured correctly."
        return cls.send_email(to_email, subject, html_content, text_content, 'test')
    
    @classmethod
    def generate_confirmation_email(cls, registration, masterclass):
        """Generate confirmation email content."""
        from flask import current_app
        with current_app.app_context():
            calendar_link = url_for('masterclass_detail', slug=masterclass.slug, _external=True)
        
        event_datetime = datetime.combine(masterclass.date, masterclass.time)
        event_date_str = event_datetime.strftime('%B %d, %Y')
        event_time_str = masterclass.time.strftime('%I:%M %p')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 40px 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 28px; font-weight: 700; }}
                .emoji {{ font-size: 48px; margin-bottom: 10px; }}
                .content {{ padding: 40px 30px; }}
                .success-box {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px; }}
                .details-card {{ background: #f9fafb; border-radius: 8px; padding: 25px; margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e5e7eb; }}
                .detail-row:last-child {{ border-bottom: none; }}
                .detail-label {{ font-weight: 600; color: #6b7280; }}
                .detail-value {{ color: #111827; }}
                .cta-button {{ display: inline-block; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
                .footer {{ background: #f9fafb; padding: 25px; text-align: center; font-size: 13px; color: #6b7280; }}
                .footer a {{ color: #4f46e5; text-decoration: none; }}
                .registration-id {{ background: #eef2ff; padding: 10px 20px; border-radius: 6px; font-family: monospace; font-size: 14px; display: inline-block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="emoji">🎉</div>
                    <h1>Your Seat Has Been Confirmed!</h1>
                </div>
                <div class="content">
                    <div class="success-box">
                        <h2 style="margin: 0 0 10px 0;">You're In!</h2>
                        <p style="margin: 0;">Get ready for an amazing session</p>
                    </div>
                    
                    <p>Hi {registration.first_name},</p>
                    <p>Thank you for registering for <strong>{masterclass.title}</strong>. We're thrilled to have you join us!</p>
                    {f'''
                    <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="margin: 0; color: #166534;">{masterclass.confirmation_message}</p>
                    </div>
                    ''' if masterclass.confirmation_message else ''}
                    
                    <div class="details-card">
                        <h3 style="margin-top: 0; color: #4f46e5;">📅 Event Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Date:</span>
                            <span class="detail-value">{event_date_str}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Time:</span>
                            <span class="detail-value">{event_time_str} ({masterclass.timezone})</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Duration:</span>
                            <span class="detail-value">{masterclass.duration} minutes</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Mode:</span>
                            <span class="detail-value">{masterclass.mode.title()}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Language:</span>
                            <span class="detail-value">{masterclass.language}</span>
                        </div>
                    </div>
                    
                    <p style="margin-bottom: 5px;"><strong>Your Registration ID:</strong></p>
                    <div class="registration-id">{registration.registration_id}</div>
                    
                    <div style="text-align: center;">
                        <a href="{calendar_link}" class="cta-button">📅 Add to Calendar</a>
                    </div>
                    
                    <div class="details-card">
                        <h3 style="margin-top: 0; color: #4f46e5;">👨‍🏫 Your Instructor</h3>
                        <p style="margin-bottom: 0;"><strong>{masterclass.instructor_name}</strong>{' - ' + masterclass.instructor_designation if masterclass.instructor_designation else ''}{' at ' + masterclass.instructor_company if masterclass.instructor_company else ''}</p>
                    </div>
                    
                    <p>We'll send you a reminder email 24 hours before the event with the joining link.</p>
                    
                    <p>If you have any questions, feel free to reply to this email.</p>
                    
                    <p>See you there!<br><strong>The HUMISENSE Team</strong></p>
                </div>
                <div class="footer">
                    <p>© 2024 HUMISENSE. All rights reserved.</p>
                    <p>You're receiving this email because you registered for {masterclass.title}.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Hi {registration.first_name},
        
        Your seat has been confirmed for {masterclass.title}!
        {f'\n{masterclass.confirmation_message}' if masterclass.confirmation_message else ''}
        
        EVENT DETAILS:
        Date: {event_date_str}
        Time: {event_time_str} ({masterclass.timezone})
        Duration: {masterclass.duration} minutes
        Mode: {masterclass.mode.title()}
        
        Your Registration ID: {registration.registration_id}
        
        Join link: {calendar_link}
        
        Instructor: {masterclass.instructor_name}
        
        We'll send you a reminder email 24 hours before the event.
        
        See you there!
        The HUMISENSE Team
        
        © 2024 HUMISENSE. All rights reserved.
        """
        
        return html_content, text_content
    
    @classmethod
    def send_masterclass_confirmation(cls, registration, masterclass):
        """Send confirmation email to participant."""
        subject = f"Your Seat Has Been Confirmed 🎉 - {masterclass.title}"
        html_content, text_content = cls.generate_confirmation_email(registration, masterclass)
        
        result = cls.send_email(registration.email, subject, html_content, text_content)
        
        # Log email
        try:
            email_log = MasterclassEmailLog(
                registration_id=registration.id,
                email_type='confirmation',
                subject=subject,
                sent_at=datetime.now(timezone.utc)
            )
            if not result:
                email_log.failed = True
            db.session.add(email_log)
            db.session.commit()
        except Exception as e:
            print(f"Failed to log email: {e}")
        
        return result
    
    @classmethod
    def send_masterclass_admin_notification(cls, registration, masterclass):
        """Send notification to admin about new registration."""
        admin_email = cls.get_setting('masterclass_admin_email', 'admin@humisense.com')
        
        subject = f"New Masterclass Registration - {masterclass.title}"
        
        event_datetime = datetime.combine(masterclass.date, masterclass.time)
        event_date_str = event_datetime.strftime('%B %d, %Y')
        event_time_str = masterclass.time.strftime('%I:%M %p')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; padding: 30px; }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .content {{ padding: 30px; }}
                .details-card {{ background: #f9fafb; border-radius: 8px; padding: 20px; margin: 15px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e5e7eb; }}
                .detail-row:last-child {{ border-bottom: none; }}
                .label {{ font-weight: 600; color: #6b7280; }}
                .value {{ color: #111827; }}
                .badge {{ display: inline-block; background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🆕 New Registration</h1>
                </div>
                <div class="content">
                    <p>A new participant has registered for <strong>{masterclass.title}</strong></p>
                    
                    <div class="details-card">
                        <h3 style="margin-top: 0; color: #dc2626;">Participant Details</h3>
                        <div class="detail-row">
                            <span class="label">Name:</span>
                            <span class="value"><strong>{registration.first_name} {registration.last_name}</strong></span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Email:</span>
                            <span class="value"><a href="mailto:{registration.email}">{registration.email}</a></span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Phone:</span>
                            <span class="value">{registration.phone or 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Company:</span>
                            <span class="value">{registration.company or 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Job Title:</span>
                            <span class="value">{registration.job_title or 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Country:</span>
                            <span class="value">{registration.country or 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Experience:</span>
                            <span class="value">{registration.experience.title() if registration.experience else 'N/A'}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Industry:</span>
                            <span class="value">{registration.industry or 'N/A'}</span>
                        </div>
                    </div>
                    
                    <div class="details-card">
                        <h3 style="margin-top: 0; color: #4f46e5;">Event Details</h3>
                        <div class="detail-row">
                            <span class="label">Date:</span>
                            <span class="value">{event_date_str}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Time:</span>
                            <span class="value">{event_time_str}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Status:</span>
                            <span class="value"><span class="badge">Confirmed</span></span>
                        </div>
                    </div>
                    
                    <p><strong>Registration ID:</strong> {registration.registration_id}</p>
                    <p><strong>Registered At:</strong> {registration.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Source:</strong> {registration.source_page or 'Direct'}</p>
                    <p><strong>Device:</strong> {registration.device.title() if registration.device else 'Unknown'}</p>
                </div>
                <div class="footer">
                    <p>This is an automated notification from HUMISENSE Masterclass System.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return cls.send_email(admin_email, subject, html_content)
    
    @classmethod
    def send_reminder_email(cls, registration, masterclass, reminder_type):
        """Send reminder email to participant."""
        subject_templates = {
            '24h': f"⏰ Reminder: {masterclass.title} is tomorrow!",
            '3h': f"🔔 {masterclass.title} starts in 3 hours!",
            '30m': f"🚀 {masterclass.title} starts in 30 minutes!"
        }
        
        subject = subject_templates.get(reminder_type, f"Reminder: {masterclass.title}")
        
        event_datetime = datetime.combine(masterclass.date, masterclass.time)
        event_date_str = event_datetime.strftime('%B %d, %Y')
        event_time_str = masterclass.time.strftime('%I:%M %p')
        
        countdown_text = {
            '24h': '24 hours',
            '3h': '3 hours',
            '30min': '30 minutes'
        }
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 24px; }}
                .content {{ padding: 30px; }}
                .cta-button {{ display: inline-block; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); color: white; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
                .footer {{ background: #f9fafb; padding: 20px; text-align: center; font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ {countdown_text.get(reminder_type, 'Reminder')}</h1>
                </div>
                <div class="content">
                    <p>Hi {registration.first_name},</p>
                    <p><strong>{masterclass.title}</strong> is starting in {countdown_text.get(reminder_type, 'a few minutes')}!</p>
                    
                    <p><strong>Date:</strong> {event_date_str}</p>
                    <p><strong>Time:</strong> {event_time_str} ({masterclass.timezone})</p>
                    
                    <p>Make sure you're ready to join. The session will be amazing!</p>
                    
                    <p>See you soon!<br><strong>The HUMISENSE Team</strong></p>
                </div>
                <div class="footer">
                    <p>© 2024 HUMISENSE. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        result = cls.send_email(registration.email, subject, html_content)
        
        # Update reminder sent status
        try:
            if reminder_type == '24h':
                registration.reminder_24h_sent = True
            elif reminder_type == '3h':
                registration.reminder_3h_sent = True
            elif reminder_type == '30min':
                registration.reminder_30m_sent = True
            db.session.commit()
        except Exception as e:
            print(f"Failed to update reminder status: {e}")
        
        return result
