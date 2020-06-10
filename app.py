from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "codingisreallyfun0192837465"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def show_survey():
    """Show the survey start page."""

    return render_template('survey.html', survey=survey)


@app.route('/survey', methods=["POST"])
def start_survey():
    """Set the value of the session key 'responses' to an empty list.
    display first survey question."""

    session["responses"] = []
    return redirect('questions/0')


@app.route('/answer', methods=["POST"])
def get_answer():
    """Get the response from the form and add it to the responses list.
       Redirect to the next question. """

    response = request.form["answer"]
    responses = session["responses"]
    responses.append(response)
    session["responses"] = responses

    if (len(responses) == len(survey.questions)):
        # Survey complete. Redirect to the thank-you page
        return redirect('/thank-you')
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:id>')
def run_survey(id):
    """Step through the survey by question.
    Do not allow manual question jumping. """

    responses = session.get("responses")

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect('/thank-you')

    if (id != len(responses)):
        flash(f'Invalid question id: {id}')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template('question.html', id=id, question=question)


@app.route('/thank-you')
def thank_you():
    """Thank the user for taking our survey."""

    return render_template('thank-you.html')
