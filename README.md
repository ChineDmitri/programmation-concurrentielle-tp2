# Projet de Serveur Multi-Thread avec MySQL

Ce projet met en place un serveur HTTP multi-thread en Python qui interagit avec une base de données MySQL exécutée dans un conteneur Docker.

## Structure du Projet

```
Parallelism/
├── .env                            # Variables d'environnement
├── docker-compose.yml              # Configuration Docker
├── multi-thread-server-python/
│   ├── app.py                     # Serveur HTTP multi-thread
│   └── requirements.txt           # Dépendances Python
├── fake-server-java/               # Serveur Java pour l'API REST
│   ├── src/                       # Code source Java
│   │   └── main/java/com/parallelism/fake/init/DataInitializer.java  # Initialisation auto des données
│   ├── pom.xml                    # Configuration Maven
│   └── Dockerfile                 # Configuration Docker pour Java
└── README.md                       # Documentation
```

## Prérequis

- Docker et Docker Compose installés
- Python 3.6+ 

## Installation

1. Clonez ce dépôt sur votre machine locale :

   ```bash
   git clone https://github.com/ChineDmitri/programmation-concurrentielle-tp2.git
   cd programmation-concurrentielle-tp2
   ```

2. Démarrez les conteneurs MySQL et le serveur Java (Spring Framework) :

   ```bash
   docker-compose up -d
   ```

   > **Note**: Le serveur Java Spring initialise automatiquement la base de données avec les utilisateurs de test grâce au composant `DataInitializer.java`.

3. Installez les dépendances Python nécessaires :

   ```bash
   cd multi-thread-server-python
   pip install -r requirements.txt
   ```

## Démarrage du Serveur

Pour lancer le serveur HTTP multi-thread, exécutez :

```bash
cd multi-thread-server-python # si vous n'êtes pas déjà dans ce répertoire
python app.py
```

Le serveur démarrera sur le port 8080.

## Variables d'environnement

Le projet utilise un fichier `.env` pour configurer la connexion à la base de données MySQL. Voici les variables disponibles :

- `MYSQL_ROOT_PASSWORD` : Mot de passe de l'utilisateur root MySQL
- `MYSQL_DATABASE` : Nom de la base de données
- `MYSQL_USER` : Nom d'utilisateur MySQL
- `MYSQL_PASSWORD` : Mot de passe de l'utilisateur MySQL

## Utilisation

Le serveur expose l'API suivante :

- `GET /user/{id}` - Récupère les informations d'un utilisateur par son ID

Exemple de requête :

```bash
curl http://localhost:8080/user/1
```

## Fonctionnement

1. Le serveur reçoit une requête pour obtenir les informations d'un utilisateur
2. Il récupère les données de base de l'utilisateur depuis la base de données MySQL
3. Il enrichit ces données en appelant l'API REST Java sur le port 8081
4. Il renvoie une réponse JSON combinant toutes ces informations

## Arrêt du Projet

Pour arrêter les conteneurs :

```bash
docker-compose down
```

## Dépannage

### Problèmes de connexion à MySQL

Si vous rencontrez des erreurs de connexion à MySQL, essayez de redémarrer le conteneur :

```bash
# Arrêter le conteneur MySQL
docker container stop mysql-tp2-ordonnancement

# Supprimer le conteneur MySQL
docker container rm mysql-tp2-ordonnancement

# Redémarrer tous les services
docker-compose up -d
```

### Problèmes avec le serveur Java

Si le serveur Java rencontre des problèmes :

```bash
# Arrêter le conteneur Java
docker container stop java-fake-server

# Supprimer le conteneur Java
docker container rm java-fake-server

# Redémarrer uniquement le serveur Java
docker-compose up -d java-app
```

### Erreur "Access denied for user"

Si vous rencontrez une erreur d'accès refusé pour l'utilisateur MySQL :

```bash
# Accéder à MySQL et configurer les permissions
docker exec -i mysql-tp2-ordonnancement mysql -uroot -prootpassword << EOF
CREATE USER IF NOT EXISTS 'springuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON userdb.* TO 'springuser'@'%';
FLUSH PRIVILEGES;
EOF
```

### Réinitialisation complète

Pour réinitialiser complètement l'environnement (supprime toutes les données) :

```bash
# Arrêter tous les conteneurs et supprimer les volumes
docker-compose down -v

# Recréer et démarrer tous les conteneurs
docker-compose up -d
```

## Architecture

Ce projet démontre un exemple de parallélisme à travers :
- Un serveur HTTP multi-thread en Python qui peut gérer plusieurs requêtes simultanément
- Une connexion à une base de données MySQL 
- Des appels à une API REST via le serveur Java Spring Boot

Chaque requête client est traitée dans un thread séparé, permettant une exécution parallèle.

## Dépôt Git

Le code source de ce projet est disponible sur GitHub :
[https://github.com/ChineDmitri/programmation-concurrentielle-tp2.git](https://github.com/ChineDmitri/programmation-concurrentielle-tp2.git)