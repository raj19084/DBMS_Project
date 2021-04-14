from flask import Flask, redirect, url_for, request, render_template
from flaskext.mysql import MySQL
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
insert_student = "insert into Student (First_name, Middle_name, Last_name, DOB, Gender, Location_ID, Phone_number, Email_Address) values "
insert_invigilator = "insert into Invigilator (First_name, Middle_name, Last_name, DOB, Gender, Location_ID, Phone_number, Email_Address) values "


@app.route("/success/<role>")
def success(role):
    return render_template("success.html", role = role)

@app.route("/register_student/<first_name>/<middle_name>/<last_name>/<dob>/<gender>/<phoneno>/<email_address>/<street_number>/<street_name>/<house_no>/<city>/<ZIP>")
def register_student(first_name, middle_name, last_name, dob, gender, phoneno, email_address, street_number, street_name, house_no, city, ZIP):
    # return str(type(dob) is str)
    q = "(%s, '%s', %s, '%s', %s, %s, %s, %s);" % (street_number, street_name, house_no, city, ZIP, 0, 0, 1)
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
    cursor.execute(insert_student + q)
    conn.commit()
    return redirect(url_for("success", role = "Student"))

@app.route("/student_registration")
def student_registration():
    return render_template("student_registration.html")

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
        return redirect(url_for('register_student', first_name = first_name, middle_name = middle_name, last_name = last_name, dob = dob, gender = gender, phoneno = phoneno, email_address = email_address, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))
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
        return redirect(url_for('register_student', first_name = first_name, middle_name = middle_name, last_name = last_name, dob = dob, gender = gender, phoneno = phoneno, email_address = email_address, street_number = street_number, street_name = street_name, house_no = house_no, city = city, ZIP = ZIP))

@app.route("/register_invigilator/<first_name>/<middle_name>/<last_name>/<dob>/<gender>/<phoneno>/<email_address>/<street_number>/<street_name>/<house_no>/<city>/<ZIP>")
def register_invigilator(first_name, middle_name, last_name, dob, gender, phoneno, email_address, street_number, street_name, house_no, city, ZIP):
    # return str(type(dob) is str)
    q = "(%s, '%s', %s, '%s', %s, %s, %s, %s);" % (street_number, street_name, house_no, city, ZIP, 0, 0, 1)
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
    return redirect(url_for("success", role = "Invigilator"))

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

if __name__ == '__main__':
   app.run(debug = True)