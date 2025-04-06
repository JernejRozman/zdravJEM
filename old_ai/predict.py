import torch
from PIL import Image
from transformers import AutoImageProcessor  # or AutoFeatureExtractor if you used that
from old_ai.trainModel import MultiHeadViT  # import your model definition

# ==== Load model ====
model_path = "vit_fold3.pt"  # or whichever trained fold you want
vit_model_folder = r"C:\Users\jerne\Desktop\Mind\FRI - LJ\Tekmovanja\Arnesov HackathON\model\vit"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load processor
extractor = AutoImageProcessor.from_pretrained(vit_model_folder)

# Load model & weights
model = MultiHeadViT(vit_model_folder).to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# ==== Load and preprocess image ====
image_path = "testneSlike\\poop1.jpg"  
image = Image.open(image_path).convert("RGB")

inputs = extractor(images=image, return_tensors="pt")
pixel_values = inputs["pixel_values"].to(device)

# ==== Predict ====
with torch.no_grad():
    zdravo_raznoliko_domace, jehrana = model(pixel_values)
    zdravo, raznoliko, domace = zdravo_raznoliko_domace[0].tolist()
    jehrana = jehrana.item()

# ==== Output ====
print("\n Prediction Results:")
print(f" Healthy (zdravo):     {zdravo:.2f}")
print(f" Diverse (raznoliko): {raznoliko:.2f}")
print(f" Homemade (domace):   {domace:.2f}")
print(f" Is food (jehrana):   {'Yes' if jehrana > 0.5 else 'No'} ({jehrana:.2f})")
