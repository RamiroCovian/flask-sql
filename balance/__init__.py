import os
from flask import Flask


app = Flask(__name__)

RUTA = os.path.join("balance", "data", "balance.db")
