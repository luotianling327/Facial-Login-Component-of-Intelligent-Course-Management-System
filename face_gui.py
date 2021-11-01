import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import webbrowser
import requests
import json


def get_weather_img(weather):
    weather_dict = {
        "雨" : "rainy.png",
        "阴" : "cloudy.png",
        "云" : "cloudy.png",
        "晴" : "sunny.png",
        "风" : "windy.png",
        "雪" : "snowy.png"
    }

    default = "晴"
    filename = "sunny.png"

    cn_weathers = list(weather_dict.keys())
    for cn_weather in cn_weathers:
        if cn_weather in weather:
            filename = weather_dict[cn_weather]
            break
    else:
        filename = weather_dict[default]

    return "./weather_img/imgs/" + filename

def get_weather(city):
    try:
        r = requests.get("http://wthrcdn.etouch.cn/weather_mini?citykey=" + city)
        result = json.loads(r.text)
        weather = result["data"]["forecast"][0]["type"]
    except:
        sg.Popup("Some error occured!")
        exit()
    return weather

def update_city_weather(window, city):
    weather = get_weather(city)

    weather_img_widget = window["-WEATHER-IMG-"]

    filename = get_weather_img(weather)

    weather_img_widget.Update(filename = filename)

# Choose a Theme for the Layout
# sg.theme('LightBlue')
sg.theme('BlueMono')

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="facerecognition")
# date = datetime.now()
# now = datetime.now()
# login_time = datetime.now()
# current_time_login = now.strftime("%H:%M:%S")
# cursor = myconn.cursor()

# 2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# 3 Define pysimplegui setting
layout = [
    [sg.Text('Setting', size=(18, 1), font=('Any', 18), text_color='#26072d', justification='left')],
    [sg.Text('Confidence'),
     sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=60, size=(15, 15), key='confidence')],
    [sg.OK(), sg.Cancel()]
]
win = sg.Window('Course Management System',
                default_element_size=(21, 1),
                text_justification='right',
                auto_size_text=False).Layout(layout)
event, values = win.Read()
if event == 'Cancel':
    exit()
args = values
gui_confidence = args["confidence"]
win_started = False
win.close()

# 4 Open the camera and start face recognition
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        # print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # If the face is recognized
        if conf >= gui_confidence:

            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            
            date = datetime.now()
            now = datetime.now()
            login_time = datetime.now()
            current_time_login = now.strftime("%H:%M:%S")
            cursor = myconn.cursor()
            
            update = "UPDATE Student SET login_date=%s WHERE name=%s"
            val = (date, current_name)
            cursor.execute(update, val)
            update = "UPDATE Student SET login_time=%s WHERE name=%s"
            val = (current_time_login, current_name)
            cursor.execute(update, val)
            myconn.commit()
               
            layout = [
                [sg.Text("Greetings and Welcome, "  + current_name + '!')],
                [sg.Text("Login time:   " + current_time_login)],
                [sg.Text("Weather:   ")],
                [sg.Image(size = (30, 30), key = "-WEATHER-IMG-")],
                [sg.Button('Enter'), sg.Button('Exit')]
            ]
            window = sg.Window("Welcome Here ", layout, finalize=True)
            update_city_weather(window, "101320101")  #Get the weather of Hong Kong
            w = get_weather("101320101")
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
            
                now = datetime.now()
                logout_time = datetime.now()
                current_time_logout = now.strftime("%H:%M:%S")
                cursor = myconn.cursor()
                update = "UPDATE Student SET logout_date=%s WHERE name=%s"
                val = (date, current_name)
                cursor.execute(update, val)
                update = "UPDATE Student SET logout_time=%s WHERE name=%s"
                val = (current_time_logout, current_name)
                cursor.execute(update, val)
                update = "UPDATE Student SET duration=%s WHERE name=%s"
                s = (logout_time - login_time)
                val = (s, current_name)
                cursor.execute(update, val)
                myconn.commit()
                exit()
            window.close()

            # Find the student information in the database.
            select = "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (
                name)
            name = cursor.execute(select)
            result = cursor.fetchall()
            # print(result)

            data = "error"

            for x in result:
                data = x

            # If the student's information is not found in the database
            if data == "error":
                # the student's data is not in the database
                print("The student", current_name, "is NOT FOUND in the database.")

            # If the student's information is found in the database
            else:
                """
                Implement useful functions here.
                Check the course and classroom for the student.
                    If the student has class room within one hour, the corresponding course materials
                        will be presented in the GUI.
                    if the student does not have class at the moment, the GUI presents a personal class 
                        timetable for the student.

                """

                select = "SELECT K.course_id, K.type, K.course_name, K.class_start_time, K.class_end_time, K.class_date, K.classroom_address, K.zoom_links, K.material_links, K.teacher_message FROM( SELECT l.course_id, l.type,c.course_name, l.class_start_time, l.class_end_time, l.class_date, cla.classroom_address, l.zoom_links, l.material_links, c.teacher_message, (TIME_TO_SEC(l.class_start_time)-TIME_TO_SEC(CURTIME()))/3600 AS timediff FROM Class l, student s, takes,classroom cla, course c WHERE s.name='%s' AND s.student_id=takes.student_id AND takes.course_id=c.course_id AND cla.classroom_id=l.classroom_id AND c.course_id=l.course_id AND  l.class_date=CURDATE() ORDER BY l.class_date ASC, l.class_start_time ASC LIMIT 1) AS K WHERE K.timediff<1 AND K.timediff>0" % (
                    current_name)
                cursor.execute(select)
                result = cursor.fetchall()
                print(result)

                if result:  # within an hour
                    select = "SELECT K.course_id, K.type, K.course_name, K.class_start_time, K.class_end_time, K.class_date, K.classroom_address, K.zoom_links, K.material_links, K.teacher_message FROM(SELECT l.course_id, l.type,c.course_name, l.class_start_time, l.class_end_time, l.class_date, cla.classroom_address, l.zoom_links, l.material_links, c.teacher_message, (TIME_TO_SEC(l.class_start_time)-TIME_TO_SEC(CURTIME()))/3600 AS timediff FROM Class l, student s, takes,classroom cla, course c WHERE s.name='%s' AND s.student_id=takes.student_id AND takes.course_id=c.course_id AND cla.classroom_id=l.classroom_id AND c.course_id=l.course_id AND  l.class_date=CURDATE() ORDER BY l.class_date ASC, l.class_start_time ASC LIMIT 1) AS K WHERE K.timediff<1 AND K.timediff>0" % (
                    current_name)

                    cursor.execute(select)
                    result = cursor.fetchall()

                    for i in result:
                        course_id=i[0]
                        type1=i[1]
                        course_name = i[2]
                        start_time = i[3]
                        end_time = i[4]
                        class_date = i[5]
                        classroom_address = i[6]
                        zoom_links = i[7]
                        material_links = i[8]
                        teachers_message = i[9]

                    select = "SELECT student.email FROM student WHERE student.name='%s'" % (
                                 current_name)
                    cursor.execute(select)
                    result = cursor.fetchall()
                    email=result[0][0]
                    menu_def = [['Menu', ['Back', 'Exit']],
                                ['Help', 'About...']
                               ]

                    layout = [
                        [sg.Menu(menu_def)],
                        [sg.Text('YOU HAVE CLASS WITHIN ONE HOUR!')],
                        [sg.Text('Course name:   ' + course_name)],
                        [sg.Text('Classroom:   ' + classroom_address)],
                        [sg.Text('Start time:   ' + str(start_time))],
                        [sg.Text('End time:   ' + str(end_time))],
                        [sg.Text('Zoom link:   ' + zoom_links, tooltip = zoom_links, 
                                enable_events=True, key=f'URL {zoom_links}')], 
                        [sg.Text('Material link:   ' +  material_links,  tooltip = material_links,
                                enable_events=True, key=f'URL {material_links}')],
                        [sg.Text("Teacher's Message:   " + teachers_message)],
                        [sg.Button("Send to My Email"), sg.Button('Back'), sg.Button('Exit')]
                    ]

                    win1 = sg.Window('Your Next Course',
                                     default_element_size=(50, 1),
                                     text_justification='left',
                                     auto_size_text=False).Layout(layout)
                   
                    while True:
                        event, values = win1.Read()

                        if event == sg.WIN_CLOSED or event is None or event == "Back" or event == 'Exit':
                            now = datetime.now()
                            logout_time = datetime.now()
                            current_time_logout = now.strftime("%H:%M:%S")
                            cursor = myconn.cursor()
                            update = "UPDATE Student SET logout_date=%s WHERE name=%s"
                            val = (date, current_name)
                            cursor.execute(update, val)
                            update = "UPDATE Student SET logout_time=%s WHERE name=%s"
                            val = (current_time_logout, current_name)
                            cursor.execute(update, val)
                            update = "UPDATE Student SET duration=%s WHERE name=%s"
                            s = (logout_time - login_time)
                            val = (s, current_name)
                            cursor.execute(update, val)
                            myconn.commit()
                            
                            if event == 'Exit':
                                exit()
                        
                            win1.close()
                            break
                        else:
                            if event.startswith("URL "):
                                url = event.split(' ')[1]
                                webbrowser.open(url)
                            if event == 'Send to My Email':
                                host_server="smtp.qq.com"
                                sender_qq="2837458469"
                                sender_address ="icms_hku@qq.com"
                                pwd = "cbubfpshcdoodech"
                                receiver = email
                                mail_title="Course Message"
                                mail_content="Hello, " + current_name + "! YOU HAVE CLASS WITHIN ONE HOUR!\n"\
                                            + "Course name:   " + course_name\
                                            + "\nClassroom:   " + classroom_address\
                                            + "\nStart time:   " + str(start_time)\
                                            + "\nEnd time:   " + str(end_time)\
                                            + "\nZoom link:   " + zoom_links\
                                            + "\nMaterial link:   " + material_links
                                            
                                smtp = smtplib.SMTP_SSL(host_server)
                                smtp.set_debuglevel(1)
                                smtp.ehlo(host_server)
                                smtp.login(sender_qq, pwd)

                                msg = MIMEText(mail_content, "plain", 'utf-8')
                                msg["Subject"] = mail_title
                                msg["From"] = sender_address
                                msg["To"] = receiver
                                smtp.sendmail(sender_address, receiver, msg.as_string())
                                smtp.quit()

                                sg.popup('Mail Sent')
                           
                            if event == "About...":
                                webbrowser.open('www.hku.hk')
                        
     

                else:  # No class at the moment
                    select="SELECT c.course_name, l.type, l.class_date, l.class_start_time, l.class_end_time, cla.classroom_address FROM Class l, Student s, Takes t, Classroom cla, Course c WHERE s.name='%s' AND (s.student_id=t.student_id AND t.course_id=c.course_id AND l.classroom_id=cla.classroom_id AND c.course_id=l.course_id AND l.class_date=CURDATE() AND HOUR(TIMEDIFF(CURTIME(),l.class_start_time)) >= 1 OR s.student_id=t.student_id AND t.course_id=c.course_id AND l.classroom_id=cla.classroom_id AND c.course_id=l.course_id AND l.class_date>CURDATE()) ORDER BY l.class_date ASC, l.class_start_time ASC"%(current_name)
                    cursor.execute(select)
                    query_results = cursor.fetchall()
                    menu_def = [['Menu', ['Back', 'Exit']],
                                ['Help', 'About...']
                               ] 

                    layout = [
                        [sg.Menu(menu_def)],
                        [sg.Text('YOU HAVE NO CLASSES WITHIN ONE HOUR :)')],
                        [sg.Text('Class TimeTable')],
                        [sg.Table(values=query_results,
                                  headings=['course_name', 'type', 'class_date', 'class_start_time',
                                            'class_end_time', 'classroom_address'],
                                  max_col_width=500,
                                  auto_size_columns=True,
                                  justification='center',
                                  num_rows=12,
                                  row_height=30,
                                  key='_table_',
                                  text_color='black',
                                  background_color='azure',
                                  alternating_row_color='azure2',
                                  enable_events=True,
                                  bind_return_key=True,
                                  tooltip='This is a table')],
                        [sg.Button('Back'),  sg.Button('Exit')]
                    ]
                    win2 = sg.Window('My Class Time Table', layout, size = (809,500))
                    
                    while True:
                    
                        event, values = win2.Read()
                        # print(values)
                        
                        if event == sg.WIN_CLOSED or event =="Back" or event == 'Exit':
                            now = datetime.now()
                            logout_time = datetime.now()
                            current_time_logout = now.strftime("%H:%M:%S")
                            cursor = myconn.cursor()
                            update = "UPDATE Student SET logout_date=%s WHERE name=%s"
                            val = (date, current_name)
                            cursor.execute(update, val)
                            update = "UPDATE Student SET logout_time=%s WHERE name=%s"
                            val = (current_time_logout, current_name)
                            cursor.execute(update, val)
                            update = "UPDATE Student SET duration=%s WHERE name=%s"
                            s = (logout_time - login_time)
                            val = (s, current_name)
                            cursor.execute(update, val)
                            myconn.commit()
                            if event == 'Exit':
                                exit()
                            win2.close()
                            break
                        else:
                            if event == "About...":
                                webbrowser.open('http://www.hku.hk')


        # If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = ("Your face is not recognized")
            print(hello)
            engine.say(hello)
            # engine.runAndWait()

    # GUI
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if not win_started:
        win_started = True
        layout = [
            [sg.Text('Course Management System Interface', size=(30, 1))],
            [sg.Image(data=imgbytes, key='_IMAGE_')],
            [sg.Text('Confidence'),
             sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=gui_confidence, size=(15, 15),
                       key='confidence')],
            [sg.Exit()]
        ]
        win = sg.Window('Course Management System',
                        default_element_size=(14, 1),
                        text_justification='right',
                        auto_size_text=False).Layout(layout).Finalize()
        image_elem = win.FindElement('_IMAGE_')
    else:
        image_elem.Update(data=imgbytes)

    event, values = win.Read(timeout=20)
    if event is None or event == 'Exit':
        break
    gui_confidence = values['confidence']

win.Close()
cap.release()


