from flask import Flask,render_template

# create instance
app = Flask(__name__)



#Filters!!!
#safe
#trim
#striptag
#title
#upper
#lower






@app.route('/')
def main():
    return render_template('index.html')



#create custom error 

#invalid url
@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404


#internal server error
@app.errorhandler(500)
def page_not_found(err):
    return render_template('500.html'), 500


