from flask_mail import Mail, Message
from flask import current_app

# Initialize Mail (will be set up in app.py)
mail = Mail()

def send_down_alert_email(user, website, result):
    """
    Send email alert when website goes down
    """
    print(f"\n📧 EMAIL FUNCTION CALLED!")
    print(f"   User: {user.email}")
    print(f"   Website: {website.name}")
    print(f"   Site is UP? {result.is_up}")
    print(f"   Alert already sent? {result.alert_sent}")
    
    # Only send if alerts enabled and alert not already sent
    if not current_app.config.get('SEND_ALERT_EMAILS'):
        print(f"   ❌ Email alerts disabled in config")
        return False
    
    if result.alert_sent:
        print(f"   ❌ Alert already sent for this check")
        return False
    
    try:
        # Build error message section
        error_section = ""
        if result.error_message:
            error_section = f"<p><strong>Error:</strong> {result.error_message}</p>"
        
        print(f"   📧 Building email message...")
        
        # Create email message
        msg = Message(
            subject=f"🚨 Alert: {website.name} is DOWN",
            recipients=[user.email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #f8d7da; padding: 20px; border-radius: 5px; border-left: 4px solid #dc3545;">
                        <h2 style="color: #721c24; margin-top: 0;">⚠️ Website Alert</h2>
                        
                        <p><strong>Website:</strong> {website.name}</p>
                        <p><strong>URL:</strong> <a href="{website.url}">{website.url}</a></p>
                        <p><strong>Status:</strong> <span style="color: #dc3545; font-weight: bold;">DOWN</span></p>
                        <p><strong>Time:</strong> {result.checked_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                        
                        {error_section}
                        
                        <hr>
                        <p>Check your WatchTower dashboard to monitor this situation:</p>
                        <p><a href="http://localhost:5000/website/{website.id}/history" style="background-color: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">View Monitoring History</a></p>
                        
                        <hr>
                        <p style="color: #666; font-size: 12px;">This is an automated alert from WatchTower. You're receiving this because you're monitoring {website.name}.</p>
                    </div>
                </body>
            </html>
            """
        )
        
        print(f"   📧 Message created, attempting to send...")
        print(f"   📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
        print(f"   📧 Mail port: {current_app.config.get('MAIL_PORT')}")
        print(f"   📧 Recipient: {user.email}")
        
        # Send email
        mail.send(msg)
        
        print(f"   ✅ Email sent successfully!")
        
        # Mark alert as sent
        result.alert_sent = True
        from models import db
        db.session.commit()
        
        print(f"✉️ Alert email sent to {user.email} for {website.name}")
        return True
        
    except Exception as e:
        print(f"   ❌ EMAIL ERROR: {str(e)}")
        print(f"   ❌ Error type: {type(e).__name__}")
        import traceback
        print(f"   ❌ Traceback: {traceback.format_exc()}")
        return False


def send_up_alert_email(user, website):
    """
    Send email when website comes back up
    """
    print(f"\n📧 RECOVERY EMAIL FUNCTION CALLED!")
    print(f"   User: {user.email}")
    print(f"   Website: {website.name}")
    
    if not current_app.config.get('SEND_ALERT_EMAILS'):
        print(f"   ❌ Email alerts disabled in config")
        return False
    
    try:
        msg = Message(
            subject=f"✅ Recovered: {website.name} is back UP",
            recipients=[user.email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <div style="background-color: #d4edda; padding: 20px; border-radius: 5px; border-left: 4px solid #28a745;">
                        <h2 style="color: #155724; margin-top: 0;">✅ Website Recovered</h2>
                        
                        <p><strong>Website:</strong> {website.name}</p>
                        <p><strong>URL:</strong> <a href="{website.url}">{website.url}</a></p>
                        <p><strong>Status:</strong> <span style="color: #28a745; font-weight: bold;">UP</span></p>
                        
                        <hr>
                        <p>Good news! Your monitored website is back online and responding normally.</p>
                        
                        <hr>
                        <p style="color: #666; font-size: 12px;">This is an automated notification from WatchTower.</p>
                    </div>
                </body>
            </html>
            """
        )
        
        print(f"   📧 Attempting to send recovery email...")
        mail.send(msg)
        print(f"✉️ Recovery email sent to {user.email} for {website.name}")
        return True
        
    except Exception as e:
        print(f"   ❌ EMAIL ERROR: {str(e)}")
        print(f"   ❌ Error type: {type(e).__name__}")
        import traceback
        print(f"   ❌ Traceback: {traceback.format_exc()}")
        return False
