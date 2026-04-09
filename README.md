<div align="center">
  <h1>🚀 OrchestrAI: Enterprise-Grade Safe AI Agent System</h1>
  <p>A production-ready, zero-hallucination AI agent architecture designed to execute critical backend operations with human-in-the-loop safety and full auditability.</p>

  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
  [![OpenAI](https://img.shields.io/badge/Brain-GPT--4o--mini-412991.svg?style=flat&logo=openai&logoColor=white)](https://openai.com/)
  [![Redis](https://img.shields.io/badge/State-Redis-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io/)
  [![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
  
</div>

---

## 🧠 The Problem It Solves

Traditional LLM chatbots hallucinate data and cannot be trusted to execute sensitive business operations (e.g., modifying databases, processing refunds, cancelling orders). **OrchestrAI** solves this by decoupling the "thinking" from the "acting".

The LLM is strictly used as a reasoning engine (Intent & Extraction) via **Function Calling**, while actual execution happens through highly-validated, schema-strict internal APIs overseen by a central Orchestrator.

## 🎯 Core Capabilities

* **Multi-Step Agentic Reasoning:** Uses a `Plan → Act → Observe → Decide` loop. The agent independently queries backend states (e.g., checking order status) before executing complex logical requests.
* **Human-in-the-Loop (Safety First):** Sensitive actions trigger a strict confirmation workflow. The system pauses execution, stores the state in memory, and waits for explicit user confirmation.
* **Zero-Hallucination Execution:** The LLM does not generate final execution queries. It strictly calls predefined backend tools validated via Pydantic schemas.
* **Stateful Memory Management:** Uses **Redis** for distributed state management, handling pending actions and conversation context without overloading the client UI.
* **100% Observability:** Every internal tool call, observation, and system decision is recorded in a PostgreSQL Audit Log.

---

## 🏗️ System Architecture

```text
User Input 
   │
   ▼
[ Streamlit UI ] (Stateless Client)
   │
   ▼
[ FastAPI Backend ] ─────────► [ Redis ] (State Management / Pending Actions)
   │
   ▼
[ Orchestrator Engine ] ◄────► [ OpenAI GPT-4o-mini ] (Function Calling Brain)
   │
   ▼
[ Safety & Tool Validation Layer ]
   │
   ▼
[ PostgreSQL Database ] (Business Data & Audit Logs)
```

## ⚙️ Tech Stack
**Frontend:** Streamlit

**Backend:** Python, FastAPI, Pydantic

**Agent Engine:** OpenAI API (Strict Function Calling)

**Databases:** PostgreSQL (Relational Data & Logs), Redis (In-memory State)

**Infrastructure:** Docker, Docker Compose

## 📸 Screenshots

![OrchestrAI Dashboard](screenshots/Screenshot%202026-04-09%20135042.png)

![Human-in-the-loop Process](screenshots/Screenshot%202026-04-09%20141837.png)

![Agent Reasoning Trail](screenshots/Screenshot%202026-04-09%20141953.png)

![Audit Logs View](screenshots/Screenshot%202026-04-09%20142156.png)

![System Reset & Safety](screenshots/Screenshot%202026-04-09%20142224.png)

## 🚀 Quick Start (Dockerized)
The entire microservice architecture can be spun up with a single command.

### 1. Clone & Configure
```bash
git clone https://github.com/souravppm/orchestrai-safe-agent-system.git
cd OrchestrAI
```
Create a `.env` file in the root directory:

```plaintext
OPENAI_API_KEY=sk-your-api-key-here
```
### 2. Run the Stack
```bash
docker-compose up --build -d
```
**Frontend UI:** http://localhost:8501

**Backend API (Swagger):** http://localhost:8000/docs

## 🧪 Demo Scenarios to Try
### 1. Seed the Environment
Open the Swagger API (http://localhost:8000/docs) and execute `POST /seed` to inject realistic dummy data into the PostgreSQL database.

### 2. Test Human-in-the-Loop Safety
**Input:** "Cancel order 1"

**System Response:** Halts execution. Warns the user and asks for confirmation. The pending action is cached in Redis.

**Input:** "Yes"

**System Response:** Retrieves the action from Redis, executes safely, clears cache, and logs the execution.

### 3. Test Agentic Multi-Step Reasoning
**Input:** "If my order 3 is delayed, please refund it."

**Internal Flow:** The agent internally calls `get_order_status(3)`, observes the state (e.g., "Delivered"), reasons that delivered items cannot be refunded directly, and logically explains this to the user without prompting for confirmation.

### 4. Check Transparency
Hit `GET /logs` on the API to view the internal observation and decision-making trails left by the agent.

## 📊 Engineering Design Decisions (Trade-offs)
**Why Redis over Client-Side State?** In a production enterprise system, relying on the frontend to pass sensitive pending actions back to the server is a security risk. Redis handles state server-side, making the APIs truly robust and scalable.

**Why Synchronous Orchestration?** For this specific real-time chat use case, synchronous execution provides immediate feedback. For long-running background tasks, the core `process_user_request` function is completely decoupled and ready to be offloaded to Celery/RabbitMQ.

**Why PostgreSQL?** Ensures ACID compliance for transactional data (Orders/Payments) and provides a permanent, reliable home for Audit Logs.
