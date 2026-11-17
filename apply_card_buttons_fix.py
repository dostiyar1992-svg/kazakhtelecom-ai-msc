with open('generate_final_index.py', encoding='utf-8') as f:
    code = f.read()

# 1. Add id="inspector-action-box"
old_box = """<!-- Resolution Action Form (Update Stage & Add Notes) -->
      <div style="background:#F1F5F9; border:1.5px solid #CBD5E1; border-radius:var(--radius-md); padding:18px;">"""

new_box = """<!-- Resolution Action Form (Update Stage & Add Notes) -->
      <div id="inspector-action-box" style="background:#F1F5F9; border:1.5px solid #CBD5E1; border-radius:var(--radius-md); padding:18px;">"""

if old_box in code:
    code = code.replace(old_box, new_box, 1)
    print("Added id='inspector-action-box'!")
else:
    print("WARNING: old_box not found!")

# 2. Update openResolutionInspector and add openAppealCard & openTokenModalWithCode
old_fn = """    function openResolutionInspector(appealIdOrToken) {
      const appeals = (window.platformStateStore ? window.platformStateStore.getState().appeals : (window.platformState ? window.platformState.appeals : []));
      const match = appeals.find(a => a.id === Number(appealIdOrToken) || a.token === appealIdOrToken || a.regNumber === appealIdOrToken);
      if (!match) {
        showToast("Обращение не найдено");
        return;
      }

      document.getElementById('inspector-current-id').value = match.id;
      document.getElementById('inspector-reg-number').textContent = match.regNumber;
      document.getElementById('inspector-token-badge').textContent = match.token;
      
      const riskEl = document.getElementById('inspector-risk-badge');
      if (riskEl) {
        riskEl.textContent = match.riskLevel ? `${match.riskLevel} RISK` : 'NORMAL';
        riskEl.className = match.riskLevel === 'CRITICAL' ? 'badge-status status-danger' : 'badge-status status-work';
      }

      document.getElementById('inspector-category-sub').textContent = `Категория: ${match.categoryTitle} • Дивизион ${match.division} • ${match.region}`;
      document.getElementById('inspector-raw-text').textContent = match.rawText || '—';
      document.getElementById('inspector-formal-fabula').textContent = match.formalFabula || match.rawText || '—';

      // Build 6-stage Stepper
      const currentStage = match.resolutionStage || match.status;
      const stagesOrder = ['REGISTERED', 'IN_WORK', 'INSPECTION', 'MEASURES_TAKEN', 'RESOLVED', 'CLOSED'];
      const stagesLabels = [
        '1. Подача и ИИ', '2. Регистрация СЭД', '3. Комиссия ДПБ', 
        '4. Выездной аудит', '5. Приняты меры', '6. Закрыто заявителем'
      ];

      let activeStepIdx = 1;
      if (currentStage === 'INSPECTION') activeStepIdx = 3;
      else if (currentStage === 'MEASURES_TAKEN') activeStepIdx = 4;
      else if (currentStage === 'RESOLVED') activeStepIdx = 5;
      else if (currentStage === 'OVERDUE' || currentStage === 'ESCALATED') activeStepIdx = 3;

      const stepperContainer = document.getElementById('inspector-stepper-container');
      if (stepperContainer) {
        stepperContainer.innerHTML = stagesLabels.map((lbl, idx) => {
          const isDone = idx <= activeStepIdx;
          const isCurrent = idx === activeStepIdx;
          const bg = isCurrent ? '#00468C' : (isDone ? '#10B981' : '#E2E8F0');
          const color = isDone ? '#FFFFFF' : '#64748B';
          return `
            <div style="background:${bg}; color:${color}; padding:8px 4px; border-radius:4px; font-size:11px; font-weight:700;">
              ${lbl}
            </div>
          `;
        }).join('');
      }

      // Populate history log
      const historyList = match.resolutionHistory || [
        { stage: 'REGISTERED', note: 'Обращение зарегистрировано в оперативном контуре МСЦ', officer: 'ИИ-Ассистент «Айгерим»', date: match.date },
        { stage: 'IN_WORK', note: `Передано в ${match.recipientDept}`, officer: match.recipientOfficer || 'Служба EX', date: match.date }
      ];

      const histCountEl = document.getElementById('inspector-history-count');
      if (histCountEl) histCountEl.textContent = `${historyList.length} записей`;

      const histContainer = document.getElementById('inspector-history-timeline');
      if (histContainer) {
        histContainer.innerHTML = historyList.map(h => `
          <div style="background:white; border:1px solid #E2E8F0; border-radius:4px; padding:8px 10px; border-left:3px solid #0284C7;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <strong style="font-size:11.5px; color:#00468C;">${h.officer || 'Служба контроля'}</strong>
              <span style="font-size:10.5px; color:#64748B;">${h.date}</span>
            </div>
            <div style="font-size:11.5px; color:#334155; line-height:1.4;">${h.note}</div>
          </div>
        `).join('');
      }

      const modal = document.getElementById('modal-appeal-resolution-inspector');
      if (modal) modal.style.display = 'flex';
    }

    function closeResolutionInspector() {
      const modal = document.getElementById('modal-appeal-resolution-inspector');
      if (modal) modal.style.display = 'none';
    }"""

new_fn = """    function openAppealCard(appealIdOrToken) {
      openResolutionInspector(appealIdOrToken);
    }

    function openTokenModalWithCode(token) {
      if (!token) {
        openTokenModal();
        return;
      }
      openResolutionInspector(token);
    }

    function openResolutionInspector(appealIdOrToken) {
      const appeals = (window.platformStateStore ? window.platformStateStore.getState().appeals : (window.platformState ? window.platformState.appeals : []));
      if (!appeals || appeals.length === 0) {
        showToast("В системе пока нет зарегистрированных обращений.");
        return;
      }

      const target = String(appealIdOrToken || '').trim().toLowerCase();
      const match = appeals.find(a => 
        String(a.id) === target ||
        (a.token && a.token.toLowerCase() === target) ||
        (a.regNumber && a.regNumber.toLowerCase() === target) ||
        (a.token && a.token.toLowerCase().includes(target)) ||
        (a.regNumber && a.regNumber.toLowerCase().includes(target))
      ) || appeals[0];

      if (!match) {
        showToast("Обращение не найдено");
        return;
      }

      const currIdEl = document.getElementById('inspector-current-id');
      if (currIdEl) currIdEl.value = match.id;
      const regNumEl = document.getElementById('inspector-reg-number');
      if (regNumEl) regNumEl.textContent = match.regNumber || 'ВХ-2026/КАНЦ';
      const tokenEl = document.getElementById('inspector-token-badge');
      if (tokenEl) tokenEl.textContent = match.token || '';

      const riskEl = document.getElementById('inspector-risk-badge');
      if (riskEl) {
        riskEl.textContent = match.riskLevel ? `${match.riskLevel} RISK` : 'NORMAL';
        riskEl.className = match.riskLevel === 'CRITICAL' ? 'badge-status status-danger' : 'badge-status status-work';
      }

      const catSubEl = document.getElementById('inspector-category-sub');
      if (catSubEl) {
        catSubEl.textContent = `Категория: ${match.categoryTitle || match.categoryCode || 'Охрана труда'} • Дивизион ${match.division || 'ОДС'} • ${match.region || 'РК'}`;
      }
      const rawTextEl = document.getElementById('inspector-raw-text');
      if (rawTextEl) rawTextEl.textContent = match.rawText || '—';
      const formalEl = document.getElementById('inspector-formal-fabula');
      if (formalEl) formalEl.textContent = match.formalFabula || match.rawText || '—';

      // Build 6-stage Stepper
      const currentStage = match.resolutionStage || match.status;
      const stagesLabels = [
        '1. Подача и ИИ', '2. Регистрация СЭД', '3. Комиссия ДПБ', 
        '4. Выездной аудит', '5. Приняты меры', '6. Закрыто заявителем'
      ];

      let activeStepIdx = 1;
      if (currentStage === 'INSPECTION') activeStepIdx = 3;
      else if (currentStage === 'MEASURES_TAKEN') activeStepIdx = 4;
      else if (currentStage === 'RESOLVED') activeStepIdx = 5;
      else if (currentStage === 'OVERDUE' || currentStage === 'ESCALATED') activeStepIdx = 3;

      const stepperContainer = document.getElementById('inspector-stepper-container');
      if (stepperContainer) {
        stepperContainer.innerHTML = stagesLabels.map((lbl, idx) => {
          const isDone = idx <= activeStepIdx;
          const isCurrent = idx === activeStepIdx;
          const bg = isCurrent ? '#00468C' : (isDone ? '#10B981' : '#E2E8F0');
          const color = isDone ? '#FFFFFF' : '#64748B';
          return `
            <div style="background:${bg}; color:${color}; padding:8px 4px; border-radius:4px; font-size:11px; font-weight:700;">
              ${lbl}
            </div>
          `;
        }).join('');
      }

      // Populate history log
      const historyList = match.resolutionHistory || [
        { stage: 'REGISTERED', note: 'Обращение зарегистрировано в оперативном контуре МСЦ', officer: 'ИИ-Ассистент «Айгерим»', date: match.date },
        { stage: 'IN_WORK', note: `Передано в ${match.recipientDept || 'ДУП'}`, officer: match.recipientOfficer || 'Служба EX', date: match.date }
      ];

      const histCountEl = document.getElementById('inspector-history-count');
      if (histCountEl) histCountEl.textContent = `${historyList.length} записей`;

      const histContainer = document.getElementById('inspector-history-timeline');
      if (histContainer) {
        histContainer.innerHTML = historyList.map(h => `
          <div style="background:white; border:1px solid #E2E8F0; border-radius:4px; padding:8px 10px; border-left:3px solid #0284C7;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <strong style="font-size:11.5px; color:#00468C;">${h.officer || 'Служба контроля'}</strong>
              <span style="font-size:10.5px; color:#64748B;">${h.date}</span>
            </div>
            <div style="font-size:11.5px; color:#334155; line-height:1.4;">${h.note}</div>
          </div>
        `).join('');
      }

      // Hide administrative stage editor for employees
      const actionBox = document.getElementById('inspector-action-box');
      const currentUser = (window.platformStateStore && window.platformStateStore.getState().currentUser) || {};
      if (actionBox) {
        actionBox.style.display = (currentUser.role === 'ROLE_EMPLOYEE') ? 'none' : 'block';
      }

      const modal = document.getElementById('modal-appeal-resolution-inspector');
      if (modal) {
        modal.style.display = 'flex';
        if (modal.classList) modal.classList.add('active');
      }
    }

    function closeResolutionInspector() {
      const modal = document.getElementById('modal-appeal-resolution-inspector');
      if (modal) {
        modal.style.display = 'none';
        if (modal.classList) modal.classList.remove('active');
      }
    }"""

if old_fn in code:
    code = code.replace(old_fn, new_fn, 1)
    print("Replaced openResolutionInspector and added openAppealCard & openTokenModalWithCode!")
else:
    print("WARNING: old_fn not matched!")

# 3. Replace onclicks in renderMyAppealsList and other places to use openAppealCard
code = code.replace("onclick=\"openTokenModalWithCode('${a.token}')\"", "onclick=\"openAppealCard('${a.id || a.token}')\"")
code = code.replace("onclick=\"openTokenModalWithCode('${newRecord.token}')\"", "onclick=\"openAppealCard('${newRecord.token}')\"")

with open('generate_final_index.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("generate_final_index.py saved successfully!")
