from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # 模擬兩個商業指標
    metrics = [
        {'title': 'Revenue', 'value': '$1,000,000'},
        {'title': 'Visitation', 'value': '25,000'}
    ]
    return render_template('home.html', metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)
