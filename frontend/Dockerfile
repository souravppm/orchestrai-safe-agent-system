# Frontend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# সরাসরি ফ্রন্টএন্ডের প্যাকেজগুলো ইন্সটল করছি (No dependency on root requirements.txt)
RUN pip install --no-cache-dir streamlit requests

# ফ্রন্টএন্ড ফোল্ডারটা কপি করছি
COPY frontend/ /app/frontend/

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
