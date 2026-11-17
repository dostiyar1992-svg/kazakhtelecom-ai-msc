# -*- coding: utf-8 -*-
"""
Full Production-Grade HTML Generator for:
АО «Казахтелеком» - Единая интеллектуальная платформа EX и мониторинга социального климата (Версия 6.0)
Complies with MASTER_ENGINEERING_PROMPT.md and ТЗ_ИИ_Мониторинг_Казахтелеком.md
"""

import sys

def generate_html():
    html_content = r'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ИИ-Приемная и Мониторинг Социального Климата | АО «Казахтелеком»</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
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
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.03);
      --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
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
      border-bottom: 2px solid rgba(2, 132, 199, 0.35);
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
      gap: 16px;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 260px;
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
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .brand-info h1 {
      font-size: 13.5px;
      font-weight: 800;
      color: #F8FAFC;
      letter-spacing: -0.2px;
      white-space: nowrap;
    }

    .brand-info span {
      font-size: 11px;
      color: #94A3B8;
      display: block;
    }

    /* ROLE SWITCHER PILL IN TOPBAR */
    .role-switcher-container {
      display: flex;
      align-items: center;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: var(--radius-full);
      padding: 3px 6px;
      gap: 4px;
    }

    .role-switcher-label {
      font-size: 11px;
      font-weight: 700;
      color: #94A3B8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 0 8px;
    }

    .role-btn {
      background: transparent;
      border: none;
      color: #CBD5E1;
      padding: 5px 12px;
      font-size: 11.5px;
      font-weight: 600;
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
      background: #0284C7;
      color: white;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.5);
      font-weight: 700;
    }

    /* TOPBAR RIGHT ACTIONS */
    .topbar-right-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-nudge-trigger {
      background: linear-gradient(135deg, #10B981, #059669);
      color: white;
      border: none;
      padding: 6px 14px;
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
      transition: transform 0.15s ease;
    }

    .btn-nudge-trigger:hover {
      transform: translateY(-1px);
    }

    .cdn-user-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 4px 12px;
      border-radius: var(--radius-full);
      font-size: 11.5px;
      cursor: pointer;
      transition: background 0.2s ease;
    }

    .cdn-user-pill:hover {
      background: rgba(255, 255, 255, 0.16);
    }

    .cdn-badge-indicator {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10B981;
      box-shadow: 0 0 8px #10B981;
      animation: pulseGreen 2s infinite;
    }

    @keyframes pulseGreen {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* SECONDARY NAVIGATION BAR (WORKSPACE TABS) */
    .workspace-subnav {
      background: #FFFFFF;
      border-bottom: 1px solid var(--border);
      padding: 6px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: var(--shadow-sm);
    }

    .canvas-nav-tabs {
      display: flex;
      gap: 6px;
      overflow-x: auto;
    }

    .nav-tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #475569;
      padding: 7px 14px;
      font-size: 12.5px;
      font-weight: 600;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .nav-tab-btn:hover {
      color: var(--primary);
      background: #F1F5F9;
    }

    .nav-tab-btn.active {
      background: var(--primary-light);
      color: var(--primary);
      border-color: rgba(0, 70, 140, 0.2);
      font-weight: 700;
    }

    .role-badge-pill {
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      background: #E2E8F0;
      color: #334155;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* MAIN VIEWPORT */
    .canvas-viewport {
      flex: 1;
      padding: 24px;
      max-width: 1440px;
      width: 100%;
      margin: 0 auto;
    }

    .canvas-screen {
      display: none;
      animation: fadeIn 0.2s ease;
    }

    .canvas-screen.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* COMMON UI ELEMENTS */
    .btn-action-primary {
      background: #00468C;
      color: white;
      border: none;
      padding: 9px 18px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      box-shadow: 0 2px 4px rgba(0, 70, 140, 0.2);
    }

    .btn-action-primary:hover {
      background: #00366D;
      box-shadow: 0 4px 8px rgba(0, 70, 140, 0.3);
    }

    .btn-action-secondary {
      background: #FFFFFF;
      color: #334155;
      border: 1px solid var(--border-dark);
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }

    .btn-action-secondary:hover {
      background: #F8FAFC;
      border-color: #94A3B8;
    }

    .badge-status {
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .status-work { background: #FEF3C7; color: #B45309; }
    .status-closed { background: #E0E7FF; color: #4338CA; }
    .status-escalated { background: #FEE2E2; color: #B91C1C; }
    .status-success { background: #DCFCE7; color: #15803D; }

    /* FORM STYLES */
    .form-group {
      margin-bottom: 16px;
    }

    .form-label {
      display: block;
      font-size: 12.5px;
      font-weight: 700;
      color: #1E293B;
      margin-bottom: 6px;
    }

    .form-control {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--border-dark);
      border-radius: var(--radius-sm);
      font-size: 13px;
      color: var(--text-main);
      background: #FFFFFF;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .form-control:focus {
      outline: none;
      border-color: #0284C7;
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }

    /* PORTAL TILES */
    .portal-banner-hero {
      background: linear-gradient(135deg, #00468C 0%, #002D5C 100%);
      color: white;
      border-radius: var(--radius-lg);
      padding: 28px 32px;
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: var(--shadow-lg);
      position: relative;
      overflow: hidden;
    }

    .portal-banner-hero::after {
      content: '';
      position: absolute;
      right: -30px;
      top: -40px;
      width: 220px;
      height: 220px;
      background: radial-gradient(circle, rgba(2, 132, 199, 0.3) 0%, rgba(255,255,255,0) 70%);
      border-radius: 50%;
    }

    .hero-text-col h2 {
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 8px;
    }

    .hero-text-col p {
      font-size: 13.5px;
      color: #BAE6FD;
      max-width: 680px;
      line-height: 1.5;
    }

    .portal-action-tiles-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-bottom: 24px;
    }

    .action-tile-card {
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .action-tile-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-md);
      border-color: #0284C7;
    }

    .tile-icon {
      font-size: 32px;
      margin-bottom: 12px;
    }

    .tile-title {
      font-size: 15px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 6px;
    }

    .tile-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.4;
      margin-bottom: 14px;
    }

    .tile-footer {
      font-size: 12px;
      font-weight: 700;
      color: #00468C;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* CHAT STREAM */
    .chat-layout-wrapper {
      background: #FFFFFF;
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-md);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 720px;
    }

    .chat-header {
      background: #F8FAFC;
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .ai-avatar-circle {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 14px;
      box-shadow: 0 2px 6px rgba(0, 70, 140, 0.4);
    }

    .chat-stream-body {
      flex: 1;
      padding: 24px;
      overflow-y: auto;
      background: #F8FAFC;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .chat-msg-row {
      display: flex;
      gap: 12px;
      max-width: 82%;
    }

    .chat-msg-row.ai {
      align-self: flex-start;
    }

    .chat-msg-row.user {
      align-self: flex-end;
      flex-direction: row-reverse;
    }

    .msg-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 12px;
      flex-shrink: 0;
    }

    .msg-avatar.ai {
      background: #00468C;
      color: white;
    }

    .msg-avatar.user {
      background: #0284C7;
      color: white;
    }

    .msg-bubble {
      padding: 14px 18px;
      border-radius: var(--radius-md);
      font-size: 13px;
      line-height: 1.5;
    }

    .chat-msg-row.ai .msg-bubble {
      background: #FFFFFF;
      border: 1px solid var(--border);
      color: #1E293B;
      box-shadow: var(--shadow-sm);
    }

    .chat-msg-row.user .msg-bubble {
      background: #00468C;
      color: white;
    }

    .formal-statement-card {
      background: #FFFFFF;
      border: 1.5px solid #00468C;
      border-radius: var(--radius-md);
      padding: 16px;
      margin-top: 10px;
      box-shadow: var(--shadow-sm);
    }

    .chat-input-bar {
      background: #FFFFFF;
      border-top: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .sla-timer-widget {
      background: #0F172A;
      color: white;
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 12px;
    }

    .sla-countdown-digits {
      font-family: 'JetBrains Mono', monospace;
      font-size: 16px;
      font-weight: 700;
      color: #38BDF8;
    }

    /* PULSE SURVEY */
    .pulse-block-card {
      background: white;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }

    .pulse-scale-row {
      display: flex;
      gap: 10px;
      margin-top: 10px;
    }

    .pulse-scale-btn {
      flex: 1;
      padding: 12px 6px;
      background: #F8FAFC;
      border: 1px solid var(--border-dark);
      border-radius: var(--radius-sm);
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
      font-weight: 600;
      font-size: 13px;
    }

    .pulse-scale-btn:hover {
      background: #EBF3FA;
      border-color: #0284C7;
    }

    .pulse-scale-btn.selected {
      background: #00468C;
      color: white;
      border-color: #00468C;
      box-shadow: 0 2px 6px rgba(0, 70, 140, 0.3);
    }

    .synergy-appeal-prompt {
      background: linear-gradient(135deg, #FEF2F2, #FFF7ED);
      border: 1.5px solid #EF4444;
      border-radius: var(--radius-md);
      padding: 16px;
      margin-top: 14px;
      display: none;
      animation: slideDown 0.25s ease;
    }

    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* TABLES */
    .appeals-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 12.5px;
    }

    .appeals-table th {
      background: #F8FAFC;
      padding: 12px 14px;
      text-align: left;
      font-weight: 700;
      color: #475569;
      border-bottom: 2px solid var(--border);
      white-space: nowrap;
    }

    .appeals-table td {
      padding: 14px;
      border-bottom: 1px solid var(--border);
      color: #1E293B;
      vertical-align: middle;
    }

    .appeals-table tr:hover td {
      background: #F8FAFC;
    }

    /* KAZAKHSTAN 20-REGION HEATMAP TILES */
    .heatmap-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-top: 16px;
    }

    .region-tile {
      background: white;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
    }

    .region-tile:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .region-tile.risk-critical {
      border-color: #EF4444;
      background: #FEF2F2;
    }

    .region-tile.risk-high {
      border-color: #F59E0B;
      background: #FFFBEB;
    }

    .region-tile.risk-moderate {
      border-color: #3B82F6;
      background: #EFF6FF;
    }

    .region-tile.risk-low {
      border-color: #10B981;
      background: #F0FDF4;
    }

    .region-tile-title {
      font-size: 13px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 4px;
    }

    .region-tile-score {
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    /* MODALS */
    .modal-backdrop-nudge {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(11, 19, 43, 0.7);
      backdrop-filter: blur(4px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      animation: fadeIn 0.2s ease;
    }

    .modal-backdrop-nudge.active {
      display: flex;
    }

    .nudge-modal-card {
      background: #FFFFFF;
      border-radius: var(--radius-lg);
      width: 580px;
      max-width: 95%;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.2);
      overflow: hidden;
      animation: popUp 0.25s ease;
    }

    @keyframes popUp {
      from { transform: scale(0.95); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .nudge-header {
      background: linear-gradient(135deg, #00468C, #0284C7);
      color: white;
      padding: 20px 24px;
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .nudge-avatar-pulse {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      border: 2px solid rgba(255, 255, 255, 0.4);
    }

    .nudge-options-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding: 20px 24px;
    }

    .nudge-option-btn {
      background: #FFFFFF;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      gap: 14px;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .nudge-option-btn:hover {
      border-color: #0284C7;
      background: #F0F9FF;
      transform: translateX(3px);
    }

    /* TOAST */
    .toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 3000;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .toast-pill {
      background: #0F172A;
      color: white;
      padding: 12px 20px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 500;
      box-shadow: var(--shadow-xl);
      display: flex;
      align-items: center;
      gap: 10px;
      border-left: 4px solid #10B981;
      animation: toastIn 0.25s ease;
    }

    @keyframes toastIn {
      from { transform: translateX(50px); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    /* OFFICIAL STAMP STYLING */
    .chancellery-official-stamp {
      border: 2.5px solid #00468C;
      border-radius: 6px;
      padding: 14px 18px;
      background: #FFFFFF;
      color: #00468C;
      font-family: 'Inter', sans-serif;
      display: inline-block;
      box-shadow: 0 4px 12px rgba(0, 70, 140, 0.15);
      position: relative;
    }

    .stamp-header {
      font-size: 11px;
      font-weight: 900;
      letter-spacing: 1px;
      text-align: center;
      border-bottom: 1.5px solid #00468C;
      padding-bottom: 4px;
      margin-bottom: 8px;
      text-transform: uppercase;
    }

    .stamp-row {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      font-size: 12px;
      margin-bottom: 4px;
    }

    .stamp-row strong {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
    }
  </style>
</head>
<body>

  <!-- ==================== TOP GLOBAL CONTROLLER NAVBAR ==================== -->
  <header class="canvas-topbar">
    <div class="brand-group">
      <div class="brand-logo-badge">
        <span>ҚТ</span>
      </div>
      <div class="brand-info">
        <h1>ҚАЗАҚТЕЛЕКОМ • ИИ-ПРИЕМНАЯ & EX</h1>
        <span>Единая платформа мониторинга климата и обращений v6.0</span>
      </div>
    </div>

    <!-- ROLE SWITCHER IN TOPBAR -->
    <div class="role-switcher-container">
      <span class="role-switcher-label">Роль:</span>
      <button class="role-btn active" id="btn-role-employee" onclick="switchRole('ROLE_EMPLOYEE')">
        👤 Сотрудник
      </button>
      <button class="role-btn" id="btn-role-ex" onclick="switchRole('ROLE_EX_SERVICE')">
        🛠️ EX-Служба
      </button>
      <button class="role-btn" id="btn-role-chancellery" onclick="switchRole('ROLE_CHANCELLERY')">
        📋 Канцелярия
      </button>
      <button class="role-btn" id="btn-role-executive" onclick="switchRole('ROLE_EXECUTIVE')">
        👔 Руководство
      </button>
    </div>

    <!-- RIGHT ACTIONS: NUDGE & USER PROFILE -->
    <div class="topbar-right-actions">
      <button class="btn-nudge-trigger" onclick="openNudgeModal()">
        💬 Чекин CDN
      </button>
      <div class="cdn-user-pill" onclick="openProfileModal()" title="SSO Профиль CDN">
        <div class="cdn-badge-indicator"></div>
        <span id="topbar-username">Ахметов Д.Б. (ОДС Запад)</span>
      </div>
    </div>
  </header>

  <!-- ==================== SECONDARY WORKSPACE SUBNAV ==================== -->
  <div class="workspace-subnav">
    <nav class="canvas-nav-tabs">
      <button class="nav-tab-btn active" id="tabbtn-portal" onclick="switchCanvasTab('tab-portal')">
        🏠 Портал сотрудника
      </button>
      <button class="nav-tab-btn" id="tabbtn-chat" onclick="switchCanvasTab('tab-chat')">
        💬 ИИ-Приемная (Чат)
      </button>
      <button class="nav-tab-btn" id="tabbtn-pulse" onclick="switchCanvasTab('tab-pulse')">
        📊 Пульс-Опрос (Q4)
      </button>
      <button class="nav-tab-btn" id="tabbtn-form" onclick="switchCanvasTab('tab-form')">
        📝 Прямой ввод (Форма)
      </button>
      <button class="nav-tab-btn" id="tabbtn-ex" onclick="switchCanvasTab('tab-ex-service')">
        🛠️ EX-Студия & Аналитика
      </button>
      <button class="nav-tab-btn" id="tabbtn-chancellery" onclick="switchCanvasTab('tab-chancellery')">
        📋 Канцелярия & Реестр SLA
      </button>
      <button class="nav-tab-btn" id="tabbtn-executive" onclick="switchCanvasTab('tab-executive')">
        📈 Руководство & Тепловая карта
      </button>
    </nav>
    <div class="role-badge-pill" id="active-role-indicator">
      <span>Активная роль:</span> <strong id="active-role-text" style="color: #00468C;">ROLE_EMPLOYEE (Сотрудник)</strong>
    </div>
  </div>

  <!-- ==================== MAIN VIEWPORT ==================== -->
  <main class="canvas-viewport">

    <!-- ========================================================================= -->
    <!-- 1. WORKSPACE: EMPLOYEE PORTAL (ROLE_EMPLOYEE)                             -->
    <!-- ========================================================================= -->
    <section id="tab-portal" class="canvas-screen active">
      <!-- Welcome Hero Banner -->
      <div class="portal-banner-hero">
        <div class="hero-text-col">
          <h2 id="portal-welcome-name">Сәлеметсіз бе, Данияр Бауыржанұлы!</h2>
          <p>
            Добро пожаловать в единый центр заботы о сотрудниках АО «Казахтелеком». 
            Здесь вы можете пройти регулярный ежеквартальный срез климата, открыто сообщить о проблемах условий труда или подать официальное обращение в Канцелярию со 100% гарантией защиты заявителя.
          </p>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px;">
          <button class="btn-action-primary" style="background: white; color: #00468C;" onclick="openNudgeModal()">
            💬 Начать чекин-диалог
          </button>
          <button class="btn-action-secondary" style="background: rgba(255,255,255,0.15); color:white; border-color:rgba(255,255,255,0.3);" onclick="openTokenModal()">
            🔍 Проверить статус по токену
          </button>
        </div>
      </div>

      <!-- Action Tiles (4 primary routes) -->
      <div class="portal-action-tiles-grid">
        <div class="action-tile-card" onclick="switchCanvasTab('tab-pulse')">
          <div>
            <div class="tile-icon">📊</div>
            <div class="tile-title">Пульс-опрос Q4 2026</div>
            <div class="tile-desc">Ежеквартальный срез климата: отношение к компании, психологическая безопасность и условия труда (60 сек).</div>
          </div>
          <div class="tile-footer">Пройти опрос →</div>
        </div>

        <div class="action-tile-card" onclick="switchCanvasTab('tab-chat')">
          <div>
            <div class="tile-icon">💬</div>
            <div class="tile-title">Диалог с ИИ-Агентом</div>
            <div class="tile-desc">Опишите проблему своими словами. ИИ задаст 3 вопроса и подготовит официальное заявление со статьями ТК РК.</div>
          </div>
          <div class="tile-footer">Начать диалог →</div>
        </div>

        <div class="action-tile-card" onclick="switchCanvasTab('tab-form')">
          <div>
            <div class="tile-icon">📝</div>
            <div class="tile-title">Самостоятельная подача</div>
            <div class="tile-desc">Прямой ввод заявления без чат-бота: выберите дивизион, регион, прикрепите файлы и зарегистрируйте в Канцелярии.</div>
          </div>
          <div class="tile-footer">Заполнить форму →</div>
        </div>

        <div class="action-tile-card" onclick="switchCanvasTab('tab-chancellery')">
          <div>
            <div class="tile-icon">📋</div>
            <div class="tile-title">Реестр Канцелярии & SLA</div>
            <div class="tile-desc">Сквозной журнал входящих документов (Lotus Notes), таймеры дедлайнов (5 дней) и проверка статуса по токену.</div>
          </div>
          <div class="tile-footer">Открыть реестр →</div>
        </div>
      </div>

      <!-- User Active Case Card & Legal Protection -->
      <div style="display:grid; grid-template-columns: 1.4fr 1fr; gap: 20px;">
        <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; box-shadow: var(--shadow-sm);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #E2E8F0; padding-bottom:10px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:18px;">📂</span>
              <h3 style="font-size:14px; font-weight:800; color:#0F172A;">Мои поданные обращения (Контур сотрудника)</h3>
            </div>
            <span class="badge-status status-work">1 активно</span>
          </div>

          <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:var(--radius-sm); padding:14px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
              <div>
                <strong style="color:#00468C; font-size:13px;" id="portal-card-num">ВХ-2026/0942-КАНЦ</strong>
                <span style="font-size:11px; color:#64748B; margin-left:8px;" id="portal-card-tok">(Токен: TK-7842-KZ)</span>
              </div>
              <span class="badge-status status-work" id="portal-card-badge">В обработке</span>
            </div>
            <div style="font-size:12px; color:#334155; margin-bottom:8px;">
              <strong>Категория:</strong> <span id="portal-card-cat">Охрана труда и СИЗ (HSE-01)</span> • <em>ОДС Западная РДТ</em>
            </div>
            <div style="background:white; border:1px solid #E2E8F0; padding:10px; border-radius:6px; font-size:12px; color:#475569; margin-bottom:10px;" id="portal-card-text">
              «Срыв выдачи зимней обуви и утепленных курток выездным аварийным бригадам монтеров. Направлен запрос на центральный склад.»
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="font-size:11.5px; color:#059669; font-weight:700;" id="portal-card-sla">
                ⏱️ До ответа SLA: 4д 23ч 59м
              </div>
              <button class="btn-action-primary" style="padding:5px 12px; font-size:11.5px;" onclick="openTokenModal()">
                💬 Открыть чат дела
              </button>
            </div>
          </div>
        </div>

        <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 20px; box-shadow: var(--shadow-sm); display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; gap:12px; align-items:center; margin-bottom:12px;">
              <div style="font-size:28px;">🛡️</div>
              <div>
                <h4 style="font-size:13.5px; font-weight:800; color:#0F172A;">Гарантия анонимности и защиты</h4>
                <span style="font-size:11px; color:#64748B;">Трудовой кодекс РК (ст. 182, 108)</span>
              </div>
            </div>
            <p style="font-size:12px; color:#475569; line-height:1.5;">
              Политика АО «Казахтелеком» гарантирует нулевую терпимость к любому давлению или преследованию за конструктивную критику. 
              При выборе анонимного режима ваши персональные данные отсекаются криптографическим хэшем, а доступ к тикету осуществляется исключительно по личному токену.
            </p>
          </div>
          <div style="border-top:1px dashed #CBD5E1; padding-top:12px; margin-top:12px; display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11px; color:#059669; font-weight:700;">● CDN SSO шифрование активно</span>
            <button class="btn-action-secondary" style="font-size:11px; padding:4px 10px;" onclick="switchCanvasTab('tab-form')">
              Подать обращение →
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 2. WORKSPACE: AI INTAKE CHAT (Qwen 2.5 on-premise)                        -->
    <!-- ========================================================================= -->
    <section id="tab-chat" class="canvas-screen">
      <div class="chat-layout-wrapper">
        <div class="chat-header">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div class="ai-avatar-circle">ИИ</div>
            <div>
              <h2 style="font-size: 14.5px; font-weight: 800; color: #0F172A;">Интеллектуальный ассистент приема обращений</h2>
              <span style="font-size: 11px; color: var(--text-muted);">
                Локальная нейросеть On-Premise (Qwen 2.5) • Конфиденциальный контур АО «Казахтелеком»
              </span>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn-action-secondary" style="font-size: 12px; padding: 6px 12px;" onclick="resetChatFlow()">
              🔄 Начать заново
            </button>
          </div>
        </div>

        <div class="chat-stream-body" id="chat-stream-box">
          <!-- Welcome message from AI -->
          <div class="chat-msg-row ai">
            <div class="msg-avatar ai">ИИ</div>
            <div class="msg-content-wrapper">
              <div class="msg-bubble">
                Сәлеметсіз бе! Я корпоративный интеллектуальный ассистент АО «Казахтелеком». 
                Я готов выслушать вашу ситуацию, помочь квалифицировать нарушение по Трудовому кодексу РК и составить официальное заявление в Канцелярию со 100% защитой ваших прав.<br><br>
                <em>Вы можете свободно описать суть проблемы или выбрать готовый типовой сценарий ниже:</em>
              </div>
              <div id="quick-chips-container" style="margin-top: 10px; display:flex; flex-direction:column; gap:6px;">
                <div style="font-size:11px; font-weight:700; color:#64748B;">Типовые кейсы:</div>
                <div style="display:flex; flex-wrap:wrap; gap:6px;">
                  <button class="nav-tab-btn" style="background:#EBF3FA; color:#00468C; font-size:11px;" onclick="applyPreset('ppe')">
                    🥾 Срыв выдачи зимней обуви и курток монтерам (Атырау)
                  </button>
                  <button class="nav-tab-btn" style="background:#EBF3FA; color:#00468C; font-size:11px;" onclick="applyPreset('overtime')">
                    ⏱️ Принуждение к неоплачиваемым субботам (Семей)
                  </button>
                  <button class="nav-tab-btn" style="background:#EBF3FA; color:#00468C; font-size:11px;" onclick="applyPreset('mobbing')">
                    🛑 Давление и угрозы увольнением со стороны мастера
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Dynamic injections: 3-question survey, generated statement, registration stamp -->
          <div id="chat-dynamic-injections"></div>
        </div>

        <!-- Input Bar -->
        <div class="chat-input-bar">
          <input type="text" id="chat-text-input" class="form-control" placeholder="Опишите проблему своими словами или выберите сценарий выше..." onkeypress="handleChatEnter(event)">
          <button class="btn-action-primary" style="padding: 10px 20px;" onclick="sendChatProblem()">
            <span>Отправить</span> ➔
          </button>
        </div>
      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 3. WORKSPACE: PULSE SURVEY WIZARD (Q4) WITH SYNERGY TRIGGER               -->
    <!-- ========================================================================= -->
    <section id="tab-pulse" class="canvas-screen">
      <div style="max-width: 900px; margin: 0 auto; background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 28px;">
        
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #E2E8F0; padding-bottom:16px; margin-bottom:20px;">
          <div>
            <span class="badge-status status-work" style="margin-bottom:6px;">ЕЖЕКВАРТАЛЬНЫЙ СРЕЗ Q4 2026</span>
            <h2 style="font-size:20px; font-weight:800; color:#00468C;">Пульс-опрос климата и благополучия коллектива</h2>
            <p style="font-size:12.5px; color:var(--text-muted);">
              Омниканальный срез (Push / Outlook / Lotus Notes). Время прохождения: 60 секунд. Данные анонимизируются.
            </p>
          </div>
          <div style="text-align:right;">
            <div style="font-size:12px; color:#64748B;">Охват кампании:</div>
            <strong style="font-size:16px; color:#00468C;">68% (12 450 чел)</strong>
          </div>
        </div>

        <!-- BLOCK 1: СОЦИАЛЬНЫЙ КЛИМАТ -->
        <div class="pulse-block-card">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:18px;">🛠️</span>
            <h3 style="font-size:14.5px; font-weight:700; color:#0F172A;">Блок 1: Социальный климат и материально-техническое обеспечение</h3>
          </div>
          <p style="font-size:12.5px; color:#475569; margin-bottom:12px;">
            1. Довольны ли вы своевременностью выдачи спецодежды, СИЗ, качеством инструмента и состоянием рабочего автотранспорта?
          </p>
          <div class="pulse-scale-row">
            <button class="pulse-scale-btn" onclick="selectPulseScore('b1', 1, this)">1 • Крайне плохо</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b1', 2, this)">2 • Неудовлетворительно</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b1', 3, this)">3 • Средне</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b1', 4, this)">4 • Хорошо</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b1', 5, this)">5 • Отлично</button>
          </div>

          <!-- SYNERGY TRIGGER ALERT BANNER (APPEARS ON SCORE 1-2) -->
          <div class="synergy-appeal-prompt" id="synergy-alert-b1">
            <div style="display: flex; gap: 12px; align-items: flex-start;">
              <span style="font-size: 26px;">⚠️</span>
              <div>
                <strong style="color: #B91C1C; font-size: 13.5px;">Синергетическая связка: Вы зафиксировали критическую проблему</strong>
                <p style="font-size: 12px; color: #475569; margin: 4px 0 10px 0;">
                  В компании действует принцип <strong>Нулевой терпимости</strong> к невыдаче СИЗ и нарушениям безопасности. 
                  Хотите прямо сейчас конвертировать этот сигнал в официальное обращение в Канцелярию со 100% анонимностью?
                </p>
                <button class="btn-action-primary" style="background: #DC2626; font-size: 12px; padding: 6px 14px;" onclick="convertPulseToAppeal('HSE-01', 'Срыв обеспечения СИЗ и транспортом')">
                  🚨 Оформить как официальное обращение
                </button>
              </div>
            </div>
          </div>

          <div style="margin-top:16px;">
            <p style="font-size:12.5px; color:#475569; margin-bottom:8px;">
              2. Считаете ли вы справедливым начисление заработной платы и учет сверхурочных часов?
            </p>
            <div class="pulse-scale-row">
              <button class="pulse-scale-btn" onclick="selectPulseScore('b1_pay', 1, this)">1 • Несправедливо</button>
              <button class="pulse-scale-btn" onclick="selectPulseScore('b1_pay', 2, this)">2 • Скорее нет</button>
              <button class="pulse-scale-btn" onclick="selectPulseScore('b1_pay', 3, this)">3 • Нормально</button>
              <button class="pulse-scale-btn" onclick="selectPulseScore('b1_pay', 4, this)">4 • Справедливо</button>
              <button class="pulse-scale-btn" onclick="selectPulseScore('b1_pay', 5, this)">5 • Полностью</button>
            </div>
          </div>
        </div>

        <!-- BLOCK 2: ОТНОШЕНИЕ К КОМПАНИИ (eNPS) -->
        <div class="pulse-block-card">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:18px;">🏢</span>
            <h3 style="font-size:14.5px; font-weight:700; color:#0F172A;">Блок 2: Отношение сотрудника к компании (eNPS и лояльность)</h3>
          </div>
          <p style="font-size:12.5px; color:#475569; margin-bottom:12px;">
            3. «Я горжусь тем, что работаю в АО „Казахтелеком“, и готов рекомендовать компанию друзьям»:
          </p>
          <div class="pulse-scale-row">
            <button class="pulse-scale-btn" onclick="selectPulseScore('b2', 1, this)">1 • Точно нет</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b2', 2, this)">2 • Вряд ли</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b2', 3, this)">3 • Нейтрально</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b2', 4, this)">4 • Рекомендую</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b2', 5, this)">5 • Определенно да</button>
          </div>
        </div>

        <!-- BLOCK 3: АТМОСФЕРА В КОЛЛЕКТИВЕ -->
        <div class="pulse-block-card">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span style="font-size:18px;">🤝</span>
            <h3 style="font-size:14.5px; font-weight:700; color:#0F172A;">Блок 3: Психологическая безопасность и атмосфера</h3>
          </div>
          <p style="font-size:12.5px; color:#475569; margin-bottom:12px;">
            4. Чувствуете ли вы психологическую безопасность и уважение со стороны непосредственного руководителя (отсутствие моббинга и грубости)?
          </p>
          <div class="pulse-scale-row">
            <button class="pulse-scale-btn" onclick="selectPulseScore('b3', 1, this)">1 • Постоянное давление</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b3', 2, this)">2 • Бывают конфликты</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b3', 3, this)">3 • Приемлемо</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b3', 4, this)">4 • Уважительно</button>
            <button class="pulse-scale-btn" onclick="selectPulseScore('b3', 5, this)">5 • Полная поддержка</button>
          </div>
        </div>

        <!-- Submit Survey -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px;">
          <span style="font-size:12px; color:#64748B;">🔒 Ответы передаются в деперсонализированный аналитический пул</span>
          <button class="btn-action-primary" style="padding:10px 24px;" onclick="finishPulseSurvey()">
            ✅ Завершить пульс-опрос
          </button>
        </div>

      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 4. WORKSPACE: SELF-SERVICE DIRECT APPEAL FORM                             -->
    <!-- ========================================================================= -->
    <section id="tab-form" class="canvas-screen">
      <div style="max-width: 900px; margin: 0 auto; background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 28px;">
        
        <div style="border-bottom: 2px solid #E2E8F0; padding-bottom: 14px; margin-bottom: 20px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <h2 style="font-size: 18px; font-weight: 800; color: #00468C;">Самостоятельное заведение официального обращения (Self-service Form)</h2>
            <p style="font-size: 12.5px; color: var(--text-muted);">
              Прямой структурированный ввод заявления без чат-бота с автоматической регистрацией в Канцелярии
            </p>
          </div>
          <span class="badge-status status-closed">Форма-бланк</span>
        </div>

        <form id="direct-appeal-form" onsubmit="event.preventDefault(); submitDirectForm();">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div class="form-group">
              <label class="form-label">Дивизион / Подразделение компании:</label>
              <select class="form-control" id="form-div">
                <option value="ОДС">ОДС — Объединенный дивизион «Сеть»</option>
                <option value="СФ">СФ — Сервисная фабрика</option>
                <option value="ДРБ">ДРБ — Дивизион розничного бизнеса</option>
                <option value="ДКБ">ДКБ — Дивизион корпоративного бизнеса</option>
                <option value="ДТК">ДТК — Дивизион телекоммуникационных сетей</option>
                <option value="КУ">КУ — Корпоративное управление</option>
                <option value="ДУП">ДУП — Департамент управления персоналом</option>
                <option value="ДПБ">ДПБ — Департамент производственной безопасности</option>
                <option value="ДЦБ">ДЦБ — Дивизион цифрового бизнеса</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Регион Казахстана (20 регионов):</label>
              <select class="form-control" id="form-region">
                <option value="Атырауская область">Атырауская область (Западная РДТ)</option>
                <option value="Мангистауская область">Мангистауская область (Западная РДТ)</option>
                <option value="Актюбинская область">Актюбинская область (Западная РДТ)</option>
                <option value="ЗКО">Западно-Казахстанская область (Уральск)</option>
                <option value="Область Абай">Область Абай (г. Семей)</option>
                <option value="ВКО">Восточно-Казахстанская область</option>
                <option value="Карагандинская область">Карагандинская область</option>
                <option value="Область Ұлытау">Область Ұлытау (г. Жезказган)</option>
                <option value="Павлодарская область">Павлодарская область</option>
                <option value="Костанайская область">Костанайская область</option>
                <option value="СКО">Северо-Казахстанская область (Петропавловск)</option>
                <option value="Акмолинская область">Акмолинская область</option>
                <option value="г. Астана">г. Астана (Центральный аппарат)</option>
                <option value="г. Алматы">г. Алматы</option>
                <option value="г. Шымкент">г. Шымкент</option>
                <option value="Жамбылская область">Жамбылская область (г. Тараз)</option>
                <option value="Туркестанская область">Туркестанская область</option>
                <option value="Кызылординская область">Кызылординская область</option>
                <option value="Алматинская область">Алматинская область (г. Конаев)</option>
                <option value="Область Жетісу">Область Жетісу (г. Талдыкорган)</option>
              </select>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div class="form-group">
              <label class="form-label">Категория инцидента:</label>
              <select class="form-control" id="form-category">
                <option value="HSE-01">HSE-01 • Охрана труда, спецодежда и СИЗ</option>
                <option value="PAY-02">PAY-02 • Оплата труда, оклады и премии</option>
                <option value="OT-03">OT-03 • Сверхурочные работы (ст. 108 ТК РК)</option>
                <option value="MOB-04">MOB-04 • Моббинг, давление и служебная этика</option>
                <option value="EMG-05">EMG-05 • Угроза забастовки / Коллективный спор</option>
                <option value="TECH-06">TECH-06 • Материально-техническое снабжение и автотранспорт</option>
                <option value="LIFE-07">LIFE-07 • Санитарно-бытовые условия на узлах связи</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Режим конфиденциальности:</label>
              <select class="form-control" id="form-anon">
                <option value="anon">🔒 Анонимно (выдать секретный токен доступа TK-XXXX-KZ)</option>
                <option value="official">👤 Официально (от своего имени: Ахметов Д.Б.)</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Суть инцидента и обстоятельства:</label>
            <textarea class="form-control" id="form-text" rows="4" placeholder="Подробно опишите факты: что произошло, даты, кто из руководителей был в курсе, какие требования необходимо выполнить..."></textarea>
          </div>

          <!-- File Upload Simulation -->
          <div class="form-group">
            <label class="form-label">Прикрепить подтверждающие материалы (фото дефектных СИЗ, табели, акты):</label>
            <div style="border: 2px dashed #CBD5E1; border-radius: var(--radius-sm); padding: 18px; text-align: center; background: #F8FAFC; cursor: pointer;" onclick="simulateFileUpload()">
              <span style="font-size: 24px;">📎</span>
              <div style="font-size: 13px; font-weight: 700; color: #00468C; margin-top: 4px;" id="file-drop-label">Нажмите для выбора файла или перетащите сюда</div>
              <span style="font-size: 11px; color: #64748B;">Поддерживаются: JPG, PNG, PDF, XLSX (до 25 МБ)</span>
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #E2E8F0; padding-top: 16px; margin-top: 20px;">
            <div style="font-size: 11.5px; color: #64748B;">
              🛡️ Защита от конфликта интересов: начальник участка не получит доступ к рассмотрению
            </div>
            <button type="submit" class="btn-action-primary" style="padding: 10px 24px;">
              🏛️ Зарегистрировать в Канцелярии
            </button>
          </div>
        </form>

      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 5. WORKSPACE: EX-SERVICE STUDIO & EXTERNAL DATA INGESTION                 -->
    <!-- ========================================================================= -->
    <section id="tab-ex-service" class="canvas-screen">
      <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 24px; margin-bottom: 24px;">
        
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #E2E8F0; padding-bottom:14px; margin-bottom:20px;">
          <div>
            <h2 style="font-size:18px; font-weight:800; color:#00468C;">Студия управления опытом работника (EX Management Studio)</h2>
            <p style="font-size:12px; color:var(--text-muted);">
              Центр социального партнерства и мониторинга (МСЦ) • Департамент управления персоналом (ДУП)
            </p>
          </div>
          <span style="background:#0284C7; color:white; font-size:11.5px; font-weight:700; padding:4px 10px; border-radius:4px;">
            ROLE_EX_SERVICE
          </span>
        </div>

        <!-- EX Metrics Header Cards -->
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; margin-bottom:24px;">
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:var(--radius-md); padding:16px;">
            <div style="font-size:12px; color:#64748B;">Индекс стабильности (SRS)</div>
            <div style="font-size:24px; font-weight:800; color:#00468C; margin:4px 0;">64%</div>
            <span style="font-size:11px; color:#10B981;">▲ +2.4% к прошлому кварталу</span>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:var(--radius-md); padding:16px;">
            <div style="font-size:12px; color:#64748B;">Индекс лояльности (eNPS)</div>
            <div style="font-size:24px; font-weight:800; color:#0284C7; margin:4px 0;">+24</div>
            <span style="font-size:11px; color:#10B981;">В зоне роста</span>
          </div>
          <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:var(--radius-md); padding:16px;">
            <div style="font-size:12px; color:#991B1B;">Индекс благополучия (ИСБ)</div>
            <div style="font-size:24px; font-weight:800; color:#DC2626; margin:4px 0;">34%</div>
            <span style="font-size:11px; color:#DC2626;">⚠️ Зона высокого напряжения</span>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:var(--radius-md); padding:16px;">
            <div style="font-size:12px; color:#64748B;">Охват пульс-опросов</div>
            <div style="font-size:24px; font-weight:800; color:#0F172A; margin:4px 0;">68%</div>
            <span style="font-size:11px; color:#64748B;">12 450 из 18 300 работников</span>
          </div>
        </div>

        <!-- Section 1: Survey Campaign Management -->
        <div style="margin-bottom:28px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h3 style="font-size:15px; font-weight:700; color:#0F172A;">📊 Регламентные кампании пульс-опросов (Q1–Q4)</h3>
            <button class="btn-action-primary" style="font-size:12px; padding:6px 14px;" onclick="showToast('Создание новой кампании Q1 2027...')">
              ➕ Создать кампанию
            </button>
          </div>

          <table class="appeals-table" style="background:#FFFFFF; border:1px solid var(--border); border-radius:var(--radius-sm); overflow:hidden;">
            <thead>
              <tr>
                <th>Кампания</th>
                <th>Период</th>
                <th>Каналы уведомлений</th>
                <th>Целевые дивизионы</th>
                <th>Охват</th>
                <th>Индекс климата</th>
                <th>Статус</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Пульс-опрос Q4 2026</strong></td>
                <td>Ноябрь – Декабрь 2026</td>
                <td><span style="font-size:11px; color:#00468C;">Push, SMS, Outlook, Lotus Notes</span></td>
                <td>Все филиалы (ОДС, СФ, ДРБ)</td>
                <td><strong>68% (12 450)</strong></td>
                <td><strong style="color:#D97706;">71.4%</strong></td>
                <td><span class="badge-status status-work">● АКТИВЕН</span></td>
                <td><button class="btn-action-secondary" style="padding:3px 8px; font-size:11px;" onclick="showToast('Рассылка досыла напоминаний запущена')">📢 Напомнить</button></td>
              </tr>
              <tr>
                <td><strong>Пульс-опрос Q3 2026</strong></td>
                <td>Сентябрь 2026</td>
                <td>Push, Outlook</td>
                <td>Все филиалы</td>
                <td>82% (14 950)</td>
                <td>73.8%</td>
                <td><span class="badge-status status-closed">Завершен</span></td>
                <td><button class="btn-action-secondary" style="padding:3px 8px; font-size:11px;" onclick="showToast('Архивный отчет выгружен')">📄 Отчет</button></td>
              </tr>
              <tr>
                <td><strong>Пульс-опрос Q2 2026</strong></td>
                <td>Июнь 2026</td>
                <td>Push, Outlook</td>
                <td>Все филиалы</td>
                <td>81% (15 120)</td>
                <td>74.2%</td>
                <td><span class="badge-status status-closed">Завершен</span></td>
                <td><button class="btn-action-secondary" style="padding:3px 8px; font-size:11px;" onclick="showToast('Архивный отчет выгружен')">📄 Отчет</button></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Section 2: EXTERNAL DATA INGESTION HUB -->
        <div style="background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%); border: 1.5px solid #CBD5E1; border-radius: var(--radius-md); padding: 20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #E2E8F0; padding-bottom:10px;">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="font-size:22px;">📥</span>
              <div>
                <h3 style="font-size:15px; font-weight:800; color:#00468C;">Хаб импорта внешних данных (External Data Ingestion Hub)</h3>
                <span style="font-size:11px; color:#64748B;">Загрузка внешних CSV/XLSX: аудит зарплат, текучесть кадров, независимые опросы для корреляции с климатом</span>
              </div>
            </div>
            <button class="btn-action-primary" style="background:#0284C7; font-size:12px; padding:6px 14px;" onclick="loadSampleCsvData()">
              📥 Загрузить эталонный CSV (Текучесть и зарплаты)
            </button>
          </div>

          <!-- Drag and Drop Box -->
          <div style="border: 2px dashed #94A3B8; border-radius: var(--radius-sm); padding: 20px; text-align: center; background: white; margin-bottom: 16px;">
            <input type="file" id="csv-file-input" accept=".csv,.xlsx,.txt" style="display:none;" onchange="handleCsvFile(event)">
            <button class="btn-action-secondary" onclick="document.getElementById('csv-file-input').click()">
              📂 Выбрать CSV-файл на диске
            </button>
            <div style="font-size:12px; color:#64748B; margin-top:6px;">
              или перетащите файл сюда. Система автоматически определит разделители и кодировку UTF-8 / Windows-1251.
            </div>
          </div>

          <!-- Parsed Data Preview Table -->
          <div id="external-data-preview-box" style="display:none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <strong style="font-size:12.5px; color:#0F172A;" id="external-table-title">Загруженные данные:</strong>
              <span class="badge-status status-success" id="external-rows-count">10 строк распознано</span>
            </div>
            
            <div style="max-height: 220px; overflow-y: auto; border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 14px;">
              <table class="appeals-table" id="external-csv-table">
                <!-- Dynamically populated -->
              </table>
            </div>

            <!-- Column Mapping & Correlation Controls -->
            <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:var(--radius-sm); padding:14px; display:flex; justify-content:space-between; align-items:center;">
              <div>
                <strong style="font-size:12.5px; color:#1E40AF;">Синхронизация с аналитической моделью Qwen 2.5:</strong>
                <p style="font-size:11.5px; color:#3B82F6; margin-top:2px;">
                  Объединить внешнюю текучесть кадров и рыночные оклады с внутренней тепловой картой обращений
                </p>
              </div>
              <button class="btn-action-primary" style="background:#1D4ED8; font-size:12px;" onclick="executeDataCorrelationMerge()">
                ⚡ Объединить с аналитикой климата
              </button>
            </div>

            <!-- Correlation Result Banner -->
            <div id="correlation-result-box" style="display:none; margin-top:14px; background:#F0FDF4; border:1.5px solid #10B981; border-radius:var(--radius-sm); padding:14px;">
              <strong style="color:#065F46; font-size:13px;">✅ Корреляционный анализ успешно завершен:</strong>
              <p style="font-size:12px; color:#1E293B; margin-top:4px; line-height:1.5;">
                Выявлена прямая высокая корреляция (<strong>r = 0.89</strong>) между уровнем внешней текучести монтеров в Западной РДТ (<strong>18.4%</strong>) и критическим индексом риска забастовки (<strong>8.8 / 10</strong>). 
                Панель руководства обновлена сводным сравнительным графиком.
              </p>
            </div>

          </div>

        </div>

      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 6. WORKSPACE: CHANCELLERY REGISTRY & SLA CONTROL                          -->
    <!-- ========================================================================= -->
    <section id="tab-chancellery" class="canvas-screen">
      <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); overflow: hidden;">
        
        <div style="background: #00468C; color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 12px; align-items: center;">
            <span style="font-size: 22px;">📋</span>
            <div>
              <h2 style="font-size: 15.5px; font-weight: 800;">Реестр входящих обращений Канцелярии и контроль регламентных сроков (SLA)</h2>
              <span style="font-size: 11px; color: #BAE6FD;">Официальный контур СЭД • Lotus Notes Domino Bridge • Защита от конфликта интересов (Conflict Guard)</span>
            </div>
          </div>
          <div style="display:flex; gap:10px;">
            <button class="btn-action-primary" style="background: rgba(255,255,255,0.2); font-size: 12px;" onclick="openTokenModal()">
              🔍 Поиск по токену
            </button>
            <button class="btn-action-primary" style="background: #10B981; font-size: 12px;" onclick="switchCanvasTab('tab-form')">
              ➕ Новое обращение
            </button>
          </div>
        </div>

        <!-- System Integration Banner -->
        <div style="background:#F1F5F9; border-bottom:1px solid #E2E8F0; padding:8px 24px; display:flex; justify-content:space-between; align-items:center; font-size:11.5px; color:#475569;">
          <div style="display:flex; gap:16px;">
            <span>🟢 <strong>СЭД Lotus Notes:</strong> Шлюз синхронизирован</span>
            <span>🛡️ <strong>Conflict Guard:</strong> Активен для всех 20 регионов</span>
            <span>⏱️ <strong>Регламент SLA:</strong> 5 дней стандарт / 24-48ч критические</span>
          </div>
          <div>
            Серверное время: <span style="font-family:monospace; font-weight:700;" id="chancellery-clock">10.11.2026 18:05:40</span>
          </div>
        </div>

        <!-- Master Table of Appeals -->
        <div style="padding: 20px; overflow-x: auto;">
          <table class="appeals-table" id="chancellery-main-table">
            <thead>
              <tr>
                <th>Вх. номер / Токен</th>
                <th>Дата регистрации</th>
                <th>Режим заявителя</th>
                <th>Дивизион / Регион</th>
                <th>Категория / Фабула</th>
                <th>Первый получатель & Conflict Guard</th>
                <th>Статус</th>
                <th>Живой контроль SLA</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody id="master-chancellery-tbody">
              <!-- Dynamically populated from window.platformState.appeals -->
            </tbody>
          </table>
        </div>

      </div>
    </section>

    <!-- ========================================================================= -->
    <!-- 7. WORKSPACE: LEADERSHIP & KAZAKHSTAN 20-REGION HEATMAP                   -->
    <!-- ========================================================================= -->
    <section id="tab-executive" class="canvas-screen">
      <div style="background: white; border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 24px;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #E2E8F0; padding-bottom: 14px; margin-bottom: 20px;">
          <div>
            <h2 style="font-size: 18px; font-weight: 800; color: #00468C;">Панель руководства: Предиктивная аналитика и тепловая карта рисков</h2>
            <p style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
              Синтез результатов квартального пульс-опроса Q4 и массива обращений Канцелярии (Qwen 2.5 On-Premise)
            </p>
          </div>
          <div style="display:flex; gap:10px;">
            <button class="btn-action-secondary" style="font-size:12px;" onclick="window.print()">
              🖨️ Печать сводки
            </button>
            <span style="background: #00468C; color: white; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 4px;">
              ROLE_EXECUTIVE (Правление)
            </span>
          </div>
        </div>

        <!-- Executive Narrative AI Summary -->
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
            <strong>3. Дисциплина исполнения (SLA):</strong> 87.4% обращений закрываются в нормативный 5-дневный срок. Среднее время первого ответа сократилось до <strong>3.7 дней</strong>.
          </div>
        </div>

        <!-- KAZAKHSTAN 20-REGION INTERACTIVE HEATMAP -->
        <div style="margin-bottom: 24px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <h3 style="font-size: 15px; font-weight: 800; color: #0F172A;">🗺️ Интерактивная тепловая карта 20 регионов Казахстана</h3>
              <p style="font-size: 12px; color: var(--text-muted);">
                Нажмите на любой регион для просмотра детального паспорта напряженности и открытых инцидентов
              </p>
            </div>
            <div style="display:flex; gap:12px; font-size:11px;">
              <span style="display:flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; background:#EF4444; border-radius:2px;"></span> Критический (&gt;7.5)</span>
              <span style="display:flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; background:#F59E0B; border-radius:2px;"></span> Высокий (6.0-7.5)</span>
              <span style="display:flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; background:#3B82F6; border-radius:2px;"></span> Средний (4.0-6.0)</span>
              <span style="display:flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; background:#10B981; border-radius:2px;"></span> Низкий (&lt;4.0)</span>
            </div>
          </div>

          <div class="heatmap-grid" id="heatmap-grid-container">
            <!-- 20 Kazakhstan Region Cards dynamically generated -->
          </div>
        </div>

        <!-- Charts Grid -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px;">
            <h4 style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 10px;">Структура обращений по 7 категориям инцидентов</h4>
            <div style="height: 250px;">
              <canvas id="chartExecCategories"></canvas>
            </div>
          </div>

          <div style="background: #F8FAFC; border: 1px solid var(--border); border-radius: var(--radius-md); padding: 16px;">
            <h4 style="font-size: 13px; font-weight: 700; color: #0F172A; margin-bottom: 10px;">Соблюдение нормативов SLA филиалами (%)</h4>
            <div style="height: 250px;">
              <canvas id="chartExecSLA"></canvas>
            </div>
          </div>
        </div>

      </div>
    </section>

  </main>

  <!-- ========================================================================= -->
  <!-- MODAL 1: CDN WELLNESS CHECK-IN (NUDGE MODAL)                              -->
  <!-- ========================================================================= -->
  <div id="modal-nudge" class="modal-backdrop-nudge" onclick="closeNudgeModal()">
    <div class="nudge-modal-card" onclick="event.stopPropagation()">
      <div class="nudge-header">
        <div class="nudge-avatar-pulse">👋</div>
        <div>
          <h3 style="font-size: 16px; font-weight: 800;">Сәлеметсіз бе, Данияр Бауыржанұлы!</h3>
          <span style="font-size: 12px; color: #BAE6FD;">Авторизация CDN • ОДС Западная РДТ • г. Атырау</span>
        </div>
      </div>

      <div style="background: #F8FAFC; border-bottom: 1px solid #E2E8F0; padding: 16px 24px; font-size: 13.5px; line-height: 1.5; color: #1E293B;">
        Все ли у вас в порядке на рабочем месте? Есть ли сложности, нерешенные вопросы или проблемы в коллективе? Хотите ли вы поговорить об этом или поделиться обратной связью?
      </div>

      <div class="nudge-options-list">
        <div class="nudge-option-btn" onclick="nudgeAction('chat')">
          <span style="font-size: 24px;">💬</span>
          <div>
            <strong style="color: #00468C; font-size: 13px;">Да, есть проблема — поговорить с ИИ-агентом</strong>
            <div style="font-size: 11px; color: #64748B;">ИИ выслушает, задаст 3 вопроса и оформит официальное заявление</div>
          </div>
        </div>

        <div class="nudge-option-btn" onclick="nudgeAction('pulse')">
          <span style="font-size: 24px;">📊</span>
          <div>
            <strong style="color: #6366F1; font-size: 13px;">Пройти квартальный пульс-опрос Q4 (60 секунд)</strong>
            <div style="font-size: 11px; color: #64748B;">Экспресс-оценка климата, отношения к компании и атмосферы в коллективе</div>
          </div>
        </div>

        <div class="nudge-option-btn" onclick="nudgeAction('form')">
          <span style="font-size: 24px;">📝</span>
          <div>
            <strong style="color: #0284C7; font-size: 13px;">Заполнить официальное обращение вручную</strong>
            <div style="font-size: 11px; color: #64748B;">Прямой структурированный ввод заявления без чат-бота</div>
          </div>
        </div>

        <div class="nudge-option-btn" onclick="nudgeAction('ok')">
          <span style="font-size: 24px;">👍</span>
          <div>
            <strong style="color: #10B981; font-size: 13px;">Все отлично, спасибо!</strong>
            <div style="font-size: 11px; color: #64748B;">У меня нет проблем, закрыть окно и продолжить работу</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL 2: TOKEN TRACKER & TWO-WAY SAFE CHAT                                -->
  <!-- ========================================================================= -->
  <div id="modal-token-tracker" class="modal-backdrop-nudge" onclick="closeTokenModal()">
    <div class="nudge-modal-card" style="width:680px;" onclick="event.stopPropagation()">
      <div style="background:#00468C; color:white; padding:16px 24px; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="font-size: 15px; font-weight: 800;">🔍 Проверка статуса обращения и безопасный чат по токену</h3>
        <button style="border: none; background: transparent; color:white; font-size: 18px; cursor: pointer;" onclick="closeTokenModal()">✕</button>
      </div>

      <div style="padding: 20px 24px;">
        <div style="display: flex; gap: 8px; margin-bottom: 16px;">
          <input type="text" id="token-search-input" class="form-control" value="TK-7842-KZ" style="font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 14px;">
          <button class="btn-action-primary" onclick="lookupToken()">Найти</button>
        </div>

        <div id="token-card-result" style="background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: var(--radius-md); padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: #00468C; font-size:14px;" id="token-res-num">ВХ-2026/0942-КАНЦ</strong>
            <span class="badge-status status-work">В работе у исполнителя</span>
          </div>
          <div style="font-size: 12px; color: #64748B; margin-bottom: 10px;">
            Категория: <strong style="color:#0F172A;" id="token-res-cat">Охрана труда и СИЗ (HSE-01)</strong><br>
            Первый получатель: <strong style="color:#0F172A;">Департамент производственной безопасности (Смагулов Б.К.)</strong><br>
            🛡️ <em>Conflict Guard: мастер участка аппаратно исключен из рассмотрения дела.</em>
          </div>

          <!-- Two-Way Safe Message Thread -->
          <div style="border-top:1px solid #E2E8F0; padding-top:10px; margin-top:10px;">
            <div style="font-size:12px; font-weight:700; color:#334155; margin-bottom:6px;">Защищенная переписка с исполнителем:</div>
            <div id="token-chat-stream" style="max-height:140px; overflow-y:auto; background:white; border:1px solid #E2E8F0; border-radius:6px; padding:10px; font-size:12px; margin-bottom:10px; display:flex; flex-direction:column; gap:8px;">
              <div style="background:#F1F5F9; padding:8px 10px; border-radius:6px;">
                <strong>Исполнитель (Смагулов Б.К., 17:40):</strong> «Обращение принято в работу. Направлен срочный запрос на центральный склад в г. Астана для перераспределения 18 комплектов утепленной обуви.»
              </div>
            </div>
            
            <div style="display:flex; gap:8px;">
              <input type="text" id="token-reply-input" class="form-control" style="font-size:12px;" placeholder="Отправить дополнительное уточнение исполнителю...">
              <button class="btn-action-primary" style="padding:6px 14px; font-size:12px;" onclick="sendTokenReply()">Отправить</button>
            </div>
          </div>

          <div style="margin-top: 12px; font-size: 12px; color: #059669; font-weight: 700;" id="token-res-sla">
            ⏱️ Контрольный срок SLA: 4 дня 23 часа
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL 3: CHANCELLERY OFFICIAL REGISTRATION STAMP                          -->
  <!-- ========================================================================= -->
  <div id="modal-chancellery-stamp" class="modal-backdrop-nudge" onclick="closeStampModal()">
    <div class="nudge-modal-card" style="width:540px;" onclick="event.stopPropagation()">
      <div style="background:#00468C; color:white; padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="font-size:15px; font-weight:800;">🏛️ Регистрационный штамп Канцелярии</h3>
        <button style="border:none; background:transparent; color:white; font-size:18px; cursor:pointer;" onclick="closeStampModal()">✕</button>
      </div>

      <div style="padding:24px; text-align:center;">
        <div class="chancellery-official-stamp" id="stamp-content-box">
          <div class="stamp-header">АО «ҚАЗАҚТЕЛЕКОМ» • КАНЦЕЛЯРИЯ СЭД</div>
          <div class="stamp-row">
            <span>Входящий номер:</span>
            <strong id="stamp-modal-num">ВХ-2026/0942-КАНЦ</strong>
          </div>
          <div class="stamp-row">
            <span>Дата и время:</span>
            <strong id="stamp-modal-date">10.11.2026 18:05:40</strong>
          </div>
          <div class="stamp-row">
            <span>СЭД Lotus Notes ID:</span>
            <strong>#DOMINO-LN-89214</strong>
          </div>
          <div class="stamp-row">
            <span>Исполнитель:</span>
            <strong id="stamp-modal-recip">Департамент охраны труда</strong>
          </div>
          <div class="stamp-row">
            <span>Контрольный срок SLA:</span>
            <strong style="color:#059669;" id="stamp-modal-sla">15.11.2026 (5 дней)</strong>
          </div>
          <div style="border-top:1px solid #00468C; margin-top:6px; padding-top:4px; font-size:10px; color:#64748B;">
            ЭЦП: ПОДПИСАНО КОРПОРАТИВНОЙ ЭЦП КАНЦЕЛЯРИИ ЦОД
          </div>
        </div>

        <div style="margin-top:20px; display:flex; justify-content:center; gap:10px;">
          <button class="btn-action-primary" onclick="showToast('Штамп скопирован в буфер СЭД Lotus Notes'); closeStampModal();">
            📋 Копировать метаданные
          </button>
          <button class="btn-action-secondary" onclick="window.print()">
            🖨️ Распечатать штамп
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL 4: REGION INSPECTOR (HEATMAP DRILL-DOWN)                            -->
  <!-- ========================================================================= -->
  <div id="modal-region-inspector" class="modal-backdrop-nudge" onclick="closeRegionModal()">
    <div class="nudge-modal-card" style="width:620px;" onclick="event.stopPropagation()">
      <div style="background:#00468C; color:white; padding:16px 20px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h3 style="font-size:15px; font-weight:800;" id="region-modal-title">Атырауская область (Западная РДТ)</h3>
          <span style="font-size:11px; color:#BAE6FD;">Паспорт социального климата и напряженности</span>
        </div>
        <button style="border:none; background:transparent; color:white; font-size:18px; cursor:pointer;" onclick="closeRegionModal()">✕</button>
      </div>

      <div style="padding:20px 24px;" id="region-modal-body">
        <!-- Dynamically rendered -->
      </div>
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div class="toast-container" id="toast-box"></div>

  <!-- ========================================================================= -->
  <!-- JAVASCRIPT LOGIC & REACTIVE STATE                                         -->
  <!-- ========================================================================= -->
  <script>
    // -------------------------------------------------------------
    // 1. UNIFIED REACTIVE STATE (window.platformState)
    // -------------------------------------------------------------
    window.platformState = {
      currentUser: {
        id: "USR-0942",
        name: "Ахметов Данияр Бауыржанұлы",
        role: "ROLE_EMPLOYEE",
        jobTitle: "Электромонтер 5 разряда",
        division: "ОДС",
        region: "Атырауская область",
        avatar: "ДБ",
        isCdnAuth: true
      },
      roles: {
        ROLE_EMPLOYEE: {
          id: "ROLE_EMPLOYEE",
          title: "Обычный сотрудник",
          subtitle: "Портал работника • CDN чекин • Подача обращений",
          primaryTab: "tab-portal",
          userLabel: "Ахметов Д.Б. (ОДС Запад)"
        },
        ROLE_EX_SERVICE: {
          id: "ROLE_EX_SERVICE",
          title: "Служба управления опытом (EX / ДУП)",
          subtitle: "Кампании пульс-опросов • Триаж • Внешние данные CSV",
          primaryTab: "tab-ex-service",
          userLabel: "Касенова А.М. (ДУП / EX)"
        },
        ROLE_CHANCELLERY: {
          id: "ROLE_CHANCELLERY",
          title: "Канцелярия / СЭД (Lotus Notes)",
          subtitle: "Официальная регистрация • Штамп • Контроль SLA",
          primaryTab: "tab-chancellery",
          userLabel: "Жумабаева Г.С. (Канцелярия ЦА)"
        },
        ROLE_EXECUTIVE: {
          id: "ROLE_EXECUTIVE",
          title: "Руководство / Правление",
          subtitle: "Executive AI Report • Карта 20 регионов • Риск забастовок",
          primaryTab: "tab-executive",
          userLabel: "Есекеев К.Б. (Правление)"
        }
      },
      appeals: [
        {
          id: 1,
          regNumber: "ВХ-2026/0942-КАНЦ",
          token: "TK-7842-KZ",
          isAnonymous: true,
          applicantName: "Анонимный заявитель",
          division: "ОДС",
          region: "Атырауская область",
          categoryCode: "HSE-01",
          categoryTitle: "Охрана труда и СИЗ",
          rawText: "Срыв выдачи зимней обуви и утепленных курток выездным бригадам. На складе задержка уже 2 месяца, монтеры работают в мороз.",
          recipientDept: "Департамент производственной безопасности (Смагулов Б.К.)",
          status: "IN_WORK",
          slaTotalSeconds: 5 * 24 * 3600,
          slaRemainingSeconds: 5 * 24 * 3600 - 45,
          conflictGuardActive: true,
          regDate: "10.11.2026 18:05"
        },
        {
          id: 2,
          regNumber: "ВХ-2026/0941-КАНЦ",
          token: "TK-8812-KZ",
          isAnonymous: true,
          applicantName: "Анонимный заявитель",
          division: "ОДС",
          region: "Область Абай",
          categoryCode: "PAY-02",
          categoryTitle: "Оплата труда и сверхурочные",
          rawText: "Принуждение к выходу в субботу без табелирования и двойной оплаты (ст. 108 ТК РК).",
          recipientDept: "Департамент оплаты труда (Ким А.В.)",
          status: "IN_WORK",
          slaTotalSeconds: 5 * 24 * 3600,
          slaRemainingSeconds: 1 * 24 * 3600 + 4 * 3600,
          conflictGuardActive: false,
          regDate: "08.11.2026 14:20"
        },
        {
          id: 3,
          regNumber: "ВХ-2026/0938-КАНЦ",
          token: "TK-5519-KZ",
          isAnonymous: false,
          applicantName: "Искаков М.А.",
          division: "ОДС",
          region: "СКО",
          categoryCode: "TECH-06",
          categoryTitle: "Инфраструктура и связь",
          rawText: "Поломка аварийного дизель-генератора на магистральном узле связи, отсутствие ЗИП.",
          recipientDept: "Дивизион «Сеть» (ОДС)",
          status: "ESCALATED",
          slaTotalSeconds: 5 * 24 * 3600,
          slaRemainingSeconds: -14400, // overdue by 4h
          conflictGuardActive: false,
          regDate: "04.11.2026 09:15"
        },
        {
          id: 4,
          regNumber: "ВХ-2026/0935-КАНЦ",
          token: "TK-9021-KZ",
          isAnonymous: true,
          applicantName: "Анонимный заявитель",
          division: "СФ",
          region: "г. Алматы",
          categoryCode: "MOB-04",
          categoryTitle: "Моббинг и служебная этика",
          rawText: "Систематическое давление и грубость со стороны начальника участка, угрозы увольнением.",
          recipientDept: "Служба комплаенс и Омбудсмен (Утепов Т.С.)",
          status: "RESOLVED",
          slaTotalSeconds: 5 * 24 * 3600,
          slaRemainingSeconds: 2 * 24 * 3600,
          conflictGuardActive: true,
          regDate: "02.11.2026 11:30"
        },
        {
          id: 5,
          regNumber: "ВХ-2026/0930-КАНЦ",
          token: "TK-3412-KZ",
          isAnonymous: false,
          applicantName: "Сагындыков Е.К.",
          division: "ДРБ",
          region: "Мангистауская область",
          categoryCode: "HSE-01",
          categoryTitle: "Транспорт и безопасность",
          rawText: "Критический износ служебного автотранспорта УАЗ аварийных бригад, лысая резина.",
          recipientDept: "Департамент логистики и транспорта",
          status: "IN_WORK",
          slaTotalSeconds: 5 * 24 * 3600,
          slaRemainingSeconds: 2 * 24 * 3600 + 18 * 3600,
          conflictGuardActive: false,
          regDate: "01.11.2026 16:40"
        }
      ],
      regions20: [
        { name: "Атырауская область", rdt: "Западная РДТ", riskScore: 8.8, riskLevel: "critical", appealsCount: 69, mainCat: "HSE-01 СИЗ", enps: -14 },
        { name: "Мангистауская область", rdt: "Западная РДТ", riskScore: 7.9, riskLevel: "high", appealsCount: 48, mainCat: "HSE-01 Транспорт", enps: -8 },
        { name: "Область Абай", rdt: "Восточная РДТ", riskScore: 7.4, riskLevel: "high", appealsCount: 34, mainCat: "PAY-02 Переработки", enps: +4 },
        { name: "Область Ұлытау", rdt: "Центральная РДТ", riskScore: 6.8, riskLevel: "high", appealsCount: 15, mainCat: "LIFE-07 Быт", enps: +10 },
        { name: "Кызылординская область", rdt: "Южная РДТ", riskScore: 6.4, riskLevel: "high", appealsCount: 19, mainCat: "PAY-02 Оклады", enps: +12 },
        { name: "ЗКО (Уральск)", rdt: "Западная РДТ", riskScore: 6.2, riskLevel: "high", appealsCount: 21, mainCat: "HSE-01 СИЗ", enps: +15 },
        { name: "Туркестанская область", rdt: "Южная РДТ", riskScore: 5.9, riskLevel: "moderate", appealsCount: 22, mainCat: "MOB-04 Этика", enps: +18 },
        { name: "Актюбинская область", rdt: "Западная РДТ", riskScore: 5.8, riskLevel: "moderate", appealsCount: 24, mainCat: "TECH-06 ЗИП", enps: +19 },
        { name: "Карагандинская область", rdt: "Центральная РДТ", riskScore: 5.5, riskLevel: "moderate", appealsCount: 19, mainCat: "PAY-02 Переработки", enps: +20 },
        { name: "Жамбылская область", rdt: "Южная РДТ", riskScore: 5.4, riskLevel: "moderate", appealsCount: 17, mainCat: "LIFE-07 Обогрев", enps: +22 },
        { name: "г. Шымкент", rdt: "Городской филиал", riskScore: 5.1, riskLevel: "moderate", appealsCount: 18, mainCat: "PAY-02 Премии", enps: +25 },
        { name: "ВКО", rdt: "Восточная РДТ", riskScore: 4.9, riskLevel: "moderate", appealsCount: 16, mainCat: "TECH-06 Связь", enps: +26 },
        { name: "г. Алматы", rdt: "Городской филиал", riskScore: 4.6, riskLevel: "moderate", appealsCount: 27, mainCat: "MOB-04 Этика", enps: +28 },
        { name: "СКО", rdt: "Северная РДТ", riskScore: 4.5, riskLevel: "moderate", appealsCount: 11, mainCat: "TECH-06 Генераторы", enps: +29 },
        { name: "Павлодарская область", rdt: "Северная РДТ", riskScore: 4.2, riskLevel: "moderate", appealsCount: 12, mainCat: "HSE-01 Обувь", enps: +30 },
        { name: "Костанайская область", rdt: "Северная РДТ", riskScore: 3.8, riskLevel: "low", appealsCount: 9, mainCat: "TECH-06 Инструмент", enps: +34 },
        { name: "Алматинская область", rdt: "Региональная РДТ", riskScore: 3.7, riskLevel: "low", appealsCount: 10, mainCat: "PAY-02 Оплата", enps: +36 },
        { name: "Область Жетісу", rdt: "Региональная РДТ", riskScore: 3.5, riskLevel: "low", appealsCount: 7, mainCat: "LIFE-07 Питание", enps: +38 },
        { name: "Акмолинская область", rdt: "Северная РДТ", riskScore: 3.2, riskLevel: "low", appealsCount: 8, mainCat: "HSE-01 СИЗ", enps: +40 },
        { name: "г. Астана", rdt: "Центральный аппарат", riskScore: 2.1, riskLevel: "low", appealsCount: 14, mainCat: "TECH-06 ПО", enps: +48 }
      ],
      currentAppealChat: {
        rawText: "",
        division: "ОДС",
        region: "Атырауская область",
        categoryTitle: "Охрана труда и СИЗ (HSE-01)",
        recipient: "Департамент производственной безопасности (Смагулов Б.К.)",
        isAnonymous: true,
        token: "TK-7842-KZ",
        regNumber: "ВХ-2026/0942-КАНЦ"
      }
    };

    // -------------------------------------------------------------
    // 2. INITIALIZATION ON LOAD
    // -------------------------------------------------------------
    document.addEventListener("DOMContentLoaded", () => {
      renderChancelleryTable();
      renderHeatmapGrid();
      initCharts();
      startSLATickingEngine();
      
      // Auto open Nudge modal after gentle delay
      setTimeout(() => {
        openNudgeModal();
      }, 1200);
    });

    // -------------------------------------------------------------
    // 3. ROLE SWITCHING CONTROLLER
    // -------------------------------------------------------------
    function switchRole(roleKey) {
      const roleDef = window.platformState.roles[roleKey];
      if (!roleDef) return;

      window.platformState.currentUser.role = roleKey;

      // Update Topbar Role Buttons
      document.querySelectorAll('.role-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.getElementById(`btn-role-${roleKey.replace('ROLE_', '').toLowerCase()}`);
      if (activeBtn) activeBtn.classList.add('active');

      // Update User Label & Active Role indicator
      document.getElementById('topbar-username').textContent = roleDef.userLabel;
      document.getElementById('active-role-text').textContent = `${roleKey} (${roleDef.title})`;

      // Switch to Primary Tab for this role
      switchCanvasTab(roleDef.primaryTab);
      showToast(`Переключено в рабочее пространство: ${roleDef.title}`);
    }

    // -------------------------------------------------------------
    // 4. TAB NAVIGATION CONTROLLER
    // -------------------------------------------------------------
    function switchCanvasTab(tabId) {
      document.querySelectorAll('.canvas-screen').forEach(el => el.classList.remove('active'));
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');

      document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = Array.from(document.querySelectorAll('.nav-tab-btn')).find(b => {
        const attr = b.getAttribute('onclick') || '';
        return attr.includes(tabId);
      });
      if (activeBtn) activeBtn.classList.add('active');
    }

    // -------------------------------------------------------------
    // 5. NUDGE MODAL CONTROLLER
    // -------------------------------------------------------------
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
        showToast("Открыта форма прямого ввода заявления...");
      } else {
        showToast("Спасибо за чекин! Рады, что у вас все в порядке.");
      }
    }

    // -------------------------------------------------------------
    // 6. CHAT CONTROLLER (AI QWEN 2.5 SIMULATION)
    // -------------------------------------------------------------
    function applyPreset(presetType) {
      const input = document.getElementById('chat-text-input');
      if (presetType === 'ppe') {
        input.value = "В филиале ОДС Запад уже 2 месяца не выдают зимнюю обувь и утепленные куртки. Монтеры вынуждены выезжать на морозы в летних ботинках.";
      } else if (presetType === 'overtime') {
        input.value = "Начальник участка принуждает оставаться после смены и выходить по субботам, табель закрывает как 8 часов. При отказе угрожает срезать премию.";
      } else {
        input.value = "Мастер систематически грубит, допускает оскорбления в адрес монтеров и угрожает увольнением за любые замечания по Колдоговору.";
      }
      sendChatProblem();
    }

    function handleChatEnter(e) {
      if (e.key === 'Enter') sendChatProblem();
    }

    function sendChatProblem() {
      const input = document.getElementById('chat-text-input');
      const text = input.value.trim();
      if (!text) return;

      window.platformState.currentAppealChat.rawText = text;
      input.value = "";
      document.getElementById('quick-chips-container').style.display = 'none';

      appendChatUserMsg(text);

      showChatTyping(() => {
        renderChatQuestionnaire();
      });
    }

    function renderChatQuestionnaire() {
      let cat = "Охрана труда и производственная безопасность (СИЗ)";
      let code = "HSE-01";
      let recip = "Департамент производственной безопасности (Смагулов Б.К.)";

      const txt = window.platformState.currentAppealChat.rawText.toLowerCase();
      if (txt.includes("суббот") || txt.includes("преми") || txt.includes("оплат") || txt.includes("табел")) {
        cat = "Оплата труда и сверхурочные работы (ст. 108 ТК РК)";
        code = "PAY-02";
        recip = "Департамент оплаты труда (Ким А.В.)";
      } else if (txt.includes("груб") || txt.includes("угрож") || txt.includes("моббинг") || txt.includes("мастер")) {
        cat = "Моббинг и служебная этика руководства";
        code = "MOB-04";
        recip = "Служба комплаенс и Омбудсмен (Утепов Т.С.)";
      }

      window.platformState.currentAppealChat.categoryTitle = cat;
      window.platformState.currentAppealChat.recipient = recip;

      appendChatAIMsg(`
        Я зафиксировал фактуру происшествия.<br>
        <strong>Категория инцидента:</strong> <span style="color:#00468C; font-weight:700;">${cat} (${code})</span>.<br><br>
        Чтобы составить юридически выверенное заявление со статьями Трудового кодекса РК, ответьте на <strong>3 уточняющих вопроса</strong>:
      `);

      const injectBox = document.getElementById('chat-dynamic-injections');
      const qCard = document.createElement('div');
      qCard.id = 'active-chat-qcard';
      qCard.style = "background:white; border:1.5px solid #CBD5E1; border-radius:12px; padding:16px; margin-top:8px; border-left:4px solid #0284C7;";
      qCard.innerHTML = `
        <div style="font-size:13px; font-weight:700; margin-bottom:8px;">1. Укажите подразделение / регион:</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">
          <button class="nav-tab-btn active" style="background:#00468C; color:white; font-size:11.5px;" onclick="selectChatQ(this)">ОДС Западная РДТ (Атырау)</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">ОДС Восточная РДТ (Семей)</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Сервисная фабрика (Алматы)</button>
        </div>

        <div style="font-size:13px; font-weight:700; margin-bottom:8px;">2. Сколько работников затронуто проблемой?</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Лично меня</button>
          <button class="nav-tab-btn active" style="background:#00468C; color:white; font-size:11.5px;" onclick="selectChatQ(this)">Вся выездная бригада (18 монтеров)</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Весь участок (&gt;35 человек)</button>
        </div>

        <div style="font-size:13px; font-weight:700; margin-bottom:8px;">3. Обращались ли вы ранее к непосредственному мастеру?</div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px;">
          <button class="nav-tab-btn active" style="background:#00468C; color:white; font-size:11.5px;" onclick="selectChatQ(this)">Да, получили отказ / бездействие</button>
          <button class="nav-tab-btn" style="background:#F1F5F9; color:#334155; font-size:11.5px;" onclick="selectChatQ(this)">Опасаемся давления руководства</button>
        </div>

        <button class="btn-action-primary" style="width:100%; justify-content:center;" onclick="proceedToChatStatement()">
          📝 Сформировать официальное заявление со статьями ТК РК
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
        appendChatAIMsg("Спасибо! На основе ваших показаний нейросеть синтезировала юридически выверенное заявление:");

        const injectBox = document.getElementById('chat-dynamic-injections');
        const st = document.createElement('div');
        st.className = 'formal-statement-card';
        st.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1.5px solid #E2E8F0; padding-bottom:8px; margin-bottom:10px;">
            <strong style="color:#00468C; font-size:13px;">ПРОЕКТ ЗАЯВЛЕНИЯ В КАНЦЕЛЯРИЮ</strong>
            <span class="badge-status status-work">🟡 Риск забастовки: 8.8/10</span>
          </div>
          <div style="font-size:12px; margin-bottom:4px;"><strong>Категория:</strong> ${window.platformState.currentAppealChat.categoryTitle}</div>
          <div style="font-size:12px; margin-bottom:4px;"><strong>Подразделение:</strong> ОДС • Атырауская область (Западная РДТ)</div>
          <div style="font-size:12px; margin-bottom:8px;"><strong>Масштаб:</strong> Коллективное (затронуто 18 монтеров)</div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:10px; border-radius:6px; font-size:12.5px; line-height:1.5; margin-bottom:12px;">
            «Заявитель сообщает о систематическом нарушении требований ст. 182 Трудового кодекса РК и п. 4.2 Коллективного договора АО „Казахтелеком“. Суть: ${window.platformState.currentAppealChat.rawText}. Требование: немедленно провести ревизию складов и обеспечить выездные бригады зимней экипировкой.»
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
                <div style="font-size:11px; color:#64748B;">С внесением ФИО из CDN SSO</div>
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
      window.platformState.currentAppealChat.isAnonymous = isAnon;
      document.getElementById('chat-mode-anon').style.border = isAnon ? "2px solid #10B981" : "1px solid #CBD5E1";
      document.getElementById('chat-mode-anon').style.background = isAnon ? "#F0FDF4" : "white";
      document.getElementById('chat-mode-off').style.border = isAnon ? "1px solid #CBD5E1" : "2px solid #00468C";
      document.getElementById('chat-mode-off').style.background = isAnon ? "white" : "#F0F9FF";
    }

    function executeRegistrationInChancellery() {
      showChatTyping(() => {
        appendChatAIMsg("🏛️ <strong>Обращение успешно зарегистрировано в официальном реестре Канцелярии!</strong>");

        const randNum = Math.floor(1000 + Math.random() * 9000);
        const newRegNum = `ВХ-2026/${randNum}-КАНЦ`;
        const newToken = `TK-${randNum}-KZ`;

        window.platformState.currentAppealChat.regNumber = newRegNum;
        window.platformState.currentAppealChat.token = newToken;

        // Add to platformState.appeals
        const newAppeal = {
          id: Date.now(),
          regNumber: newRegNum,
          token: newToken,
          isAnonymous: window.platformState.currentAppealChat.isAnonymous,
          applicantName: window.platformState.currentAppealChat.isAnonymous ? "Анонимный заявитель" : "Ахметов Данияр Бауыржанұлы",
          division: "ОДС",
          region: "Атырауская область",
          categoryCode: "HSE-01",
          categoryTitle: window.platformState.currentAppealChat.categoryTitle,
          rawText: window.platformState.currentAppealChat.rawText,
          recipientDept: window.platformState.currentAppealChat.recipient,
          status: "IN_WORK",
          slaTotalSeconds: 5 * 24 * 3600,
          slaRemainingSeconds: 5 * 24 * 3600 - 10,
          conflictGuardActive: true,
          regDate: "10.11.2026 18:05"
        };
        window.platformState.appeals.unshift(newAppeal);
        renderChancelleryTable();

        const injectBox = document.getElementById('chat-dynamic-injections');
        const stamp = document.createElement('div');
        stamp.style = "background:#F8FAFC; border:2px dashed #00468C; border-radius:12px; padding:16px; margin-top:8px;";
        stamp.innerHTML = `
          <div style="background:#00468C; color:white; font-size:11px; font-weight:800; padding:4px 8px; border-radius:4px; display:inline-block; margin-bottom:8px;">
            🏛️ ЗАРЕГИСТРИРОВАНО В КАНЦЕЛЯРИИ
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:12px; margin-bottom:8px;">
            <div>Входящий номер: <strong style="color:#00468C;">${newRegNum}</strong></div>
            <div>Статус: <strong style="color:#0284C7;">В ОБРАБОТКЕ</strong></div>
            <div>Режим: <strong>${window.platformState.currentAppealChat.isAnonymous ? '🔒 Конфиденциально' : '👤 Официально'}</strong></div>
            <div>Дата: <strong>10.11.2026 18:05</strong></div>
          </div>
          <div style="background:#0B132B; color:#38BDF8; font-family:'JetBrains Mono', monospace; font-size:15px; font-weight:700; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
            <span>${newToken}</span>
            <button style="background:#0284C7; color:white; border:none; padding:4px 8px; border-radius:4px; font-size:11px; cursor:pointer;" onclick="copyTokenText('${newToken}')">Скопировать</button>
          </div>
          <div style="margin-top:10px; font-size:12px; color:#475569;">
            🎯 <strong>Первый получатель:</strong> ${window.platformState.currentAppealChat.recipient}<br>
            🛡️ <em>Conflict Guard: мастер участка аппаратно исключен из проверки.</em>
          </div>
          <div class="sla-timer-widget">
            <div>
              <div style="font-size:11px; color:#94A3B8;">⏱️ Нормативный срок ответа (SLA 5 дней):</div>
              <div class="sla-countdown-digits" id="live-chat-sla">04д 23ч 59м 50с</div>
            </div>
            <button class="btn-action-primary" style="background:#0284C7; font-size:11.5px;" onclick="switchCanvasTab('tab-chancellery')">
              Перейти в Реестр →
            </button>
          </div>
        `;
        injectBox.appendChild(stamp);
        scrollChat();

        showToast("Обращение успешно зарегистрировано в реестре Канцелярии!");
      });
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
      t.innerHTML = `<div class="msg-avatar ai">ИИ</div><div style="padding:10px 14px; background:white; border:1px solid #CBD5E1; border-radius:12px; font-size:12px; color:#64748B;">🧠 Нейросеть квалифицирует нарушение и проверяет ТК РК...</div>`;
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

    // -------------------------------------------------------------
    // 7. PULSE SURVEY & SYNERGY TRIGGER
    // -------------------------------------------------------------
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
      showToast("🎉 Спасибо! Ваши ответы запечатаны в квартальный аналитический пул Q4.");
      switchCanvasTab('tab-portal');
    }

    // -------------------------------------------------------------
    // 8. SELF-SERVICE DIRECT FORM
    // -------------------------------------------------------------
    function submitDirectForm() {
      const text = document.getElementById('form-text').value.trim();
      if (!text) {
        alert("Пожалуйста, опишите суть инцидента в поле ввода.");
        return;
      }

      const div = document.getElementById('form-div').value;
      const reg = document.getElementById('form-region').value;
      const catSelect = document.getElementById('form-category');
      const catCode = catSelect.value;
      const catTitle = catSelect.options[catSelect.selectedIndex].text;
      const isAnon = (document.getElementById('form-anon').value === 'anon');

      const randNum = Math.floor(1000 + Math.random() * 9000);
      const newRegNum = `ВХ-2026/${randNum}-КАНЦ`;
      const newToken = `TK-${randNum}-KZ`;

      let recip = "Департамент производственной безопасности";
      if (catCode === "PAY-02" || catCode === "OT-03") recip = "Департамент оплаты труда (Ким А.В.)";
      if (catCode === "MOB-04") recip = "Служба комплаенс и Омбудсмен";

      const newAppeal = {
        id: Date.now(),
        regNumber: newRegNum,
        token: newToken,
        isAnonymous: isAnon,
        applicantName: isAnon ? "Анонимный заявитель" : "Ахметов Данияр Бауыржанұлы",
        division: div,
        region: reg,
        categoryCode: catCode,
        categoryTitle: catTitle,
        rawText: text,
        recipientDept: recip,
        status: "IN_WORK",
        slaTotalSeconds: 5 * 24 * 3600,
        slaRemainingSeconds: 5 * 24 * 3600,
        conflictGuardActive: true,
        regDate: "10.11.2026 18:08"
      };

      window.platformState.appeals.unshift(newAppeal);
      renderChancelleryTable();

      showToast(`Обращение ${newRegNum} зарегистрировано в Канцелярии!`);
      switchCanvasTab('tab-chancellery');
    }

    function simulateFileUpload() {
      document.getElementById('file-drop-label').textContent = "✅ Прикреплено: foto_defekt_obuvi_2026.jpg (3.2 МБ)";
      showToast("Файл доказательства успешно прикреплен!");
    }

    // -------------------------------------------------------------
    // 9. CHANCELLERY REGISTRY TABLE & LIVE SLA ENGINE
    // -------------------------------------------------------------
    function renderChancelleryTable() {
      const tbody = document.getElementById('master-chancellery-tbody');
      if (!tbody) return;

      tbody.innerHTML = window.platformState.appeals.map(a => {
        let badgeHtml = '<span class="badge-status status-work">В работе</span>';
        if (a.status === 'ESCALATED') badgeHtml = '<span class="badge-status status-escalated">Эскалация</span>';
        if (a.status === 'RESOLVED') badgeHtml = '<span class="badge-status status-success">Закрыто</span>';

        let slaColor = '#059669';
        let slaText = formatSecondsToSLA(a.slaRemainingSeconds);
        if (a.slaRemainingSeconds <= 0) {
          slaColor = '#DC2626';
          slaText = '⚠️ ПРОСРОЧЕНО';
        } else if (a.slaRemainingSeconds < 24 * 3600) {
          slaColor = '#D97706';
        }

        return `
          <tr>
            <td>
              <strong style="color: #00468C;">${a.regNumber}</strong><br>
              <span style="font-family:'JetBrains Mono', monospace; font-size:10.5px; color:#64748B;">${a.token}</span>
            </td>
            <td>${a.regDate}</td>
            <td>
              ${a.isAnonymous 
                ? '<span class="badge-status status-closed">🔒 Анонимно</span>' 
                : `<span class="badge-status" style="background:#EBF3FA; color:#00468C;">👤 ${a.applicantName}</span>`}
            </td>
            <td><strong>${a.division}</strong> • ${a.region}</td>
            <td>
              <strong>${a.categoryTitle}</strong><br>
              <span style="font-size:11px; color:#64748B;">${a.rawText.substring(0, 48)}...</span>
            </td>
            <td>
              <strong>${a.recipientDept}</strong><br>
              <span style="font-size:10.5px; color:#10B981;">🛡️ Conflict Guard: Защищен</span>
            </td>
            <td>${badgeHtml}</td>
            <td style="font-family:'JetBrains Mono', monospace; font-weight:700; color:${slaColor};" id="sla-cell-${a.id}">
              ${slaText}
            </td>
            <td>
              <div style="display:flex; gap:4px;">
                <button class="btn-action-primary" style="padding:4px 8px; font-size:11px;" onclick="openStampModal('${a.regNumber}', '${a.recipientDept}', '${a.regDate}')">🏛️ Штамп</button>
                <button class="btn-action-secondary" style="padding:4px 8px; font-size:11px;" onclick="openTokenModal()">👁️</button>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    function formatSecondsToSLA(totalSec) {
      if (totalSec <= 0) return '⚠️ ПРОСРОЧЕНО';
      const d = Math.floor(totalSec / (24 * 3600));
      const h = Math.floor((totalSec % (24 * 3600)) / 3600);
      const m = Math.floor((totalSec % 3600) / 60);
      const s = totalSec % 60;
      return `⏱️ ${d}д ${h}ч ${m}м ${s}с`;
    }

    function startSLATickingEngine() {
      setInterval(() => {
        window.platformState.appeals.forEach(a => {
          if (a.status !== 'RESOLVED') {
            a.slaRemainingSeconds--;
            const cell = document.getElementById(`sla-cell-${a.id}`);
            if (cell) {
              cell.textContent = formatSecondsToSLA(a.slaRemainingSeconds);
              if (a.slaRemainingSeconds <= 0) {
                cell.style.color = '#DC2626';
              } else if (a.slaRemainingSeconds < 24 * 3600) {
                cell.style.color = '#D97706';
              }
            }
          }
        });

        // Update chat SLA widget if present
        const chatSla = document.getElementById('live-chat-sla');
        if (chatSla && window.platformState.appeals.length > 0) {
          chatSla.textContent = formatSecondsToSLA(window.platformState.appeals[0].slaRemainingSeconds);
        }

        // Live clock
        const clockEl = document.getElementById('chancellery-clock');
        if (clockEl) {
          const now = new Date();
          clockEl.textContent = now.toLocaleDateString('ru-RU') + ' ' + now.toLocaleTimeString('ru-RU');
        }
      }, 1000);
    }

    // -------------------------------------------------------------
    // 10. EXTERNAL DATA INGESTION (CSV/XLSX PARSER IN EX SERVICE)
    // -------------------------------------------------------------
    const sampleCsvContent = `Регион,Дивизион,Текучесть_монтеров_%,Дефицит_СИЗ_%,Разрыв_зарплат_%,Индекс_риска_забастовки
Атырауская область,ОДС,18.4,42.5,22.1,8.8
Мангистауская область,ОДС,16.2,38.1,19.4,7.9
Область Абай,ОДС,14.8,31.0,17.5,7.4
Область Ұлытау,СФ,13.5,28.4,15.2,6.8
Кызылординская область,ОДС,12.8,25.0,14.1,6.4
ЗКО (Уральск),ОДС,12.1,23.5,13.0,6.2
Актюбинская область,ОДС,11.5,21.0,12.2,5.8
г. Алматы,СФ,9.8,12.4,8.5,4.6
г. Астана,ЦА,4.2,3.1,2.0,2.1`;

    function loadSampleCsvData() {
      parseAndDisplayCsv(sampleCsvContent, "Внешний аудит текучести и дефицита СИЗ 2026.csv");
      showToast("Эталонный CSV загружен и распарсен!");
    }

    function handleCsvFile(e) {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(evt) {
        parseAndDisplayCsv(evt.target.result, file.name);
        showToast(`Файл ${file.name} успешно прочитан!`);
      };
      reader.readAsText(file, "UTF-8");
    }

    function parseAndDisplayCsv(text, filename) {
      const lines = text.trim().split(/\r?\n/);
      if (lines.length < 2) return;

      const headers = lines[0].split(/[;,]/);
      const rows = lines.slice(1).map(l => l.split(/[;,]/));

      const table = document.getElementById('external-csv-table');
      table.innerHTML = `
        <thead>
          <tr>${headers.map(h => `<th>${h.trim()}</th>`).join('')}</tr>
        </thead>
        <tbody>
          ${rows.map(r => `<tr>${r.map(c => `<td>${c.trim()}</td>`).join('')}</tr>`).join('')}
        </tbody>
      `;

      document.getElementById('external-table-title').textContent = `Загруженный файл: ${filename}`;
      document.getElementById('external-rows-count').textContent = `${rows.length} строк импортировано`;
      document.getElementById('external-data-preview-box').style.display = 'block';
    }

    function executeDataCorrelationMerge() {
      document.getElementById('correlation-result-box').style.display = 'block';
      showToast("Внешние данные объединены с аналитической моделью климата!");
    }

    // -------------------------------------------------------------
    // 11. KAZAKHSTAN 20-REGION HEATMAP CONTROLLER
    // -------------------------------------------------------------
    function renderHeatmapGrid() {
      const container = document.getElementById('heatmap-grid-container');
      if (!container) return;

      container.innerHTML = window.platformState.regions20.map(reg => {
        let badgeColor = '#10B981';
        if (reg.riskLevel === 'critical') badgeColor = '#EF4444';
        if (reg.riskLevel === 'high') badgeColor = '#F59E0B';
        if (reg.riskLevel === 'moderate') badgeColor = '#3B82F6';

        return `
          <div class="region-tile risk-${reg.riskLevel}" onclick="openRegionModal('${reg.name}')">
            <div class="region-tile-title">${reg.name}</div>
            <div style="font-size:11px; color:#64748B; margin-bottom:8px;">${reg.rdt}</div>
            <div class="region-tile-score" style="color:${badgeColor};">
              <span>Риск: ${reg.riskScore}</span>
              <span style="font-size:11px; font-weight:600; color:#475569;">${reg.appealsCount} дел</span>
            </div>
            <div style="font-size:10.5px; color:#64748B; margin-top:4px;">
              Фокус: <strong>${reg.mainCat}</strong>
            </div>
          </div>
        `;
      }).join('');
    }

    function openRegionModal(regionName) {
      const reg = window.platformState.regions20.find(r => r.name === regionName);
      if (!reg) return;

      document.getElementById('region-modal-title').textContent = `${reg.name} (${reg.rdt})`;
      const body = document.getElementById('region-modal-body');

      let riskBadge = `<span class="badge-status status-work" style="background:#FEE2E2; color:#B91C1C;">КРИТИЧЕСКИЙ РИСК (${reg.riskScore}/10)</span>`;
      if (reg.riskLevel === 'high') riskBadge = `<span class="badge-status" style="background:#FEF3C7; color:#B45309;">ВЫСОКИЙ РИСК (${reg.riskScore}/10)</span>`;
      if (reg.riskLevel === 'moderate') riskBadge = `<span class="badge-status" style="background:#DBEAFE; color:#1E40AF;">УМЕРЕННЫЙ РИСК (${reg.riskScore}/10)</span>`;
      if (reg.riskLevel === 'low') riskBadge = `<span class="badge-status status-success">СТАБИЛЬНО (${reg.riskScore}/10)</span>`;

      body.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #E2E8F0; padding-bottom:10px;">
          <div>
            <strong>Интегральный статус региона:</strong><br>
            <span style="font-size:11.5px; color:#64748B;">Индекс напряженности и трудовых рисков</span>
          </div>
          ${riskBadge}
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px;">
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:8px;">
            <div style="font-size:11px; color:#64748B;">Открытые обращения</div>
            <div style="font-size:20px; font-weight:800; color:#00468C;">${reg.appealsCount} дел</div>
            <span style="font-size:10.5px; color:#EF4444;">87% через анонимный контур</span>
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; padding:12px; border-radius:8px;">
            <div style="font-size:11px; color:#64748B;">Индекс лояльности (eNPS)</div>
            <div style="font-size:20px; font-weight:800; color:${reg.enps < 0 ? '#DC2626' : '#0284C7'};">${reg.enps}</div>
            <span style="font-size:10.5px; color:#64748B;">Пульс-опрос Q4</span>
          </div>
        </div>

        <div style="background:#FFFFFF; border:1px solid var(--border); border-radius:8px; padding:12px; margin-bottom:16px;">
          <strong style="font-size:12.5px; color:#0F172A;">Системный очаг в регионе:</strong>
          <p style="font-size:12px; color:#475569; margin-top:4px; line-height:1.4;">
            Преобладающая категория обращений — <strong>${reg.mainCat}</strong>. 
            Нейросеть Qwen 2.5 выявила задержки в материально-техническом снабжении аварийно-восстановительных бригад и необходимость точечной проверки графиков сменности.
          </p>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center;">
          <button class="btn-action-primary" style="font-size:12px;" onclick="closeRegionModal(); switchCanvasTab('tab-chancellery');">
            📋 Открыть реестр по данному региону
          </button>
          <button class="btn-action-secondary" style="font-size:12px;" onclick="closeRegionModal()">
            Закрыть
          </button>
        </div>
      `;

      document.getElementById('modal-region-inspector').classList.add('active');
    }

    function closeRegionModal() {
      document.getElementById('modal-region-inspector').classList.remove('active');
    }

    // -------------------------------------------------------------
    // 12. TOKEN SEARCH & SAFE TWO-WAY CHAT MODAL
    // -------------------------------------------------------------
    function openTokenModal() {
      document.getElementById('modal-token-tracker').classList.add('active');
    }

    function closeTokenModal() {
      document.getElementById('modal-token-tracker').classList.remove('active');
    }

    function lookupToken() {
      const code = document.getElementById('token-search-input').value.trim();
      const match = window.platformState.appeals.find(a => a.token.toLowerCase() === code.toLowerCase() || a.regNumber.toLowerCase() === code.toLowerCase());
      if (match) {
        document.getElementById('token-res-num').textContent = match.regNumber;
        document.getElementById('token-res-cat').textContent = match.categoryTitle;
        document.getElementById('token-res-sla').textContent = `⏱️ Контрольный срок SLA: ${formatSecondsToSLA(match.slaRemainingSeconds)}`;
        showToast(`Обращение ${match.regNumber} найдено!`);
      } else {
        showToast("Обращение с таким токеном не найдено.");
      }
    }

    function sendTokenReply() {
      const input = document.getElementById('token-reply-input');
      const txt = input.value.trim();
      if (!txt) return;

      const stream = document.getElementById('token-chat-stream');
      const userMsg = document.createElement('div');
      userMsg.style = "background:#EBF3FA; color:#00468C; padding:8px 10px; border-radius:6px; align-self:flex-end;";
      userMsg.innerHTML = `<strong>Вы (18:10):</strong> ${txt}`;
      stream.appendChild(userMsg);
      input.value = "";

      setTimeout(() => {
        const resp = document.createElement('div');
        resp.style = "background:#F1F5F9; padding:8px 10px; border-radius:6px;";
        resp.innerHTML = `<strong>Исполнитель (Смагулов Б.К.):</strong> «Дополнительные сведения приняты и приобщены к материалам проверки.»`;
        stream.appendChild(resp);
      }, 1000);
    }

    // -------------------------------------------------------------
    // 13. CHANCELLERY STAMP MODAL
    // -------------------------------------------------------------
    function openStampModal(num, recip, date) {
      document.getElementById('stamp-modal-num').textContent = num || 'ВХ-2026/0942-КАНЦ';
      document.getElementById('stamp-modal-recip').textContent = recip || 'Департамент охраны труда';
      document.getElementById('stamp-modal-date').textContent = date || '10.11.2026 18:05:40';
      document.getElementById('modal-chancellery-stamp').classList.add('active');
    }

    function closeStampModal() {
      document.getElementById('modal-chancellery-stamp').classList.remove('active');
    }

    function openProfileModal() {
      alert(`Профиль CDN SSO:\nФИО: ${window.platformState.currentUser.name}\nТабельный номер: TN-48291\nПодразделение: ${window.platformState.currentUser.division} (${window.platformState.currentUser.region})\nУровень доступа: Авторизован в защищенном контуре`);
    }

    function copyTokenText(txt) {
      navigator.clipboard.writeText(txt);
      showToast(`Токен ${txt} скопирован в буфер!`);
    }

    function showToast(msg) {
      const box = document.getElementById('toast-box');
      const toast = document.createElement('div');
      toast.className = 'toast-pill';
      toast.innerHTML = `<span>🔔</span><span>${msg}</span>`;
      box.appendChild(toast);
      setTimeout(() => { toast.remove(); }, 4000);
    }

    // -------------------------------------------------------------
    // 14. CHART.JS VISUALIZATIONS
    // -------------------------------------------------------------
    function initCharts() {
      const c1 = document.getElementById('chartExecCategories');
      if (c1) {
        new Chart(c1, {
          type: 'doughnut',
          data: {
            labels: ['HSE-01 Охрана труда / СИЗ', 'PAY-02 Оплата труда', 'OT-03 Сверхурочные', 'MOB-04 Моббинг', 'TECH-06 Инфраструктура'],
            datasets: [{
              data: [38, 26, 14, 12, 10],
              backgroundColor: ['#00468C', '#0284C7', '#6366F1', '#F59E0B', '#EF4444'],
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: { boxWidth: 10, font: { size: 10.5 } }
              }
            }
          }
        });
      }

      const c2 = document.getElementById('chartExecSLA');
      if (c2) {
        new Chart(c2, {
          type: 'bar',
          data: {
            labels: ['ОДС (Сеть)', 'СФ (Сервис)', 'ДРБ (Розница)', 'ДКБ (Корп)', 'ДУП (HR)', 'ДПБ (HSE)'],
            datasets: [{
              label: 'Соблюдение SLA (%)',
              data: [96.4, 97.2, 98.6, 100, 99.1, 98.0],
              backgroundColor: ['#0284C7', '#0284C7', '#10B981', '#10B981', '#10B981', '#10B981'],
              borderRadius: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              y: { min: 85, max: 100 }
            }
          }
        });
      }
    }
  </script>
</body>
</html>
'''
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content.strip())
    print(f"index.html successfully created with {len(html_content)} characters.")

if __name__ == "__main__":
    generate_html()
