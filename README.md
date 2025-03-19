# 📊 DataViewer - Django, Prefect & Celery

## 📌 Description
DataViewer est une application Django qui permet d'entrer une URL, d'extraire les données de la page web (paragraphes, tableaux, images) et de les structurer en datasets exploitables. L'application utilise **Prefect** pour l'orchestration des workflows et **Celery** pour le traitement asynchrone.

## 🚀 Fonctionnalités
- ✅ **Saisie d'une URL** pour extraction de données.
- 📄 **Récupération des paragraphes** avec leur titre associé.
- 📊 **Extraction des tableaux** et conversion en dataset.
- 🖼️ **Téléchargement des images** et stockage.
- ⚡ **Traitement asynchrone** avec Celery.
- 🎯 **Orchestration avec Prefect**.
- 📂 **Export des datasets en CSV ou JSON**.

## 🛠️ Technologies Utilisées
- **Django** - Framework web principal.
- **BeautifulSoup** - Parsing des pages HTML.
- **Pandas** - Manipulation des données extraites.
- **Prefect** - Orchestration des workflows.
- **Celery** - Exécution des tâches en arrière-plan.
- **Redis** - Broker de messages pour Celery.
- **PostgreSQL** - Base de données principale.

## ⚙️ Installation

### 1️⃣ Prérequis
Assurez-vous d'avoir installé :
- **Python 3.9+**
- **Docker & Docker Compose** *(optionnel mais recommandé)*

### 2️⃣ Cloner le projet
```bash
git clone https://github.com/votre-repo/dataviewer.git
cd dataviewer
```

### 3️⃣ Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Mac/Linux
venv\Scripts\activate  # Sur Windows
```

### 4️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5️⃣ Configurer la base de données
Dans `settings.py`, configurez PostgreSQL :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dataviewer_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Appliquez les migrations :
```bash
python manage.py migrate
```

### 6️⃣ Lancer les services
**Lancer Django** :
```bash
python manage.py runserver
```

**Lancer Redis (si nécessaire)** :
```bash
docker run -d -p 6379:6379 redis
```

**Lancer Celery** :
```bash
celery -A dataviewer worker --loglevel=info
```

**Lancer Prefect Server** *(optionnel si vous utilisez Prefect Cloud)* :
```bash
prefect server start
```

## 📌 Utilisation
1. Accédez à **`http://127.0.0.1:8000`**.
2. Saisissez une URL.
3. L'application **parse la page** et affiche les paragraphes, tableaux et images.
4. Les données extraites sont **converties en datasets** et exportables en **CSV/JSON**.

## 🛠️ API REST
Le projet expose une API permettant d'envoyer une URL et de récupérer les datasets extraits.

### 🔹 **Envoyer une URL pour extraction**
```http
POST /api/extract/
```
**Exemple de payload** :
```json
{
    "url": "https://fr.wikipedia.org/wiki/M%C3%A9canique_quantique"
}
```

### 🔹 **Récupérer un dataset**
```http
GET /api/dataset/1/
```

### Development 
#### NPM 
```bash
npm init
npm install webpack webpack-cli --save-dev
npm run build (production)
npm run dev (development)
```


## 📜 Licences & Contribution
Projet open-source sous licence **MIT**. Contributions bienvenues ! 🚀

## 📧 Contact
Pour toute question ou suggestion, contactez-nous sur **contact@dataviewer.com**.

