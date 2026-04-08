# 🚀 OrchestrAI: Safe Agent System

A production-grade, zero-hallucination AI agent designed to execute real-world backend operations safely using natural language. 

Unlike traditional chatbots that hallucinate data, OrchestrAI uses a controlled Agentic Architecture where the LLM is only the "Brain" (intent & planning), while a strict Orchestrator handles all validations, safety checks, and API executions.

## 🎯 Key Features

* **Multi-Step Reasoning (Agentic Loop):** Implements a `Plan → Act → Observe → Decide` loop. The agent can observe backend states before making decisions (e.g., checking if an order is delayed before processing a refund).
* **Zero-Hallucination Operations:** The LLM cannot fabricate actions. It strictly calls predefined, schema-validated backend tools.
* **Human-in-the-Loop (Safety First):** Sensitive actions (like `cancel_order` or `refund_order`) trigger a strict confirmation workflow. The agent pauses execution and requests explicit human approval.
* **Full Observability:** Every internal thought, tool call, and database modification is recorded in an Audit Log for total transparency.

## 🏗️ Architecture

```text
User Input → [ FastAPI ] → [ Orchestrator Engine ] ↔ [ LLM Brain (Function Calling) ]
                                    ↓
                           [ Safety / Tool Layer ]
                                    ↓
                           [ Database & Audit Logs ]
```

## ⚙️ Tech Stack
* **Backend:** FastAPI, Python
* **AI/LLM:** OpenAI API (gpt-4o-mini for fast/cheap function calling)
* **Database:** SQLite (Dev) / SQLAlchemy ORM
* **Validation:** Pydantic

## 🚀 Quick Start Guide

### 1. Setup Environment
```bash
git clone https://github.com/souravppm/orchestrai-safe-agent-system.git
cd OrchestrAI
python -m venv venv
source venv/bin/activate # On Windows use: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the root directory:

```plaintext
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload
```
Access the Swagger UI at: http://127.0.0.1:8000/docs

## 🧪 How to Test (Demo Workflow)
* **Seed the Database:** Hit `POST /seed` to inject dummy orders.
* **Standard Action:** Hit `POST /chat` with `{"query": "Cancel order 1"}`. Observe the system halting to ask for confirmation.
* **Multi-Step Reasoning:** Hit `POST /chat` with `{"query": "If order 3 is delayed, refund it."}`. The system will internally fetch the status, observe it's "Delivered", and logically refuse the refund without prompting for confirmation.
* **Audit Trail:** Hit `GET /logs` to see the internal reasoning steps the agent took.
