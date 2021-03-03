from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def ():


@app.route("/scrape")
def echo(): return render_template("index.html", Mars=Mars)
    

if __name__ == "__main__":
    app.run(debug=True)