from flask import Flask, render_template, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField

from main import FEMloader

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'stuff'
app.config['DOWNLOAD_FOLDER'] = 'zips/'


@app.route('/', methods=['GET', 'POST'])
def divide():
    class UrlLink(FlaskForm):
        url = StringField("URL:")

    form = UrlLink()
    loc = None

    if form.validate_on_submit():
        url = form.url.data
        obj = FEMloader(url)
        # loc = obj.dl_location
        loc = ''

    return render_template('base.html', link=loc, form=form)


@app.route('/zips/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
