from flask import render_template, request, redirect, url_for
from app import app, db
from models import EmployeeSheet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clock_in', methods=['POST'])
def clock_in():
    existing_entry = EmployeeSheet.query.filter_by(employee_name=request.form['employee_name'], clock_out_time=None).first()
    if existing_entry:
        return redirect(url_for('hours'))
    
    new_entry = EmployeeSheet(
        employee_name=request.form['employee_name'],
        clock_in_time=db.func.now(),
        clock_out_time=None
    )
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('hours'))

@app.route('/clock_out/<int:entry_id>', methods=['POST'])
def clock_out(entry_id):
    entry = EmployeeSheet.query.get_or_404(entry_id)
    if entry.clock_out_time is not None:
        return redirect(url_for('hours'))

    entry.clock_out_time = db.func.now()
    db.session.commit()
    return redirect(url_for('hours'))

@app.route('/hours')
def hours():
    # Query all hours from the database, ordered by time_created (newest first)
    entries = EmployeeSheet.query.order_by(EmployeeSheet.time_created.desc()).all()
    return render_template('hours.html', entries=entries)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = EmployeeSheet.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('hours'))

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        employee = EmployeeSheet.query.filter_by(employee_name=employee_name).first()
        
        if employee and employee.clock_in_time and employee.clock_out_time:
            time_spent = employee.clock_out_time - employee.clock_in_time
            hours_spent = time_spent.total_seconds() / 3600  # Convert to hours
            result = f"{employee_name} spent {round(hours_spent, 2)} hours clocked in."
        else:
            result = "Invalid data or employee not found."

        return render_template('track.html', result=result)
    return render_template('track.html', result=None)

@app.route('/profiles')
def profiles():
    return render_template('profiles.html')

