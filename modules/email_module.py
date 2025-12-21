"""
Email Module for Voris
Handles email checking and notifications
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime
import json
from pathlib import Path

class EmailModule:
    """Manages email checking via IMAP"""
    
    def __init__(self, config_dir):
        self.config_dir = Path(config_dir)
        self.email_config_file = self.config_dir / "email_config.json"
        self.config = self.load_config()
        self.connection = None
    
    def load_config(self):
        """Load email configuration"""
        if self.email_config_file.exists():
            with open(self.email_config_file, 'r') as f:
                return json.load(f)
        return {
            "accounts": []
        }
    
    def save_config(self):
        """Save email configuration"""
        with open(self.email_config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def add_account(self, email_address, password, imap_server="imap.gmail.com", imap_port=993):
        """
        Add an email account
        
        Args:
            email_address: Email address
            password: App-specific password (not regular password for Gmail)
            imap_server: IMAP server address
            imap_port: IMAP port (usually 993 for SSL)
        """
        account = {
            "email": email_address,
            "password": password,
            "imap_server": imap_server,
            "imap_port": imap_port,
            "enabled": True
        }
        
        self.config["accounts"].append(account)
        self.save_config()
        
        return {
            "success": True,
            "message": f"Email account {email_address} added successfully"
        }
    
    def connect(self, account):
        """Connect to IMAP server"""
        try:
            mail = imaplib.IMAP4_SSL(account["imap_server"], account["imap_port"])
            mail.login(account["email"], account["password"])
            return mail
        except Exception as e:
            return None
    
    def get_unread_count(self, account_email=None):
        """
        Get count of unread emails
        
        Args:
            account_email: Specific account or None for all accounts
        """
        if not self.config["accounts"]:
            return {
                "success": False,
                "error": "No email accounts configured"
            }
        
        results = []
        total_unread = 0
        
        accounts = self.config["accounts"]
        if account_email:
            accounts = [a for a in accounts if a["email"] == account_email]
        
        for account in accounts:
            if not account.get("enabled", True):
                continue
            
            try:
                mail = self.connect(account)
                if not mail:
                    results.append({
                        "email": account["email"],
                        "error": "Failed to connect"
                    })
                    continue
                
                mail.select("INBOX")
                status, messages = mail.search(None, "UNSEEN")
                
                if status == "OK":
                    unread_ids = messages[0].split()
                    unread_count = len(unread_ids)
                    total_unread += unread_count
                    
                    results.append({
                        "email": account["email"],
                        "unread": unread_count
                    })
                
                mail.close()
                mail.logout()
                
            except Exception as e:
                results.append({
                    "email": account["email"],
                    "error": str(e)
                })
        
        return {
            "success": True,
            "accounts": results,
            "total_unread": total_unread
        }
    
    def get_latest_emails(self, account_email=None, count=5):
        """
        Get latest emails
        
        Args:
            account_email: Specific account or None for first configured account
            count: Number of emails to retrieve
        """
        if not self.config["accounts"]:
            return {
                "success": False,
                "error": "No email accounts configured"
            }
        
        account = None
        if account_email:
            account = next((a for a in self.config["accounts"] if a["email"] == account_email), None)
        else:
            account = self.config["accounts"][0]
        
        if not account:
            return {
                "success": False,
                "error": "Account not found"
            }
        
        try:
            mail = self.connect(account)
            if not mail:
                return {
                    "success": False,
                    "error": "Failed to connect to email server"
                }
            
            mail.select("INBOX")
            
            # Get latest emails
            status, messages = mail.search(None, "ALL")
            if status != "OK":
                return {
                    "success": False,
                    "error": "Failed to search emails"
                }
            
            email_ids = messages[0].split()
            latest_ids = email_ids[-count:] if len(email_ids) > count else email_ids
            latest_ids.reverse()  # Most recent first
            
            emails = []
            for email_id in latest_ids:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    continue
                
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Decode subject
                subject = ""
                subject_header = msg.get("Subject", "")
                if subject_header:
                    decoded = decode_header(subject_header)
                    subject = decoded[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(decoded[0][1] or "utf-8")
                
                # Get sender
                from_header = msg.get("From", "")
                
                # Get date
                date_header = msg.get("Date", "")
                
                # Check if unread
                status, flags = mail.fetch(email_id, "(FLAGS)")
                is_unread = b'\\Seen' not in flags[0]
                
                emails.append({
                    "id": email_id.decode(),
                    "from": from_header,
                    "subject": subject,
                    "date": date_header,
                    "unread": is_unread
                })
            
            mail.close()
            mail.logout()
            
            return {
                "success": True,
                "account": account["email"],
                "emails": emails
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_for_new_emails(self):
        """Quick check for new unread emails across all accounts"""
        result = self.get_unread_count()
        if result["success"] and result["total_unread"] > 0:
            return {
                "has_new": True,
                "count": result["total_unread"],
                "accounts": result["accounts"]
            }
        return {
            "has_new": False,
            "count": 0
        }
