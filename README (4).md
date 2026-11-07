# 🚆 Supervision embarquée du CVS — Locomotive E1100 (ONCF)

> Prototype de **surveillance et de diagnostic en temps réel** du Convertisseur Auxiliaire Statique (CVS) des locomotives électriques **E1100 (3000 V CC)**, réalisé lors d'un stage à l'**ONCF — Établissement de Maintenance Industrielle de Safi (EMIS)**.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![MQTT](https://img.shields.io/badge/MQTT-660066?style=for-the-badge&logo=mqtt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

## 🎯 Contexte

Les avaries du CVS (modules IGBT, cartes de commande ESBX2, allumeurs) provoquent des arrêts non programmés des locomotives. Ce projet propose une démarche de **maintenance conditionnelle** : simuler les mesures du CVS, les transmettre en temps réel, détecter automatiquement les anomalies et les afficher sur un tableau de bord.

## 🏗️ Architecture

```
Simulateur CVS ──MQTT──▶ Broker Mosquitto ──▶ mqtt_subscriber.py
 (Publisher)                                   │  (diagnostic des seuils)
                                               ▼
                                        Base SQLite
                                (tables : measurements, alarms)
                                               │
                                               ▼
                                      API REST FastAPI (:8000)
                                               │
                                               ▼
                                   Dashboard React (:5173)
```

| Composant | Rôle |
|---|---|
| **Simulateur CVS** | Génère périodiquement les mesures selon un scénario sélectionnable |
| **Broker MQTT (Mosquitto)** | Transport léger Publish/Subscribe |
| **Subscriber + moteur de diagnostic** | Reçoit les mesures, applique les règles, produit les états et alarmes |
| **SQLite** | Persistance des mesures et des alarmes |
| **API FastAPI** | Accès JSON aux données pour l'interface |
| **Dashboard React** | Supervision visuelle de l'état du CVS |

## 🔍 Diagnostic automatique

Trois états globaux : **NORMAL**, **WARNING**, **CRITICAL**.

| Grandeur | Avertissement | Critique |
|---|---|---|
| Tension d'entrée | — | < 2700 V (CVS-001) · > 3300 V (CVS-002) |
| Température IGBT | > 85 °C | > 100 °C |
| Courant | > 90 A | > 100 A |
| Tension de sortie | — | < 350 V · > 430 V |
| Vibrations | > 4 | — |
| Rendement | < 90 % | < 85 % |
| Ventilation | — | T > 85 °C et ventilateur arrêté (CVS-008) |

## 🔌 API REST

| Endpoint | Fonction |
|---|---|
| `/api/health` | Vérification du service |
| `/api/measurements/latest` | Dernière mesure |
| `/api/measurements` | Historique des mesures |
| `/api/alarms` | Liste des alarmes |
| `/api/alarms/latest` | Dernière alarme |
| `/api/statistics` | Statistiques |
| `/api/simulation/scenario` | Scénario actif |
| `/api/simulation/scenario/{scenario}` | Changement du scénario |

## ▶️ Lancer le projet

> ⚠️ Adaptez les noms de fichiers et dossiers à ceux de votre projet.

```bash
# 1. Broker MQTT
mosquitto

# 2. Backend (dans le dossier du backend)
pip install -r requirements.txt
# lancer le subscriber, le simulateur, puis l'API :
uvicorn main:app --reload --port 8000

# 3. Dashboard (dans le dossier du frontend)
npm install
npm run dev     # http://localhost:5173
```

## 🔭 Perspectives

Exploiter l'historique stocké dans SQLite pour entraîner des modèles de **maintenance prédictive**.

## 👤 Auteur

**Bader Alouli** — Master Ingénierie Informatique et Systèmes Embarqués, Université Ibn Zohr (Agadir)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bader-alouli-ab30a9278/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:baderalouli04@gmail.com)
