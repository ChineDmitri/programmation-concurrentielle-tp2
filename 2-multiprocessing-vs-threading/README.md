# Étude de cas 2 : Multiprocessing vs Threading

Ce projet compare les temps d’entraînement d’un modèle RandomForest en mode séquentiel, multiprocessing et threading.

## Prérequis

- Python 3.8 ou supérieur  
- pip (installé par défaut avec Python)

## Installation

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. érifiez que tp_parallele.py et traffic_data.csv sont bien dans le même dossier.

2. Lancer le script :
```bash 
python tp_parallele.py --input traffic_data.csv --output results.csv
```

3. Ouvrez results.csv pour consulter les durées d’entraînement :
exemple 
```csv
Méthode,Durée (s)
Séquentiel,0.0417
Multiprocessing (2),0.0568
Threading (2),0.0945
```