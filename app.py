import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    bot_response = get_rasa_response(user_message)
    return jsonify(response=bot_response)

def get_rasa_response(message):
    rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"  # Replace with your Rasa server URL
    payload = {
        "sender": "user",
        "message": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(rasa_server_url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            return response_data[0].get("text", "I didn't understand that.")
        else:
            return "I didn't get a response from the bot."
    else:
        return "Failed to connect to Rasa server."

if __name__ == '__main__':
    app.run(debug=True)
