from apscheduler.schedulers.background import BackgroundScheduler
from models import db, Website
from monitoring import run_check_for_website

scheduler = BackgroundScheduler(daemon=True)

def check_all_websites():
    """Check all active websites every minute"""
    from datetime import datetime
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f"\n🔄 PERIODIC CHECK STARTED at {current_time}")
    
    try:
        from app import app
        with app.app_context():
            active_websites = Website.query.filter_by(is_active=True).all()
            
            if not active_websites:
                print("ℹ️ No active websites")
                return
            
            print(f"📊 Checking {len(active_websites)} websites...")
            
            for website in active_websites:
                try:
                    result = run_check_for_website(website)
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
            
            print("=" * 50)
    except Exception as e:
        print(f"❌ CHECK ERROR: {str(e)}")

# Add the scheduled job
scheduler.add_job(
    func=check_all_websites,
    trigger="interval",
    minutes=1,
    id="check_websites_job",
    name="Check all websites every minute",
    replace_existing=True
)

def start_scheduler():
    """Start the background scheduler"""
    if not scheduler.running:
        scheduler.start()
        print("✅ Scheduler started - checking websites every minute")
