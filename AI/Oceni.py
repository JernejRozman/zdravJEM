#!/usr/bin/env python
"""
Oceni.py: Izvede inferenco na novi sliki s tvojim fine-tunanim ViT modelom (multi-label pristop).
Rezultati bodo vrnjeni v JSON obliki, kjer so ocene vrnjene kot cela števila.
Uporaba:
    python Oceni.py path/to/your/image.jpg
"""

import sys
import torch
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import json

def main(image_path):
    # 1. Naloži fine-tunan model in processor iz Hugging Face.
    model_name = "google/vit-base-patch16-224"
    model = ViTForImageClassification.from_pretrained(model_name)
    processor = ViTImageProcessor.from_pretrained(model_name)

    # Definiramo mapping labelov (v tem primeru le za informacijo, če bi jih potrebovali)
    label_names = ["zdravo", "raznoliko", "domace", "jehrana"]

    # 2. Naloži in predprocesiraj sliko.
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(json.dumps({"error": f"Napaka pri nalaganju slike {image_path}: {e}"}))
        sys.exit(1)

    inputs = processor(images=image, return_tensors="pt")
    
    # 3. Izvedi inferenco.
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits  # Oblika: [1, 4]
    
    # Za prve tri kategorije uporabimo sigmoid, pomnožimo s 100, zaokrožimo in pretvorimo v int.
    continuous_logits = logits[:, :3]
    continuous_scores = torch.sigmoid(continuous_logits)[0] * 100
    continuous_ints = [int(round(score.item())) for score in continuous_scores]
    
    # Za četrto kategorijo ("jehrana") uporabimo sigmoid in prag 0.5 za binarno odločitev.
    binary_logit = logits[:, 3]
    binary_prob = torch.sigmoid(binary_logit)[0]
    binary_pred = 1 if binary_prob > 0.5 else 0

    # 4. Pripravimo rezultate v JSON obliki in jih izpišemo.
    results = {
        "ocene": {
            "zdravo": continuous_ints[0],
            "raznoliko": continuous_ints[1],
            "domace": continuous_ints[2]
        },
        "jehrana": binary_pred
    }
    
    # Izpišemo samo veljaven JSON.
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Uporabi: python Oceni.py path/to/your/image.jpg"}))
        sys.exit(1)
    image_path = sys.argv[1]
    main(image_path)
