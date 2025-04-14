#!/bin/bash
#SBATCH --job-name=vit-finetune         # Ime dela
#SBATCH --output=out_%j.txt              # Izhodni log
#SBATCH --error=err_%j.txt               # Log napak
#SBATCH --time=02:00:00                  # Najdaljši čas izvajanja (2 uri)
#SBATCH --partition=standard             # Ime particije (prilagodi glede na razpoložljivost)
#SBATCH --nodes=1                        # Število nodov
#SBATCH --ntasks=1                       # Število opravil na nod
#SBATCH --cpus-per-task=4                # Število CPU jeder
#SBATCH --gres=gpu:1                     # Zahteva eno GPU (prilagodi glede na sistem)

# Naloži modul Python 3 
module load python/3

# Aktiviraj virtualno okolje 
source venv/bin/activate

# Zaženi Python skripto (npr. vaše "your_script.py", če je notebook pretvorjen v .py)
python TrainModelSLURM.py
