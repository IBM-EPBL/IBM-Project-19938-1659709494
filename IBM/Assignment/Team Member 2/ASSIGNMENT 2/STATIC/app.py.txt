from flask import Flask, render_template, flash, request, redirect, url_for, session
import sqlite3 

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists users(pid integer primary key,name TEXT, email TEXT, contact TEXT, password TEXT)")
con.close()

@app.route('/')
def home():
   return render_template('HOME.html')

@app.route('/PROFILE')
def profile():
   return render_template('PROFILE.html')

@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/signin',methods=["GET","POST"])
def signin():
   if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where email=? and password=?",(email,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["email"]=data["email"]
            session["password"]=data["password"]
            return redirect(url_for("profile"))
        else:
            flash("Username and Password Mismatch","danger")
            return redirect(url_for("home"))
   return render_template('signin.html')

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         contact=request.form['contact']
         password = request.form['password']
         password1 = request.form['password1']
         if(password==password1):
            con=sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO users (name,email,contact,password) VALUES (?,?,?,?)",(name,email,contact,password))
            con.commit()
            flash("Register successfully","success")   
         else:
            flash("Password Mismatch","danger")  
      except:
         flash("Error","danger")
      
      finally:
         return redirect(url_for("signin"))
         con.close()
   return render_template('signup.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("home"))


if __name__ == '__main__':
   app.run(debug = True)