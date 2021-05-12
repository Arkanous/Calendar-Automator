import requests
import smtplib 

# API key

def Distance_Calc(home, destination):
    api_file = open("maps_api.txt", "r")
    api_key = api_file.readline()
    api_file.close()
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"

    # Get response
    r = requests.get(url + "origins=" + home + "&destinations=" + destination + "&key=" + api_key) 
    time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
    seconds = r.json()["rows"][0]["elements"][0]["duration"]["value"]
    print("\nThe total travel time from home to work is", time)
    return seconds

def Late_Email(sender, recipient):
    subject = "Sick Day"
    message = "Hello,\n\nSorry, but I will not be able make it to the destination on time."
    email = "Subject: {}\n\n{}".format(subject, message)
    password_file = open("password.txt", "r")
    password = password_file.readline()
    password_file.close()
    s = smtplib.SMTP("smtp.gmail.com", 587) 
    s.starttls() 
    s.login(sender, password)
    s.sendmail(sender, recipient, email)
    s.quit() 
    print("\nSuccessfully sent a sick-day email to", recipient, "since the travel time was too long")

def Notification_Email(sender, recipient, event):
    subject = event
    message = "You should start packing up right about now."
    email = "Subject: {}\n\n{}".format(subject, message)
    password_file = open("password.txt", "r")
    password = password_file.readline()
    password_file.close()
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(sender, password)
    s.sendmail("Antyolonio@gmail.com", recipient, email)
    s.quit()
    print("\nSuccessfully sent a to", recipient)