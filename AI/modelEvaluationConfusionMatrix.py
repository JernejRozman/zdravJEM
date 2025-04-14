import os
import torch
import numpy as np
import pandas as pd
from PIL import Image as PilImage
import matplotlib.pyplot as plt
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from transformers import ViTForImageClassification, ViTImageProcessor

# Naloži model in processor iz checkpoint-a.
# To je bilo narejeno, za lokalni model, ki je bil shranjen v ./vit-checkpoints/checkpoint-50.	
checkpoint_path = "./vit-checkpoints/checkpoint-68"
model = ViTForImageClassification.from_pretrained(checkpoint_path)
processor = ViTImageProcessor.from_pretrained(checkpoint_path)

# Nastavi transformacije za validacijo.
size = processor.size["height"]
normalize = Normalize(mean=processor.image_mean, std=processor.image_std)
val_transform = Compose([
    Resize(size),
    CenterCrop(size),
    ToTensor(),
    normalize,
])

# Naloži metapodatke.
meta_df = pd.read_csv('./data/metadata.csv')

true_labels_list = []
pred_labels_list = []
model.eval()

with torch.no_grad():
    for idx, row in meta_df.iterrows():
        file_name = row['file_name']
        img_path = os.path.join('./data/images', f"{file_name}.jpg")
        if not os.path.exists(img_path):
            print(f"Slika ne obstaja: {img_path}")
            continue
        image = PilImage.open(img_path).convert('RGB')
        input_tensor = val_transform(image).unsqueeze(0)
        outputs = model(input_tensor)
        logits = outputs.logits.squeeze(0)
        probabilities = torch.sigmoid(logits).cpu().numpy()
        preds = (probabilities > 0.5).astype(int)
        pred_labels_list.append(preds)
        true = np.array([
            1 if row['zdravo'] >= 50 else 0,
            1 if row['raznoliko'] >= 50 else 0,
            1 if row['domace'] >= 50 else 0,
            int(row['jehrana'])
        ])
        true_labels_list.append(true)

true_labels = np.array(true_labels_list)
pred_labels = np.array(pred_labels_list)

label_names = ["zdravo", "raznoliko", "domace", "jehrana"]
for i, label in enumerate(label_names):
    cm = confusion_matrix(true_labels[:, i], pred_labels[:, i])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f"Confusion Matrix for '{label}'")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()
