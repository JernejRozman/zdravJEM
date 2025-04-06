import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, Subset
from sklearn.model_selection import KFold
import pandas as pd
from PIL import Image
from transformers import AutoModel, AutoFeatureExtractor
from tqdm import tqdm

# ==== Paths ====
csv_path = r"C:\Users\jerne\Desktop\Mind\FRI - LJ\Tekmovanja\Arnesov HackathON\labels.csv"
img_dir = r"C:\Users\jerne\Desktop\Mind\FRI - LJ\Tekmovanja\Arnesov HackathON\slike"
model_path = r"C:\Users\jerne\Desktop\Mind\FRI - LJ\Tekmovanja\Arnesov HackathON\model\vit"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==== Dataset ====
class FoodDataset(Dataset):
    def __init__(self, csv_path, img_dir, extractor):
        self.df = pd.read_csv(csv_path)
        self.img_dir = img_dir
        self.extractor = extractor

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(self.img_dir, row["imageName"] + ".jpg")
        image = Image.open(img_path).convert("RGB")
        inputs = self.extractor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"].squeeze(0)

        zdravo = row["zdravo"] / 100.0
        raznoliko = row["raznoliko"] / 100.0
        domace = row["domace"] / 100.0
        jehrana = row["jehrana"]

        regression_targets = torch.tensor([zdravo, raznoliko, domace], dtype=torch.float)
        binary_target = torch.tensor(jehrana, dtype=torch.float)

        return pixel_values, regression_targets, binary_target

# ==== Model ====
class MultiHeadViT(nn.Module):
    def __init__(self, model_path):
        super().__init__()
        self.backbone = AutoModel.from_pretrained(model_path)
        hidden_size = self.backbone.config.hidden_size

        self.reg_head = nn.Sequential(
            nn.Linear(hidden_size, 3),   # zdravo, raznoliko, domace
            nn.Sigmoid()
        )
        self.bin_head = nn.Sequential(
            nn.Linear(hidden_size, 1),   # jehrana
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.backbone(pixel_values=x).last_hidden_state[:, 0]
        reg_out = self.reg_head(x)
        bin_out = self.bin_head(x).squeeze(1)
        return reg_out, bin_out

# ==== Training ====
def train_one_epoch(model, loader, opt, loss_fn_reg, loss_fn_bin):
    model.train()
    total_loss = 0
    for x, y_reg, y_bin in loader:
        x, y_reg, y_bin = x.to(device), y_reg.to(device), y_bin.to(device)
        opt.zero_grad()
        out_reg, out_bin = model(x)
        loss = loss_fn_reg(out_reg, y_reg) + loss_fn_bin(out_bin, y_bin)
        loss.backward()
        opt.step()
        total_loss += loss.item()
    return total_loss / len(loader)

def evaluate(model, loader, loss_fn_reg, loss_fn_bin):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for x, y_reg, y_bin in loader:
            x, y_reg, y_bin = x.to(device), y_reg.to(device), y_bin.to(device)
            out_reg, out_bin = model(x)
            loss = loss_fn_reg(out_reg, y_reg) + loss_fn_bin(out_bin, y_bin)
            total_loss += loss.item()
    return total_loss / len(loader)

# ==== MAIN ====
def main():
    print("🔬 Loading extractor and data...")
    extractor = AutoFeatureExtractor.from_pretrained(model_path)
    full_dataset = FoodDataset(csv_path, img_dir, extractor)

    kf = KFold(n_splits=3, shuffle=True, random_state=42)
    EPOCHS = 10
    BATCH_SIZE = 4

    for fold, (train_idx, val_idx) in enumerate(kf.split(full_dataset)):
        print(f"\n🔁 Fold {fold+1}")
        train_ds = Subset(full_dataset, train_idx)
        val_ds = Subset(full_dataset, val_idx)
        train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)

        model = MultiHeadViT(model_path).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
        loss_reg = nn.MSELoss()
        loss_bin = nn.BCELoss()

        for epoch in range(EPOCHS):
            train_loss = train_one_epoch(model, train_loader, optimizer, loss_reg, loss_bin)
            val_loss = evaluate(model, val_loader, loss_reg, loss_bin)
            print(f"Epoch {epoch+1:02d} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

        torch.save(model.state_dict(), f"vit_fold{fold+1}.pt")
        print(f"💾 Model saved: vit_fold{fold+1}.pt")

if __name__ == "__main__":
    main()
