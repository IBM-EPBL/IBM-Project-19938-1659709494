from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for
import sqlite3
import re
import hashlib
from flask_login import (login_required, login_user, logout_user)
import uuid
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
bcrypt = Bcrypt(app)
salt = "5gz"


app.config["KEY"] = "Hello"


def verify(token):
    data = jwt.decode(token, "Hello", algorithms='HS256')
    return data["email"]

@app.route('/')
def home():
    return render_template('./sign/hrsignin.html')

@app.route("/hr/signin", methods=['GET', 'POST'])
def hrSignIn():
    if request.method == "GET":
        return render_template("./sign/hrsignin.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        with sqlite3.connect('hr.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT email FROM RECRUITER WHERE email=?", (email,))
            user = cursor.fetchone()
            if user == None:
                print("No user")
                return redirect("/hr/profile")
            else:
                db_password = password+salt
                pw_hash = hashlib.md5(db_password.encode())

                cursor.execute(
                    "SELECT email,password FROM RECRUITER WHERE email=?", (email,))
                details = cursor.fetchone()
                print(details)
                if pw_hash.hexdigest() == details[1]:
                    token = jwt.encode({"email": email, 'exp': datetime.utcnow(
                    )+timedelta(minutes=30)}, "Hello", algorithm='HS256')
                    print(token)

                    response = make_response(
                        render_template("./feed/feed.html"))
                    response.set_cookie('token', token)
                    return response

                else:
                    return "wrong password"


@app.route("/hr/signup", methods=["GET", "POST"])
def hrSignUp():
    if request.method == "GET":
        return render_template("./sign/hrsignup.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm = request.form["re-password"]
        if email:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            def check(email):
                if (re.fullmatch(regex, email)):
                    print("valid email")
                else:
                    return "not an valid email"
        if password != confirm:
            return "Password mismatch"
        else:
            with sqlite3.connect('hr.db') as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """ SELECT email FROM RECRUITER WHERE email=? """, (email,))
                user = cursor.fetchone()
                print(user)
                if user == None:
                    key = uuid.uuid1().hex
                    print(key)

                    db_password = password+salt
                    pw_hash = hashlib.md5(db_password.encode())

                    cursor.execute("INSERT INTO RECRUITER (name,email,phone,password,id) VALUES (?,?,?,?,?)", (
                        name, email, phone, pw_hash.hexdigest(), key))
                    connection.commit()
                    return redirect("/hr/signin")
                else:
                    print("exists")
                    return redirect("/hr/signin")


@app.route("/hr/logout")
def logout():
    response = make_response(render_template("./sign/hrsignin.html"))
    response.set_cookie('token', '')
    return response


@app.route('/hr/feed')
def hrFeed():
    try:
        token = request.cookies.get('token')
        data = jwt.decode(token, "Hello", algorithms='HS256')
        return render_template("./feed/feed.html")
    except:
        return render_template("./feed/feed.html")


@app.route("/hr/feed/<id>")
def hrOneFeed(id):
    try:
        token = request.cookies.get('token')
        data = jwt.decode(token, "Hello", algorithms='HS256')

        print(id)
        return render_template("./feed/oneFeed.html")
    except:
        return redirect("/hr/signin")


@app.route("/hr/application")
def hrApplication():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)
        return render_template("./application/applications.html")
    except:
        return render_template("./application/applications.html")

@app.route("/hr/application/<id>")
def hrOneApplication(id):
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)

        return render_template("./application/oneApplication.html")
    except:
        return redirect("/hr/signin")


@app.route("/hr/profile")
def hrProfile():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)
        with sqlite3.connect('hr.db') as connection:
            cursor=connection.cursor()
            cursor.execute("""
            
            SELECT name,
            email,
            about_me,
            designation,
            experience ,
            url ,
            company_name ,
            company_description ,
            location ,
            website ,
            in_url 
             FROM RECRUITER WHERE email=?""", (email,))
            data=cursor.fetchone()
            print(data) 
            if not data:
                return redirect("/hr/logout")
            else:
                return render_template("./profile/viewProfile.html",data=data)


            

        
    except Exception as e:
        print(e)
        return redirect("/hr/signin")


@app.route("/hr/profile/edit")
def hrProfileEdit():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)


        with sqlite3.connect('hr.db') as connection:
            cursor=connection.cursor()
            cursor.execute("""
            
            SELECT name,
            email,
            about_me,
            designation,
            experience ,
            url ,
            company_name ,
            company_description ,
            location ,
            website ,
            in_url ,
            id
             FROM RECRUITER WHERE email=?""", (email,))
            data=cursor.fetchone()
            print(data[11]) 
            if not data:
                return redirect("/hr/logout")
            else:
                return render_template("./profile/editProfile.html",data=data)


        return render_template("./profile/editProfile.html")
    except:
        return redirect("/hr/signin")


@app.route("/hr/profile/edit/<id>",methods=("POST","GET"))
def profileEditIID(id):

    if request.method=="POST":
        
        token = request.cookies.get('token')
        print("post")
        try:
            print(email)
            email = verify(token)
            name=request.form["name"],
            
            about_me=request.form["about_me"],
            designation=request.form['designation'],
            experience=request.form['experience'],
            url=request.form['url'],
            company_name=request.form['company_name'],
            company_description=request.form['company_description'],
            location =request.form['location'],
            website=request.form['website'],
            in_url=request.form['in_url'] ,



            if not id:
                return redirect("/hr/profile")
            with sqlite3.connect('hr.db') as connection:
                cursor=connection.cursor()
                cursor.execute("""SELECT id FROM RECRUITER WHERE email=?""",(email,))
                if data[11]==id:

                    cursor.execute("""
                SELECT name,
                email,
                about_me,
                designation,
                experience ,
                url ,
                company_name ,
                company_description ,
                location ,
                website ,
                in_url ,
                id
                FROM RECRUITER WHERE email=?""", (email,))
                data=cursor.fetchone()
                cursor.execute("""
            
                    UPDATE RECRUITER SET name=?,
                    
                    about_me=?,
                    designation=?,
                    experience=?,
                    url=?,
                    company_name=? ,
                    company_description=? ,
                    location =?,
                    website=?,
                    in_url=? ,
                    
                     FROM RECRUITER WHERE email=?""", (name,
                    
                    about_me,
                    designation,
                    experience,
                    url,
                    company_name,
                    company_description ,
                    location,
                    website,
                    in_url ,email))
                connection.commit()
                return "Success"

        except Exception as e:
            print(e)
            return "failed"




@app.route("/hr/profile/pwd", methods=("GET", "POST"))
def hrProfileEditPWD():

    if request.method == "GET":

        try:
            token = request.cookies.get('token')
            email = verify(token)
            print(email)
            return render_template("./profile/passwordReset.html")

        except:
            return redirect("/hr/signin")

    else:
        try:
            token = request.cookies.get('token')
            email = verify(token)
            print(email)
            password = request.form["password"]
            newPWD = request.form['newPassword']
            confirmPWD = request.form['confirmPassword']
            print(password, newPWD, confirmPWD)
            return redirect("/hr/profile/pwd")
        except:
            return redirect("/hr/signin")

#VIEWING OPENING
@app.route("/hr/openings")
def hrOpenings():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        with sqlite3.connect('hr.db') as connection:
            cursor=connection.cursor()
            cursor.execute(""" SELECT id,title,company_name,designation,salary_range,skills_required,roles_responsibilities,company_description,location,website,author FROM OPENINGS WHERE author=?""", (email,))
            data=cursor.fetchall()
            data.reverse()
            
            connection.commit()
            return render_template("./openings/viewOpening.html",data=data)
    except Exception as e:
       # return redirect("/hr/signin")
       return render_template("./openings/viewOpening.html")

# CREATION NEW OPPENING
@app.route("/hr/openings/new", methods=('GET', 'POST'))
def hrOpeningsCreate():
    if request.method == 'GET':
        try:
            token = request.cookies.get('token')
            email = verify(token)
            

            return render_template("./openings/oneOpening.html")
        except:

            return redirect("/hr/signin")
    else:

        try:
            token = request.cookies.get('token')
            email = verify(token)
            
            title = request.form["title"]
            company_name = request.form["company_name"]

            designation = request.form["designation"]

            salary_range = request.form["salary_range"]
            skills_required = request.form["skills_required"]
            roles_responsibilities = request.form["roles_responsibilities"]
            company_description = request.form["company_description"]
            location = request.form["location"]
            website = request.form["website"]

            author = email
            
            with sqlite3.connect('hr.db') as connection:
                key = uuid.uuid1().hex
                cursor = connection.cursor()
                cursor.execute("INSERT INTO OPENINGS (id,title,company_name,designation,salary_range,skills_required,roles_responsibilities,company_description,location,website,author) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                    key, title, company_name, designation, salary_range, skills_required, roles_responsibilities, company_description, location, website, author))
                connection.commit()
                print("created successfully")

                return redirect('/hr/openings')

        except Exception as e:
            print(e)
            return redirect('/hr/openings')


# DELETEING THE  OPENINGS
@app.route("/hr/opening/<id>")
def deleteOpening(id):
    try:
        token = request.cookies.get('token')
        email = verify(token)
        with sqlite3.connect('hr.db') as connection:
            cursor=connection.cursor()
            cursor.execute(""" SELECT id FROM OPENINGS WHERE id=?""",(id,))
            data=cursor.fetchone()
            if not data:
                return redirect("/hr/openings")
            else:
                print(data[0])
                cursor.execute(""" DELETE FROM OPENINGS WHERE id=? """,(data[0],))
                connection.commit()
                return  redirect("/hr/openings") 

    except Exception as e:
        connection.commit()
        print(e)    
        return "null"





@app.route("/hr/openings/edit/<id>",methods=('GET','POST'))
def hrOpeningsOne(id):
    if request.method=="GET":
        try:
            token = request.cookies.get('token')
            email = verify(token)
            print(email)
            if not id:
                return render_template("./openings/oneOpening.html")
            with sqlite3.connect('hr.db') as connection:
                cursor=connection.cursor()
                cursor.execute("""SELECT id,author FROM OPENINGS WHERE id=? """,(id,))
                data=cursor.fetchone()
                if not data :
                    return redirect("/hr/openings")    
                elif email== data[1]:
                    cursor.execute(""" SELECT 
                    id,
                    title,company_name,
                    designation,
                    salary_range,
                    skills_required,
                    roles_responsibilities,
                    company_description,
                    location,website,
                    author
                    FROM OPENINGS WHERE id=?""", (id,))
                    data=cursor.fetchone()
                    connection.commit()
                    print(data)
                    return render_template("./openings/editing.html",data=data)
                else:
                    return redirect("/hr/openings")   
            return render_template("./openings/oneOpening.html")
        except Exception as e:
            print(e)
            return redirect("/hr/signin")
    else:


        token = request.cookies.get('token')
        email = verify(token)
        
        title = request.form["title"]
        company_name = request.form["company_name"]
        designation = request.form["designation"]
        salary_range = request.form["salary_range"]
        skills_required = request.form["skills_required"]
        roles_responsibilities = request.form["roles_responsibilities"]
        company_description = request.form["company_description"]
        location = request.form["location"]
        website = request.form["website"]
        author = email
        with sqlite3.connect('hr.db') as connection:
                cursor=connection.cursor()
                cursor.execute("""SELECT id,author FROM OPENINGS WHERE id=? """,(id,))
                data=cursor.fetchone()
                if not data :
                    return redirect("/hr/openings")    
                elif email== data[1]:
                    cursor.execute("""
                    UPDATE OPENINGS SET 
                    title=?,
                    company_name=?,designation=?,
                    salary_range=?,
                    skills_required=? ,
                    roles_responsibilities=? ,
                    company_description=?,
                    location=?,
                    website=?
                    WHERE id=? """,(title,
                    company_name,designation,
                    salary_range,
                    skills_required ,
                    roles_responsibilities ,
                    company_description,
                    location,
                    website,
                    id
))
                    data=cursor.fetchone()
                    connection.commit()
                    print(data)
                    return redirect("/hr/openings")
                else:
                    return redirect("/hr/openings") 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)