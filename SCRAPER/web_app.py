from flask import Flask , render_template


app = Flask(__name__ ,template_folder = 'templates')

@app.route('/')
def Option():
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug = True)