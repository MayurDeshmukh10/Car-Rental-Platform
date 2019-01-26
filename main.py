from flask import Flask, render_template, redirect, url_for , flash
import MySQLdb		#Mysql connector
import base64
from flask_weasyprint import HTML,render_pdf   #for generating invoice
import re	#for regular expression
from flask_mail import Mail,Message	#for sending mail to customers
from Crypto.Cipher import AES            #for encrypting password recovery answer of customers
from passlib.hash import pbkdf2_sha256    #for hashing password of customers
from flask import request
import datetime
import time
import os

app = Flask(__name__)



app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'abc@gmail.com', #Enter your emailid along with enable "recieve mails from unprotected services' in your gmail account
	MAIL_PASSWORD = '*****'    #enter your password
	)

#app.config.update(mail_settings)
mail = Mail(app)

app.secret_key = 'my unobvious secret key'

conn = MySQLdb.connect(host='localhost',user='yourusername',passwd = '******',port = 8090,db="car_rental") #enter Database username and password of mysql here
cursor = conn.cursor()
master_password = "REAPER"  #just master password for a session
custid = ""
driverID = 0
CARID = ""
payment_type = ""
payment_status = ["Paid","Not Paid"]
b_actual_id = 0

def checkstring(inputstring):
	F = 0;
	length = len(inputstring)
	for a in range(0,length):
		if (inputstring[a] >= 'a' and inputstring[a] <= 'z') or (inputstring[a] >= 'A' and inputstring[a] <= 'Z'):
			F = 1
		else:
			F = 0
	if F == 1:
		return False
	else:
		return True
	
	#return any(char.isdigit() for char in inputstring)
	
#-----------------------------------------------FRONT PAGE -------------------------------------------------------
@app.route("/",methods=['GET','POST'])

def homepage():
	print("ENTERED")
	return render_template("index.html")
#---------------------------ADD New CUSTOMER ----------------------------------------------------------------------------

@app.route('/addcustomer/',methods = ['GET','POST'])

def register():
	
	print("entered")
	#adduser()
	return render_template('addcustomer.html')
	

@app.route('/adduser/',methods = ['GET','POST'])

def adduser():
	print("entered")
	Username_to_string1 = ""
	flag = False
	cursor = conn.cursor()
	secret_key = '1234567890123456'
	#security_questions["1","2"
	try:
		user_rating = ""
		current_day = ""
		current_month = ""
		current_year = "" 
		current = datetime.datetime.now()
		current_day = str(current.day)
		current_month = str(current.month)
		current_year = str(current.year)
		current_date3 = current_day + "-" + current_month + "-" + current_year
		#Username_to_string1 = ""
		fname = request.form["FName"]
		value1 = checkstring(fname)
		if value1 == True:
			flash("Please enter a Valid First Name !!!")
			return render_template("addcustomer.html")
		
		lname = request.form["lName"]
		value2 = checkstring(lname)
		if value2 == True:
			flash("Please enter a Valid Last Name !!!")
			return render_template("addcustomer.html")
		username= request.form["username"]
		cursor.execute("""SELECT userId FROM Cust_User """)
		actual_usernames1 = cursor.fetchall()
		list1 = list(actual_usernames1)
		Username_to_string1 = str(username)
		length = len(list1)
		for a in range(0,length):
			print(actual_usernames1[a])
			print(Username_to_string1)
			if actual_usernames1[a][0] == Username_to_string1:
				print(actual_usernames1[a])
				print(Username_to_string1)
				flag = True
		print(Username_to_string1)
		print(list1)
	#	user_present1 = Username_to_string1 not in actual_usernames1
		print(flag)
		if flag == True:
			flash("Sorry Username is Already Present !!!")
			return render_template("addcustomer.html")
		else:
			
			email = request.form["email"]
			if re.search('@',email):
				em = 0
			else:
				flash("Please Enter Valid Email  !!!")
				return render_template("addcustomer.html")	
			phone = request.form["PhoneNumber"]
			plen = len(phone)
			if plen != 10:
				flash("Please Enter 10 Digit Phone Number only !!!")
				return render_template("addcustomer.html")
			age = request.form["age"]
			int_age = int(age)
			if int_age < 17 :
				flash("Sorry you must above 15 years of age !!!")
				return render_template("addcustomer.html")
			
				
			password = request.form["Password"]
			
			cpassword = request.form["ConfirmPassword"]
			print("CHECKED")
			security_question = int(request.form["squestion"])
			security_ans = request.form["answer"]
				
			hash_password = pbkdf2_sha256.hash(password)					# Hashing + salting Password
			S_ans = security_ans.rjust(32)
			
			encrypted = AES.new(secret_key,AES.MODE_ECB)
			ansEncoded = base64.b64encode(encrypted.encrypt(S_ans))
			ansEncoded = ansEncoded.strip()
	#		obj = AES.new('This is a key123',AES.MODE_CFB,'This is an IV456')
	#		encrypted_SQans = obj.encrypt(security_ans)					#Encrypting security Question Answer
				
			print("Encrypted ans : ",ansEncoded)
			print(hash_password)
			#selection = request.form['selection']
			#answer = request.form['answer']
		
			msg=Message("Welcome to Car Rental Services",sender="Car Rentel Services",recipients=[email])
			msg.body = "Thank you for signing up for Car Rental Service, Now Book a Cab Now !!!"
			mail.send(msg)
			'''except Exception, e:
				return(str(e)) '''	
			print( fname,lname,password,username,cpassword,email,security_question,security_ans)
			cursor.execute("""INSERT INTO Cust_User(userId,fName,lName,emailId,phone,registration_Date,password,reset_Question,reset_Ans_Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(username,fname,lname,email,phone,current_date3,hash_password,security_question,ansEncoded)) 
				
					
			#cursor.execute("select * from login")
			#data = cursor.fetchall()
				
				
			conn.commit()    
			cursor.close()   
			print ("Registered")
				
			flash("Successfully Registered !!! ")
			return redirect('/login')
	except Exception as e:
		return(str(e))
			
			
			
#---------------------------------------END------------------------------------------------------

#-------------------------------------LOGIN PAGE--------------------------------------------------------
@app.route('/login')

def signin():
	print("entered")
	return render_template('signin.html')
	
	
@app.route('/echo',methods=['POST'])

def sign():
	Cinflag = False
	Ainflag = False
	admin_password_match = False
	cust_password_match = False
	A = "Admin"
	C = "Customer"
	user_rating = ""
	current_day = ""
	current_month = ""
	current_year = "" 
	current = datetime.datetime.now()
	current_day = str(current.day)
	current_month = str(current.month)
	current_year = str(current.year)
	current_date4 = current_day + "-" + current_month + "-" + current_year
	print("entered")
	cursor = conn.cursor()
	Username_to_string = ""
	Username = request.form['Username']
	Password = request.form['Password']
	cursor.execute("""SELECT userId FROM Cust_User """)
	cust_actual_usernames = cursor.fetchall()
	cust_actual_usernames_list = list(cust_actual_usernames)
	cust_length = len(cust_actual_usernames_list)
	Username_to_string1 = Username
	print(cust_actual_usernames)
	for a in range(0,cust_length):
		if cust_actual_usernames_list[a][0] == Username_to_string1:
			Cinflag = True
	
	#user_present = Username_to_string in actual_usernames
	
	cursor.execute("""SELECT userId FROM Admin_User """)
	admin_actual_usernames = cursor.fetchall()
	admin_actual_usernames_list = list(admin_actual_usernames)
	admin_length = len(admin_actual_usernames_list)
	Username_to_string2 = Username
	print(admin_actual_usernames)
	for a in range(0,admin_length):
		if admin_actual_usernames_list[a][0] == Username_to_string2:
			Ainflag = True
			
	if Cinflag == True:
		print("CUSTUser is present")
		cursor.execute("""SELECT password FROM Cust_User WHERE userId =%s""",[Username])
		cust_actual_password = cursor.fetchone()
		cust_password_match = pbkdf2_sha256.verify(Password,cust_actual_password[0])
	elif Ainflag == True:
		print("ADMINUser is present")
		cursor.execute("""SELECT password FROM Admin_User WHERE userId =%s""",[Username])
		admin_actual_password = cursor.fetchone()
		admin_password_match = pbkdf2_sha256.verify(Password,admin_actual_password[0]) 
	else:
		flash("Sorry Username Invalid !!!")
		return render_template("signin.html")
		
	
	
	
	
	
	#cursor.close()
	if cust_password_match == True:
		current_time = time.strftime("%X")
		cursor.execute("""INSERT INTO Login_History(user,userId,Date,Time) values(%s,%s,%s,%s)""",(C,Username,current_date4,current_time))
		conn.commit()
		global custid
		custid = Username[:]
		flash("Login Sucessfull, Now Book a Cab !!!")
		return render_template("booking.html")
		print("CUSTOMER TRUE")
	elif admin_password_match == True:
		current_time = time.strftime("%X")
		cursor.execute("""INSERT INTO Login_History(user,userId,Date,Time) values(%s,%s,%s,%s)""",(A,Username,current_date4,current_time))
		conn.commit()
		flash("Welcome Admin !!!")
		return redirect("/adminpage")
		print("ADMIN TRUE")
	else:
		flash("Password Incorrect")
		return render_template("signin.html")

#**********************************RESET PASSWORD-----------------------------------------------------------------------------------

@app.route('/resetpassword/',methods=['GET','POST'])

def resetdriver():
	print("Entered")
	return render_template("resetpassword.html")

@app.route('/reset/',methods=['GET','POST'])

def resetpasswordform():
	cursor = conn.cursor()
	secret_key = '1234567890123456'
	uflag = False
	aflag = False
	cqflag = False
	aqflag = False
	reset_username = request.form["username"]
	Lreset_username = str(reset_username)
	Squestion = int(request.form["squestion"])
	answer = request.form["answer"]
	newpassword = request.form["password"]
	
	print(reset_username,Squestion,answer,newpassword)
	
	cursor.execute("""SELECT userId FROM Cust_User""")
	usernames = cursor.fetchall()
	usernames_list = list(usernames)
	usernames_len = len(usernames_list)
	for a in range(0,usernames_len):
		if usernames_list[a][0] == Lreset_username:
			uflag = True
		
	cursor.execute("""SELECT userId FROM Admin_User""")
	usernames = cursor.fetchall()
	usernames_list = list(usernames)
	usernames_len = len(usernames_list)
	for a in range(0,usernames_len):
		if usernames_list[a][0] == Lreset_username:
			aflag = True
			
	if aflag == False and uflag == False:
		flash("Entered Username does not Exist !!!")
		return render_template("resetpassword.html")
			
	cursor.execute("""SELECT reset_Question FROM Cust_User""")
	Aquestions = cursor.fetchall()
	Aquestion_list = list(Aquestions)
	Aquestion_len = len(Aquestion_list)
	print("SQUESTION",Squestion)
	print("CUSTORMER")
	for a in range(0,Aquestion_len):
		print(Aquestion_list[a][0])
		if Aquestion_list[a][0] == Squestion:
			cqflag = True
	
	print("ADMIN")		
	cursor.execute("""SELECT reset_Question FROM Admin_User""")
	questions = cursor.fetchall()
	question_list = list(questions)
	question_len = len(question_list)
	for a in range(0,question_len):
		print(question_list[a][0])
		if question_list[a][0] == Squestion:
			aqflag = True
			

	"""if aqflag == False and cqflag == False:
		flash("Invalid security question Selected, Please select correct Security question !!!")
		return render_template("resetpassword.html")
	print("Question = ",aqflag)
	"""
	if uflag == True:
		cursor.execute("""SELECT reset_Ans_Type FROM Cust_User WHERE userId = %s""",[Lreset_username])
		O_ans = cursor.fetchone()
		Original_ans = O_ans[0]
		print("Original ans : ",Original_ans)
	
	if aflag == True:
		cursor.execute("""SELECT reset_Ans_Type FROM Admin_User WHERE userId = %s""",[Lreset_username])
		O_ans = cursor.fetchone()
		Original_ans = O_ans[0]
		print("Original ans : ",Original_ans)
		
	cipher = AES.new(secret_key,AES.MODE_ECB)
	decode1 = cipher.decrypt(base64.b64decode(Original_ans))
	decoded = decode1.strip()
	actual_ans = decoded.decode("utf-8")
	
	if actual_ans == answer:
		print("CHECK PASSORD : ",newpassword)
		hashednewpassword = pbkdf2_sha256.hash(newpassword)
		if uflag == True:
			cursor.execute("""UPDATE Cust_User SET password = %s WHERE userId = %s""",(hashednewpassword,Lreset_username))
		if aflag == True:
			cursor.execute("""UPDATE Admin_User SET password = %s WHERE userId = %s""",(hashednewpassword,Lreset_username))
		conn.commit()
		flash("Password Successfully Changed, Please Login Now !!!")
		return render_template("signin.html")
	else:
		flash("Entered Security Answer is Wrong !!!")
		return render_template("resetpassword.html")
	#print("DECODED Question " ,actual_ans)
	#resetp = cursor.fetchone()
	#old_password = resetp[0]
	#print("OLD PASSOWORD",old_password)
#--------------------------------------------BOOKING PAGE-----------------------------------------------------

@app.route('/booking/',methods = ['GET','POST'])
def bookingdriver():
	
	print("entered")
	#booking()
	return render_template('booking.html')
	
	
@app.route('/bookingNow/',methods = ['GET','POST'])


def booking():
	print("entered")
	cabs_list = ["Hatchback","Sedan","SUV"]
	buflag = False
	try:
		cab_route = ['Nashik-Pune','Nashik-Mumbai','Nashik-Nagpur','Nashik-Dhule','Nashik-Aurangabad']
		car_empty = False
		driver_empty = False
		userId=request.form["userId"]
		cursor.execute("""SELECT userId FROM Cust_User""")
		busernames = cursor.fetchall()
		busernames_list = list(busernames)
		busernames_len = len(busernames_list)
		for a in range(0,busernames_len):
			if busernames_list[a][0] == userId:
				buflag = True
		if buflag == False:
			flash("Entered Username does not Exist !!!")
			return render_template('booking.html')
		
		#userId = userId.encode(userId.originalEncoding)
		cursor.execute("""SELECT fName,lName,emailId,phone FROM Cust_User WHERE userId = %s""",[userId])
		custinfo = cursor.fetchall()
		custinfo_list = list(custinfo)
		print(custinfo_list)
		fname = custinfo_list[0][0]
		lname = custinfo_list[0][1]
		email = custinfo_list[0][2]
		phone = custinfo_list[0][3]
		print(fname,lname,email,phone)
		'''fname = request.form["fName"]
		print(fname)
		lname = request.form["lName"]
		phone = request.form["PhoneNumber"]
		email = request.form["email"]	'''
		cab1 = request.form["cab"]
		cab = int(cab1)
		print(userId,fname,lname,phone,email,cab)
		cab_name = ""
		route = ""
		cab_name = cabs_list[cab]
		startDate = request.form["startDate"]
		endDate = request.form["endDate"]
		time = request.form["time"]
		carroute = int(request.form["route"])
		route = cab_route[carroute]
		pickupLocation = request.form["pickupLocation"]
		dropoffLocation = request.form["dropoffLocation"]
		pricePerKm = 10;
		car_name = cabs_list[cab]
	
		print(userId,fname,lname,phone,email,cab,startDate,endDate,time,pickupLocation,dropoffLocation,route)
		
		cursor.execute("""SELECT Car_id FROM Car WHERE status = 'Available' and Car_type = %s """,[car_name])
		car = cursor.fetchall()
		if car:
			print('Structure is not empty.')
			car_empty = False
		else:
			print('Structure is empty.')
			return redirect('/allbooked')
			car_empty =  True
		print("CAR NAME ",car)
		carid = car[0][0]
		
		cursor.execute("""SELECT driverId FROM Driver WHERE status = 'Available' """)
		driver = cursor.fetchall()
		if driver:
			print('Structure is not empty.')
			car_empty = False
		else:
			print('Structure is empty.')
			return redirect('/allbooked')
			car_empty =  True
		driverid = driver[0][0]
		
		print("NULL CARID" ,carid)
		print("NULL driverid",driverid)
		cursor.execute("""UPDATE Car SET status = "BOOKED" WHERE Car_id = %s""",[carid])
		#print("DRIVER ID : ",driverid)
		global CARID
		CARID = carid[:]
		global driverID
		driverID = driverid
		
		cursor.execute("""UPDATE Driver SET status = "BOOKED" WHERE driverId = %s""",[driverid])
		print("DRIVER ID : ",driverid)
		cursor.execute("""INSERT INTO Booking(userId,Cab,startDate,endDate,Pickup_time,Pickup_location,Drop_off_location,driverId,carid,cab_route) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(userId,cab_name,startDate,endDate,time,pickupLocation,dropoffLocation,driverid,carid,route)) 
		
		conn.commit()
		global b_actual_id
		cursor.execute("""select bookingId from Booking where Pickup_time=%s and startDate=%s """,[time,startDate])
		b_id=cursor.fetchall()
		b_actual_id=b_id[0][0]
		print(b_actual_id)  
		print ("Booked")
		print ("Booked")
		
		return redirect("/payment")
		
	except Exception as e:
		return(str(e))
#--------------------------------------------------BOOKING PAGE ENDS------------------------------------------------------------------------------

#------------------------------------------------DISPLAY BOOKING ------------------------------------------------------------------

@app.route("/displaybooking/",methods=['GET','POST'])

def displaybooking():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Booking""")
	data5 = cursor.fetchall()
	cursor.close()
	
	return render_template("displaybooking.html",data = data5)
	
#--------------------------------------------DISPLAY BOOKING END--------------------------------------------------------------------
#--------------------------------------------ADMIN PAGE -------------------------------------------------------------
@app.route('/adminpage/',methods=['GET','POST'])

def adminpage():
	print("Entered") 	#Testing
	
	return render_template("adminpage.html")
#---------------------------------END ADMIN PAGE-----------------------------------------------

#----------------------------------LOGIN HISTORY----------------------------------------------
@app.route("/logindetails/",methods=['GET','POST'])

def logindetails():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Login_History""")
	data5 = cursor.fetchall()
	cursor.close()
	
	return render_template("loginhistory.html",data = data5)
#------------------------------------FEEDBACK FORM------------------------------------------------------------

@app.route('/feedback/',methods=['GET','POST'])

def feedbackdriver():
	print("Entered") 	#Testing
	
	return render_template("feedback.html")
	

@app.route('/addfeedback/',methods=['GET','POST'])

def feedbackform():
	cursor = conn.cursor()
	actual_ratings = ['Excellent','Good','Neutral','Poor']  #actual rating present in website
	user_rating = ""
	current_day = ""
	current_month = ""
	current_year = "" 
	current = datetime.datetime.now()
	current_day = str(current.day)
	current_month = str(current.month)
	current_year = str(current.year)
	current_date = current_day + "-" + current_month + "-" + current_year
	print("Date of today = ",current_date)
	print("Entered123")		#Testing
	rating = request.form["view"]
	int_rating = int(rating)           #Convert string into int
	comments = request.form["comments"]
	username = request.form["userid"]
	email = request.form["email"]

	cursor.execute("""SELECT fName,lName from Cust_User WHERE userId = %s""",[username])
	name = cursor.fetchall()
	fname = name[0][0]
	lname = name[0][1]
	print("FNAME : ",fname)
	print("LNAME : ",lname)
	"""cursor.execute(""SELECT username from login where email = %s"",[email])
	username1 = cursor.fetchall()
	username2  = username1[0]
	print("Username : ",username2) """
	print("intRATING:",int_rating)
	user_rating = actual_ratings[int_rating]	#selecting user rating
	
	print(user_rating,comments,name,email)
	cursor.execute("""INSERT INTO Feedback(userId,fName,lName,emailId,rating,comments,Date) values (%s,%s,%s,%s,%s,%s,%s)""",(username,fname,lname,email,user_rating,comments,current_date))
	#cursor.execute("""INSERT INTO Feedback(rating,comment,name,email,date) VALUES (%s,%s,%s,%s,%s)""",(user_rating,comments,name,email,current_date)) 
	
	conn.commit()
	flash("Feedback Successfully Send !!!")
	cursor.close()
	return render_template("feedback.html")
#---------------------------------------------------FEEDBACK FORM END-------------------------------------------------------------------
#-------------------------------------------------ADD ADMIN-------------------------------------------------------------------------------------
@app.route('/addadmin/',methods = ['GET','POST'])

def addadmindriver():
	
	print("entered")
	#adduser()
	return render_template('addadmin.html')
	

@app.route('/addADMIN/',methods = ['GET','POST'])

def addadmin():
	print("entered")
	Username_to_string1 = ""
	flag = False
	cursor = conn.cursor()
	secret_key = '1234567890123456'
	#security_questions["1","2"
	try:
		#Username_to_string1 = ""
		current_day = ""
		current_month = ""
		current_year = "" 
		current = datetime.datetime.now()
		current_day = str(current.day)
		current_month = str(current.month)
		current_year = str(current.year)
		current_date = current_day + "-" + current_month + "-" + current_year
		print("Date of today = ",current_date)
		fname = request.form["FName"]
		lname = request.form["lName"]
		username= request.form["username"]
		cursor.execute("""SELECT userId FROM Admin_User """)
		actual_usernames1 = cursor.fetchall()
		list1 = list(actual_usernames1)
		Username_to_string1 = str(username)
		length = len(list1)
		for a in range(0,length):
			print(actual_usernames1[a])
			print(Username_to_string1)
			if actual_usernames1[a][0] == Username_to_string1:
				print(actual_usernames1[a])
				print(Username_to_string1)
				flag = True
		print(Username_to_string1)
		print(list1)
	#	user_present1 = Username_to_string1 not in actual_usernames1
		print(flag)
		if flag == True:
			flash("Sorry Username is Already Present !!!")
			return render_template("addadmin.html")
		else:
			email = request.form["email"]	
			phone = request.form["PhoneNumber"]
			age = request.form["age"]
			int_age = int(age)
			if int_age < 15 :
				flash("Sorry you must above 15 years of age !!!")
				return render_template("addadmin.html")
				
			password = request.form["Password"]
			cpassword = request.form["ConfirmPassword"]
			security_question = int(request.form["squestion"])
			security_ans = request.form["answer"]
				
			hash_password = pbkdf2_sha256.hash(password)					# Hashing + salting Password
			S_ans = security_ans.rjust(32)
			
			encrypted = AES.new(secret_key,AES.MODE_ECB)
			ansEncoded = base64.b64encode(encrypted.encrypt(S_ans))
			ansEncoded = ansEncoded.strip()
	#		obj = AES.new('This is a key123',AES.MODE_CFB,'This is an IV456')
	#		encrypted_SQans = obj.encrypt(security_ans)					#Encrypting security Question Answer
				
			print("Encrypted ans : ",ansEncoded)
			print(hash_password)
			#selection = request.form['selection']
			#answer = request.form['answer']
				
			print( fname,lname,password,username,cpassword,email,security_question,security_ans)
			cursor.execute("""INSERT INTO Admin_User(userId,fName,lName,emailId,phone,registration_Date,password,reset_Question,reset_Ans_Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(username,fname,lname,email,phone,current_date,hash_password,security_question,ansEncoded)) 
					
			#cursor.execute("select * from login")
			#data = cursor.fetchall()
				
				
			conn.commit()    
			cursor.close()   
			print ("Registered")
				
			flash("Admin Successfully Registered !!! ")
			return render_template('addadmin.html')
	except Exception as e:
		return(str(e))
			

#-----------------------------------------------DISPLAY ADMIN DETAILS-------------------------------------------------------------------------------
@app.route("/admindetails/",methods=['GET','POST'])

def admindetails():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Admin_User""")
	data = cursor.fetchall()
	cursor.close()
	
	return render_template("admindetails.html",data = data)
#------------------------------------------------DISPLAY ADMIN ENDS--------------------------------------------------------------------------

#------------------------------------------------DELETE ADMIN---------------------------------------------------------------------------------------
@app.route("/deleteadmin/",methods=['GET','POST'])

def deleteadmindriver():
	return render_template("deleteadmin.html")	
	
@app.route("/deleteADMIN/",methods=['GET','POST'])

def deleteadmin():
	cursor = conn.cursor()
	mpassword = request.form["mpassword"]
	dusername = str(request.form["dusername"])
	husername = request.form["husername"]
	adflag = False
	cursor.execute("""SELECT userId FROM Admin_User""")
	usernamesad = cursor.fetchall()
	usernames_listad = list(usernamesad)
	usernames_lenad = len(usernames_listad)
	for a in range(0,usernames_lenad):
		if usernames_listad[a][0] == dusername:
			adflag = True
	if adflag == False:
		flash("Entered Username does not Exist !!!")
		return render_template("deleteadmin.html")
		
	if master_password == mpassword:
		cursor.execute("""DELETE FROM Admin_User WHERE userId = %s""",[dusername])
		conn.commit()
		print(mpassword,dusername,husername)
		flash("Admin Successfully Deleted !!!")
		return render_template("deleteadmin.html")
	else:
		flash("Incorrect Master Password !!!")
		return render_template("deleteadmin.html")
		
		
#------------------------------------------END DELETE ADMIN ----------------------------------------------------------------------
#----------------------------------------FEEDBACK DISPLAY-----------------------------------------------------------------------

@app.route("/feedbackdisplay/",methods=['GET','POST'])

def feedbackdisplay():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Feedback""")
	data1 = cursor.fetchall()
	cursor.close()
	
	return render_template("feedbackdisplay.html",data = data1)
	
#------------------------------------FEEDBACK DISPLAY END -------------------------------------------------------------------------------
#-----------------------------------Display Customer Details----------------------------
@app.route("/displaycustomer/",methods=['GET','POST'])

def displaycustomer():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Cust_User""")
	data1 = cursor.fetchall()
	cursor.close()
	
	return render_template("displaycustomers.html",data = data1)
#-------------------------------------DELETE CUSTOMER USER-----------------------------------------------------------------------------
@app.route("/deleteuser/",methods=['GET','POST'])

def deleteuserdriver():
	return render_template("deleteuser.html")	
	
@app.route("/deleteUSER/",methods=['GET','POST'])

def deleteuser():
	cursor = conn.cursor()
	dusername1 = str(request.form["dusername"])
	husername1 = request.form["husername"]
	
	udflag = False
	cursor.execute("""SELECT userId FROM Cust_User""")
	usernamesud = cursor.fetchall()
	usernames_listud = list(usernamesud)
	usernames_lenud = len(usernames_listud)
	for a in range(0,usernames_lenud):
		if usernames_listud[a][0] == dusername1:
			udflag = True
	if udflag == False:
		flash("Entered Username does not Exist !!!")
		return render_template("deleteuser.html")
		
	cursor.execute("""DELETE FROM Cust_User WHERE userId = %s""",[dusername1])
	conn.commit()
	#print(mpassword,dusername,husername)
	cursor.close()
	flash("Customer Successfully Deleted !!!")
	return render_template("deleteuser.html")
	
#------------------------------DELETE CUSTOMER ENDS --------------------------------------------------------------------------------

#----------------------------------ADD NEW CAR -----------------------------------------------------------------------------------------------

@app.route("/addcar/",methods=['GET','POST'])

def addcardriver():
	return render_template("addcar.html")

@app.route("/addCAR/",methods=['GET','POST'])

def addcarform():
	car_type = ['Sedan','Hatchback','SUV']
	Car_Type = ""
	cursor = conn.cursor()
	carid = str(request.form["carid"])
	model = request.form["model"]
	registration = request.form["registration"]
	seating = request.form["seating"]
	Type = int(request.form["type"])
	Car_Type = car_type[Type]
	price = int(request.form["price"])
	
	cursor.execute("""INSERT INTO Car(Car_id,model_name,registeration_no,seating_capacity,Car_type,price_per_km) VALUES (%s,%s,%s,%s,%s,%s)""",(carid,model,registration,seating,Car_Type,price)) 
	conn.commit()
	cursor.close()
	#print(mpassword,dusername,husername)
	flash("New Car Successfully Added !!!")
	return render_template("addcar.html")
	
#-----------------------------------ADD CAR ENDS---------------------------------------------------------------------------------

#------------------------------------------------DISPLAY CARS-----------------------------------------------------------------------------

@app.route("/displaycars/",methods=['GET','POST'])

def displaycars():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Car""")
	data2 = cursor.fetchall()
	cursor.close()
	
	return render_template("displaycars.html",data = data2)
#--------------------------------------------DISPLAY CAR ENDS-------------------------------------------------------------------------------

#---------------------------------------------DELETE CAR----------------------------------------------------------------------------------

@app.route("/deletecars/",methods=['GET','POST'])

def deletecardriver():
	return render_template("deletecars.html")	
	
@app.route("/deleteCARS/",methods=['GET','POST'])

def deletecar():
	cursor = conn.cursor()
	carid = str(request.form["carid"])
	
	cflag = False
	cursor.execute("""SELECT Car_id FROM Car""")
	carids = cursor.fetchall()
	carid_list = list(carids)
	carid_list_len = len(carid_list)
	for a in range(0,carid_list_len):
		if carid_list[a][0] == carid:
			cflag = True
	if cflag == False:
		flash("Entered CarId does not Exist !!!")
		return render_template("deletecars.html")
		
	cursor.execute("""DELETE FROM Car WHERE Car_id = %s""",[carid])
	conn.commit()
	#print(mpassword,dusername,husername)
	cursor.close()
	flash("Car Successfully Deleted !!!")
	return render_template("deletecars.html")
	

#-----------------------------------------------------------------------

#---------------------------------------------ADD Driver-----------------------------------------------------------------------------------------

@app.route("/adddriver/",methods=['GET','POST'])

def adddriver():
	return render_template("adddriver.html")

@app.route("/addDRIVER/",methods=['GET','POST'])

def adddriverform():
	
	cursor = conn.cursor()
	dfname = request.form["dfname"]
	dlname = request.form["dlname"]
	dphone = request.form["dphone"]
	license = request.form["license"]
	dage = request.form["dage"]
	cursor.execute("""INSERT INTO Driver(fName,lName,phone_no,licence_no,age) VALUES (%s,%s,%s,%s,%s)""",(dfname,dlname,dphone,license,dage)) 
	conn.commit()
	cursor.close()
	#print(mpassword,dusername,husername)
	flash("New Driver Successfully Added !!!")
	return render_template("adddriver.html")
	
#-------------------------------------ADD DRIVER END------------------------------------------------

#-------------------------------Display Driver -------------------------------------------------
@app.route("/displaydrivers/",methods=['GET','POST'])

def displaydriver():
	cursor = conn.cursor()
	cursor.execute("""SELECT * FROM Driver""")
	data1 = cursor.fetchall()
	cursor.close()
	
	return render_template("displaydrivers.html",data = data1)
	
#----------------------------DISPLAY DRIVER ENDS------------------------------------------------------------

#---------------------------DELETE DRIVER-----------------------------------------------------------------
@app.route("/deletedriver/",methods=['GET','POST'])

def delete_driver():
	return render_template("deletedriver.html")	
	
@app.route("/deleteDriver/",methods=['GET','POST'])

def deletedriver():
	cursor = conn.cursor()
	driverid = str(request.form["driverid"])
	
	'''dflag = False
	cursor.execute("""SELECT driverId FROM Driver""")
	driverids = cursor.fetchall()
	driverid_list = list(driverids)
	driverid_list_len = len(driverid_list)
	for a in range(0,driverid_list_len):
		if driverid_list[a][0] == driverid:
			dflag = True
	if dflag == False:
		flash("Entered DriverId does not Exist !!!")
		return render_template("deletedriver.html")
	'''
	cursor.execute("""DELETE FROM Booking WHERE driverId = %s""",[driverid])	
	cursor.execute("""DELETE FROM Driver WHERE driverId = %s""",[driverid])
	conn.commit()
	#print(mpassword,dusername,husername)
	cursor.close()
	flash("Driver Successfully Deleted !!!")
	return render_template("deletedriver.html")

#----------------------------ABOUT PAGE-------------------------------------------

@app.route('/aboutpage/',methods=['GET','POST'])

def aboutpage():
	print("Entered") 	#Testing
	
	return render_template("about.html")	
	
@app.route('/contactpage/',methods=['GET','POST'])

#--------------------------END ABOUT PAGE -------------------------------------------------------------------------

@app.route("/payment",methods=["GET","POST"])

def paymentdriver():
	print("ENTERED")
	
	return render_template("payment.html")
	
@app.route("/creditPAYMENT",methods=["GET","POST"])

def credit_payment():
	
	km = {'Nashik-Pune': 211,'Nashik-Mumbai':165,'Nashik-Nagpur':680,'Nashik-Dhule':144,'Nashik-Aurangabad':160}
	cursor = conn.cursor()
	print("CUST ID ",custid)
	#paid = int(request.form["radio"])
	
	#payment = payment_status[paid]
	payment = "Paid"
	payment_type = "Credit Card"
	
	print("CUSTID : ",custid)
	cursor.execute("""SELECT bookingId FROM Booking WHERE userId = %s and carid =%s and driverid =%s""",[custid,CARID,driverID])
	book = cursor.fetchall()
	bookingid = book[0][0]
	
	cursor.execute("""SELECT cab_route FROM Booking WHERE bookingId = %s""",[bookingid])
	route = cursor.fetchall()
	cab_route = route[0][0]
	KM = km[cab_route]
	
	cursor.execute("""SELECT carid FROM Booking WHERE bookingId = %s""",[bookingid])
	carID = cursor.fetchall()
	carid = carID[0][0]
	
	cursor.execute("""SELECT price_per_km FROM Car WHERE Car_id = %s""",[carid])
	cabprice = cursor.fetchall()
	price = int(cabprice[0][0])
	
	print(price,KM)
	final_amount = KM * price
	
	cursor.execute("""INSERT INTO Payment(payment_type,status,bookingId,total_amount) values(%s,%s,%s,%s)""",(payment_type,payment,bookingid,final_amount))
	
	conn.commit()
	
	print("PAID CREDIT ")
	print("STATUS : ",payment)
	print("payment_type : ",payment_type)
	return redirect('/generateinvoice')
	
@app.route("/netbankingPAYMENT",methods=["GET","POST"])

def netbanking_payment():
	km = {'Nashik-Pune': 211,'Nashik-Mumbai':165,'Nashik-Nagpur':680,'Nashik-Dhule':144,'Nashik-Aurangabad':160}
	#paid = int(request.form["radio"])
	
	#payment = payment_status[paid]
	payment = "Paid"
	payment_type = "Net Banking"
	
	print("CUSTID : ",custid)
	cursor.execute("""SELECT bookingId FROM Booking WHERE userId = %s and carid =%s and driverid =%s""",[custid,CARID,driverID])
	book = cursor.fetchall()
	bookingid = book[0][0]
	
	cursor.execute("""SELECT cab_route FROM Booking WHERE bookingId = %s""",[bookingid])
	route = cursor.fetchall()
	cab_route = route[0][0]
	KM = km[cab_route]
	
	cursor.execute("""SELECT carid FROM Booking WHERE bookingId = %s""",[bookingid])
	carID = cursor.fetchall()
	carid = carID[0][0]
	
	cursor.execute("""SELECT price_per_km FROM Car WHERE Car_id = %s""",[carid])
	cabprice = cursor.fetchall()
	price = int(cabprice[0][0])
	
	print(price,KM)
	final_amount = KM * price
	
	cursor.execute("""INSERT INTO Payment(payment_type,status,bookingId,total_amount) values(%s,%s,%s,%s)""",(payment_type,payment,bookingid,final_amount))
	
	conn.commit()
	print("PAID NET ")
	print("STATUS : ",payment)
	print("payment_type : ",payment_type)
	return redirect('/generateinvoice')
	
@app.route("/debitPAYMENT",methods=["GET","POST"])

def debit_payment():
	km = {'Nashik-Pune': 211,'Nashik-Mumbai':165,'Nashik-Nagpur':680,'Nashik-Dhule':144,'Nashik-Aurangabad':160}
	#paid = int(request.form["radio"])
	
	#payment = payment_status[paid]
	payment = "Paid"	
	payment_type = "Debit Card"
	
	print("CUSTID : ",custid)
	cursor.execute("""SELECT bookingId FROM Booking WHERE userId = %s and carid =%s and driverid =%s""",[custid,CARID,driverID])
	book = cursor.fetchall()
	bookingid = book[0][0]
	
	cursor.execute("""SELECT cab_route FROM Booking WHERE bookingId = %s""",[bookingid])
	route = cursor.fetchall()
	cab_route = route[0][0]
	KM = km[cab_route]
	
	cursor.execute("""SELECT carid FROM Booking WHERE bookingId = %s""",[bookingid])
	carID = cursor.fetchall()
	carid = carID[0][0]
	
	cursor.execute("""SELECT price_per_km FROM Car WHERE Car_id = %s""",[carid])
	cabprice = cursor.fetchall()
	price = int(cabprice[0][0])
	
	print(price,KM)
	final_amount = KM * price
	
	cursor.execute("""INSERT INTO Payment(payment_type,status,bookingId,total_amount) values(%s,%s,%s,%s)""",(payment_type,payment,bookingid,final_amount))
	
	
	conn.commit()
	print("PAID DEBIT ")
	print("STATUS : ",payment)
	print("payment_type : ",payment_type)

	return redirect('/generateinvoice')
#------------------------PAYMENT END--------------------------------------------
#-----------------------INVOICE ------------------------------------------------------------------

@app.route("/generateinvoice/",methods=['GET','POST'])

def invoice():
	cursor = conn.cursor()
	
	print("CUSTID : ",custid)
	#user_id=request.form['user']
	cursor.execute("""SELECT carId FROM Booking WHERE bookingId = %s""",[b_actual_id])
	carr = cursor.fetchall()
	carrid = carr[0][0]
	#print(bookingid)
	
	cursor.execute("""SELECT model_name FROM Car WHERE car_id = %s""",[carrid])
	modell = cursor.fetchall()
	model = modell[0][0]
	#print(bookingId)
	#cursor.execute("""select Payment_id from Payment where status=%s and payment_type=%s""",(payment,payment_type))
	#pay=cursor.fetchall()
	#payment_id=pay[0][0]
	cursor.execute("""SELECT fName,lName FROM Cust_User where userId=%s""",[custid])
	#data5 = cursor.fetchall()
	data5 = cursor.fetchall()
	cursor.execute("""SELECT emailId FROM Cust_User WHERE userId = %s""",[custid])
	emaill = cursor.fetchall()
	semail = emaill[0][0]
	print(data5)
	data10=data5[0][0] +" "+data5[0][1]
	cursor.execute("""SELECT phone FROM Cust_User where userId=%s""",[custid])
	p_no=cursor.fetchall()
	p_no1=p_no[0][0]
	print(p_no)
	cursor.execute("""SELECT Cab,startdate,endDate,Pickup_time,Pickup_location,Drop_off_location FROM Booking where bookingId=%s""",[b_actual_id])
	union=cursor.fetchall()
	Cab=union[0][0]
	Sd=union[0][1]
	Ed=union[0][2]
	P_time=union[0][3]
	P_loc=union[0][4]
	D_loc=union[0][5]
	cursor.execute("""SELECT driverId FROM Booking where  bookingId=%s""",[b_actual_id])
	d_id=cursor.fetchall()
	driverid=d_id[0][0]
	cursor.execute("""SELECT fName,lName FROM Driver where driverId=%s""",[driverid])
	d_name=cursor.fetchall()
	d_full_name=d_name[0][0]+" "+d_name[0][1]
	cursor.execute("""SELECT phone_no FROM Driver where driverId=%s""",[driverid])
	dphone = cursor.fetchall()
	dphoneno = dphone[0][0]
	cursor.execute("""SELECT payment_type  FROM Payment where bookingId=%s""",[b_actual_id])
	pType=cursor.fetchall()
	print("PTYPE",pType)
	P_type=pType[0][0]
	
	cursor.execute("""SELECT total_amount FROM Payment where bookingId=%s""",[b_actual_id])
	amt1=cursor.fetchall()
	amt=amt1[0][0]
	bID = str(b_actual_id)
	msg=Message("Your Cab is Successfully Booked !!!",sender="Car Rentel Services",recipients=[semail])
	msg.body = "Thank you for Booking Cab from Us.Your Booking ID is "+bID
	mail.send(msg)
			
	return render_template("invoice.html",data =b_actual_id,name=data10,cab=Cab,cab_model=model,sd=Sd,ed=Ed,p_time=P_time,p_loc=P_loc,d_loc=D_loc,dName=d_full_name,dphone1=dphoneno,p_type=P_type,amount = amt)
	
	
#---------------------DISPLAY CAR STATUS ---------------------------------------

@app.route("/displaycarstatus/",methods=['GET','POST'])

def carstatusdriver():
	cursor = conn.cursor()
	cursor.execute("""SELECT Car_id,model_name,registeration_no,Car_type,status FROM Car""")
	data1 = cursor.fetchall()
	cursor.close()
	
	return render_template("displaystatuscar.html",data = data1)

#---------------------DISPLAY CAR STATUS ENDS---------------------------------------.

#---------------------Change CAR STATUS ---------------------------------------
@app.route("/changecarstatus/",methods=['GET','POST'])

def changecarstatusdriver():
	return render_template("changecarstatus.html")

@app.route("/changecarSTATUS/",methods=['GET','POST'])

def changecarstatus():
	ccflag = False
	status_type = ['Available','Booked']
	Car_Type = ""
	cursor = conn.cursor()
	carid1 = request.form["cari"]
	
	cursor.execute("""SELECT Car_id FROM Car WHERE Car_id = %s""",[carid1])
	cid = cursor.fetchall()
	cid_list = list(cid)
	cid_len = len(cid_list)
	for a in range(0,cid_len):
		if cid_list[a][0] == carid1:
			ccflag = True
	if ccflag == False:
		flash("Entered CarID is Invalid !!!")
		return render_template("changecarstatus.html")
			
	Type = int(request.form["status"])
	status_Type = status_type[Type]
	
	cursor.execute("""UPDATE Car SET status = %s WHERE Car_id = %s""",(status_Type,carid1))
	conn.commit()
	cursor.close()
	#print(mpassword,dusername,husername)
	flash("Car Status Successfully Changed !!!")
	return render_template("changecarstatus.html")

#---------------------DISPLAY DRIVER STATUS ---------------------------------------

@app.route("/displaydriverstatus/",methods=['GET','POST'])

def driverstatusdriver():
	cursor = conn.cursor()
	cursor.execute("""SELECT driverId,fName,lName,licence_no,status FROM Driver""")
	data1 = cursor.fetchall()
	cursor.close()
	
	return render_template("displaystatusdriver.html",data = data1)

#---------------------DISPLAY DRIVER STATUS ENDS---------------------------------------.

#---------------------Change DRIVER STATUS ---------------------------------------
@app.route("/changedriverstatus/",methods=['GET','POST'])

def changedriverstatusdriver():
	return render_template("changedriverstatus.html")

@app.route("/changedriverSTATUS/",methods=['GET','POST'])

def changedriverstatus():
	cdflag1 = False
	status_type = ['Available','Booked']
	Car_Type = ""
	cursor = conn.cursor()
	driverid = request.form["driverid"]
	driverid2 = int(driverid)
	cursor.execute("""SELECT driverId FROM Driver WHERE driverId = %s""",[driverid])
	did = cursor.fetchall()
	did_list = list(did)
	did_len = len(did_list)
	print("DID LIST",did_list)
	print("DRIVER ID :",driverid)
	for a in range(0,did_len):
		if did_list[a][0] == driverid2:
			cdflag1 = True
	if cdflag1 == False:
		flash("Entered DriverID is Invalid !!!")
		return render_template("changedriverstatus.html")
		
	Type = int(request.form["status"])
	status_Type = status_type[Type]
	
	cursor.execute("""UPDATE Driver SET status = %s WHERE driverId = %s""",(status_Type,driverid))
	conn.commit()
	cursor.close()
	#print(mpassword,dusername,husername)
	flash("Driver Status Successfully Changed !!!")
	return render_template("changedriverstatus.html")


#-----------------------------------------------------------------------------------------------------------------
@app.route('/pdf_download/',methods=['GET','POST'])

def pdf_download():
	cursor = conn.cursor()
	
	print("CUSTID : ",custid)
	#user_id=request.form['user']
	cursor.execute("""SELECT carId FROM Booking WHERE bookingId = %s""",[b_actual_id])
	carr = cursor.fetchall()
	carrid = carr[0][0]
	#print(bookingid)
	
	cursor.execute("""SELECT model_name FROM Car WHERE car_id = %s""",[carrid])
	modell = cursor.fetchall()
	model = modell[0][0]
	
	#print(bookingId)
	#cursor.execute("""select Payment_id from Payment where status=%s and payment_type=%s""",(payment,payment_type))
	#pay=cursor.fetchall()
	#payment_id=pay[0][0]
	
	cursor.execute("""SELECT fName,lName FROM Cust_User where userId=%s""",[custid])
	#data5 = cursor.fetchall()
	data5 = cursor.fetchall()

	print(data5)
	data10=data5[0][0] +" "+data5[0][1]
	cursor.execute("""SELECT phone FROM Cust_User where userId=%s""",[custid])
	p_no=cursor.fetchall()
	p_no1=p_no[0][0]
	print(p_no)
	cursor.execute("""SELECT Cab,startdate,endDate,Pickup_time,Pickup_location,Drop_off_location FROM Booking where bookingId=%s""",[b_actual_id])
	union=cursor.fetchall()
	Cab=union[0][0]
	Sd=union[0][1]
	Ed=union[0][2]
	P_time=union[0][3]
	P_loc=union[0][4]
	D_loc=union[0][5]
	cursor.execute("""SELECT driverId FROM Booking where  bookingId=%s""",[b_actual_id])
	d_id=cursor.fetchall()
	driverid=d_id[0][0]
	cursor.execute("""SELECT fName,lName FROM Driver where driverId=%s""",[driverid])
	d_name=cursor.fetchall()
	d_full_name=d_name[0][0]+" "+d_name[0][1]
	cursor.execute("""SELECT phone_no FROM Driver where driverId=%s""",[driverid])
	dphone = cursor.fetchall()
	dphoneno = dphone[0][0]
	cursor.execute("""SELECT payment_type  FROM Payment where bookingId=%s""",[b_actual_id])
	pType=cursor.fetchall()
	print("PTYPE",pType)
	P_type=pType[0][0]
	
	cursor.execute("""SELECT total_amount FROM Payment where bookingId=%s""",[b_actual_id])
	amt1=cursor.fetchall()
	amt=amt1[0][0]
	
	html =  render_template("invoice.html",data = b_actual_id,name=data10,cab=Cab,cab_model=model,sd=Sd,ed=Ed,p_time=P_time,p_loc=P_loc,d_loc=D_loc,dName=d_full_name,dphone1=dphoneno,p_type=P_type,amount = amt)
	return render_pdf(HTML(string=html))

#------------------------------------------------STATUS PAGE--------------------------------------------------
@app.route('/status/',methods=['GET','POST'])

def statusdriver():
	most_used_route = ""
	cursor = conn.cursor()
	cursor.execute("""SELECT COUNT(*) FROM Cust_User""")
	total_c = cursor.fetchall()
	total_cust = total_c[0][0]
	cursor.execute("""SELECT COUNT(*) FROM Car""")
	total_ca = cursor.fetchall()
	total_car1 = total_ca[0][0]
	cursor.execute("""SELECT COUNT(*) FROM Car""")
	total_ca = cursor.fetchall()
	total_car1 = total_ca[0][0]
	cursor.execute("""SELECT COUNT(*) FROM Admin_User""")
	total_a = cursor.fetchall()
	total_admin = int(total_a[0][0])
	cursor.execute("""SELECT COUNT(*) FROM Driver""")
	total_d = cursor.fetchall()
	total_driver = int(total_d[0][0])
	total_employ = total_driver + total_admin
	cursor.execute("""SELECT COUNT(*) FROM Car WHERE status = 'Available' """)
	cart = cursor.fetchall()
	tcar = cart[0][0]
	cursor.execute("""SELECT COUNT(*) FROM Driver WHERE status = 'Available' """)
	drivert = cursor.fetchall()
	drivert = drivert[0][0]
	cursor.execute("""SELECT COUNT(*) FROM Booking""")
	tbook = cursor.fetchall()
	tbooking = tbook[0][0]
	cursor.execute("""SELECT COUNT(*) FROM Booking WHERE cab_route = 'Nashik-Pune' """)
	NP = cursor.fetchall()
	NProute = int(NP[0][0])
	cursor.execute("""SELECT COUNT(*) FROM Booking WHERE cab_route = 'Nashik-Nagpur' """)
	NN = cursor.fetchall()
	NNroute = int(NN[0][0])
	cursor.execute("""SELECT COUNT(*) FROM Booking WHERE cab_route = 'Nashik-Mumbai' """)
	NM = cursor.fetchall()
	NMroute = int(NM[0][0])
	cursor.execute("""SELECT COUNT(*) FROM Booking WHERE cab_route = 'Nashik-Aurangabad' """)
	NA = cursor.fetchall()
	NAroute = int(NA[0][0])
	cursor.execute("""SELECT COUNT(*) FROM Booking WHERE cab_route = 'Nashik-Dhule' """)
	ND = cursor.fetchall()
	NDroute = int(ND[0][0])
	if NProute > NNroute and NProute > NMroute and NProute > NAroute and NProute > NDroute:
		most_used_route = "Nashik-Pune"
	elif NNroute > NProute and NNroute > NMroute and NNroute > NAroute and NNroute > NDroute:
		most_used_route = "Nashik-Nagpur"
	elif NMroute > NNroute and NMroute > NProute and NMroute > NAroute and NMroute > NDroute:
		most_used_route = "Nashik-Mumbai"
	elif NAroute > NNroute and NAroute > NMroute and NAroute > NProute and NAroute > NDroute:
		most_used_route = "Nashik-Aurangabad"
	elif NDroute > NNroute and NDroute > NMroute and NDroute > NAroute and NDroute > NProute:
		most_used_route = "Nashik-Dhule"
	
	cursor.execute("""SELECT SUM(total_amount) FROM Payment""")
	total_sum = cursor.fetchall()
	tsum = int(total_sum[0][0])	
	print("TOTAL CUST",total_cust)
	return render_template('Status.html',total = total_cust,tcar=total_car1,total_e=total_employ,total_car = tcar,total_driver=drivert,total_booking=tbooking,mroute=most_used_route,total_sum1=tsum)

@app.route('/allbooked/',methods=['GET','POST'])
def allbooked():
	print("Entered") 	#Testing
	
	return render_template("allbooked.html")


@app.route('/booked/',methods=['GET','POST'])
def booked():
	return redirect("/")
	
	
@app.route('/lastpage/',methods=['GET','POST'])

def lastpage():
	print("Entered") 	#Testing
	
	return render_template("final.html")
	
if __name__ == "__main__":
	
	app.run(debug=True)	
	
