from flask import Flask, request, jsonify
import maxminddb
import ipaddress

app = Flask(__name__)

GEOIP_DB_PATH = './country.mmdb'

@app.route('/', methods=['GET'])
def check_ip():
    try:
        country = "Unknown"
        
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        client_ip = client_ip.split(',')[0].strip()

        if not client_ip:
            return jsonify({"error": "Invalid IP address"}), 500
        
        ip_obj = ipaddress.ip_address(client_ip)
        
        if not isinstance(ip_obj, ipaddress.IPv4Address):
            return jsonify({"error": "Only IPv4 addresses are supported"}), 404
        
        with maxminddb.open_database(GEOIP_DB_PATH) as reader:
            response = reader.get(client_ip)
            if response is not None:
                country = response['country']

        return jsonify({"ip": client_ip, "country": country}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
