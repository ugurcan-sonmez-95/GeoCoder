from flask import Flask, render_template, request, send_file
from geopy.geocoders import ArcGIS
import pandas
import datetime

app = Flask(__name__)

### Routes to home page, success page and download
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods = ['POST'])
def success():
    if request.method == 'POST':
        file = request.files['file']
        try:
            df = pandas.read_excel(file)
            geoc = ArcGIS(scheme = 'http')
            df.columns = [i.capitalize() for i in df.columns]
            df['Coordinates'] = df['Address'].apply(geoc.geocode)
            df['Latitude'] = df['Coordinates'].apply(lambda x: x.latitude if x != None else None)
            df['Longitude'] = df['Coordinates'].apply(lambda x: x.longitude if x != None else None)
            df = df.drop('Coordinates', 1)
            filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f" + ".xlsx")
            df.to_excel(filename, index = None)
            return render_template("index.html", filename = filename, text = df.to_html(), bttn = 'download.html')
        except Exception:
            return render_template("index.html", text = "Please make sure that you have chosen the file and it has an 'Address' or 'address' column.")

@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, attachment_filename = 'new_file.xlsx', as_attachment = True)

if __name__ == '__main__':
    #app.debug = True
    app.run()