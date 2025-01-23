import re
import requests
import socket
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

def is_valid_ip(ip):
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    return bool(re.match(pattern, ip))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
    

@app.route('/ipinfo', methods=['GET'])
def get_ip_info():
    
    ip = request.args.get('ip', request.remote_addr)

    try:
        if not is_valid_ip(ip):
            ip = socket.gethostbyname(ip)
    except socket.gaierror:
        return render_template('index.html', error=f"Invalid Domain {ip}"), 400
    
    api = f'https://ipinfo.io/{ip}/json/'

    try:
        response = requests.get(api)
        response.raise_for_status()
        ipinfo = response.json()
        return render_template('index.html', ipinfo=ipinfo)  # ✅ Pass data to template
    except requests.RequestException:
        return render_template('index.html', error="Unable to Fetch the IP Details"), 500

if __name__ == "__main__":
    app.run(debug=True)
