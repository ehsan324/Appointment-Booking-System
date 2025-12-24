# 📘 Appointment Booking API

A **production-ready backend** built with **Django REST Framework**, **PostgreSQL**, **Docker**, **JWT authentication**, **GitHub Actions CI**, and a **layered (service-layer) architecture**.

---

## 🚀 Features

- Django REST Framework + PostgreSQL  
- JWT Authentication (access/refresh)  
- Role-based permissions (**CLIENT**, **PROVIDER**)  
- Booking domain with full business rules  
- `BookingService` (Clean / service-layer architecture)  
- Time slot management with availability engine  
- Docker + docker-compose setup  
- GitHub Actions CI (tests + Postgres service)  
- Rate limiting (Login + Booking creation)  
- CORS configuration (per environment)  
- Custom exception handler (standardized error format)  
- Fully documented API using OpenAPI / Swagger  
- Production-ready settings (security, logging, env-based config)

---

## 🐳 Running with Docker

```bash
cp .env.example .env
docker compose up --build
```

### Local URLs

- **App:** http://localhost:8000  
- **Swagger:** http://localhost:8000/api/docs/swagger/  
- **Redoc:** http://localhost:8000/api/docs/redoc/

---

## 🔐 Auth

JWT-based authentication:

- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`

### Example header

```http
Authorization: Bearer <access_token>
```

---

## 📚 API Documentation

- **OpenAPI schema:** `/api/schema/`
- **Swagger UI:** `/api/docs/swagger/`
- **Redoc:** `/api/docs/redoc/`

---

## 🧠 Architecture Overview

```text
services/     → business logic (BookingService, SlotService…)
views/        → thin DRF controllers
serializers/  → validation + mapping
permissions/  → role-based access
throttles/    → rate limiting
core/         → shared logic (exception handler, health, permissions)
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

CI runs automatically on every push.

---

## 🧰 Technologies

- Django & DRF  
- PostgreSQL  
- Docker / docker-compose  
- JWT (simplejwt)  
- drf-spectacular (OpenAPI)  
- GitHub Actions CI  
- CORS middleware  
- Rate limiting  
- Python 3.11

---

## 📛 CI Badge


```markdown
![CI](https://github.com/<YOUR_GITHUB_USERNAME>/<REPO_NAME>/actions/workflows/ci.yml/badge.svg)
```
