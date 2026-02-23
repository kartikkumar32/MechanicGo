# 🔧 MechanicGo — Complete Roadside Assistance Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey.svg?logo=flask&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg?logo=mysql&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-black?logo=render&logoColor=white)
![Railway](https://img.shields.io/badge/Database-Railway-black?logo=railway&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A full-stack, feature-rich roadside assistance application built with Flask and MySQL. MechanicGo connects stranded drivers with the nearest available mechanics using real-time GPS tracking and automated dispatching.

---

### 🌐 Live Demos
- **Main Demo:** [https://mechanicgo.onrender.com/](https://mechanicgo.onrender.com/)
- **Alternative Demo:** [https://ministerchief-mechanicgo.hf.space](https://ministerchief-mechanicgo.hf.space)

---

## ✨ Key Features

### 🚗 For Car Owners (Users)
- 🚨 **One-tap SOS:** Triggers automatic nearest mechanic assignment.
- 📍 **Live GPS-based Matching:** Uses the Haversine formula to find the closest available mechanic.
- 🗺️ **Map Integration:** Embedded OpenStreetMap for live location tracking.
- ⭐ **Rate & Review:** Star rating system after job completion.
- 🔔 **Real-time Notifications:** Status updates from dispatch to completion.

### 🔧 For Mechanics
- 🟢 **Availability Toggle:** Control online/offline status with one click.
- 📍 **Auto Location Sharing:** Seamlessly updates server with live coordinates.
- 📥 **Job Dashboard:** View assigned requests, customer details, and map routes.
- ▶ **Workflow Management:** Update job status (Start → In Progress → Complete).
- 💰 **Earnings Tracker:** Per-job earnings summary.

### 👑 Admin Console
- 📊 **Analytics Dashboard:** Visual charts (Chart.js) for requests over time and issue breakdown.
- 👥 **User & Mechanic Management:** View, monitor, and manage all platform participants.
- 📋 **Global Request Oversight:** View and override the status of any active request.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask 3.x
- **Database:** MySQL (Deployed on Railway) + `mysql-connector-python` with connection pooling
- **Frontend:** HTML5, CSS3, Vanilla JS, Chart.js 4.4, OpenStreetMap
- **Authentication:** Custom token-based Auth (SHA-256 hashed passwords)
- **Deployment:** Render (Web Service) + Railway (MySQL Database)

---

## 🚀 Local Setup Instructions

### 1. Clone the Repository
```bash
git clone [https://github.com/username/mechanicgo.git](https://github.com/username/mechanicgo.git)
cd mechanicgo

```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env_example .env

```

Edit the `.env` file with your local or remote MySQL credentials:

```env
SECRET_KEY=generate_a_random_secure_string_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=mechanicgo
DB_PORT=3306
FLASK_ENV=development

```

### 4. Run the Application

The database tables will automatically initialize on the first run.

```bash
python app.py

```

App runs at **http://localhost:5000**

---

## ☁️ Deployment Guide

### Step 1: Deploy MySQL Database on Railway

1. Go to [Railway.app](https://railway.app/) and sign in.
2. Click **New Project** -> **Provision PostgreSQL/MySQL/Redis** -> Select **MySQL**.
3. Wait a few seconds for the database to provision.
4. Click on the newly created MySQL card, go to the **Connect** tab.
5. Note down the following credentials (you will need them for Render):
* **Host** (e.g., `xxxxxxx.proxy.rlwy.net`)
* **Port** (e.g., `23921`)
* **User** (usually `root`)
* **Password**
* **Database Name** (usually `railway`)



### Step 2: Deploy Flask App on Render

1. Go to [Render.com](https://render.com/) and sign in.
2. Click **New** -> **Web Service**.
3. Connect your GitHub repository (`username/mechanicgo`).
4. Fill in the deployment settings:
* **Name:** `mechanicgo`
* **Environment:** `Python 3`
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn app:app`


5. Scroll down to **Environment Variables** and add the variables from your Railway setup:
* `SECRET_KEY`: (Create a secure random string)
* `DB_HOST`: (Paste Railway Host)
* `DB_USER`: (Paste Railway User)
* `DB_PASSWORD`: (Paste Railway Password)
* `DB_NAME`: (Paste Railway DB Name)
* `DB_PORT`: (Paste Railway Port)
* `FLASK_ENV`: `production`


6. Click **Create Web Service**. Render will now build and deploy your app.

---

## 🗄️ Database Schema

The platform automatically generates the following tables on startup:

* `users`: Stores all user, mechanic, and admin profiles.
* `sessions`: Manages token-based authentication.
* `mechanics`: Stores specific mechanic data (specialty, live location, rating).
* `sos_requests`: Handles all dispatch tickets and statuses.
* `ratings`: User reviews for completed jobs.
* `notifications`: In-app alerts for users.
* `payments`: Tracks transaction statuses.

---

## 🔑 Default Admin Account

A default admin account is created automatically upon database initialization.

* **Email:** `admin@mechanicgo.com`
* **Password:** `admin123`

> ⚠️ *Important: Change this password immediately after deploying to production!*

---

## 🔌 Core API Routes

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Register a new user or mechanic |
| `POST` | `/api/auth/login` | Login to receive a session token |
| `POST` | `/api/sos` | Trigger an SOS to the nearest mechanic |
| `GET` | `/api/requests` | List requests (role-filtered) |
| `PATCH` | `/api/requests/:id/status` | Update the state of a job |
| `POST` | `/api/mechanics/location` | Update mechanic's live GPS coordinates |
| `GET` | `/api/admin/stats` | Fetch system-wide analytics (Admin) |

---

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
