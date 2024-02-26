from flask import Flask, request, jsonify, render_template
import pandas as pd
from ydata_profiling import ProfileReport
import os

app = Flask(__name__)

def Report_Generator(df):
    profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
    profile.to_file("result.html")


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_csv(file)
    df = df.dropna()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    df.to_csv('data.csv', index=False)
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/report', methods=['GET'])
def report():
    df = pd.read_csv('data.csv')
    Report_Generator(df)
    os.rename('result.html', 'templates/result.html')
    return jsonify({'message': 'Report generated successfully'})

@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
