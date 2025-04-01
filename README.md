# Kart
====

[![Build Status](https://travis-ci.org/Fresnoy/kart.svg?branch=master)](https://travis-ci.org/Fresnoy/kart)

LeFresnoy's data server.

## Présentation du Fresnoy

## Description de Kart
Kart est la base de données du Fresnoy, elle comporte des informations sur les artistes ainsi que leurs oeuvres.

## Technologies employées
- Python v3.8
- Django v4.1
- Django graphene v3.1
- Django graphQL JWT v0.3
- Psycopg v2.9
- Elasticsearch v7.15
- PostgreSQL

## Prérequis
- Python
- PostgreSQL

## Installation
### 1 - Python
Tout d'abord, installer la version 3.8 de python
```
sudo add-apt-repository ppa:deadsnakes/ppa
```

```
sudo apt install python3.8
```

### 2 - environnement virtuel
Créer un environnement virtuel avec la version 3.8 de Python, par exemple avec venv
```
sudo apt install python3.8-venv
```

```
python3.8 -m venv kart-env
```

Pour activer cet environnement virtuel
```
source kart-env/bin/activate 
```

### 3 - Django
Il faut à présent installer Django dans l'environnement que nous venons de créer
```
python -m pip install Django
```

### 4 - Installation des dépendances
Il est nécessaire d'installer les dépendances listées dans le fichier **requirements.txt**
```
pip install -r requirements.txt
```

### 5 - PostgreSQL
#### 5.1 - Création nde la base de données
Créer une base de données PostgresSQL,
Pour cela, une fois entré dans dans le psql de PostgreSQL:

Créer le futur propriétaire de la base de données
```
CREATE USER mon_utilisateur WITH PASSWORD 'mon_mot_de_passe';
```
Créer la base de donnée et l'assigner à l'utilisateur nouvellement créé
```
CREATE DATABASE ma_base_de_donnees OWNER mon_utilisateur;
```
Donner les privilèges de la base de données à l'utilisateur
```
GRANT ALL PRIVILEGES ON DATABASE ma_base_de_donnees TO mon_utilisateur;
```

- Si vous souhaitez vous connecter
```
sudo -u mon_utilisateur psql -h localhost -d ma_base_de_donnees
```

- Si vous avez un script de base de données, vous pouvez lancer la commande suivante:
```
psql -h localhost -d ma_base_de_donnees -U mon_utilisateur -W < /chemin/vers/le/script
```

#### 5.2 - Définition de la base de données dans django
Tout d'abord, dupliquer le fichier site_settings.py.dev et le renommer site_settings.py

Ensuite, dans le fichier site_settings.py, au niveau des paramètres DATABASE, au lieu de ce code:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'MIRROR': 'test'
        }
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "test.db.pg",
    }
}
```

le modifier par le code suivant:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'django_kart_service',
        },
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "test.db.pg",
    }
}
```
Ensuite, pour ajouter le service. Aller à la racine de votre dossier ou de votre dossier user, trouver ou créer le fichier **.pg_service.conf ** et ajouter le service en modifiant ce fichier:
```
[django_kart_service]
host=localhost
user=mon_utilisateur
dbname=ma_base_de_donnees
password=mon_mot_de_passe
port=5432
```
De retour dans le projet Django, faire les migrations de python
```
python manage.py migrate
```

## Démarrage
Pour lancer l'application, employer la commande suivante:
```
python manage.py runserver
```

## Fonctionnalités

## Contribuer
- git flow