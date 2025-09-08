# Templated Email Sender

A Python-based email sender that allows you to send personalized HTML emails using Gmail SMTP, with support for CSV recipient lists and Jinja2 templates.

## Features

- 📧 Gmail SMTP integration with app password authentication
- 🎨 HTML email templates using Jinja2
- 📊 CSV file support for bulk recipient management
- 🔒 Environment variable configuration for security
- 📝 Comprehensive logging and error handling
- ✅ Batch sending with success/failure tracking

## Prerequisites

- Python 3.7+
- Gmail account with 2-factor authentication enabled
- Gmail App Password (see setup instructions below)

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Gmail Setup

To use Gmail SMTP, you need to generate an App Password:

1. **Enable 2-Factor Authentication** on your Gmail account
2. Go to [Google Account Settings](https://myaccount.google.com/) > Security
3. Under "Signing in to Google", click on "App passwords"
4. Generate a new app password for "Mail"
5. Copy the 16-character password (you'll use this in the next step)

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Gmail credentials:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-16-character-app-password
   SENDER_NAME=Your Name
   ```

## Usage

### Basic Usage

```python
from email_sender import TemplatedEmailSender

# Initialize the sender
sender = TemplatedEmailSender()

# Send bulk emails
results = sender.send_bulk_emails(
    csv_file_path="recipients.csv",
    template_name="welcome_email.html",
    subject_template="Welcome {{name}}! Your account is ready",
    company_name="Your Company",
    support_email="support@yourcompany.com"
)

print(f"Successful: {results['success']}, Failed: {results['failed']}")
```

### CSV File Format

Your CSV file should contain at least `name` and `email` columns:

```csv
name,email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
```

You can add additional columns that will be available as template variables.

### Creating Templates

Templates are stored in the `templates/` directory and use Jinja2 syntax:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome {{name}}</title>
</head>
<body>
    <h1>Hello {{name}}!</h1>
    <p>Welcome to {{company_name}}!</p>
    <p>Contact us at {{support_email}}</p>
</body>
</html>
```

### Running the Script

Execute the main script:

```bash
python email_sender.py
```

Or import and use the class in your own code:

```python
from email_sender import TemplatedEmailSender

sender = TemplatedEmailSender()
# Use sender methods...
```

## Project Structure

```
templated-email-sender/
├── email_sender.py          # Main email sender class
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Your actual environment variables (create this)
├── recipients.csv          # Example CSV file
├── templates/              # Email templates directory
│   └── welcome_email.html  # Example HTML template
├── email_sender.log        # Log file (created automatically)
└── README.md              # This file
```

## Template Variables

The following variables are automatically available in templates:

- `name` - Recipient's name (from CSV)
- `email` - Recipient's email (from CSV)
- Any additional columns from your CSV file
- Any custom variables passed to `send_bulk_emails()`

## Error Handling

- All operations are logged to `email_sender.log`
- Failed emails are tracked and reported
- Network errors and authentication issues are handled gracefully
- Invalid CSV data is caught and reported

## Security Notes

- Never commit your `.env` file to version control
- Use Gmail App Passwords, not your regular password
- Keep your credentials secure and rotate them regularly

## Troubleshooting

### Common Issues

1. **Authentication Error**: Make sure you're using an App Password, not your regular Gmail password
2. **Template Not Found**: Ensure your template files are in the `templates/` directory
3. **CSV Error**: Check that your CSV has the required `name` and `email` columns
4. **SMTP Error**: Verify your internet connection and Gmail settings

### Logs

Check `email_sender.log` for detailed error information and sending status.

## License

This project is open source and available under the MIT License.
