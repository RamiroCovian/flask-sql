import os
from flask import Flask


RUTA = os.path.join("balance", "data", "balance.db")
app = Flask(__name__)
app.config.from_prefixed_env()
