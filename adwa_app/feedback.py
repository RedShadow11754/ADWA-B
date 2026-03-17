import smtplib
import os

class EmailHandler:
    def __init__(self, feed, name, email="No Email"):
        self.status = "Failed"
        # We get the password directly from Render's Environment Variables
        email_psd = os.environ.get("EMAIL_PSD")
        sender_email = "abelalex530@gmail.com"
        receiver_email = "abelalex122129@gmail.com"

        try:
            # 1. Added port 587 and a 10-second timeout
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as connection:
                connection.starttls()
                connection.login(sender_email, email_psd)
                
                # 2. Simplified message formatting
                message = f"Subject: New Feedback from {name}\n\nName: {name}\nEmail: {email}\n\nMessage:\n{feed}"
                
                connection.sendmail(
                    from_addr=sender_email, 
                    to_addrs=receiver_email,
                    msg=message.encode('utf-8') # Added encoding for safety
                )
                self.status = "Success"
        except Exception as e:
            print(f"SMTP Error: {e}")
            self.status = f"Failed: {str(e)}"

    def status_email(self):
        return {"status": self.status}