from flask import Flask, redirect,render_template,url_for,request
from compiler import main
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        # file = request.form["fileContents"]
        files = request.form["inputFile"]
        print(files)
        check = files.split("\n")
        try:
            result = main(check)
        except:
            result = "Found an Error while compiling."
        return render_template("index.html", result=result, files=files)
    else:
        print("get it")
        return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
