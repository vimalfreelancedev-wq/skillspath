# skillspath
Education Platform

Home: select a student from the dropdown or search courses by skill.

Student Dashboard: view enrolled courses, skills, and recommendations.

Course Detail: see course info, required skills, prerequisites, and instructors.

Admin Seed: /admin/seed/ – reload sample data.



# SkillPath – Course Recommendation with Graph Database

A Django app that recommends courses to students based on their skills and prerequisites, using CognoDB (Neo4j) as the graph database.

---

## Quick Setup

### 1. Prerequisites
- Python 3.9+
- A free CognoDB instance ([console.cognodb.com](https://console.cognodb.com/signup)) – save the connection URI and password.

### 2. Clone & enter project
```bash
git clone https://github.com/vimalfreelancedev-wq/skillspath
cd skillpath
```

## 3. Create a .env file
```bash
NEO4J_URI=bolt+s://<your-instance>.databases.cognodb.cloud
NEO4J_USER=cognodb
NEO4J_PASSWORD=<your-password>
NEO4J_DATABASE=neo4j
SECRET_KEY=your-secret-key
```
## 3. Run the below commands one by one
### Installs the dependency -  for creating virtual environment you can use venv or pipenv shell.
```bash
pip install -r requirements.txt
```
### This will load the hard coded data into session. And automatically fetch data from cloud space
```bash
python manage.py seed
```

### For running the django server
```bash
python manage.py runserver
```

