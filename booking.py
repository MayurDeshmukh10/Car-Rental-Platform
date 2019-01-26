from flask import Flask, render_template
import MySQLdb
from flask import request

app = Flask(__name__)

conn = MySQLdb.connect(host='localhost',user='mayur',passwd = 'mayur2219981092',port = 8090,db="test_project")
cursor = conn.cursor()

@app.route('/register/',methods = ['GET','POST'])


def register():
	
	print("entered")
	#booking()
	return render_template('booking1.html')
	
	
@app.route('/booking/',methods = ['GET','POST'])


def booking():
	print("entered")
	cabs_list = ["Mini","Sedan","SUV"]
	try:
		userId=request.form["userId"].encode("utf-8")
		#userId = userId.encode(userId.originalEncoding)
		fname = request.form["fName"].encode("utf-8")
		print(fname)
		lname = request.form["lName"].encode("utf-8")
		phone = request.form["PhoneNumber"].encode("utf-8")
		email = request.form["email"].encode("utf-8")	
		cab1 = request.form["cab"].encode("utf-8")
		cab = int(cab1)
		print(userId,fname,lname,phone,email,cab)
		cab_name = ""
		cab_name = cabs_list[cab]
		startDate = request.form["startDate"].encode("utf-8")
		endDate = request.form["endDate"].encode("utf-8")
		time = request.form["time"].encode("utf-8")
		pickupLocation = request.form["pickupLocation"].encode("utf-8")
		dropoffLocation = request.form["dropoffLocation"].encode("utf-8")
		pricePerKm = 10;
		if cabs_list[cab] == 0:
		    pricePerKm = 10 
		elif cabs_list[cab] == 1:
		   pricePerKm = 12
		else:
		   pricePerKm = 16
		print(userId,fname,lname,phone,email,cab,startDate,endDate,time,pickupLocation,dropoffLocation,pricePerKm)
		cursor.execute("""INSERT INTO book(userId,fname,lname,phone,email,cab,startDate,endDate,time,pickupLocation,dropoffLocation,pricePerKm) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(userId,fname,lname,phone,email,cab_name,startDate,endDate,time,pickupLocation,dropoffLocation,pricePerKm)) 
		
		conn.commit()       
		print ("Booked")
		
	except Exception as e:
		return(str(e))
	
		
if __name__ == '__main__':
	app.run(debug=True)
	
	

