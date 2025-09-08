# Kashphool Bengali Association - Email Sender

A Python-based email sender system specifically designed for the Kashphool Bengali Association's Durga Puja 2025 invitations. Features beautiful HTML email templates, Gmail SMTP integration, and bulk sending capabilities.

## Features

- 🪔 **Durga Puja 2025 Invitation System** - Beautiful, responsive HTML email templates
- 📧 Gmail SMTP integration with app password authentication
- 🎨 Professional email design with yellow banners and cultural themes
- 📊 CSV file support for bulk community member management
- 🔗 Integrated registration and cultural performance signup links
- 📱 Mobile-responsive design with cross-platform compatibility
- 🔒 Environment variable configuration for security
- 📝 Comprehensive logging and error handling
- ✅ Batch sending with success/failure tracking
- 🎯 Static styling (no dark mode variations) for consistent appearance

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

### Durga Puja Invitation Usage

To send Durga Puja 2025 invitations:

```bash
python send_durga_puja_invitations.py
```

This will automatically:
- Load recipients from `durga_puja_recipients.csv`
- Use the beautiful Durga Puja invitation template
- Send personalized invitations to all community members
- Generate detailed success/failure reports

### Custom Usage (Advanced)

```python
from email_sender import TemplatedEmailSender

# Initialize the sender
sender = TemplatedEmailSender()

# Send custom emails using the core class
results = sender.send_bulk_emails(
    csv_file_path="your_recipients.csv",
    template_name="your_template.html",
    subject_template="Your Custom Subject {{first_name}}"
)

print(f"Successful: {results['success']}, Failed: {results['failed']}")
```

### CSV File Format

For Durga Puja invitations, your CSV file should contain:

```csv
first_name,last_name,email
Pradatta,Adhikary,pradatta.adhikary@gmail.com
Kaushik,Banerjee,kaushik@example.com
Tanumoy,Talukder,tanumoy@example.com
```

**Important**: 
- Copy `durga_puja_recipients.example.csv` to `durga_puja_recipients.csv`
- Add your real community member details
- The actual CSV files are gitignored to protect privacy

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
kashphool-email-sender/
├── email_sender.py                    # Main email sender class
├── send_durga_puja_invitations.py     # Durga Puja invitation sender script
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .env                              # Your actual environment variables (create this)
├── .gitignore                        # Git ignore file (protects sensitive data)
├── durga_puja_recipients.example.csv  # Example CSV for Durga Puja invitations
├── templates/                         # Email templates directory
│   └── durga_puja_invitation.html    # Beautiful Durga Puja 2025 invitation template
├── images/                           # Email images and assets
│   ├── banner.png                    # Durga Puja banner image
│   ├── signature-logo.png            # Association logo
│   ├── facebook-50.png               # Social media icons
│   └── map.png                       # Venue location map
└── README.md                         # This file

# Files you need to create:
├── durga_puja_recipients.csv         # Your actual recipient list (gitignored)
└── email_sender.log                  # Log file (created automatically, gitignored)
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
