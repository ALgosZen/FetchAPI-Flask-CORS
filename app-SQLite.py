from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize Flask app and configure SQLite URI
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Define the User model (Table in SQLite)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

# Initialize the database (create the table)
@app.before_request
def create_tables():
    db.create_all()

@app.route('/save', methods=['POST'])
def save_user():
    try:
        # Get the JSON data from the frontend
        data = request.get_json()

        # Extract user information from the received data
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        phone_number = data.get('phoneNumber')

        if not all([first_name, last_name, phone_number]):
            return jsonify({'message': 'Invalid input'}), 400

        # Create a new User instance
        new_user = User(first_name=first_name, last_name=last_name, phone_number=phone_number)

        # Add the user to the database and commit
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User saved successfully!'}), 200
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500

@app.route('/')
def index():
    return "Flask with SQLite is working!"

if __name__ == '__main__':
    app.run(debug=True, port=5010)
