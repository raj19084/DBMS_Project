from flask import Flask, redirect, url_for, request, render_template
from flaskext.mysql import MySQL
import requests
import urllib.parse
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MySQL@1408'
app.config['MYSQL_DATABASE_DB'] = 'DBMS_Project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



conn = mysql.connect()
cursor = conn.cursor()



insert_location = "insert into Location (Street_Number, Street_Name, Apartment_Number, City, Zip, latitude, longitude, Region_ID) values "
insert_student = "insert into Student (First_name, Middle_name, Last_name, DOB, Gender, Location_ID, Phone_number, Email_Address, Exam_ID) values "
insert_invigilator = "insert into Invigilator (First_name, Middle_name, Last_name, DOB, Gender, Location_ID, Phone_number, Email_Address) values "
insert_centre = "insert into Exam_Centre (Centre_Name, Location_ID, Capacity) values "

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/success/<name>/<role>")
def success(name, role):
    return render_template("success.html", name = name, role = role)

@app.route("/register_student/<first_name>/<middle_name>/<last_name>/<dob>/<gender>/<phoneno>/<email_address>/<exam>/<street_number>/<street_name>/<house_no>/<city>/<ZIP>")
def register_student(first_name, middle_name, last_name, dob, gender, phoneno, email_address, exam, street_number, street_name, house_no, city, ZIP):
    address = '%s, %s' % (street_name, city)
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    response = requests.get(url).json()
    lat = str(response[0]['lat'])
    lon = str(response[0]['lon'])
    q = "(%s, '%s', %s, '%s', %s, %s, %s, %s);" % (street_number, street_name, house_no, city, ZIP, lat, lon, 1)
    cursor.execute(insert_location + q)
    conn.commit()
    if(middle_name != "NULL"):
        middle_name = "'" + middle_name + "'"

    if(last_name != "NULL"):
        last_name = "'" + last_name + "'"
    else:
        last_name = "'" + last_name + "'"
    cursor.execute("SELECT LAST_INSERT_ID();")
    location_id = str(cursor.fetchone()[0])
    exam_id_query = "SELECT ID FROM Exam where Exam_name = '%s';" % exam 
    cursor.execute(exam_id_query)
    exam_id = str(cursor.fetchone()[0])
    q = "('%s', %s, %s, '%s', '%s', %s, %s, '%s', %s);" % (first_name, middle_name, last_name, dob, gender, location_id, phoneno, email_address, exam_id)
    cursor.execute(insert_student + q)
    conn.commit()
    return redirect(url_for("success", name = first_name, role = "Student"))

@app.route("/student_registration")
def student_registration():
    cursor.execute("SELECT Exam_name from Exam;")
    data = cursor.fetchall()
    return render_template("student_registration.html", data = data)

@app.route("/invigilator_registration")
def invigilator_registration():
    return render_template("invigilator_registration.html")

@app.route("/get_student_data", methods=['GET', 'POST'])
def get_student_data():
    if(request.method == 'POST'):
        first_name = request.form['firstname']
        middle_name = request.form['middlename']
        last_name = request.form['lastname']
        dob = request.form['dob']
        gender = request.form['gender']
        email_address = request.form['email']
        exam = request.form['exam']
        street_number = request.form['stnumber']
        street_name = request.form['stname']
        house_no = request.form['houseno']
        phoneno = request.form['phoneno']
        city = request.form['city']
        ZIP = request.form['zip']
        region = request.form['region']
        if(len(middle_name) == 0):
            middle_name = "NULL"
        if(len(last_name) == 0):
            last_name = "NULL"
        return redirect(url_for('register_student', first_name = first_name, middle_name = middle_name, last_name = last_name, dob = dob, gender = gender, phoneno = phoneno, email_address = email_address, exam = exam, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))
    else:
        first_name = request.args.get('firstname')
        middle_name = request.args.get('middlename')
        last_name = request.args.get('lastname')
        dob = request.args.get('dob')
        gender = request.args.get('gender')
        email_address = request.args.get('email')
        exam = request.args.get('exam')
        street_number = request.args.get('stnumber')
        street_name = request.args.get('stname')
        house_no = request.args.get('houseno')
        phoneno = request.args.get('phoneno')
        city = request.args.get('city')
        ZIP = request.args.get('zip')
        region = request.args.get('region')
        return redirect(url_for('register_student', first_name = first_name, middle_name = middle_name, last_name = last_name, dob = dob, gender = gender, phoneno = phoneno, email_address = email_address, exam = exam, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))

@app.route("/register_invigilator/<first_name>/<middle_name>/<last_name>/<dob>/<gender>/<phoneno>/<email_address>/<street_number>/<street_name>/<house_no>/<city>/<ZIP>")
def register_invigilator(first_name, middle_name, last_name, dob, gender, phoneno, email_address, street_number, street_name, house_no, city, ZIP):
    address = '%s, %s' % (street_name, city)
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    response = requests.get(url).json()
    lat = str(response[0]['lat'])
    lon = str(response[0]['lon'])
    q = "(%s, '%s', %s, '%s', %s, %s, %s, %s);" % (street_number, street_name, house_no, city, ZIP, lat, lon, 1)
    cursor.execute(insert_location + q)
    conn.commit()
    if(middle_name != "NULL"):
        middle_name = "'" + middle_name + "'"

    if(last_name != "NULL"):
        last_name = "'" + last_name + "'"
    else:
        last_name = "'" + last_name + "'"
    cursor.execute("SELECT LAST_INSERT_ID();")
    location_id = str(cursor.fetchone()[0])
    q = "('%s', %s, %s, '%s', '%s', %s, %s, '%s');" % (first_name, middle_name, last_name, dob, gender, location_id, phoneno, email_address)
    cursor.execute(insert_invigilator + q)
    conn.commit()
    return redirect(url_for("success", name = first_name, role = "Invigilator"))

@app.route("/get_invigilator_data", methods=['GET', 'POST'])
def get_invigilator_data():
    if(request.method == 'POST'):
        first_name = request.form['firstname']
        middle_name = request.form['middlename']
        last_name = request.form['lastname']
        dob = request.form['dob']
        gender = request.form['gender']
        email_address = request.form['email']
        street_number = request.form['stnumber']
        street_name = request.form['stname']
        house_no = request.form['houseno']
        phoneno = request.form['phoneno']
        city = request.form['city']
        ZIP = request.form['zip']
        region = request.form['region']
        if(len(middle_name) == 0):
            middle_name = "NULL"
        if(len(last_name) == 0):
            last_name = "NULL"
        return redirect(url_for('register_invigilator', first_name = first_name, middle_name = middle_name, last_name = last_name, dob = dob, gender = gender, phoneno = phoneno, email_address = email_address, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))
    else:
        first_name = request.args.get('firstname')
        middle_name = request.args.get('middlename')
        last_name = request.args.get('lastname')
        dob = request.args.get('dob')
        gender = request.args.get('gender')
        email_address = request.args.get('email')
        street_number = request.args.get('stnumber')
        street_name = request.args.get('stname')
        house_no = request.args.get('houseno')
        phoneno = request.args.get('phoneno')
        city = request.args.get('city')
        ZIP = request.args.get('zip')
        region = request.args.get('region')
        return redirect(url_for('register_invigilator', first_name = first_name, middle_name = middle_name, last_name = last_name, dob = dob, gender = gender, phoneno = phoneno, email_address = email_address, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))

@app.route("/user_selection")
def user_selection():
    return render_template("user_selection.html")

@app.route("/centre_registration")
def centre_registration():
    return render_template("centre_registration.html")

@app.route("/register_centre/<centre_name>/<capacity>/<street_number>/<street_name>/<house_no>/<city>/<ZIP>")
def register_centre(centre_name, capacity, street_number, street_name, house_no, city, ZIP):
    address = '%s, %s' % (street_name, city)
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    response = requests.get(url).json()
    lat = str(response[0]['lat'])
    lon = str(response[0]['lon'])
    q = "(%s, '%s', %s, '%s', %s, %s, %s, %s);" % (street_number, street_name, house_no, city, ZIP, lat, lon, 1)
    cursor.execute(insert_location + q)
    conn.commit()
    cursor.execute("SELECT LAST_INSERT_ID();")
    location_id = str(cursor.fetchone()[0])
    q = "('%s', %s, %s);" % (centre_name, location_id, capacity)
    cursor.execute(insert_centre + q)
    conn.commit()
    return redirect(url_for("success", name = centre_name, role = "Exam Centre"))

@app.route("/get_centre_data", methods=['GET', 'POST'])
def get_centre_data():
    if(request.method == 'POST'):
        centre_name = request.form['centrename']
        capacity = str(request.form['centrecapacity'])
        street_number = request.form['stnumber']
        street_name = request.form['stname']
        house_no = request.form['houseno']
        city = request.form['city']
        ZIP = request.form['zip']
        region = request.form['region']
        return redirect(url_for('register_centre', centre_name = centre_name, capacity = capacity, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))
    else:
        centre_name = request.args.get('centrename')
        capacity = request.args.get('centrecapacity')
        street_number = request.args.get('stnumber')
        street_name = request.args.get('stname')
        house_no = request.args.get('houseno')
        city = request.args.get('city')
        ZIP = request.args.get('zip')
        region = request.args.get('region')
        return redirect(url_for('register_centre', centre_name = centre_name, capacity = capacity, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))

@app.route("/table_display/<headings>/<data>")
def table_display(headings, data):
    cursor.execute("show columns from Student;")
    temp = cursor.fetchall()
    headings = []
    for i in temp:
        headings.append(i[0])
    cursor.execute("select * from Student where ID < 10;")
    data = cursor.fetchall()
    # return str(data)
    return render_template("table_display.html", headings = headings, data = data)

@app.route("/admin/user_selection")
def admin_user_selection():
    return render_template("admin_user_selection.html")

@app.route("/admin/exam/list")
def list_exam():
    cursor.execute("SELECT Exam_name FROM Exam;")
    data = cursor.fetchall()
    return render_template("list_exam.html", heading = "Select Exam", data = data)

@app.route("/admin/exam/queries/<exam>")
def exam_queries(exam):
    queries = [
        "Details of the exam",
        "Number of regions in which exam %s is conducted:" % exam,
        "Number of students taking exam %s:" %exam
    ]
    sql_queries = [
        "Select Exam_name, Exam_date, Exam_time, DURATION From Exam where Exam_name = '%s'" % exam, 
        "Select count_region as Number_Of_Regions from (Select Exam_ID,Count(Region_ID) as count_region  from Conducted_In_Region group by Exam_ID) as k where Exam_ID in (Select ID from Exam where Exam_name='%s');" % exam,
        "select count(*) as Number_Of_Students from Student where Exam_ID in (select ID from Exam where Exam_name = '%s');" % exam
    ]
    headings = [
        ["Exam name", "Exam date", "Exam time", "Duration (in hours)"],
        ["Number of regions"],
        ["Number of students"]
    ]
    query_results = []
    for q in sql_queries:
        cursor.execute(q)
        query_results.append(cursor.fetchall())
    return render_template("table_display.html", list_tables = query_results, headings = headings, title = queries)

if __name__ == '__main__':
   app.run(debug = True)