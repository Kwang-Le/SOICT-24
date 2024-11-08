from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from .detect import detect_violations

app = Flask(__name__)
swagger = Swagger(app)

# Example endpoint with Swagger documentation
@app.route('/api/detect_violations', methods=['POST'])
@swag_from({
    'description': 'get violation detections from website',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'url': {
                        'type': 'string',
                        'example': 'https://example.com',
                        'description': 'url for the website to detect violations'
                    },
                },
                'required': ['url']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'List of cookies and their corresponding labels',
            'examples': {
                'application/json': {
                    'message': 'Request successfull',
                    'data': [
                            {
                                'cookie_1': 'Advertising'
                            },
                            {
                                'cookie_2': 'Analytics'
                            }
                    ]
                }
            }
        },
        400: {
            'description': 'Invalid request payload'
        }
    }
})
def example_endpoint():
    # Get JSON data from the request
    data = request.get_json()
    print(data)

    # Validate the data
    if not data or 'url' not in data:
        return jsonify({'error': 'Invalid request payload'}), 400

    detect_violations(data['url'])
    
    # Respond with the received data
    return jsonify({
        'message': 'Data received',
        'data': data
    }), 200
