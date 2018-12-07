from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

field_dict = [
    "Username":"text", 
    "Password": "password"
    "Verify Password": "password",
    "Email (optional)":"text"
]

@app.route("/signup", methods=['POST'])
def validate_signup():
    # look inside the request to figure out what the user typed
    input_username = request.form['username']
    input_pword = request.form['pword']
    input_verify = request.form["verify_pword"]
    input_email = request.form("email")
    
    # if the user typed nothing at all, redirect and tell them the error
    if (not input_username) or (input_username.strip() == ""):
        error = "Please Enter Unsername."
        return redirect("/?error=" + error)
    if (not input_pword) or (input_pword.strip() == ""):
        error = "Please Enter Password."
        return redirect("/?error=" + error)
    if (not input_verify) or (input_verify.strip() == ""):
        error = "Please Verify Password."
        return redirect("/?error=" + error)
    
    # if the user wants to add a terrible movie, redirect and tell them the error
    if new_movie in terrible_movies:
        error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie)
        return redirect("/?error=" + error)

    # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
    new_movie_escaped = cgi.escape(new_movie, quote=True)

    # TODO:
    # Create a template called add-confirmation.html inside your /templates directory
    # Use that template to render the confirmation message instead of this temporary message below
    #return "Confirmation Message Under Construction..."
    return render_template('add-confirmation.html', new_movie=new_movie)

@app.route("/")
def index():
    encoded_error = request.args.get("error")
    return render_template('signup.html', error=encoded_error and cgi.escape(encoded_error, quote=True))

app.run()