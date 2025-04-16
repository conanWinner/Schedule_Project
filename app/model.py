import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from app.config import Config

class TextToJSONModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = Config.DEVICE

    def load(self):
        try:
            print(f"Loading tokenizer from {Config.MODEL_PATH}...")
            self.tokenizer = T5Tokenizer.from_pretrained(Config.MODEL_PATH)

            print(f"Loading model from {Config.MODEL_PATH}...")
            if Config.USE_FP16:
                self.model = T5ForConditionalGeneration.from_pretrained(
                    Config.MODEL_PATH,
                    torch_dtype=torch.float16
                )
            else:
                self.model = T5ForConditionalGeneration.from_pretrained(Config.MODEL_PATH)

            self.model.to(self.device)

            self.model.eval()

            print(f"Model loaded successfully. Using device: {self.device}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def predict(self, text):
        if self.model is None or self.tokenizer is None:
            return {"success": False, "error": "Model not loaded"}

        try:
            inputs = self.tokenizer(
                text,
                max_length=Config.MAX_SOURCE_LENGTH,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )

            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_length=Config.MAX_TARGET_LENGTH,
                    num_beams=Config.NUM_BEAMS,
                    early_stopping=True
                )

            prediction = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
            prediction = prediction.replace(self.tokenizer.pad_token, "").replace(self.tokenizer.unk_token, "").replace(self.tokenizer.eos_token, "").strip()

            try:
                json_result = json.loads(prediction)
                return {"success": True, "result": json_result}
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Model output is not valid JSON",
                    "raw_output": prediction
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

model_instance = TextToJSONModel()
