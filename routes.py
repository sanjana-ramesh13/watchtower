from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Website, MonitoringResult
from forms import SignupForm, LoginForm, AddWebsiteForm
from monitoring import run_check_for_website

def register_routes(app, limiter):
    """Register all application routes"""
    
    @app.route('/')
    def index():
        """Home page"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """User registration"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = SignupForm()
        
        # Only rate limit POST requests (form submission)
        if request.method == 'POST':
            limiter.limit("3 per minute")(lambda: None)()
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already registered', 'danger')
                return redirect(url_for('signup'))
            
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        
        return render_template('signup.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        
        # Only rate limit POST requests (form submission)
        if request.method == 'POST':
            limiter.limit("5 per minute")(lambda: None)()
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('dashboard'))
            flash('Invalid email or password', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        logout_user()
        flash('Logged out successfully', 'success')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard"""
        websites = Website.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', websites=websites)
    
    @app.route('/add-website', methods=['GET', 'POST'])
    @login_required
    def add_website():
        """Add a website to monitor"""
        form = AddWebsiteForm()
        if form.validate_on_submit():
            website = Website.query.filter_by(
                user_id=current_user.id,
                url=form.url.data
            ).first()
            
            if website:
                flash('You are already monitoring this website', 'warning')
                return redirect(url_for('dashboard'))
            
            website = Website(
                url=form.url.data,
                user_id=current_user.id,
                is_active=True
            )
            db.session.add(website)
            db.session.commit()
            
            flash(f'Started monitoring {form.url.data}', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('add_website.html', form=form)
    
    @app.route('/website/<int:website_id>/check', methods=['POST'])
    @login_required
    def check_website(website_id):
        """Manually check a website"""
        website = Website.query.get(website_id)
        
        if not website or website.user_id != current_user.id:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        try:
            result = run_check_for_website(website)
            flash(f'Check complete: {result.status_code}', 'success')
        except Exception as e:
            flash(f'Error checking website: {str(e)}', 'danger')
        
        return redirect(url_for('website_history', website_id=website_id))
    
    @app.route('/website/<int:website_id>/history')
    @login_required
    def website_history(website_id):
        """View monitoring history"""
        website = Website.query.get(website_id)
        
        if not website or website.user_id != current_user.id:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        results = MonitoringResult.query.filter_by(website_id=website_id).order_by(
            MonitoringResult.checked_at.desc()
        ).limit(100).all()
        
        return render_template('website_history.html', website=website, results=results)
    
    @app.route('/website/<int:website_id>/delete', methods=['POST'])
    @login_required
    def delete_website(website_id):
        """Delete a website"""
        website = Website.query.get(website_id)
        
        if not website or website.user_id != current_user.id:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        MonitoringResult.query.filter_by(website_id=website_id).delete()
        db.session.delete(website)
        db.session.commit()
        
        flash(f'Stopped monitoring {website.url}', 'success')
        return redirect(url_for('dashboard'))
    
    @app.route('/website/<int:website_id>/toggle', methods=['POST'])
    @login_required
    def toggle_website(website_id):
        """Toggle website monitoring"""
        website = Website.query.get(website_id)
        
        if not website or website.user_id != current_user.id:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        website.is_active = not website.is_active
        db.session.commit()
        
        status = 'enabled' if website.is_active else 'disabled'
        flash(f'Monitoring {status}', 'success')
        return redirect(url_for('dashboard'))
