from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/other")
def about():
    return render_template('other.html')


if __name__ == '__main__':
    app.run(debug=True)
