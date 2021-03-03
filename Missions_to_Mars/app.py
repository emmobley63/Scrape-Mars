from flask import Flask, render_template
from scrape_mars import *

app = Flask(__name__)



conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.Mars

@app.route("/scrape")
scrape()

@app.route("/")
def index():
    #Storing Mars data in a list 
    Mars = list(db.Mars.find())

    # Rendering it into index
    return render_template("index.html", Mars=Mars)


    

if __name__ == "__main__":
    app.run(debug=True)