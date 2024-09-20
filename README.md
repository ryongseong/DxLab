### Run Methods
1. Download Docker Desktop Application
2. put the necessary files and directories in place
3. command "docker-compose up --build"
5. command "docker-compose run web alembic revision --autogenerate"
6. command "docker-compose run web alembic upgrade head"
7. Go to "http://localhost:8000/docs"
- signup
- find post /exam methods and login with your username and password
- execute that api
8. If you want to show Web Application, go to "http://localhost:3000"

### Directory Structure

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