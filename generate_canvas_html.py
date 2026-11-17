# -*- coding: utf-8 -*-
"""
Generator for index.html - Master Canvas:
«ИИ-Приемная обращений, регулярные пульс-опросы и мониторинг социального климата АО «Казахтелеком»»

Полное соответствие ТЗ Версии 6.0:
1. Авторизация через корпоративный CDN / SSO (Ахметов Данияр, ОДС Западная РДТ)
2. Всплывающее модальное окно вовлечения (Wellness Check-in / Nudge Modal):
   «Все ли у вас в порядке? Есть ли проблемы? Хотите поговорить?»
3. Модуль Ежеквартального пульс-опроса (3 блока: климат, отношение к компании, атмосфера в коллективе)
   с переходом в жалобу при оценках 1-2 балла
4. Диалог с ИИ-агентом (свободный ввод -> адаптивный опросник -> заявление по ТК РК -> анонимность -> регистрация Канцелярией -> SLA)
5. Раздел самостоятельного заведения обращения (Self-service Form с дивизионом, 20 регионами, файлами)
6. Реестр Канцелярии (Lotus Notes) и живой контроль сроков (SLA-таймеры)
7. Панель руководства: аналитический отчет On-Premise LLM, тепловая карта регионов и дашборды
8. Персональный кабинет по токену TK-XXXX-KZ с двухсторонней анонимной перепиской
"""

canvas_html = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ИИ-Приемная и Пульс-Мониторинг Климата | АО «Казахтелеком»</title>
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
      --accent-purple: #6366F1;
      --success: #10B981;
      --warning: #F59E0B;
      --danger: #EF4444;
      --bg-slate: #F8FAFC;
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

    /* TOP GLOBAL CONTROLLER NAVBAR */
    .canvas-topbar {
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

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-logo-badge {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      font-weight: 800;
      font-size: 13px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
      box-shadow: 0 2px 8px rgba(0, 70, 140, 0.5);
    }

    .brand-info h1 {
      font-size: 13.5px;
      font-weight: 800;
      color: #F8FAFC;
      letter-spacing: -0.2px;
    }

    .brand-info span {
      font-size: 11px;
      color: #94A3B8;
    }

    /* Top Navigation Tabs */
    .canvas-nav-tabs {
      display: flex;
      background: rgba(255, 255, 255, 0.08);
      padding: 4px;
      border-radius: var(--radius-full);
      gap: 4px;
    }

    .nav-tab-btn {
      background: transparent;
      border: none;
      color: #CBD5E1;
      padding: 7px 14px;
      font-size: 12px;
      font-weight: 600;
      border-radius: var(--radius-full);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .nav-tab-btn:hover {
      color: white;
      background: rgba(255, 255, 255, 0.12);
    }

    .nav-tab-btn.active {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4);
    }

    /* Topbar Right Actions (CDN User Pill) */
    .topbar-right-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .cdn-user-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-size: 11.5px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .cdn-user-pill:hover {
      background: rgba(255, 255, 255, 0.18);
    }

    .cdn-badge-indicator {
      width: 8px;
      height: 8px;
      background: #10B981;
      border-radius: 50%;
      box-shadow: 0 0 6px #10B981;
    }

    .btn-nudge-trigger {
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

    .btn-nudge-trigger:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(245, 158, 11, 0.6);
    }

    /* MAIN WORKSPACE VIEWPORT */
    .canvas-viewport {
      flex: 1;
      display: flex;
      justify-content: center;
      padding: 20px 24px 40px 24px;
      background: #F1F5F9;
      position: relative;
    }

    .canvas-screen {
      display: none;
      width: 100%;
      max-width: 1360px;
      animation: fadeIn 0.3s ease;
    }

    .canvas-screen.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ==============================================================
       CANVAS 1: CDN PORTAL OVERVIEW (ГЛАВНАЯ СТРАНИЦА И ЧЕКИН)
       ============================================================== */
    .portal-banner-hero {
      background: linear-gradient(135deg, #002D5C 0%, #00468C 50%, #0284C7 100%);
      color: white;
      border-radius: var(--radius-lg);
      padding: 24px 30px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-md);
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      overflow: hidden;
    }

    .portal-banner-hero::after {
      content: '';
      position: absolute;
      right: -40px;
      bottom: -40px;
      width: 220px;
      height: 220px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 50%;
    }

    .hero-text-col h2 {
      font-size: 20px;
      font-weight: 800;
      margin-bottom: 6px;
    }

    .hero-text-col p {
      font-size: 13px;
      color: #BAE6FD;
      max-width: 650px;
      line-height: 1.5;
    }

    .portal-action-tiles-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }

    .action-tile-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 18px;
      cursor: pointer;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 160px;
      position: relative;
      overflow: hidden;
    }

    .action-tile-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
      border-color: var(--accent);
    }

    .action-tile-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
    }

    .tile-pulse::before { background: #6366F1; }
    .tile-chat::before { background: #00468C; }
    .tile-form::before { background: #0284C7; }
    .tile-chancellery::before { background: #10B981; }

    .tile-icon {
      font-size: 26px;
      margin-bottom: 8px;
    }

    .tile-title {
      font-size: 14px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 4px;
    }

    .tile-desc {
      font-size: 11.5px;
      color: var(--text-muted);
      line-height: 1.4;
    }

    .tile-footer {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 8px;
    }

    /* ==============================================================
       CANVAS 2: ДИАЛОГ С ИИ-АГЕНТОМ (ПРИЕМНАЯ)
       ============================================================== */
    .chat-layout-wrapper {
      max-width: 940px;
      margin: 0 auto;
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-lg);
      display: flex;
      flex-direction: column;
      height: calc(100vh - 120px);
      overflow: hidden;
    }

    .chat-header {
      padding: 14px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #FFFFFF;
    }

    .ai-avatar-circle {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: #E0F2FE;
      color: #0284C7;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 15px;
      border: 1.5px solid #BAE6FD;
      position: relative;
    }

    .ai-avatar-circle::after {
      content: '';
      position: absolute;
      bottom: 0;
      right: 0;
      width: 10px;
      height: 10px;
      background: var(--success);
      border-radius: 50%;
      border: 2px solid white;
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

    .chat-msg-row {
      display: flex;
      gap: 12px;
      max-width: 90%;
    }

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

    .msg-content-wrapper { display: flex; flex-direction: column; gap: 6px; }

    .msg-bubble {
      padding: 12px 16px;
      border-radius: var(--radius-lg);
      font-size: 13.5px;
      line-height: 1.5;
    }

    .chat-msg-row.ai .msg-bubble {
      background: #FFFFFF;
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
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: var(--radius-md);
      padding: 10px 14px;
      font-size: 12.5px;
      color: #334155;
      cursor: pointer;
      display: flex;
      align-items: flex-start;
      gap: 10px;
      transition: all 0.2s;
      box-shadow: var(--shadow-sm);
      margin-bottom: 6px;
    }

    .quick-chip:hover {
      border-color: #0284C7;
      background: #F0F9FF;
      transform: translateY(-1px);
    }

    .badge-hse { background: #FEF3C7; color: #92400E; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
    .badge-labor { background: #EDE9FE; color: #5B21B6; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
    .badge-infra { background: #FEE2E2; color: #991B1B; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; }

    /* Statement preview card */
    .formal-statement-card {
      background: #FFFFFF;
      border: 2px solid #00468C;
      border-radius: var(--radius-md);
      padding: 18px;
      box-shadow: var(--shadow-lg);
      margin-top: 8px;
    }

    /* Live SLA Timer */
    .sla-timer-widget {
      background: linear-gradient(135deg, #0F172A, #1E293B);
      color: white;
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-top: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .sla-countdown-digits {
      font-size: 22px;
      font-weight: 800;
      font-family: monospace;
      color: #34D399;
      letter-spacing: 1px;
    }

    /* Chat bottom input */
    .chat-input-container {
      padding: 12px 20px;
      border-top: 1px solid var(--border);
      background: #FFFFFF;
    }

    .chat-input-box {
      display: flex;
      align-items: center;
      background: #F8FAFC;
      border: 1.5px solid #CBD5E1;
      border-radius: var(--radius-full);
      padding: 4px 8px 4px 16px;
    }

    .chat-input-field {
      flex: 1;
      border: none;
      background: transparent;
      outline: none;
      font-size: 13.5px;
      padding: 8px 4px;
    }

    .chat-send-btn {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #00468C;
      color: white;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s;
    }

    .chat-send-btn:hover { background: #0284C7; transform: scale(1.05); }

    /* ==============================================================
       CANVAS 3: КВАРТАЛЬНЫЙ ПУЛЬС-ОПРОС
       ============================================================== */
    .pulse-survey-card {
      max-width: 860px;
      margin: 0 auto;
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-md);
      padding: 28px;
    }

    .pulse-block-section {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 20px;
    }

    .pulse-block-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-bottom: 8px;
      border-bottom: 1px solid #E2E8F0;
    }

    .pulse-scale-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 10px;
      margin: 12px 0;
    }

    .pulse-scale-btn {
      padding: 10px;
      border: 1.5px solid #CBD5E1;
      border-radius: var(--radius-sm);
      background: white;
      text-align: center;
      cursor: pointer;
      transition: all 0.15s;
    }

    .pulse-scale-btn:hover { border-color: var(--accent); background: #F0F9FF; }
    .pulse-scale-btn.selected { border-color: #00468C; background: #EBF3FA; box-shadow: 0 0 0 2px rgba(0, 70, 140, 0.2); }

    .pulse-score-digit { font-size: 16px; font-weight: 800; color: #00468C; display: block; }
    .pulse-score-text { font-size: 10px; color: var(--text-muted); font-weight: 600; }

    /* Synergy alert banner in pulse */
    .synergy-appeal-prompt {
      display: none;
      background: #FEF2F2;
      border: 1.5px solid #FCA5A5;
      border-radius: var(--radius-md);
      padding: 14px 18px;
      margin-top: 14px;
      animation: fadeIn 0.3s ease;
    }

    /* ==============================================================
       CANVAS 4: САМОСТОЯТЕЛЬНАЯ ФОРМА ОБРАЩЕНИЯ (SELF-SERVICE)
       ============================================================== */
    .self-service-form-card {
      max-width: 900px;
      margin: 0 auto;
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-md);
      padding: 28px;
    }

    .form-grid-2col {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }

    .form-label {
      display: block;
      font-size: 12px;
      font-weight: 700;
      color: #334155;
      margin-bottom: 6px;
    }

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

    .file-dropzone {
      border: 2px dashed #94A3B8;
      border-radius: var(--radius-md);
      padding: 20px;
      text-align: center;
      background: #F8FAFC;
      cursor: pointer;
      transition: all 0.2s;
    }

    .file-dropzone:hover {
      border-color: var(--accent);
      background: #F0F9FF;
    }

    /* ==============================================================
       CANVAS 5 & 6: КАНЦЕЛЯРИЯ, РЕЕСТР И ПАНЕЛЬ РУКОВОДСТВА
       ============================================================== */
    .appeals-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
      background: white;
    }

    .appeals-table th {
      background: #F8FAFC;
      padding: 12px 14px;
      font-weight: 700;
      color: #475569;
      text-align: left;
      border-bottom: 1.5px solid var(--border);
    }

    .appeals-table td {
      padding: 12px 14px;
      border-bottom: 1px solid #F1F5F9;
      vertical-align: middle;
    }

    .appeals-table tr:hover td { background: #F8FAFC; }

    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
    }

    .status-work { background: #E0F2FE; color: #0369A1; }
    .status-closed { background: #DCFCE7; color: #15803D; }

    .btn-action-primary {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .btn-action-primary:hover { opacity: 0.95; transform: translateY(-1px); }

    /* ==============================================================
       MODAL: CDN WELLNESS CHECK-IN (NUDGE MODAL)
       ============================================================== */
    .modal-backdrop-nudge {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(5px);
      z-index: 3000;
      align-items: center;
      justify-content: center;
    }

    .modal-backdrop-nudge.active { display: flex; animation: fadeIn 0.25s ease; }

    .nudge-modal-card {
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      padding: 28px;
      max-width: 580px;
      width: 90%;
      box-shadow: var(--shadow-xl);
      border: 1.5px solid var(--border);
      position: relative;
    }

    .nudge-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
    }

    .nudge-avatar-pulse {
      width: 48px;
      height: 48px;
      background: #EBF3FA;
      color: #00468C;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      border: 2px solid #BAE6FD;
    }

    .nudge-options-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 18px;
    }

    .nudge-option-btn {
      background: #F8FAFC;
      border: 1.5px solid #CBD5E1;
      border-radius: var(--radius-md);
      padding: 14px 16px;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: all 0.2s;
    }

    .nudge-option-btn:hover {
      border-color: #0284C7;
      background: #F0F9FF;
      transform: translateX(4px);
    }

    /* Toast Notification */
    .toast-container {
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

  <!-- ==================== ВЕРХНЯЯ ГЛОБАЛЬНАЯ ПАНЕЛЬ (CDN ШЛЮЗ) ==================== -->
  <header class="canvas-topbar">
    <div class="brand-group">
      <div class="brand-logo-badge">КТ СМСК</div>
      <div class="brand-info">
        <h1>ИИ-Приемная и Пульс-Мониторинг Климата</h1>
        <span>АО «Казахтелеком» • Центр социального партнерства и мониторинга</span>
      </div>
    </div>

    <!-- Вкладки Канваса -->
    <nav class="canvas-nav-tabs">
      <button class="nav-tab-btn active" onclick="switchCanvasTab('tab-portal')">
        🏠 Портал CDN
      </button>
      <button class="nav-tab-btn" onclick="switchCanvasTab('tab-chat')">
        💬 Диалог с ИИ (Жалоба)
      </button>
      <button class="nav-tab-btn" onclick="switchCanvasTab('tab-pulse')">
        📊 Пульс-Опрос (Q4)
      </button>
      <button class="nav-tab-btn" onclick="switchCanvasTab('tab-form')">
        📝 Прямой ввод (Форма)
      </button>
      <button class="nav-tab-btn" onclick="switchCanvasTab('tab-chancellery')">
        📋 Канцелярия & SLA
      </button>
      <button class="nav-tab-btn" onclick="switchCanvasTab('tab-executive')">
        📈 Панель руководства
      </button>
    </nav>

    <!-- Правый блок: CDN авторизация и триггер чекина -->
    <div class="topbar-right-actions">
      <button class="btn-nudge-trigger" onclick="openNudgeModal()">
        💬 Вовлекающий Чекин
      </button>
      <div class="cdn-user-pill" title="Авторизован в корпоративной сети CDN" onclick="toggleCDNProfileModal()">
        <div class="cdn-badge-indicator"></div>
        <span>Ахметов Д.Б. (ОДС Запад)</span>
      </div>
    </div>
  </header>

  <!-- ==================== ОСНОВНОЙ ВЬЮПОРТ КАНВАСА ==================== -->
  <main class="canvas-viewport">

    <!-- ==================== ЭКРАН 1: ПОРТАЛ CDN И ОБЗОР ==================== -->
    <section id="tab-portal" class="canvas-screen active">
      
      <!-- Приветственный баннер -->
      <div class="portal-banner-hero">
        <div class="hero-text-col">
          <h2>Сәлеметсіз бе, Данияр Бауыржанұлы!</h2>
          <p>
            Добро пожаловать в единый центр заботы о сотрудниках АО «Казахтелеком». 
            Здесь вы можете пройти регулярный ежеквартальный срез климата, открыто сообщить о проблемах условий труда или подать официальное обращение в Канцелярию со 100% гарантией защиты заявителя.
          </p>
        </div>
        <button class="btn-action-primary" style="background: white; color: #00468C;" onclick="openNudgeModal()">
          💬 Начать чекин-диалог
        </button>
      </div>

      <!-- Карточки ключевых сценариев (4 плитки) -->
      <div class="portal-action-tiles-grid">
        <div class="action-tile-card tile-pulse" onclick="switchCanvasTab('tab-pulse')">
          <div>
            <div class="tile-icon">📊</div>
            <div class="tile-title">Пульс-опрос Q4 2026</div>
            <div class="tile-desc">Ежеквартальный срез климата: отношение к компании, психологическая безопасность и условия труда (60 сек).</div>
          </div>
          <div class="tile-footer">Пройти опрос →</div>
        </div>

        <div class="action-tile-card tile-chat" onclick="switchCanvasTab('tab-chat')">
          <div>
            <div class="tile-icon">💬</div>
            <div class="tile-title">Диалог с ИИ-Агентом</div>
            <div class="tile-desc">Опишите проблему своими словами. ИИ задаст 3 вопроса и подготовит официальное заявление со статьями ТК РК.</div>
          </div>
          <div class="tile-footer">Начать диалог →</div>
        </div>

        <div class="action-tile-card tile-form" onclick="switchCanvasTab('tab-form')">
          <div>
            <div class="tile-icon">📝</div>
            <div class="tile-title">Самостоятельная подача</div>
            <div class="tile-desc">Прямой ввод заявления без чат-бота: выберите дивизион, регион, прикрепите файлы и зарегистрируйте в Канцелярии.</div>
          </div>
          <div class="tile-footer">Заполнить форму →</div>
        </div>

        <div class="action-tile-card tile-chancellery" onclick="switchCanvasTab('tab-chancellery')">
          <div>
            <div class="tile-icon">📋</div>
            <div class="tile-title">Реестр Канцелярии & SLA</div>
            <div class="tile-desc">Сквозной журнал входящих документов (Lotus Notes), таймеры дедлайнов (5 дней) и проверка статуса по токену.</div>
          </div>
          <div class="tile-footer">Открыть реестр →</div>
        </div>
      </div>

      <!-- Блок информации о правах и защите заявителя -->
      <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; box-shadow: var(--shadow-sm); display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; gap: 14px; align-items: center;">
          <div style="font-size: 32px;">🛡️</div>
          <div>
            <h3 style="font-size: 14px; font-weight: 700; color: #0F172A;">Политика «Нулевой терпимости» к давлению и моббингу</h3>
            <p style="font-size: 12px; color: var(--text-muted); max-width: 800px;">
              АО «Казахтелеком» гарантирует абсолютную защиту сотрудников от преследования за критику или сообщения о нарушениях. Вы вправе подать любое обращение анонимно с выдачей защищенного токена доступа.
            </p>
          </div>
        </div>
        <button class="btn-action-primary" style="background: #F1F5F9; color: #334155;" onclick="openTokenModal()">
          🔍 Проверить тикет по токену
        </button>
      </div>

    </section>

    <!-- ==================== ЭКРАН 2: ДИАЛОГ С ИИ-АГЕНТОМ ПО ОБРАЩЕНИЯМ ==================== -->
    <section id="tab-chat" class="canvas-screen">
      <div class="chat-layout-wrapper">
        
        <div class="chat-header">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div class="ai-avatar-circle">ИИ</div>
            <div>
              <h2 style="font-size: 14.5px; font-weight: 800; color: #0F172A;">Интеллектуальный ассистент приема обращений</h2>
              <span style="font-size: 11px; color: #10B981;">● Локальный On-Premise контур • Защищенный прием</span>
            </div>
          </div>
          <button class="btn-action-primary" style="padding: 6px 12px; font-size: 12px; background: #F1F5F9; color: #475569;" onclick="resetChatFlow()">
            🔄 Начать диалог заново
          </button>
        </div>

        <div class="chat-stream-body" id="chat-stream-box">
          
          <div class="chat-msg-row ai">
            <div class="msg-avatar ai">ИИ</div>
            <div class="msg-content-wrapper">
              <div class="msg-bubble">
                Сәлеметсіз бе, Данияр! Я корпоративный ИИ-ассистент АО «Казахтелеком».<br><br>
                Опишите своими словами, с какой проблемой или несправедливостью на рабочем месте вы столкнулись (задержка зимней обуви/СИЗ, неоплаченные переработки, давление руководства, аварийность техники).<br><br>
                Я задам вам 3 уточняющих вопроса, составлю официальное заявление и помогу зарегистрировать его в Канцелярии.
              </div>
              <div style="font-size: 11px; color: #94A3B8;">Только что</div>

              <div id="quick-chips-container" style="margin-top: 10px;">
                <div style="font-size: 11px; color: #64748B; font-weight: 700; margin-bottom: 6px;">💡 Выберите пример для быстрого тестирования:</div>
                <div class="quick-chip" onclick="applyPreset('ppe')">
                  <span class="badge-hse">Охрана труда</span>
                  <div><strong>Задержка зимней обуви и спецодежды:</strong> «В ОДС Запад уже 2 месяца не выдают зимнюю обувь монтерам, на складе говорят ждать...»</div>
                </div>
                <div class="quick-chip" onclick="applyPreset('overtime')">
                  <span class="badge-labor">Оплата труда</span>
                  <div><strong>Неоплачиваемые сверхурочные по субботам:</strong> «Начальник участка заставляет выходить по субботам без табелирования и оплаты...»</div>
                </div>
                <div class="quick-chip" onclick="applyPreset('mobbing')">
                  <span class="badge-infra">Этика / Моббинг</span>
                  <div><strong>Давление и угрозы мастера:</strong> «Мастер систематически грубит, угрожает лишением премии за любые замечания...»</div>
                </div>
              </div>

            </div>
          </div>

          <div id="chat-dynamic-injections"></div>

        </div>

        <div class="chat-input-container">
          <div class="chat-input-box">
            <input type="text" id="chat-text-input" class="chat-input-field" placeholder="Опишите проблему своими словами или выберите сценарий выше..." onkeypress="handleChatEnter(event)">
            <button class="chat-send-btn" onclick="sendChatProblem()">➤</button>
          </div>
        </div>

      </div>
    </section>

    <!-- ==================== ЭКРАН 3: КВАРТАЛЬНЫЙ ПУЛЬС-ОПРОС ==================== -->
    <section id="tab-pulse" class="canvas-screen">
      <div class="pulse-survey-card">
        
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 14px; margin-bottom: 20px;">
          <div>
            <h2 style="font-size: 18px; font-weight: 800; color: #00468C;">Ежеквартальный пульс-опрос социального климата (Q4 2026)</h2>
            <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
              Уведомление направлено в Push, Outlook и Lotus Notes. Прохождение занимает 60–90 секунд.
            </p>
          </div>
          <span style="background: #E0F2FE; color: #0369A1; font-size: 11.5px; font-weight: 700; padding: 4px 10px; border-radius: var(--radius-full);">
            🔒 Строго анонимно
          </span>
        </div>

        <!-- БЛОК 1: Климат и условия -->
        <div class="pulse-block-section">
          <div class="pulse-block-header">
            <h3 style="font-size: 14px; font-weight: 700; color: #0F172A;">1. Социальный климат и условия труда</h3>
            <span style="font-size: 11px; color: var(--text-muted);">Блок 1 из 3</span>
          </div>
          <p style="font-size: 13px; color: #334155; margin-bottom: 8px;">
            «Материально-техническое снабжение (СИЗ, инструменты, спецодежда, транспорт) позволяет мне безопасно выполнять работу»:
          </p>
          <div class="pulse-scale-grid">
            <div class="pulse-scale-btn" onclick="selectPulseScore('b1', 1, this)">
              <span class="pulse-score-digit">1</span>
              <span class="pulse-score-text">Совсем нет</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b1', 2, this)">
              <span class="pulse-score-digit">2</span>
              <span class="pulse-score-text">Скорее нет</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b1', 3, this)">
              <span class="pulse-score-digit">3</span>
              <span class="pulse-score-text">Средне</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b1', 4, this)">
              <span class="pulse-score-digit">4</span>
              <span class="pulse-score-text">Скорее да</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b1', 5, this)">
              <span class="pulse-score-digit">5</span>
              <span class="pulse-score-text">Полностью</span>
            </div>
          </div>
          <!-- Synergy Alert Trigger -->
          <div class="synergy-appeal-prompt" id="synergy-alert-b1">
            <div style="display: flex; gap: 10px; align-items: center;">
              <span style="font-size: 20px;">⚠️</span>
              <div style="flex: 1;">
                <strong style="color: #991B1B; font-size: 12.5px;">Вы указали низкий балл по условиям труда.</strong>
                <p style="font-size: 12px; color: #7F1D1D; margin-top: 2px;">
                  Желаете ли вы прямо сейчас оформить это как официальное обращение в Канцелярию для срочного устранения нарушения?
                </p>
              </div>
              <button class="btn-action-primary" style="background: #DC2626; padding: 6px 12px; font-size: 12px;" onclick="convertPulseToAppeal('HSE-01', 'Срыв сроков обеспечения зимними СИЗ и спецодеждой')">
                Передать в Канцелярию →
              </button>
            </div>
          </div>
        </div>

        <!-- БЛОК 2: Отношение к компании -->
        <div class="pulse-block-section">
          <div class="pulse-block-header">
            <h3 style="font-size: 14px; font-weight: 700; color: #0F172A;">2. Отношение к компании (Лояльность и eNPS)</h3>
            <span style="font-size: 11px; color: var(--text-muted);">Блок 2 из 3</span>
          </div>
          <p style="font-size: 13px; color: #334155; margin-bottom: 8px;">
            «Я доверяю решениям руководства компании и готов рекомендовать „Казахтелеком“ как надежного работодателя»:
          </p>
          <div class="pulse-scale-grid">
            <div class="pulse-scale-btn" onclick="selectPulseScore('b2', 1, this)">
              <span class="pulse-score-digit">1</span>
              <span class="pulse-score-text">Категорически нет</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b2', 2, this)">
              <span class="pulse-score-digit">2</span>
              <span class="pulse-score-text">Скорее нет</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b2', 3, this)">
              <span class="pulse-score-digit">3</span>
              <span class="pulse-score-text">Нейтрально</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b2', 4, this)">
              <span class="pulse-score-digit">4</span>
              <span class="pulse-score-text">Да, доверяю</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b2', 5, this)">
              <span class="pulse-score-digit">5</span>
              <span class="pulse-score-text">Полностью горжусь</span>
            </div>
          </div>
        </div>

        <!-- БЛОК 3: Атмосфера в коллективе -->
        <div class="pulse-block-section">
          <div class="pulse-block-header">
            <h3 style="font-size: 14px; font-weight: 700; color: #0F172A;">3. Атмосфера в коллективе и психологическая безопасность</h3>
            <span style="font-size: 11px; color: var(--text-muted);">Блок 3 из 3</span>
          </div>
          <p style="font-size: 13px; color: #334155; margin-bottom: 8px;">
            «В нашем коллективе царит уважительная атмосфера, я не сталкиваюсь с грубостью, давлением или угрозами начальства»:
          </p>
          <div class="pulse-scale-grid">
            <div class="pulse-scale-btn" onclick="selectPulseScore('b3', 1, this)">
              <span class="pulse-score-digit">1</span>
              <span class="pulse-score-text">Постоянный прессинг</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b3', 2, this)">
              <span class="pulse-score-digit">2</span>
              <span class="pulse-score-text">Часто бывает</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b3', 3, this)">
              <span class="pulse-score-digit">3</span>
              <span class="pulse-score-text">Иногда</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b3', 4, this)">
              <span class="pulse-score-digit">4</span>
              <span class="pulse-score-text">Скорее комфортно</span>
            </div>
            <div class="pulse-scale-btn" onclick="selectPulseScore('b3', 5, this)">
              <span class="pulse-score-digit">5</span>
              <span class="pulse-score-text">Отличный климат</span>
            </div>
          </div>
        </div>

        <button class="btn-action-primary" style="width: 100%; justify-content: center; padding: 14px;" onclick="finishPulseSurvey()">
          ✅ Завершить и запечатать ответы в аналитический пул
        </button>

      </div>
    </section>

    <!-- ==================== ЭКРАН 4: САМОСТОЯТЕЛЬНАЯ ФОРМА ЗАЯВЛЕНИЯ ==================== -->
    <section id="tab-form" class="canvas-screen">
      <div class="self-service-form-card">
        
        <div style="border-bottom: 2px solid #E2E8F0; padding-bottom: 14px; margin-bottom: 20px;">
          <h2 style="font-size: 18px; font-weight: 800; color: #00468C;">Самостоятельное заведение официального обращения</h2>
          <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
            Заполните форму-бланк заявления вручную для прямой регистрации в Канцелярии без прохождения диалога с чат-ботом.
          </p>
        </div>

        <form id="direct-appeal-form" onsubmit="event.preventDefault(); submitDirectForm();">
          <div class="form-grid-2col">
            <div>
              <label class="form-label">Структурное подразделение (Дивизион):</label>
              <select class="form-control" id="form-div">
                <option value="ОДС">Объединение «Дивизион „Сеть“» (ОДС)</option>
                <option value="СФ">Сервисная фабрика (СФ)</option>
                <option value="ДРБ">Дивизион по розничному бизнесу (ДРБ)</option>
                <option value="ДКБ">Дивизион по корпоративному бизнесу (ДКБ)</option>
                <option value="ДТК">Дивизион «Телеком Комплект» (ДТК)</option>
                <option value="ДУП">Департамент управления персоналом (ДУП)</option>
                <option value="ДПБ">Департамент производственной безопасности (ДПБ / HSE)</option>
                <option value="ДЦБ">Дивизион цифрового бизнеса (ДЦБ / IT)</option>
                <option value="ЦА">Центральный аппарат (ЦА)</option>
              </select>
            </div>

            <div>
              <label class="form-label">Регион нахождения филиала (20 регионов РК):</label>
              <select class="form-control" id="form-region">
                <option value="Атырауская область">Атырауская область</option>
                <option value="Мангыстауская область">Мангыстауская область</option>
                <option value="Западно-Казахстанская область">Западно-Казахстанская область (ЗКО)</option>
                <option value="Актюбинская область">Актюбинская область</option>
                <option value="область Абай (г. Семей)">область Абай (г. Семей)</option>
                <option value="Восточно-Казахстанская область">Восточно-Казахстанская область (ВКО)</option>
                <option value="Карагандинская область">Карагандинская область</option>
                <option value="область Ұлытау">область Ұлытау</option>
                <option value="Павлодарская область">Павлодарская область</option>
                <option value="г. Астана">г. Астана</option>
                <option value="г. Алматы">г. Алматы</option>
                <option value="г. Шымкент">г. Шымкент</option>
                <option value="Акмолинская область">Акмолинская область</option>
                <option value="Костанайская область">Костанайская область</option>
                <option value="Северо-Казахстанская область">Северо-Казахстанская область (СКО)</option>
                <option value="Алматинская область">Алматинская область</option>
                <option value="область Жетісу">область Жетісу</option>
                <option value="Жамбылская область">Жамбылская область</option>
                <option value="Кызылординская область">Кызылординская область</option>
                <option value="Туркестанская область">Туркестанская область</option>
              </select>
            </div>
          </div>

          <div class="form-grid-2col">
            <div>
              <label class="form-label">Категория нарушения / инцидента:</label>
              <select class="form-control" id="form-category">
                <option value="HSE-01">HSE-01 • Охрана труда: задержка спецобуви и СИЗ (SLA 5 дней)</option>
                <option value="PAY-02">PAY-02 • Оплата труда: задержка выплат, неначисление ночных (SLA 5 дней)</option>
                <option value="OT-03">OT-03 • Принуждение к сверхурочным по субботам (SLA 3 дня)</option>
                <option value="MOB-04">MOB-04 • Моббинг, давление, угрозы руководства (SLA 7 дней)</option>
                <option value="EMG-05">EMG-05 • Угроза забастовки / коллективного отказа от выезда (SLA 24ч)</option>
                <option value="TECH-06">TECH-06 • Износ автопарка АВР (УАЗ), поломки дизелей (SLA 3 дня)</option>
                <option value="LIFE-07">LIFE-07 • Бытовые условия на объектах (отопление, вода) (SLA 5 дней)</option>
              </select>
            </div>

            <div>
              <label class="form-label">Режим конфиденциальности подачи:</label>
              <select class="form-control" id="form-anon">
                <option value="anon">🔒 Строго анонимно (выдать секретный токен TK-XXXX)</option>
                <option value="official">👤 Официально (от имени Ахметов Д.Б., таб. №104291)</option>
              </select>
            </div>
          </div>

          <div style="margin-bottom: 16px;">
            <label class="form-label">Суть инцидента и ваши требования (Фабула обращения):</label>
            <textarea class="form-control" id="form-text" rows="4" placeholder="Подробно опишите факты: что произошло, дата, кто из руководителей был в курсе, какие требования необходимо выполнить..."></textarea>
          </div>

          <div style="margin-bottom: 20px;">
            <label class="form-label">Прикрепить подтверждающие материалы (фото дефектов, наряды, акты):</label>
            <div class="file-dropzone" onclick="simulateFileUpload()">
              <div style="font-size: 26px;">📎</div>
              <div style="font-size: 13px; font-weight: 700; color: #00468C;" id="file-drop-label">Нажмите для выбора файла или перетащите сюда</div>
              <div style="font-size: 11px; color: #94A3B8;">Поддерживаются: JPG, PNG, PDF, DOCX (до 25 МБ)</div>
            </div>
          </div>

          <button type="submit" class="btn-action-primary" style="width: 100%; justify-content: center; padding: 14px;">
            🏛️ Зарегистрировать в Канцелярии и запустить таймер SLA
          </button>
        </form>

      </div>
    </section>

    <!-- ==================== ЭКРАН 5: КАНЦЕЛЯРИЯ И РЕЕСТР SLA ==================== -->
    <section id="tab-chancellery" class="canvas-screen">
      <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); overflow: hidden;">
        
        <div style="background: #00468C; color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 20px;">📋</span>
            <div>
              <h2 style="font-size: 15px; font-weight: 800;">Реестр обращений Канцелярии и контроль регламентных сроков (SLA)</h2>
              <span style="font-size: 11px; color: #BAE6FD;">Этап 2 консолидации • Интеграция с СЭД Lotus Notes • Защита от конфликта интересов</span>
            </div>
          </div>
          <button class="btn-action-primary" style="background: rgba(255,255,255,0.2); font-size: 12px;" onclick="openTokenModal()">
            🔍 Поиск по токену
          </button>
        </div>

        <!-- Таблица обращений -->
        <div style="padding: 20px;">
          <table class="appeals-table">
            <thead>
              <tr>
                <th>Вх. номер / Токен</th>
                <th>Дата регистрации</th>
                <th>Режим</th>
                <th>Дивизион / Регион</th>
                <th>Категория / Фабула</th>
                <th>Первый получатель</th>
                <th>Статус</th>
                <th>Контроль SLA</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody id="master-chancellery-tbody">
              <!-- Newly submitted item appears dynamically at top -->
              <tr id="live-new-table-row" style="background: #F0FDF4; display: none;">
                <td>
                  <strong style="color: #00468C;" id="live-row-num">ВХ-2026/0942-КАНЦ</strong><br>
                  <span style="font-size: 10px; color: #10B981; font-weight: 800;">● НОВОЕ ОБРАЩЕНИЕ</span>
                </td>
                <td id="live-row-date">10.11.2026 18:05</td>
                <td><span class="badge-status status-closed" id="live-row-anon">🔒 Анонимно (TK-7842)</span></td>
                <td id="live-row-div">ОДС • Атырауская обл.</td>
                <td>
                  <strong id="live-row-cat">Охрана труда (HSE-01)</strong><br>
                  <span style="font-size: 11px; color: #64748B;" id="live-row-text">Срыв выдачи зимней обуви выездным бригадам</span>
                </td>
                <td>
                  <strong id="live-row-recip">Департамент охраны труда</strong><br>
                  <span style="font-size: 11px; color: #10B981;">🛡️ Conflict Guard: OK</span>
                </td>
                <td><span class="badge-status status-work">В работе</span></td>
                <td style="font-family: monospace; font-weight: 700; color: #059669;" id="live-row-sla">⏱️ 4д 23ч 59м</td>
                <td><button class="btn-action-primary" style="padding: 4px 8px; font-size: 11px;" onclick="inspectTicket('ВХ-2026/0942-КАНЦ')">👁️ Карточка</button></td>
              </tr>

              <!-- Preloaded Static Samples -->
              <tr>
                <td><strong>ВХ-2026/0941-КАНЦ</strong><br><span style="font-size:10px; color:#64748B;">TK-8812-KZ</span></td>
                <td>08.11.2026 14:20</td>
                <td><span class="badge-status status-closed">🔒 Анонимно</span></td>
                <td>ОДС • область Абай (Семей)</td>
                <td><strong>PAY-02 Оплата труда</strong><br><span style="font-size: 11px; color: #64748B;">Принуждение к выходу в субботу без табелирования</span></td>
                <td><strong>Департамент оплаты труда</strong><br><span style="font-size: 11px; color: #64748B;">Ким А.В.</span></td>
                <td><span class="badge-status status-work">В работе</span></td>
                <td style="font-family: monospace; font-weight: 700; color: #D97706;">⏱️ 1д 04ч (Внимание)</td>
                <td><button class="btn-action-primary" style="padding: 4px 8px; font-size: 11px;" onclick="inspectTicket('ВХ-2026/0941-КАНЦ')">👁️ Карточка</button></td>
              </tr>

              <tr>
                <td><strong>ВХ-2026/0938-КАНЦ</strong></td>
                <td>04.11.2026 09:15</td>
                <td><span class="badge-status" style="background:#EBF3FA; color:#00468C;">👤 Искаков М.А.</span></td>
                <td>ОДС • СКО (Петропавловск)</td>
                <td><strong>TECH-06 Инфраструктура</strong><br><span style="font-size: 11px; color: #64748B;">Поломка аварийного дизель-генератора на узле связи</span></td>
                <td><strong>Дивизион «Сеть» (ОДС)</strong></td>
                <td><span class="badge-status" style="background:#FEE2E2; color:#B91C1C;">Эскалация</span></td>
                <td style="font-family: monospace; font-weight: 700; color: #DC2626;">⚠️ ПРОСРОЧЕНО (4ч)</td>
                <td><button class="btn-action-primary" style="padding: 4px 8px; font-size: 11px; background:#DC2626;" onclick="alert('Эскалация направлена Главному директору HRD')">⚡ Эскалировать</button></td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </section>

    <!-- ==================== ЭКРАН 6: ПАНЕЛЬ РУКОВОДСТВА И ОТЧЕТЫ ИИ ==================== -->
    <section id="tab-executive" class="canvas-screen">
      <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 24px;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 14px; margin-bottom: 20px;">
          <div>
            <h2 style="font-size: 18px; font-weight: 800; color: #00468C;">Панель руководства: Предиктивная аналитика и тепловая карта рисков</h2>
            <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
              Синтез результатов квартального пульс-опроса Q4 и массива обращений Канцелярии (Qwen 2.5 On-Premise)
            </p>
          </div>
          <span style="background: #00468C; color: white; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 4px;">
            ROLE_EXECUTIVE (Правление)
          </span>
        </div>

        <!-- Развернутый текстовый отчет ИИ -->
        <div style="background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%); border: 1.5px solid #CBD5E1; border-left: 5px solid #00468C; border-radius: var(--radius-md); padding: 20px; margin-bottom: 24px;">
          <h3 style="font-size: 15px; font-weight: 800; color: #00468C; margin-bottom: 10px;">
            ✨ Сводный аналитический отчет ИИ по социальному климату и рискам (Executive Summary)
          </h3>
          <div style="font-size: 13px; line-height: 1.6; color: #1E293B;">
            <strong>1. Интегральные показатели социального климата:</strong> Индекс вовлеченности персонала (ИВ) зафиксирован на уровне <strong>70%</strong>, при этом индекс социального благополучия (ИСБ) находится в зоне напряжения (<strong>34%</strong>). 76% всех поступающих сигналов подаются анонимно.<br><br>
            <strong>2. Критические очаги напряженности (Системная кластеризация):</strong>
            <ul style="margin: 8px 0 8px 24px;">
              <li><strong style="color: #B91C1C;">Очаг №1 (Западная РДТ, ОДС): 69 обращений.</strong> Задержка выдачи зимней обуви и курток монтерам связи. Индекс риска забастовки вырос до <strong>8.8 / 10</strong>. <em>Рекомендация: срочная переброска 240 пар обуви со склада ЦА.</em></li>
              <li><strong style="color: #D97706;">Очаг №2 (Восточная РДТ, ОДС): 34 обращения.</strong> Скрытые неоплачиваемые переработки по субботам. <em>Рекомендация: проверка табелей учета рабочего времени по ст. 108 ТК РК.</em></li>
              <li><strong style="color: #4338CA;">Очаг №3 (Сервисная фабрика): 28 обращений.</strong> Износ служебного автотранспорта УАЗ аварийных бригад. <em>Рекомендация: выделение целевого лимита на закупку запчастей.</em></li>
            </ul>
            <strong>3. Дисциплина исполнения (SLA):</strong> 87% обращений закрываются в нормативный 5-дневный срок. Среднее время первого ответа сократилось до <strong>3.7 дней</strong>.
          </div>
        </div>

        <!-- Графики Chart.js -->
        <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px;">
          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px;">
            <h4 style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 10px;">Структура обращений и жалоб по категориям</h4>
            <div style="height: 250px;">
              <canvas id="chartExecCategories"></canvas>
            </div>
          </div>

          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px;">
            <h4 style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 10px;">Соблюдение SLA исполнителями по филиалам (%)</h4>
            <div style="height: 250px;">
              <canvas id="chartExecSLA"></canvas>
            </div>
          </div>
        </div>

      </div>
    </section>

  </main>

  <!-- ==================== МОДАЛЬНОЕ ОКНО: CDN ЧЕКИН (WELLNESS NUDGE) ==================== -->
  <div id="modal-nudge" class="modal-backdrop-nudge active" onclick="closeNudgeModal()">
    <div class="nudge-modal-card" onclick="event.stopPropagation()">
      
      <div class="nudge-header">
        <div class="nudge-avatar-pulse">👋</div>
        <div>
          <h3 style="font-size: 16px; font-weight: 800; color: #00468C;">Сәлеметсіз бе, Данияр Бауыржанұлы!</h3>
          <span style="font-size: 12px; color: var(--text-muted);">Авторизация CDN • ОДС Западная РДТ • г. Атырау</span>
        </div>
      </div>

      <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: var(--radius-md); padding: 14px; font-size: 13.5px; line-height: 1.5; color: #1E293B;">
        Все ли у вас в порядке на рабочем месте? Есть ли сложности, нерешенные вопросы или проблемы в коллективе? Хотите ли вы поговорить об этом или поделиться обратной связью?
      </div>

      <div class="nudge-options-list">
        <div class="nudge-option-btn" onclick="nudgeAction('chat')">
          <span style="font-size: 22px;">💬</span>
          <div>
            <strong style="color: #00468C; font-size: 13px;">Да, есть проблема — поговорить с ИИ-агентом</strong>
            <div style="font-size: 11px; color: #64748B;">ИИ выслушает, задаст наводящие вопросы и оформит официальное обращение</div>
          </div>
        </div>

        <div class="nudge-option-btn" onclick="nudgeAction('pulse')">
          <span style="font-size: 22px;">📊</span>
          <div>
            <strong style="color: #6366F1; font-size: 13px;">Пройти квартальный пульс-опрос Q4 (60 секунд)</strong>
            <div style="font-size: 11px; color: #64748B;">Экспресс-оценка климата, отношения к компании и атмосферы в коллективе</div>
          </div>
        </div>

        <div class="nudge-option-btn" onclick="nudgeAction('form')">
          <span style="font-size: 22px;">📝</span>
          <div>
            <strong style="color: #0284C7; font-size: 13px;">Заполнить официальное обращение вручную</strong>
            <div style="font-size: 11px; color: #64748B;">Прямой ввод заявления без чат-бота с прикреплением файлов</div>
          </div>
        </div>

        <div class="nudge-option-btn" onclick="nudgeAction('ok')">
          <span style="font-size: 22px;">👍</span>
          <div>
            <strong style="color: #10B981; font-size: 13px;">Все отлично, спасибо!</strong>
            <div style="font-size: 11px; color: #64748B;">У меня нет проблем, закрыть окно и перейти к работе</div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- ==================== МОДАЛЬНОЕ ОКНО: ПОИСК ПО ТОКЕНУ ==================== -->
  <div id="modal-token-tracker" class="modal-backdrop-nudge" onclick="closeTokenModal()">
    <div class="nudge-modal-card" onclick="event.stopPropagation()">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 16px; font-weight: 800; color: #00468C;">🔍 Проверка статуса обращения по токену</h3>
        <button style="border: none; background: transparent; font-size: 18px; cursor: pointer;" onclick="closeTokenModal()">✕</button>
      </div>

      <div style="display: flex; gap: 8px; margin-bottom: 16px;">
        <input type="text" id="token-search-input" class="form-control" value="TK-7842-KZ" style="font-family: monospace; font-weight: 700; font-size: 14px;">
        <button class="btn-action-primary" onclick="lookupToken()">Найти</button>
      </div>

      <div id="token-card-result" style="background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: var(--radius-md); padding: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <strong style="color: #00468C;" id="token-res-num">ВХ-2026/0942-КАНЦ</strong>
          <span class="badge-status status-work">В работе у исполнителя</span>
        </div>
        <div style="font-size: 12px; color: #64748B; margin-bottom: 8px;">
          Категория: <strong style="color:#0F172A;" id="token-res-cat">Охрана труда и СИЗ</strong><br>
          Первый получатель: <strong style="color:#0F172A;">Департамент производственной безопасности (Смагулов Б.К.)</strong>
        </div>
        <div style="background: white; border: 1px solid #E2E8F0; padding: 10px; border-radius: var(--radius-sm); font-size: 12px;">
          💬 <strong>Ответ исполнителя (17:40):</strong> «Обращение принято в работу. Направлен запрос на центральный склад в г. Астана для перераспределения 18 комплектов утепленной обуви.»
        </div>
        <div style="margin-top: 10px; font-size: 11.5px; color: #10B981; font-weight: 700;">
          ⏱️ До окончания нормативного срока ответа: 4 дня 23 часа
        </div>
      </div>
    </div>
  </div>

  <!-- Toast Контейнер -->
  <div class="toast-container" id="toast-box"></div>

  <!-- ==================== ИНТЕРАКТИВНЫЙ JAVASCRIPT ==================== -->
  <script>
    let activeTabId = 'tab-portal';
    let liveCountdownSeconds = 5 * 24 * 3600 - 15;
    let timerLoop = null;

    // Модель обращения
    let currentAppealState = {
      rawText: "",
      division: "ОДС",
      region: "Атырауская область",
      category: "HSE-01",
      categoryTitle: "Охрана труда и СИЗ",
      recipient: "Департамент производственной безопасности (Смагулов Б.К.)",
      isAnonymous: true,
      token: "TK-7842-KZ",
      regNumber: "ВХ-2026/0942-КАНЦ",
      slaDays: 5
    };

    document.addEventListener("DOMContentLoaded", () => {
      initCharts();
      startSLATicker();
    });

    // Переключение вкладок Канваса
    function switchCanvasTab(tabId) {
      activeTabId = tabId;
      document.querySelectorAll('.canvas-screen').forEach(el => el.classList.remove('active'));
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');

      document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.nav-tab-btn')).find(b => {
        const onclickAttr = b.getAttribute('onclick') || '';
        return onclickAttr.includes(tabId);
      });
      if (activeBtn) activeBtn.classList.add('active');
    }

    // Модальное окно вовлечения (Nudge)
    function openNudgeModal() {
      document.getElementById('modal-nudge').classList.add('active');
    }

    function closeNudgeModal() {
      document.getElementById('modal-nudge').classList.remove('active');
    }

    function nudgeAction(type) {
      closeNudgeModal();
      if (type === 'chat') {
        switchCanvasTab('tab-chat');
        showToast("Переход в диалог с ИИ-агентом...");
      } else if (type === 'pulse') {
        switchCanvasTab('tab-pulse');
        showToast("Запущен квартальный пульс-опрос Q4...");
      } else if (type === 'form') {
        switchCanvasTab('tab-form');
        showToast("Открыта самостоятельная форма заявления...");
      } else {
        showToast("Спасибо за обратную связь! Рады, что у вас все в порядке.");
      }
    }

    // Быстрые сценарии в чате
    function applyPreset(presetType) {
      const input = document.getElementById('chat-text-input');
      if (presetType === 'ppe') {
        input.value = "В филиале ОДС Запад уже 2 месяца не выдают зимнюю обувь и утепленные куртки. На складе говорят ждать декабря, а монтеры выезжают на аварии в мороз в летних ботинках.";
      } else if (presetType === 'overtime') {
        input.value = "Начальник участка принуждает оставаться после смены и выходить по субботам, табель закрывает как 8 часов. При отказе угрожает срезать премию.";
      } else {
        input.value = "Мастер систематически грубит, допускает оскорбления в адрес монтеров и угрожает увольнением за любые замечания по Колдоговору.";
      }
      sendChatProblem();
    }

    // Чат: отправка проблемы
    function sendChatProblem() {
      const input = document.getElementById('chat-text-input');
      const text = input.value.trim();
      if (!text) return;

      currentAppealState.rawText = text;
      input.value = "";
      document.getElementById('quick-chips-container').style.display = 'none';

      appendChatUserMsg(text);

      showChatTyping(() => {
        // ИИ выводит адаптивный опросник
        renderChatQuestionnaire();
      });
    }

    function handleChatEnter(e) {
      if (e.key === 'Enter') sendChatProblem();
    }

    function renderChatQuestionnaire() {
      let cat = "Охрана труда и производственная безопасность (СИЗ)";
      if (currentAppealState.rawText.includes("суббот") || currentAppealState.rawText.includes("преми")) {
        cat = "Оплата труда и сверхурочные работы (ст. 108 ТК РК)";
        currentAppealState.categoryTitle = cat;
        currentAppealState.recipient = "Департамент оплаты труда (Ким А.В.)";
      } else if (currentAppealState.rawText.includes("груб") || currentAppealState.rawText.includes("угрож")) {
        cat = "Моббинг и этика (Служба комплаенс)";
        currentAppealState.categoryTitle = cat;
        currentAppealState.recipient = "Служба комплаенс и Омбудсмен";
      }

      appendChatAIMsg(`
        Я зафиксировал суть проблемы.<br>
        <strong>Категория инцидента:</strong> <span style="color:#00468C; font-weight:700;">${cat}</span>.<br><br>
        Чтобы составить юридически выверенное заявление, ответьте, пожалуйста, на <strong>3 уточняющих вопроса</strong>:
      `);

      const injectBox = document.getElementById('chat-dynamic-injections');
      const qCard = document.createElement('div');
      qCard.id = 'active-chat-qcard';
      qCard.style = "background:white; border:1.5px solid #CBD5E1; border-radius:12px; padding:16px; margin-top:8px; border-left:4px solid #0284C7;";
      qCard.innerHTML = `
        <div style="font-size:13px; font-weight:700; margin-bottom:8px;">1. Укажите подразделение / филиал:</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">
          <button class="nav-tab-btn active" style="background:#00468C; font-size:11.5px;" onclick="selectChatQ(this)">ОДС Западная РДТ (Атырау)</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">ОДС Восточная РДТ (Семей)</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Алматинский филиал</button>
        </div>

        <div style="font-size:13px; font-weight:700; margin-bottom:8px;">2. Сколько работников затронуто?</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Лично меня</button>
          <button class="nav-tab-btn active" style="background:#00468C; font-size:11.5px;" onclick="selectChatQ(this)">Вся выездная бригада (18 чел)</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Весь участок (>30 чел)</button>
        </div>

        <div style="font-size:13px; font-weight:700; margin-bottom:8px;">3. Обращались ли вы ранее к мастеру?</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px;">
          <button class="nav-tab-btn active" style="background:#00468C; font-size:11.5px;" onclick="selectChatQ(this)">Да, получили отказ</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Опасаемся давления</button>
        </div>

        <button class="btn-action-primary" style="width:100%; justify-content:center;" onclick="proceedToChatStatement()">
          📝 Сформировать официальное заявление
        </button>
      `;
      injectBox.appendChild(qCard);
      scrollChat();
    }

    function selectChatQ(btn) {
      btn.parentElement.querySelectorAll('button').forEach(b => {
        b.style.background = "#F1F5F9";
        b.style.color = "#334155";
      });
      btn.style.background = "#00468C";
      btn.style.color = "white";
    }

    function proceedToChatStatement() {
      const q = document.getElementById('active-chat-qcard');
      if (q) q.style.opacity = '0.7';

      showChatTyping(() => {
        appendChatAIMsg("Спасибо! На основе ваших ответов я составил структурированное заявление по стандартам АО «Казахтелеком»:");

        const injectBox = document.getElementById('chat-dynamic-injections');
        const st = document.createElement('div');
        st.className = 'formal-statement-card';
        st.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1.5px solid #E2E8F0; padding-bottom:8px; margin-bottom:10px;">
            <strong style="color:#00468C; font-size:13px;">КАРТОЧКА ОБРАЩЕНИЯ (ПРОЕКТ)</strong>
            <span class="badge-hse">🟡 Системный риск</span>
          </div>
          <div style="font-size:12px; margin-bottom:4px;"><strong>Категория:</strong> ${currentAppealState.categoryTitle}</div>
          <div style="font-size:12px; margin-bottom:4px;"><strong>Подразделение:</strong> ОДС • Атырауская область (Запад)</div>
          <div style="font-size:12px; margin-bottom:8px;"><strong>Масштаб:</strong> Коллективное (затронуто 18 монтеров)</div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:10px; border-radius:6px; font-size:12.5px; line-height:1.5; margin-bottom:12px;">
            «Заявитель сообщает о факте несоблюдения требований ст. 182 ТК РК и п. 4.2 Коллективного договора. Суть: ${currentAppealState.rawText}. Требование: срочно провести ревизию и обеспечить выдачу экипировки.»
          </div>

          <div style="border-top:1px dashed #CBD5E1; padding-top:10px; margin-top:10px;">
            <div style="font-size:12.5px; font-weight:700; margin-bottom:6px;">Выберите режим подачи:</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px;">
              <div id="chat-mode-anon" style="border:2px solid #10B981; background:#F0FDF4; padding:8px 12px; border-radius:8px; cursor:pointer;" onclick="setChatAnon(true)">
                <strong style="color:#059669; font-size:12px;">🔒 Анонимно</strong>
                <div style="font-size:11px; color:#64748B;">Секретный токен TK-7842-KZ</div>
              </div>
              <div id="chat-mode-off" style="border:1px solid #CBD5E1; padding:8px 12px; border-radius:8px; cursor:pointer;" onclick="setChatAnon(false)">
                <strong style="color:#00468C; font-size:12px;">👤 Официально</strong>
                <div style="font-size:11px; color:#64748B;">С внесением ФИО</div>
              </div>
            </div>
            <button class="btn-action-primary" style="width:100%; justify-content:center;" onclick="executeRegistrationInChancellery()">
              🏛️ Утвердить и зарегистрировать в Канцелярии
            </button>
          </div>
        `;
        injectBox.appendChild(st);
        scrollChat();
      });
    }

    function setChatAnon(isAnon) {
      currentAppealState.isAnonymous = isAnon;
      document.getElementById('chat-mode-anon').style.border = isAnon ? "2px solid #10B981" : "1px solid #CBD5E1";
      document.getElementById('chat-mode-anon').style.background = isAnon ? "#F0FDF4" : "white";
      document.getElementById('chat-mode-off').style.border = isAnon ? "1px solid #CBD5E1" : "2px solid #00468C";
      document.getElementById('chat-mode-off').style.background = isAnon ? "white" : "#F0F9FF";
    }

    function executeRegistrationInChancellery() {
      showChatTyping(() => {
        appendChatAIMsg("🏛️ <strong>Обращение успешно зарегистрировано в Канцелярии АО «Казахтелеком»!</strong>");

        const injectBox = document.getElementById('chat-dynamic-injections');
        const stamp = document.createElement('div');
        stamp.style = "background:#F8FAFC; border:2px dashed #00468C; border-radius:12px; padding:16px; margin-top:8px;";
        stamp.innerHTML = `
          <div style="background:#00468C; color:white; font-size:11px; font-weight:800; padding:4px 8px; border-radius:4px; display:inline-block; margin-bottom:8px;">
            🏛️ ЗАРЕГИСТРИРОВАНО В КАНЦЕЛЯРИИ
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:12px; margin-bottom:8px;">
            <div>Входящий номер: <strong style="color:#00468C;">${currentAppealState.regNumber}</strong></div>
            <div>Статус: <strong style="color:#0284C7;">В ОБРАБОТКЕ</strong></div>
            <div>Режим: <strong>${currentAppealState.isAnonymous ? '🔒 Конфиденциально' : '👤 Официально'}</strong></div>
            <div>Дата: <strong>10.11.2026 18:05</strong></div>
          </div>
          <div style="background:#0B132B; color:#38BDF8; font-family:monospace; font-size:16px; font-weight:700; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
            <span>${currentAppealState.token}</span>
            <button style="background:#0284C7; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;" onclick="copyToken()">Скопировать</button>
          </div>
          <div style="margin-top:10px; font-size:12px; color:#475569;">
            🎯 <strong>Первый получатель:</strong> ${currentAppealState.recipient}<br>
            🛡️ <em>Conflict of Interest Guard: начальник участка аппаратно исключен из проверки.</em>
          </div>
          <div class="sla-timer-widget">
            <div>
              <div style="font-size:11px; color:#94A3B8;">⏱️ Нормативный срок ответа (SLA 5 дней):</div>
              <div class="sla-countdown-digits" id="live-chat-sla">04д 23ч 59м 45с</div>
            </div>
            <button class="btn-action-primary" style="background:#0284C7; font-size:11.5px;" onclick="switchCanvasTab('tab-chancellery')">
              Перейти в Реестр →
            </button>
          </div>
        `;
        injectBox.appendChild(stamp);
        scrollChat();

        // Показываем в реестре Канцелярии
        activateTableNewItem();
        showToast("Обращение успешно зарегистрировано в реестре Канцелярии!");
      });
    }

    function activateTableNewItem() {
      const row = document.getElementById('live-new-table-row');
      if (row) {
        row.style.display = 'table-row';
        document.getElementById('live-row-text').textContent = currentAppealState.rawText.substring(0, 48) + "...";
      }
    }

    // Квартальный пульс-опрос логика
    function selectPulseScore(block, score, btn) {
      const parent = btn.parentElement;
      parent.querySelectorAll('.pulse-scale-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');

      if (block === 'b1' && score <= 2) {
        document.getElementById('synergy-alert-b1').style.display = 'block';
      } else if (block === 'b1') {
        document.getElementById('synergy-alert-b1').style.display = 'none';
      }
    }

    function convertPulseToAppeal(catCode, summaryText) {
      switchCanvasTab('tab-chat');
      const input = document.getElementById('chat-text-input');
      input.value = `По результатам квартального пульс-опроса: выявлена критическая проблема (${summaryText}). Прошу зарегистрировать официальное обращение.`;
      sendChatProblem();
    }

    function finishPulseSurvey() {
      showToast("🎉 Спасибо! Ваши ответы запечатаны в квартальный аналитический пул.");
      switchCanvasTab('tab-portal');
    }

    // Самостоятельная форма подачи
    function submitDirectForm() {
      const text = document.getElementById('form-text').value.trim();
      if (!text) {
        alert("Пожалуйста, опишите суть инцидента в поле ввода.");
        return;
      }
      currentAppealState.rawText = text;
      currentAppealState.division = document.getElementById('form-div').value;
      currentAppealState.region = document.getElementById('form-region').value;
      currentAppealState.categoryTitle = document.getElementById('form-category').options[document.getElementById('form-category').selectedIndex].text;
      currentAppealState.isAnonymous = (document.getElementById('form-anon').value === 'anon');

      activateTableNewItem();
      showToast("Обращение из формы успешно зарегистрировано в Канцелярии!");
      switchCanvasTab('tab-chancellery');
    }

    function simulateFileUpload() {
      document.getElementById('file-drop-label').textContent = "✅ Прикреплено: foto_defekt_obuvi_2026.jpg (3.2 МБ)";
      showToast("Файл успешно прикреплен!");
    }

    // SLA таймер отсчет
    function startSLATicker() {
      if (timerLoop) clearInterval(timerLoop);
      timerLoop = setInterval(() => {
        liveCountdownSeconds--;
        if (liveCountdownSeconds < 0) liveCountdownSeconds = 0;

        const d = Math.floor(liveCountdownSeconds / (24 * 3600));
        const h = Math.floor((liveCountdownSeconds % (24 * 3600)) / 3600);
        const m = Math.floor((liveCountdownSeconds % 3600) / 60);
        const s = liveCountdownSeconds % 60;

        const str = `0${d}д ${h < 10 ? '0' : ''}${h}ч ${m < 10 ? '0' : ''}${m}м ${s < 10 ? '0' : ''}${s}с`;
        
        const cEl = document.getElementById('live-chat-sla');
        if (cEl) cEl.textContent = str;

        const tEl = document.getElementById('live-row-sla');
        if (tEl) tEl.textContent = `⏱️ ${d}д ${h}ч ${m}м`;
      }, 1000);
    }

    // Toast
    function showToast(msg) {
      const box = document.getElementById('toast-box');
      const toast = document.createElement('div');
      toast.className = 'toast-pill';
      toast.innerHTML = `<span>🔔</span><span>${msg}</span>`;
      box.appendChild(toast);
      setTimeout(() => { toast.remove(); }, 4000);
    }

    function copyToken() {
      navigator.clipboard.writeText(currentAppealState.token);
      showToast(`Токен ${currentAppealState.token} скопирован в буфер!`);
    }

    function openTokenModal() {
      document.getElementById('modal-token-tracker').classList.add('active');
    }

    function closeTokenModal() {
      document.getElementById('modal-token-tracker').classList.remove('active');
    }

    function lookupToken() {
      const code = document.getElementById('token-search-input').value.trim();
      showToast(`Обращение ${code} найдено. Статус: В работе у исполнителя.`);
    }

    function inspectTicket(num) {
      alert(`Карточка дела ${num}\\nСтатус: В работе у исполнителя\\nSLA: Соблюдается (норматив 5 дней)\\nПервый получатель назначен без конфликта интересов.`);
    }

    function resetChatFlow() {
      document.getElementById('chat-dynamic-injections').innerHTML = "";
      document.querySelectorAll('.chat-msg-row.user').forEach(e => e.remove());
      document.getElementById('quick-chips-container').style.display = 'block';
      showToast("Диалог начат заново.");
    }

    function appendChatUserMsg(txt) {
      const stream = document.getElementById('chat-stream-box');
      const inj = document.getElementById('chat-dynamic-injections');
      const row = document.createElement('div');
      row.className = 'chat-msg-row user';
      row.innerHTML = `<div class="msg-avatar user">Я</div><div class="msg-content-wrapper"><div class="msg-bubble">${txt}</div><div style="font-size:10px; color:#94A3B8; text-align:right;">18:04</div></div>`;
      stream.insertBefore(row, inj);
      scrollChat();
    }

    function appendChatAIMsg(html) {
      const stream = document.getElementById('chat-stream-box');
      const inj = document.getElementById('chat-dynamic-injections');
      const row = document.createElement('div');
      row.className = 'chat-msg-row ai';
      row.innerHTML = `<div class="msg-avatar ai">ИИ</div><div class="msg-content-wrapper" style="width:100%;"><div class="msg-bubble">${html}</div><div style="font-size:10px; color:#94A3B8;">Только что</div></div>`;
      stream.insertBefore(row, inj);
      scrollChat();
    }

    function showChatTyping(cb) {
      const stream = document.getElementById('chat-stream-box');
      const inj = document.getElementById('chat-dynamic-injections');
      const t = document.createElement('div');
      t.id = 'temp-typing';
      t.className = 'chat-msg-row ai';
      t.innerHTML = `<div class="msg-avatar ai">ИИ</div><div style="padding:10px 14px; background:white; border:1px solid #CBD5E1; border-radius:12px; font-size:12px; color:#64748B;">🧠 ИИ анализирует фактуру...</div>`;
      stream.insertBefore(t, inj);
      scrollChat();
      setTimeout(() => {
        const el = document.getElementById('temp-typing');
        if (el) el.remove();
        if (cb) cb();
      }, 700);
    }

    function scrollChat() {
      const stream = document.getElementById('chat-stream-box');
      if (stream) { setTimeout(() => { stream.scrollTop = stream.scrollHeight; }, 40); }
    }

    // Chart.js
    function initCharts() {
      const c1 = document.getElementById('chartExecCategories');
      if (c1) {
        new Chart(c1, {
          type: 'doughnut',
          data: {
            labels: ['Охрана труда и СИЗ', 'Оплата труда и надбавки', 'Сверхурочные работы', 'Моббинг / Этика', 'Инфраструктура'],
            datasets: [{
              data: [38, 28, 14, 12, 8],
              backgroundColor: ['#00468C', '#0284C7', '#6366F1', '#F59E0B', '#EF4444'],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }
          }
        });
      }

      const c2 = document.getElementById('chartExecSLA');
      if (c2) {
        new Chart(c2, {
          type: 'bar',
          data: {
            labels: ['ОДС', 'СФ', 'ДРБ', 'ДКБ', 'ДТК', 'ДУП'],
            datasets: [{
              label: 'Соблюдение SLA (%)',
              data: [96.9, 97.4, 98.6, 100, 100, 100],
              backgroundColor: ['#0284C7', '#0284C7', '#10B981', '#10B981', '#10B981', '#10B981'],
              borderRadius: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { min: 80, max: 100 } }
          }
        });
      }
    }
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(canvas_html)

print("Canvas successfully written to index.html!")

