## Run Methods

### Docker-Environment Methods
1. Download Docker Desktop Application
2. put the necessary files and directories in place
3. command "docker-compose up --build"
4. command "docker-compose run web alembic revision --autogenerate"
5. command "docker-compose run web alembic upgrade head"
6. Go to "http://localhost:8000/docs"
- signup
  <br>
  <img width="300" alt="스크린샷 2024-09-20 17 45 52" src="https://github.com/user-attachments/assets/c7a05e0b-8699-4a57-a7c8-973c97c53b94">
- find post /exam methods and login with your username and password
  <br>
  <img width="300" alt="스크린샷 2024-09-20 17 48 44" src="https://github.com/user-attachments/assets/dc0b6c24-4d50-41c5-9842-6d2a00baaf4b">
  <img width="100" alt="스크린샷 2024-09-20 17 51 44" src="https://github.com/user-attachments/assets/eb862105-9b29-454d-8467-ad8832bb0e4a">
  <br>
  <img width="400" alt="스크린샷 2024-09-20 17 48 53" src="https://github.com/user-attachments/assets/c09947db-d5e1-415d-97f8-4effbb05f941">
- execute that api
7. If you want to show Web Application, go to "http://localhost:3000"

### Local-Environment Methods
1. Download Python v3.10
2. install pip libraries
3. Install Ollama
4. Ollama pull llama3.1
5. command "uvicorn model_server:app --host 0.0.0.0 --port 8001"

## Directory Structure

      DXLAB / Main Directory
      ├── data / Data Directory - Hidden
      │
      ├── domain / Backend Directory
      │   ├── exam / Exam Directory - crud.py, schema.py, router.py
      │   ├── gemini / Gemini Directory - crud.py, schema.py, router.py
      │   ├── user / User Directory - crud.py, schema.py, router.py
      │   └── question / Question Directory - crud.py, schema.py, router.py
      │
      ├── frontend
      │   ├── src
      │   │   ├── components / For Error, Header
      │   │   ├── lib / API, Auth, Store 
      │   │   ├── routes / Pages Directory
      │   │   ├── App.svelte / Connect Routers
      │   │   └── main.js / Connect App
      │   │
      │   ├── .env / Environment - server_url, Hidden
      │   ├── Dockerfile / Build Nginx Server Template
      │   ├── .gitignore
      │   ├── nginx.conf / Control Nginx Server
      │   └── package.json / npm Libraries
      │
      ├── migration
      │
      ├── .env / Environment - API Keys, Hidden
      ├── alembic.ini / Initialize DB
      ├── database.py / Initialize DB
      ├── docker-compose.yml / Connect Docker Server - fastapi, svelte, postgresql 
      ├── Dockerfile / Build Fastapi Server Template
      ├── main.py / Control Fastapi Server
      ├── model_server.py / Control Server for Using GPU
      ├── models.py / For Setting Query Language
      └── requirements.txt / pip Libraries
