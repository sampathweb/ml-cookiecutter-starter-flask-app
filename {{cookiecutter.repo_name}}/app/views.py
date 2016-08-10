import logging
import json

from flask import render_template
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required

from . import app, MODELS

logger = logging.getLogger('app')

class PredictForm(Form):
    """Fields for Predict"""
    sepal_length = fields.DecimalField('Sepal Length:', places=2, validators=[Required()])
    sepal_width = fields.DecimalField('Sepal Width:', places=2, validators=[Required()])
    petal_length = fields.DecimalField('Petal Length:', places=2, validators=[Required()])
    petal_width = fields.DecimalField('Petal Width:', places=2, validators=[Required()])

    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    predicted_iris = None
    data = []

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data
        logger.info(submitted_data)

        # Retrieve values from form
        sepal_length = float(submitted_data['sepal_length'])
        sepal_width = float(submitted_data['sepal_width'])
        petal_length = float(submitted_data['petal_length'])
        petal_width = float(submitted_data['petal_width'])

        # Build the X values in the same order expected by model or how model is trained
        flower_instance = [sepal_length, sepal_width, petal_length, petal_width]

        iris = MODELS["iris"]
        estimator, target_names = iris["estimator"], iris["target_names"]

        my_predictions = estimator.predict([flower_instance])
        # predictions is also an Array with a predition for each row of our 2-D Array
        # We are only passing one row for prediction, so index it to get the first element
        my_prediction = my_predictions[0]

        # Lookup the predicted Index on target Names to get the Predicted iris species
        predicted_iris = target_names[my_prediction].capitalize()
        data = [flower_instance]

    return render_template('index.html',
        form=form,
        prediction=predicted_iris,
        data=json.dumps(data))
