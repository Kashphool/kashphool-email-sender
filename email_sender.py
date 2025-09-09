import smtplib
import csv
import os
import logging
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template, FileSystemLoader, Environment
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TemplatedEmailSender:
    """
    A class to send templated HTML emails via Gmail SMTP.
    """
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')  # App password
        self.sender_name = os.getenv('SENDER_NAME', 'Email Sender')
        
        if not self.sender_email or not self.sender_password:
            raise ValueError("SENDER_EMAIL and SENDER_PASSWORD must be set in environment variables")
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(loader=FileSystemLoader('templates'))
    
    def load_csv_data(self, csv_file_path: str) -> List[Dict]:
        """
        Load recipient data from CSV file.
        Expected columns: name, email, and any additional template variables.
        """
        try:
            recipients = []
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    recipients.append(row)
            logger.info(f"Loaded {len(recipients)} recipients from {csv_file_path}")
            return recipients
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render HTML template with provided variables.
        """
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**kwargs)
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            raise
    
    def create_email_message(self, recipient_email: str, recipient_name: str, 
                           subject: str, html_content: str) -> MIMEMultipart:
        """
        Create email message with HTML content and embedded images.
        """
        message = MIMEMultipart("related")
        message["Subject"] = subject
        message["From"] = f"{self.sender_name} <{self.sender_email}>"
        message["To"] = f"{recipient_name} <{recipient_email}>"
        
        # Create HTML part
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Embed images as attachments
        image_files = [
            ("images/banner.png", "banner"),
            ("images/map.png", "map"),
            ("images/signature-logo.png", "signature-logo"),
            ("images/facebook-50.png", "facebook-icon"),
            ("images/whatsapp-50.png", "whatsapp-icon"),
            # New fixed-color section images
            ("images/invitation_banner.png", "invitation_banner"),
            ("images/cultural_banner.png", "cultural_banner"),
            ("images/schedule.png", "schedule"),
        ]
        
        for file_path, cid in image_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        img_data = f.read()
                    
                    # Determine MIME type
                    mime_type, _ = mimetypes.guess_type(file_path)
                    if file_path.endswith('.svg'):
                        # Handle SVG files specifically
                        img = MIMEBase('image', 'svg+xml')
                        img.set_payload(img_data)
                        encoders.encode_base64(img)
                        img.add_header('Content-ID', f'<{cid}>')
                        img.add_header('Content-Disposition', 'inline', filename=os.path.basename(file_path))
                        message.attach(img)
                    elif mime_type and mime_type.startswith('image'):
                        img = MIMEImage(img_data)
                        img.add_header('Content-ID', f'<{cid}>')
                        img.add_header('Content-Disposition', 'inline', filename=os.path.basename(file_path))
                        message.attach(img)
                except Exception as e:
                    logger.warning(f"Could not attach image {file_path}: {e}")
        
        return message
    
    def send_email(self, message: MIMEMultipart) -> bool:
        """
        Send individual email via Gmail SMTP.
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_bulk_emails(self, csv_file_path: str, template_name: str, 
                        subject_template: str, **template_vars) -> Dict[str, int]:
        """
        Send bulk emails using CSV data and HTML template.
        
        Args:
            csv_file_path: Path to CSV file with recipient data
            template_name: Name of HTML template file (in templates/ directory)
            subject_template: Subject line template (can include variables)
            **template_vars: Additional variables to pass to template
        
        Returns:
            Dictionary with success/failure counts
        """
        recipients = self.load_csv_data(csv_file_path)
        results = {"success": 0, "failed": 0, "failed_emails": []}
        
        logger.info(f"Starting bulk email send to {len(recipients)} recipients")
        
        for recipient in recipients:
            try:
                # Create combined name from first_name and last_name if available
                if 'first_name' in recipient and 'last_name' in recipient:
                    recipient['name'] = f"{recipient['first_name']} {recipient['last_name']}"
                elif 'name' not in recipient:
                    recipient['name'] = recipient['email']
                
                # Merge recipient data with additional template variables
                template_data = {**recipient, **template_vars}
                
                # Render subject and HTML content
                subject = Template(subject_template).render(**template_data)
                html_content = self.render_template(template_name, **template_data)
                
                # Create and send email
                message = self.create_email_message(
                    recipient_email=recipient['email'],
                    recipient_name=recipient.get('name', recipient['email']),
                    subject=subject,
                    html_content=html_content
                )
                
                if self.send_email(message):
                    results["success"] += 1
                    logger.info(f"Email sent successfully to {recipient['email']}")
                else:
                    results["failed"] += 1
                    results["failed_emails"].append(recipient['email'])
                    logger.error(f"Failed to send email to {recipient['email']}")
                    
            except Exception as e:
                results["failed"] += 1
                results["failed_emails"].append(recipient.get('email', 'unknown'))
                logger.error(f"Error processing recipient {recipient.get('email', 'unknown')}: {e}")
        
        logger.info(f"Bulk email send completed. Success: {results['success']}, Failed: {results['failed']}")
        return results


def main():
    """
    Example usage of the TemplatedEmailSender class.
    """
    try:
        # Initialize email sender
        sender = TemplatedEmailSender()
        
        # Send bulk emails
        results = sender.send_bulk_emails(
            csv_file_path="recipients.csv",
            template_name="welcome_email.html",
            subject_template="Welcome {{name}}! Your account is ready",
            company_name="Your Company",
            support_email="support@yourcompany.com"
        )
        
        print(f"Email sending completed!")
        print(f"Successful: {results['success']}")
        print(f"Failed: {results['failed']}")
        
        if results['failed_emails']:
            print(f"Failed emails: {', '.join(results['failed_emails'])}")
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
