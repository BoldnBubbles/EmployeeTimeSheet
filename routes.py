from flask import render_template, request, redirect, url_for
from app import app, db
from models import EmployeeSheet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_hours', methods=['GET', 'POST'])
def add_hours():
    if request.method == 'POST':
        new_hours = EmployeeSheet(
            employee_name=request.form['employee_name'],
            hours=request.form['hours']
        )
        
        db.session.add(new_hours)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_hours.html')

@app.route('/hours')
def hours():
    # Query all hours from the database, ordered by time_created (newest first)
    hours = EmployeeSheet.query.order_by(EmployeeSheet.time_created.desc()).all()
    return render_template('hours.html', hours=hours)

@app.route('/edit_hours/<int:hours_id>', methods=['GET', 'POST'])
def edit_hours(hours_id):
    hours = EmployeeSheet.query.get_or_404(hours_id)
    
    if request.method == 'POST':
        hours.employee_name = request.form['employee_name']
        hours.hours = request.form['hours']
        
        db.session.commit()
        return redirect(url_for('hours'))
    
    return render_template('edit_hours.html', hours=hours)

@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/profiles')
def profiles():
    return render_template('profiles.html')

@app.route('/delete_hours/<int:hours_id>', methods=['POST'])
def delete_hours(hours_id):
    hours = EmployeeSheet.query.get_or_404(hours_id)
    db.session.delete(hours)
    db.session.commit()
    return redirect(url_for('hours'))