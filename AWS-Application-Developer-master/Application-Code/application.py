from flask import render_template
from flask import Flask, request

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def usage():
    return render_template('risingminerva-generic.html')

@application.route('/english')
def englishgreeting():
    username = request.args.get('user')
    if username:
        user = {'username': username, 'greeting': 'Hello'}
    else:
        user = {'username': 'Rising Minerva', 'greeting': 'Hello'}
    return render_template('risingminerva-eb.html', user=user)
    
@application.route('/spanish')
def spanishgreeting():
    username = request.args.get('user')
    if username:
        user = {'username': username, 'greeting': 'Hola'}
    else:
        user = {'username': 'Rising Minerva', 'greeting': 'Hola'}
    return render_template('risingminerva-eb.html', user=user)    
   
# run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()