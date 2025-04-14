import os
import torch
import numpy as np
import pandas as pd
from PIL import Image as PilImage
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from sklearn.metrics import recall_score
from transformers import ViTForImageClassification, ViTImageProcessor

# ------------------------------------------------------------------
# 1. Naloži fine-tunan model in procesor iz checkpoint-a.
# To je bilo narejeno, za lokalni model, ki je bil shranjen v ./vit-checkpoints/checkpoint-50.	
checkpoint_path = "./vit-checkpoints/checkpoint-68"
model = ViTForImageClassification.from_pretrained(checkpoint_path)
processor = ViTImageProcessor.from_pretrained(checkpoint_path)

# ------------------------------------------------------------------
# 2. Nastavi transformacije za validacijo.
size = processor.size["height"]
normalize = Normalize(mean=processor.image_mean, std=processor.image_std)
val_transform = Compose([
    Resize(size),
    CenterCrop(size),
    ToTensor(),
    normalize,
])

# ------------------------------------------------------------------
# 3. Naloži datoteko metadata.csv.
meta_df = pd.read_csv('./data/metadata.csv')

# Pripravi sezname za shranjevanje dejanskih oznak in napovedi.
true_labels_list = []
pred_labels_list = []

# Nastavi model v evalvacijski način.
model.eval()

# ------------------------------------------------------------------
# 4. Obdelaj vsako sliko, pridobi napovedi modela in shrani dejanske oznake.
with torch.no_grad():
    for idx, row in meta_df.iterrows():
        # Pridobi ime slike (npr. "zdravaHrana1")
        file_name = row['file_name']
        # Sestavi celotno pot do slike (po potrebi prilagodi končnico)
        img_path = os.path.join('./data/images', f"{file_name}.jpg")
        if not os.path.exists(img_path):
            print(f"Slika ne obstaja: {img_path}")
            continue
        
        # Odpri sliko in uporabi transformacije za validacijo.
        image = PilImage.open(img_path).convert('RGB')
        input_tensor = val_transform(image).unsqueeze(0)  # dodaj dimenzijo za batch
        
        # Izvedi naprejni prenos skozi model.
        outputs = model(input_tensor)
        logits = outputs.logits.squeeze(0)  # oblika: [4]
        
        # Pretvori logite v verjetnosti z uporabo sigmoid funkcije (multi-label primer).
        probabilities = torch.sigmoid(logits).cpu().numpy()
        # Pretvori napovedi v binarno obliko: uporabi prag 0.5.
        preds = (probabilities > 0.5).astype(int)
        pred_labels_list.append(preds)
        
        # Pretvori dejanske vrednosti v binarno obliko:
        # Za "zdravo", "raznoliko" in "domace" uporabi prag 50, "jehrana" je že binarna.
        true = np.array([
            1 if row['zdravo'] >= 50 else 0,
            1 if row['raznoliko'] >= 50 else 0,
            1 if row['domace'] >= 50 else 0,
            int(row['jehrana'])
        ])
        true_labels_list.append(true)

# Pretvori sezname v NumPy polja.
true_labels = np.array(true_labels_list)  # oblika: (št_primerov, 4)
pred_labels = np.array(pred_labels_list)  # oblika: (št_primerov, 4)

# ------------------------------------------------------------------
# 5. Izračunaj in izpiši recall vrednosti za vsako kategorijo.
label_names = ["zdravo", "raznoliko", "domace", "jehrana"]

for i, label in enumerate(label_names):
    rec = recall_score(true_labels[:, i], pred_labels[:, i], average='binary')
    print(f"Recall za {label}: {rec:.2f}")
