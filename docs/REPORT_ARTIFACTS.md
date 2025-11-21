# Project Management Artifacts & Report Content

This document contains the generated artifacts for your Semester Project Report. You can copy and paste these sections directly into your PDF report.

## 1. Project Overview & Objectives

**Problem Statement:**
In today's fast-paced world, maintaining a balanced diet is challenging. People often struggle to track their nutrition accurately due to the friction of manual logging. Existing apps require tedious data entry, leading to user drop-off. There is a need for an intelligent, conversational agent that can understand natural language food descriptions, analyze nutritional content instantly, and provide personalized, empathetic feedback to encourage healthy habits.

**Project Goals:**
1.  **Develop an AI Agent**: Create a "Mindful Eating Agent" that understands natural language food logs (e.g., "I had a bowl of oatmeal and a coffee").
2.  **Implement Supervisor-Worker Architecture**: Utilize a robust architecture where a Supervisor delegates tasks to specialized Workers (Parser, Nutritionist, Analyst).
3.  **Personalized Feedback**: Go beyond simple tracking by providing actionable, empathetic recommendations based on user history.
4.  **Seamless Integration**: Provide a user-friendly web interface (Next.js) backed by a powerful Python/Flask agent system.

## 2. Work Breakdown Structure (WBS)

1.  **Project Initiation**
    *   1.1 Define Requirements
    *   1.2 Select Tech Stack (Next.js, Flask, MongoDB, LangGraph)
2.  **System Design**
    *   2.1 Architecture Design (Supervisor-Worker)
    *   2.2 Database Schema Design (Users, Logs, Sessions)
    *   2.3 API Contract Definition
3.  **Backend Development**
    *   3.1 Setup Flask Environment
    *   3.2 Implement MongoDB Client
    *   3.3 Develop Supervisor Agent & Workers
    *   3.4 Implement API Endpoints (Auth, Logging, Chat)
4.  **Frontend Development**
    *   4.1 Setup Next.js Project
    *   4.2 Build UI Components (Chat, Dashboard)
    *   4.3 Integrate API Client
5.  **Testing & Deployment**
    *   5.1 Unit Testing (Agent Logic)
    *   5.2 Integration Testing (API)
    *   5.3 Documentation (User Manual, API Docs)

## 3. Project Schedule (Gantt Chart Data)

| Task | Duration | Start Date | End Date | Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| **Requirement Analysis** | 3 Days | Nov 1 | Nov 3 | - |
| **System Design** | 4 Days | Nov 4 | Nov 7 | Requirement Analysis |
| **Backend: Agent Core** | 7 Days | Nov 8 | Nov 14 | System Design |
| **Backend: API & DB** | 5 Days | Nov 10 | Nov 14 | System Design |
| **Frontend: UI Implementation** | 7 Days | Nov 15 | Nov 21 | Backend: API & DB |
| **Integration & Testing** | 5 Days | Nov 22 | Nov 26 | Frontend: UI Implementation |
| **Final Report & Presentation** | 4 Days | Nov 27 | Nov 30 | Integration & Testing |

## 4. Cost Estimate

| Item | Description | Estimated Cost (Monthly) |
| :--- | :--- | :--- |
| **Development Labor** | 3 Developers @ $30/hr (Part-time) | $0 (Student Project) |
| **Cloud Hosting (AWS)** | EC2 (t3.micro) + S3 | ~$15.00 |
| **Database** | MongoDB Atlas (Shared Tier) | Free / $9.00 |
| **AI API Costs** | OpenAI/Gemini API (if used) | ~$10.00 |
| **Domain Name** | .com domain | $1.00 (Yearly amortized) |
| **Total Estimated** | | **~$35.00 / month** |

## 5. Risk Management Plan

| Risk ID | Risk Description | Probability | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | **API Latency**: AI processing takes too long, degrading UX. | Medium | High | Implement optimistic UI updates; use async processing for heavy tasks; cache common food queries. |
| **R2** | **Data Inaccuracy**: Agent misinterprets food quantities (e.g., "a lot of rice"). | High | Medium | Implement a "Clarification" loop where the agent asks for specifics if confidence is low. |
| **R3** | **Integration Failure**: Frontend and Backend fail to communicate due to CORS/Network issues. | Low | High | comprehensive integration testing; strict API contract adherence; Dockerized environment for consistency. |
| **R4** | **Scope Creep**: Adding too many features (e.g., image recognition) delays core delivery. | Medium | Medium | Stick strictly to the WBS; prioritize "Must-Have" features for the deadline. |

## 6. Quality Assurance Plan

*   **Code Reviews**: All code merged to `main` must be reviewed by at least one peer.
*   **Linting**: Use `flake8` for Python and `ESLint` for TypeScript to enforce style.
*   **Testing**:
    *   *Unit Tests*: Verify nutrition calculations and parser logic.
    *   *Integration Tests*: Verify `/health` and `/api/log-food` endpoints.
*   **User Acceptance Testing (UAT)**: Perform a walkthrough of the "Happy Path" (Register -> Log Food -> Get Recommendation) to ensure usability.

## 7. Integration Plan (Supervisor-Worker)

The system uses a **Supervisor-Worker** architecture implemented via **LangGraph**:

1.  **Supervisor Node**: Acts as the central brain. It receives the user's input and the current state. It evaluates what needs to be done next.
2.  **Routing Logic**:
    *   If food is not parsed $\rightarrow$ Route to **FoodParser Worker**.
    *   If nutrition is missing $\rightarrow$ Route to **Nutrition Worker**.
    *   If analysis is needed $\rightarrow$ Route to **Pattern Analyst Worker**.
    *   If advice is needed $\rightarrow$ Route to **Recommendation Worker**.
3.  **Worker Execution**: Each worker performs a specialized task and updates the global state, then returns control to the Supervisor.
4.  **Completion**: When the Supervisor determines the state is complete (all data present), it terminates the workflow and returns the response to the API.

This ensures modularity; we can upgrade the "Nutrition Worker" without breaking the "FoodParser Worker".
