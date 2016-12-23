import pandas as pd
import logging
from sklearn.externals import joblib
from gensim.similarities.docsim import MatrixSimilarity 
import pickle

from flask import Flask

# create logger for app
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

app = Flask(__name__)
app.config.from_object("app.config")

# unpickle my model

highlights = pd.read_csv('models/Highlights.csv', header = None)

business = pd.read_csv('models/Business.csv', index_col=0)

mat_index = MatrixSimilarity.load('models/similar_vec')

# review_vec = None
# with open('models/review_vec.pkl', 'rb') as f:
#     review_vec = pickle.load(f)

from .views import *   # flake8: noqa


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
