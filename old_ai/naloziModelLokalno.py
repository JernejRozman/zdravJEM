import os
from transformers import AutoModel, AutoFeatureExtractor

#############################################
# 1: NALAGANJE MODELA NA LOKALNO RAČUNALNIK #
#############################################


# STEP 1: Set Hugging Face cache path
custom_hf_cache = r"C:\Users\jerne\Desktop\Mind\FRI - LJ\Tekmovanja\Arnesov HackathON\model"
os.environ["HF_HOME"] = custom_hf_cache

# STEP 2: Choose your image model
model_id = "google/vit-base-patch16-224"

# STEP 3: Download model and feature extractor (for images!)
print("🔄 Downloading model and feature extractor...")
model = AutoModel.from_pretrained(model_id)
extractor = AutoFeatureExtractor.from_pretrained(model_id)

# STEP 4: Save locally
target_path = os.path.join(custom_hf_cache, "vit")
model.save_pretrained(target_path)
extractor.save_pretrained(target_path)

print(f"✅ Model and extractor saved to: {target_path}")
