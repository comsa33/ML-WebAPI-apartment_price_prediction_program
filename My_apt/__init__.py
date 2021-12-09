from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

def create_app(config=None):
    app = Flask(__name__)
    
    # 여기에서 주어진 config 에 따라 추가 설정을 합니다.
    if config is not None:
        app.config.update(config)
    
    from My_apt.views.main_views import main_bp

    app.register_blueprint(main_bp)

    return app
    

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)