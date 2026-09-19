import requests
import time
from datetime import datetime
from models import db, MonitoringResult, Website, User
from email_service import send_down_alert_email, send_up_alert_email

def check_website(website):
    """
    Check if a website is up and return monitoring result
    """
    
    result = MonitoringResult(website_id=website.id)
    
    try:
        start_time = time.time()
        response = requests.get(website.url, timeout=10)
        response_time_ms = (time.time() - start_time) * 1000
        
        result.status_code = response.status_code
        result.response_time_ms = response_time_ms
        result.is_up = 200 <= response.status_code < 400
        result.error_message = None
        
    except requests.exceptions.Timeout:
        result.status_code = None
        result.response_time_ms = None
        result.is_up = False
        result.error_message = 'Request timeout (>10 seconds)'
        
    except requests.exceptions.ConnectionError:
        result.status_code = None
        result.response_time_ms = None
        result.is_up = False
        result.error_message = 'Connection failed'
        
    except Exception as e:
        result.status_code = None
        result.response_time_ms = None
        result.is_up = False
        result.error_message = str(e)[:255]
    
    return result


def run_check_for_website(website):
    """
    Check a website and save result to database.
    Send alert email only on NEW outages (not repeated downs).
    """
    result = check_website(website)
    db.session.add(result)
    db.session.commit()
    
    print(f"\n🔍 CHECK RESULT for {website.name}:")
    print(f"   Is UP? {result.is_up}")
    print(f"   Status code: {result.status_code}")
    print(f"   Error: {result.error_message}")
    
    # Get the previous check result
    previous_result = MonitoringResult.query.filter_by(
        website_id=website.id
    ).order_by(MonitoringResult.checked_at.desc()).offset(1).first()
    
    user = User.query.get(website.user_id)
    
    # Send DOWN alert only if:
    # 1. Current check is DOWN
    # 2. Previous check was UP (or doesn't exist - first check)
    # This prevents duplicate alerts for ongoing outages
    if not result.is_up:
        if previous_result is None:
            # First check, and it's down
            print(f"⚠️ FIRST CHECK - WEBSITE DOWN! Sending alert...")
            send_down_alert_email(user, website, result)
        elif previous_result.is_up:
            # Was up, now down - NEW outage!
            print(f"⚠️ NEW OUTAGE! Website just went DOWN! Sending alert...")
            send_down_alert_email(user, website, result)
        else:
            # Was already down, still down - no new alert
            print(f"⚠️ Website still DOWN, but alert already sent (no duplicate)")
    else:
        print(f"✅ Website is up")
    
    # Send RECOVERY email if website just came back up
    if result.is_up and previous_result and not previous_result.is_up:
        print(f"🎉 WEBSITE RECOVERED! Sending recovery email...")
        send_up_alert_email(user, website)
    
    return result


def run_checks_for_user(user):
    """
    Check all websites for a specific user
    """
    results = []
    for website in user.websites:
        if website.is_active:
            result = run_check_for_website(website)
            results.append(result)
    return results
