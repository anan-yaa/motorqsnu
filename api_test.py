import requests

BASE_URL = "http://127.0.0.1:5000"

def test_get_vehicles():
    response = requests.get(f"{BASE_URL}/vehicles")
    print("GET /vehicles:", response.status_code, response.json())

def test_post_vehicle():
    new_vehicle = {
        "vin": "9999999",
        "manufacturer": "TestMaker",
        "model": "TestModel",
        "fleet_id": "99",
        "owner_operator": "Test Owner",
        "registration_status": "Active"
    }
    response = requests.post(f"{BASE_URL}/vehicles", json=new_vehicle)
    print("POST /vehicles:", response.status_code, response.json())

def test_put_vehicle():
    update_data = {
        "registration_status": "Maintenance"
    }
    response = requests.put(f"{BASE_URL}/vehicles/9999999", json=update_data)
    print("PUT /vehicles/9999999:", response.status_code, response.json())

def test_delete_vehicle():
    response = requests.delete(f"{BASE_URL}/vehicles/9999999")
    print("DELETE /vehicles/9999999:", response.status_code, response.json())

def test_post_telemetry():
    telemetry_data = {
        "gps": {"latitude": 37.7749, "longitude": -122.4194},
        "speed": 60,
        "engine_status": "On"
    }
    response = requests.post(f"{BASE_URL}/telemetry/8345774", json=telemetry_data)
    print("POST /telemetry/8345774:", response.status_code, response.json())

if __name__ == "__main__":
    test_get_vehicles()
    test_post_vehicle()
    test_put_vehicle()
    test_post_telemetry()
    test_delete_vehicle()
