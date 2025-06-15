# tg-init-backend

FastAPI backend for Telegram sticker pack initData validation and payment processing.

## Setup & Deploy

### Prerequisites
- Python 3.9+
- Git
- Render account connected to GitHub

### Local Setup

```bash
git clone https://github.com/hansellf/tg-init-backend.git
cd tg-init-backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Deploy to Render

1. Push your local repo to GitHub (if not done):

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/hansellf/tg-init-backend.git
git push -u origin main
```

2. Go to [Render](https://render.com) dashboard.
3. Click **New Web Service**.
4. Connect GitHub and select `tg-init-backend` repo.
5. Set build command:

```bash
pip install -r requirements.txt
```

6. Set start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

7. Deploy. Render auto-deploys on every push to `main`.

---

## API

- `GET /init-data`: Returns JSON with sticker init data.

---

## License

MIT
