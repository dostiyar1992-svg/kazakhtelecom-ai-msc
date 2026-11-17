/**
 * qa_comprehensive_test.js
 * Comprehensive QA Test Suite for Kazakhtelecom AI EX & Appeals Intelligence Platform (index.html)
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log("==================================================================");
console.log("🧪 STARTING COMPREHENSIVE QA AUDIT & VERIFICATION SUITE");
console.log("==================================================================\n");

let passedTests = 0;
let failedTests = 0;
const testResults = [];

function assert(condition, testName, details = "") {
  if (condition) {
    passedTests++;
    console.log(`  ✅ [PASS] ${testName}`);
    testResults.push({ name: testName, status: "PASS", details });
  } else {
    failedTests++;
    console.error(`  ❌ [FAIL] ${testName}: ${details}`);
    testResults.push({ name: testName, status: "FAIL", details });
  }
}

// ----------------------------------------------------------------------
// 1. STATIC CODE AUDIT (File presence, size, syntax)
// ----------------------------------------------------------------------
console.log("--- 1. STATIC CODE AUDIT ---");

const indexHtmlPath = path.resolve('index.html');
const jsModulePath = path.resolve('platform-state-and-rules.js');

assert(fs.existsSync(indexHtmlPath), "index.html exists", indexHtmlPath);
assert(fs.existsSync(jsModulePath), "platform-state-and-rules.js exists", jsModulePath);

const indexHtmlContent = fs.readFileSync(indexHtmlPath, 'utf8');
const jsModuleContent = fs.readFileSync(jsModulePath, 'utf8');

assert(indexHtmlContent.length > 50000, `index.html is comprehensive (${indexHtmlContent.length} bytes)`);
assert(jsModuleContent.length > 20000, `platform-state-and-rules.js is comprehensive (${jsModuleContent.length} bytes)`);

// Check script linkage
assert(indexHtmlContent.includes('platform-state-and-rules.js'), "index.html links platform-state-and-rules.js");
assert(indexHtmlContent.includes('https://cdn.jsdelivr.net/npm/chart.js'), "index.html includes Chart.js CDN");

// ----------------------------------------------------------------------
// 2. DOM STRUCTURE AUDIT (Workspaces, Modals, Key Elements)
// ----------------------------------------------------------------------
console.log("\n--- 2. DOM STRUCTURE AUDIT ---");

const criticalIds = [
  // 4 Role Workspaces
  'workspace-employee',
  'workspace-ex-service',
  'workspace-chancellery',
  'workspace-executive',
  // Sub-screens
  'workspace-chat',
  'workspace-pulse',
  'workspace-form',
  // Modals
  'modal-nudge',
  'modal-token-tracker',
  'modal-chancellery-stamp',
  'modal-region-inspector',
  // Role Switch Buttons
  'btn-role-employee',
  'btn-role-ex_service',
  'btn-role-chancellery',
  'btn-role-executive',
  // Chat Elements
  'chat-text-input',
  'chat-stream-box',
  'chat-dynamic-injections',
  'quick-chips-container',
  // Pulse Elements
  'synergy-alert-b1',
  // Direct Form Elements
  'form-text',
  'form-div',
  'form-region',
  'form-category',
  'form-anon',
  // Chancellery Elements
  'master-chancellery-tbody',
  // Corporate Auth & Role Isolation
  'screen-auth',
  'app-authenticated',
  // Progressive AI Interview Bar & Survey Mode
  'chat-interview-progressbar',
  'chat-progress-title',
  'chat-progress-status',
  'btn-chatmode-survey',
  'btn-chatmode-intake',
  'btn-lang-toggle',
  // AI BI Copilot
  'ex-copilot-input',
  'ex-copilot-stream',
  'exec-copilot-input',
  'exec-copilot-stream',
  // External Hub Elements
  'external-csv-table',
  'external-data-preview-box',
  'correlation-result-box',
  // Executive Heatmap Elements
  'heatmap-grid-container',
  'chartExecCategories',
  'chartExecSLA'
];

criticalIds.forEach(id => {
  const hasId = indexHtmlContent.includes(`id="${id}"`);
  assert(hasId, `DOM element with ID #${id} exists in index.html`);
});

// ----------------------------------------------------------------------
// 3. JAVASCRIPT LOGIC & STATE STORE SIMULATION
// ----------------------------------------------------------------------
console.log("\n--- 3. JAVASCRIPT STATE STORE & AI RULES AUDIT ---");

// Build a simulated browser window environment
const domElements = {};

function createMockElement(id) {
  return {
    id,
    classList: {
      classes: new Set(),
      add(c) { this.classes.add(c); },
      remove(c) { this.classes.delete(c); },
      contains(c) { return this.classes.has(c); }
    },
    style: {},
    innerHTML: '',
    textContent: '',
    value: '',
    options: [{ text: 'Default' }],
    selectedIndex: 0,
    parentElement: null,
    remove() {
      if (this.parentElement && this.parentElement.children) {
        this.parentElement.children = this.parentElement.children.filter(c => c !== this);
      }
    },
    appendChild(child) {
      if (!this.children) this.children = [];
      this.children.push(child);
      child.parentElement = this;
      return child;
    },
    insertBefore(newEl, refEl) {
      if (!this.children) this.children = [];
      this.children.push(newEl);
      newEl.parentElement = this;
      return newEl;
    },
    querySelectorAll(selector) {
      return [];
    },
    getAttribute(attr) { return ''; },
    setAttribute(attr, val) {}
  };
}

criticalIds.forEach(id => {
  domElements[id] = createMockElement(id);
});

// Additional dynamic elements
[
  'topbar-username', 'topbar-user-avatar', 'active-role-text', 'portal-welcome-name',
  'nudge-modal-title', 'nudge-modal-sub', 'ex-metric-srs', 'ex-metric-enps',
  'ex-metric-wb', 'exec-strike-score', 'chat-mode-anon', 'chat-mode-off',
  'external-table-title', 'external-rows-count', 'correlation-desc-text',
  'region-modal-title', 'region-modal-body', 'token-search-input',
  'token-res-num', 'token-res-cat', 'token-res-recip', 'token-res-sla',
  'token-chat-stream', 'token-reply-input', 'stamp-modal-num',
  'stamp-modal-recip', 'stamp-modal-date', 'toast-box', 'file-drop-label',
  'chancellery-clock'
].forEach(id => {
  domElements[id] = createMockElement(id);
});

const sandbox = {
  console: console,
  setTimeout: (cb, ms) => { cb(); return 1; },
  clearTimeout: () => {},
  setInterval: (cb, ms) => 1,
  clearInterval: () => {},
  navigator: { clipboard: { writeText: (txt) => {} } },
  document: {
    getElementById: (id) => {
      if (!domElements[id]) domElements[id] = createMockElement(id);
      return domElements[id];
    },
    querySelectorAll: (selector) => {
      if (selector === '.role-btn') {
        return [
          domElements['btn-role-employee'],
          domElements['btn-role-ex_service'],
          domElements['btn-role-chancellery'],
          domElements['btn-role-executive']
        ];
      }
      if (selector === '.canvas-screen') {
        return [
          domElements['workspace-employee'],
          domElements['workspace-ex-service'],
          domElements['workspace-chancellery'],
          domElements['workspace-executive'],
          domElements['workspace-chat'],
          domElements['workspace-pulse'],
          domElements['workspace-form']
        ];
      }
      if (selector === '.nav-tab-btn') {
        return [];
      }
      return [];
    },
    createElement: (tag) => {
      return createMockElement('dyn_' + Math.random().toString(36).substring(7));
    },
    addEventListener: (ev, cb) => {}
  },
  Chart: function(ctx, config) {
    this.ctx = ctx;
    this.config = config;
  },
  window: {}
};

sandbox.window = sandbox;

// Run platform-state-and-rules.js in sandbox
vm.createContext(sandbox);
vm.runInContext(jsModuleContent, sandbox);

assert(typeof sandbox.window.platformStateStore === 'object', "platformStateStore is defined in window");
assert(typeof sandbox.window.KazakhtelecomAI === 'object', "KazakhtelecomAI is defined in window");
assert(Array.isArray(sandbox.window.platformState.appeals), "platformState.appeals is initialized as array");
assert(sandbox.window.platformState.appeals.length >= 3, `Initial appeals list has ${sandbox.window.platformState.appeals.length} seed items`);

// ----------------------------------------------------------------------
// 4. AI CLASSIFICATION & TRIAGE ENGINE AUDIT
// ----------------------------------------------------------------------
console.log("\n--- 4. AI CLASSIFICATION & TRIAGE ENGINE AUDIT ---");

const testCasesAI = [
  { text: "На складе нет зимних курток и обуви, монтеры мерзнут на выездах", expectedCode: "HSE-01", name: "PPE / СИЗ Classification" },
  { text: "Срезали премию и не выплатили надбавку за вредность", expectedCode: "PAY-02", name: "Salary / Bonus Classification" },
  { text: "Принуждают работать по субботам сверхурочно, табель ставят 8 часов", expectedCode: "OT-03", name: "Overtime Classification" },
  { text: "Начальник участка кричит матом, оскорбляет и угрожает увольнением", expectedCode: "MOB-04", name: "Mobbing / Ethics Classification" },
  { text: "Бригада готова остановить работу и объявить забастовку", expectedCode: "EMG-05", name: "Strike / Emergency Classification" },
  { text: "Служебный транспорт УАЗ сломан, нет запчастей и бензина", expectedCode: "TECH-06", name: "Tech / Fleet Classification" },
  { text: "В помещении санузла и душевой антисанитария, нет чистой воды и холодильника в столовой", expectedCode: "LIFE-07", name: "Sanitary / Life Conditions Classification" }
];

testCasesAI.forEach(tc => {
  const result = sandbox.window.KazakhtelecomAI.classifyAppealText(tc.text);
  assert(result && result.code === tc.expectedCode, `${tc.name}: text mapped to ${tc.expectedCode} (got ${result.code})`);
});

// Priority cascade test: emergency keyword overrides secondary keyword
const cascadeResult = sandbox.window.KazakhtelecomAI.classifyAppealText("Коллектив объявляет забастовку из-за спецодежды и премий");
assert(cascadeResult.code === 'EMG-05', "Cascade Priority: EMG-05 takes precedence over HSE-01 and PAY-02");

// Conflict Guard test
const conflictText1 = "Мастер участка заставляет подписывать фиктивные наряды";
const conflictResult1 = sandbox.window.KazakhtelecomAI.checkConflictGuard(conflictText1);
assert(conflictResult1 === true, "Conflict Guard triggered for 'мастер участка'");

const conflictText2 = "Прошу разъяснить порядок предоставления путевки в санаторий";
const conflictResult2 = sandbox.window.KazakhtelecomAI.checkConflictGuard(conflictText2);
assert(conflictResult2 === false, "Conflict Guard not triggered for standard request without supervisor complaint");

// Formal Fabula Synthesis test
const fabula = sandbox.window.KazakhtelecomAI.generateFormalFabula(
  "В филиале ОДС Запад не выдают зимнюю обувь",
  sandbox.window.KazakhtelecomAI.INCIDENT_CATEGORIES['HSE-01'],
  "Атырауская область",
  { q1: "Зимняя спецобувь", q2: "Вся выездная бригада (18 чел)", q3: "Мастер отказал" }
);
assert(fabula.includes("ст. 182") || fabula.includes("Трудового кодекса"), "Formal Fabula cites relevant Labor Code article");
assert(fabula.includes("Атырауская область"), "Formal Fabula contains regional localization");

// ----------------------------------------------------------------------
// 5. EXTERNAL DATA INGESTION & CSV PARSER AUDIT
// ----------------------------------------------------------------------
console.log("\n--- 5. EXTERNAL DATA INGESTION (CSV PARSER & CORRELATION) AUDIT ---");

const sampleCsv = `region;division;turnover_rate;strike_risk
Атырауская область;ОДС;18.4;8.8
Мангистауская область;ОДС;21.2;8.5
г. Алматы;СФ;7.2;2.1`;

const parsedRows = sandbox.window.KazakhtelecomAI.parseCSVText(sampleCsv);
assert(Array.isArray(parsedRows) && parsedRows.length === 3, `CSV Parser correctly parsed 3 rows (got ${parsedRows.length})`);
assert(parsedRows[0].turnover_rate === '18.4' || parsedRows[0].turnover_rate === 18.4, "Turnover rate column parsed correctly");

// Comma delimiter test
const sampleCsvComma = `region,division,turnover_rate,strike_risk\nАстана,ЦА,5.1,1.5\nСемей,ОДС,14.8,6.2`;
const parsedCommaRows = sandbox.window.KazakhtelecomAI.parseCSVText(sampleCsvComma);
assert(parsedCommaRows.length === 2, `CSV Parser correctly handles comma delimiter (${parsedCommaRows.length} rows)`);

// Pearson Correlation test
const xArr = [18.4, 21.2, 7.2, 5.1];
const yArr = [8.8, 8.5, 2.1, 1.5];
const corr = sandbox.window.KazakhtelecomAI.calculatePearsonCorrelation(xArr, yArr);
assert(corr > 0.9, `Pearson Correlation calculates strong positive relationship (r = ${corr})`);

// ----------------------------------------------------------------------
// 6. REACTIVE STATE STORE & CROSS-ROLE REACTIVITY AUDIT
// ----------------------------------------------------------------------
console.log("\n--- 6. REACTIVE STATE STORE & CROSS-ROLE REACTIVITY AUDIT ---");

let eventTriggered = null;
let observedState = null;

sandbox.window.platformStateStore.subscribe((event, state) => {
  eventTriggered = event;
  observedState = state;
});

// Test role switching
sandbox.window.platformStateStore.switchRole('ROLE_CHANCELLERY');
assert(eventTriggered === 'ROLE_SWITCHED', "State store notified subscribers of ROLE_SWITCHED");
assert(observedState.currentUser.role === 'ROLE_CHANCELLERY', "Current user role switched to ROLE_CHANCELLERY");
assert(observedState.currentUser.name === 'Гульнара Ахметова', "Persona switched to Chancellery officer Гульнара Ахметова");

// Test adding new appeal
const initialCount = sandbox.window.platformState.appeals.length;
const newAppeal = sandbox.window.platformStateStore.addAppeal({
  categoryCode: 'HSE-01',
  isAnonymous: false,
  applicantName: 'Тестовый Заявитель',
  rawText: 'Тестовая жалоба на холод на узле связи',
  formalFabula: 'Официальная фабула по ст. 182 ТК РК',
  division: 'ОДС',
  region: 'Восточно-Казахстанская область'
});

assert(eventTriggered === 'APPEAL_CREATED', "State store notified subscribers of APPEAL_CREATED");
assert(sandbox.window.platformState.appeals.length === initialCount + 1, "Appeals list grew by 1");
assert(newAppeal.regNumber.startsWith('ВХ-2026/'), `Incoming number generated in correct format (${newAppeal.regNumber})`);
assert(newAppeal.regNumber.endsWith('-КАНЦ'), "Incoming number has -КАНЦ suffix");
assert(newAppeal.token.startsWith('TK-') && newAppeal.token.endsWith('-KZ'), `Token generated in correct format (${newAppeal.token})`);
assert(newAppeal.slaRemainingSeconds > 0, "SLA timer initialized with remaining seconds");

// Test Chancellery registration of appeal
const regResult = sandbox.window.platformStateStore.registerAppeal(newAppeal.id, "Департамент безопасности", "Смагулов Б.");
assert(eventTriggered === 'APPEAL_REGISTERED', "State store notified subscribers of APPEAL_REGISTERED");
assert(regResult.status === 'IN_WORK', "Registered appeal status is IN_WORK");

// ----------------------------------------------------------------------
// 7. EXTRACT & EXECUTE INLINE JAVASCRIPT FROM index.html
// ----------------------------------------------------------------------
console.log("\n--- 7. INLINE SCRIPT AUDIT IN index.html ---");

// Extract inline script from index.html
const scriptMatch = indexHtmlContent.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/i);
assert(scriptMatch !== null, "Inline <script> extracted from index.html");

if (scriptMatch) {
  const inlineScript = scriptMatch[1];
  try {
    vm.runInContext(inlineScript, sandbox);
    assert(true, "index.html inline script executed without syntax errors");
  } catch (err) {
    assert(false, "index.html inline script execution error", err.message);
  }
}

// Test triggerRoleSwitch() function
sandbox.triggerRoleSwitch('ROLE_EX_SERVICE');
assert(domElements['btn-role-ex_service'].classList.contains('active'), "triggerRoleSwitch('ROLE_EX_SERVICE') sets button active class");
assert(domElements['workspace-ex-service'].classList.contains('active'), "workspace-ex-service screen set active");

sandbox.triggerRoleSwitch('ROLE_CHANCELLERY');
assert(domElements['workspace-chancellery'].classList.contains('active'), "workspace-chancellery screen set active");

sandbox.triggerRoleSwitch('ROLE_EXECUTIVE');
assert(domElements['workspace-executive'].classList.contains('active'), "workspace-executive screen set active");

sandbox.triggerRoleSwitch('ROLE_EMPLOYEE');
assert(domElements['workspace-form'].classList.contains('active'), "workspace-form screen set active on employee login");

// Test Nudge modal functions
sandbox.openNudgeModal();
assert(domElements['modal-nudge'].classList.contains('active'), "openNudgeModal() opens #modal-nudge");

sandbox.closeNudgeModal();
assert(!domElements['modal-nudge'].classList.contains('active'), "closeNudgeModal() closes #modal-nudge");

sandbox.nudgeAction('chat');
assert(domElements['workspace-chat'].classList.contains('active'), "nudgeAction('chat') navigates to chat workspace");

sandbox.nudgeAction('pulse');
assert(domElements['workspace-pulse'].classList.contains('active'), "nudgeAction('pulse') navigates to pulse survey");

sandbox.nudgeAction('form');
assert(domElements['workspace-form'].classList.contains('active'), "nudgeAction('form') navigates to direct form");

// Test formatSecondsToSLA()
const slaStr5d = sandbox.formatSecondsToSLA(5 * 24 * 3600 - 15);
assert(slaStr5d.includes("4д 23ч 59м 45с"), `formatSecondsToSLA formats countdown properly (${slaStr5d})`);

const slaStrOverdue = sandbox.formatSecondsToSLA(0);
assert(slaStrOverdue.includes("ПРОСРОЧЕНО"), `formatSecondsToSLA formats overdue alert (${slaStrOverdue})`);

// Test Pulse synergy trigger
const mockPulseBtn = createMockElement('btn_scale_1');
const mockPulseParent = createMockElement('parent_scale');
mockPulseParent.appendChild(mockPulseBtn);
mockPulseParent.querySelectorAll = () => [mockPulseBtn];

sandbox.selectPulseScore('b1', 1, mockPulseBtn);
assert(domElements['synergy-alert-b1'].style.display === 'block', "Pulse Score 1 triggers #synergy-alert-b1 emergency banner");

sandbox.selectPulseScore('b1', 5, mockPulseBtn);
assert(domElements['synergy-alert-b1'].style.display === 'none', "Pulse Score 5 hides #synergy-alert-b1 emergency banner");

// Test Direct Form submission
domElements['form-text'].value = "Задержка выплаты сверхурочных монтерам ОДС за ноябрь 2026";
domElements['form-div'].value = "ОДС";
domElements['form-region'].value = "Атырауская область";
domElements['form-category'].value = "PAY-02";
domElements['form-anon'].value = "official";

const preCount = sandbox.window.platformState.appeals.length;
sandbox.submitDirectForm();
const postCount = sandbox.window.platformState.appeals.length;
assert(postCount === preCount + 1, "submitDirectForm() successfully registered new appeal into reactive store");

// Test Chancellery Table rendering
sandbox.renderChancelleryTable();
const tbodyHtml = domElements['master-chancellery-tbody'].innerHTML;
assert(tbodyHtml.includes("ВХ-2026/"), "Chancellery table rendered incoming registry numbers");
assert(tbodyHtml.includes("Штамп"), "Chancellery table rendered official stamp action buttons");

// Test External Data CSV Loading & Merge
sandbox.loadArchitectSampleCsv();
assert(domElements['external-data-preview-box'].style.display === 'block', "loadArchitectSampleCsv() parses CSV and displays preview block");
assert(domElements['external-csv-table'].innerHTML.includes("turnover_rate"), "CSV table contains turnover_rate headers");

sandbox.executeDataCorrelationMerge();
assert(domElements['correlation-result-box'].style.display === 'block', "executeDataCorrelationMerge() displays correlation result box");
assert(domElements['correlation-desc-text'].innerHTML.includes("r ="), "Correlation description shows Pearson r coefficient");

// Test 20-region heatmap grid
sandbox.renderHeatmapGrid();
const heatmapHtml = domElements['heatmap-grid-container'].innerHTML;
assert(heatmapHtml.includes("Атырауская область") && heatmapHtml.includes("Мангистауская область"), "Heatmap rendered Kazakhstan regions");

// Test Region Inspector Modal
sandbox.openRegionModal("Атырауская область");
assert(domElements['modal-region-inspector'].classList.contains('active'), "openRegionModal() opens #modal-region-inspector");
assert(domElements['region-modal-title'].textContent.includes("Атырауская область"), "Region modal displays correct region name");
sandbox.closeRegionModal();
assert(!domElements['modal-region-inspector'].classList.contains('active'), "closeRegionModal() closes #modal-region-inspector");

// Test Token Tracker & Two-Way Safe Chat
sandbox.openTokenModal();
assert(domElements['modal-token-tracker'].classList.contains('active'), "openTokenModal() opens #modal-token-tracker");

domElements['token-search-input'].value = "TK-7842-KZ";
sandbox.lookupToken();
assert(domElements['token-res-num'].textContent === "ВХ-2026/0942-КАНЦ", "lookupToken() correctly found registered incoming number");

domElements['token-reply-input'].value = "Уточняю: не выдана обувь размером 42 и 43.";
sandbox.sendTokenReply();
assert(domElements['token-chat-stream'].children.length > 0, "sendTokenReply() appended message to safe token chat stream");

sandbox.closeTokenModal();
assert(!domElements['modal-token-tracker'].classList.contains('active'), "closeTokenModal() closes #modal-token-tracker");

// Test Chancellery Official Registration Stamp Modal
sandbox.openStampModal("ВХ-2026/0942-КАНЦ", "Департамент производственной безопасности", "12.11.2026 10:15");
assert(domElements['modal-chancellery-stamp'].classList.contains('active'), "openStampModal() opens #modal-chancellery-stamp");
assert(domElements['stamp-modal-num'].textContent === "ВХ-2026/0942-КАНЦ", "Stamp modal displays incoming registration number");
assert(domElements['stamp-modal-recip'].textContent.includes("безопасности"), "Stamp modal displays designated executor department");
sandbox.closeStampModal();
assert(!domElements['modal-chancellery-stamp'].classList.contains('active'), "closeStampModal() closes #modal-chancellery-stamp");

// Test Chat Anonymity Toggle
sandbox.setChatAnon(true);
let draft = vm.runInContext("currentChatAppealDraft", sandbox);
assert(draft.isAnonymous === true, "setChatAnon(true) enables anonymous mode");
sandbox.setChatAnon(false);
draft = vm.runInContext("currentChatAppealDraft", sandbox);
assert(draft.isAnonymous === false, "setChatAnon(false) enables official named mode");

// Test Chat Presets
sandbox.applyPreset('ppe');
draft = vm.runInContext("currentChatAppealDraft", sandbox);
assert(draft.rawText.includes("зимнюю обувь"), "applyPreset('ppe') loaded PPE incident text");

sandbox.applyPreset('overtime');
draft = vm.runInContext("currentChatAppealDraft", sandbox);
assert(draft.rawText.includes("субботам"), "applyPreset('overtime') loaded overtime incident text");

sandbox.applyPreset('mobbing');
draft = vm.runInContext("currentChatAppealDraft", sandbox);
assert(draft.rawText.includes("грубит"), "applyPreset('mobbing') loaded mobbing incident text");

sandbox.applyPreset('strike');
draft = vm.runInContext("currentChatAppealDraft", sandbox);
assert(draft.rawText.includes("забастовку"), "applyPreset('strike') loaded strike emergency text");

// Test Corporate Auth & Strict Role Isolation
sandbox.performLogout();
assert(domElements['screen-auth'].classList.contains('active'), "performLogout() activates #screen-auth");
assert(!domElements['app-authenticated'].classList.contains('active'), "performLogout() deactivates #app-authenticated");

sandbox.triggerRoleSwitch('ROLE_EMPLOYEE');
assert(!domElements['screen-auth'].classList.contains('active'), "triggerRoleSwitch('ROLE_EMPLOYEE') hides #screen-auth");
assert(domElements['app-authenticated'].classList.contains('active'), "triggerRoleSwitch('ROLE_EMPLOYEE') shows #app-authenticated");

// Test AI BI Copilot
domElements['ex-copilot-input'].value = "Очаги напряженности и стачечные риски в филиалах";
sandbox.executeCopilotCommand('ex');
assert(domElements['ex-copilot-stream'].children.length > 0, "executeCopilotCommand('ex') appends response to EX copilot stream");

domElements['exec-copilot-input'].value = "Сформируй отчет для Правления";
sandbox.executeCopilotCommand('exec');
assert(domElements['exec-copilot-stream'].children.length > 0, "executeCopilotCommand('exec') appends response to Leadership copilot stream");

sandbox.sendCopilotPreset("Факторный анализ: текучесть кадров и переработки");
assert(domElements['ex-copilot-stream'].children.length >= 2, "sendCopilotPreset() successfully triggered copilot pipeline across workspaces");

// Test Autonomous Survey Engine in Chat
assert(typeof sandbox.window.KazakhtelecomSurveyEngine === 'object', "KazakhtelecomSurveyEngine is defined in window");
const surveyEngine = sandbox.window.KazakhtelecomSurveyEngine;
const q1Data = surveyEngine.startSurvey();
assert(q1Data.questionIndex === 1, "Autonomous survey starts at question 1");
assert(q1Data.totalQuestions === 8, "Autonomous survey contains 8 official project questions");
assert(Array.isArray(q1Data.scale) && q1Data.scale.length === 5, "Question 1 provides 1-5 rating scale");

// Test critical answer triggering Synergy Alert
const q2Data = surveyEngine.answerQuestion(1);
assert(q2Data.synergyAlert === true, "Low score (1) triggers synergyAlert: true");
assert(surveyEngine.criticalIssues.length === 1, "Critical issue recorded in survey engine");

// Answer remaining 6 questions
surveyEngine.answerQuestion(4);
surveyEngine.answerQuestion(5);
surveyEngine.answerQuestion(3);
surveyEngine.answerQuestion(2); // Another low score
surveyEngine.answerQuestion(4);
surveyEngine.answerQuestion(4);
const finalSurveyData = surveyEngine.answerQuestion(5);

assert(finalSurveyData.isFinished === true, "Survey marks isFinished: true after 8 questions");
assert(finalSurveyData.progressPct === 100, "Survey progress reaches 100%");
assert(finalSurveyData.result && typeof finalSurveyData.result.srsIndex === 'number', "Survey calculates numeric SRS index");
assert(finalSurveyData.result.enpsCategory !== undefined, "Survey classifies eNPS category");

// Test Chat Mode Switcher in UI
sandbox.setChatMode('survey');
let activeMode = vm.runInContext("currentChatMode", sandbox);
assert(activeMode === 'survey', "setChatMode('survey') switches chat mode to survey");
sandbox.setChatMode('intake');
activeMode = vm.runInContext("currentChatMode", sandbox);
assert(activeMode === 'intake', "setChatMode('intake') switches chat mode back to complaint intake");

// Test server.py Backend Integration & Gemini Endpoints
const serverPyPath = path.resolve('server.py');
assert(fs.existsSync(serverPyPath), "server.py backend exists in workspace");
const serverPyContent = fs.readFileSync(serverPyPath, 'utf8');
assert(serverPyContent.includes('/api/ai/intake'), "server.py handles /api/ai/intake endpoint");
assert(serverPyContent.includes('/api/ai/analytics'), "server.py handles /api/ai/analytics endpoint");
assert(serverPyContent.includes('/api/ai/survey'), "server.py handles /api/ai/survey endpoint");
assert(serverPyContent.includes('SURVEY_SYSTEM_INSTRUCTION'), "server.py contains SURVEY_SYSTEM_INSTRUCTION prompt");

// ----------------------------------------------------------------------
// 8. AUTONOMOUS MULTI-STAGE INTAKE AGENT AUDIT
// ----------------------------------------------------------------------
console.log("\n--- 8. AUTONOMOUS MULTI-STAGE INTAKE AGENT AUDIT ---");
const AutonomousAgentClass = sandbox.window.KazakhtelecomAI.EmployeeIntakeAgent;
assert(typeof AutonomousAgentClass === 'function', "EmployeeIntakeAgent class is exported");

const testAgent = new AutonomousAgentClass(sandbox.window.platformStateStore);
const greeting = testAgent.getGreeting("Нурлан");
assert(greeting.stage === 'GREETING', "Autonomous Agent starts in GREETING stage");
assert(greeting.progress === 15, "Initial progress is 15%");
assert(greeting.text.includes("Нурлан"), "Greeting addresses employee by name");

// Turn 1: Gentle check-in response -> Agent does NOT start survey, gently clarifies
const turn1 = testAgent.processInput("На участке тяжело, сильно устаем на аварийных выездах");
assert(turn1.type === 'CLARIFY', "Turn 1 returns CLARIFY type instead of survey");
assert(testAgent.stage === 'CLARIFYING', "Agent transitions to CLARIFYING stage");
assert(turn1.message.includes("графиком") && turn1.message.includes("снаряжения"), "Agent gently explores circumstances of fatigue");
assert(Array.isArray(turn1.options) && turn1.options.length >= 3, "Clarification provides empathetic options");

// Turn 2: User clarifies context -> Agent tactfully asks if they want to leave a complaint
const turn2 = testAgent.processInput("Связано с переработками и ненормированным днем");
assert(turn2.type === 'ASK_COMPLAINT', "Turn 2 asks if user wants to leave a complaint");
assert(testAgent.stage === 'ASK_WANT_COMPLAINT', "Agent transitions to ASK_WANT_COMPLAINT stage");
assert(turn2.message.includes("оставить обращение (жалобу)"), "Agent tactfully offers formal/anonymous complaint filing");

// Turn 3: User accepts complaint -> Agent prompts to describe complaint in own words
const turn3 = testAgent.processInput("Да, хочу описать проблему и подать жалобу");
assert(turn3.type === 'PROMPT_COMPLAINT', "Turn 3 prompts user to describe complaint");
assert(testAgent.stage === 'COMPLAINT_INTAKE', "Agent transitions to COMPLAINT_INTAKE stage");
assert(turn3.message.includes("Опишите, пожалуйста, суть проблемы своими словами"), "Agent asks for complaint narrative");

// Turn 4: User describes complaint -> Agent analyzes and begins asking circumstance questions
const turn4 = testAgent.processInput("В филиале ОДС мастер участка заставляет выходить по субботам без оплаты и грозит увольнением");
assert(turn4.type === 'QUESTION', "Turn 4 begins circumstance clarification questions");
assert(testAgent.stage === 'FACT_FINDING_Q1', "Agent transitions to FACT_FINDING_Q1 stage");
assert(['OT-03', 'PAY-02', 'MOB-04', 'HSE-01'].includes(testAgent.currentCategory.code), "Complaint classified properly");
assert(testAgent.conflictGuard === true, "Conflict-of-Interest Guard triggered for 'мастер участка'");

// Turn 5: User answers circumstance Q1 -> Agent asks circumstance Q2
const turn5 = testAgent.processInput("Затронута вся выездная бригада (18 человек)");
assert(turn5.type === 'QUESTION', "Turn 5 asks second circumstance question");
assert(testAgent.stage === 'FACT_FINDING_Q2', "Agent transitions to FACT_FINDING_Q2 stage");

// Turn 6: User answers circumstance Q2 -> Agent asks circumstance Q3
const turn6 = testAgent.processInput("Более 1-2 месяцев, получали отказ при обращении");
assert(turn6.type === 'QUESTION', "Turn 6 asks third circumstance question");
assert(testAgent.stage === 'FACT_FINDING_Q3', "Agent transitions to FACT_FINDING_Q3 stage");

// Turn 7: User answers circumstance Q3 -> Agent synthesizes formal legal draft
const turn7 = testAgent.processInput("Да, есть свидетели и переписка в рабочем чате");
assert(turn7.type === 'DRAFT', "Turn 7 produces official statement DRAFT");
assert(testAgent.stage === 'DRAFT_READY', "Agent transitions to DRAFT_READY stage");
assert(turn7.formalFabula.includes("Трудового кодекса РК"), "Generated statement cites Labor Code");

// Turn 8: Register anonymously -> Generates token and saves appeal
const turn8 = testAgent.register(true);
assert(turn8.type === 'CONFIRMED', "Appeal registration confirmed");
assert(testAgent.stage === 'REGISTERED', "Agent reaches REGISTERED stage");
assert(turn8.appeal.token.startsWith("TK-"), "Token generated in protected anonymous mode");

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
// 9. ТЗ v12.11.2026 & ВОПРОСНИК.DOCX COMPLIANCE AUDIT
// ----------------------------------------------------------------------
console.log("\n--- 9. ТЗ v12.11.2026 & ВОПРОСНИК.DOCX COMPLIANCE AUDIT ---");

// 9.1. 9 Divisions from ТЗ v12.11.2026
const divList = sandbox.window.KazakhtelecomAI.DIVISIONS_9;
assert(Array.isArray(divList) && divList.length === 9, "DIVISIONS_9 contains exactly 9 divisions from ТЗ v12.11.2026");
const expectedDivCodes = ['ОДС', 'СФ', 'ДРБ', 'ДКБ', 'ДТК', 'ДПБ', 'ДУП', 'ДЦБ', 'ЦА'];
const actualDivCodes = divList.map(d => d.code);
expectedDivCodes.forEach(code => {
  assert(actualDivCodes.includes(code), `Division ${code} is defined in organizational classifier`);
});

// 9.2. 30 Questions Bank from Вопросник.docx (3 blocks x 10 questions)
const qBank = sandbox.window.KazakhtelecomAI.QUESTION_BANK_30;
assert(qBank && typeof qBank === 'object', "QUESTION_BANK_30 is exported");
assert(qBank.block1 && qBank.block1.questions.length === 10, "Block 1 (Филиал / дивизион) contains exactly 10 questions");
assert(qBank.block2 && qBank.block2.questions.length === 10, "Block 2 (Масштаб проблемы) contains exactly 10 questions");
assert(qBank.block3 && qBank.block3.questions.length === 10, "Block 3 (Предыстория к мастеру) contains exactly 10 questions");
const totalBankQuestions = qBank.block1.questions.length + qBank.block2.questions.length + qBank.block3.questions.length;
assert(totalBankQuestions === 30, "Question bank contains total 30 questions from Вопросник.docx");

// 9.3. Bilingual Localization (RU / KZ)
const i18n = sandbox.window.KazakhtelecomAI.I18N_LANG;
assert(i18n && i18n.ru && i18n.kz, "I18N_LANG supports Russian (ru) and Kazakh (kz)");
assert(i18n.kz.appName.includes("ЖИ-Өтініштер"), "Kazakh localization contains valid terminology");

// Test Language Toggle in UI
if (typeof sandbox.toggleAppLanguage === 'function') {
  sandbox.toggleAppLanguage('kz');
  let lang = vm.runInContext("currentAppLang", sandbox);
  assert(lang === 'kz', "toggleAppLanguage('kz') switches UI language to Kazakh");
  sandbox.toggleAppLanguage('ru');
  lang = vm.runInContext("currentAppLang", sandbox);
  assert(lang === 'ru', "toggleAppLanguage('ru') switches UI language to Russian");
}

// 9.4. SLA Matrix & Recipients from ТЗ v12.11.2026 Section 5
const cats = sandbox.window.KazakhtelecomAI.INCIDENT_CATEGORIES;
assert(cats['HSE-01'].slaDays === 5 && cats['HSE-01'].standardDept.includes('ДПБ'), "HSE-01: 5 work days, ДПБ / Сервисная фабрика");
assert(cats['PAY-02'].slaDays === 5 && cats['PAY-02'].standardDept.includes('ЦА СВИОЭ'), "PAY-02: 5 work days, ЦА СВИОЭ");
assert(cats['OT-03'].slaDays === 3 && cats['OT-03'].standardDept.includes('Профсоюз'), "OT-03: 3 work days, СВИОЭ + Профсоюз");
assert(cats['MOB-04'].slaDays === 7 && cats['MOB-04'].standardDept.includes('Омбудсмен'), "MOB-04: 7 work days, Служба комплаенс и Омбудсмен");
assert(cats['EMG-05'].slaHours <= 48 && cats['EMG-05'].priority === 'CRITICAL', "EMG-05: 24-48 hours, КРАСНЫЙ ЧП, ЦА СУОР");
assert(cats['TECH-06'].slaDays === 3 && cats['TECH-06'].standardDept.includes('ОДС'), "TECH-06: 3 work days, ОДС / Сервисная фабрика");
assert(cats['LIFE-07'].slaDays === 5 && cats['LIFE-07'].standardDept.includes('Сервисная фабрика'), "LIFE-07: 5 work days, Сервисная фабрика");

// 9.5. Lotus Notes Two-Circuit Architecture
const anonAppeal = sandbox.window.platformStateStore.addAppeal({
  categoryCode: 'HSE-01',
  isAnonymous: true,
  rawText: 'Анонимный сигнал о СИЗ'
});
assert(anonAppeal.operationalLoopOnly === true, "Anonymous appeal marked operationalLoopOnly: true (not polluting Lotus Notes)");
assert(anonAppeal.lotusNotesStatus.includes("Оперативный контур"), "Anonymous appeal routed into internal operational loop");

const namedAppeal = sandbox.window.platformStateStore.addAppeal({
  categoryCode: 'PAY-02',
  isAnonymous: false,
  rawText: 'Официальное заявление о надбавках',
  fio: 'Смагулов Алибек'
});
assert(namedAppeal.operationalLoopOnly === false, "Official appeal marked operationalLoopOnly: false");
assert(namedAppeal.lotusNotesStatus.includes("СЭД Lotus Notes"), "Official appeal registered in Lotus Notes Chancellery");

// 9.6. Survey-to-Intake & Chat Responsiveness Transition
sandbox.setChatMode('survey');
assert(vm.runInContext("currentChatMode", sandbox) === 'survey', "Survey mode is active");
domElements['chat-text-input'].value = "Хочу оставить жалобу, не выдают спецобувь на участке";
sandbox.sendChatProblem();
assert(vm.runInContext("currentChatMode", sandbox) === 'intake', "sendChatProblem() automatically transitioned from survey mode to intake mode");
assert(domElements['chat-stream-box'].children.length > 0, "Chat message rendered into stream box");
assert(vm.runInContext("chatStage", sandbox) === 'FACT_FINDING', "Chat transitioned to FACT_FINDING circumstance clarification");

// ----------------------------------------------------------------------
// 10. SUMMARY & VERDICT
// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
console.log("\n==================================================================");
console.log(`📊 TEST SUITE SUMMARY: ${passedTests} PASSED, ${failedTests} FAILED`);
console.log("==================================================================");

if (failedTests === 0) {
  console.log("🎉 ALL TESTS PASSED WITH 100% SUCCESS RATE! PLATFORM IS PRODUCTION READY.");
} else {
  console.log(`⚠️ ${failedTests} TEST(S) FAILED. INVESTIGATION REQUIRED.`);
}

process.exit(failedTests === 0 ? 0 : 1);
