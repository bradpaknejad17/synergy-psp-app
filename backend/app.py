from flask import Flask, jsonify
from flask_cors import CORS

from .repository.db import init_db


def create_app():
    app = Flask(__name__)
    # Initialize DB (create tables)
    init_db()

    # Enable CORS for API routes (development)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from .api.resources.psp import bp as psp_bp
    from .api.resources.tasks import bp as tasks_bp
    app.register_blueprint(psp_bp)
    app.register_blueprint(tasks_bp)

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'})

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
