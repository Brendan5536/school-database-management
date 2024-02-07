import mysql.connector, random, openai, os
from flask import Flask, flash, session, render_template, redirect, url_for, request, jsonify
from datetime import date
app = Flask('app')

app.secret_key = "pass"


mydb = mysql.connector.connect(
    host = "HOST_SQL_HERE", # put your own stuff here
    user="username",
    password="password",
    database="university"
)
# # Create cursor object
# cursor = mydb.cursor()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # mydb = get_mysql_connection()
    cursor = mydb.cursor(dictionary=True)

    # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables!
    if request.method == 'POST':
        UserID = request.form["UserID"]
        upass = request.form["password"]
        cursor.execute("SELECT * FROM users WHERE UserID = %s AND passw = %s ",(UserID, upass))
        
        result = cursor.fetchone()
        
        if result:
            session["userID"] = result["UserID"]
            #session['userid'] = result['UserID']
            session['utype'] = result['userType']
            session['email'] = result['email']
            session["fname"] = result['fName']
            session["lname"] = result['lName']

            if(result['userType'] == 'GS'):
                return render_template("gsPage.html")
            if(result['userType'] == 'Faculty'):
                return redirect(url_for("faculty"))
            if(result['userType'] == 'ADMIN'):
                return render_template("sysadmin.html")
            # if(result['userType'] == 'Recommender'):
            #     print("it is a recommender")
                return redirect(url_for("recommender"))
            if(result['userType'] == 'Applicant'):
                return redirect(url_for("applicant"))
            if(result['userType'] == 'CAC'):
                return redirect(url_for('cac'))
            if(result['userType'] == 'Student'):
                return redirect(url_for('student'))
            if(result['userType'] == 'Alumni'):
                return redirect(url_for('alumni'))
           
            # return redirect('/')  
        # Else, give an error message and redirect them to the same login page
        else: 
            error= "Error: Username and Password Combination not found"
            return render_template("login.html",error=error)
    return render_template("login.html")
   
@app.route('/recLogin', methods=['GET', 'POST'])
def recLogin():
    cursor = mydb.cursor(dictionary=True)
    if request.method == 'POST':
        email = request.form['email']
        cursor.execute("SELECT * FROM referenceInfo WHERE (referencer1email = (%s) OR referencer2email=(%s) OR referencer3email = (%s))",(email, email, email) )
        found = cursor.fetchall()
        if found:
            session['email'] = email
            return redirect(url_for("recommender"))
    return render_template("recLogin.html")


@app.route('/alumni',methods=['GET', 'POST'])
def alumni():
    return render_template('alumni.html')




openai.api_key = "" # put your own key here

# Set up the GPT-3.5-turbo model
model_engine = "text-davinci-003"
prompt = "You are a chatbot who is implemented in a school management system. Only answer questions related to school, courses, or majors. Be nice, courteous and helpful."

def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]
    response = generate_response(prompt + "\nUser: " + message)
    return jsonify({"message": response})

@app.route('/talk',methods=['GET', 'POST'])
def talk():
    return render_template('talk.html')

@app.route('/student',methods=['GET', 'POST'])
def student():
    return render_template('studentHome.html')

#log out 
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('userID', None)
    session.pop('utype', None)
    session.pop('email', None)
    session.pop('fname', None)
    session.pop('lname', None)
    return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)

#route to faculty page
@app.route('/faculty', methods=['GET', 'POST'])
def faculty():

    # mydb = get_mysql_connection()
    if 'userID' not in session or session['utype'] != 'Faculty':
        return redirect('/')
    if session['utype'] == 'CAC':
        return redirect(url_for('/cac'))
   
    return render_template('faculty.html')



#view the list of appliciations pending
@app.route('/faculty/applications', methods= ['GET', 'POST'])
def viewList():

    # mydb = get_mysql_connection()
    if session['utype'] != 'Faculty':
        return redirect('/')
    
    cursor = mydb.cursor(dictionary=True)
    #check if user is logged i
    # if 'UserID' not in session:
    #     print("user not in session")
    #     return redirect(url_for('/'))
    #review  1 received  or review 0
    cursor.execute("SELECT IDapp FROM ApplicationChecklist WHERE transcriptReceived = 1 AND finaldecisionreceived = 0 AND (isReferenced = 1)")
    apps = cursor.fetchall()

    return render_template('listOfApplications.html', apps = apps) 

#review applications
@app.route('/faculty/applications/<IDapp>', methods= ['GET', 'POST'])
def goReview(IDapp):
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    # mydb = get_mysql_connection()
    # need to add a redirect
    print("before session")
    if session['utype'] != 'Faculty':
        if session['utype'] != 'CAC':
            return redirect('/')
    print("after session")
    cursor = mydb.cursor(dictionary=True)
    print("before post")
    if request.method == 'POST':
        print("after post")
        reviewerID = request.form["reviewerID"] #the faculty reviewer
        print("got reviewerID")
        reviewerName = request.form["reviewerName"] #name of reviewer
        print("got reviewerName ")
        #should be including rating 1-4
        rating = request.form["rating"] #rating overall
        print("got rating")
        #referencer 1
        refFrom1 = request.form['refFrom1'] #who wrote the letter
        print("got refFrom1")
        reviewerScore1 = request.form["reviewerScore1"] #rating of letter
        print("got reviewerScore1")
        isGeneric1 = request.form["isGeneric1"]
        print("got isGeneric1")
        isCredible1 = request.form["isCredible1"]
        print("got isCredible1")

        #referencer 2
        refFrom2 = request.form['refFrom2'] #who wrote the letter
        print("got refFrom2")
        reviewerScore2 = request.form["reviewerScore2"] #rating of letter
        print("got reviewerScore2")
        isGeneric2 = request.form["isGeneric2"]
        print("got isGeneric2")
        isCredible2 = request.form["isCredible2"]
        print("got isCredible2")

        #referencer 3
        refFrom3 = request.form['refFrom3'] #who wrote the letter
        print("got refFrom3")
        reviewerScore3 = request.form["reviewerScore3"] #rating of letter
        print("got reviewerScore3")
        isGeneric3 = request.form["isGeneric3"]
        print("got isGeneric3")
        isCredible3 = request.form["isCredible3"]
        print("gets referencers")

        #include comments about applicant deficiency
       
        deficiency = request.form["deficiency"]
        print("gets deficiency")
        commenting = request.form["commenting"]
        print("gets commenting")
        
        print("before if statement")
        if(reviewerName == '' or reviewerID == '' or reviewerScore1 == '' or reviewerScore2 == '' or reviewerScore3 == ''  or isGeneric1 == '' or isGeneric2 == '' or isGeneric3 == '' or isCredible1 == '' or isCredible2 == '' or isCredible3 == '' or refFrom1 == '' or refFrom2 == '' or refFrom3 == '' or rating == '' or deficiency == ''):
            error = "please fill out all forms."
            return render_template('reviewer.html', error=error)
        else:
            print("after if statement")
            #ref 1
            cursor.execute("INSERT INTO ReviewInfo(IDA, reviewerID, reviewerName, reviewerScore, isGeneric,isCredible, refFrom, rating, deficiency, commenting) VALUES ((%s),(%s),(%s),(%s),(%s), (%s),(%s),(%s),(%s),(%s))", (IDapp, reviewerID, reviewerName, reviewerScore1, isGeneric1, isCredible1, refFrom1, rating, deficiency, commenting))
            #ref 2
            cursor.execute("INSERT INTO ReviewInfo(IDA, reviewerID, reviewerName, reviewerScore, isGeneric,isCredible, refFrom, rating, deficiency, commenting) VALUES ((%s),(%s),(%s),(%s),(%s), (%s),(%s),(%s),(%s),(%s))", (IDapp, reviewerID, reviewerName, reviewerScore2, isGeneric2, isCredible2, refFrom2, rating, deficiency, commenting))
            #ref 3
            cursor.execute("INSERT INTO ReviewInfo(IDA, reviewerID, reviewerName, reviewerScore, isGeneric,isCredible, refFrom, rating, deficiency, commenting) VALUES ((%s),(%s),(%s),(%s),(%s), (%s),(%s),(%s),(%s),(%s))", (IDapp, reviewerID, reviewerName, reviewerScore3, isGeneric3, isCredible3, refFrom3, rating, deficiency, commenting))

            # cursor.execute("SELECT * FROM ApplicationChecklist WHERE IDapp = (%s)", (IDapp,))
            
            mydb.commit()
            cursor.execute("SELECT * FROM checkReview WHERE idAPP = (%s)", (IDapp,))
            checkReview = cursor.fetchall()
            if not checkReview:
                cursor.execute("INSERT INTO checkReview(idAPP, review1received, review2received, review3received) VALUES((%s), (%s), (%s), (%s))", (IDapp, True, False, False))
            elif checkReview['review2received'] == 0:
                cursor.execute("UPDATE checkReview SET review2received = 1 WHERE idAPP=(%s)",(IDapp,) )
            elif checkReview['review3received'] == 0:
                cursor.execute("UPDATE checkReview SET review3received = 1 WHERE idAPP=(%s)",(IDapp,) )
            mydb.commit()
            return redirect(url_for('/faculty'))

    #initializing them to see if it works
    fname = ''
    lname = ''
    GREScore = 0
    Verbal = 0
    Quantitative = 0
    GREAdvScore = 0
    GREAdvSbj = ''
    TOEFL = 0
    TOEFLDate = ''
    mDegree = ''
    mGPA = 0.0
    mMajor = ''
    mPriorYear = 0
    mUni = ''

    # cursor = mydb.cursor(dictionary=True)
    print(IDapp)
    cursor.execute("SELECT * from Applications INNER JOIN PriorDegree ON PriorDegree.AID = Applications.ApplicationID INNER JOIN users ON users.UserID = Applications.userIdent JOIN ApplicationChecklist ON ApplicationID = IDapp JOIN Recommendation ON Recommendation.IDApplication = Applications.applicationID JOIN referenceInfo ON referenceInfo.appID = Recommendation.IDApplication JOIN GRE ON GRE.AppID = referenceInfo.appID WHERE Applications.applicationID = (%s)",(IDapp,) )
    reviewApp = cursor.fetchone()

    if reviewApp == None:
        return redirect('/faculty/applications')

    appID = reviewApp['applicationID']
    fname = reviewApp['fName']
    lname = reviewApp['lName']
    studentNum = reviewApp['userIdent']
    sem = reviewApp['admissionSem']
    appYear = reviewApp['admissionYr']
    degreeSought = reviewApp['degreeSought']
    interests = reviewApp['interests']
    experience = reviewApp['priorWorkExperience']

    bDegree = reviewApp['DegreeType']
    GPA = reviewApp['GPA']
    major = reviewApp['Major']
    priorYear = reviewApp['priorYear']
    uni = reviewApp['University']

    if reviewApp['DegreeType'] == 'Masters' or reviewApp['DegreeType'] == 'MS':
        mDegree = reviewApp['DegreeType']
        mGPA = reviewApp['GPA']
        mMajor = reviewApp['Major']
        mPriorYear = reviewApp['priorYear']
        mUni = reviewApp['University'] 

    #For some reason, in degreetype for BS/BA this works...
    if reviewApp['DegreeType'] == 'BS'or reviewApp['DegreeType'] == 'BA':
        bDegree = reviewApp['DegreeType']
        GPA = reviewApp['GPA']
        major = reviewApp['Major']
        priorYear = reviewApp['priorYear']
        uni = reviewApp['University']

    ref1fname = reviewApp['referencer1fname']
    ref1lname = reviewApp['referencer1lname']
    ref1title = reviewApp['referencer1title']
    ref1aff = reviewApp['referencer1affil']
    ref1letter = reviewApp['letter']

    ref2fname = reviewApp['referencer2fname']
    ref2lname = reviewApp['referencer2lname']
    ref2title = reviewApp['referencer2title']
    ref2aff = reviewApp['referencer2affil']
    ref2letter = reviewApp['letter']

    ref3fname = reviewApp['referencer3fname']
    ref3lname = reviewApp['referencer3lname']
    ref3title = reviewApp['referencer3title']
    ref3aff = reviewApp['referencer3affil']
    ref3letter = reviewApp['letter']

    GREScore = reviewApp['GREScore']   
    Verbal = reviewApp['Verbal']
    Quantitative = reviewApp['Quantitative']
    GREAdvScore = reviewApp['GREAdvScore'] 
    GREAdvSbj = reviewApp['GREAdvSbj']
    TOEFL = reviewApp['TOEFL']
    TOEFLDate = reviewApp['TOEFLDate']
    examYear = reviewApp['examYear']
    # return render_template("reviewer.html", appID = appID, fn = fname, lname = lname, studentNum=studentNum, sem=sem, appYear = appYear, degreeSought = degreeSought,bDegree = bDegree, GPA = GPA, major = major,priorYear = priorYear,uni = uni, interests = interests, experience=experience, GREScore = GREScore, Verbal = Verbal, Quantitative=Quantitative, GREAdvScore = GREAdvScore, GREAdvSbj= GREAdvSbj, TOEFL=TOEFL, TOEFLDate=TOEFLDate, mDegree=mDegree,mGPA=mGPA,mMajor=mMajor, mPriorYear=mPriorYear, mUni=mUni, ref1fname = ref1fname, ref1lname = ref1lname, ref1title = ref1title, ref1aff = ref1aff, ref1letter = ref1letter,ref2fname = ref2fname, ref2lname = ref2lname, ref2title = ref2title, ref2aff = ref2aff, ref2letter = ref2letter, ref3fname = ref3fname, ref3lname = ref3lname, ref3title = ref3title, ref3aff = ref3aff, ref3letter = ref3letter)

    return render_template("reviewer.html", appID = appID, fn = fname, lname = lname, studentNum=studentNum, sem=sem, appYear = appYear, degreeSought = degreeSought,bDegree = bDegree, GPA = GPA, major = major,priorYear = priorYear,uni = uni, interests = interests, experience=experience, GREScore = GREScore, Verbal = Verbal, Quantitative=Quantitative, GREAdvScore = GREAdvScore, GREAdvSbj= GREAdvSbj, TOEFL=TOEFL, TOEFLDate=TOEFLDate, mDegree=mDegree,mGPA=mGPA,mMajor=mMajor, mPriorYear=mPriorYear, mUni=mUni,ref1fname = ref1fname, ref1lname = ref1lname, ref1title = ref1title, ref1aff = ref1aff, ref1letter = ref1letter,ref2fname = ref2fname, ref2lname = ref2lname, ref2title = ref2title, ref2aff = ref2aff, ref2letter = ref2letter, ref3fname = ref3fname, ref3lname = ref3lname, ref3title = ref3title, ref3aff = ref3aff, ref3letter = ref3letter)
mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
@app.route('/pickstudent', methods=['GET', 'POST'])
def pick_student():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE userID NOT IN (SELECT studentID FROM Student)")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM users WHERE userType='Faculty'")
    advisors = cursor.fetchall()

    return render_template('pickstudent.html', students=students, advisors=advisors)



@app.route('/apply-graduation', methods=['GET', 'POST'])
def apply_graduation():
    if request.method == 'POST':
        # get form data
        student_id = request.form['student_id']
        graduation_degree = request.form['graduation_degree']
        major = request.form['major']
        thesis = request.form['thesis']
        application_date = date.today()

        # insert into database
        cur = mydb.cursor()
        cur.execute("INSERT INTO GradApplication (student_id, application_date, graduating_status, thesis, graduating_degree) VALUES (%s, %s, %s, %s, %s)", (student_id, application_date, major, thesis, graduation_degree))
        mydb.commit()

        return redirect(url_for('success'))
    else:
        return render_template('apply-grad.html')

@app.route('/success')
def success():
    return render_template('gradsuccess.html')

@app.route('/grad-applications')
def grad_applications():
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    cur = mydb.cursor(dictionary=True)
    cur.execute("SELECT * FROM GradApplication")
    gradApplications = cur.fetchall()
    return render_template('grad-applications.html', gradApplications=gradApplications)

@app.route('/view-grad-applications')
def view_grad_applications():
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    cur = mydb.cursor(dictionary=True)
    cur.execute("SELECT student_id, graduating_degree, application_date, graduating_status, thesis, metRequirements FROM GradApplication")
    grad_applications = cur.fetchall()
    cur.close()
    return render_template('view-grad-applications.html', grad_applications=grad_applications)


@app.route('/approve-grad-application/<int:application_id>')
def approve_grad_application(application_id):
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    cur = mydb.cursor()
    cur.execute("UPDATE GradApplication SET isApproved = 1 WHERE student_id = %s", (application_id,))
    cur.execute("UPDATE users SET userType= %s WHERE userID = %s", ('Alumni', application_id))
    mydb.commit()

    return redirect(url_for('view_grad_applications'))




@app.route('/form1', methods=['GET', 'POST'])
def form1():
    if request.method == 'POST':
        # Get form data
        univ_id = request.form['univ-id']
        last_name = request.form['last-name']
        first_name = request.form['first-name']
        degree = request.form['degree']
        course_list = []
        for i in range(1, 13):
            course_dept = request.form.get(f"course-{i}")
            course_num = request.form.get(f"courseNumber-{i}")
            if course_dept and course_num:
                course_list.append(f"{course_dept} {course_num}")
        extremely_long_string = ", ".join(course_list)
        is_approved = False
        
        # Insert data into database
        cnx = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
        cursor = cnx.cursor()
        add_form1 = ("INSERT INTO Form1 "
                     "(UserID, ExtremelyLongString, IsApproved) "
                     "VALUES (%s, %s, %s)")
        data_form1 = (univ_id, extremely_long_string, is_approved)
        cursor.execute(add_form1, data_form1)
        cnx.commit()
        cursor.close()
        cnx.close()
        
        # Redirect to success page
        return render_template('form1_success.html')
    else:
        return render_template('form1.html')

db = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
@app.route('/form1s')
def list_form1s():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Form1")
    form1s = cursor.fetchall()
    return render_template('form1_list.html', form1s=form1s)

@app.route('/update_is_approved', methods=['POST'])
def update_is_approved():
    cursor = db.cursor()
    form1_id = request.form['form1_id']
    is_approved = request.form['is_approved']
    cursor.execute("UPDATE Form1 SET IsApproved=1 WHERE UserID=%s", (form1_id,))
    db.commit()
    return "Form1 updated successfully, return <a href='/faculty'>home</a>." 
    #return render_template('form1changed.html')

@app.route('/assignadvisor', methods=['POST'])
def assign_advisor():
    # Get the student ID and advisor ID from the form data
    student_id = request.form['student']
    advisor_id = request.form['advisor']

    # Update the Student table in the database
    cursor = mydb.cursor()
    cursor.execute("UPDATE Student SET advisor_id = %s WHERE studentID = %s", (advisor_id, student_id))
    mydb.commit()

    # Redirect to a confirmation page
    return render_template('assignconfirmation.html', student_id=student_id, advisor_id=advisor_id)

@app.route('/search', methods= ['GET', 'POST'])
def searchApp():

    # mydb = get_mysql_connection()
    if 'userID' not in session:
        return redirect('/')

    if session['utype'] != 'Faculty':
        if session['utype'] != 'CAC':
            return redirect('/')

    cursor = mydb.cursor(dictionary=True)
    if request.method == 'POST':
        IDapp = request.form["IDapp"]
        cursor.execute("SELECT * FROM Applications WHERE applicationID =(%s)",
                       (IDapp, ))
        result = cursor.fetchone()
        if not result: 
            return redirect(url_for('viewList'))
        if result:
            return render_template('listOfApplications.html', result=result)
    
    return redirect('/')

@app.route('/GS')
def gsHome():
    if(session['utype'] == 'CAC'):
        return redirect('/cac')
    
    if session['utype'] != 'GS':
        return redirect('/')


    return render_template('gsPage.html')

@app.route('/GS/addTranscripts', methods=['GET', 'POST'])
def addTranscripts():
    # post will go here

    # mydb = get_mysql_connection()
    if session['utype'] != 'GS':
        return redirect('/')

    if request.method == 'POST':
        thisID = request.form['id']
        cursor = mydb.cursor(buffered=True)
        # error check in case multiple applications
        cursor.execute("UPDATE ApplicationChecklist SET transcriptReceived = 1 WHERE iduser = (%s)", (thisID,))
        mydb.commit()
    
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT fname, lname, UserID FROM users JOIN ApplicationChecklist ON UserID = iduser WHERE transcriptReceived = 0")
    apps = cursor.fetchall()

    return render_template('addTranscripts.html', applicants = apps)

@app.route('/GS/decide')
def viewDecisions():

    # mydb = get_mysql_connection()
    if session['utype'] != 'GS':
        if session['utype'] != 'CAC':
            return redirect('/')


    #base info on getting appid, not user id

    cursor = mydb.cursor(dictionary=True)
    # need to error check decision recieved
    # possibly drop application checklists once final decision has been made
    cursor.execute("SELECT * FROM users JOIN ApplicationChecklist ON UserID = IDuser WHERE GREIncluded = 1 AND transcriptReceived = 1 AND isReferenced = 1 AND isReviewed= 1 AND finaldecisionreceived = 0")
    curApplicants = cursor.fetchall()

    return render_template('decideApplicants.html', applicants = curApplicants)

@app.route('/GS/<userData>', methods=['GET', 'POST'])
def decide(userData):
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    #cursor = mydb.cursor(dictionary=True)
    if session['utype'] != 'GS':
        return redirect('/')
    print("before post")
    if request.method =='POST':
        print("after post")
        #convert to int
        decision = request.form['decision']
        comment = request.form['reason']
        admissionDate = request.form['admissionDate']
        recAdvisor = request.form['recommendedAdvisor']
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("INSERT INTO DecisionInfo VALUES((%s), (%s), (%s), (%s), (%s), (%s))", (userData, session['userID'],decision,comment,admissionDate,recAdvisor))
        cursor.execute("UPDATE ApplicationChecklist SET finaldecisionreceived = 1 WHERE IDapp = (%s)", (userData,))
        mydb.commit()
        return redirect("/GS/decide")
    print("didn't post")
    cursor2 = mydb.cursor(dictionary=True)

    cursor2.execute("SELECT * FROM ReviewInfo WHERE IDA = (%s)", (userData,))
    info = cursor2.fetchall()

    cursor2.execute("SELECT * FROM Applications JOIN users ON userIdent = UserID JOIN PriorDegree ON applicationID = AID WHERE applicationID = (%s)", (userData,))
    applicant = cursor2.fetchone()
    cursor2.fetchall()
    cursor2.execute("SELECT * FROM GRE WHERE AppID = (%s)", (applicant['applicationID'],))
    gre = cursor2.fetchone()
    cursor2.fetchall()
    if gre: 
        return render_template('decideApplicantIndividual.html', information = info, userI = userData, app = applicant, gre=gre)
    
    return render_template('decideApplicantIndividual.html', information = info, userI = userData, app = applicant)

@app.route('/cac')
def cac():
    
    if session['utype'] != 'CAC':
        return redirect('/')

    return render_template('cacHome.html')

@app.route('/sysadmin')
def admin():

  
    if session['utype'] != 'ADMIN':
        return redirect('/')

    return render_template('sysadmin.html')

@app.route('/sysadmin/manage', methods=['GET', 'POST'])
def adminManage():

    # mydb = get_mysql_connection()
    if session['utype'] != 'ADMIN':
        return redirect('/')

    cursor = mydb.cursor(dictionary=True)
    if request.method == 'POST':
        deleteEmail = request.form['userEmail']
        cursor.execute('DELETE FROM users WHERE email = (%s)', (deleteEmail,))
        mydb.commit()
        flash("User deleted")


    cursor.execute("SELECT * FROM users")
    userList = cursor.fetchall()
    return render_template('sysManage.html', users = userList)

@app.route('/sysadmin/addFaculty', methods=['GET', 'POST'])
def adminAddFaculty():

    # mydb = get_mysql_connection()  
    if session['utype'] != 'ADMIN':
        return redirect('/')


    # if method = post
    if request.method == 'POST':
    # take info and create new faculty member
        firstname = request.form['fname']
        lastname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        usertype = request.form['usertype']
        primaryaddress = request.form['primaryaddress']
        primaryphone = request.form['primaryphone']
        ssn = request.form['ssn'] 
        
        newID = generateUserId()

        cursor = mydb.cursor(dictionary=True)

        # error check to make sure al forms are filled out

        cursor.execute("INSERT INTO users VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s)) ", (newID, email, password, firstname, lastname, usertype, primaryaddress, primaryphone, ssn))
        # flash to let admin know that user has been added
        mydb.commit()
        flash("User " + firstname + " "+ lastname + " has been added")

    return render_template('sysAddFaculty.html')

@app.route('/sysadmin/<userData>', methods=['GET', 'POST'])
def adminView(userData):

    # mydb = get_mysql_connection()    
    if session['utype'] != 'ADMIN':
        return redirect('/')


    # if method post, have recieved confirmation to edit a user
    if request.method == 'POST':
        change = request.form['proposedChange']
        colName = request.form['columnType']
        cur = mydb.cursor(dictionary=True)
        cur.execute(f"UPDATE users SET fName = (%s) WHERE email = (%s)", (change, userData))
        # flash admin that user values were updated
        flash("User values have been updateed")

    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = (%s)", (userData,))
    currentValues = cursor.fetchone()
    return render_template('sysViewUser.html', values = currentValues)

def generateUserId():

    # mydb = get_mysql_connection()
    cursor = mydb.cursor(dictionary=True)
    while(1):

        id = str(random.randint(10000000,99999999))
        cursor.execute("SELECT * FROM users WHERE UserID = (%s)",(id,))

        result = cursor.fetchone()
        if not result: #if result does not exist, return the id
            return id

@app.route('/recommender', methods=['GET','POST'])
def recommender():

    # mydb = get_mysql_connection() 
     

    # if session['utype'] != 'Recommender':
    #     return redirect('/')
    
    cursor = mydb.cursor(dictionary=True)
    
    #cursor.execute("SELECT * FROM Applications JOIN ApplicationChecklist ON applicationID = IDapp WHERE referencer1email = (%s) AND reference1Recieved = 0",(session['email'],))
    cursor.execute("SELECT * FROM referenceInfo JOIN checkReference ON referenceInfo.appID = checkReference.idApp JOIN Applications ON referenceInfo.appID = Applications.applicationID WHERE referenceInfo.referencer1email = (%s) AND checkReference.reference1received = 0", (session['email'],))
    reference1 = cursor.fetchone()
    test = cursor.fetchone()
    while test != None:
        test = cursor.fetchone()
    #cursor.execute("SELECT * FROM Applications JOIN ApplicationChecklist ON applicationID = IDapp WHERE referencer2email = (%s) AND reference2Recieved = 0",(session['email'],))
    cursor.execute("SELECT * FROM referenceInfo JOIN checkReference ON referenceInfo.appID = checkReference.idApp JOIN Applications ON referenceInfo.appID = Applications.applicationID WHERE referenceInfo.referencer2email = (%s) AND checkReference.reference2received = 0", (session['email'],))
    reference2 = cursor.fetchone()
    test = cursor.fetchone()
    while test != None:
        test = cursor.fetchone()

    cursor.execute("SELECT * FROM referenceInfo JOIN checkReference ON referenceInfo.appID = checkReference.idApp JOIN Applications ON referenceInfo.appID = Applications.applicationID WHERE referenceInfo.referencer3email = (%s) AND checkReference.reference3received = 0", (session['email'],))
    reference3 = cursor.fetchone()
    print("check if it is ref3")
    test = cursor.fetchone()
    while test != None:
        test = cursor.fetchone()
    

    if reference1 != None:
        
        if request.method == 'POST':
            
            rec = request.form['recommendation']

            cursor.execute("INSERT INTO Recommendation(referencerfname, referencerlname, letter, IDApplication) VALUES((%s), (%s), (%s), (%s))", (reference1['referencer1fname'], reference1['referencer1lname'], rec, reference1['applicationID']))

            cursor.execute("UPDATE checkReference SET reference1received = 1 WHERE idApp = (%s)", (reference1['applicationID'],))
            mydb.commit()
            
            return redirect("/")
       
        cursor.execute("SELECT * FROM users WHERE UserID = (%s)", (reference1['userIdent'],))
        applicant = cursor.fetchone()
        return render_template("recommender.html", fname = applicant['fName'], lname = applicant['lName'])
    
    elif reference2 != None:
        
        if request.method == 'POST':
            rec = request.form['recommendation']

            cursor.execute("INSERT INTO Recommendation(referencerfname, referencerlname, letter, IDApplication) VALUES((%s), (%s), (%s), (%s))", (reference2['referencer2fname'], reference2['referencer2lname'], rec, reference2['applicationID']))

            cursor.execute("UPDATE checkReference SET reference2received = 1 WHERE IDapp = (%s)", (reference2['applicationID'],))
            mydb.commit()

            return redirect("/")

        cursor.execute("SELECT * FROM users WHERE UserID = (%s)", (reference2['userIdent'],))
        applicant = cursor.fetchone()
        return render_template("recommender.html")

    elif reference3 != None:
        print(reference3)
        if request.method == 'POST':
            rec = request.form['recommendation']

            cursor.execute("INSERT INTO Recommendation(referencerfname, referencerlname, letter, IDApplication) VALUES((%s), (%s), (%s), (%s))", (reference3['referencer3fname'], reference3['referencer3lname'], rec, reference3['applicationID']))

            cursor.execute("UPDATE checkReference SET reference3received = 1 WHERE IDapp = (%s)", (reference3['applicationID'],))
            mydb.commit()
            return redirect("/")
        cursor.execute("SELECT * FROM users WHERE UserID = (%s)", (reference3['userIdent'],))
        applicant = cursor.fetchone()
        return render_template("recommender.html")

    print("reaches here")
    return redirect('/')

def generateAppID():

    # mydb = get_mysql_connection()
    cursor = mydb.cursor(dictionary=True)
    while(1):
        id = str(random.randint(10000000,99999999))
        cursor.execute("SELECT * FROM Applications WHERE applicationID = (%s)",(id,))
        result = cursor.fetchone()

        if not result: #if result does not exist, return the id
            return id

@app.route('/applicant/',methods=['GET','POST'])
def applicant():
    
    # mydb = get_mysql_connection()
    
    if 'userID' not in session or session['utype'] != 'Applicant':
        return redirect('/')

    cursor = mydb.cursor(dictionary=True)
    userid = session["userID"]

    #check status of application
    cursor.execute("SELECT * FROM ApplicationChecklist WHERE transcriptReceived = 1 AND isReviewed = 1 AND isReferenced = 1 AND finaldecisionreceived=1 AND isCompleted=1 AND IDuser = (%s)", (userid,))
    decisionMade = cursor.fetchall()

    cursor.execute("SELECT * FROM ApplicationChecklist WHERE transcriptReceived = 1 AND (isReviewed = 0 OR finaldecisionreceived = 0) AND isReferenced = 1 AND isCompleted =1 AND IDuser = (%s)", (userid,))
    completed = cursor.fetchall()
   
    cursor.execute("SELECT * FROM ApplicationChecklist WHERE (transcriptReceived = 0 OR isReferenced = 0 OR isCompleted = 0) AND IDuser = (%s)", (userid,))
    incomplete = cursor.fetchall()

    if decisionMade:
       print("decision ready to be viewed")
       status = "A Decision Has Been Made. Please Check on your Portal"
    elif completed:
        print("complete:")
        print(completed)
        status = "Application Complete and Under Review/No Decision Yet"
    elif incomplete:
        print("incomplete")
        print(incomplete)
        status = "Application Incomplete - materials missing"
    else:
        status = "Status Currently Not Available"

    #check if application has at least one reference
    cursor.execute("SELECT * FROM checkReference JOIN ApplicationChecklist ON ApplicationChecklist.IDapp = checkReference.idApp WHERE (reference1received=1 OR reference2received=1 OR reference3received=1) AND IDuser=(%s)", (userid,))
    refReceived = cursor.fetchall()
    if refReceived:
        cursor.execute("UPDATE ApplicationChecklist SET isReferenced=1 WHERE IDuser=(%s)",(userid,))
        mydb.commit()

    #check if application is complete and ready to review
    #for doctoral
    cursor.execute("SELECT * FROM ApplicationChecklist JOIN Applications ON ApplicationChecklist.IDapp = Applications.applicationID WHERE degreeSought=1 AND GREIncluded=1 AND transcriptReceived=1 AND isReferenced=1 AND IDuser =(%s)", (userid,))
    foundD = cursor.fetchall()
    #for masters
    cursor.execute("SELECT * FROM ApplicationChecklist JOIN Applications ON ApplicationChecklist.IDapp = Applications.applicationID WHERE degreeSought=0 AND transcriptReceived=1 AND isReferenced=1 AND IDuser =(%s)", (userid,))
    foundM = cursor.fetchall()
    if foundD:
        cursor.execute("UPDATE ApplicationChecklist SET isCompleted=1 WHERE IDuser=(%s)",(userid,))
        mydb.commit()
    elif foundM:
        cursor.execute("UPDATE ApplicationChecklist SET isCompleted=1 WHERE IDuser=(%s)",(userid,))
        mydb.commit()

    #check if application has at least one review
    cursor.execute("SELECT * FROM checkReview JOIN ApplicationChecklist ON ApplicationChecklist.IDapp = checkReview.idAPP WHERE (review1received=1 OR review2received=1 OR review3received=1) AND IDuser=(%s)", (userid,))
    revReceived = cursor.fetchall()
    if revReceived:
        cursor.execute("UPDATE ApplicationChecklist SET isReviewed=1 WHERE IDuser=(%s)",(userid,))
        mydb.commit()
    

    cursor.execute("SELECT * FROM ApplicationChecklist WHERE IDuser = %s",(userid,))
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM Applications WHERE userIdent = %s ORDER BY applicationID ASC",(userid,))
    data = cursor.fetchall()
    required = []
    if data:
        for i in data:
            if(i["degreeSought"] == 1):
                required.append("YES")
            if(i["degreeSought"] == 0):
                required.append("NO")
        
    
    if result:
        return render_template("applicant.html",all=zip(result,required), status=status)
    else:
        return render_template("applicant.html",all=zip(result,required), status =status)

# UNUSED CODE. ABSOLUTELY WORTHLESS BUT IN HERE IN CASE WE WANT TO MAKE A MODIFIED APPLICATIONS PAGE.
@app.route('/applications/', methods =['GET','POST'])
def applications():
    
    # mydb = get_mysql_connection()
    if session['utype'] != 'Applicant':
        return redirect('/')


   
    cursor = mydb.cursor(dictionary=True)
    userid = session["userid"]
    cursor.execute("SELECT * FROM ApplicationChecklist WHERE IDuser = %s ORDER BY IDapp ASC",(userid,))
    result = cursor.fetchall()
    cursor.execute("SELECT * FROM Applications WHERE userIdent = %s ORDER BY applicationID ASC",(userid,))
    data = cursor.fetchall()
    required = []
    if data:
        for i in data:
            if(i["degreeSought"] == 1):
                required.append("YES")
            if(i["degreeSought"] == 0):
                required.append("NO")
        
    
    if result:
        return render_template("applications.html",result=result,required=required)
    else:
        return render_template("applications.html",result=result,required=required)


@app.route('/applications/editgre/<aid>/<uid>',methods=['GET','POST'])
def greAddEdit(aid,uid):
    
    # mydb = get_mysql_connection()

    error = None
    # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables!
    if request.method == 'GET':
        # connection = sqlite3.connect('myDatabase.db')
        # connection.row_factory = sqlite3.Row
        # c = connection.cursor()

        return render_template('gre.html',error=error,aid=aid,uid=uid)

    if request.method == 'POST':
        c =  mydb.cursor(buffered=True,dictionary=True)
        greverbal = request.form["greverbal"]
        grequantitative = request.form["grequantitative"]
        gretotal = greverbal+grequantitative
        greascore = request.form["greascore"]
        greasubject = request.form["greasubject"]
        toefl = request.form["toefl"]
        toefldate= request.form["toefl"]
        greyear = request.form["greyear"]


        if(greverbal == '' or grequantitative == '' or greascore == '' or greasubject == '' or toefl == '' or toefldate == '' or greyear == '' ) :
          error = "please fill out all forms."
          return render_template('gre.html', error=error,aid=aid,uid=uid)

          
        c.execute("SELECT * FROM GRE WHERE AppID=(%s) AND UI=(%s)",(aid,uid))
        data = c.fetchone()
        if data:
            c.execute("DELETE FROM GRE WHERE AppID=(%s) AND UI=(%s)",(aid,uid))
            mydb.commit()
        
        c.execute("INSERT INTO GRE (AppID,UI,GREScore,Verbal,Quantitative,GREAdvScore,GREAdvSbj,TOEFL,TOEFLDate,examYear) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                aid,
                uid,
                gretotal,
                greverbal,
                grequantitative,
                greascore,
                greasubject,
                toefl,
                toefldate,
                greyear
            ))
        mydb.commit()
        t = True
        c.execute(
              "UPDATE ApplicationChecklist SET GREIncluded=(%s) WHERE IDapp = (%s)", (
                  t,aid
              ))
        c.execute(
              "UPDATE Applications SET GREInclude=(%s) WHERE applicationID = (%s)", (
                  gretotal,aid
              ))
        c.execute("SELECT * FROM GRE WHERE AppID=(%s) AND UI=(%s)",(aid,uid))
        data = c.fetchone()
        
        
        mydb.commit()  
        if data:
            return redirect(url_for("applicant"))

        else:
              # Else, give an error message and redirect them to the same login page
              error = 'ERROR: please fill out all forms'


    return render_template('gre.html',error=error,aid=aid,uid=uid)

@app.route('/applications/new/doctoral/',methods=['GET','POST'])    
def doctoralApp():
    
    # mydb = get_mysql_connection()
    
    if 'utype' not in session or session['utype'] != 'Applicant':
        return redirect('/')

    error = None
    # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables!
    if request.method == 'GET':
        # connection = sqlite3.connect('myDatabase.db')
        # connection.row_factory = sqlite3.Row
        # c = connection.cursor()

        return render_template('doctoral.html',error=error)

    if request.method == 'POST':
        c =  mydb.cursor(dictionary=True)

        ref1fname = request.form["ref1fname"]
        ref1lname = request.form["ref1lname"]
        ref1email = request.form["ref1email"]
        ref1title = request.form["ref1title"]
        ref1aff = request.form["ref1aff"]

        ref2fname = request.form["ref2fname"]
        ref2lname = request.form["ref2lname"]
        ref2email = request.form["ref2email"]
        ref2title = request.form["ref2title"]
        ref2aff = request.form["ref2aff"]

        ref3fname = request.form["ref3fname"]
        ref3lname = request.form["ref3lname"]
        ref3email = request.form["ref3email"]
        ref3title = request.form["ref3title"]
        ref3aff = request.form["ref3aff"]

        gre = request.form["gre"]

        #info about GRE
        #max for verbal and quantitative is 170
        verbal = request.form["verbal"]
        quantitative = request.form["quantitative"]
        GREAdvScore = request.form["GREAdvScore"]
        GREAdvSbj = request.form["GREAdvSbj"]
        TOEFL = request.form["TOEFL"]
        TOEFLDate = request.form["TOEFLDate"]
        examYear = request.form["examYear"]
    
        #info about Prior Degree
        #masters
        #mDegree = request.form["mDegree"] 
        mGPA = request.form["mGPA"]
        mMajor = request.form["mMajor"]
        mPriorYear = request.form["mPriorYear"]
        mUni = request.form["mUni"]
        
        #bachelors
        #bDegree =request.form["bDegree"]
        bGPA = request.form["bGPA"]
        bMajor = request.form["bMajor"]
        bPriorYear = request.form["bPriorYear"]
        bUni = request.form["bUni"]
       

        priorWorkExperience = request.form["priorworkexperience"]
        interest = request.form["interest"]
        admissionyr = request.form["admissionyr"]
        admissionsem= request.form["admissionsem"]
        degreesought = 1 #means wants a phd
        GREInclude = True #need to make way to upload it. should be in form
        appid = generateAppID()
        userid = session["userID"]
        numPriorDegree = 2 #needs to be adjusted later
        sendTranscript = request.form["sendTranscript"]
        if(sendTranscript == "mail"):
            sendT = 0
        if(sendTranscript == "email"):
            sendT = 1
       
        if(sendT == '' or ref1fname == '' or ref1lname == '' or ref1email == '' or ref1title == '' or ref1aff == '' or ref2fname == '' or ref2lname == '' or ref2email == '' or ref2title == '' or ref2aff == '' or ref3fname == '' or ref3lname == '' or ref3email == '' or ref3title == ''or ref3aff == ''):
            error = "please fill out all forms."
            return render_template('doctoral.html', error=error)
        if(gre == '' or priorWorkExperience == '' or admissionyr == '' or admissionsem == '' or interest == '' or verbal == '' or quantitative == '' or examYear == '' or GREAdvScore == '' or GREAdvSbj == '' or 
        TOEFL == '' or TOEFLDate == ''  or mGPA == '' or mMajor == '' or mPriorYear == '' or mUni == ''  or bGPA == '' or bMajor == '' or bPriorYear == '' or bUni == '') :
            error = "please fill out all forms."
            return render_template('doctoral.html', error=error)
        
        
        
        c.execute("INSERT INTO Applications (applicationID,userIdent,degreeSought,NumPriorDegree,GREInclude,priorWorkExperience,interests,admissionSem,admissionYr, sendTranscript) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                appid,
                userid,
                degreesought,
                numPriorDegree,
                GREInclude,
                priorWorkExperience,
                interest,
                admissionsem,
                admissionyr,
                sendT
            ))
       
        c.execute("INSERT INTO ApplicationChecklist (IDapp,IDuser,GREIncluded,transcriptReceived, isReviewed, isReferenced,finaldecisionreceived,isCompleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ", (
                appid,
                userid,
                GREInclude,
                False,
                False,
                False,
                False,
                False
                
            ))

        c.execute("INSERT INTO referenceInfo (appID, referencer1fname, referencer1lname, referencer1email,  referencer1title, referencer1affil, referencer2fname,referencer2lname, referencer2email, referencer2title, referencer2affil, referencer3fname, referencer3lname, referencer3email, referencer3title, referencer3affil) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
            appid,
            ref1fname,
            ref1lname,
            ref1email,
            ref1title,
            ref1aff,
            ref2fname,
            ref2lname,
            ref2email,
            ref2title,
            ref2aff,
            ref3fname,
            ref3lname,
            ref3email,
            ref3title,
            ref3aff

        ))
       
        c.execute("INSERT INTO GRE (AppID, UI, GREScore, Verbal, Quantitative, GREAdvScore, GREAdvSbj, TOEFL, TOEFLDate, examYear) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (
            appid,
            userid,
            gre, #INT
            verbal, #INT
            quantitative, #INT
            GREAdvScore, #INT
            GREAdvSbj, #varchar
            TOEFL, #varchar
            TOEFLDate, #INT
            examYear #int
            )
        )
        
        c.execute("INSERT INTO PriorDegree(AID, DegreeType, GPA, Major, priorYear, University) VALUES (%s, %s, %s, %s, %s, %s)", (
            appid,
            "MS", #VARCHAR
            mGPA, #FLOAT
            mMajor, #text
            mPriorYear, #int
            mUni #text
        ))

        c.execute("INSERT INTO PriorDegree(AID, DegreeType, GPA, Major, priorYear, University) VALUES (%s, %s, %s, %s, %s, %s) ", (
            appid,
            "BS/BA",
            bGPA,
            bMajor,
            bPriorYear,
            bUni
        ))
        
        c.execute("INSERT INTO checkReference(idApp, reference1received, reference2received, reference3received) VALUES (%s, %s, %s, %s)", (
            appid,
            False,
            False,
            False
        ))

        c.execute(
              "SELECT * FROM Applications WHERE applicationID = (%s)", (
                  appid,
              ))
        data = c.fetchone()
        
        mydb.commit()  
        if data:
            return redirect(url_for("applicant"))

        else:
              # Else, give an error message and redirect them to the same login page
              error = 'ERROR: please fill out all forms'

    
    return render_template('doctoral.html',error=error)

@app.route('/applications/new/masters/',methods=['GET','POST'])    
def mastersApp():

    # mydb = get_mysql_connection()
    if 'userID' not in session or session['utype'] != 'Applicant':
        return redirect('/')


    error = None
    # If the username/password is correct, log them in and redirect them to the home page. Remember to set your session variables!
    if request.method == 'GET':
        # connection = sqlite3.connect('myDatabase.db')
        # connection.row_factory = sqlite3.Row
        # c = connection.cursor()

        return render_template('masters.html',error=error)

    if request.method == 'POST':

        c =  mydb.cursor(dictionary=True)

        ref1fname = request.form["ref1fname"]
        ref1lname = request.form["ref1lname"]
        ref1email = request.form["ref1email"]
        ref1title = request.form["ref1title"]
        ref1aff = request.form["ref1aff"]

        ref2fname = request.form["ref2fname"]
        ref2lname = request.form["ref2lname"]
        ref2email = request.form["ref2email"]
        ref2title = request.form["ref2title"]
        ref2aff = request.form["ref2aff"]

        ref3fname = request.form["ref3fname"]
        ref3lname = request.form["ref3lname"]
        ref3email = request.form["ref3email"]
        ref3title = request.form["ref3title"]
        ref3aff = request.form["ref3aff"]

        gre = request.form.get('gre')
        if gre:
            print("GRE included")
            GREInclude = True
        else:
            print("GRE not included")
            GREInclude = False

        #info about GRE
        #max for verbal and quantitative is 170
        verbal = request.form["verbal"]
        quantitative = request.form["quantitative"]
        GREAdvScore = request.form["GREAdvScore"]
        GREAdvSbj = request.form["GREAdvSbj"]
        TOEFL = request.form["TOEFL"]
        TOEFLDate = request.form["TOEFLDate"]
        examYear = request.form["examYear"]

        #bachelors
        #bDegree =request.form["bDegree"]
        bGPA = request.form["bGPA"]
        bMajor = request.form["bMajor"]
        bPriorYear = request.form["bPriorYear"]
        bUni = request.form["bUni"]

        priorWorkExperience = request.form["priorworkexperience"]
        interest = request.form["interest"]
        admissionyr = request.form["admissionyr"]
        admissionsem= request.form["admissionsem"]
        degreesought = 0 #means wants a masters
        
        appid = generateAppID()
        # GREInclude = False #need to make way to upload it. should be in form

        userid = session["userID"]
        numPriorDegree = 1 #needs to be adjusted later
        sendTranscript = request.form["sendTranscript"]
        if(sendTranscript == "mail"):
            sendT = 0
        if(sendTranscript == "email"):
            sendT = 1


        if(sendT == '' or ref1title == '' or ref1aff == '' or ref2title == '' or ref2aff == '' or ref3title == '' or ref3aff == '' ):
            error = "please fill out all required forms."
            return render_template('masters.html', error=error)
        if(ref1fname == '' or ref1lname == '' or ref1email == '' or ref2fname == '' or ref2lname == '' or ref2email == ''
        or ref3fname == '' or ref3lname == '' or ref3email == '' or priorWorkExperience == '' or admissionyr == '' or admissionsem == '' or interest == '' or  
        bGPA == '' or bMajor == '' or bPriorYear == '' or bUni == '') :
          error = "please fill out all required forms."
          return render_template('masters.html', error=error)
       

        c.execute("INSERT INTO Applications (applicationID,userIdent,degreeSought,NumPriorDegree,GREInclude,priorWorkExperience,interests,admissionSem,admissionYr,sendTranscript) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ", (
                appid,
                userid,
                degreesought,
                numPriorDegree,
                GREInclude,
                priorWorkExperience,
                interest,
                admissionsem,
                admissionyr,
                sendT
            ))
    
        c.execute("INSERT INTO ApplicationChecklist (IDapp,IDuser,GREIncluded,transcriptReceived, isReviewed, isReferenced, finaldecisionreceived,isCompleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ", (
                appid,
                userid,
                GREInclude,
                False,
                False,
                False,
                False,
                False
        ))

        c.execute("INSERT INTO referenceInfo (appID, referencer1fname, referencer1lname, referencer1email, referencer1title, referencer1affil, referencer2fname,referencer2lname, referencer2email, referencer2title, referencer2affil, referencer3fname, referencer3lname, referencer3email, referencer3title, referencer3affil) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
            appid,
            ref1fname,
            ref1lname,
            ref1email,
            ref1title,
            ref1aff,
            ref2fname,
            ref2lname,
            ref2email,
            ref2title,
            ref2aff,
            ref3fname,
            ref3lname,
            ref3email,
            ref3title,
            ref3aff

        ))

        if gre:
            c.execute("INSERT INTO GRE (AppID, UI, GREScore, Verbal, Quantitative, GREAdvScore, GREAdvSbj, TOEFL, TOEFLDate, examYear) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (
            appid,
            userid,
            gre, #INT
            verbal, #INT
            quantitative, #INT
            GREAdvScore, #INT
            GREAdvSbj, #varchar
            TOEFL, #varchar
            TOEFLDate, #INT
            examYear #int
            )
            )
        
        c.execute("INSERT INTO PriorDegree(AID, DegreeType, GPA, Major, priorYear, University) VALUES (%s, %s, %s, %s, %s, %s) ", (
            appid,
            "BS/BA",
            bGPA,
            bMajor,
            bPriorYear,
            bUni
        ))

        c.execute("INSERT INTO checkReference(idApp, reference1received, reference2received, reference3received) VALUES (%s, %s, %s, %s)", (
            appid,
            False,
            False,
            False
        ))

        c.execute(
              "SELECT * FROM Applications WHERE applicationID = (%s)", (
                  appid,
              ))
        data = c.fetchone()
      


        mydb.commit()  
        if data:
            #application added
            return redirect(url_for("applicant"))
           
        else:
              # Else, give an error message and redirect them to the same login page
              error = 'ERROR: please fill out all forms'


    return render_template('masters.html',error=error)


@app.route('/applicant/emailTranscript/<appID>',methods=['GET','POST'])    
def emailTranscript(appID):
    if 'userID' not in session or session['utype'] != 'Applicant':
        return redirect('/')
    print("after checking session")

    cursor = mydb.cursor(dictionary= True)
    cursor.execute("SELECT * FROM Applications WHERE sendTranscript=1 AND applicationID = (%s)", (appID,))
    email = cursor.fetchall()
    print(email)
    if email:
        cursor.execute("UPDATE ApplicationChecklist SET transcriptReceived = 1 WHERE IDapp = (%s)", (appID,))
        mydb.commit()
        return redirect(url_for("applicant"))
    return redirect(url_for("applicant"))


@app.route('/AssignGrades', methods = ["GET", "POST"])
def assign_grades():

    if ("utype" not in session):
        return "no type"
    
    if(session['utype'] not in {"Faculty", "GS", "ADMIN"}):
        return "RESTRICTED ACCESS"

    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # )
    cursor = mydb.cursor()

    if (request.method == "POST"):
        fgrade = request.form.get("fgrade")
        cid = request.form["cid"]
        userID = request.form.get("userID")

        cursor.execute("UPDATE c_history SET fgrade = %s WHERE cid = %s AND userID = %s", (fgrade, cid, userID))
        mydb.commit()
        print(fgrade)
        print(cid)
        print(userID)


        if (session['utype'] in {"ADMIN"}):
            return render_template("sysadmin.html")
        
        if (session['utype'] in {"GS"}):
            return render_template("gsPage.html")
        
        
        return redirect(url_for('assign_grades'))
     # get all the courses in PROGR, so you can assign grades. 
    cursor.execute("SELECT * FROM c_history JOIN users ON c_history.userID = users.UserID WHERE c_history.instructor_ID = %s AND c_history.fgrade = %s", (session['userID'],"IN PROGR"))
    courses = cursor.fetchall()

    cursor.execute("SELECT * FROM c_history")
    allCourses = cursor.fetchall()

    return render_template("assign.html", courses = courses, allCourses = allCourses)

@app.route('/c_catalogue', methods=['GET', 'POST'])
def c_catalogue():
    if 'utype' not in session:
        return redirect(url_for('home'))
    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # )   
    cur = mydb.cursor()
    if request.method == 'POST':
        cid =request.form['cid']
        cur.execute("SELECT c_schedule.cDay,c_schedule.cTime, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.fName, users.lName FROM c_schedule JOIN c_catalogue ON c_schedule.cid=c_catalogue.cid JOIN users ON c_catalogue.instructorID = users.UserID WHERE c_catalogue.cid LIKE %s ORDER BY c_schedule.cid",('%'+cid+'%',))
        catalogue_init = cur.fetchall()
        search = 1
    else:
        cur.execute("SELECT c_schedule.cDay,c_schedule.cTime, c_schedule.cid,c_catalogue.dept,c_catalogue.cnum,c_catalogue.title, c_catalogue.cred, c_catalogue.prone, c_catalogue.prtwo,users.fName, users.lName FROM c_schedule JOIN c_catalogue ON c_schedule.cid=c_catalogue.cid LEFT JOIN users ON c_catalogue.instructorID = users.UserID ORDER BY c_schedule.cid")
        catalogue_init = cur.fetchall()
        search = 0

    catalogue = {}
    cnt = 0
    for course in catalogue_init:
        catalogue[cnt] = {'cDay' : course[0], 'cTime' : course[1], 'cid' : course[2],'dept' : course[3], 'cnum' : course[4], 'title' : course[5], 'cred' : course[6], 'prone' : course[7], 'prtwo' : course[8], 'ins_name' : course[9]+" "+course[10]}
        cnt=cnt+1
    return render_template('c_catalogue.html',catalogue=catalogue,search=search)

@app.route('/register/<cid>', methods = ['GET','POST'])
def register (cid):
    if 'userID' not in session:
        return redirect(url_for('home'))
    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # )   
    cur = mydb.cursor()
    
    cur.execute("SELECT IsApproved FROM Form1 WHERE UserID = %s", (session['userID'],))
    form1_approval = cur.fetchone()

    if form1_approval is None or not form1_approval[0]:
        return render_template('register.html', err_msg="Form1 not approved. Unable to register.")
    
    cur.execute ("SELECT * FROM c_history WHERE cid = %s and userID = %s",(cid,session['userID']))
    prev = cur.fetchone()
    if prev != None:
        return render_template ('register.html',err_msg = "Already taken the course")
    cur.execute("SELECT c_schedule.cid, c_schedule.cTime, c_schedule.cDay, c_catalogue.sem, c_catalogue.cataYear, c_catalogue.instructorID,c_catalogue.prone, c_catalogue.prtwo FROM c_schedule JOIN c_catalogue ON c_schedule.cid= c_catalogue.cid WHERE c_schedule.cid = %s",(cid,))
    course_time = cur.fetchone()
    if course_time[6] != None:
        dept_pr1 = course_time[6][0:4]
        cnum_pr1 = int(course_time[6][5:9])
        cur.execute("SELECT c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.userID = %s AND c_catalogue.dept = %s AND c_catalogue.cnum = %s",(session['userID'],dept_pr1,cnum_pr1))
        pr1 = cur.fetchone()
        if pr1 == None:
            return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[6])
        if pr1[0] == "IP":
            return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[6])
        if course_time[7] != None:
            dept_pr2 = course_time[7][0:4]
            cnum_pr2 = int(course_time[7][5:9])
            cur.execute("SELECT c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.userID = %s AND c_catalogue.dept = %s AND c_catalogue.cnum = %s",(session['userID'],dept_pr2,cnum_pr2))
            pr2 = cur.fetchone()
            if pr2 == None:
                return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[7])
            if pr2[0] == "IN PROGR":
                return render_template ('register.html',err_msg = "Prerequest needed: "+ course_time[7])
        
    st_h = course_time[1][0:2]
    st_min = course_time[1][2:4]
    print(st_h + ":" + st_min)
    st_final = 60 * int(st_h)+int(st_min)
    print(st_final)
    ed_h= course_time[1][5:7]
    ed_min = course_time[1][7:9]
    print(ed_h + ":" + ed_min)
    ed_final = 60 * int(ed_h)+int(ed_min)
    print(ed_final)
    cur.execute("SELECT c_history.cid, c_schedule.cTime, c_schedule.cDay FROM c_history JOIN c_schedule ON c_history.cid = c_schedule.cid WHERE c_history.userID = %s AND c_history.fgrade = %s",(session['userID'],"IN PROGR"))
    student_schedule = cur.fetchall()
    if student_schedule == None :
        cur.execute ("INSERT INTO c_history (userID, cid, fgrade,sem, year, instructor_ID) VALUES (%s,%s,%s,%s,%s,%s)",(session['userID'],course_time[0],"IN PROGR",course_time[3],course_time[4],course_time[5]))
        mydb.commit()
    for c_registered in student_schedule:
        r_st = 60* int (c_registered[1][0:2]) + int (c_registered[1][2:4])
        r_ed = 60* int (c_registered[1][5:7]) + int (c_registered[1][7:9])
        if c_registered[2]==course_time[2]:
            if ed_final+30 > r_st:
                #return render_template ('register.html',err_msg = "Unable to Register: Time Conflict")
                if r_ed + 30 > st_final:
                    return render_template ('register.html',err_msg = "Unable to Register: Time Conflict")
    cur.execute ("INSERT INTO c_history (userID, cid, fgrade,sem, prevYear, instructor_ID) VALUES (%s,%s,%s,%s,%s,%s)",(session['userID'],course_time[0],"IN PROGR",course_time[3],course_time[4],course_time[5]))
    mydb.commit()
    return render_template ('register.html',err_msg = "Register Success")

@app.route('/drop/<cid>', methods = ['GET','POST'])
def drop (cid):
    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # )   
    cur = mydb.cursor()
    cur.execute("DELETE FROM c_history WHERE userID = %s AND cid = %s",(session['userID'],cid))
    mydb.commit()
    return redirect (url_for('registered_course'))

@app.route('/c_registered', methods = ['GET','POST'])
def registered_course():
    print("forgrer")

    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # )   
    cur = mydb.cursor()
    cur.execute("SELECT c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_schedule.cDay, c_schedule.cTime, users.fName, users.lName FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid JOIN c_schedule ON c_history.cid = c_schedule.cid JOIN users ON c_history.instructor_ID = users.UserID WHERE c_history.userID = %s AND c_history.fgrade = %s",(session['userID'],"IN PROGR"))
    catalogue_init = cur.fetchall()

    if len(catalogue_init) == 0:
        return render_template ('c_registered.html',catalogue=None)  
    catalogue = {}
    cnt = 0
    for course in catalogue_init:
        catalogue[cnt] = {'cDay' : course[5], 'cTime' : course[6], 'cid' : course[0],'dept' : course[1], 'cnum' : course[2], 'title' : course[3], 'cred' : course[4], 'ins_name' : course[7]+" "+course[8]}
        cnt=cnt+1      
    print("cata:")
    print(catalogue)
    return render_template ('c_registered.html',catalogue=catalogue)  

@app.route('/transcript', methods = ['GET'])
def transcript():
    if 'utype' not in session:
        return redirect(url_for('login'))
    
    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # ) 

    cur = mydb.cursor()
    cur.execute("SELECT c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.userID = %s", (session['userID'],))
    transcript_data = cur.fetchall()

    transcript = {}
    count = 0
    for course in transcript_data:
        transcript[count] = {'cid' : course[0], 'dept' : course[1], 'cnum' : course[2], 'title' : course[3], 'cred' : course[4], 'fgrade' : course[5]}
        count += 1

    return render_template('transcript.html', transcript = transcript)

@app.route('/student_info')
def student_info():
    if 'userID' not in session:
        return redirect(url_for('home'))
    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    cursor = mydb.cursor()
    cursor.execute("SELECT fName, lName, primaryAddress, email, primaryphone, SSN, userType FROM users WHERE UserID = %s", (session['userID'],))
    student_data = cursor.fetchone()

    cursor.execute("SELECT p.program_name, p.program_major FROM Student s JOIN Program p ON s.program_id = p.programID WHERE s.studentID = %s", (session['userID'],))
    program_data = cursor.fetchone()

    if student_data:
        return render_template("student_info.html", fname=student_data[0], lname=student_data[1], primaryAddress=student_data[2], email=student_data[3], primaryphone=student_data[4], SSN=student_data[5], userType = student_data[6], program=f"{program_data[0]} {program_data[1]}" if program_data else "Not available")
    
@app.route('/update_address', methods = ['POST'])
def update_address():
    if 'userID' not in session:
        return redirect(url_for('home'))
    new_address = request.form.get('primaryAddress')
    # mydb = mysql.connector.connect(
    #     host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
    #     user="admin",
    #     password="Password11",
    #     database="university"
    # )
    cursor = mydb.cursor()
    cursor.execute("UPDATE users SET primaryAddress = %s WHERE UserID = %s", (new_address, session['userID']))
    mydb.commit()
    if (session['utype'] == "Student" or session['utype'] == "Applicant") :
        return redirect(url_for("student_info"))
    
    elif (session['utype'] == "Alumni") :
        return redirect(url_for("alumni_info"))
        
    else:
        return redirect(url_for("staff_info"))


@app.route('/transcriptSearch', methods=["POST"])
def transcriptSearch():
    if ("utype" not in session or session['utype'] not in {"Faculty", "GS", "ADMIN"}):
        return "RESTRICTED ACCESS"

    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    uid = request.form.get("userID")
    lname = request.form.get("lname")

    if not uid and not lname:
        return render_template('transcriptSearch.html', transcripts={}, uid=uid, lname=lname)

    cur = mydb.cursor()
    if uid:
        cur.execute(
            "SELECT c_history.userID, c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid WHERE c_history.userID = %s", (uid,))
    elif lname:
        cur.execute(
            "SELECT c_history.userID, c_history.cid, c_catalogue.dept, c_catalogue.cnum, c_catalogue.title, c_catalogue.cred, c_history.fgrade FROM c_history JOIN c_catalogue ON c_history.cid = c_catalogue.cid JOIN users ON c_history.userID = users.UserID WHERE users.lname = %s", (lname,))
    transcript_data = cur.fetchall()

    transcripts = {}
    for course in transcript_data:
        user_id = course[0]
        if user_id not in transcripts:
            transcripts[user_id] = []
        transcripts[user_id].append({'cid': course[1], 'dept': course[2], 'cnum': course[3],
                                     'title': course[4], 'cred': course[5], 'fgrade': course[6]})

    return render_template('transcriptSearch.html', transcripts=transcripts, uid=uid, lname=lname)

def generate_random_user_id(length):
    return ''.join(random.choice('0123456789') for _ in range(length))

@app.route('/createUser', methods=["GET", "POST"])
def createUser():
    if ("utype" not in session or session['utype'] not in {"ADMIN"}):
        return "RESTRICTED ACCESS"

    # mydb = get_mysql_connection()
    cur = mydb.cursor()
    
    if request.method ==  'POST':
        passw = request.form['passw']
        fName = request.form['fName']
        lName = request.form['lName']
        SSN = request.form['SSN']
        email = request.form['email']
        primaryphone = request.form['primaryphone']
        primaryAddress = request.form['primaryAddress']
        type = request.form['type']

        while True:
            userID = generate_random_user_id(8)
            cur.execute("SELECT * FROM users WHERE UserID = %s", (userID,))
            if not cur.fetchone():
                break

        error_signup = "Please fill in the missing fields!"

        if not passw:
            return render_template("createUser.html", error_signup = error_signup)

        if not fName:
            return render_template("createUser.html", error_signup = error_signup)

        if not lName:
            return render_template("createUser.html", error_signup = error_signup)

        if not primaryAddress:
            return render_template("createUser.html", error_signup = error_signup)

        if not SSN:
            return render_template("createUser.html", error_signup = error_signup)

        cur.execute("INSERT INTO users (UserID, fname, lname, email, passw, primaryphone, primaryAddress, usertype, SSN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (userID, fName, lName, email, passw, primaryphone, primaryAddress, type, SSN))

        mydb.commit()
        cur.close()
        mydb.close()
        return render_template("createUser.html",userID = userID)

    return render_template("createUser.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():

    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )    
    cur = mydb.cursor()
    
    if request.method ==  'POST':
        passw = request.form['passw']
        fName = request.form['fName']
        lName = request.form['lName']
        SSN = request.form['SSN']
        email = request.form['email']
        primaryphone = request.form['primaryphone']
        primaryAddress = request.form['primaryAddress']
        type = "Applicant"

        while True:
            userID = generate_random_user_id(8)
            cur.execute("SELECT * FROM users WHERE UserID = %s", (userID,))
            if not cur.fetchone():
                break

        error_signup = "Please fill in the missing fields!"

        if not fName:
            return render_template("signup.html", error_signup = error_signup)

        if not lName:
            return render_template("signup.html", error_signup = error_signup)

        if not passw:
            return render_template("signup.html", error_signup = error_signup)
        
        if not primaryAddress:
            return render_template("signup.html", error_signup = error_signup)

        if not email:
            return render_template("signup.html", error_signup = error_signup)

        if not primaryphone:
            return render_template("signup.html", error_signup = error_signup)
        
        if not SSN:
            return render_template("signup.html", error_signup = error_signup)

        cur.execute("INSERT INTO users (UserID, fname, lname, email, passw, primaryphone, primaryAddress, usertype, SSN) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (userID, fName, lName, email, passw, primaryphone, primaryAddress, type, SSN))

        mydb.commit()
        cur.close()
        mydb.close()
        return render_template("signup.html",userID = userID)
    return render_template("signup.html")


@app.route('/email_update', methods = ['POST'])
def email_update():
    if 'userID' not in session:
        return redirect(url_for('home'))
    new_email = request.form.get('email')
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    cursor = mydb.cursor()
    cursor.execute("UPDATE users SET email = %s WHERE UserID = %s", (new_email, session['userID']))
    mydb.commit()
    if (session['utype'] == "Student" or session['utype'] == "Applicant") :
        return redirect(url_for("student_info"))
    
    elif (session['utype'] == "Alumni") :
        return redirect(url_for("alumni_info"))
    
    else:
        return redirect(url_for("staff_info"))


@app.route('/phone_update', methods=['POST'])
def phone_update():
    if 'userID' not in session:
        return redirect(url_for('home'))
    new_phone = request.form.get('primaryphone')
    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    cursor = mydb.cursor()
    cursor.execute("UPDATE users SET primaryphone = %s WHERE UserID = %s", (new_phone, session['userID']))
    mydb.commit()
    if (session['utype'] == "Student" or session['utype'] == "Applicant") :
        return redirect(url_for("student_info"))
    
    elif (session['utype'] == "Alumni") :
        return redirect(url_for("alumni_info"))
    
    else:
        return redirect(url_for("staff_info"))


@app.route('/openDecision', methods=["GET","POST"])
def openDecision():
    if 'userID' not in session:
        return redirect(url_for('home'))

    cursor = mydb.cursor()
    userid = session["userID"]
    cursor.execute("SELECT * FROM ApplicationChecklist JOIN DecisionInfo ON ApplicationChecklist.IDapp = DecisionInfo.ApplicationI WHERE finalDecision = 1 AND transcriptReceived = 1 AND isReviewed = 1 AND isReferenced = 1 AND finaldecisionreceived=1 AND isCompleted =1 AND IDuser = (%s)", (userid,))
    accept = cursor.fetchall()

    cursor.execute("SELECT * FROM ApplicationChecklist JOIN DecisionInfo ON ApplicationChecklist.IDapp = DecisionInfo.ApplicationI WHERE finalDecision = 0 AND transcriptReceived = 1 AND isReviewed = 1 AND isReferenced = 1 AND finaldecisionreceived=1 AND isCompleted=1 AND IDuser = (%s)", (userid,))
    reject = cursor.fetchall()

    yay = ""
    nay = ""

    if accept:
        yay = "CONGRATULATIONS! YOU HAVE BEEN OFFERED AN ADMISSION"
        return render_template("openDecision.html", yay = yay)

    if reject:
        nay = "We regret to inform you that unfortunately we do not have an offer for you at this time"
        return render_template("openDecision.html",  nay = nay)
    
    return render_template("openDecision.html", yay = yay, nay = nay)

@app.route('/staff_info')
def staff_info():
    if 'userID' not in session:
        return redirect(url_for('home'))
    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    cursor = mydb.cursor()
    cursor.execute("SELECT fName, lName, primaryAddress, email, primaryphone, SSN, userType FROM users WHERE UserID = %s", (session['userID'],))
    staff_data = cursor.fetchone()


    if staff_data:
        return render_template("staff_info.html", fname=staff_data[0], lname=staff_data[1], primaryAddress=staff_data[2], email=staff_data[3], primaryphone=staff_data[4], SSN=staff_data[5], userType = staff_data[6])


@app.route('/openDecision/accept',methods=['GET','POST'])    
def accept():
    print("got here")
    if 'userID' not in session or session['utype'] != 'Applicant':
        return redirect('/')

    userid = session["userID"]
    cursor = mydb.cursor(dictionary= True)
    cursor.execute("SELECT * FROM ApplicationChecklist JOIN DecisionInfo ON ApplicationChecklist.IDapp = DecisionInfo.ApplicationI WHERE finalDecision = 1 AND transcriptReceived = 1 AND isReviewed = 1 AND isReferenced = 1 AND finaldecisionreceived=1 AND isCompleted =1 AND IDuser = (%s)", (userid,))
    acceptOffer = cursor.fetchall()
    print(acceptOffer)
    if acceptOffer:
        cursor.execute("INSERT INTO matChecklist(idUser, acceptance, payFee) VALUES (%s, true, true)", (userid,))
        cursor.execute("UPDATE users SET userType = 'Student' WHERE UserID = (%s)", (userid,))
        mydb.commit()
        return redirect(url_for("login"))
    return redirect(url_for("index"))

@app.route('/applicant_info')
def applicant_info():
    if 'userID' not in session or session['utype'] != "Applicant":
        return redirect(url_for('home'))

    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    cursor = mydb.cursor()
    cursor.execute("SELECT fName, lName, primaryAddress, email, primaryphone, SSN, userType FROM users WHERE UserID = %s", (session['userID'],))
    applicant_data = cursor.fetchone()


    if applicant_data:
        return render_template("applicant_info.html", fname=applicant_data[0], lname=applicant_data[1], primaryAddress=applicant_data[2], email=applicant_data[3], primaryphone=applicant_data[4], SSN=applicant_data[5], userType = applicant_data[6])

@app.route('/applicant_update_address', methods = ['POST'])
def applicant_update_address():
    if 'userID' not in session:
        return redirect(url_for('home'))
    new_address = request.form.get('primaryAddress')
    cursor = mydb.cursor()
    cursor.execute("UPDATE users SET primaryAddress = %s WHERE UserID = %s", (new_address, session['userID']))
    mydb.commit()
    return redirect(url_for('applicant_info'))

@app.route('/applicant_email_update', methods = ['POST'])
def applicant_email_update():
    if 'userID' not in session:
        return redirect(url_for('home'))
    new_email = request.form.get('email')
    mydb = mysql.connector.connect(
        host = "group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    cursor = mydb.cursor()
    cursor.execute("UPDATE users SET email = %s WHERE UserID = %s", (new_email, session['userID']))
    mydb.commit()
    return redirect(url_for('applicant_info'))

@app.route('/applicant_phone_update', methods=['POST'])
def applicant_phone_update():
    if 'userID' not in session:
        return redirect(url_for('home'))
    new_phone = request.form.get('primaryphone')
    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )
    cursor = mydb.cursor()
    cursor.execute("UPDATE users SET primaryphone = %s WHERE UserID = %s", (new_phone, session['userID']))
    mydb.commit()
    return redirect(url_for('applicant_info'))

@app.route('/alumni_info')
def alumni_info():
    if 'userID' not in session:
        return redirect(url_for('home'))
    mydb = mysql.connector.connect(
        host="group-11.ci6j3qzwmmr9.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Password11",
        database="university"
    )

    cursor = mydb.cursor()
    cursor.execute("SELECT fName, lName, primaryAddress, email, primaryphone, SSN, userType FROM users WHERE UserID = %s", (session['userID'],))
    staff_data = cursor.fetchone()


    if staff_data:
        return render_template("alumni_info.html", fname=staff_data[0], lname=staff_data[1], primaryAddress=staff_data[2], email=staff_data[3], primaryphone=staff_data[4], SSN=staff_data[5], userType = staff_data[6])
    
app.run(host = '0.0.0.0', port = 8080)

