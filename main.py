from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

@app.route("/")
def root():
    return "Hello world"

def load_vehicle_data():
    with open('vehicles.json', 'r') as f:
        data = json.load(f)
    return data

def save_vehicle_data(data):
    with open('vehicles.json', 'w') as f:
        json.dump(data, f, indent=2)

telemetry_data = {}

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicle_data = load_vehicle_data()
    return jsonify(vehicle_data)

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    new_vehicle = request.get_json()
    required_fields = ['vin', 'manufacturer', 'model', 'fleet_id', 'owner_operator', 'registration_status']
    if not all(field in new_vehicle for field in required_fields):
        return jsonify({'error': 'Missing required vehicle fields'}), 400

    vehicles = load_vehicle_data()
    if any(v['vin'] == new_vehicle['vin'] for v in vehicles):
        return jsonify({'error': 'Vehicle with this VIN already exists'}), 400

    vehicles.append(new_vehicle)
    save_vehicle_data(vehicles)
    return jsonify(new_vehicle), 201

@app.route('/vehicles/<vin>', methods=['PUT'])
def update_vehicle(vin):
    update_data = request.get_json()
    vehicles = load_vehicle_data()
    for vehicle in vehicles:
        if vehicle['vin'] == vin:
            vehicle.update(update_data)
            save_vehicle_data(vehicles)
            return jsonify(vehicle)
    return jsonify({'error': 'Vehicle not found'}), 404

@app.route('/vehicles/<vin>', methods=['DELETE'])
def delete_vehicle(vin):
    vehicles = load_vehicle_data()
    for i, vehicle in enumerate(vehicles):
        if vehicle['vin'] == vin:
            del vehicles[i]
            save_vehicle_data(vehicles)
            return jsonify({'message': 'Vehicle deleted'})
    return jsonify({'error': 'Vehicle not found'}), 404

@app.route('/telemetry/<vin>', methods=['POST'])
def receive_telemetry(vin):
    data = request.get_json()
    required_fields = ['gps', 'speed', 'engine_status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing telemetry data fields'}), 400

    vehicles = load_vehicle_data()
    if not any(v['vin'] == vin for v in vehicles):
        return jsonify({'error': 'Vehicle not found'}), 404

    entry = {
        'gps': data['gps'],  
        'speed': data['speed'], 
        'engine_status': data['engine_status']  
    }
    if vin not in telemetry_data:
        telemetry_data[vin] = []
    telemetry_data[vin].append(entry)
    return jsonify({'message': 'Telemetry data received'}), 201

from flask import send_from_directory, abort

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory('static', filename)
    except FileNotFoundError:
        abort(404)

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Route not found'}), 404

if __name__ == '__main__':
    app.run()

