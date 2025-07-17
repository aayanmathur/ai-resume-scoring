from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resume-options')
def resume_options():
    return render_template('resume-options.html')  # filename must match

if __name__ == '__main__':
    app.run(debug=True)
