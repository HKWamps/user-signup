from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

#set up array of input fields (PROMPT, NAME, TYPE, Validation Required)
input_fields = [("Username:", "username", "text") , ("Password:", "password", "password"),
    ("Verify Password:", "verify_pwd", "password"), ("Email (optional):","user_email", "text")]

#set up array to hold error messages
error_list=["","","",""]
input_values=["","","",""]
#set up variable to indicate if error is found
error = ""

def isValidEmail(email):
    rtn_error = ""
    if (len(email) < 3) or (len(email) > 20): 
        rtn_error = "Email MUST be at least 3 and not more than 20 characters with no spaces"
        return rtn_error 
    elif " " in email:
        rtn_error = "Email MUST be at least 3 and not more than 20 characters with no spaces"
        return rtn_error 

    count_p = 0
    count_a = 0
    for char in email:
        if char == ".":
            count_p += 1
        if char=="@":
            count_a += 1
    if count_p != 1 or count_a != 1:
        rtn_error = "Not a valid email address, in the format of XXX@YYY.COM"
        return rtn_error 
    
    return True
    

@app.route("/signup", methods=['POST'])
def validate_signup():

    error = ""


    # look inside the request to figure out what the user typed
    input_username = request.form['username']
    input_pword = request.form['password']
    input_verify = request.form["verify_pwd"]
    input_email = request.form["user_email"]
    
    #save username and email for persistence
    input_values[0]=input_username
    input_values[3]=input_email

    # User Name Validation
    # if the user typed nothing at all, redirect and tell them the error
    if (not input_username) or (input_username.strip() == ""):
        error_list[0] = "Please Enter Username."
        error = "Please Correct Errors Identified Above and Resubmit"
    elif (len(input_username) < 3) or (len(input_username) > 20): 
        error_list[0] = "Username MUST be at least 3 and not more than 20 characters with no spaces"
        error = "Please Correct Errors Identified Above and Resubmit"
    else: 
        error_list[0] = ""
    
    # Password Entry Validation
    if (not input_pword) or (input_pword.strip() == ""):
        error_list[1] = "Please Enter Password."
        error = "Please Correct Errors Identified Above and Resubmit"
    elif (len(input_pword) < 3) or (len(input_pword) > 20): 
        error_list[1] = "Password MUST be at least 3 and not more than 20 characters with no spaces"
        error = "Please Correct Errors Identified Above and Resubmit"   
    else:
        error_list[1] = ""
    
    # Verify Password Validation
    if (not input_verify) or (input_verify.strip() == ""):
        error_list[2] = "Please Verify Password."
        error = "Please Correct Errors Identified Above and Resubmit"
    elif input_verify != input_pword:
        error_list[2] = "Passwords provided do not match"
        error = "Please Correct Errors Identified Above and Resubmit"
    else:
        error_list[2] = ""
    
    # E-Mail validation
    # skip checking email if field is empty
    if not(not(input_email)) or (input_email.strip() != ""):
        
        #call function to check email format
        rtnValue = isValidEmail(input_email)
        if  rtnValue != True:
            error_list[3] = rtnValue
            error = "Please Correct Errors Identified Above and Resubmit"
        



    #if error found, redirect to User Signup page with error message
    if len(error) > 0:
        return redirect("/?error=" + error)


    # if the user wants to add a terrible movie, redirect and tell them the error
    #if new_movie in terrible_movies:
    #    error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
    #    return redirect("/?error=" + error)

    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    #new_movie_escaped = cgi.escape(new_movie, quote=True)

    # TODO:
    # Create a template called add-confirmation.html inside your /templates directory
    # Use that template to render the confirmation message instead of this temporary message below
    #return "Confirmation Message Under Construction..."
    #return render_template('add-confirmation.html', new_movie=new_movie)

    #Successful, send to welcome screen
    return render_template('welcome.html', username=input_username)
    #return render_template('signup.html', input_fields=input_fields, error_list = error_list) #, error=encoded_error and cgi.escape(encoded_error, quote=True))

@app.route("/")
def index():
    encoded_error = request.args.get("error")

    return render_template('signup.html', input_fields=input_fields, error_list = error_list, 
        input_values = input_values, error=encoded_error) # and cgi.escape(encoded_error, quote=True))

app.run()