from flask import Blueprint,Flask,request, render_template, redirect, url_for,jsonify,g,session
import os
from werkzeug import secure_filename
import json
from notifications import send_email
import sqlite3
from os import path
from random import randint

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return render_template('index.html')

@app.route('/')
def index():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select * from texts ''')
    gh = [dict(text_one=row[1],text_two=row[2],text_three=row[3])for row in cur.fetchall()]
    return render_template('index.html',gh=gh)

@app.route('/change_texts')
def change_texts():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select * from texts ''')
    gh = [dict(text_one=row[1],text_two=row[2],text_three=row[3])for row in cur.fetchall()]
    return render_template('admin_texts.html',gh=gh)

@app.route('/change_texts_save1',methods=['GET','POST'])
def change_texts_save1():
    quote_one = request.form['quote_one']
    # quote_two = request.form['quote_two']
    # quote_three = request.form['quote_three']
    print(quote_one)
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))

    db.execute('''update texts SET text1="'''+quote_one+'''" where slno=1 ''')
    db.commit()

    cur = db.execute('''select * from texts ''')
    gh = [dict(text_one=row[1],text_two=row[2],text_three=row[3])for row in cur.fetchall()]

    return render_template('admin_texts.html',gh=gh)

@app.route('/change_texts_save2',methods=['GET','POST'])
def change_texts_save2():
    # quote_one = request.form['quote_one']
    quote_two = request.form['quote_two']
    # quote_three = request.form['quote_three']
    print(quote_two)
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))

    db.execute('''update texts SET text2="'''+quote_two+'''" where slno=1 ''')
    db.commit()

    cur = db.execute('''select * from texts ''')
    gh = [dict(text_one=row[1],text_two=row[2],text_three=row[3])for row in cur.fetchall()]

    return render_template('admin_texts.html',gh=gh)

@app.route('/change_texts_save3',methods=['GET','POST'])
def change_texts_save3():
    # quote_one = request.form['quote_one']
    # quote_two = request.form['quote_two']
    quote_three = request.form['quote_three']
    print(quote_three)
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))

    db.execute('''update texts SET text3="'''+quote_three+'''" where slno=1 ''')
    db.commit()

    cur = db.execute('''select * from texts ''')
    gh = [dict(text_one=row[1],text_two=row[2],text_three=row[3])for row in cur.fetchall()]

    return render_template('admin_texts.html',gh=gh)

@app.route('/gallery')
def gallery():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select * from gallery ''')
    hj = [dict(slno=row[0],img_src=row[1]) for row in cur.fetchall()]
    return render_template('gallery.html',hj=hj)


@app.route('/careers_save',methods=['GET','POST'])
def careers_save():
    bran = request.form['bran']
    branch = request.form['branch']
    name = request.form['name']
    email = request.form['email']
    ph_no = request.form['ph_number']
    classesto = request.form['classesto']
    subjects = request.form['subjects']
    data = [branch,name,email,ph_no,classesto,subjects]

    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    db.execute('''insert into careers(branch,name,email,phno,classes,subjects) values(?,?,?,?,?,?) ''',data)
    db.commit()

    subject = "Careers Enquiry"
    fileToSend = None
    msgg = " Branch : "+branch+" \n Name : "+name+" \n EMail : "+email+" \n Phone Number : "+ph_no+"  \n Class to teachs : "+classesto+" \n Subjects : "+subjects+" "

    toaddr = "gearsaca@gmail.com"
    send_email(msgg,subject,toaddr,fileToSend)

    if bran == "yelahanka":
        return redirect(url_for('branches_yelahanka'))
    if bran == "dasarahalli":
        return redirect(url_for('branches_dasarahalli'))
    if bran == "malleswaram":
        return redirect(url_for('branches_maleswaram'))

@app.route('/enquiry_save',methods=['GET','POST'])
def enquiry_save():
    # bran = request.form['bran']
    branch = request.form['branch']
    name = request.form['name']
    email = request.form['email']
    ph_no = request.form['ph_number']
    school = request.form['school']
    classes = request.form['classes']
    data = [branch,name,email,ph_no,classes,school,'']

    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    db.execute('''insert into enquiry(branch,name,email,phno,classes,school,interest) values(?,?,?,?,?,?,?) ''',data)
    db.commit()

    subject = "Enquiry"
    fileToSend = None
    msgg = " Branch : "+branch+" \n Name : "+name+" \n EMail : "+email+" \n Phone Number : "+ph_no+" \n School : "+school+" \n Class : "+classes+" "
    if branch == 'yelahanka':
        toaddr = "ylk@gearsacademy.org"
        send_email(msgg,subject,toaddr,fileToSend)
    if branch == 'dasarahalli':
        toaddr = "tdh@gearsacademy.org"
        send_email(msgg,subject,toaddr,fileToSend)
    if branch == 'malleswaram':
        toaddr = "mlm@gearsacademy.org"
        send_email(msgg,subject,toaddr,fileToSend)

    return render_template('courses.html')

@app.route('/enquiry_save1',methods=['GET','POST'])
def enquiry_save1s():
    interest = request.form['interest']
    branch = request.form['branch']
    name = request.form['name']
    email = request.form['email']
    ph_no = request.form['ph_number']
    school = request.form['school']
    classes = request.form['classes']
    data = [branch,name,email,ph_no,classes,school,interest]

    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    db.execute('''insert into enquiry(branch,name,email,phno,classes,school,interest) values(?,?,?,?,?,?,?) ''',data)
    db.commit()

    subject = "Enquiry"
    fileToSend = None
    msgg = " Branch : "+branch+" \n Name : "+name+" \n EMail : "+email+" \n Phone Number : "+ph_no+" \n School : "+school+" \n Class : "+classes+" \n Interest : "+interest+" "
    if branch == 'yelahanka':
        toaddr = "ylk@gearsacademy.org"
        send_email(msgg,subject,toaddr,fileToSend)
    if branch == 'dasarahalli':
        toaddr = "tdh@gearsacademy.org"
        send_email(msgg,subject,toaddr,fileToSend)
    if branch == 'malleswaram':
        toaddr = "mlm@gearsacademy.org"
        send_email(msgg,subject,toaddr,fileToSend)


    return render_template('courses.html')

@app.route('/forgot_password')
def forgot_password():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select login_space from passwords where places="first" ''')
    gh = [dict(pas=row[0])for row in cur.fetchall()]

    subject = "Forgot Password"
    fileToSend = None
    msgg = " Password id : \n Subjects : "+gh[0]['pas']+" "

    toaddr = "gearsaca@gmail.com"
    send_email(msgg,subject,toaddr,fileToSend)

    return render_template('admin_login.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

# @app.route('/aboutus')
# def aboutus():
#     return render_template('aboutus.html')

@app.route('/malleswaram')
def branches_malleswaram():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select * from malleswaram ''')
    gh = [dict(img_src=row[0],branch=row[1])for row in cur.fetchall()]
    return render_template('malleswaram.html',gh=gh)

@app.route('/dasarahalli')
def branches_dasarahalli():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select * from dasarahalli ''')
    gh = [dict(img_src=row[0],branch=row[1])for row in cur.fetchall()]
    return render_template('dasarahalli.html',gh=gh)

@app.route('/yelahanka')
def branches_yelahanka():
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select * from yelahanka ''')
    gh = [dict(img_src=row[0],branch=row[1])for row in cur.fetchall()]
    return render_template('yelahanka.html',gh=gh)


@app.route('/courses1')
def courses1():
    return render_template('courses1.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/signedup',methods=['GET','POST'])
def signedup():
    user = request.form['user']
    passs = request.form['pass']
    ROOT = path.dirname(path.realpath(__file__))
    db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
    cur = db.execute('''select login_space from passwords where places="first" ''')
    gh = [dict(pas=row[0])for row in cur.fetchall()]

    if user == "admin" and passs == gh[0]['pas'] :
        session['user'] = user
        return redirect(url_for('admin_enquiry'))
    else:
        return render_template('admin_login.html',log="Username or Password Incorrect")



@app.route('/admin_enquiry')
def admin_enquiry():
    if 'user' in session:
        name = session['user']
        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        cur = db.execute('''select * from enquiry ''')
        hj = [dict(slno=row[0],name=row[1],email=row[3],phno=row[2],school=row[6],classes=row[7],branch=row[4],interest=row[5]) for row in cur.fetchall()]

        return render_template('admin_enquiry.html',hj=hj)
    return "not Logged In"

@app.route('/admin_careers')
def admin_careers():
    if 'user' in session:
        name = session['user']
        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        cur = db.execute('''select * from careers ''')
        hj = [dict(slno=row[0],name=row[1],email=row[3],phno=row[2],classes=row[5],branch=row[4],subs=row[6]) for row in cur.fetchall()]

        return render_template('admin_careers.html',hj=hj)
    return "not Logged In"


@app.route('/change_password')
def change_password():
    if 'user' in session:
        name = session['user']
        return render_template('change_password.html')
    return "not Logged In"

@app.route('/changes',methods=['GET','POST'])
def changes():
    if 'user' in session:
        name = session['user']
        pas = request.form['passs']
        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        db.execute('''update passwords SET login_space="'''+pas+'''" where places="first" ''')
        db.commit()
        return render_template('admin_login.html')
    return "not Logged In"

@app.route('/admin_malleswaram')
def admin_malleswaram():
    if 'user' in session:
        name = session['user']
        return render_template('admin_malleswaram.html')
    return "not Logged In"

@app.route('/admin_col1', methods=['GET', 'POST'])
def admin_col1():
    if 'user' in session:
        name = session['user']

        image_one = request.files['col_one']
        # image_two = request.files['col_two']
        # image_three = request.files['col_three']
        ROOT = path.dirname(path.realpath(__file__))
        file_name1 = secure_filename(image_one.filename)
        filename1 = secure_filename(image_one.filename)
        image_one.save(os.path.join(ROOT+'/static/images/',filename1))

        # file_name2 = secure_filename(image_two.filename)
        # filename2 = secure_filename(image_two.filename)
        # image_two.save(os.path.join(ROOT+'/static/images/',filename2))
        #
        # file_name3 = secure_filename(image_three.filename)
        # filename3 = secure_filename(image_three.filename)
        # image_three.save(os.path.join(ROOT+'/static/images/',filename3))

        thr1 = '/static/images/'+filename1
        # thr2 = '/static/images/'+filename2
        # thr3 = '/static/images/'+filename3

        branch = request.form['branch']

        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        db.execute('''update "'''+branch+'''" SET images="'''+thr1+'''" where place="first" ''')
        # db.execute('''update "'''+branch+'''" SET images="'''+thr2+'''" where place="second" ''')
        # db.execute('''update "'''+branch+'''" SET images="'''+thr3+'''" where place="third" ''')

        db.commit()

        if branch == "yelahanka":
            return render_template('admin_yelahanka.html')
        if branch == "dasarahalli":
            return render_template('admin_dasarahalli.html')
        if branch == "malleswaram":
            return render_template('admin_malleswaram.html')
    return "not Logged In"

@app.route('/admin_col2', methods=['GET', 'POST'])
def admin_col2():
    if 'user' in session:
        name = session['user']

        # image_one = request.files['col_one']
        image_two = request.files['col_two']
        # image_three = request.files['col_three']
        ROOT = path.dirname(path.realpath(__file__))
        # file_name1 = secure_filename(image_one.filename)
        # filename1 = secure_filename(image_one.filename)
        # image_one.save(os.path.join(ROOT+'/static/images/',filename1))

        file_name2 = secure_filename(image_two.filename)
        filename2 = secure_filename(image_two.filename)
        image_two.save(os.path.join(ROOT+'/static/images/',filename2))

        # file_name3 = secure_filename(image_three.filename)
        # filename3 = secure_filename(image_three.filename)
        # image_three.save(os.path.join(ROOT+'/static/images/',filename3))

        # thr1 = '/static/images/'+filename1
        thr2 = '/static/images/'+filename2
        # thr3 = '/static/images/'+filename3

        branch = request.form['branch']

        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        # db.execute('''update "'''+branch+'''" SET images="'''+thr1+'''" where place="first" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr2+'''" where place="second" ''')
        # db.execute('''update "'''+branch+'''" SET images="'''+thr3+'''" where place="third" ''')

        db.commit()

        if branch == "yelahanka":
            return render_template('admin_yelahanka.html')
        if branch == "dasarahalli":
            return render_template('admin_dasarahalli.html')
        if branch == "malleswaram":
            return render_template('admin_malleswaram.html')
    return "not Logged In"


@app.route('/admin_col3', methods=['GET', 'POST'])
def admin_col3():
    if 'user' in session:
        name = session['user']

        # image_one = request.files['col_one']
        # image_two = request.files['col_two']
        image_three = request.files['col_three']
        ROOT = path.dirname(path.realpath(__file__))
        # file_name1 = secure_filename(image_one.filename)
        # filename1 = secure_filename(image_one.filename)
        # image_one.save(os.path.join(ROOT+'/static/images/',filename1))
        #
        # file_name2 = secure_filename(image_two.filename)
        # filename2 = secure_filename(image_two.filename)
        # image_two.save(os.path.join(ROOT+'/static/images/',filename2))

        file_name3 = secure_filename(image_three.filename)
        filename3 = secure_filename(image_three.filename)
        image_three.save(os.path.join(ROOT+'/static/images/',filename3))

        # thr1 = '/static/images/'+filename1
        # thr2 = '/static/images/'+filename2
        thr3 = '/static/images/'+filename3

        branch = request.form['branch']

        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        # db.execute('''update "'''+branch+'''" SET images="'''+thr1+'''" where place="first" ''')
        # db.execute('''update "'''+branch+'''" SET images="'''+thr2+'''" where place="second" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr3+'''" where place="third" ''')

        db.commit()

        if branch == "yelahanka":
            return render_template('admin_yelahanka.html')
        if branch == "dasarahalli":
            return render_template('admin_dasarahalli.html')
        if branch == "malleswaram":
            return render_template('admin_malleswaram.html')
    return "not Logged In"


@app.route('/admin_fac', methods=['GET', 'POST'])
def admin_fac():
    if 'user' in session:
        name = session['user']

        image_one = request.files['col_one']
        image_two = request.files['col_two']
        image_three = request.files['col_three']
        image_four = request.files['col_four']
        image_five = request.files['col_five']
        image_six = request.files['col_six']
        image_sev = request.files['col_sev']
        image_eight = request.files['col_eight']

        ROOT = path.dirname(path.realpath(__file__))
        file_name1 = secure_filename(image_one.filename)
        filename1 = secure_filename(image_one.filename)
        image_one.save(os.path.join(ROOT+'/static/images/',filename1))

        file_name2 = secure_filename(image_two.filename)
        filename2 = secure_filename(image_two.filename)
        image_two.save(os.path.join(ROOT+'/static/images/',filename2))

        file_name3 = secure_filename(image_three.filename)
        filename3 = secure_filename(image_three.filename)
        image_three.save(os.path.join(ROOT+'/static/images/',filename3))

        file_name4 = secure_filename(image_four.filename)
        filename4 = secure_filename(image_four.filename)
        image_four.save(os.path.join(ROOT+'/static/images/',filename4))

        file_name5 = secure_filename(image_five.filename)
        filename5 = secure_filename(image_five.filename)
        image_five.save(os.path.join(ROOT+'/static/images/',filename5))

        file_name6 = secure_filename(image_six.filename)
        filename6 = secure_filename(image_six.filename)
        image_six.save(os.path.join(ROOT+'/static/images/',filename6))

        file_name7 = secure_filename(image_sev.filename)
        filename7 = secure_filename(image_sev.filename)
        image_sev.save(os.path.join(ROOT+'/static/images/',filename7))

        file_name8 = secure_filename(image_eight.filename)
        filename8 = secure_filename(image_eight.filename)
        image_eight.save(os.path.join(ROOT+'/static/images/',filename8))

        thr1 = '/static/images/'+filename1
        thr2 = '/static/images/'+filename2
        thr3 = '/static/images/'+filename3
        thr4 = '/static/images/'+filename4
        thr5 = '/static/images/'+filename5
        thr6 = '/static/images/'+filename6
        thr7 = '/static/images/'+filename7
        thr8 = '/static/images/'+filename8

        branch = request.form['branch']

        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        db.execute('''update "'''+branch+'''" SET images="'''+thr1+'''" where place="first_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr2+'''" where place="sec_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr3+'''" where place="thi_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr4+'''" where place="forth_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr5+'''" where place="five_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr6+'''" where place="six_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr7+'''" where place="sev_gallery" ''')
        db.execute('''update "'''+branch+'''" SET images="'''+thr8+'''" where place="eight_gallery" ''')

        db.commit()
        if branch == "yelahanka":
            return render_template('admin_yelahanka.html')
        if branch == "dasarahalli":
            return render_template('admin_dasarahalli.html')
        if branch == "malleswaram":
            return render_template('admin_malleswaram.html')
    return "not Logged In"

@app.route('/admin_yelahanka')
def admin_yelahanka():
    if 'user' in session:

        name = session['user']
        return render_template('admin_yelahanka.html')
    return "not Logged In"


@app.route('/admin_dasarahalli')
def admin_dasarahalli():
    if 'user' in session:
        name = session['user']
        return render_template('admin_dasarahalli.html')
    return "not Logged In"


@app.route('/admin_gallery')
def admin_gallery():
    if 'user' in session:
        name = session['user']
        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        cur = db.execute('''select * from gallery ''')
        hj = [dict(slno=row[0],img_src=row[1]) for row in cur.fetchall()]

        return render_template('admin_gallery.html',hj=hj)
    return "not Logged In"

@app.route('/admin_gallery_save', methods=['GET', 'POST'])
def admin_gallery_save():
    if 'user' in session:
        name = session['user']


        image_one = request.files['col_one']

        ROOT = path.dirname(path.realpath(__file__))
        file_name1 = secure_filename(image_one.filename)
        filename1 = secure_filename(image_one.filename)
        image_one.save(os.path.join(ROOT+'/static/images/',filename1))

        thr1 = '/static/images/'+filename1

        data = [thr1]
        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        db.execute('''insert into gallery(img_src) values(?) ''',data)
        db.commit()

        return redirect(url_for('admin_gallery'))
    return "not Logged In"

@app.route('/admin_gallery_del', methods=['GET', 'POST'])
def admin_gallery_del():
    if 'user' in session:
        name = session['user']
        slnos = request.form['slno']
        # print(slnos)
        ROOT = path.dirname(path.realpath(__file__))
        db = sqlite3.connect(path.join(ROOT, "main.sqlite"))
        db.execute('''delete from gallery where slno="'''+str(int(slnos))+'''" ''')
        db.commit()
        return redirect(url_for('admin_gallery'))
    return "not Logged In"

if __name__ == '__main__':
   app.run(debug=True)
