# Fantasy Hockey Flask App - Main entry point
import os
from flaskr import create_app

# Create the app using the factory pattern
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)