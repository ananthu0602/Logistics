from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

EXCEL_FILE = 'trucks.xlsx'

@app.route('/')
def home():
    return render_template("Logistics.html")  #
# Create Excel file with headers if not present
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["vin", "model", "year", "capacity", "charges", "notes"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/api/trucks', methods=['POST'])
def add_truck():
    data = request.get_json()
    df = pd.read_excel(EXCEL_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    return jsonify({"status": "success"}), 201

@app.route('/api/trucks', methods=['GET'])
def get_trucks():
    df = pd.read_excel(EXCEL_FILE)
    return jsonify(df.to_dict(orient="records"))

@app.route('/api/download', methods=['GET'])
def download_excel():
    try:
        return send_file(
            EXCEL_FILE,
            as_attachment=True,
            download_name='trucks.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
