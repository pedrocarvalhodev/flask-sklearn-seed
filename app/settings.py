import os

# 2 dir back to main (flask-sklearn-seed) and then 
MODELS_ROOT = os.path.abspath(__file__ + "/../../app/models")
DATA_ROOT = os.path.abspath(__file__ + "/../../data/raw")
LOG_FILE = os.path.abspath(__file__ + "/../../data/application.log")
PORT = 8080
