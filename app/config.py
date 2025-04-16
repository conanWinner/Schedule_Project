import os
import torch

class Config:
    MODEL_PATH = os.environ.get("MODEL_PATH", "conanWinner/model_scheduler")
    MAX_SOURCE_LENGTH = int(os.environ.get("MAX_SOURCE_LENGTH", "350"))
    MAX_TARGET_LENGTH = int(os.environ.get("MAX_TARGET_LENGTH", "1024"))
    DEVICE = os.environ.get("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
    NUM_BEAMS = int(os.environ.get("NUM_BEAMS", "4"))

    # Cấu hình server
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", "5000"))
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

    # Sử dụng FP16 để tiết kiệm bộ nhớ nếu sử dụng GPU
    USE_FP16 = os.environ.get("USE_FP16", "True").lower() == "true" and DEVICE == "cuda"


