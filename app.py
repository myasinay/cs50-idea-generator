from flask import Flask, flash, redirect, render_template, url_for, request
from flask_session import Session

# Helpers
from helpers import generateIdea, allowed_file, custom_data

# Configure application
app = Flask(__name__)
# Max file upload size
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000
# Session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Lists to keeping the history
all_ideas = []
liked_ideas = []


@app.route("/")
def index():
    """Return the index page"""
    if all_ideas:
        return render_template("index.html", idea=all_ideas[-1])

    return render_template("index.html")


@app.route("/generate")
def generate():
    """Generate a new idea"""
    # Generate the new idea
    idea = generateIdea()
    # Save it to history
    all_ideas.append(idea)
    # Show the index page
    return redirect(url_for('index', idea=idea))


@app.route("/like")
def like():
    """Save idea to liked ideas"""
    # Pre-check for newbies
    if not all_ideas:
        flash("I know you're excited, but first you need to generate some ideas. :)")
        return redirect("/")

    # Get the current idea
    current_idea = all_ideas[-1]

    for idea in liked_ideas:
        if idea == current_idea:
            flash("You already liked this idea. If you liked it so much, why are you waiting to take action! :)")
            return redirect("/")

    # Add idea to liked ones
    liked_ideas.append(current_idea)
    # Do not change the screen, show the last idea to user
    return redirect("/")


@app.route("/liked")
def liked():
    """Show the liked ideas"""
    if liked_ideas:
        # Variable for file saver
        ideas = "\n".join(liked_ideas)
        return render_template("liked.html", liked_ideas=liked_ideas, ideas=ideas)
    else:
        return render_template("liked.html")


@app.route("/history")
def history():
    """Show all the ideas generated recently"""
    if all_ideas:
        # Variable for file saver
        ideas = "\n".join(all_ideas)
        return render_template("history.html", all_ideas=all_ideas, ideas=ideas)
    else:
        return render_template("history.html")


@app.route("/advanced")
def advanced():
    """Render advanced options page"""
    # Convert byte to MB
    max_size = app.config['MAX_CONTENT_LENGTH'] / 1000000
    return render_template("advanced.html", max_size=max_size)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    """Validate uploaded file"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash("No file part.")
            return redirect(url_for('advanced'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash("No file selected.")
            return redirect(url_for('advanced'))
        if file and allowed_file(file.filename) and custom_data(file):
            flash("Your data has been successfully activated.")
            return redirect(url_for('advanced'))
        else:
            flash("Your data file could not be verified!")
            return redirect(url_for('advanced'))
    # Render advanced options page
    return redirect(url_for('advanced'))


@app.errorhandler(413)
def largefile_error(e):
    """Error handling for 413 errors"""
    # Convert byte to MB
    max_size = app.config['MAX_CONTENT_LENGTH'] / 1000000
    flash(f"Maximum file size ({max_size} MB) exceeded.")
    return redirect("/advanced")