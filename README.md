# Kart
====

[![Build Status](https://travis-ci.org/Fresnoy/kart.svg?branch=master)](https://travis-ci.org/Fresnoy/kart)

LeFresnoy's data server.

## Présentation - Le Fresnoy
**Le Fresnoy - Studio national des arts contemporains** est une **institution** de **formation**, de **production** et de **diffusion artistiques**, **audiovisuelles** et **numériques**. L’objectif du Studio national est de permettre à de **jeunes créateurs** venus **du monde entier**, de réaliser des **œuvres** avec des **moyens techniques professionnels** et dans un large **décloisonnement** des différents **moyens d’expression**. Le champ de travail, théorique et pratique, est celui de **tous les langages audiovisuels** sur les **supports traditionnels**, **argentiques** et **électroniques** (photographie, cinéma et vidéo) comme sur ceux de la **création numérique**. 

## Description de Kart
**Kart** est l'**API** du **Fresnoy**. **Publique**, elle comporte des **informations liées à l'institution**: les étudiants, les artistes, leurs oeuvres, les expositions etc. Les informations de cette API sont en **français** et en **anglais**.

**Kart** sert principalement pour **Kartel**, l'interface des données du **Fresnoy**.

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

## Démarrage
Pour lancer l'application, employer la commande suivante:
```
python manage.py runserver
```

## Fonctionnalités
Il s'agit d'une **API** en **graphQL** qui permet de consulter les données suivantes:

### Des informations concernant les personnes liées au Fresnoy:
- Le personnel du Fresnoy
    - Permanent
    - Lié à une production
- Les étudiants, classés par cursus
- Les artistes
    - Dont les artistes professeurs
- Des collectifs d'artistes
- Des organisations liées au Fresnoy

On y retrouve pour chaque type de personnes des renseignements le concernant.

En plus de ces données commune, d'autres sont spécifiques au type de personnes:
- Pour les artistes, biographie, pseudonyme et liens vers leur présence en ligne.
- Pour les organisations, une description.

### Les productions du Fresnoy, classées par type:
- Les films
- Les installations
- Les perfomances

Chaque production dispose d'une légende telle qu'on pourrait la lire sur un cartel:
- Titre
- Date
- Images
- Description
- Collaborateurs
- Partenaires
- Auteur
- Remerciements
- Un ensemble de galeries photo classées par thématique:
    - Le processus de création
    - La médiation
    - L'œuvre *in situ*
    - La présence de l'œuvre dans la presse
    - Le teaser de l'œuvre

En plus de ces informations communes, d'autres informations son spécifiques au médium:
- Pour le film, sa durée, son support, son format, ses choix de couleur, son genre et son lieu.
- Pour l'installation, sa description technique et son genre.

Sont également présentes des explications concernant les tâches de chaque corps de métier au sein d'une production.

Les évènements dans lesquels les oeuvres sont passées sont également répertoriés:
- Les festivals
- Les compétitions
- Les projections
- Les vernissages
- Les fêtes
- Les workshop
- Les soirées

Pour chaque évènement sont notés la période ainsi que le lieu.

Les parcours artistiques sont aussi sauvegardés.

### Les diffusions et les récompenses:
Les diffusion peuvent être:
- Mondiales
- Internationales
- Nationales

Est également noté lorsque les oeuvres sont nominées lors d'une compétition

Les récompenses peuvent être:
- Individuelles
- De groupe
- Liées à la carrière
- Autres

### Ce qui est relatif à l'école, son administration
- Les promotions
- Les candidatures d'étudiants

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
A présent, installer Django dans l'environnement que nous venons de créer
```
python -m pip install Django
```

### 4 - Installation des dépendances
Il est nécessaire d'installer les dépendances listées dans le fichier **requirements.txt**
```
pip install -r requirements.txt
```

### 5 - PostgreSQL
#### 5.1 - Création de la base de données
Créer une base de données PostgresSQL.
Pour cela, une fois entré dans dans le **psql** de PostgreSQL:

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

- Si vous disposez d'un fichier de données, vous pouvez l'importer au moyen de la commande suivante:
```
psql -h localhost -d ma_base_de_donnees -U mon_utilisateur -W < /chemin/vers/le/fichier/de/donnees
```

#### 5.2 - Choix de la base de données dans django
Tout d'abord, dupliquer le fichier **site_settings.py.dev** et le renommer **site_settings.py**

Ensuite, dans le fichier **site_settings.py**, au niveau des paramètres **DATABASES**, au lieu de ce code:
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
Ensuite, pour ajouter le service. Aller à la racine de votre dossier ou de votre dossier user, trouver ou créer le fichier **.pg_service.conf** et ajouter le service en modifiant ce fichier:
```
[django_kart_service]
host=localhost
user=mon_utilisateur
dbname=ma_base_de_donnees
password=mon_mot_de_passe
port=5432
```
*Note:* Il est également possible, plutot que d'ajouter ce service, d'intégrer son contenu directement dans le **DATABASES** de **site_settings.py**

De retour dans le projet Django, faire les migrations de python
```
python manage.py migrate
```

## Contribuer
Vous souhaitez contribuer à ce projet?

Toute contribution, qu'elle soit grande ou petite, est la bienvenue. Merci d'avance de nous aider dans l'amélioration de ce projet!

### Comment contribuer?
1. Réaliser un fork du projet
2. Initaliser gitflow
3. Travailler sur votre contribution dans une feature
4. Employer la convention de nommage Angular pour vos commit: https://www.conventionalcommits.org/en/v1.0.0-beta.4/
5. Terminer votre feature
6. Pusher sur votre dépôt
7. Lancer une pull request
8. Retravailler votre contribution si besoin jusqu'à validation de votre contribution

## Licence
 AGPL-3.0 license 