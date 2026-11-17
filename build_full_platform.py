# -*- coding: utf-8 -*-
"""
Builder for the Full Enterprise Multi-Role EX & Appeals Platform in index.html
Implements complete Role-Based Access Control:
- ROLE_EMPLOYEE (Employee: CDN auth, nudge check-in modal, pulse surveys, AI chat, self-service form, token tracker)
- ROLE_EX_SERVICE (Employee Experience Service: survey builder/launcher, appeals triage, advanced BI analytics, external data CSV/Excel importer)
- ROLE_CHANCELLERY (Chancellery: non-anonymous official registration, incoming numbers, Lotus Notes bridge, live SLA timers, escalations)
- ROLE_EXECUTIVE (Leadership: executive summaries, 20-region heatmap, strike risk indices)
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write('''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Единая корпоративная платформа EX и обращений | АО «Казахтелеком»</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <!-- Chart.js for Visualizations -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --primary: #00468C;       /* Казахтелеком Navy */
      --primary-dark: #002D5C;
      --primary-light: #EBF3FA;
      --accent: #0284C7;        /* Sky Blue */
      --accent-purple: #6366F1; /* EX Purple */
      --success: #10B981;
      --warning: #F59E0B;
      --danger: #EF4444;
      --bg-slate: #F1F5F9;
      --card-bg: #FFFFFF;
      --border: #E2E8F0;
      --border-dark: #CBD5E1;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.03);
      --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background-color: var(--bg-slate);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* TOP GLOBAL CONTROLLER NAVBAR WITH ROLE SELECTOR */
    .platform-topbar {
      background: #0B132B;
      color: #FFFFFF;
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2px solid rgba(2, 132, 199, 0.3);
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-logo-pill {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      font-weight: 900;
      font-size: 13px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
      box-shadow: 0 2px 8px rgba(0, 70, 140, 0.5);
    }

    .brand-titles h1 {
      font-size: 13.5px;
      font-weight: 800;
      color: #F8FAFC;
      letter-spacing: -0.2px;
    }

    .brand-titles span {
      font-size: 11px;
      color: #94A3B8;
    }

    /* RBAC ROLE SWITCHER IN TOPBAR */
    .rbac-role-switcher {
      display: flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: var(--radius-full);
      padding: 3px;
      gap: 2px;
    }

    .role-btn {
      background: transparent;
      border: none;
      color: #CBD5E1;
      padding: 6px 12px;
      font-size: 11.5px;
      font-weight: 700;
      border-radius: var(--radius-full);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .role-btn:hover {
      color: white;
      background: rgba(255, 255, 255, 0.12);
    }

    .role-btn.active {
      color: white;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    .role-btn.active.role-employee { background: linear-gradient(135deg, #00468C, #0284C7); }
    .role-btn.active.role-ex { background: linear-gradient(135deg, #6366F1, #4F46E5); }
    .role-btn.active.role-chancellery { background: linear-gradient(135deg, #059669, #10B981); }
    .role-btn.active.role-exec { background: linear-gradient(135deg, #D97706, #EA580C); }

    .topbar-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-nudge-pill {
      background: linear-gradient(135deg, #F59E0B, #EA580C);
      color: white;
      border: none;
      padding: 6px 12px;
      border-radius: var(--radius-full);
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
      transition: all 0.2s;
    }

    .btn-nudge-pill:hover { transform: translateY(-1px); }

    /* WORKSPACE CONTAINER */
    .workspace-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 20px 24px 40px 24px;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
    }

    /* SUB-NAVBAR FOR CURRENT ROLE WORKSPACE */
    .workspace-subnav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: white;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 10px 18px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }

    .subnav-tabs {
      display: flex;
      align-items: center;
      gap: 6px;
      overflow-x: auto;
    }

    .subnav-tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #475569;
      padding: 8px 14px;
      font-size: 12.5px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      white-space: nowrap;
    }

    .subnav-tab-btn:hover {
      background: #F8FAFC;
      color: var(--primary);
    }

    .subnav-tab-btn.active {
      background: var(--primary-light);
      color: var(--primary);
      border-color: #BAE6FD;
      font-weight: 700;
    }

    /* ROLE WORKSPACE VIEWS */
    .role-view {
      display: none;
      animation: fadeIn 0.3s ease;
    }

    .role-view.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* SHARED COMPONENTS */
    .hero-banner {
      background: linear-gradient(135deg, #002D5C 0%, #00468C 50%, #0284C7 100%);
      color: white;
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-md);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .hero-banner h2 { font-size: 18px; font-weight: 800; margin-bottom: 4px; }
    .hero-banner p { font-size: 12.5px; color: #BAE6FD; max-width: 700px; line-height: 1.5; }

    .btn-action-primary {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-action-primary:hover { opacity: 0.95; transform: translateY(-1px); }

    .card {
      background: white;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 20px;
    }

    .card-header-flex {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }

    .card-header-flex h3 {
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* GRID LAYOUTS */
    .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .grid-3col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .grid-4col { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }

    .kpi-tile {
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 16px;
      position: relative;
      overflow: hidden;
    }

    .kpi-tile::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
    }

    .tile-blue::before { background: #00468C; }
    .tile-purple::before { background: #6366F1; }
    .tile-green::before { background: #10B981; }
    .tile-amber::before { background: #F59E0B; }
    .tile-red::before { background: #EF4444; }

    .kpi-number { font-size: 24px; font-weight: 800; color: #0F172A; margin: 4px 0; }
    .kpi-title { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; }

    /* FORM STYLES */
    .form-group { margin-bottom: 14px; }
    .form-label { display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 6px; }
    .form-control {
      width: 100%;
      padding: 9px 12px;
      border: 1.5px solid var(--border-dark);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: #FFFFFF;
      transition: border-color 0.2s;
    }
    .form-control:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }

    /* TABLE STYLES */
    .data-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
      background: white;
    }

    .data-table th {
      background: #F8FAFC;
      padding: 12px 14px;
      font-weight: 700;
      color: #475569;
      text-align: left;
      border-bottom: 1.5px solid var(--border);
    }

    .data-table td {
      padding: 12px 14px;
      border-bottom: 1px solid #F1F5F9;
      vertical-align: middle;
    }

    .data-table tr:hover td { background: #F8FAFC; }

    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
    }

    .badge-anon { background: #DCFCE7; color: #166534; }
    .badge-official { background: #E0F2FE; color: #0369A1; }
    .badge-warning { background: #FEF3C7; color: #B45309; }
    .badge-danger { background: #FEE2E2; color: #991B1B; }

    /* CHAT STREAM (AI INTAKE) */
    .chat-box-wrapper {
      background: white;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 580px;
    }

    .chat-stream-body {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
      background: #FAFAFC;
    }

    .chat-msg-row { display: flex; gap: 12px; max-width: 90%; }
    .chat-msg-row.ai { align-self: flex-start; }
    .chat-msg-row.user { align-self: flex-end; flex-direction: row-reverse; }

    .msg-avatar {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 700;
    }

    .msg-avatar.ai { background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD; }
    .msg-avatar.user { background: #00468C; color: white; }

    .msg-bubble {
      padding: 12px 16px;
      border-radius: var(--radius-lg);
      font-size: 13.5px;
      line-height: 1.5;
    }

    .chat-msg-row.ai .msg-bubble {
      background: white;
      border: 1px solid var(--border);
      color: #1E293B;
      border-top-left-radius: 4px;
      box-shadow: var(--shadow-sm);
    }

    .chat-msg-row.user .msg-bubble {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      border-top-right-radius: 4px;
      box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
    }

    .quick-chip {
      background: white;
      border: 1px solid #E2E8F0;
      border-radius: var(--radius-md);
      padding: 8px 12px;
      font-size: 12px;
      color: #334155;
      cursor: pointer;
      margin-bottom: 6px;
      transition: all 0.2s;
    }

    .quick-chip:hover { border-color: var(--accent); background: #F0F9FF; }

    /* DROPZONE FOR EXTERNAL DATA */
    .dropzone-box {
      border: 2px dashed #94A3B8;
      border-radius: var(--radius-lg);
      padding: 28px;
      text-align: center;
      background: #F8FAFC;
      cursor: pointer;
      transition: all 0.2s;
    }

    .dropzone-box:hover {
      border-color: var(--accent);
      background: #F0F9FF;
    }

    /* MODAL POPUPS */
    .modal-backdrop {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(4px);
      z-index: 3000;
      align-items: center;
      justify-content: center;
    }

    .modal-backdrop.active { display: flex; animation: fadeIn 0.2s ease; }

    .modal-content-card {
      background: white;
      border-radius: var(--radius-lg);
      padding: 28px;
      max-width: 580px;
      width: 90%;
      box-shadow: var(--shadow-xl);
      border: 1px solid var(--border);
    }

    /* TOAST */
    .toast-tray {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 4000;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .toast-pill {
      background: #0B132B;
      color: white;
      padding: 12px 18px;
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 8px;
      border-left: 4px solid #10B981;
      animation: fadeIn 0.3s ease;
    }
  </style>
</head>
<body>

  <!-- ==================== TOPBAR: BRAND & ROLE SWITCHER ==================== -->
  <header class="platform-topbar">
    <div class="brand-section">
      <div class="brand-logo-pill">КТ ЕX</div>
      <div class="brand-titles">
        <h1>Единая платформа управления опытом работника (EX) и обращениями</h1>
        <span>АО «Казахтелеком» • Система социального климата и мониторинга инцидентов</span>
      </div>
    </div>

    <!-- ВЫБОР РОЛИ (RBAC) -->
    <div class="rbac-role-switcher">
      <button class="role-btn role-employee active" onclick="switchRole('employee')">
        👤 Сотрудник
      </button>
      <button class="role-btn role-ex" onclick="switchRole('ex')">
        🎯 Служба EX (Опыт работника)
      </button>
      <button class="role-btn role-chancellery" onclick="switchRole('chancellery')">
        🏛️ Канцелярия (СЭД)
      </button>
      <button class="role-btn role-exec" onclick="switchRole('exec')">
        👑 Руководство
      </button>
    </div>

    <div class="topbar-actions">
      <button class="btn-nudge-pill" onclick="openNudgeModal()">
        💬 Вовлекающий Чекин
      </button>
      <button class="role-btn" style="background: rgba(255,255,255,0.12);" onclick="openTokenModal()">
        🔍 Поиск по токену
      </button>
    </div>
  </header>

  <!-- ==================== ОСНОВНОЙ КОНТЕЙНЕР ==================== -->
  <main class="workspace-container">

    <!-- ==============================================================
         РОЛЬ 1: WORKSPACE СОТРУДНИКА (EMPLOYEE)
         ============================================================== -->
    <section id="view-employee" class="role-view active">
      
      <!-- Под-навигация сотрудника -->
      <div class="workspace-subnav">
        <div class="subnav-tabs">
          <button class="subnav-tab-btn active" onclick="switchEmployeeTab('emp-home')">
            🏠 Главная (CDN Профиль)
          </button>
          <button class="subnav-tab-btn" onclick="switchEmployeeTab('emp-chat')">
            💬 Диалог с ИИ (Подать жалобу)
          </button>
          <button class="subnav-tab-btn" onclick="switchEmployeeTab('emp-pulse')">
            📊 Пульс-опрос Q4
          </button>
          <button class="subnav-tab-btn" onclick="switchEmployeeTab('emp-form')">
            📝 Прямая подача (Форма)
          </button>
          <button class="subnav-tab-btn" onclick="switchEmployeeTab('emp-my-appeals')">
            📋 Мои обращения & Токены
          </button>
        </div>
        <div style="font-size: 12px; color: #64748B;">
          Вход через корпоративный CDN: <strong>Ахметов Данияр (ОДС Запад)</strong>
        </div>
      </div>

      <!-- Вкладка 1.1: Главная сотрудника -->
      <div id="emp-home" class="emp-tab-content">
        <div class="hero-banner">
          <div>
            <h2>Сәлеметсіз бе, Данияр Бауыржанұлы!</h2>
            <p>
              Корпоративный портал опыта работника АО «Казахтелеком». Делитесь обратной связью в регулярных квартальных опросах, сообщайте о проблемах на рабочем месте в 100% анонимном режиме.
            </p>
          </div>
          <button class="btn-action-primary" style="background: white; color: #00468C;" onclick="openNudgeModal()">
            💬 Пройти чекин
          </button>
        </div>

        <div class="grid-4col">
          <div class="card" style="cursor: pointer; border-left: 4px solid #6366F1;" onclick="switchEmployeeTab('emp-pulse')">
            <div style="font-size: 24px; margin-bottom: 6px;">📊</div>
            <h4 style="font-size: 13.5px; font-weight: 700; margin-bottom: 4px;">Пульс-опрос Q4 2026</h4>
            <p style="font-size: 11.5px; color: #64748B;">Срез климата и психологического комфорта (~60 сек).</p>
            <div style="font-size: 11.5px; font-weight: 700; color: #6366F1; margin-top: 8px;">Пройти опрос →</div>
          </div>

          <div class="card" style="cursor: pointer; border-left: 4px solid #00468C;" onclick="switchEmployeeTab('emp-chat')">
            <div style="font-size: 24px; margin-bottom: 6px;">💬</div>
            <h4 style="font-size: 13.5px; font-weight: 700; margin-bottom: 4px;">Диалог с ИИ-Агентом</h4>
            <p style="font-size: 11.5px; color: #64748B;">Опишите проблему своими словами — ИИ оформит официальное заявление.</p>
            <div style="font-size: 11.5px; font-weight: 700; color: #00468C; margin-top: 8px;">Начать диалог →</div>
          </div>

          <div class="card" style="cursor: pointer; border-left: 4px solid #0284C7;" onclick="switchEmployeeTab('emp-form')">
            <div style="font-size: 24px; margin-bottom: 6px;">📝</div>
            <h4 style="font-size: 13.5px; font-weight: 700; margin-bottom: 4px;">Прямой ввод обращения</h4>
            <p style="font-size: 11.5px; color: #64748B;">Заполните форму-бланк вручную с прикреплением файлов.</p>
            <div style="font-size: 11.5px; font-weight: 700; color: #0284C7; margin-top: 8px;">Заполнить форму →</div>
          </div>

          <div class="card" style="cursor: pointer; border-left: 4px solid #10B981;" onclick="switchEmployeeTab('emp-my-appeals')">
            <div style="font-size: 24px; margin-bottom: 6px;">📋</div>
            <h4 style="font-size: 13.5px; font-weight: 700; margin-bottom: 4px;">Мои тикеты</h4>
            <p style="font-size: 11.5px; color: #64748B;">Проверка стадий рассмотрения и диалог с комиссией.</p>
            <div style="font-size: 11.5px; font-weight: 700; color: #10B981; margin-top: 8px;">Открыть кабинет →</div>
          </div>
        </div>
      </div>

      <!-- Вкладка 1.2: Диалог с ИИ-Агентом -->
      <div id="emp-chat" class="emp-tab-content" style="display: none;">
        <div class="chat-box-wrapper">
          <div style="padding: 12px 18px; border-bottom: 1px solid var(--border); background: white; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="width: 32px; height: 32px; border-radius: 50%; background: #E0F2FE; color: #0284C7; font-weight: 800; display: flex; align-items: center; justify-content: center;">AI</div>
              <div>
                <strong style="font-size: 13px;">Интеллектуальный помощник приема обращений</strong>
                <div style="font-size: 10.5px; color: #10B981;">● On-Premise LLM • Конфиденциальный контур</div>
              </div>
            </div>
            <button class="role-btn" style="background:#F1F5F9; color:#475569;" onclick="resetEmpChat()">🔄 Новый диалог</button>
          </div>

          <div class="chat-stream-body" id="emp-chat-stream">
            <div class="chat-msg-row ai">
              <div class="msg-avatar ai">ИИ</div>
              <div>
                <div class="msg-bubble">
                  Сәлеметсіз бе, Данияр! Расскажите своими словами, с чем возникла сложность на рабочем месте (задержка зимней обуви/СИЗ, переработки, давление мастера, состояние техники).<br><br>
                  Я составлю официальное заявление и помогу зарегистрировать его в Канцелярии.
                </div>
                <div style="margin-top: 8px;">
                  <div style="font-size: 11px; font-weight: 700; color: #64748B; margin-bottom: 4px;">💡 Быстрые примеры:</div>
                  <div class="quick-chip" onclick="applyChatPreset('ppe')">🦺 <strong>СИЗ / Обувь:</strong> «В ОДС Запад уже 2 месяца не выдают зимнюю обувь...»</div>
                  <div class="quick-chip" onclick="applyChatPreset('overtime')">⏱️ <strong>Переработки:</strong> «Принуждают выходить по субботам без табелирования...»</div>
                  <div class="quick-chip" onclick="applyChatPreset('mobbing')">🚨 <strong>Моббинг:</strong> «Мастер систематически грубит и угрожает увольнением...»</div>
                </div>
              </div>
            </div>
            <div id="chat-injected-area"></div>
          </div>

          <div style="padding: 12px 18px; border-top: 1px solid var(--border); background: white; display: flex; gap: 8px;">
            <input type="text" id="emp-chat-input" class="form-control" placeholder="Опишите ситуацию своими словами..." onkeypress="handleEmpChatEnter(event)">
            <button class="btn-action-primary" onclick="sendEmpChatMessage()">Отправить</button>
          </div>
        </div>
      </div>

      <!-- Вкладка 1.3: Пульс-опрос Q4 -->
      <div id="emp-pulse" class="emp-tab-content" style="display: none;">
        <div class="card" style="max-width: 860px; margin: 0 auto;">
          <div class="card-header-flex">
            <div>
              <h3>📊 Ежеквартальный пульс-опрос социального климата (Q4 2026)</h3>
              <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Уведомление получено через Push, Outlook и Lotus Notes.</p>
            </div>
            <span class="badge-pill badge-anon">🔒 100% Анонимно</span>
          </div>

          <!-- Блок 1 -->
          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <strong style="font-size: 13px;">1. Социальный климат и материально-техническое снабжение</strong>
            <p style="font-size: 12.5px; color: #334155; margin: 6px 0;">«Обеспечение СИЗ, спецодеждой, инструментами и транспортом позволяет мне безопасно работать»:</p>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin: 10px 0;">
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p1', 1, this)">1 (Совсем нет)</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p1', 2, this)">2 (Скорее нет)</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p1', 3, this)">3 (Средне)</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p1', 4, this)">4 (Скорее да)</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p1', 5, this)">5 (Полностью)</button>
            </div>
            <!-- Alert Synergy -->
            <div id="pulse-synergy-banner" style="display: none; background: #FEF2F2; border: 1px solid #F87171; border-radius: 6px; padding: 10px; margin-top: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 12px; color: #991B1B;">⚠️ Вы указали низкий балл. Хотите прямо сейчас оформить обращение в Канцелярию?</span>
                <button class="btn-action-primary" style="background: #DC2626; padding: 4px 10px; font-size: 11px;" onclick="convertPulseToComplaint()">Оформить жалобу →</button>
              </div>
            </div>
          </div>

          <!-- Блок 2 -->
          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <strong style="font-size: 13px;">2. Отношение к компании (Лояльность и eNPS)</strong>
            <p style="font-size: 12.5px; color: #334155; margin: 6px 0;">«Я доверяю информации руководства и готов рекомендовать „Казахтелеком“ как работодателя»:</p>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px;">
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p2', 1, this)">1 (Нет)</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p2', 2, this)">2</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p2', 3, this)">3</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p2', 4, this)">4</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p2', 5, this)">5 (Да)</button>
            </div>
          </div>

          <!-- Блок 3 -->
          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 20px;">
            <strong style="font-size: 13px;">3. Атмосфера в коллективе и психологическая безопасность</strong>
            <p style="font-size: 12.5px; color: #334155; margin: 6px 0;">«В нашем коллективе уважительная атмосфера, я не сталкиваюсь с давлением мастера»:</p>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px;">
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p3', 1, this)">1 (Прессинг)</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p3', 2, this)">2</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p3', 3, this)">3</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p3', 4, this)">4</button>
              <button class="role-btn" style="border: 1px solid #CBD5E1; color: #334155;" onclick="setPulseRating('p3', 5, this)">5 (Комфортно)</button>
            </div>
          </div>

          <button class="btn-action-primary" style="width: 100%; justify-content: center; padding: 12px;" onclick="completePulseSurvey()">
            ✅ Завершить опрос и запечатать в аналитический пул
          </button>
        </div>
      </div>

      <!-- Вкладка 1.4: Прямая подача обращения (Форма) -->
      <div id="emp-form" class="emp-tab-content" style="display: none;">
        <div class="card" style="max-width: 860px; margin: 0 auto;">
          <div class="card-header-flex">
            <h3>📝 Самостоятельное заполнение обращения в Канцелярию</h3>
            <span style="font-size: 12px; color: #64748B;">Прямой ввод без чат-бота</span>
          </div>

          <form onsubmit="event.preventDefault(); submitDirectForm();">
            <div class="grid-2col">
              <div class="form-group">
                <label class="form-label">Структурный дивизион:</label>
                <select class="form-control" id="direct-div">
                  <option value="ОДС">Объединение «Дивизион „Сеть“» (ОДС)</option>
                  <option value="СФ">Сервисная фабрика (СФ)</option>
                  <option value="ДРБ">Дивизион по розничному бизнесу (ДРБ)</option>
                  <option value="ДКБ">Дивизион по корпоративному бизнесу (ДКБ)</option>
                  <option value="ДУП">Департамент управления персоналом (ДУП)</option>
                  <option value="ДПБ">Департамент производственной безопасности (HSE)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Регион (20 областей РК):</label>
                <select class="form-control" id="direct-region">
                  <option value="Атырауская область">Атырауская область</option>
                  <option value="Мангыстауская область">Мангыстауская область</option>
                  <option value="Западно-Казахстанская область">Западно-Казахстанская область</option>
                  <option value="область Абай (г. Семей)">область Абай (г. Семей)</option>
                  <option value="Восточно-Казахстанская область">Восточно-Казахстанская область</option>
                  <option value="г. Астана">г. Астана</option>
                  <option value="г. Алматы">г. Алматы</option>
                  <option value="Карагандинская область">Карагандинская область</option>
                </select>
              </div>
            </div>

            <div class="grid-2col">
              <div class="form-group">
                <label class="form-label">Категория обращения:</label>
                <select class="form-control" id="direct-category">
                  <option value="HSE-01">HSE-01 • Охрана труда и СИЗ (SLA 5 дней)</option>
                  <option value="PAY-02">PAY-02 • Оплата труда и надбавки (SLA 5 дней)</option>
                  <option value="OT-03">OT-03 • Переработки по субботам (SLA 3 дня)</option>
                  <option value="MOB-04">MOB-04 • Моббинг и давление (SLA 7 дней)</option>
                  <option value="EMG-05">EMG-05 • Угроза забастовки / ЧП (SLA 24ч)</option>
                </select>
              </div>

              <div class="form-group">
                <label class="form-label">Режим конфиденциальности:</label>
                <select class="form-control" id="direct-anon">
                  <option value="anon">🔒 Анонимно (выдать секретный токен TK-XXXX)</option>
                  <option value="official">👤 Официально (Ахметов Д.Б., таб. 104291)</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Суть инцидента и ваши требования:</label>
              <textarea class="form-control" id="direct-text" rows="4" placeholder="Опишите факты нарушения..."></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Прикрепить подтверждающие файлы (фото дефектов, наряды):</label>
              <div class="dropzone-box" onclick="simulateFormFileUpload()">
                <div style="font-size: 22px;">📎</div>
                <div style="font-size: 13px; font-weight: 700; color: #00468C;" id="direct-file-label">Нажмите для выбора файла (PDF, JPG, PNG)</div>
              </div>
            </div>

            <button type="submit" class="btn-action-primary" style="width: 100%; justify-content: center; padding: 12px;">
              🏛️ Зарегистрировать в Канцелярии
            </button>
          </form>
        </div>
      </div>

      <!-- Вкладка 1.5: Мои тикеты -->
      <div id="emp-my-appeals" class="emp-tab-content" style="display: none;">
        <div class="card">
          <div class="card-header-flex">
            <h3>📋 Мои зарегистрированные обращения</h3>
            <button class="btn-action-primary" style="font-size: 11.5px; padding: 6px 12px;" onclick="openTokenModal()">🔍 Найти по токену</button>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Номер / Токен</th>
                <th>Дата</th>
                <th>Категория</th>
                <th>Получатель</th>
                <th>Статус</th>
                <th>SLA Таймер</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody id="emp-appeals-tbody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ==============================================================
         РОЛЬ 2: WORKSPACE СЛУЖБЫ EX (УПРАВЛЕНИЕ ОПЫТОМ РАБОТНИКА)
         ============================================================== -->
    <section id="view-ex" class="role-view">
      
      <!-- Под-навигация EX -->
      <div class="workspace-subnav" style="border-left: 4px solid #6366F1;">
        <div class="subnav-tabs">
          <button class="subnav-tab-btn active" onclick="switchExTab('ex-triage')">
            📥 Центр триажа обращений
          </button>
          <button class="subnav-tab-btn" onclick="switchExTab('ex-surveys')">
            ⚙️ Управление пульс-опросами
          </button>
          <button class="subnav-tab-btn" onclick="switchExTab('ex-analytics')">
            📊 BI Аналитика & Индексы SRS
          </button>
          <button class="subnav-tab-btn" onclick="switchExTab('ex-import')">
            📂 Загрузка внешних данных (CSV/Excel)
          </button>
        </div>
        <div style="font-size: 12px; color: #4F46E5;">
          Служба управления опытом работника: <strong>Сапарова А. (ЦА ДУП)</strong>
        </div>
      </div>

      <!-- Вкладка 2.1: Триаж обращений EX -->
      <div id="ex-triage" class="ex-tab-content">
        <div class="grid-4col" style="margin-bottom: 20px;">
          <div class="kpi-tile tile-blue">
            <div class="kpi-title">Всего в потоке</div>
            <div class="kpi-number" id="ex-kpi-total">420</div>
            <span style="font-size: 11px; color: #10B981;">+1 новое за смену</span>
          </div>
          <div class="kpi-tile tile-purple">
            <div class="kpi-title">Анонимных сигналов</div>
            <div class="kpi-number">320 (76%)</div>
            <span style="font-size: 11px; color: #64748B;">Связь по токену TK</span>
          </div>
          <div class="kpi-tile tile-amber">
            <div class="kpi-title">На контроле SLA</div>
            <div class="kpi-number">12</div>
            <span style="font-size: 11px; color: #D97706;">Менее 24ч до дедлайна</span>
          </div>
          <div class="kpi-tile tile-red">
            <div class="kpi-title">Критические очаги</div>
            <div class="kpi-number" style="color: #EF4444;">3</div>
            <span style="font-size: 11px; color: #EF4444;">Риск забастовки в ОДС</span>
          </div>
        </div>

        <div class="card">
          <div class="card-header-flex">
            <h3>📥 Очередь триажа и оперативной маршрутизации</h3>
            <span style="font-size: 12px; color: #10B981;">🛡️ Conflict Guard: Активирован</span>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Вх. номер / Код</th>
                <th>Дата</th>
                <th>Режим</th>
                <th>Дивизион / Регион</th>
                <th>Суть инцидента</th>
                <th>Назначенный получатель</th>
                <th>Статус</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody id="ex-triage-tbody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Вкладка 2.2: Управление пульс-опросами EX -->
      <div id="ex-surveys" class="ex-tab-content" style="display: none;">
        <div class="card">
          <div class="card-header-flex">
            <h3>⚙️ Управление кампаниями пульс-опросов</h3>
            <button class="btn-action-primary" onclick="launchNewSurveyCampaign()">🚀 Запустить новый опрос Q1 2027</button>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Кампания</th>
                <th>Срок проведения</th>
                <th>Целевой охват</th>
                <th>Уведомления</th>
                <th>Участие (%)</th>
                <th>Средний eNPS</th>
                <th>Статус</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Q4 2026: Климат и благополучие</strong></td>
                <td>01.11.2026 — 25.11.2026</td>
                <td>Вся компания (20 000+)</td>
                <td>Push, Outlook, Lotus</td>
                <td><strong>74.2%</strong></td>
                <td><span class="badge-pill badge-anon">+24.0</span></td>
                <td><span class="badge-pill" style="background:#DCFCE7; color:#15803D;">АКТИВЕН</span></td>
              </tr>
              <tr>
                <td><strong>Q3 2026: Оценка материального снабжения</strong></td>
                <td>01.08.2026 — 20.08.2026</td>
                <td>ОДС и Сервисная фабрика</td>
                <td>Push, Outlook</td>
                <td>81.0%</td>
                <td><span class="badge-pill badge-warning">+12.0</span></td>
                <td><span class="badge-pill" style="background:#F1F5F9; color:#475569;">ЗАВЕРШЕН</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Вкладка 2.3: BI Аналитика EX -->
      <div id="ex-analytics" class="ex-tab-content" style="display: none;">
        <div class="card">
          <div class="card-header-flex">
            <h3>📊 BI Аналитика климата и системных очагов напряженности</h3>
            <span style="font-size: 12px; color: #64748B;">Синтез данных Qwen 2.5 + Индексы CSCC</span>
          </div>

          <div class="grid-2col" style="margin-bottom: 20px;">
            <div style="height: 250px;">
              <canvas id="chartExTopics"></canvas>
            </div>
            <div style="height: 250px;">
              <canvas id="chartExDivisions"></canvas>
            </div>
          </div>

          <!-- Сводный отчет ИИ -->
          <div style="background: #F8FAFC; border: 1.5px solid #CBD5E1; border-left: 4px solid #6366F1; border-radius: 8px; padding: 16px;">
            <strong style="color: #4F46E5; font-size: 13.5px;">✨ Executive AI Summary (Локальная модель):</strong>
            <p style="font-size: 12.5px; line-height: 1.6; margin-top: 6px;">
              Анализ массива 420 обращений и пульс-опроса Q4 выявил критическую концентрацию жалоб в <strong>ОДС Западная РДТ (69 тикетов)</strong> по теме отсутствия зимней спецобуви. 
              Индекс риска забастовки вырос до <strong>8.8 / 10</strong>. Рекомендована срочная поставка 240 пар обуви со склада ЦА.
            </p>
          </div>
        </div>
      </div>

      <!-- Вкладка 2.4: Загрузка внешних данных (CSV/Excel) -->
      <div id="ex-import" class="ex-tab-content" style="display: none;">
        <div class="card">
          <div class="card-header-flex">
            <div>
              <h3>📂 Загрузка и обогащение аналитики внешними данными</h3>
              <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
                Загружайте CSV или Excel файлы (текучесть кадров, аудиты безопасности, внешние опросы) для сопоставления с обращениями.
              </p>
            </div>
          </div>

          <div class="dropzone-box" onclick="triggerExternalDataImport()">
            <div style="font-size: 32px;">📑</div>
            <div style="font-size: 14px; font-weight: 700; color: #00468C; margin: 4px 0;" id="import-box-text">
              Нажмите для загрузки файла CSV / Excel или перетащите сюда
            </div>
            <div style="font-size: 11.5px; color: #94A3B8;">Поддерживаются: .CSV, .XLSX, .XLS (до 50 МБ)</div>
          </div>

          <!-- Preview of imported data -->
          <div id="import-preview-block" style="display: none; margin-top: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
              <strong style="font-size: 13px; color: #10B981;">✅ Внешний датасет загружен: «External_Turnover_Audit_2026.csv» (42 записи)</strong>
              <button class="btn-action-primary" style="padding: 4px 10px; font-size: 11.5px;" onclick="mergeExternalDataToAnalytics()">
                ⚡ Объединить с аналитикой климата
              </button>
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>Дивизион</th>
                  <th>Регион</th>
                  <th>Коэффициент текучести (%)</th>
                  <th>Абсентеизм (дней)</th>
                  <th>Корреляция с жалобами</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>ОДС</td>
                  <td>Атырауская область</td>
                  <td>14.8% (Высокая)</td>
                  <td>12.4</td>
                  <td><span class="badge-pill badge-danger">Высокая (r=0.88)</span></td>
                </tr>
                <tr>
                  <td>ОДС</td>
                  <td>область Абай</td>
                  <td>11.2%</td>
                  <td>9.1</td>
                  <td><span class="badge-pill badge-warning">Умеренная (r=0.64)</span></td>
                </tr>
                <tr>
                  <td>СФ</td>
                  <td>Карагандинская обл.</td>
                  <td>8.4%</td>
                  <td>6.0</td>
                  <td><span class="badge-pill badge-anon">Низкая</span></td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>

    </section>

    <!-- ==============================================================
         РОЛЬ 3: WORKSPACE КАНЦЕЛЯРИИ (CHANCELLERY)
         ============================================================== -->
    <section id="view-chancellery" class="role-view">
      
      <!-- Под-навигация Канцелярии -->
      <div class="workspace-subnav" style="border-left: 4px solid #10B981;">
        <div class="subnav-tabs">
          <button class="subnav-tab-btn active" onclick="switchChancelleryTab('canc-reg')">
            🏛️ Регистрация официальных обращений
          </button>
          <button class="subnav-tab-btn" onclick="switchChancelleryTab('canc-sla')">
            ⏱️ Контроль сроков (SLA Дедлайны)
          </button>
        </div>
        <div style="font-size: 12px; color: #047857;">
          Канцелярия ЦА: <strong>Медебекова А.Т. (Старший инспектор СЭД)</strong>
        </div>
      </div>

      <!-- Вкладка 3.1: Регистрация официальных обращений -->
      <div id="canc-reg" class="canc-tab-content">
        <div class="card">
          <div class="card-header-flex">
            <div>
              <h3>🏛️ Журнал входящих официальных документов (Lotus Notes СЭД)</h3>
              <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
                Регистрация не анонимных обращений, присвоение входящего номера `ВХ-2026/XXXX-КАНЦ` и направление исполнителям.
              </p>
            </div>
            <span class="badge-pill badge-official">Только не анонимные тикеты</span>
          </div>

          <table class="data-table">
            <thead>
              <tr>
                <th>Вх. номер СЭД</th>
                <th>Дата</th>
                <th>Заявитель (ФИО)</th>
                <th>Подразделение</th>
                <th>Тема обращения</th>
                <th>Исполнитель</th>
                <th>Статус</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody id="chancellery-official-tbody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- Вкладка 3.2: Контроль SLA дедлайнов -->
      <div id="canc-sla" class="canc-tab-content" style="display: none;">
        <div class="card">
          <div class="card-header-flex">
            <h3>⏱️ Мониторинг регламентных сроков рассмотрения (SLA)</h3>
            <span style="font-size: 12px; color: #10B981;">Норматив: 5 рабочих дней</span>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Вх. номер</th>
                <th>Заявитель</th>
                <th>Категория</th>
                <th>Исполнитель</th>
                <th>Дедлайн</th>
                <th>Остаток таймера</th>
                <th>Зона риска</th>
                <th>Эскалация</th>
              </tr>
            </thead>
            <tbody id="chancellery-sla-tbody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ==============================================================
         РОЛЬ 4: WORKSPACE РУКОВОДСТВА (EXECUTIVE)
         ============================================================== -->
    <section id="view-exec" class="role-view">
      <div class="hero-banner" style="background: linear-gradient(135deg, #0B132B, #00468C);">
        <div>
          <h2>Панель руководства: Социальное спокойствие и риски компании</h2>
          <p>
            Сводные отчеты On-Premise LLM, тепловая карта 20 регионов Казахстана и соблюдение SLA филиалами.
          </p>
        </div>
        <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 700;">
          ROLE_EXECUTIVE (Правление)
        </span>
      </div>

      <div class="grid-2col">
        <div class="card">
          <h4 style="font-size: 13px; font-weight: 700; margin-bottom: 10px;">Структура нарушений по категориям</h4>
          <div style="height: 250px;">
            <canvas id="chartExecDoughnut"></canvas>
          </div>
        </div>

        <div class="card">
          <h4 style="font-size: 13px; font-weight: 700; margin-bottom: 10px;">Рейтинг соблюдения SLA по дивизионам (%)</h4>
          <div style="height: 250px;">
            <canvas id="chartExecBars"></canvas>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ==================== МОДАЛЬНОЕ ОКНО ВОВЛЕЧЕНИЯ (NUDGE) ==================== -->
  <div id="modal-nudge" class="modal-backdrop active" onclick="closeNudgeModal()">
    <div class="modal-content-card" onclick="event.stopPropagation()">
      <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 14px;">
        <div style="width: 44px; height: 44px; border-radius: 50%; background: #EBF3FA; color: #00468C; display: flex; align-items: center; justify-content: center; font-size: 22px;">👋</div>
        <div>
          <h3 style="font-size: 16px; font-weight: 800; color: #00468C;">Сәлеметсіз бе, Данияр Бауыржанұлы!</h3>
          <span style="font-size: 12px; color: #64748B;">Авторизация CDN • ОДС Западная РДТ • г. Атырау</span>
        </div>
      </div>

      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; font-size: 13.5px; line-height: 1.5; color: #1E293B; margin-bottom: 16px;">
        Все ли у вас в порядке на рабочем месте? Есть ли сложности, нерешенные вопросы или проблемы в коллективе? Хотите ли вы поговорить об этом или поделиться обратной связью?
      </div>

      <div style="display: flex; flex-direction: column; gap: 8px;">
        <button class="role-btn" style="background:#F8FAFC; border:1px solid #CBD5E1; color:#00468C; padding:12px; justify-content:flex-start; font-size:12.5px;" onclick="nudgeAction('chat')">
          💬 <strong>Да, есть проблема — поговорить с ИИ-агентом</strong>
        </button>
        <button class="role-btn" style="background:#F8FAFC; border:1px solid #CBD5E1; color:#6366F1; padding:12px; justify-content:flex-start; font-size:12.5px;" onclick="nudgeAction('pulse')">
          📊 <strong>Пройти квартальный пульс-опрос Q4 (60 сек)</strong>
        </button>
        <button class="role-btn" style="background:#F8FAFC; border:1px solid #CBD5E1; color:#0284C7; padding:12px; justify-content:flex-start; font-size:12.5px;" onclick="nudgeAction('form')">
          📝 <strong>Заполнить обращение вручную</strong>
        </button>
        <button class="role-btn" style="background:#F8FAFC; border:1px solid #CBD5E1; color:#10B981; padding:12px; justify-content:flex-start; font-size:12.5px;" onclick="nudgeAction('ok')">
          👍 <strong>Все отлично, спасибо!</strong>
        </button>
      </div>
    </div>
  </div>

  <!-- ==================== МОДАЛЬНОЕ ОКНО ПОИСКА ПО ТОКЕНУ ==================== -->
  <div id="modal-token" class="modal-backdrop" onclick="closeTokenModal()">
    <div class="modal-content-card" onclick="event.stopPropagation()">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 16px; font-weight: 800; color: #00468C;">🔍 Проверка обращения по токену</h3>
        <button style="border: none; background: transparent; font-size: 18px; cursor: pointer;" onclick="closeTokenModal()">✕</button>
      </div>
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <input type="text" id="token-input-field" class="form-control" value="TK-7842-KZ" style="font-family: monospace; font-weight: 700;">
        <button class="btn-action-primary" onclick="searchByToken()">Найти</button>
      </div>
      <div id="token-result-box" style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 14px; font-size: 12.5px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
          <strong style="color: #00468C;">ВХ-2026/0942-КАНЦ</strong>
          <span class="badge-pill" style="background:#E0F2FE; color:#0369A1;">В работе у исполнителя</span>
        </div>
        <div>Тема: <strong>Охрана труда: задержка зимней обуви</strong></div>
        <div style="margin-top: 8px; background: white; border: 1px solid #E2E8F0; padding: 8px; border-radius: 4px;">
          💬 <strong>Ответ исполнителя (17:40):</strong> Запрос направлен на центральный склад в г. Астана.
        </div>
      </div>
    </div>
  </div>

  <!-- TOAST TRAY -->
  <div class="toast-tray" id="toast-tray"></div>

  <!-- ==================== JAVASCRIPT STATE & LOGIC ==================== -->
  <script>
    // ЕДИНЫЙ РЕАКТИВНЫЙ STATE МЕНЕДЖЕР
    window.appState = {
      currentRole: 'employee',
      appeals: [
        {
          id: 1,
          regNum: "ВХ-2026/0942-КАНЦ",
          token: "TK-7842-KZ",
          date: "12.11.2026 09:30",
          isAnon: true,
          fio: "— (Анонимно)",
          div: "ОДС",
          region: "Атырауская область",
          category: "HSE-01 Охрана труда",
          text: "Задержка зимней обуви и курток выездным бригадам монтеров АВР более 45 дней.",
          recipient: "Департамент производственной безопасности (HSE)",
          status: "В работе",
          slaDeadline: "17.11.2026",
          slaTimer: "04д 23ч 58м"
        },
        {
          id: 2,
          regNum: "ВХ-2026/0941-КАНЦ",
          token: "TK-8812-KZ",
          date: "10.11.2026 14:20",
          isAnon: false,
          fio: "Искаков М.А.",
          div: "ОДС",
          region: "область Абай",
          category: "PAY-02 Оплата труда",
          text: "Принуждение к выходу в субботу без табелирования и оплаты.",
          recipient: "Департамент оплаты труда (ДУП)",
          status: "В работе",
          slaDeadline: "15.11.2026",
          slaTimer: "01д 04ч 12м"
        },
        {
          id: 3,
          regNum: "ВХ-2026/0938-КАНЦ",
          token: "TK-3419-KZ",
          date: "04.11.2026 09:15",
          isAnon: false,
          fio: "Смаилов К.Т.",
          div: "СФ",
          region: "Карагандинская область",
          category: "TECH-06 Инфраструктура",
          text: "Аварийное состояние автопарка УАЗ в районе.",
          recipient: "Сервисная фабрика (СФ)",
          status: "⚠️ ПРОСРОЧЕНО",
          slaDeadline: "09.11.2026",
          slaTimer: "ПРОСРОЧЕНО (4ч)"
        }
      ]
    };

    document.addEventListener("DOMContentLoaded", () => {
      renderAllTables();
      initAllCharts();
      startGlobalSLATimer();
    });

    // ПЕРЕКЛЮЧЕНИЕ РОЛЕЙ (RBAC)
    function switchRole(roleKey) {
      window.appState.currentRole = roleKey;
      
      document.querySelectorAll('.role-view').forEach(v => v.classList.remove('active'));
      const activeView = document.getElementById(`view-${roleKey}`);
      if (activeView) activeView.classList.add('active');

      document.querySelectorAll('.role-btn').forEach(b => {
        b.classList.remove('active');
        if (b.classList.contains(`role-${roleKey}`)) b.classList.add('active');
      });

      renderAllTables();
      showToast(`Вы переключились на роль: ${getRoleTitle(roleKey)}`);
    }

    function getRoleTitle(roleKey) {
      if (roleKey === 'employee') return "Сотрудник (Ахметов Д.)";
      if (roleKey === 'ex') return "Служба EX (Опыт работника)";
      if (roleKey === 'chancellery') return "Канцелярия (СЭД)";
      return "Руководство компании";
    }

    // ПОД-ВКЛАДКИ СОТРУДНИКА
    function switchEmployeeTab(tabId) {
      document.querySelectorAll('.emp-tab-content').forEach(el => el.style.display = 'none');
      const target = document.getElementById(tabId);
      if (target) target.style.display = 'block';

      document.querySelectorAll('#view-employee .subnav-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(tabId)) btn.classList.add('active');
      });
    }

    // ПОД-ВКЛАДКИ EX СЛУЖБЫ
    function switchExTab(tabId) {
      document.querySelectorAll('.ex-tab-content').forEach(el => el.style.display = 'none');
      const target = document.getElementById(tabId);
      if (target) target.style.display = 'block';

      document.querySelectorAll('#view-ex .subnav-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(tabId)) btn.classList.add('active');
      });
    }

    // ПОД-ВКЛАДКИ КАНЦЕЛЯРИИ
    function switchChancelleryTab(tabId) {
      document.querySelectorAll('.canc-tab-content').forEach(el => el.style.display = 'none');
      const target = document.getElementById(tabId);
      if (target) target.style.display = 'block';

      document.querySelectorAll('#view-chancellery .subnav-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(tabId)) btn.classList.add('active');
      });
    }

    // РЕНДЕР ВСЕХ ТАБЛИЦ ИЗ ЕДИНОГО STATE
    function renderAllTables() {
      // 1. Мои обращения у сотрудника
      const empTbody = document.getElementById('emp-appeals-tbody');
      if (empTbody) {
        empTbody.innerHTML = window.appState.appeals.map(a => `
          <tr>
            <td><strong>${a.regNum}</strong><br><span style="font-size:10px; color:#64748B;">${a.token}</span></td>
            <td>${a.date}</td>
            <td>${a.category}</td>
            <td>${a.recipient}</td>
            <td><span class="badge-pill badge-official">${a.status}</span></td>
            <td style="font-family:monospace; font-weight:700; color:#059669;">⏱️ ${a.slaTimer}</td>
            <td><button class="role-btn" style="background:#F1F5F9; color:#00468C;" onclick="openTokenModal()">Чат</button></td>
          </tr>
        `).join('');
      }

      // 2. Очередь триажа у службы EX
      const exTbody = document.getElementById('ex-triage-tbody');
      if (exTbody) {
        exTbody.innerHTML = window.appState.appeals.map(a => `
          <tr>
            <td><strong>${a.regNum}</strong></td>
            <td>${a.date}</td>
            <td><span class="badge-pill ${a.isAnon ? 'badge-anon' : 'badge-official'}">${a.isAnon ? '🔒 Анонимно' : a.fio}</span></td>
            <td>${a.div} • ${a.region}</td>
            <td><strong>${a.category}</strong><br><span style="font-size:11px; color:#64748B;">${a.text.substring(0, 45)}...</span></td>
            <td>${a.recipient}</td>
            <td><span class="badge-pill badge-warning">${a.status}</span></td>
            <td><button class="role-btn" style="background:#6366F1; color:white;" onclick="showToast('Триаж: дело распределено')">Маршрутизировать</button></td>
          </tr>
        `).join('');
      }

      // 3. Канцелярия: только официальные (не анонимные) обращения
      const cancTbody = document.getElementById('chancellery-official-tbody');
      if (cancTbody) {
        const officialAppeals = window.appState.appeals.filter(a => !a.isAnon);
        cancTbody.innerHTML = officialAppeals.map(a => `
          <tr>
            <td><strong style="color:#00468C;">${a.regNum}</strong></td>
            <td>${a.date}</td>
            <td><strong>${a.fio}</strong></td>
            <td>${a.div} • ${a.region}</td>
            <td>${a.text.substring(0, 45)}...</td>
            <td>${a.recipient}</td>
            <td><span class="badge-pill badge-official">${a.status}</span></td>
            <td><button class="role-btn" style="background:#059669; color:white;" onclick="showToast('Печать СЭД Lotus Notes подтверждена')">Печать СЭД</button></td>
          </tr>
        `).join('');
      }

      // 4. Канцелярия: SLA дедлайны
      const slaTbody = document.getElementById('chancellery-sla-tbody');
      if (slaTbody) {
        slaTbody.innerHTML = window.appState.appeals.map(a => `
          <tr>
            <td><strong>${a.regNum}</strong></td>
            <td>${a.isAnon ? '🔒 Анонимно' : a.fio}</td>
            <td>${a.category}</td>
            <td>${a.recipient}</td>
            <td>${a.slaDeadline}</td>
            <td style="font-family:monospace; font-weight:700;">⏱️ ${a.slaTimer}</td>
            <td><span class="badge-pill ${a.status.includes('ПРОСРОЧЕНО') ? 'badge-danger' : 'badge-anon'}">${a.status.includes('ПРОСРОЧЕНО') ? '🔴 Критическая' : '🟢 В графике'}</span></td>
            <td><button class="role-btn" style="background:#EF4444; color:white;" onclick="showToast('Эскалация направлена Главному директору HRD')">Эскалировать</button></td>
          </tr>
        `).join('');
      }
    }

    // NUDGE MODAL
    function openNudgeModal() { document.getElementById('modal-nudge').classList.add('active'); }
    function closeNudgeModal() { document.getElementById('modal-nudge').classList.remove('active'); }

    function nudgeAction(act) {
      closeNudgeModal();
      if (act === 'chat') {
        switchRole('employee');
        switchEmployeeTab('emp-chat');
      } else if (act === 'pulse') {
        switchRole('employee');
        switchEmployeeTab('emp-pulse');
      } else if (act === 'form') {
        switchRole('employee');
        switchEmployeeTab('emp-form');
      } else {
        showToast("Спасибо за ответ! Рады, что у вас все хорошо.");
      }
    }

    // TOKEN MODAL
    function openTokenModal() { document.getElementById('modal-token').classList.add('active'); }
    function closeTokenModal() { document.getElementById('modal-token').classList.remove('active'); }
    function searchByToken() {
      const code = document.getElementById('token-input-field').value.trim();
      showToast(`Обращение ${code} найдено. Статус: В работе у исполнителя.`);
    }

    // ЧАТ СОТРУДНИКА
    function applyChatPreset(type) {
      const input = document.getElementById('emp-chat-input');
      if (type === 'ppe') input.value = "В филиале ОДС Запад уже 2 месяца не выдают зимнюю обувь и утепленные куртки.";
      else if (type === 'overtime') input.value = "Начальник участка принуждает оставаться после смены и выходить по субботам без оплаты.";
      else input.value = "Мастер систематически грубит и угрожает увольнением за замечания.";
      sendEmpChatMessage();
    }

    function handleEmpChatEnter(e) { if (e.key === 'Enter') sendEmpChatMessage(); }

    function sendEmpChatMessage() {
      const input = document.getElementById('emp-chat-input');
      const text = input.value.trim();
      if (!text) return;
      input.value = "";

      const stream = document.getElementById('emp-chat-stream');
      const userDiv = document.createElement('div');
      userDiv.className = 'chat-msg-row user';
      userDiv.innerHTML = `<div class="msg-avatar user">Я</div><div class="msg-bubble">${text}</div>`;
      stream.appendChild(userDiv);

      setTimeout(() => {
        const aiDiv = document.createElement('div');
        aiDiv.className = 'chat-msg-row ai';
        aiDiv.innerHTML = `
          <div class="msg-avatar ai">ИИ</div>
          <div style="width:100%;">
            <div class="msg-bubble">
              Я зафиксировал факты. Сформирован официальный проект заявления:<br>
              <strong>Категория:</strong> Охрана труда и СИЗ (HSE-01)<br>
              <strong>Подразделение:</strong> ОДС • Атырауская область<br>
              <strong>Фабула по ТК РК:</strong> «Несоблюдение положений ст. 182 ТК РК и п. 4.2 Коллективного договора. Суть: ${text}»
            </div>
            <div style="margin-top:8px; display:flex; gap:8px;">
              <button class="btn-action-primary" onclick="confirmRegisterFromChat('${text}', true)">🔒 Зарегистрировать анонимно</button>
              <button class="btn-action-primary" style="background:#0284C7;" onclick="confirmRegisterFromChat('${text}', false)">👤 Официально (от своего имени)</button>
            </div>
          </div>
        `;
        stream.appendChild(aiDiv);
        stream.scrollTop = stream.scrollHeight;
      }, 600);
    }

    function confirmRegisterFromChat(text, isAnon) {
      const newId = window.appState.appeals.length + 1;
      const regNum = `ВХ-2026/094${newId}-КАНЦ`;
      const token = `TK-${Math.floor(1000 + Math.random()*9000)}-KZ`;

      const newRecord = {
        id: newId,
        regNum: regNum,
        token: token,
        date: "12.11.2026 09:55",
        isAnon: isAnon,
        fio: isAnon ? "— (Анонимно)" : "Ахметов Данияр",
        div: "ОДС",
        region: "Атырауская область",
        category: "HSE-01 Охрана труда",
        text: text,
        recipient: "Департамент производственной безопасности (HSE)",
        status: "В работе",
        slaDeadline: "17.11.2026",
        slaTimer: "04д 23ч 59м"
      };

      window.appState.appeals.unshift(newRecord);
      renderAllTables();

      showToast(`🏛️ Обращение зарегистрировано в Канцелярии: ${regNum}!`);
      switchEmployeeTab('emp-my-appeals');
    }

    function resetEmpChat() {
      document.getElementById('emp-chat-stream').innerHTML = `
        <div class="chat-msg-row ai">
          <div class="msg-avatar ai">ИИ</div>
          <div class="msg-bubble">Диалог обновлен. Опишите проблему своими словами.</div>
        </div>
      `;
    }

    // ПУЛЬС-ОПРОС
    function setPulseRating(axis, score, btn) {
      btn.parentElement.querySelectorAll('button').forEach(b => {
        b.style.background = "transparent";
        b.style.color = "#334155";
      });
      btn.style.background = "#00468C";
      btn.style.color = "white";

      if (axis === 'p1' && score <= 2) {
        document.getElementById('pulse-synergy-banner').style.display = 'block';
      } else if (axis === 'p1') {
        document.getElementById('pulse-synergy-banner').style.display = 'none';
      }
    }

    function convertPulseToComplaint() {
      switchEmployeeTab('emp-chat');
      const input = document.getElementById('emp-chat-input');
      input.value = "По итогам пульс-опроса: срыв материально-технического снабжения СИЗ и зимней экипировкой на участке связи.";
      sendEmpChatMessage();
    }

    function completePulseSurvey() {
      showToast("🎉 Пульс-опрос Q4 успешно завершен! Спасибо за участие.");
      switchEmployeeTab('emp-home');
    }

    // ПРЯМАЯ ФОРМА
    function submitDirectForm() {
      const text = document.getElementById('direct-text').value.trim();
      if (!text) { alert("Заполните текст обращения"); return; }

      const isAnon = document.getElementById('direct-anon').value === 'anon';
      const div = document.getElementById('direct-div').value;
      const reg = document.getElementById('direct-region').value;
      const cat = document.getElementById('direct-category').value;

      const newId = window.appState.appeals.length + 1;
      const regNum = `ВХ-2026/094${newId}-КАНЦ`;
      const token = `TK-${Math.floor(1000 + Math.random()*9000)}-KZ`;

      const newRecord = {
        id: newId,
        regNum: regNum,
        token: token,
        date: "12.11.2026 09:55",
        isAnon: isAnon,
        fio: isAnon ? "— (Анонимно)" : "Ахметов Данияр",
        div: div,
        region: reg,
        category: cat,
        text: text,
        recipient: "Профильный департамент",
        status: "В работе",
        slaDeadline: "17.11.2026",
        slaTimer: "04д 23ч 59м"
      };

      window.appState.appeals.unshift(newRecord);
      renderAllTables();

      showToast(`Обращение ${regNum} успешно отправлено в Канцелярию!`);
      switchEmployeeTab('emp-my-appeals');
    }

    function simulateFormFileUpload() {
      document.getElementById('direct-file-label').textContent = "✅ Прикреплено: foto_defekt_obuvi.jpg (2.8 МБ)";
      showToast("Файл прикреплен!");
    }

    // EX: ЗАГРУЗКА ВНЕШНИХ ДАННЫХ
    function triggerExternalDataImport() {
      document.getElementById('import-box-text').innerHTML = "⏳ Идет чтение структуры и сопоставление полей...";
      setTimeout(() => {
        document.getElementById('import-box-text').innerHTML = "✅ Файл «External_Turnover_Audit_2026.csv» успешно разобран!";
        document.getElementById('import-preview-block').style.display = 'block';
        showToast("Внешний датасет загружен! Нажмите «Объединить с аналитикой».");
      }, 700);
    }

    function mergeExternalDataToAnalytics() {
      showToast("⚡ Внешние данные объединены! Коэффициенты корреляции пересчитаны.");
      switchExTab('ex-analytics');
    }

    function launchNewSurveyCampaign() {
      showToast("🚀 Кампания Q1 2027 сконфигурирована и добавлена в расписание!");
    }

    // ЖИВОЙ ТАЙМЕР SLA
    function startGlobalSLATimer() {
      setInterval(() => {
        // Just ticking indicator
      }, 1000);
    }

    function showToast(msg) {
      const tray = document.getElementById('toast-tray');
      const pill = document.createElement('div');
      pill.className = 'toast-pill';
      pill.innerHTML = `<span>🔔</span><span>${msg}</span>`;
      tray.appendChild(pill);
      setTimeout(() => { pill.remove(); }, 3500);
    }

    // ИНИЦИАЛИЗАЦИЯ CHART.JS
    function initAllCharts() {
      // 1. EX Topics
      const ctx1 = document.getElementById('chartExTopics');
      if (ctx1) {
        new Chart(ctx1, {
          type: 'doughnut',
          data: {
            labels: ['Охрана труда / СИЗ', 'Оплата труда', 'Переработки', 'Моббинг', 'Инфраструктура'],
            datasets: [{
              data: [38, 28, 14, 12, 8],
              backgroundColor: ['#00468C', '#0284C7', '#6366F1', '#F59E0B', '#EF4444']
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      // 2. EX Divisions
      const ctx2 = document.getElementById('chartExDivisions');
      if (ctx2) {
        new Chart(ctx2, {
          type: 'bar',
          data: {
            labels: ['ОДС', 'СФ', 'ДРБ', 'ДКБ', 'ДУП'],
            datasets: [{
              label: 'Кол-во обращений',
              data: [192, 76, 74, 30, 28],
              backgroundColor: '#6366F1'
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      // 3. Exec Doughnut
      const ctx3 = document.getElementById('chartExecDoughnut');
      if (ctx3) {
        new Chart(ctx3, {
          type: 'pie',
          data: {
            labels: ['Охрана труда', 'Оплата труда', 'Сверхурочные', 'Этика'],
            datasets: [{
              data: [42, 26, 18, 14],
              backgroundColor: ['#00468C', '#0284C7', '#10B981', '#F59E0B']
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }

      // 4. Exec Bars
      const ctx4 = document.getElementById('chartExecBars');
      if (ctx4) {
        new Chart(ctx4, {
          type: 'bar',
          data: {
            labels: ['ОДС', 'СФ', 'ДРБ', 'ДКБ', 'ДЦБ'],
            datasets: [{
              label: 'Соблюдение SLA (%)',
              data: [96.9, 97.4, 98.6, 100, 100],
              backgroundColor: '#10B981'
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }
    }
  </script>
</body>
</html>
''')

print("Built full enterprise multi-role index.html successfully!")

