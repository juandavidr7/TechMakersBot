# Proyecto: Chatbot con Backend y Frontend

Este proyecto integra un backend desarrollado con **FastAPI** y un frontend construido con **Next.js** y **React**, utilizando **Tailwind CSS** para los estilos.  
El backend maneja datos estaticos en **JSON** y usa **LangChain** y la **API** de OPENAI para mejorar la generación de respuestas del chatbot.

## 📌 Requisitos

Asegúrate de tener instalado en tu sistema:

✅ **Python 3.11** (para el backend)  
✅ **Node.js 18+ y npm o yarn** (para el frontend)

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el Repositorio

```sh
git clone https://github.com/juandavidr7/TechMakersBot.git
cd TechMakersBot

```

2️⃣ Iniciar el Backend (FastAPI)
📌 El backend usa FastAPI, almacena datos en JSON y está configurado en http://127.0.0.1:8092.

Si deseas ejecutar el backend manualmente:

```sh
cd BackEnd
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8092 --reload
```
✅ El backend se ejecutará en: http://127.0.0.1:8092
✅ Para probar la API, abre en tu navegador: http://127.0.0.1:8092/docs

3️⃣ Iniciar el Frontend (Next.js)
📌 El frontend está desarrollado con Next.js y React, y utiliza Tailwind CSS o Bootstrap.

Para ejecutarlo:
```sh
cd frontend
npm install  # o yarn install
npm run dev  # o yarn dev
```
✅ El frontend se ejecutará en: http://localhost:3000

4️⃣ Configurar la Conexión entre el Frontend y el Backend
📌 El frontend debe comunicarse con el backend en el puerto 8092.

Si hay errores de conexión, revisa dónde se define la API en el frontend 

📌 API Endpoints
Para explorar la API, visita:

🔹 http://127.0.0.1:8092/docs

🔹 Ejemplo de solicitud al chatbot (usando curl):
```sh
curl -X POST "http://127.0.0.1:8092/chatbot/" \
     -H "Content-Type: application/json" \
     -d '{"query": "¿Qué laptops ASUS tienen en stock?"}'

```

