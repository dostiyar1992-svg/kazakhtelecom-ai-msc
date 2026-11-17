# -*- coding: utf-8 -*-
"""
Generator for index.html: ИИ-Приемная обращений и жалоб АО «Казахтелеком»
Полная реализация нового сценария:
1. Описание проблемы сотрудником своими словами
2. Динамический опросник ИИ
3. Формирование официального заявления
4. Выбор анонимности
5. Регистрация канцелярией с присвоением входящего номера
6. Определение первого получателя (маршрутизация)
7. Контроль сроков ответа (SLA-таймер)
8. Сводный аналитический отчет ИИ и дашборд руководства
"""

html_content = '''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ИИ-Приемная обращений и мониторинг климата | АО «Казахтелеком»</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <!-- Chart.js for Visualizations -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --primary: #00468C;       /* Казахтелеком Navy */
      --primary-light: #EBF3FA;
      --primary-hover: #00366D;
      --accent: #0284C7;        /* Sky Blue */
      --accent-purple: #6366F1;
      --success: #10B981;
      --warning: #F59E0B;
      --orange: #F97316;
      --danger: #EF4444;
      --bg-slate: #F8FAFC;
      --border: #E2E8F0;
      --text-main: #1E293B;
      --text-muted: #64748B;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.03);
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
    .demo-navbar {
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

    .demo-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .demo-logo-badge {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      font-weight: 800;
      font-size: 13px;
      padding: 6px 10px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
      box-shadow: 0 2px 8px rgba(0, 70, 140, 0.5);
    }

    .demo-title-group h1 {
      font-size: 14px;
      font-weight: 700;
      color: #F8FAFC;
      letter-spacing: -0.2px;
    }

    .demo-title-group span {
      font-size: 11px;
      color: #94A3B8;
    }

    .demo-nav-tabs {
      display: flex;
      background: rgba(255, 255, 255, 0.08);
      padding: 4px;
      border-radius: var(--radius-full);
      gap: 4px;
    }

    .demo-tab-btn {
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
    }

    .demo-tab-btn:hover {
      color: white;
      background: rgba(255, 255, 255, 0.12);
    }

    .demo-tab-btn.active {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      box-shadow: 0 2px 10px rgba(2, 132, 199, 0.4);
    }

    .demo-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .badge-live {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      border: 1px solid rgba(16, 185, 129, 0.3);
      font-weight: 600;
    }

    .pulse-dot {
      width: 7px;
      height: 7px;
      background-color: #10B981;
      border-radius: 50%;
      box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
      animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
    }

    @keyframes pulse-ring {
      0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
      70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
      100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Main Viewport */
    .app-viewport {
      flex: 1;
      display: flex;
      justify-content: center;
      padding: 24px;
      background: #F1F5F9;
      position: relative;
    }

    .screen-view {
      display: none;
      width: 100%;
      max-width: 1340px;
      animation: fadeIn 0.3s ease;
    }

    .screen-view.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ==============================================================
       SCREEN 1: ДИАЛОГОВОЕ ОКНО СОТРУДНИКА С ИИ
       ============================================================== */
    .chat-layout-wrapper {
      max-width: 920px;
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
      z-index: 10;
    }

    .chat-header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .ai-avatar-circle {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #E0F2FE;
      color: #0284C7;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 14px;
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

    .chat-header-title h2 {
      font-size: 15px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.2;
    }

    .chat-header-title span {
      font-size: 11px;
      color: var(--success);
      display: flex;
      align-items: center;
      gap: 4px;
      font-weight: 500;
    }

    .chat-header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-header-action {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border);
      background: white;
      color: var(--text-muted);
      font-size: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-header-action:hover {
      background: #F8FAFC;
      color: var(--text-main);
      border-color: #CBD5E1;
    }

    /* Privacy Banner */
    .privacy-trust-banner {
      background: #F0FDF4;
      border-bottom: 1px solid #BBF7D0;
      padding: 8px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: #166534;
    }

    .privacy-trust-banner .shield-tag {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 600;
    }

    /* Chat Messages Stream */
    .chat-stream-body {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
      background: #FAFAFC;
    }

    .chat-msg-row {
      display: flex;
      gap: 12px;
      max-width: 90%;
    }

    .chat-msg-row.ai {
      align-self: flex-start;
    }

    .chat-msg-row.user {
      align-self: flex-end;
      flex-direction: row-reverse;
    }

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

    .msg-avatar.ai {
      background: #E0F2FE;
      color: #0284C7;
      border: 1px solid #BAE6FD;
    }

    .msg-avatar.user {
      background: #00468C;
      color: white;
    }

    .msg-content-wrapper {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

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

    .msg-meta-row {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 10.5px;
      color: #94A3B8;
      padding: 0 4px;
    }

    /* Quick Preset Chips */
    .quick-chips-grid {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 10px;
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
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: var(--shadow-sm);
    }

    .quick-chip:hover {
      border-color: #0284C7;
      background: #F0F9FF;
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
    }

    .quick-chip-badge {
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      text-transform: uppercase;
      white-space: nowrap;
    }

    .badge-hse { background: #FEF3C7; color: #92400E; }
    .badge-labor { background: #EDE9FE; color: #5B21B6; }
    .badge-infra { background: #FEE2E2; color: #991B1B; }

    /* Interactive Questionnaire Cards */
    .questionnaire-card {
      background: #FFFFFF;
      border: 1.5px solid #CBD5E1;
      border-radius: var(--radius-md);
      padding: 16px;
      margin-top: 8px;
      box-shadow: var(--shadow-md);
      border-left: 4px solid var(--accent);
    }

    .question-title {
      font-size: 13.5px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .options-btn-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }

    .option-btn {
      background: #F8FAFC;
      border: 1px solid #CBD5E1;
      color: #334155;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }

    .option-btn:hover {
      border-color: var(--accent);
      background: #F0F9FF;
      color: var(--primary);
    }

    .option-btn.selected {
      background: #00468C;
      color: white;
      border-color: #00468C;
      box-shadow: 0 2px 6px rgba(0, 70, 140, 0.3);
    }

    /* Formal Statement Preview Card */
    .formal-statement-card {
      background: #FFFFFF;
      border: 2px solid #00468C;
      border-radius: var(--radius-md);
      padding: 20px;
      margin-top: 10px;
      box-shadow: var(--shadow-lg);
      position: relative;
    }

    .statement-header-stamp {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1.5px solid #E2E8F0;
      padding-bottom: 12px;
      margin-bottom: 14px;
    }

    .statement-title-h3 {
      font-size: 14px;
      font-weight: 800;
      color: #00468C;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }

    .statement-field-row {
      display: grid;
      grid-template-columns: 140px 1fr;
      gap: 8px;
      font-size: 12.5px;
      margin-bottom: 8px;
    }

    .statement-label {
      color: #64748B;
      font-weight: 600;
    }

    .statement-value {
      color: #0F172A;
      font-weight: 500;
    }

    .statement-fabula-box {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: var(--radius-sm);
      padding: 12px;
      margin: 12px 0;
      font-size: 13px;
      line-height: 1.6;
      color: #1E293B;
    }

    /* Anonymity Choice Cards */
    .anonymity-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 12px;
    }

    .anonymity-card {
      border: 2px solid #E2E8F0;
      border-radius: var(--radius-md);
      padding: 14px;
      cursor: pointer;
      transition: all 0.2s;
      background: #FFFFFF;
    }

    .anonymity-card:hover {
      border-color: var(--accent);
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }

    .anonymity-card.active-anon {
      border-color: #10B981;
      background: #F0FDF4;
    }

    .anonymity-card.active-official {
      border-color: #00468C;
      background: #F0F9FF;
    }

    .anon-title {
      font-size: 13.5px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 6px;
    }

    .anon-desc {
      font-size: 11.5px;
      color: #64748B;
      line-height: 1.4;
    }

    /* Chancellery Stamp & Registration Box */
    .chancellery-stamp-card {
      background: #F8FAFC;
      border: 2px dashed #00468C;
      border-radius: var(--radius-md);
      padding: 18px;
      margin-top: 12px;
      position: relative;
    }

    .stamp-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #00468C;
      color: white;
      font-weight: 800;
      font-size: 12px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 12px;
    }

    .token-display-box {
      background: #0B132B;
      color: #38BDF8;
      font-family: monospace;
      font-size: 18px;
      font-weight: 700;
      padding: 10px 16px;
      border-radius: var(--radius-sm);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 10px 0;
    }

    .btn-copy-token {
      background: #0284C7;
      color: white;
      border: none;
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 11px;
      cursor: pointer;
      font-family: 'Inter', sans-serif;
    }

    /* Recipient Routing Card */
    .routing-card {
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-radius: var(--radius-md);
      padding: 14px 18px;
      margin-top: 10px;
      border-left: 4px solid #6366F1;
    }

    .routing-header {
      font-size: 12.5px;
      font-weight: 700;
      color: #4F46E5;
      text-transform: uppercase;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* SLA Live Countdown Timer Widget */
    .sla-timer-widget {
      background: linear-gradient(135deg, #0F172A, #1E293B);
      color: white;
      border-radius: var(--radius-md);
      padding: 16px 20px;
      margin-top: 12px;
      box-shadow: var(--shadow-md);
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

    .sla-badge-zone {
      font-size: 11px;
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.2);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }

    /* Typing indicator */
    .typing-bubble {
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 12px 18px;
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      width: fit-content;
    }

    .typing-dot {
      width: 7px;
      height: 7px;
      background: #0284C7;
      border-radius: 50%;
      animation: typing 1.4s infinite ease-in-out;
    }

    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typing {
      0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
      30% { transform: translateY(-5px); opacity: 1; }
    }

    /* Chat Footer Input */
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
      transition: all 0.2s;
    }

    .chat-input-box:focus-within {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
      background: #FFFFFF;
    }

    .chat-input-field {
      flex: 1;
      border: none;
      background: transparent;
      outline: none;
      font-size: 13.5px;
      color: var(--text-main);
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

    .chat-send-btn:hover {
      background: #0284C7;
      transform: scale(1.05);
    }

    .chat-footer-brand {
      text-align: center;
      font-size: 10.5px;
      color: #94A3B8;
      margin-top: 6px;
    }

    /* ==============================================================
       SCREEN 2: РЕЕСТР КАНЦЕЛЯРИИ & КОНТРОЛЬ СРОКОВ SLA
       ============================================================== */
    .admin-container {
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      box-shadow: var(--shadow-md);
      overflow: hidden;
    }

    .admin-header-strip {
      background: #00468C;
      color: white;
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .kpi-cards-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 14px;
      padding: 20px 24px 10px 24px;
    }

    .kpi-card {
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px;
      position: relative;
      overflow: hidden;
    }

    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
    }

    .kpi-total::before { background: #00468C; }
    .kpi-work::before { background: #0284C7; }
    .kpi-sla::before { background: #F59E0B; }
    .kpi-overdue::before { background: #EF4444; }
    .kpi-anon::before { background: #10B981; }

    .kpi-value {
      font-size: 24px;
      font-weight: 800;
      color: #0F172A;
      margin: 4px 0;
    }

    .kpi-label {
      font-size: 11px;
      color: #64748B;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }

    .table-container-card {
      padding: 10px 24px 24px 24px;
    }

    .filter-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }

    .filter-btn-group {
      display: flex;
      gap: 6px;
    }

    .filter-pill {
      background: #F1F5F9;
      border: 1px solid #CBD5E1;
      padding: 6px 12px;
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 600;
      color: #475569;
      cursor: pointer;
    }

    .filter-pill.active {
      background: #00468C;
      color: white;
      border-color: #00468C;
    }

    .appeals-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
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
      color: #1E293B;
      vertical-align: middle;
    }

    .appeals-table tr:hover td {
      background: #F8FAFC;
    }

    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
    }

    .status-new { background: #FEF3C7; color: #B45309; }
    .status-work { background: #E0F2FE; color: #0369A1; }
    .status-closed { background: #DCFCE7; color: #15803D; }

    .sla-timer-cell {
      font-family: monospace;
      font-weight: 700;
      font-size: 12px;
    }

    .sla-green { color: #059669; }
    .sla-yellow { color: #D97706; }
    .sla-red { color: #DC2626; }

    .btn-table-action {
      padding: 4px 8px;
      border: 1px solid #CBD5E1;
      border-radius: 4px;
      background: white;
      color: #334155;
      font-size: 11px;
      cursor: pointer;
      font-weight: 600;
    }

    .btn-table-action:hover {
      background: #00468C;
      color: white;
      border-color: #00468C;
    }

    /* ==============================================================
       SCREEN 3: СВОДНАЯ АНАЛИТИКА И ОТЧЕТЫ ИИ
       ============================================================== */
    .exec-grid {
      display: grid;
      grid-template-columns: 1.3fr 1fr;
      gap: 20px;
      margin-top: 16px;
    }

    .exec-card {
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
    }

    .ai-narrative-box {
      background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
      border: 1.5px solid #CBD5E1;
      border-radius: var(--radius-md);
      padding: 20px;
      margin-top: 10px;
      border-left: 4px solid var(--accent);
    }

    .ai-report-title {
      font-size: 14.5px;
      font-weight: 800;
      color: #00468C;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .ai-report-bullets {
      margin: 10px 0 10px 20px;
      font-size: 12.5px;
      line-height: 1.7;
      color: #334155;
    }

    /* Modal dialog */
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 2000;
      align-items: center;
      justify-content: center;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-box {
      background: white;
      border-radius: var(--radius-lg);
      padding: 24px;
      max-width: 540px;
      width: 90%;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--border);
    }
  </style>
</head>
<body>

  <!-- ==================== ВЕРХНЯЯ ПАНЕЛЬ УПРАВЛЕНИЯ ==================== -->
  <header class="demo-navbar">
    <div class="demo-brand">
      <div class="demo-logo-badge">КТ МСЦ</div>
      <div class="demo-title-group">
        <h1>ИИ-Приемная обращений и мониторинг соцклимата</h1>
        <span>АО «Казахтелеком» • Центр социального партнерства и мониторинга</span>
      </div>
    </div>

    <!-- Навигационные вкладки -->
    <nav class="demo-nav-tabs">
      <button class="demo-tab-btn active" onclick="switchScreen('screen-chat')">
        💬 Диалог с ИИ (Подача)
      </button>
      <button class="demo-tab-btn" onclick="switchScreen('screen-admin')">
        📋 Реестр Канцелярии & SLA
      </button>
      <button class="demo-tab-btn" onclick="switchScreen('screen-executive')">
        📊 Аналитика и Отчеты ИИ
      </button>
      <button class="demo-tab-btn" onclick="switchScreen('screen-auth')">
        🔐 Keycloak SSO
      </button>
    </nav>

    <div class="demo-actions">
      <button class="demo-tab-btn" style="background: rgba(2, 132, 199, 0.3); border: 1px solid #0284C7;" onclick="openTokenModal()">
        🔍 Проверить статус по токену
      </button>
      <div class="badge-live">
        <div class="pulse-dot"></div>
        On-Premise LLM
      </div>
    </div>
  </header>

  <!-- ==================== ОСНОВНОЙ ВЬЮПОРТ ==================== -->
  <main class="app-viewport">

    <!-- ==================== ЭКРАН 1: ДИАЛОГОВОЕ ОКНО СОТРУДНИКА ==================== -->
    <section id="screen-chat" class="screen-view active">
      <div class="chat-layout-wrapper">
        
        <!-- Header -->
        <div class="chat-header">
          <div class="chat-header-left">
            <div class="ai-avatar-circle">ИИ</div>
            <div class="chat-header-title">
              <h2>ИИ-Ассистент приема обращений</h2>
              <span>● Локальный защищенный контур (On-Premise)</span>
            </div>
          </div>
          <div class="chat-header-actions">
            <button class="btn-header-action" onclick="toggleLanguage()">
              <span id="lang-indicator">🌐 Русский</span>
            </button>
            <button class="btn-header-action" onclick="resetChatFlow()" title="Начать заново">
              🔄 Новое обращение
            </button>
          </div>
        </div>

        <!-- Privacy Banner -->
        <div class="privacy-trust-banner">
          <div class="shield-tag">
            🛡️ 100% Конфиденциальность гарантирована
          </div>
          <div style="font-size: 11px; color: #15803D;">
            Анонимный режим по умолчанию • Без привязки к логину • Защита заявителя
          </div>
        </div>

        <!-- Chat Stream Body -->
        <div class="chat-stream-body" id="chat-messages-container">
          
          <!-- Message 1: AI Greeting & Process overview -->
          <div class="chat-msg-row ai">
            <div class="msg-avatar ai">ИИ</div>
            <div class="msg-content-wrapper">
              <div class="msg-bubble">
                Сәлеметсіз бе! Здравствуйте! Я интеллектуальный ассистент Центра мониторинга АО «Казахтелеком».<br><br>
                Опишите, пожалуйста, своими словами проблему или ситуацию, с которой вы столкнулись на рабочем месте (условия труда, спецодежда/СИЗ, невыплата надбавок, давление руководства, состояние техники).<br><br>
                <strong>Как устроен прием обращения:</strong><br>
                1. Вы описываете суть своими словами;<br>
                2. Я формирую короткий уточняющий опросник;<br>
                3. Составляю официальное заявление и согласую анонимность;<br>
                4. Регистрирую в Канцелярии с входящим номером и ставлю на контроль сроков (SLA).
              </div>
              <div class="msg-meta-row">
                <span>Только что</span>
              </div>

              <!-- Quick Prompt Presets for instant testing -->
              <div class="quick-chips-grid" id="quick-presets-box">
                <div style="font-size: 11px; color: #64748B; font-weight: 600;">
                  💡 Выберите готовый пример для быстрой демонстрации или введите свой текст ниже:
                </div>
                <div class="quick-chip" onclick="applyPresetCase('ppe')">
                  <span class="quick-chip-badge badge-hse">Охрана труда</span>
                  <div>
                    <strong>Задержка зимней обуви и спецодежды (ОДС):</strong><br>
                    «В филиале ОДС Запад уже 2 месяца не выдают зимнюю обувь и утепленные куртки. На складе говорят "ждите декабря", а монтеры выезжают на аварии в мороз в летних ботинках.»
                  </div>
                </div>
                <div class="quick-chip" onclick="applyPresetCase('overtime')">
                  <span class="quick-chip-badge badge-labor">Оплата труда</span>
                  <div>
                    <strong>Принуждение к неоплачиваемым сверхурочным:</strong><br>
                    «Начальник районного участка заставляет оставаться после смены и выходить по субботам, табель закрывает как 8 часов. При отказе угрожает срезать премию.»
                  </div>
                </div>
                <div class="quick-chip" onclick="applyPresetCase('infra')">
                  <span class="quick-chip-badge badge-infra">Инфраструктура</span>
                  <div>
                    <strong>Аварийное состояние оборудования узла связи:</strong><br>
                    «На опорном узле связи неисправна система охлаждения и резервный генератор не запускается. Неоднократные заявки игнорируются, есть риск сбоя связи района.»
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Dynamic Dialogue Container (Where AI inserts Questionnaire, Statement, Registration, SLA) -->
          <div id="dynamic-chat-content"></div>

        </div>

        <!-- Chat Input Bar -->
        <div class="chat-input-container">
          <div class="chat-input-box">
            <input type="text" id="chat-text-input" class="chat-input-field" placeholder="Опишите проблему своими словами или выберите вариант выше..." onkeypress="handleInputKeypress(event)">
            <button class="chat-send-btn" onclick="submitUserProblem()" title="Отправить">
              ➤
            </button>
          </div>
          <div class="chat-footer-brand">АО «Казахтелеком» • Локальная языковая модель Qwen 2.5 • Шифрование AES-256</div>
        </div>

      </div>
    </section>

    <!-- ==================== ЭКРАН 2: РЕЕСТР КАНЦЕЛЯРИИ & КОНТРОЛЬ СРОКОВ (SLA) ==================== -->
    <section id="screen-admin" class="screen-view">
      <div class="admin-container">
        
        <div class="admin-header-strip">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">📋</span>
            <div>
              <h2 style="font-size: 15px; font-weight: 800;">Реестр входящих обращений и контроль исполнения (SLA)</h2>
              <span style="font-size: 11px; color: #BAE6FD;">Канцелярия ЦА • Этап 2 консолидации • Интеграция с контуром МСЦ</span>
            </div>
          </div>
          <div style="font-size: 12px; background: rgba(255,255,255,0.15); padding: 4px 10px; border-radius: 4px;">
            Оператор: Медебекова А.Т. (Канцелярия / HR)
          </div>
        </div>

        <!-- KPI Metrics Strip -->
        <div class="kpi-cards-grid">
          <div class="kpi-card kpi-total">
            <div class="kpi-label">Всего обращений</div>
            <div class="kpi-value" id="kpi-total-val">419</div>
            <div style="font-size: 11px; color: #10B981;">+1 новое только что</div>
          </div>
          <div class="kpi-card kpi-work">
            <div class="kpi-label">В работе у исполнителей</div>
            <div class="kpi-value" id="kpi-work-val">84</div>
            <div style="font-size: 11px; color: #0284C7;">Назначены первые получатели</div>
          </div>
          <div class="kpi-card kpi-sla">
            <div class="kpi-label">На контроле сроков SLA</div>
            <div class="kpi-value">12</div>
            <div style="font-size: 11px; color: #F59E0B;">Остаток менее 24 часов</div>
          </div>
          <div class="kpi-card kpi-overdue">
            <div class="kpi-label">Просрочено исполнителем</div>
            <div class="kpi-value" style="color: #EF4444;">2</div>
            <div style="font-size: 11px; color: #EF4444;">Эскалировано руководству</div>
          </div>
          <div class="kpi-card kpi-anon">
            <div class="kpi-label">Доля анонимных сигналов</div>
            <div class="kpi-value" style="color: #10B981;">76%</div>
            <div style="font-size: 11px; color: #64748B;">Связь по защищенным токенам</div>
          </div>
        </div>

        <!-- Table Container -->
        <div class="table-container-card">
          <div class="filter-bar">
            <div class="filter-btn-group">
              <button class="filter-pill active">Все обращения</button>
              <button class="filter-pill">🔒 Анонимные (76%)</button>
              <button class="filter-pill">🦺 Охрана труда</button>
              <button class="filter-pill">💰 Оплата труда</button>
              <button class="filter-pill">⏱️ Угроза срыва SLA</button>
            </div>
            <div style="font-size: 12px; color: #64748B;">
              Автообновление реестра в реальном времени: <span style="color: #10B981; font-weight: 700;">● Синхронизировано</span>
            </div>
          </div>

          <table class="appeals-table">
            <thead>
              <tr>
                <th>Вх. номер / Код</th>
                <th>Дата регистрации</th>
                <th>Заявитель</th>
                <th>Филиал / Подразделение</th>
                <th>Категория / Суть</th>
                <th>Первый получатель</th>
                <th>Статус</th>
                <th>Контроль SLA (Дедлайн)</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody id="appeals-table-body">
              <!-- Live Registered Item will be prepended here -->
              <tr id="live-appeal-row" style="background: #F0FDF4; display: none;">
                <td>
                  <strong style="color: #00468C;" id="live-reg-num">ВХ-2026/0942-КАНЦ</strong><br>
                  <span style="font-size: 10px; color: #10B981; font-weight: 700;">● НОВОЕ (ИИ-ДИАЛОГ)</span>
                </td>
                <td id="live-reg-date">09.11.2026 17:35</td>
                <td>
                  <span class="badge-status status-closed" id="live-reg-anon">🔒 Анонимно (TK-7842)</span>
                </td>
                <td id="live-reg-branch">ОДС Западная РДТ</td>
                <td id="live-reg-category">
                  <strong>Охрана труда и СИЗ</strong><br>
                  <span style="font-size: 11px; color: #64748B;" id="live-reg-summary">Задержка зимней обуви и курток монтерам</span>
                </td>
                <td id="live-reg-assignee">
                  <strong>Департамент охраны труда</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Смагулов Б.К.</span>
                </td>
                <td>
                  <span class="badge-status status-work">В работе</span>
                </td>
                <td class="sla-timer-cell sla-green" id="live-table-sla">
                  ⏱️ 4д 23ч 59м
                </td>
                <td>
                  <button class="btn-table-action" onclick="viewAppealDetails()">👁️ Карточка</button>
                </td>
              </tr>

              <!-- Preloaded Static Samples -->
              <tr>
                <td><strong>ВХ-2026/0941-КАНЦ</strong></td>
                <td>08.11.2026 14:20</td>
                <td><span class="badge-status status-closed">🔒 Анонимно</span></td>
                <td>ОДС Восточная РДТ</td>
                <td>
                  <strong>Оплата труда</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Принуждение к выходу в субботу без табелирования</span>
                </td>
                <td>
                  <strong>Департамент оплаты труда</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Ким А.В.</span>
                </td>
                <td><span class="badge-status status-work">В работе</span></td>
                <td class="sla-timer-cell sla-yellow">⏱️ 1д 04ч 12м (Внимание)</td>
                <td><button class="btn-table-action" onclick="alert('Открыта карточка ВХ-2026/0941-КАНЦ')">👁️ Карточка</button></td>
              </tr>

              <tr>
                <td><strong>ВХ-2026/0938-КАНЦ</strong></td>
                <td>04.11.2026 09:15</td>
                <td><span class="badge-status status-new">👤 Искаков М.А.</span></td>
                <td>Северная РДТ</td>
                <td>
                  <strong>Инфраструктура и связь</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Перегрев узла связи, неисправность дизель-генератора</span>
                </td>
                <td>
                  <strong>Дивизион «Сеть» (ОДС)</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Техническая дирекция</span>
                </td>
                <td><span class="badge-status" style="background:#FEE2E2; color:#B91C1C;">Эскалация</span></td>
                <td class="sla-timer-cell sla-red">⚠️ ПРОСРОЧЕНО (4 часа)</td>
                <td><button class="btn-table-action" onclick="alert('Эскалация на Главного директора направлена')">⚡ Эскалировать</button></td>
              </tr>

              <tr>
                <td><strong>ВХ-2026/0935-КАНЦ</strong></td>
                <td>02.11.2026 11:40</td>
                <td><span class="badge-status status-closed">🔒 Анонимно</span></td>
                <td>Алматинский филиал</td>
                <td>
                  <strong>Корпоративная этика / Моббинг</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Моральное давление и угрозы увольнением от мастера</span>
                </td>
                <td>
                  <strong>Служба комплаенс и этики</strong><br>
                  <span style="font-size: 11px; color: #64748B;">Омбудсмен</span>
                </td>
                <td><span class="badge-status status-closed">Решено</span></td>
                <td class="sla-timer-cell" style="color: #64748B;">✅ Ответ дан в срок</td>
                <td><button class="btn-table-action" onclick="alert('Просмотр протокола расследования')">👁️ Карточка</button></td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </section>

    <!-- ==================== ЭКРАН 3: СВОДНАЯ АНАЛИТИКА И ОТЧЕТЫ ИИ ==================== -->
    <section id="screen-executive" class="screen-view">
      <div class="admin-container">
        
        <div class="admin-header-strip" style="background: linear-gradient(135deg, #0B132B, #00468C);">
          <div>
            <h2 style="font-size: 16px; font-weight: 800;">Панель руководства: Аналитический отчет ИИ и карта напряженности</h2>
            <span style="font-size: 11px; color: #BAE6FD;">Автоматическая аналитика On-Premise LLM по массиву 419 принятых обращений</span>
          </div>
          <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600;">
            ROLE_EXECUTIVE (Правление)
          </span>
        </div>

        <div style="padding: 24px;">
          
          <!-- AI Executive Report Card -->
          <div class="ai-narrative-box">
            <div class="ai-report-title">
              ✨ Сводный аналитический отчет ИИ (Executive AI Incident Intelligence)
            </div>
            <div style="font-size: 13px; line-height: 1.6; color: #1E293B;">
              <strong>1. Общая оценка социального спокойствия и очагов:</strong> За текущий отчетный период принято <strong>419 обращений</strong> (76% анонимно). Выявлена тенденция перетока «серых» обращений из личных переписок исполнителей в контролируемый контур МСЦ.<br><br>
              <strong>2. Выявленные системные очаги социальной напряженности:</strong>
              <ul class="ai-report-bullets">
                <li>
                  <strong style="color: #B91C1C;">Очаг №1: ОДС Западная РДТ (69 обращений):</strong> 
                  Критическая концентрация жалоб на задержку выдачи зимней обуви и спецодежды. Выявлен высокий риск отказа выездных бригад от выполнения аварийных работ при наступлении морозов (риск стихийного протеста). <em>Рекомендовано: экстренная передача 240 комплектов со склада Центрального аппарата.</em>
                </li>
                <li>
                  <strong style="color: #D97706;">Очаг №2: ОДС Восточная РДТ (34 обращения):</strong> 
                  Систематические жалобы на скрытые переработки по субботам без оплаты. Исполнители филиала нарушают требования ст. 108 ТК РК.
                </li>
                <li>
                  <strong style="color: #4338CA;">Очаг №3: Сервисная фабрика и автобазы (28 обращений):</strong> 
                  Простои служебного транспорта из-за задержек поставок запчастей и компенсаций ГСМ.
                </li>
              </ul>
              <strong>3. Дисциплина исполнения (SLA):</strong> Средний срок подготовки ответа снизился с 11 до <strong>4.2 рабочих дней</strong>. 87% обращений закрываются без срыва регламента.
            </div>
          </div>

          <!-- Charts Row -->
          <div class="exec-grid">
            <div class="exec-card">
              <h3 style="font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">
                Структура обращений по категориям нарушений
              </h3>
              <div style="height: 260px;">
                <canvas id="chartAppealsCategories"></canvas>
              </div>
            </div>

            <div class="exec-card">
              <h3 style="font-size: 14px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">
                Соблюдение сроков ответа (SLA) исполнителями по филиалам (%)
              </h3>
              <div style="height: 260px;">
                <canvas id="chartAppealsSLA"></canvas>
              </div>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- ==================== ЭКРАН 4: KEYCLOAK SSO ==================== -->
    <section id="screen-auth" class="screen-view">
      <div style="max-width: 440px; margin: 40px auto; background: white; border-radius: var(--radius-lg); border: 1px solid var(--border); box-shadow: var(--shadow-lg); overflow: hidden;">
        <div style="background: #00468C; color: white; padding: 24px; text-align: center;">
          <div style="font-size: 24px; font-weight: 800; margin-bottom: 4px;">KEYCLOAK SSO</div>
          <div style="font-size: 12px; color: #BAE6FD;">Единая точка входа АО «Казахтелеком»</div>
        </div>
        <div style="padding: 24px;">
          <p style="font-size: 12.5px; color: #64748B; margin-bottom: 16px;">
            Вход для сотрудников Канцелярии, службы безопасности, HR и Руководства компании:
          </p>
          <div style="display: flex; flex-direction: column; gap: 10px;">
            <button class="btn-send-survey-step" style="background: #00468C;" onclick="loginWithRole('admin')">
              Войти как Канцелярия / HR (ROLE_ADMIN)
            </button>
            <button class="btn-send-survey-step" style="background: #0284C7;" onclick="loginWithRole('executive')">
              Войти как Руководство (ROLE_EXECUTIVE)
            </button>
            <button class="btn-send-survey-step" style="background: #10B981;" onclick="switchScreen('screen-chat')">
              Анонимная приемная (Без Keycloak)
            </button>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ==================== МОДАЛЬНОЕ ОКНО ПРОВЕРКИ СТАТУСА ПО ТОКЕНУ ==================== -->
  <div id="token-lookup-modal" class="modal-overlay" onclick="closeTokenModal()">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="font-size: 16px; font-weight: 700; color: #00468C;">🔍 Проверка статуса обращения по токену</h3>
        <button style="border: none; background: transparent; font-size: 18px; cursor: pointer;" onclick="closeTokenModal()">✕</button>
      </div>

      <div style="margin-bottom: 14px;">
        <label style="font-size: 12px; font-weight: 600; color: #334155; display: block; margin-bottom: 6px;">
          Введите ваш секретный токен доступа:
        </label>
        <div style="display: flex; gap: 8px;">
          <input type="text" id="token-input-field" class="form-input" placeholder="Например: TK-7842-KZ" value="TK-7842-KZ" style="font-family: monospace; font-size: 14px; font-weight: 700;">
          <button class="btn-send-survey-step" style="width: auto; margin-top: 0; padding: 8px 16px;" onclick="searchTokenStatus()">
            Найти
          </button>
        </div>
      </div>

      <!-- Result Card -->
      <div id="token-result-card" style="display: block; background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: var(--radius-md); padding: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-weight: 700; color: #00468C;" id="modal-res-number">ВХ-2026/0942-КАНЦ</span>
          <span class="badge-status status-work" id="modal-res-status">В работе у исполнителя</span>
        </div>
        <div style="font-size: 12px; color: #64748B; margin-bottom: 8px;">
          Тема: <strong style="color: #0F172A;" id="modal-res-topic">Охрана труда: Задержка зимней обуви и курток</strong><br>
          Первый получатель: <strong style="color: #0F172A;" id="modal-res-assignee">Департамент охраны труда (Смагулов Б.К.)</strong>
        </div>
        <div style="background: white; border: 1px solid #E2E8F0; padding: 10px; border-radius: var(--radius-sm); font-size: 12px; margin-top: 8px;">
          💬 <strong>Ответ исполнителя (17:40):</strong> «Обращение принято в работу. Направлен запрос на центральный склад в г. Астана для перераспределения 18 комплектов утепленной обуви.»
        </div>
        <div style="margin-top: 10px; font-size: 11px; color: #10B981; font-weight: 600;">
          ⏱️ До окончания нормативного срока ответа: 4 дня 23 часа
        </div>
      </div>
    </div>
  </div>

  <!-- ==================== ИНТЕРАКТИВНЫЙ СЦЕНАРИЙ (JAVASCRIPT) ==================== -->
  <script>
    // Текущее состояние мастера обращения
    let currentStep = 'INPUT_PROBLEM'; // 'INPUT_PROBLEM', 'QUESTIONNAIRE', 'STATEMENT', 'ANONYMITY', 'REGISTERED'
    let currentLanguage = 'ru';
    let liveTimerInterval = null;
    let liveSecondsRemaining = 5 * 24 * 3600 - 15; // 5 рабочих дней

    // Модель текущего заводимого обращения
    let currentAppeal = {
      rawText: "",
      category: "Охрана труда и производственная безопасность (СИЗ)",
      branch: "ОДС Западная РДТ",
      scale: "Бригада АВР (18 сотрудников)",
      attempt: "Мастер отказал в выдаче из-за отсутствия на складе",
      isAnonymous: true,
      regNumber: "ВХ-2026/0942-КАНЦ",
      token: "TK-7842-KZ",
      recipient: "Департамент охраны труда и экологии (Смагулов Б.К.)",
      slaDays: 5,
      riskLevel: "YELLOW"
    };

    document.addEventListener("DOMContentLoaded", () => {
      initCharts();
      startSLACountdown();
    });

    // Переключение главных экранов
    function switchScreen(screenId) {
      document.querySelectorAll('.screen-view').forEach(el => el.classList.remove('active'));
      const target = document.getElementById(screenId);
      if (target) target.classList.add('active');

      document.querySelectorAll('.demo-nav-tabs .demo-tab-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.demo-nav-tabs .demo-tab-btn')).find(b => {
        const text = b.textContent.toLowerCase();
        if (screenId.includes('chat') && text.includes('диалог')) return true;
        if (screenId.includes('admin') && text.includes('канцеляр')) return true;
        if (screenId.includes('executive') && text.includes('аналитик')) return true;
        if (screenId.includes('auth') && text.includes('keycloak')) return true;
        return false;
      });
      if (activeBtn) activeBtn.classList.add('active');
    }

    // Быстрый выбор готовых кейсов
    function applyPresetCase(type) {
      const input = document.getElementById('chat-text-input');
      if (type === 'ppe') {
        input.value = "В филиале ОДС Запад уже 2 месяца не выдают зимнюю обувь и утепленные куртки. На складе говорят ждать декабря, а монтеры выезжают на аварии в мороз в летних ботинках.";
      } else if (type === 'overtime') {
        input.value = "Начальник районного участка заставляет оставаться после смены и выходить по субботам, табель закрывает как 8 часов. При отказе угрожает срезать премию.";
      } else {
        input.value = "На опорном узле связи неисправна система охлаждения и резервный генератор не запускается. Неоднократные заявки игнорируются, есть риск отключения абонентов.";
      }
      submitUserProblem();
    }

    // Шаг 1: Пользователь вводит проблему своими словами
    function submitUserProblem() {
      const input = document.getElementById('chat-text-input');
      const text = input.value.trim();
      if (!text) return;

      currentAppeal.rawText = text;
      input.value = "";
      
      // Скрываем быстрые чипсы
      const presets = document.getElementById('quick-presets-box');
      if (presets) presets.style.display = 'none';

      // Добавляем сообщение пользователя
      appendUserMessage(text);

      // ИИ показывает индикатор анализа
      showTypingIndicator(() => {
        // Шаг 2: ИИ выводит динамический опросник
        renderDynamicQuestionnaire();
      });
    }

    function handleInputKeypress(e) {
      if (e.key === 'Enter') submitUserProblem();
    }

    // Шаг 2: ИИ составляет и показывает адаптивный опросник
    function renderDynamicQuestionnaire() {
      currentStep = 'QUESTIONNAIRE';

      // Определяем категорию по ключевым словам
      let cat = "Охрана труда и производственная безопасность (СИЗ)";
      let risk = "🟡 Системный риск";
      if (currentAppeal.rawText.includes("преми") || currentAppeal.rawText.includes("суббот") || currentAppeal.rawText.includes("оплат")) {
        cat = "Трудовые отношения и оплата труда";
        currentAppeal.category = cat;
        currentAppeal.recipient = "Департамент оплаты труда и трудовых отношений (Ким А.В.)";
      } else if (currentAppeal.rawText.includes("генератор") || currentAppeal.rawText.includes("связ") || currentAppeal.rawText.includes("узел")) {
        cat = "Инфраструктура и надежность сети";
        currentAppeal.category = cat;
        currentAppeal.recipient = "Дивизион «Сеть» (Техническая дирекция)";
      }

      appendAIMessage(`
        Я проанализировал ваше описание проблемы.<br>
        <strong>Категория инцидента:</strong> <span style="color: #00468C; font-weight: 700;">${cat}</span> (${risk}).<br><br>
        Чтобы составить юридически выверенное заявление и точно назначить ответственных исполнителей, ответьте, пожалуйста, на <strong>3 уточняющих вопроса</strong>:
      `);

      const container = document.getElementById('dynamic-chat-content');
      const widget = document.createElement('div');
      widget.id = 'active-questionnaire-widget';
      widget.className = 'questionnaire-card';
      widget.innerHTML = `
        <div class="question-title">
          <span>📋 1. Укажите филиал / подразделение:</span>
        </div>
        <div class="options-btn-group" id="q1-options">
          <button class="option-btn selected" onclick="selectQOption('branch', 'ОДС Западная РДТ (Атырау / Актау)', this)">ОДС Западная РДТ (Атырау/Актау)</button>
          <button class="option-btn" onclick="selectQOption('branch', 'ОДС Восточная РДТ (Семей / Усть-Каменогорск)', this)">ОДС Восточная РДТ</button>
          <button class="option-btn" onclick="selectQOption('branch', 'Алматинский филиал', this)">Алматинский филиал</button>
          <button class="option-btn" onclick="selectQOption('branch', 'Астана / Головной офис', this)">Астана / ЦА</button>
        </div>

        <div class="question-title" style="margin-top: 14px;">
          <span>👥 2. Сколько сотрудников затронуто проблемой?</span>
        </div>
        <div class="options-btn-group" id="q2-options">
          <button class="option-btn" onclick="selectQOption('scale', 'Лично меня одного', this)">Лично меня одного</button>
          <button class="option-btn selected" onclick="selectQOption('scale', 'Вся выездная бригада (18 человек)', this)">Вся выездная бригада (18 чел)</button>
          <button class="option-btn" onclick="selectQOption('scale', 'Весь цех / участок (свыше 30 чел)', this)">Весь участок (>30 чел)</button>
        </div>

        <div class="question-title" style="margin-top: 14px;">
          <span>🗣️ 3. Обращались ли вы к непосредственному руководству?</span>
        </div>
        <div class="options-btn-group" id="q3-options">
          <button class="option-btn selected" onclick="selectQOption('attempt', 'Обращались устно к мастеру — получили отказ', this)">Да, получили устный отказ</button>
          <button class="option-btn" onclick="selectQOption('attempt', 'Обещали решить, но ничего не меняется больше месяца', this)">Обещали решить, но тянут время</button>
          <button class="option-btn" onclick="selectQOption('attempt', 'Нет, опасаемся прессинга и угроз', this)">Нет, опасаемся прессинга</button>
        </div>

        <button class="btn-send-survey-step" onclick="proceedToStatement()">
          📝 Сформировать официальное заявление
        </button>
      `;

      container.appendChild(widget);
      scrollChatToBottom();
    }

    function selectQOption(field, value, btn) {
      currentAppeal[field] = value;
      const group = btn.parentElement;
      group.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
    }

    // Шаг 3: ИИ формирует официальное заявление
    function proceedToStatement() {
      // Удаляем кнопки выбора в опроснике, оставляем сам виджет зафиксированным
      const qWidget = document.getElementById('active-questionnaire-widget');
      if (qWidget) {
        qWidget.style.opacity = '0.9';
        const submitBtn = qWidget.querySelector('.btn-send-survey-step');
        if (submitBtn) submitBtn.remove();
      }

      showTypingIndicator(() => {
        appendAIMessage(`
          Спасибо за ответы! На основе предоставленных фактов я сформировал <strong>проект официального заявления</strong> в соответствии с регламентом АО «Казахтелеком».
        `);

        const container = document.getElementById('dynamic-chat-content');
        const statementCard = document.createElement('div');
        statementCard.className = 'formal-statement-card';
        statementCard.innerHTML = `
          <div class="statement-header-stamp">
            <div>
              <div class="statement-title-h3">КАРТОЧКА ОБРАЩЕНИЯ (ПРОЕКТ)</div>
              <div style="font-size: 11px; color: #64748B;">АО «Казахтелеком» • Центр мониторинга и социального партнерства</div>
            </div>
            <span style="background: #FEF3C7; color: #92400E; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 4px;">
              🟡 Системный риск
            </span>
          </div>

          <div class="statement-field-row">
            <span class="statement-label">Категория:</span>
            <span class="statement-value"><strong>${currentAppeal.category}</strong></span>
          </div>
          <div class="statement-field-row">
            <span class="statement-label">Подразделение:</span>
            <span class="statement-value">${currentAppeal.branch}</span>
          </div>
          <div class="statement-field-row">
            <span class="statement-label">Масштаб:</span>
            <span class="statement-value">${currentAppeal.scale}</span>
          </div>
          <div class="statement-field-row">
            <span class="statement-label">Предыстория:</span>
            <span class="statement-value">${currentAppeal.attempt}</span>
          </div>

          <div class="statement-fabula-box">
            <strong>Фабула заявления (составлено ИИ):</strong><br>
            «Заявитель сообщает о факте несоблюдения положений ст. 182 ТК РК и п. 4.2 Коллективного договора компании в части своевременного материально-технического снабжения. 
            Суть: ${currentAppeal.rawText} 
            Действия на месте результата не принесли. Имеется риск срыва выполнения аварийно-восстановительных работ.»
          </div>

          <!-- Шаг 4: Вопрос об анонимности -->
          <div style="margin-top: 16px; border-top: 1px dashed #CBD5E1; padding-top: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 6px;">
              🔒 Выберите режим конфиденциальности подачи:
            </div>
            <div style="font-size: 11.5px; color: #64748B; margin-bottom: 10px;">
              Компания гарантирует защиту ваших прав в любом из выбранных вариантов.
            </div>

            <div class="anonymity-grid">
              <div class="anonymity-card active-anon" id="card-opt-anon" onclick="chooseAnonymityMode(true)">
                <div class="anon-title" style="color: #059669;">
                  <span>🔒 Подать АНОНИМНО</span>
                </div>
                <div class="anon-desc">
                  ФИО и контакты скрыты. Связь и проверка статуса происходят через секретный токен доступа <strong>TK-7842-KZ</strong>.
                </div>
              </div>

              <div class="anonymity-card" id="card-opt-official" onclick="chooseAnonymityMode(false)">
                <div class="anon-title" style="color: #00468C;">
                  <span>👤 Подать ОФИЦИАЛЬНО</span>
                </div>
                <div class="anon-desc">
                  В карточку будут внесены учетные данные заявителя для получения официального бумажного ответа на бланке канцелярии.
                </div>
              </div>
            </div>

            <button class="btn-send-survey-step" style="margin-top: 14px; background: linear-gradient(135deg, #00468C, #0284C7);" onclick="registerInChancellery()">
              🏛️ Утвердить и зарегистрировать в Канцелярии
            </button>
          </div>
        `;

        container.appendChild(statementCard);
        scrollChatToBottom();
      });
    }

    function chooseAnonymityMode(isAnon) {
      currentAppeal.isAnonymous = isAnon;
      document.getElementById('card-opt-anon').className = isAnon ? 'anonymity-card active-anon' : 'anonymity-card';
      document.getElementById('card-opt-official').className = isAnon ? 'anonymity-card' : 'anonymity-card active-official';
    }

    // Шаг 5, 6, 7: Регистрация канцелярией, назначение получателя и запуск таймера SLA
    function registerInChancellery() {
      showTypingIndicator(() => {
        appendAIMessage(`
          🏛️ <strong>Обращение успешно зарегистрировано в Канцелярии АО «Казахтелеком»!</strong><br>
          Ему присвоен официальный регистрационный номер и назначен первый профильный исполнитель.
        `);

        const container = document.getElementById('dynamic-chat-content');

        // Шаг 5: Карточка регистрации
        const regCard = document.createElement('div');
        regCard.className = 'chancellery-stamp-card';
        regCard.innerHTML = `
          <div class="stamp-badge">
            🏛️ ЗАРЕГИСТРИРОВАНО В КАНЦЕЛЯРИИ
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12.5px; margin-bottom: 10px;">
            <div>Входящий номер: <strong style="color: #00468C;">${currentAppeal.regNumber}</strong></div>
            <div>Дата регистрации: <strong>09.11.2026, 17:35</strong></div>
            <div>Статус: <strong style="color: #0284C7;">В ОБРАБОТКЕ (ПРИНЯТО)</strong></div>
            <div>Режим: <strong>${currentAppeal.isAnonymous ? '🔒 Конфиденциально' : '👤 Официально'}</strong></div>
          </div>

          <div style="font-size: 11.5px; color: #475569; margin-top: 6px;">
            Ваш персональный токен для отслеживания и безопасного чата с исполнителем:
          </div>
          <div class="token-display-box">
            <span>${currentAppeal.token}</span>
            <button class="btn-copy-token" onclick="copyTokenValue('${currentAppeal.token}')">📋 Скопировать</button>
          </div>
        `;

        // Шаг 6: Карточка назначения первого получателя (Маршрутизация)
        const routingCard = document.createElement('div');
        routingCard.className = 'routing-card';
        routingCard.innerHTML = `
          <div class="routing-header">
            🎯 Первый получатель и маршрутизация ИИ
          </div>
          <div style="font-size: 13px; color: #0F172A; margin-bottom: 4px;">
            Ответственное подразделение: <strong>${currentAppeal.recipient}</strong>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">
            👥 На контроле: <strong>Центр мониторинга (МСЦ) и Технический инспектор Профсоюза</strong><br>
            🛡️ <em>Анти-конфликт интересов: прямое руководство участка исключено из модерации жалобы.</em>
          </div>
        `;

        // Шаг 7: Контроль сроков ответа (SLA-таймер)
        const slaCard = document.createElement('div');
        slaCard.className = 'sla-timer-widget';
        slaCard.innerHTML = `
          <div>
            <div style="font-size: 11px; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.5px;">
              ⏱️ Контроль нормативного срока ответа (SLA):
            </div>
            <div class="sla-countdown-digits" id="chat-live-sla-timer">
              04д 23ч 59м 45с
            </div>
            <div style="font-size: 11px; color: #CBD5E1; margin-top: 2px;">
              Крайний срок: <strong>16 ноября 2026 г., 18:00</strong> (5 рабочих дней)
            </div>
          </div>
          <div style="text-align: right;">
            <div class="sla-badge-zone">🟢 В СПОКОЙНОЙ ЗОНЕ</div>
            <button class="btn-send-survey-step" style="margin-top: 8px; padding: 6px 12px; font-size: 11.5px; background: #0284C7;" onclick="switchScreen('screen-admin')">
              📋 Посмотреть в Реестре Канцелярии
            </button>
          </div>
        `;

        container.appendChild(regCard);
        container.appendChild(routingCard);
        container.appendChild(slaCard);
        scrollChatToBottom();

        // Обновляем данные в таблице Канцелярии (Экран 2)
        activateLiveAppealInTable();
      });
    }

    // Активация зарегистрированного обращения в таблице Канцелярии
    function activateLiveAppealInTable() {
      const row = document.getElementById('live-appeal-row');
      if (row) {
        row.style.display = 'table-row';
        document.getElementById('live-reg-num').textContent = currentAppeal.regNumber;
        document.getElementById('live-reg-anon').textContent = currentAppeal.isAnonymous ? `🔒 Анонимно (${currentAppeal.token})` : '👤 Официально';
        document.getElementById('live-reg-branch').textContent = currentAppeal.branch;
        document.getElementById('live-reg-category').innerHTML = `<strong>${currentAppeal.category}</strong><br><span style="font-size:11px; color:#64748B;">${currentAppeal.rawText.substring(0, 48)}...</span>`;
        document.getElementById('live-reg-assignee').innerHTML = `<strong>${currentAppeal.recipient.split('(')[0]}</strong><br><span style="font-size:11px; color:#64748B;">${currentAppeal.recipient.includes('(') ? currentAppeal.recipient.split('(')[1].replace(')', '') : ''}</span>`;
      }
      // Увеличиваем счетчик KPI
      const kpiTot = document.getElementById('kpi-total-val');
      if (kpiTot) kpiTot.textContent = "420";
    }

    // Живой обратный таймер SLA
    function startSLACountdown() {
      if (liveTimerInterval) clearInterval(liveTimerInterval);
      liveTimerInterval = setInterval(() => {
        liveSecondsRemaining--;
        if (liveSecondsRemaining < 0) liveSecondsRemaining = 0;

        const days = Math.floor(liveSecondsRemaining / (24 * 3600));
        const hours = Math.floor((liveSecondsRemaining % (24 * 3600)) / 3600);
        const mins = Math.floor((liveSecondsRemaining % 3600) / 60);
        const secs = liveSecondsRemaining % 60;

        const str = `0${days}д ${hours < 10 ? '0' : ''}${hours}ч ${mins < 10 ? '0' : ''}${mins}м ${secs < 10 ? '0' : ''}${secs}с`;
        
        const chatTimer = document.getElementById('chat-live-sla-timer');
        if (chatTimer) chatTimer.textContent = str;

        const tableTimer = document.getElementById('live-table-sla');
        if (tableTimer) tableTimer.textContent = `⏱️ ${days}д ${hours}ч ${mins}м`;
      }, 1000);
    }

    // Вспомогательные функции добавления сообщений
    function appendUserMessage(text) {
      const stream = document.getElementById('chat-messages-container');
      const content = document.getElementById('dynamic-chat-content');
      
      const userRow = document.createElement('div');
      userRow.className = 'chat-msg-row user';
      userRow.innerHTML = `
        <div class="msg-avatar user">Я</div>
        <div class="msg-content-wrapper">
          <div class="msg-bubble">${text}</div>
          <div class="msg-meta-row" style="justify-content: flex-end;">
            <span>17:34</span>
          </div>
        </div>
      `;
      stream.insertBefore(userRow, content);
      scrollChatToBottom();
    }

    function appendAIMessage(html) {
      const stream = document.getElementById('chat-messages-container');
      const content = document.getElementById('dynamic-chat-content');
      
      const aiRow = document.createElement('div');
      aiRow.className = 'chat-msg-row ai';
      aiRow.innerHTML = `
        <div class="msg-avatar ai">ИИ</div>
        <div class="msg-content-wrapper" style="width: 100%;">
          <div class="msg-bubble">${html}</div>
          <div class="msg-meta-row">
            <span>Только что</span>
          </div>
        </div>
      `;
      stream.insertBefore(aiRow, content);
      scrollChatToBottom();
    }

    function showTypingIndicator(callback) {
      const stream = document.getElementById('chat-messages-container');
      const content = document.getElementById('dynamic-chat-content');

      const typing = document.createElement('div');
      typing.id = 'temp-typing-indicator';
      typing.className = 'chat-msg-row ai';
      typing.innerHTML = `
        <div class="msg-avatar ai">ИИ</div>
        <div class="typing-bubble">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <span style="font-size: 11px; color: #64748B; margin-left: 6px;">ИИ анализирует фактуру...</span>
        </div>
      `;
      stream.insertBefore(typing, content);
      scrollChatToBottom();

      setTimeout(() => {
        const el = document.getElementById('temp-typing-indicator');
        if (el) el.remove();
        if (callback) callback();
      }, 700);
    }

    function scrollChatToBottom() {
      const stream = document.getElementById('chat-messages-container');
      if (stream) {
        setTimeout(() => {
          stream.scrollTop = stream.scrollHeight;
        }, 50);
      }
    }

    function resetChatFlow() {
      document.getElementById('dynamic-chat-content').innerHTML = "";
      document.querySelectorAll('.chat-msg-row.user').forEach(e => e.remove());
      const presets = document.getElementById('quick-presets-box');
      if (presets) presets.style.display = 'flex';
      currentStep = 'INPUT_PROBLEM';
    }

    function copyTokenValue(token) {
      navigator.clipboard.writeText(token);
      alert(`Секретный токен ${token} скопирован в буфер обмена!`);
    }

    // Модальное окно поиска по токену
    function openTokenModal() {
      document.getElementById('token-lookup-modal').classList.add('active');
    }

    function closeTokenModal() {
      document.getElementById('token-lookup-modal').classList.remove('active');
    }

    function searchTokenStatus() {
      const code = document.getElementById('token-input-field').value.trim();
      alert(`Данные по обращению ${code} загружены. Статус: В работе у исполнителя. Дедлайн: соблюдается.`);
    }

    function viewAppealDetails() {
      alert(`Детальная карточка ${currentAppeal.regNumber}\nКатегория: ${currentAppeal.category}\nФилиал: ${currentAppeal.branch}\nПервый получатель: ${currentAppeal.recipient}\nКонтроль сроков: Норматив 5 дней, в процессе исполнения.`);
    }

    function loginWithRole(role) {
      if (role === 'admin') {
        alert("Вход выполнен успешно через Keycloak SSO (Пользователь: Айман Медебекова, Роль: ROLE_CHANCELLERY). Открывается Реестр Канцелярии.");
        switchScreen('screen-admin');
      } else {
        alert("Вход выполнен успешно через Keycloak SSO (Пользователь: Член Правления, Роль: ROLE_EXECUTIVE). Открывается Панель руководства.");
        switchScreen('screen-executive');
      }
    }

    function toggleLanguage() {
      currentLanguage = currentLanguage === 'ru' ? 'kz' : 'ru';
      document.getElementById('lang-indicator').textContent = currentLanguage === 'ru' ? '🌐 Русский' : '🌐 Қазақша';
    }

    // Инициализация графиков в Панели руководства
    function initCharts() {
      // 1. Диаграмма категорий обращений
      const ctxCat = document.getElementById('chartAppealsCategories');
      if (ctxCat) {
        new Chart(ctxCat, {
          type: 'doughnut',
          data: {
            labels: ['Охрана труда и СИЗ', 'Оплата труда и надбавки', 'Условия труда и оборудование', 'Давление руководства/Моббинг', 'Бытовые вопросы'],
            datasets: [{
              data: [38, 29, 16, 11, 6],
              backgroundColor: ['#00468C', '#0284C7', '#6366F1', '#F59E0B', '#94A3B8'],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
            }
          }
        });
      }

      // 2. График соблюдения SLA исполнителями по филиалам
      const ctxSLA = document.getElementById('chartAppealsSLA');
      if (ctxSLA) {
        new Chart(ctxSLA, {
          type: 'bar',
          data: {
            labels: ['Западная РДТ', 'Восточная РДТ', 'Северная РДТ', 'Южная РДТ', 'Алматы', 'Астана', 'ДЦБ IT'],
            datasets: [{
              label: 'Соблюдение SLA (%)',
              data: [81, 84, 88, 92, 95, 96, 99],
              backgroundColor: ['#F59E0B', '#F59E0B', '#0284C7', '#0284C7', '#10B981', '#10B981', '#10B981'],
              borderRadius: 6
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { min: 60, max: 100 } }
          }
        });
      }
    }
  </script>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Updated index.html successfully!")

