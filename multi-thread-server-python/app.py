import json
import threading
import mysql.connector
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import requests
import os
from dotenv import load_dotenv

# Chemin vers le fichier .env dans le répertoire parent
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')

# Vérification que le fichier .env existe avant de le charger
if os.path.exists(env_path):
    print(f"Chargement des variables d'environnement depuis {env_path}")
    load_dotenv(env_path)
else:
    print(f"Attention: Fichier .env non trouvé à {env_path}")
    print("Utilisation des valeurs par défaut pour la connexion MySQL")

# Configuration de la connexion MySQL avec l'utilisateur root pour éviter les problèmes d'autorisation
db_config = {
    "host": "localhost",
    "user": "root", # Utiliser root au lieu de springuser
    "password": os.getenv("MYSQL_ROOT_PASSWORD", "rootpassword"),
    "database": os.getenv("MYSQL_DATABASE", "userdb")
}

print(f"Configuration de la base de données: {db_config}")


# Handler HTTP multi-threads
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/user/"):
            user_id = self.path.split("/")[-1]
            # 1- Récupérer l'utilisateur depuis MySQL
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if not user:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"User not found")
                    return
                    
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
                return
                
            # 2- Récupérer des infos supplémentaires depuis l'API PHP
            try:
                api_url = f"http://localhost:8081/api/users/{user['email']}"
                print(user)
                print(api_url)
                response = requests.get(api_url)
                api_data = response.json() if response.status_code == 200 else {}
                print(api_data)
                # 3- Combiner et renvoyer les données
                user.update(api_data.get("data", {}))
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(user).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"API Error: {str(e)}".encode())
        else:
            # Route par défaut
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


# Lancement du serveur multi-threads
def run_server(port=8080):
    server_address = ("", port)
    httpd = ThreadingHTTPServer(server_address, MyRequestHandler)
    print(f"Serveur en cours d'exécution sur le port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
