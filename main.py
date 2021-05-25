import flask
from flask import Flask,request,render_template,redirect, url_for
from flask_mysqldb import MySQL
import os
from os.path import join, dirname, realpath
import pandas as pd



app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

#Connect MYSQL 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

# Root URL
@app.route('/')
def home():
    return render_template('form.html')

#content URL
@app.route('')
# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
          # save the file
          
      return redirect(url_for('home'))

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['first_name','last_name']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      cursor = mysql.connection.cursor()
      cursor.execute(''' CREATE TABLE IF NOT EXISTS TestImport(name varchar(255),last_name varchar(255)) ''')
      # Loop through the Rows
      for i,row in csvData.iterrows():
             sql = "INSERT INTO TestImport (first_name, last_name) VALUES (%s, %s)"
             value = (row['first_name'],row['last_name'])
             cursor.execute(sql, value)
             mysql.connection.commit()
             print(i,row['first_name'],row['last_name'])
       
              
if (__name__ == "__main__"):
     app.run(port = 5000)


