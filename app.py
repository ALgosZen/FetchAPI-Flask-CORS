from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

@app.route('/save', methods=['POST'])
def save_user():
    data = request.get_json()

    first_name = data.get('firstName')
    last_name = data.get('lastName')
    phone_number = data.get('phoneNumber')

    if not all([first_name, last_name, phone_number]):
        return jsonify({'message': 'Invalid input'}), 400

    # Save data to a temporary file
    with open('temp_users.txt', 'a') as file:
        file.write(f'{first_name},{last_name},{phone_number}\n')

    return jsonify({'message': 'User saved successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5010)
