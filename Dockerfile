FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV PORT 8505
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port", "8505", 
"--server.enableCORS", "false"]
cat Dockerfile
gcloud builds submit --tag gcr.io/digital-vim-471122-t5/empathy-app .
gcloud auth revoke
gcloud auth application-default login


