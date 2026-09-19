from app import limiter
from flask import render_template, request, redirect, url_for, session, flash
from functools import wraps
from models import db, User, Website, MonitoringResult
from forms import SignupForm, LoginForm, AddWebsiteForm
from monitoring import run_check_for_website, run_checks_for_user

def login_required(f):
    """Decorator to protect routes - only logged-in users can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def register_routes(app):
    """Register all routes for the application"""
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    @limiter.limit("3 per minute")
    def signup():
        """User signup route"""
        form = SignupForm(request.form)
        
        if request.method == 'POST' and form.validate():
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        
        return render_template('signup.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    @limiter.limit("5 per minute")
    def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)
    
    @app.route('/logout')
    def logout():
        """Log user out"""
        session.clear()
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard"""
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        websites = Website.query.filter_by(user_id=user_id).all()
        
        return render_template('dashboard.html', user=user, websites=websites)
    
    @app.route('/add-website', methods=['GET', 'POST'])
    @login_required
    def add_website():
        """Add a new website"""
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        form = AddWebsiteForm(request.form)
        message = None
        
        if request.method == 'POST' and form.validate():
            website = Website(
                name=form.name.data,
                url=form.url.data,
                user_id=user_id
            )
            db.session.add(website)
            db.session.commit()
            return redirect(url_for('dashboard'))
        
        return render_template('add_website.html', form=form, user=user, message=message)
    
    @app.route('/website/<int:website_id>/delete', methods=['POST'])
    @login_required
    def delete_website(website_id):
        """Delete a website"""
        user_id = session.get('user_id')
        website = Website.query.get(website_id)
        
        if website and website.user_id == user_id:
            db.session.delete(website)
            db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    @app.route('/website/<int:website_id>/check', methods=['POST'])
    @login_required
    def check_website_manual(website_id):
        """Manually check a website"""
        user_id = session.get('user_id')
        website = Website.query.get(website_id)
        
        # Verify user owns the website
        if website and website.user_id == user_id:
            run_check_for_website(website)
        
        return redirect(url_for('website_history', website_id=website_id))
    
    @app.route('/website/<int:website_id>/history')
    @login_required
    def website_history(website_id):
        """View monitoring history for a website"""
        user_id = session.get('user_id')
        website = Website.query.get(website_id)
        
        # Verify user owns the website
        if not website or website.user_id != user_id:
            return redirect(url_for('dashboard'))
        
        # Get last 20 monitoring results, ordered by most recent first
        results = MonitoringResult.query.filter_by(website_id=website_id).order_by(
            MonitoringResult.checked_at.desc()
        ).limit(20).all()
        
        return render_template('website_history.html', website=website, results=results)
