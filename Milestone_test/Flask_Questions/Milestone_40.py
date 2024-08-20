from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        data = request.form['data']
        return f"Received: {data}"
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
