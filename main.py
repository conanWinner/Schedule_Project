from app import create_app
from app.model import model_instance
from app.config import Config

if __name__ == '__main__':
    # Tạo ứng dụng Flask
    app = create_app()
    
    # Load mô hình trước khi khởi động server
    print("Loading model...")
    if model_instance.load():
        # Chạy server sau khi đã load mô hình
        print(f"Starting server on {Config.HOST}:{Config.PORT}...")
        app.run(
            host=Config.HOST, 
            port=Config.PORT, 
            debug=Config.DEBUG
        )
    else:
        print("Failed to load model. Exiting.")
