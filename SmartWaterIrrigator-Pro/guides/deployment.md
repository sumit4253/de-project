# Deployment Guide

This guide covers deploying the Smart Water Irrigator to platforms like Render or Railway.

## Prerequisites
- A GitHub repository containing this code.
- An account on Render (render.com) or Railway (railway.app).
- A managed MySQL database (e.g., PlanetScale, Aiven, or a MySQL addon on your deployment platform).

## Deploying to Render

1. Create a new Web Service on Render and link your GitHub repository.
2. In the "Build Command" field, enter: `pip install -r requirements.txt`
3. In the "Start Command" field, enter: `gunicorn app:app` (Make sure to add `gunicorn` to your `requirements.txt` before pushing to GitHub).
4. Add your Environment Variables:
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (pointing to your managed MySQL database).
   - `OPENWEATHERMAP_API_KEY` (your API key).
   - `SECRET_KEY` (a strong random string).
5. Click "Create Web Service".

## Deploying to Railway

1. Click "New Project" -> "Deploy from GitHub repo".
2. Select your repository.
3. Railway will automatically detect the `requirements.txt` and build the Python environment.
4. Go to Variables and add your `.env` variables (DB credentials, API keys).
5. (Optional) You can provision a MySQL database directly within the Railway project and link it easily by copying the connection credentials into your variables.
6. The service will deploy automatically on port 5000 (or the port defined by Railway's `$PORT` variable). To handle `$PORT` correctly, update `app.run()` in `app.py` or use gunicorn as the start command.
