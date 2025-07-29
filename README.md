# 💊 AI-Powered Dose Lookup — Hinckley Medical Assignment

This project demonstrates a complete AI-powered system to extract and retrieve medical protocol doses using natural language queries. Built to fulfill the Hinckley Medical technical assignment.

---

## 🚀 Live Deployment

**Backend API**: [https://hinckley-backend-production.up.railway.app](https://hinckley-backend-production.up.railway.app)  
**Health Check**: `GET /`  
Response:  
```json
{"status": "✅ Server is up and running"}
```

---

## 🧠 Features

- Query dosage using natural language prompts like:  
  `Administer Epinephrine under Trauma Protocol`
- OpenAI API used to extract structured medication + protocol
- Async PostgreSQL querying for medication doses
- Frontend interface using simple HTML + Bootstrap + JS
- Supports real-time query and response

---

## 🏗️ Architecture

```
User → Frontend → OpenAI → FastAPI → PostgreSQL → Response
```

See architecture diagram in the PDF submission.

---

## 🧪 Sample Prompts

1. `Administer Epinephrine under Trauma Protocol`
2. `What is the dose for Ibuprofen in Fever Protocol?`

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python) + asyncpg
- **Database**: PostgreSQL (via Railway)
- **AI/NLP**: OpenAI Chat Completion API
- **Frontend**: HTML + Bootstrap + JS
- **Deployment**: Railway

---

## 📂 Folder Structure

```
hinckley-backend/
├── app/
│   ├── db.py
│   ├── routes/
│   │   └── ask.py
│   └── prompt_parser.py
├── main.py
├── .env
├── index.html
├── requirements.txt
└── README.md
```

---

## 📝 Notes

- Developed in < 24 hours post working hours.
- Optimized for clarity, structure, and maintainability.
- Meant to show initiative, real-world understanding, and thoughtful architecture.

For more details, refer to the PDF report in this submission.
