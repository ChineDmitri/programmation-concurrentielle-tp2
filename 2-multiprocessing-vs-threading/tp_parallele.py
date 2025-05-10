import pandas as pd
import time
import multiprocessing as mp
import threading
import csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Partie 1 – Chargement et exploration des données
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    print("Aperçu des données :")
    print(df.head(), "\n")
    return df

# Partie 2 – Entraînement séquentiel
def sequential_training(X_train, y_train):
    start = time.time()
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    duration = time.time() - start
    print(f"Temps séquentiel : {duration:.4f} secondes")
    return duration

# Fonction utilitaire pour multiprocessing et threading
def train_model_dummy(args):
    X, y = args
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

# Partie 3 – Entraînement avec multiprocessing
def multiprocessing_training(X_train, y_train, n_jobs=2):
    start = time.time()
    with mp.Pool(processes=n_jobs) as pool:
        pool.map(train_model_dummy, [(X_train, y_train)] * n_jobs)
    duration = time.time() - start
    print(f"Temps multiprocessing ({n_jobs} processus) : {duration:.4f} secondes")
    return duration

# Classe Thread pour l'entraînement
class TrainingThread(threading.Thread):
    def __init__(self, X, y, durations, index):
        super().__init__()
        self.X = X
        self.y = y
        self.durations = durations
        self.index = index

    def run(self):
        start = time.time()
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(self.X, self.y)
        duration = time.time() - start
        self.durations[self.index] = duration

# Partie 4 – Entraînement avec threading
def threading_training(X_train, y_train, n_threads=2):
    durations = [0] * n_threads
    threads = []
    start = time.time()
    for i in range(n_threads):
        t = TrainingThread(X_train, y_train, durations, i)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    total_duration = time.time() - start
    print(f"Temps threading ({n_threads} threads) : {total_duration:.4f} secondes")
    return total_duration, durations

# Partie 5 – Comparaison des performances et export en CSV
def compare_and_export(csv_input, csv_output):
    df = load_data(csv_input)
    X = df.drop(columns=["trip_duration"])
    y = df["trip_duration"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    t_seq = sequential_training(X_train, y_train)
    t_mp = multiprocessing_training(X_train, y_train, n_jobs=2)
    t_thr, thr_durations = threading_training(X_train, y_train, n_threads=2)

    # Export des résultats
    with open(csv_output, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Méthode", "Durée (s)"])
        writer.writerow(["Séquentiel", f"{t_seq:.4f}"])
        writer.writerow(["Multiprocessing (2)", f"{t_mp:.4f}"])
        writer.writerow(["Threading (2)", f"{t_thr:.4f}"])

    print(f"\nRésultats exportés dans {csv_output}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Étude de cas : Multiprocessing vs Threading")
    parser.add_argument("--input", type=str, default="traffic_data.csv", help="Chemin vers traffic_data.csv")
    parser.add_argument("--output", type=str, default="results.csv", help="Chemin vers le fichier de résultats CSV")
    args = parser.parse_args()

    compare_and_export(args.input, args.output)
