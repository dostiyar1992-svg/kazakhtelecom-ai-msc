# MASTER ENGINEERING SPECIFICATION & SYSTEM PROMPT
## Platform: Enterprise AI-Powered Employee Experience (EX) & Appeals Intelligence System

### 1. Executive Summary & Core Objective
Build a production-grade, enterprise-ready, interactive Single Page Application (SPA) for "Kazakhtelecom" (and large distributed enterprises) that unifies:
1. **Pulse Survey Lifecycle Management** (Quarterly automated campaigns, distribution over Push/SMS, Outlook, Lotus Notes).
2. **Dual-Channel Appeal & Complaint Intake** (AI-guided conversational intake + Direct self-service form, supporting 100% anonymous whistleblower mode and official named mode).
3. **Strict Role-Based Access Control (RBAC)** with dedicated workspaces, navigation, and permissions:
   - **Regular Employee (Обычный сотрудник)**: CDN login, wellness check-in modal, survey participation, anonymous/named appeal filing, tracking via secret token (`TK-XXXX-KZ`), two-way safe chat.
   - **Employee Experience (EX) Management Service (Служба управления опытом работника / ДУП)**: Survey authoring & launch studio, appeal triage hub, routing engine with Conflict-of-Interest Guard, advanced BI analytics (SRS, eNPS, Strike Risk Score), and an **External Data Ingestion Hub** to upload and merge external CSV/Excel datasets for correlation.
   - **Chancellery (Канцелярия / СЭД)**: Intake registry for non-anonymous and escalated appeals, official registration stamping (`ВХ-2026/XXXX-КАНЦ`), Lotus Notes bridge, SLA deadline enforcement (5-day standard, 24-48h crisis) with live countdown timers and auto-escalation.
   - **Executive / Leadership (Руководство / Правление)**: High-level executive summaries, regional heatmaps across 20 regions of Kazakhstan, trend analysis, and automated AI narrative reports.
4. **Embedded Local On-Premise AI (Qwen 2.5 architecture simulation)**:
   - Semantic classification into 7 incident categories (HSE-01, PAY-02, OT-03, MOB-04, EMG-05, TECH-06, LIFE-07).
   - Dynamic 3-question adaptive survey generation.
   - Automatic statement drafting with Labor Code (ТК РК) and Collective Agreement clauses.
   - Conflict-of-interest hardware detection.
   - Strike Risk & Social Tension scoring (based on Meshcheryakova & CSCC Samruk-Kazyna methodology).

---

### 2. Role-Based Permissions & Interface Matrix

| Role | Workspace View | Core Capabilities & Permissions |
| :--- | :--- | :--- |
| **ROLE_EMPLOYEE** | Employee Portal | • CDN single-sign-on (SSO) profile view.<br>• Wellness check-in nudge modal ("Are you okay?").<br>• Complete active pulse surveys (3 axes: Climate, Loyalty/eNPS, Team).<br>• AI-guided intake conversation or self-service direct form.<br>• Anonymous mode with crypto token `TK-XXXX-KZ` generation.<br>• Token tracker & two-way safe chat with investigators. |
| **ROLE_EX_SERVICE** | EX Management Studio | • Create, configure & launch pulse survey campaigns.<br>• Review, triage & assign incoming appeals.<br>• Route appeals to designated departments with Conflict Guard.<br>• BI Dashboards (SRS Index, eNPS, category breakdown, division rankings).<br>• Executive AI report generation.<br>• **External Data Ingestion Hub** (upload CSV/XLSX, map columns, merge external survey/turnover data into analytics). |
| **ROLE_CHANCELLERY** | Chancellery Registry | • View and filter official (non-anonymous) appeals.<br>• Assign incoming register number (`ВХ-2026/XXXX-КАНЦ`) and stamp.<br>• Track live SLA countdowns (5-day norm, 24-48h emergency).<br>• Dispatch cases to external departmental executors.<br>• Trigger manual or automated executive escalations. |
| **ROLE_EXECUTIVE** | Leadership Dashboard | • Real-time Executive AI Summary.<br>• Kazakhstan 20-region interactive tension heatmap.<br>• Strike Risk Score monitoring.<br>• Division SLA compliance leaderboards. |

---

### 3. Data Architecture & Unified Reactive State

1. **State Machine (`window.platformState`)**:
   - `currentUser`: { id, name, role, division, region, avatar, isCdnAuth }
   - `surveys`: list of pulse survey campaigns (Q1-Q4) with target divisions, status (DRAFT, ACTIVE, CLOSED), and aggregated scores.
   - `appeals`: list of appeals containing id, regNumber, token, isAnonymous, applicantName, division, region, categoryCode, categoryTitle, rawText, formalFabula, recipientDept, recipientOfficer, status (REGISTERED, IN_WORK, RESOLVED, OVERDUE), slaDeadline, slaRemainingSeconds, riskLevel, conflictGuardActive, messages[].
   - `externalDataSets`: imported third-party metrics (turnover rates, external audit files, salary benchmark data).
   - `analytics`: calculated SRS (64%), eNPS (+24), Wellbeing (34%), Strike Risk (8.8 in Western ODS).
2. **Cross-Role Reactivity**:
   - Submitting an appeal as an Employee immediately updates the Chancellery registry and EX triage queues in real time without refreshing.
   - Registering a case in Chancellery updates the Employee's token tracker view.
   - Launching a survey in EX Service updates the Employee's active survey card and topbar notifications.
   - Uploading an external CSV in EX Service immediately updates the correlation charts in the Executive Analytics view.

---

### 4. Technical Stack & UI/UX Guidelines
- Pure HTML5, modern CSS3 (Tailwind-like utility tokens, CSS custom properties, responsive flex/grid layouts), ES6+ Vanilla JavaScript.
- Chart.js for data visualization (doughnut charts, bar charts, trend lines).
- Seamless client-side CSV/Excel parsing engine for the External Data Hub.
- Lucide-style crisp SVG icons and enterprise styling tailored to Kazakhtelecom corporate palette (#00468C Navy, #0284C7 Sky Blue, #10B981 Emerald, #F59E0B Amber, #EF4444 Crimson).

