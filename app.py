from flask import Flask, render_template, request, url_for, redirect, Markup
from datetime import datetime
import csv
import os

app = Flask(__name__)

@app.route('/')
def form():
	return "Nightcore Generation"

if __name__ == '__main__':
	app.run(debug=True)
