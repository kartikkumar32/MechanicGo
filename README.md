# 🔧 MechanicGo — Complete Roadside Assistance Platform

A full-stack, feature-rich roadside assistance application built with Flask + MySQL. Users can trigger SOS requests, track mechanics in real-time, and rate their experience.

---

Live Demo: https://ministerchief-mechanicgo.hf.space

Live Demo: https://mechanicgo.onrender.com/


## ✨ Features

### For Car Owners (Users)
- 🚨 **One-tap SOS** — triggers automatic nearest mechanic assignment
- 📍 **Live GPS-based matching** — Haversine formula finds closest available mechanic  
- 🗺️ **Map Integration** — OpenStreetMap embedded for live location display
- 📋 **Request History** — view all past and current requests
- ⭐ **Rate & Review** — star rating system after job completion
- 🔔 **Notifications** — real-time status updates
- 👤 **Profile Management** — update personal info

### For Mechanics
- 🟢 **Online/Offline Toggle** — control availability with one click
- 📍 **Auto Location Sharing** — GPS auto-updates to server
- 📥 **Job Dashboard** — see all assigned requests with customer details
- ▶ **Job Status Updates** — Start → Complete workflow
- 💰 **Earnings Tracker** — per-job earnings summary
- 🔄 **Auto-refresh** — polls for new jobs every 15 seconds

### Admin Console
- 📊 **Analytics Dashboard** — requests over time, issue breakdown charts (Chart.js)
- 👥 **User Management** — view and delete users
- 🔧 **Mechanic Oversight** — monitor all mechanics and their status
- 📋 **Request Management** — change status of any request
- 🔍 **Search & Filter** — real-time table filtering

### Backend / API
- 🔐 **Token-based Auth** — secure session tokens with 7-day expiry
- 🗄️ **Connection Pooling** — MySQL pool of 10 connections
- 🧮 **Haversine Distance** — SQL-based nearest mechanic calculation
- 💳 **Payment Model** — cash/card/UPI support (schema ready)
- 🔒 **Role-based Access** — user / mechanic / admin roles
- 🏗️ **Auto DB Init** — creates all tables on startup

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repo>
cd mechanicgo
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

### 3. Start MySQL & Run
```bash
python app.py
```
App runs at **http://localhost:5000**

---

## 🗺️ Routes

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/dashboard` | User dashboard |
| `/mechanic` | Mechanic portal |
| `/admin` | Admin console |

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register user or mechanic |
| POST | `/api/auth/login` | Login, returns token |
| POST | `/api/auth/logout` | Invalidate session |
| GET | `/api/auth/me` | Current user info |

### SOS & Requests
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sos` | Trigger SOS, auto-assigns mechanic |
| GET | `/api/requests` | List requests (filtered by role) |
| PATCH | `/api/requests/:id/status` | Update request status |

### Mechanics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/mechanics` | List all mechanics |
| POST | `/api/mechanics/location` | Update mechanic GPS |
| PATCH | `/api/mechanics/availability` | Toggle online/offline |

### Ratings & Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ratings` | Submit rating after completion |
| GET | `/api/admin/stats` | Dashboard analytics |
| GET | `/api/admin/users` | All users (admin only) |
| DELETE | `/api/admin/users/:id` | Delete user (admin only) |
| GET | `/api/notifications` | User notifications |

---

## 🔑 Default Admin Account
```
Email:    admin@mechanicgo.com
Password: admin123
```
> Change this in production!

---

## 🗄️ Database Schema

**Tables:** `users`, `sessions`, `mechanics`, `sos_requests`, `ratings`, `notifications`, `payments`

All tables auto-created on first run via `init_db()`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.x, Python |
| Database | MySQL + mysql-connector-python |
| Auth | Token-based (SHA-256) |
| Maps | OpenStreetMap (Leaflet-ready) |
| Charts | Chart.js 4.4 |
| Fonts | Syne + DM Sans (Google Fonts) |
| CSS | Pure CSS custom variables |

---

## 🔧 Production Deployment

```bash
# Use gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Or with nginx reverse proxy
# Point nginx to localhost:8000
```

Set `FLASK_ENV=production` in `.env` for production mode.

---

## 📁 Project Structure

```
mechanicgo/
├── app.py              # Main Flask app with all routes
├── database.py         # DB connection pool & schema init  
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── serviceAccountKey.json  # Firebase (optional)
└── templates/
    ├── index.html      # Landing page
    ├── dashboard.html  # User dashboard
    ├── mechanic.html   # Mechanic portal
    └── admin.html      # Admin console
```
