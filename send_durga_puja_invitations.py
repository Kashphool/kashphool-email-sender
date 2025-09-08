#!/usr/bin/env python3
"""
Send Durga Puja invitation emails using the templated email sender.
"""

import os
import sys
from email_sender import TemplatedEmailSender

def main():
    """
    Send Durga Puja invitation emails to all recipients in the CSV file.
    """
    try:
        # Initialize email sender
        print("Initializing email sender...")
        sender = TemplatedEmailSender()
        
        # Check if CSV file exists
        csv_file = "durga_puja_recipients.csv"
        if not os.path.exists(csv_file):
            print(f"Error: CSV file '{csv_file}' not found!")
            return
        
        # Check if template exists
        template_file = "templates/durga_puja_invitation.html"
        if not os.path.exists(template_file):
            print(f"Error: Template file '{template_file}' not found!")
            return
        
        print(f"Sending Durga Puja invitations...")
        print(f"CSV file: {csv_file}")
        print(f"Template: {template_file}")
        
        # Send bulk emails
        results = sender.send_bulk_emails(
            csv_file_path=csv_file,
            template_name="durga_puja_invitation.html",
            subject_template="🪔 You're Invited: Kashphool, Durga Puja 2025! 🪔"
        )
        
        # Print results
        print("\n" + "="*50)
        print("EMAIL SENDING RESULTS")
        print("="*50)
        print(f"✅ Successfully sent: {results['success']} emails")
        print(f"❌ Failed to send: {results['failed']} emails")

        if results['failed_emails']:
            print(f"\nFailed email addresses:")
            for email in results['failed_emails']:
                print(f"  - {email}")
        
        if results['success'] > 0:
            print(f"\n🎉 Durga Puja invitations sent successfully!")
        else:
            print(f"\n⚠️  No emails were sent successfully. Please check your configuration.")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
