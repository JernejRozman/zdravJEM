# %% [markdown]
# # Doučenje modela google/vit-base-patch16-224 za prepoznavanje in ocenjevanje slik hrane

# %% [markdown]
# Učenje poteka po vzorcu na povezavi: https://huggingface.co/learn/cookbook/fine_tuning_vit_custom_dataset#fine-tuning-the-model

# %%
from huggingface_hub import login

my_token = "#####################################"
           
login(token=my_token)


# %% [markdown]
# ### Priprava podatkov

# %% [markdown]
# V tem bloku kode se najprej naloži slikovni nabor podatkov iz mape "./data/images" s pomočjo Hugging Face funkcije load_dataset, pri čemer se stolpec "image" eksplicitno nastavi, da ne dešifrira slik (tako da vsak primer vsebuje le pot do slike). Nato se iz CSV datoteke "./data/metadata.csv" preberejo metapodatki (ocene) za posamezne slike in se zgradi slovar (score_dict), kjer so ključi imena slik, vrednosti pa ocene za kategorije "zdravo", "raznoliko", "domace" in "jehrana". Funkcija add_scores_from_csv nato za vsak primer dobi ime slike iz poti, s tem pridobi ustrezne ocene iz slovarja (če slike ne najde, nastavi ocene na 0) in jih doda v primer. Na koncu se podatki razdelijo na treniranje, validacijo in testiranje, pri čemer se na vsak sklop uporabi ta funkcija, da se vsakemu primeru združijo ustrezni metapodatki – to je potrebno, ker model potrebuje te ročno zapisane ocene za nadaljnjo obdelavo.

# %%
from datasets import load_dataset, DatasetDict, Image, Features, ClassLabel
import pandas as pd
import os

# 1 ustvarimo slovar, ki pove HF: "Ne dekodiraj 'image'."

dataset = load_dataset("imagefolder", data_dir="./data/images")  # By default decodes, but we'll override
dataset = dataset.cast_column("image", Image(decode=False))


# 2) Ustvarimo slovar iz CSV datoteke, ki vsebuje ocene
df_meta = pd.read_csv("./data/metadata.csv")
score_dict = {}
for idx, row in df_meta.iterrows():
    fn = row["file_name"]
    score_dict[fn] = {
        "zdravo":     row["zdravo"],
        "raznoliko":  row["raznoliko"],
        "domace":     row["domace"],
        "jehrana":    row["jehrana"]
    }

# 3) Naredimo funkcijo, ki uporablja 'example["image"]["path"]'
def add_scores_from_csv(example):
    # Zdaj lahko enostavno dostopamo do poti
    path = example["image"]["path"]
    base_name = os.path.basename(path)            # e.g. "zdravaHrana1.jpg"
    file_stem = os.path.splitext(base_name)[0]    # e.g. "zdravaHrana1"

    if file_stem in score_dict:
        example["zdravo"]     = score_dict[file_stem]["zdravo"]
        example["raznoliko"]  = score_dict[file_stem]["raznoliko"]
        example["domace"]     = score_dict[file_stem]["domace"]
        example["jehrana"]    = score_dict[file_stem]["jehrana"]
    else:
        example["zdravo"]     = 0
        example["raznoliko"]  = 0
        example["domace"]     = 0
        example["jehrana"]    = 0

    return example

# 4) Razdelimo podatke na train/validation/test 
split_1 = dataset["train"].train_test_split(test_size=0.2, seed=42)
split_2 = split_1["train"].train_test_split(test_size=0.125, seed=42)  # 10% of remaining 80% is validation

train_ds = DatasetDict({
    "train":      split_2["train"].map(add_scores_from_csv),
    "validation": split_2["test"].map(add_scores_from_csv),
    "test":       split_1["test"].map(add_scores_from_csv)
})

print("Train:", len(train_ds["train"]))
print("Validation:", len(train_ds["validation"]))
print("Test:", len(train_ds["test"]))


# %% [markdown]
# ### Preslikava oznak
# Oznakam priredimo ID, ki se potem ujemajo z imenom. Uporabno za treniranje in ocenjevanje modela.
# 
# 

# %%
label_names = ["zdravo", "raznoliko", "domace", "jehrana"]
label2id = {label: idx for idx, label in enumerate(label_names)}
id2label = {idx: label for label, idx in label2id.items()}


# %%
import numpy as np

def create_multi_hot_label(example):
    # Preberemo stolpce (privzeto 0, če jih ni)
    score_zdravo    = example.get("zdravo", 0)
    score_raznoliko = example.get("raznoliko", 0)
    score_domace    = example.get("domace", 0)
    score_jehrana   = example.get("jehrana", 0)
    
    # Shranimo kot 4-elementni seznam 
    # (lahko je float: 0.0 ali 1.0 - odvisno od tvojih podatkov)
    example["labels"] = [score_zdravo, score_raznoliko, score_domace, score_jehrana]
    
    return example

# Apply the function to every split in your dataset
for split in ["train", "validation", "test"]:
    train_ds[split] = train_ds[split].map(create_multi_hot_label)

# Verify that the "label" field has been added
print(train_ds["train"][0])


# %% [markdown]
# ### Procesiranje slik
# 
# 
# Uporabimo VitImageProcessor, da poenotimo vhod  velikosti slik in jih normaliziramo za že treniran model.
# Definiramo tudi različne transformacije za treniranje, validacijo in testiranje modela, da ga lahko izboljšamo z "torchvision"
# 
# 

# %%
from transformers import ViTImageProcessor

model_name = "google/vit-large-patch16-224"
processor = ViTImageProcessor.from_pretrained(model_name)

# %% [markdown]
# V tem delu se definirajo različne transformacije za trening, validacijo in testiranje: za trening se uporablja naključno prilagajanje velikosti in horizontalno preklapljanje, medtem ko se za validacijo/testiranje slike najprej prilagodijo z Resize in CenterCrop. Nato se slike pretvorijo v tensore in normalizirajo z mean in std vrednostmi, pridobljenimi iz ViTImageProcessorja, kar zagotovi enotno predobdelavo za model.
# 
# 
# 
# 
# 
# 
# 
# 

# %%
from torchvision.transforms import (
    CenterCrop,
    Compose,
    Normalize,
    RandomHorizontalFlip,
    RandomResizedCrop,
    ToTensor,
    Resize,
)

image_mean, image_std = processor.image_mean, processor.image_std
size = processor.size["height"]

normalize = Normalize(mean=image_mean, std=image_std)

train_transforms = Compose(
    [
        RandomResizedCrop(size),
        RandomHorizontalFlip(),
        ToTensor(),
        normalize,
    ]
)
val_transforms = Compose(
    [
        Resize(size),
        CenterCrop(size),
        ToTensor(),
        normalize,
    ]
)
test_transforms = Compose(
    [
        Resize(size),
        CenterCrop(size),
        ToTensor(),
        normalize,
    ]
)

# %% [markdown]
# #### Ustvarjanje transform funkcij
# 
# Implementiramo funkcije za transformacijo podatkov za vse tri datasete. 
# Slike spremenimo v pravilen format in velikost za ViT model.
# 

# %%
def apply_train_transforms(examples):
    examples["pixel_values"] = [train_transforms(image.convert("RGB")) for image in examples["image"]]
    return examples


def apply_val_transforms(examples):
    examples["pixel_values"] = [val_transforms(image.convert("RGB")) for image in examples["image"]]
    return examples


def apply_test_transforms(examples):
    examples["pixel_values"] = [val_transforms(image.convert("RGB")) for image in examples["image"]]
    return examples

# %% [markdown]
# Transformacije uporabimo nad vsakim delom podatkov.
# 

# %%
train_ds["train"].set_transform(apply_train_transforms)
train_ds["validation"].set_transform(apply_val_transforms)
train_ds["test"].set_transform(apply_test_transforms)

# %% [markdown]
# #### Nalaganje podatkov
# 
# Naredimo lastno collate funkcijo, ki ustvari pravilne serije slik in oznak.
# Ustvarimo Dataloader za učinkovito nalaganje in serializacijo med treniranjem modela.
# 

# %%
def collate_fn(examples):
    pixel_values = torch.stack([example["pixel_values"] for example in examples])
    # Vsak example["labels"] je zdaj seznam dolžine 4
    labels = torch.tensor([example["labels"] for example in examples], dtype=torch.float)
    return {"pixel_values": pixel_values, "labels": labels}


# %%
from torch.utils.data import DataLoader

train_dl = DataLoader(train_ds["train"], collate_fn=collate_fn, batch_size=4)

# %% [markdown]
# #### Fine-tuning the Model
# 

# %% [markdown]
# Naložimo model ViTForImageClassification iz predtreniranega modela z naslednjimi nastavitvami: nastavljen je na 4 oznake, uporabljamo multi-label pristop, preslikave med imeni in id-ji oznak so določene s parametri id2label in label2id, ter parameter ignore_mismatched_sizes=True omogoča nalaganje modela, četudi se dimenzije tehtnic ne ujemajo popolnoma.
# 
# 
# 
# 
# 
# 
# 
# 

# %%
from transformers import ViTForImageClassification

model = ViTForImageClassification.from_pretrained(
    model_name,
    num_labels=4,
    problem_type="multi_label_classification",
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)


# %% [markdown]
# Prijavimo se v storitev Weights & Biases (wandb) z uporabo danega ključa, s čimer omogoči spremljanje eksperimentov, treniranja in vizualizacijo metrik med treniranjem modela.
# 
# 

# %% Zakomentiramo za SLURM
#import wandb
#wandb.login(key="########################################")
        


# %% [markdown]
# S pomočjo funkcije cast_column iz knjižnice datasets se stolpec "image" v trenirnem, validacijskem in testnem naboru ponovno pretvori – tokrat se slike dešifrirajo (decode=True), tako da so vsaka slika predstavljena kot pravi PIL objekt, ki se lahko uporabi pri nadaljnji obdelavi (npr. transformacijah in inferenci).

# %%
from datasets import Image

train_ds["train"] = train_ds["train"].cast_column("image", Image(decode=True))
train_ds["validation"] = train_ds["validation"].cast_column("image", Image(decode=True))
train_ds["test"] = train_ds["test"].cast_column("image", Image(decode=True))


# %% [markdown]
# Preverimo celovitost in strukturo trenirnega nabora podatkov s tem, da izpiše število primerov v trenirnem naboru, prikaže en primer za vizualno potrditev pravilne strukture, izpiše nastavitve modela (da ima model pričakovano število izhodnih oznak) ter preveri, ali funkcija za združevanje (collate_fn) pravilno združuje podatke v serije, kar potrdi z izpisom oblik vhodnih slikovnih tenzorjev in oznak.
# 
# 

# %%
import torch

# 1. Preveri če podatki obstajajo
print("Train set size:", len(train_ds["train"]))

# 2. Preveri en primer
print(train_ds["train"][0])

# 3. Preveri ali se število glav modela ujema s številom oznak
print(model.config.num_labels)

# 4. Preveri ali collator vrne pravilne oblike
batch = [train_ds["train"][i] for i in range(4)]
collated = collate_fn(batch)
print(collated["pixel_values"].shape, collated["labels"])


# %% [markdown]
# Naložimo predtreniran model ViTForImageClassification in ga ponovno nastavimo za regresijo, kar pomeni, da se spremeni tip problema (problem_type="regression") in s tem se interna funkcija zgube, ki se uporablja, spremeni (npr. na MSE – srednja kvadratna napaka). Pri tem se model nastavi s štirimi izhodnimi oznakami, kjer se preslikave med imeni in numeričnimi identifikatorji zagotavljajo z id2label in label2id, parameter ignore_mismatched_sizes pa omogoča nalaganje modela tudi v primeru neujemanja dimenzij. Takšna konfiguracija je primerna za regresijske naloge, kjer so vrednosti ne le binarne, temveč zvezne ocene.

# %% [markdown]
# Nato se definirajo parametri za treniranje s pomočjo TrainingArguments, kjer se nastavi izhodna mapa, velikosti batch-ev, število epoch-ov, pogostost logiranja in shranjevanja ter druge možnosti. Nato se ustvari Trainer, ki model poveže z naborom trenirnih in validacijskih podatkov, uporablja definiran data collator (ki združuje podatke v batch-e) in processor kot tokenizer. Na koncu se s klicema trainer.train() in trainer.evaluate() sproži proces treniranja in evalvacije modela.

# %%
from transformers import ViTForImageClassification, Trainer, TrainingArguments


model = ViTForImageClassification.from_pretrained(
    model_name,
    num_labels=4,
    problem_type="regression",  
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True
)


train_args = TrainingArguments(
    output_dir="./vit-checkpoints",
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=4,
    logging_steps=10,
    save_steps=50,
    remove_unused_columns=False,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=train_args,
    train_dataset=train_ds["train"],
    eval_dataset=train_ds["validation"],
    data_collator=collate_fn,
    tokenizer=processor,
)

trainer.train()
trainer.evaluate()



