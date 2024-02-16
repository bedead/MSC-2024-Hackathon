# @author Satyam Mishra


from flask import Flask
from routes.__config__ import DevConfig, ProdConfig


def create_app():
    name = "KarmaYogi"
    # performance and error monitoring
    app = Flask(name, instance_relative_config=False)
    # selecting config file for application to run
    # Basic config, Dev, and Prod
    app.config.from_object(DevConfig)

    with app.app_context():
        # Import parts of our application
        from .__home__ import base_page_bp
        from .auth.__auth__ import auth_page_bp
        from .dashboards.__main__ import dashboard_page

        # Register Blueprints
        app.register_blueprint(base_page_bp)
        app.register_blueprint(dashboard_page)
        app.register_blueprint(auth_page_bp)

        # returning app
        return app
