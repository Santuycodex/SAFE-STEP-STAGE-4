from flask import Flask, request, jsonify
app = Flask(__name__)
latest_data = {'lat': 0, 'lng': 0}

@app.route('/gps', methods=['POST'])
def gps():
    global latest_data
    data = request.get_json()
    latest_data = data
    return jsonify({"status": "received"})

@app.route('/data', methods=['GET'])
def data():
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
