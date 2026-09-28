from flask import render_template, redirect, url_for, flash
from models import db, User, Website, MonitoringResult
from forms import SignupForm, LoginForm, AddWebsiteForm
from monitoring import run_check_for_website

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
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
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid email or password', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/dashboard')
    def dashboard():
        websites = Website.query.all()
        user = {'username': 'User'}
        return render_template('dashboard.html', websites=websites, user=user)
    
    @app.route('/add-website', methods=['GET', 'POST'])
    def add_website():
        form = AddWebsiteForm()
        if form.validate_on_submit():
            website = Website.query.filter_by(url=form.url.data).first()
            if website:
                flash('Website already being monitored', 'warning')
                return redirect(url_for('dashboard'))
            
            website = Website(url=form.url.data, user_id=1, is_active=True)
            db.session.add(website)
            db.session.commit()
            
            flash(f'Started monitoring {form.url.data}', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('add_website.html', form=form)
    
    @app.route('/website/<int:website_id>/check', methods=['POST'])
    def check_website(website_id):
        website = Website.query.get(website_id)
        if not website:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        try:
            result = run_check_for_website(website)
            flash(f'Check complete: {result.status_code}', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        
        return redirect(url_for('website_history', website_id=website_id))
    
    @app.route('/website/<int:website_id>/history')
    def website_history(website_id):
        website = Website.query.get(website_id)
        if not website:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        results = MonitoringResult.query.filter_by(website_id=website_id).order_by(
            MonitoringResult.checked_at.desc()
        ).limit(100).all()
        
        return render_template('website_history.html', website=website, results=results)
    
    @app.route('/website/<int:website_id>/delete', methods=['POST'])
    def delete_website(website_id):
        website = Website.query.get(website_id)
        if not website:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        MonitoringResult.query.filter_by(website_id=website_id).delete()
        db.session.delete(website)
        db.session.commit()
        
        flash(f'Stopped monitoring {website.url}', 'success')
        return redirect(url_for('dashboard'))
    
    @app.route('/website/<int:website_id>/toggle', methods=['POST'])
    def toggle_website(website_id):
        website = Website.query.get(website_id)
        if not website:
            flash('Website not found', 'danger')
            return redirect(url_for('dashboard'))
        
        website.is_active = not website.is_active
        db.session.commit()
        
        status = 'enabled' if website.is_active else 'disabled'
        flash(f'Monitoring {status}', 'success')
        return redirect(url_for('dashboard'))
