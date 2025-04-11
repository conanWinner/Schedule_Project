from sentence_transformers import SentenceTransformer

def load_model():
    # Load mô hình Sentence Transformer để tạo embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model
