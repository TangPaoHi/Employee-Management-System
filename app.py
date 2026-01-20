from flask import Flask, request, render_template_string, redirect, url_for
import pyodbc

def show_alert(message , icon="error"):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
           <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
    </head>
    <body>
           <script>
                swal({{
                title:"Warning!",
                text:"{message}",
                icon:"{icon}",
                button:"Back",
                }}).then((value) => {{
                    window.history.back();
                }});
            </script>
    </body>
    </html>
    """            


app = Flask(__name__)


conn_str = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=sqlserver;'
    'DATABASE=master;'
    'UID=sa;'
    'PWD=Password123!;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)

def get_db_connection():
    return pyodbc.connect(conn_str)


BASE_STYLE = '''
<style>
    body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #f4f4f9; color: #333; }
    .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    h1, h2 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    
    
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 12px 15px; border-bottom: 1px solid #ddd; text-align: left; }
    th { background-color: #0078d4; color: white; }
    tr:hover { background-color: #f1f1f1; }

   
    .btn { padding: 6px 10px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; font-size: 13px; margin-right: 5px;}
    .btn-view { background: #17a2b8; color: white; }
    .btn-edit { background: #ffc107; color: black; }
    .btn-delete { background: #dc3545; color: white; }
    .btn-back { background: #6c757d; color: white; margin-top: 20px; padding: 10px 20px; font-size: 16px; }
    
    
    .add-box { background: #e9ecef; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
    .form-row { display: flex; gap: 10px; margin-bottom: 10px; }
    input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
    .btn-add { background: #28a745; color: white; padding: 10px 20px; font-size: 16px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
    .btn-add:hover { background: #218838; }
</style>
'''


INDEX_TEMPLATE = BASE_STYLE + '''
<div class="container">
    <h1>🏢 Employee Management System</h1>
    
    <div class="add-box">
        <h3>➕Add New Employee</h3>
        <form method="POST" action="/add">
            <div class="form-row">
                <input type="text" name="name" placeholder="Name *" required>
                <input type="text" name="dept" placeholder="Department*" required>
            </div>
            <div class="form-row">
                <input type="text" name="email" placeholder="Email">
                <input type="text" name="phone" placeholder="Phone Number">
                <input type="number" name="salary" placeholder="Salary">
            </div>
            <button type="submit" class="btn-add">ADD</button>
        </form>
    </div>

    <h3>📋Employee List</h3>
    <table>
        <thead>
            <tr>
                <th width="50">ID</th>
                <th>Name</th>
                <th>Department</th>
                <th width="220">Action</th>
            </tr>
        </thead>
        <tbody>
            {% for emp in employees %}
            <tr>
                <td>{{ emp.id }}</td>
                <td><strong>{{ emp.name }}</strong></td>
                <td>{{ emp.department }}</td>
                <td>
                    <a href="/view/{{ emp.id }}" class="btn btn-view">Read</a>
                    <a href="/edit/{{ emp.id }}" class="btn btn-edit">Edit</a>
                    <a href="/delete/{{ emp.id }}" class="btn btn-delete" onclick="return confirm('Are you sure you want to delete {{ emp.name }} ? ')">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div style="margin-top: 30px; text-align: center;">
        <a href="/reset_db" style="color: #999; font-size: 12px;" onclick="return confirm('Warning: This will clear all data! Are you sure?')">Reset Database</a>
    </div>
</div>
'''


VIEW_TEMPLATE = BASE_STYLE + '''
<div class="container">
    <h1>👤Employee Profile</h1>
    <div style="font-size: 16px; line-height: 2; border: 1px solid #eee; padding: 20px; border-radius: 5px;">
        <p><strong>ID:</strong> {{ emp.id }}</p>
        <p><strong>Name:</strong> {{ emp.name }}</p>
        <p><strong>Department:</strong> {{ emp.department }}</p>
        <hr>
        <p><strong>📧 Email:</strong> {{ emp.email or 'Not filled in' }}</p>
        <p><strong>📞 Phone Number:</strong> {{ emp.phone or 'Not filled in' }}</p>
        <p><strong>💰 Salary:</strong> ${{ emp.salary or '0' }}</p>
    </div>
    <a href="/" class="btn btn-back">⬅ Back</a>
    <a href="/edit/{{ emp.id }}" class="btn btn-edit" style="padding: 10px 20px; font-size: 16px;">Edit</a>
</div>
'''


EDIT_TEMPLATE = BASE_STYLE + '''
<div class="container">
    <h1>✏️ Edit Employee: {{ emp.name }}</h1>
    <form method="POST" action="/update/{{ emp.id }}" style="margin-top: 20px;">
        <div style="margin-bottom: 15px;">
            <label style="display:block; margin-bottom:5px; font-weight:bold;">Name</label>
            <input type="text" name="name" value="{{ emp.name }}" required style="width:100%;cursor:not-allowed;" readonly>
        </div>
        <div style="margin-bottom: 15px;">
            <label style="display:block; margin-bottom:5px; font-weight:bold;">Department</label>
            <input type="text" name="dept" value="{{ emp.department }}" required style="width:100%;" readonly>
        </div>
        <div style="margin-bottom: 15px;">
            <label style="display:block; margin-bottom:5px; font-weight:bold;">Email</label>
            <input type="text" name="email" value="{{ emp.email or '' }}" style="width:100%;">
        </div>
        <div style="margin-bottom: 15px;">
            <label style="display:block; margin-bottom:5px; font-weight:bold;">Phone Number</label>
            <input type="text" name="phone" value="{{ emp.phone or '' }}" style="width:100%;">
        </div>
        <div style="margin-bottom: 15px;">
            <label style="display:block; margin-bottom:5px; font-weight:bold;">Salary</label>
            <input type="number" name="salary" value="{{ emp.salary or '' }}" style="width:100%;">
        </div>
        
        <button type="submit" class="btn-add">💾 Save</button>
        <a href="/" class="btn btn-back" style="background: #999; margin-left: 0; margin-top: 10px; display:inline-block;">Cancel</a>
    </form>
</div>
'''



@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department FROM Employees")
    rows = cursor.fetchall()
    employees = [{"id": r[0], "name": r[1], "department": r[2]} for r in rows]
    return render_template_string(INDEX_TEMPLATE, employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form.get('name')
    dept = request.form.get('dept')
    email = request.form.get('email')
    phone = request.form.get('phone')
    salary = request.form.get('salary')
    
    if not name:
        return show_alert(message="Name Cannot Be Empty!",icon="error"),400

    if any(x.isdigit() for x in name):
        return show_alert(message="The Name Must Not Contain Number!",icon="error"),400

    if not dept:
        return show_alert(message="Department Cannot Be Empty!",icon="error"),400

    if not phone.isdigit():
        return show_alert(message="The Phone Number Only Can Contain Digits!",icon="error"),400
    
    if not email:
        return show_alert(message="Email Cannot Be Empty!",icon="error"),400
    
    if '@' not in email or '.' not in email:
        return show_alert(message="Invalid Email Format!",icon="error"),400


    try:
        if salary == '':
            salary = None
        else:
            salary = float (salary)
            if salary <= 0:
              return show_alert(message="Salary Cannot Be Negative And 0!",icon="error"),400
    except ValueError:
        return show_alert(message="Salary Must Be Numeric Format!",icon="error"),400


    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO Employees (name, department, email, phone, salary) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (name, dept, email, phone, salary))
    conn.commit()
    return redirect('/')

@app.route('/view/<int:id>')
def view_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, email, phone, salary FROM Employees WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        emp = {"id": row[0], "name": row[1], "department": row[2], "email": row[3], "phone": row[4], "salary": row[5]}
        return render_template_string(VIEW_TEMPLATE, emp=emp)
    return "Employee Not Found!"

@app.route('/edit/<int:id>')
def edit_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department, email, phone, salary FROM Employees WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        emp = {"id": row[0], "name": row[1], "department": row[2], "email": row[3], "phone": row[4], "salary": row[5]}
        return render_template_string(EDIT_TEMPLATE, emp=emp)
    return "Employee Not Found!"

@app.route('/update/<int:id>', methods=['POST'])
def update_employee(id):
    name = request.form.get('name')
    dept = request.form.get('dept')
    email = request.form.get('email')
    phone = request.form.get('phone')
    salary = request.form.get('salary')

    
    
    if not phone.isdigit():
        return show_alert(message="Phone Number Must Be Digits!",icon="error"),400
    
    if '@' not in email or '.' not in email:
        return show_alert(message="Invalid Email Format!Please Try Again!",icon="error"),400


    
    try:
        if salary == '':
            salary = None
        else:
            salary = float(salary)
            if salary <= 0:
                return show_alert(message="Salary Cannot Be Negative And 0!",icon="error"),400
    except ValueError:
        return show_alert(message="Salary Must Be Numeric Format!",icon="error"),400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE Employees 
        SET name=?, department=?, email=?, phone=?, salary=? 
        WHERE id=?
    """
    cursor.execute(sql, (name, dept, email, phone, salary, id))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employees WHERE id = ?", (id,))
    conn.commit()
    return redirect('/')

@app.route('/reset_db')
def reset_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS Employees")
        cursor.execute('''
            CREATE TABLE Employees (
                id INT PRIMARY KEY IDENTITY(1,1),
                name NVARCHAR(100),
                department NVARCHAR(100),
                email NVARCHAR(100),
                phone NVARCHAR(50),
                salary DECIMAL(10,2)
            )
        ''')
        conn.commit()
        return "<h1>✅ Database structure has been reset!</h1><p>New field enabled:Email, Phone, Salary。</p><a href='/'>Back</a>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)