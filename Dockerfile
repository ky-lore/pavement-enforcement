# Static site only: the server serves the generated public/ folder and never handles leads.
FROM python:3.12-alpine
WORKDIR /srv
ENV PYTHONUNBUFFERED=1
COPY server.py ./
COPY public ./public
EXPOSE 8080
CMD ["python", "server.py"]
