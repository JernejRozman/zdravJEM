# predict.py
import torch
from PIL import Image
from transformers import AutoImageProcessor
from trainModel import MultiHeadViT
import io

# ==== Load model (do this once when the server starts) ====
model_path = "vit_fold3.pt"
vit_model_folder = r"C:\Users\jerne\Desktop\Mind\FRI - LJ\GitHubRepos\zdravJEM\AI\vit_fold1.pt"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

extractor = AutoImageProcessor.from_pretrained(vit_model_folder)
model = MultiHeadViT(vit_model_folder).to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# ==== Prediction Function ====
def predict(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = extractor(images=image, return_tensors="pt")
    pixel_values = inputs["pixel_values"].to(device)

    with torch.no_grad():
        zdravo_raznoliko_domace, jehrana = model(pixel_values)
        zdravo, raznoliko, domace = zdravo_raznoliko_domace[0].tolist()
        jehrana = jehrana.item()

    return {
        "zdravo": round(zdravo, 2),
        "raznoliko": round(raznoliko, 2),
        "domace": round(domace, 2),
        "jehrana": "Yes" if jehrana > 0.5 else "No",
        "jehrana_score": round(jehrana, 2)
    }
