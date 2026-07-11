# KSP Crime Intelligence Platform

An AI-powered cognitive investigative intelligence platform designed to assist law enforcement agencies (such as Karnataka State Police) in linking cases, analyzing telephone Call Detail Records (CDRs), detecting crime hotspots, mapping syndicates, and evaluating evidence contradictions.

---

## Project Structure

The repository is organized as a monorepo:
* **`/apps/api`**: FastAPI Python backend running the core intelligence APIs, search routing, governance substrate, and intelligence evaluations.
* **`/apps/web`**: React + TypeScript + Vite frontend dashboard showcasing interactive visualizations (network graphs, incident maps, interactive timelines) and the conversational investigation assistant.

---

## Local Setup & Run Guide

To run this platform locally on your machine in VS Code, follow these instructions to launch the Backend and Frontend services simultaneously.

### Prerequisites
Ensure you have the following installed:
* **Node.js** (v18 or higher recommended)
* **Python** (v3.10 or higher recommended)

---

### 1. Launch the Backend (FastAPI)

1. Open your terminal in VS Code and navigate to the API directory:
   ```bash
   cd apps/api
   ```
2. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   * **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   * **Windows (Cmd / PowerShell)**:
     ```cmd
     .\venv\Scripts\activate
     ```
4. Install all python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the FastAPI dev server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   * The API server will be available at [http://localhost:8000](http://localhost:8000)
   * The interactive OpenAPI / Swagger documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 2. Launch the Frontend (React + Vite)

1. Open a **new terminal window** in VS Code and navigate to the web directory:
   ```bash
   cd apps/web
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   * The frontend application will start up at [http://localhost:5173](http://localhost:5173)

---

## Connecting Frontend to Backend

* **Normal Integration Mode**: The web application's [api.ts](apps/web/src/api.ts) automatically routes backend calls to `http://localhost:8000`. You can customize this by creating an `apps/web/.env.local` file:
  ```env
  VITE_API_BASE_URL=http://localhost:8000
  ```
* **Offline Demo Mode**: If you do not have backend services fully configured or connected to a live database, you can log into the frontend using the built-in sandbox demo credentials to preview and evaluate the interactive features (e.g. mock search, case maps, timelines, and network graphs):
  * **Badge Number**: `KSP-ADMIN-001`
  * **Password**: `KspAdmin@2026`
