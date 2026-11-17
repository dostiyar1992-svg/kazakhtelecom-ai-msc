# -*- coding: utf-8 -*-
"""
patch_chat_survey.py
Integrates the Autonomous Project-Driven Survey into the Chat view of generate_final_index.py
and index.html.
"""

import sys

with open("generate_final_index.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add mode buttons above chat header
old_chat_header = """<section id="workspace-chat" class="canvas-screen" data-tab="tab-chat">
        <div class="chat-layout-wrapper">
          <div class="chat-header">"""

new_chat_header = """<section id="workspace-chat" class="canvas-screen" data-tab="tab-chat">
        <div class="chat-layout-wrapper">
          <!-- Chat Mode Switcher: Intake vs Autonomous Survey -->
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; background:white; padding:8px 12px; border-radius:8px; border:1px solid #E2E8F0;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:11.5px; font-weight:800; color:#64748B; text-transform:uppercase;">Режим ИИ-Диалога:</span>
              <button class="nav-tab-btn active" id="btn-chatmode-intake" style="font-size:11.5px; padding:5px 12px;" onclick="setChatMode('intake')">
                ⚖️ Прием обращений и жалоб
              </button>
              <button class="nav-tab-btn" id="btn-chatmode-survey" style="font-size:11.5px; padding:5px 12px; background:#F8FAFC; color:#00468C;" onclick="setChatMode('survey')">
                📋 Пульс-опрос по проекту (8 вопросов)
              </button>
            </div>
            <span class="badge-pill badge-official" style="font-size:10.5px;">Gemini 1.5 Flash • On-Premise Engine</span>
          </div>

          <div class="chat-header">"""

text = text.replace(old_chat_header, new_chat_header)

# 2. Add survey quick chip
old_chip = """<button class="nav-tab-btn" style="background:#EBF3FA; color:#00468C; font-size:11px;" onclick="applyPreset('ppe')">
                      🥾 Срыв выдачи зимней обуви и курток монтерам (Атырау)
                    </button>"""

new_chip = """<button class="nav-tab-btn" style="background:#F0FDF4; border:1px solid #86EFAC; color:#15803D; font-size:11.5px; font-weight:700; width:100%; text-align:left;" onclick="setChatMode('survey')">
                      📋 Запустить пульс-опрос по документам проекта (пульс ө опрос.docx, ОПРОСНИК ПРОФС.docx)
                    </button>
                    <button class="nav-tab-btn" style="background:#EBF3FA; color:#00468C; font-size:11px;" onclick="applyPreset('ppe')">
                      🥾 Срыв выдачи зимней обуви и курток монтерам (Атырау)
                    </button>"""

text = text.replace(old_chip, new_chip)

# 3. Add JS functions for survey in chat
survey_js_code = """
    // -------------------------------------------------------------
    // AUTONOMOUS SURVEY DRIVEN BY GEMINI & PROJECT DATA
    // -------------------------------------------------------------
    let currentChatMode = 'intake'; // 'intake' | 'survey'
    let surveyChatSession = null;

    function setChatMode(mode) {
      currentChatMode = mode;
      const btnIntake = document.getElementById('btn-chatmode-intake');
      const btnSurvey = document.getElementById('btn-chatmode-survey');

      if (mode === 'survey') {
        if (btnIntake) btnIntake.classList.remove('active');
        if (btnSurvey) { btnSurvey.classList.add('active'); btnSurvey.style.background = '#00468C'; btnSurvey.style.color = 'white'; }
        startSurveyInChat();
      } else {
        if (btnSurvey) { btnSurvey.classList.remove('active'); btnSurvey.style.background = '#F8FAFC'; btnSurvey.style.color = '#00468C'; }
        if (btnIntake) btnIntake.classList.add('active');
        resetChatFlow();
      }
    }

    function startSurveyInChat() {
      currentChatMode = 'survey';
      const stream = document.getElementById('chat-stream-box');
      if (!stream) return;

      const engine = window.KazakhtelecomSurveyEngine || (window.KazakhtelecomAI && window.KazakhtelecomAI.AutonomousSurveyEngine ? new window.KazakhtelecomAI.AutonomousSurveyEngine(window.platformStateStore) : null);
      if (engine) {
        surveyChatSession = engine;
        const qData = engine.startSurvey();
        renderSurveyQuestionInChat(qData);
      }
    }

    function renderSurveyQuestionInChat(qData) {
      const stream = document.getElementById('chat-stream-box');
      if (!stream) return;

      // Update progress bar
      updateChatProgress(qData.questionIndex, `Вопрос ${qData.questionIndex} из ${qData.totalQuestions}: ${qData.question.block}`, qData.progressPct);

      const aiRow = document.createElement('div');
      aiRow.className = 'chat-msg-row ai';
      aiRow.innerHTML = `
        <div class="msg-avatar ai">ИИ</div>
        <div class="msg-content-wrapper" style="width:100%;">
          <div class="msg-bubble">
            <div style="font-size:11px; font-weight:800; color:#0284C7; text-transform:uppercase; margin-bottom:4px;">
              ${qData.question.block} (Вопрос ${qData.questionIndex} из ${qData.totalQuestions})
            </div>
            <strong style="font-size:13.5px; color:#0F172A; display:block; margin-bottom:8px;">
              «${qData.question.text}»
            </strong>
            <div style="font-size:11px; color:#64748B; margin-bottom:12px;">
              📄 Источник в проекте: <em>${qData.question.docSource}</em>
            </div>
            
            <div style="background:#F8FAFC; padding:10px; border-radius:8px; border:1px solid #E2E8F0;">
              <div style="font-size:11px; font-weight:700; color:#475569; margin-bottom:8px; display:flex; justify-content:space-between;">
                <span>1 — ${qData.scaleMin || 'Не согласен'}</span>
                <span>5 — ${qData.scaleMax || 'Полностью согласен'}</span>
              </div>
              <div style="display:flex; gap:8px; justify-content:space-between;">
                ${[1, 2, 3, 4, 5].map(s => `
                  <button class="nav-tab-btn" style="flex:1; text-align:center; padding:8px 0; font-size:13px; font-weight:800; background:white; border:1px solid #CBD5E1; color:#00468C; cursor:pointer;" onclick="answerSurveyInChat(${s}, this)">
                    ${s}
                  </button>
                `).join('')}
              </div>
            </div>
          </div>
        </div>
      `;
      stream.appendChild(aiRow);
      stream.scrollTop = stream.scrollHeight;
    }

    function answerSurveyInChat(score, btnEl) {
      if (btnEl && btnEl.parentElement) {
        btnEl.parentElement.querySelectorAll('button').forEach(b => {
          b.disabled = true;
          b.style.opacity = '0.5';
        });
        btnEl.style.background = '#00468C';
        btnEl.style.color = 'white';
        btnEl.style.opacity = '1';
      }

      appendChatUserMsg(`Моя оценка: ${score} из 5`);

      setTimeout(() => {
        if (!surveyChatSession) return;
        const nextData = surveyChatSession.answerQuestion(score);

        // Check synergy trigger
        if (nextData.synergyAlert && nextData.criticalIssue) {
          renderChatSynergyAlert(nextData.criticalIssue, score);
        }

        if (nextData.isFinished) {
          renderSurveyCompletionInChat(nextData);
        } else {
          renderSurveyQuestionInChat(nextData);
        }
      }, 400);
    }

    function renderChatSynergyAlert(issue, score) {
      const stream = document.getElementById('chat-stream-box');
      if (!stream) return;

      const alertRow = document.createElement('div');
      alertRow.className = 'chat-msg-row ai';
      alertRow.innerHTML = `
        <div class="msg-avatar ai" style="background:#EF4444;">⚠️</div>
        <div class="msg-content-wrapper" style="width:100%;">
          <div style="background:#FEF2F2; border:1.5px solid #FCA5A5; border-radius:10px; padding:12px; box-shadow:0 2px 8px rgba(239,68,68,0.15);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span style="font-size:12px; font-weight:800; color:#DC2626;">🚨 СИНЕРГИЯ ОПРОСА И ПРИЕМНОЙ (Synergy Alert)</span>
              <span class="badge-pill badge-danger" style="font-size:10px;">Низкая оценка ${score}/5</span>
            </div>
            <p style="font-size:12px; color:#7F1D1D; line-height:1.4; margin-bottom:10px;">
              По вопросу <strong>«${issue.block}»</strong> вами зафиксирован критический уровень проблемы. 
              Хотите, чтобы ИИ сразу подготовил официальное заявление в Службу EX и Канцелярию для устранения нарушения?
            </p>
            <div style="display:flex; gap:8px;">
              <button class="btn-action-primary" style="background:#DC2626; font-size:11.5px; padding:6px 14px;" onclick="convertSurveyAlertToAppeal('${issue.id}', '${issue.text}')">
                ⚖️ Оформить жалобу по этому пункту
              </button>
              <button class="btn-action-secondary" style="font-size:11.5px; padding:6px 14px;" onclick="showToast('Продолжаем опрос. Данные сохранены в аналитический пул.')">
                Продолжить опрос ➔
              </button>
            </div>
          </div>
        </div>
      `;
      stream.appendChild(alertRow);
      stream.scrollTop = stream.scrollHeight;
    }

    function convertSurveyAlertToAppeal(qId, topicText) {
      setChatMode('intake');
      const input = document.getElementById('chat-text-input');
      if (input) {
        input.value = `По результатам пульс-опроса АО «Казахтелеком»: выявлена критическая проблема (${topicText}). Прошу провести проверку и устранить нарушение.`;
      }
      sendChatProblem();
      showToast("Трансформация в официальное обращение выполнена!");
    }

    function renderSurveyCompletionInChat(resData) {
      const stream = document.getElementById('chat-stream-box');
      if (!stream) return;

      updateChatProgress(8, "Пульс-опрос успешно завершен", 100);

      const r = resData.result;
      const compRow = document.createElement('div');
      compRow.className = 'chat-msg-row ai';
      compRow.innerHTML = `
        <div class="msg-avatar ai" style="background:#10B981;">🎉</div>
        <div class="msg-content-wrapper" style="width:100%;">
          <div style="background:linear-gradient(135deg, #F0FDF4, #FFFFFF); border:1.5px solid #86EFAC; border-radius:12px; padding:16px; box-shadow:0 4px 12px rgba(16,185,129,0.15);">
            <div style="font-size:15px; font-weight:800; color:#065F46; margin-bottom:4px;">
              🎉 Пульс-опрос АО «Казахтелеком» успешно завершен!
            </div>
            <p style="font-size:12px; color:#047857; margin-bottom:12px;">
              Спасибо за участие! Ваши ответы запечатаны в квартальный аналитический пул Samruk-Kazyna SRS.
            </p>

            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; margin-bottom:12px;">
              <div style="background:white; padding:10px; border-radius:8px; border:1px solid #A7F3D0; text-align:center;">
                <div style="font-size:11px; color:#059669; font-weight:700;">Индекс SRS</div>
                <div style="font-size:22px; font-weight:900; color:#065F46;">${r.srsIndex}%</div>
              </div>
              <div style="background:white; padding:10px; border-radius:8px; border:1px solid #A7F3D0; text-align:center;">
                <div style="font-size:11px; color:#059669; font-weight:700;">Лояльность eNPS</div>
                <div style="font-size:13px; font-weight:800; color:#065F46; margin-top:4px;">${r.enpsCategory}</div>
              </div>
              <div style="background:white; padding:10px; border-radius:8px; border:1px solid #A7F3D0; text-align:center;">
                <div style="font-size:11px; color:#059669; font-weight:700;">Статус климата</div>
                <div style="font-size:12px; font-weight:800; color:#065F46; margin-top:4px;">${r.climateStatus}</div>
              </div>
            </div>

            <div style="display:flex; gap:8px;">
              <button class="btn-action-primary" style="font-size:12px; background:#059669;" onclick="setChatMode('intake')">
                ⚖️ Перейти в режим приема обращений
              </button>
              <button class="btn-action-secondary" style="font-size:12px;" onclick="switchCanvasTab('workspace-employee')">
                Вернуться на главную
              </button>
            </div>
          </div>
        </div>
      `;
      stream.appendChild(compRow);
      stream.scrollTop = stream.scrollHeight;
      showToast("Пульс-опрос учтен в общекорпоративной аналитике!");
    }
"""

pos_js = text.find("// -------------------------------------------------------------")
if "startSurveyInChat" not in text:
    text = text[:pos_js] + survey_js_code + "\n" + text[pos_js:]

with open("generate_final_index.py", "w", encoding="utf-8") as f:
    f.write(text)

print("generate_final_index.py patched with survey in chat!")

