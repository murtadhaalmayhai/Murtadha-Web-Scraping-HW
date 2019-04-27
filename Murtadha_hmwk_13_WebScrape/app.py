from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars_data

@app.route("/")
def index():
    mars_data = db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data_final = scrape_mars.scrape()
    mars_data = db.mars_data
    mars_data.update({}, mars_data_final, upsert=True)
    return redirect("http://localhost:5000/", code=302)
    
if __name__ == "__main__":
    app.run(debug=True)