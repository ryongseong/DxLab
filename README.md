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