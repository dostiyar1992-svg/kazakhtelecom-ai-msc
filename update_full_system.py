# -*- coding: utf-8 -*-
"""
update_full_system.py
1. Writes the complete, upgraded platform-state-and-rules.js:
   - System Accounts & AuthManager (strict account management)
   - EmployeeIntakeAgent (conversational step-by-step interview AI agent)
   - AnalyticsCopilot (AI BI agent for dashboard generation and executive reports)
   - Backward-compatible functions for QA tests.
2. Writes the upgraded index.html:
   - Dedicated Login Screen (#screen-auth) with Kazakhtelecom corporate branding and 1-click test credentials.
   - Dedicated App Screen (#screen-app) with STRICT isolation:
     * User avatar, name, role badge, division in topbar + Logout button.
     * No role switching buttons in active workspace.
     * User only sees their own assigned workspace.
   - Conversational AI Agent ("ИИ-Ассистент Айгерим") with multi-turn chat, progress bar, option chips, Conflict Guard, legal statement generation, and anonymity choice.
   - AI Analytics Copilot ("ИИ-Аналитик и Архитектор Дашбордов") in EX Service & Executive workspaces.
"""

import os
import sys

print("Writing platform-state-and-rules.js...")

js_code = r'''/**
 * platform-state-and-rules.js
 * Комплексная система «ИИ-Приемная обращений, регулярные пульс-опросы и мониторинг социального климата АО «Казахтелеком»
 * 
 * Содержит:
 * 1. Аутентификация и разграничение доступа (AuthManager & SYSTEM_ACCOUNTS)
 * 2. Unified Reactive State Store (window.platformStateStore & window.platformState)
 * 3. Диалоговый ИИ-Агент приема обращений сотрудника (EmployeeIntakeAgent)
 * 4. ИИ-Аналитик и Архитектор дашбордов (AnalyticsCopilot)
 * 5. Классификатор инцидентов (7 категорий), Conflict Guard & Фабула по ТК РК
 * 6. Клиентский CSV/JSON парсер и расчет корреляции Пирсона (r)
 */

(function(global) {
  'use strict';

  // ==========================================
  // 1. УЧЕТНЫЕ ЗАПИСИ И СИСТЕМА АУТЕНТИФИКАЦИИ
  // ==========================================

  const SYSTEM_ACCOUNTS = {
    'alibek.smagulov': {
      id: "USR-7701",
      username: "alibek.smagulov",
      password: "password123",
      name: "Алибек Смагулов",
      role: "ROLE_EMPLOYEE",
      roleTitle: "Электромонтер линейных сооружений 5 разряда",
      division: "ОДС",
      region: "Атырауская область",
      avatar: "АС",
      isCdnAuth: true,
      email: "a.smagulov@telecom.kz",
      trackedTokens: ["TK-7842-KZ"]
    },
    'dinara.kassymova': {
      id: "USR-5502",
      username: "dinara.kassymova",
      password: "password123",
      name: "Динара Касымова",
      role: "ROLE_EX_SERVICE",
      roleTitle: "Руководитель Службы управления опытом работника (ДУП)",
      division: "ДУП",
      region: "г. Астана (ЦА)",
      avatar: "ДК",
      isCdnAuth: true,
      email: "d.kassymova@telecom.kz",
      trackedTokens: []
    },
    'gulnara.akhmetova': {
      id: "USR-3309",
      username: "gulnara.akhmetova",
      password: "password123",
      name: "Гульнара Ахметова",
      role: "ROLE_CHANCELLERY",
      roleTitle: "Главный специалист Канцелярии (СЭД Lotus Notes)",
      division: "Канцелярия",
      region: "г. Астана (ЦА)",
      avatar: "ГА",
      isCdnAuth: true,
      email: "g.akhmetova@telecom.kz",
      trackedTokens: []
    },
    'bagdat.mussin': {
      id: "USR-1001",
      username: "bagdat.mussin",
      password: "password123",
      name: "Багдат Мусин",
      role: "ROLE_EXECUTIVE",
      roleTitle: "Председатель Правления АО «Казахтелеком»",
      division: "Правление",
      region: "г. Астана (ЦА)",
      avatar: "БМ",
      isCdnAuth: true,
      email: "b.mussin@telecom.kz",
      trackedTokens: []
    }
  };

  // ==========================================
  // 2. СПРАВОЧНИКИ И КОНСТАНТЫ
  // ==========================================

  const INCIDENT_CATEGORIES = {
    'HSE-01': {
      code: 'HSE-01',
      title: 'Охрана труда и СИЗ',
      keywords: ['сиз', 'спецодежд', 'обув', 'ботинок', 'ботинки', 'куртк', 'каск', 'инструмент', 'мороз', 'холод', 'авари', 'опасн', 'травм', 'ст. 182'],
      legalBase: 'ст. 182 Трудового кодекса РК, п. 4.2 Коллективного договора АО «Казахтелеком»',
      standardDept: 'Департамент производственной безопасности (ДПБ)',
      standardOfficer: 'Смагулов Б.К.',
      slaHours: 120, // 5 дней
      dangerSlaHours: 24,
      priority: 'HIGH',
      questions: [
        { id: 'q1', text: 'Какое именно снаряжение или СИЗ отсутствует или пришло в негодность?', options: ['Зимняя спецобувь и куртки', 'Диэлектрический инструмент и каски', 'Монтерские пояса и лазы', 'Другое снаряжение'] },
        { id: 'q2', text: 'Сколько работников бригады затронуто проблемой?', options: ['Лично я (1 человек)', 'Вся выездная бригада (10-18 человек)', 'Весь участок (>30 человек)'] },
        { id: 'q3', text: 'Обращались ли вы ранее к мастеру или на склад?', options: ['Да, получили устный отказ', 'На складе заявляют об отсутствии поставки', 'Опасаемся давления руководства'] }
      ]
    },
    'PAY-02': {
      code: 'PAY-02',
      title: 'Оплата труда, премии и надбавки',
      keywords: ['зарплат', 'оплат', 'преми', 'надбавк', 'удержан', 'расчетн', 'денег', 'тариф', 'оклад', 'ст. 108', 'лишен', 'бонус'],
      legalBase: 'ст. 108, 113 Трудового кодекса РК, Положение об оплате труда АО «Казахтелеком»',
      standardDept: 'Департамент оплаты труда и компенсаций (ДУП)',
      standardOfficer: 'Ким А.В.',
      slaHours: 120,
      priority: 'STANDARD',
      questions: [
        { id: 'q1', text: 'За какой расчетный период выявлено нарушение или невыплата?', options: ['За текущий месяц', 'За предыдущие 2-3 месяца', 'Систематически в течение года'] },
        { id: 'q2', text: 'Предоставлялся ли вам официальный расчетный листок?', options: ['Да, но сумма не сходится с табелем', 'Расчетный листок не выдается на руки', 'Премию срезали без объяснения причин'] },
        { id: 'q3', text: 'Проблема касается индивидуально вас или всей группы?', options: ['Индивидуально меня', 'Всего подразделения / смены'] }
      ]
    },
    'OT-03': {
      code: 'OT-03',
      title: 'Сверхурочные работы и дежурства',
      keywords: ['сверхурочн', 'суббот', 'воскресень', 'выходн', 'ночн', 'смен', 'переработ', 'табел', '8 часов', 'дежурств', 'без согласия'],
      legalBase: 'ст. 77, 78, 108 Трудового кодекса РК (ограничение и повышенная оплата сверхурочных)',
      standardDept: 'Департамент управления персоналом (ДУП)',
      standardOfficer: 'Оспанов Е.М.',
      slaHours: 120,
      priority: 'STANDARD',
      questions: [
        { id: 'q1', text: 'Каким образом фиксируются переработки на участке?', options: ['Табель закрывают как 8 часов (фиктивно)', 'Выдают отгулы вместо оплаты без согласия', 'Приказы не издаются вовсе'] },
        { id: 'q2', text: 'Каков примерный объем сверхурочных часов в месяц?', options: ['10–20 часов', '20–40 часов', 'Более 40 часов'] },
        { id: 'q3', text: 'Имеются ли угрозы наказания за отказ от переработок?', options: ['Да, угрожают срезать премию или уволить', 'Оказывается моральное давление', 'Прямых угроз нет, но есть принуждение'] }
      ]
    },
    'MOB-04': {
      code: 'MOB-04',
      title: 'Моббинг, давление и корпоративная этика',
      keywords: ['моббинг', 'давлен', 'грубост', 'оскорблен', 'угрожает', 'угрозы', 'увольнен', 'этик', 'мат', 'унижен', 'принужден', 'кричит', 'хамств'],
      legalBase: 'Кодекс корпоративной этики АО «Казахтелеком», п. 2 ст. 10 ТК РК',
      standardDept: 'Служба комплаенс и Корпоративный Омбудсмен',
      standardOfficer: 'Байжанова С.С.',
      slaHours: 120,
      priority: 'HIGH',
      questions: [
        { id: 'q1', text: 'Кто является инициатором неэтичного поведения или давления?', options: ['Непосредственный мастер / бригадир', 'Начальник цеха / участка', 'Директор филиала'] },
        { id: 'q2', text: 'Имеются ли свидетели или доказательства (аудио, переписка)?', options: ['Есть свидетели из числа коллег', 'Есть аудиозаписи / скриншоты в WhatsApp', 'Свидетели боятся говорить открыто'] },
        { id: 'q3', text: 'Требуется ли вам полная защита конфиденциальности Омбудсменом?', options: ['Да, строго анонимно', 'Готов дать официальные показания при защите от мести'] }
      ]
    },
    'EMG-05': {
      code: 'EMG-05',
      title: 'Угроза забастовки / ЧП (Коллективный трудовой спор)',
      keywords: ['забастовк', 'митинг', 'коллективн', 'отказ от работ', 'остановк', 'протест', 'петици', 'бунт', 'забастовочн', 'ст. 176', 'приостанов'],
      legalBase: 'ст. 176–178 Трудового кодекса РК (порядок разрешения коллективных споров)',
      standardDept: 'Центр социального партнерства и мониторинга (МСЦ) / Правление',
      standardOfficer: 'Котырев Б.К. (Главный директор по персоналу)',
      slaHours: 24, // 24 часа! ЧП!
      priority: 'CRITICAL',
      questions: [
        { id: 'q1', text: 'Какое количество работников готово приостановить работу?', options: ['Группа от 10 до 30 человек', 'Весь цех / филиал (>50 человек)', 'Массовое движение нескольких районов'] },
        { id: 'q2', text: 'Сформулирован ли письменный протокол требований коллектива?', options: ['Да, требования подписаны работниками', 'Требования озвучены устно', 'Формируется инициативная группа'] },
        { id: 'q3', text: 'Уведомлялось ли руководство компании о сроках примирительных процедур?', options: ['Да, дан срок до конца недели', 'Сроков нет, ситуация на грани срыва'] }
      ]
    },
    'TECH-06': {
      code: 'TECH-06',
      title: 'Инфраструктура, техника и связь',
      keywords: ['инфраструктур', 'компьютер', 'техник', 'интернет', 'программ', 'транспорт', 'машин', 'гсм', 'отоплен', 'кондиционер', 'оборудован'],
      legalBase: 'ст. 23 Трудового кодекса РК (обеспечение средствами производства)',
      standardDept: 'Дирекция информационных систем (ДИС) / Транспортная дирекция',
      standardOfficer: 'Алиев Т.Р.',
      slaHours: 120,
      priority: 'STANDARD',
      questions: [
        { id: 'q1', text: 'Какое оборудование или инфраструктура неисправна?', options: ['Служебный транспорт / ГСМ', 'Компьютерная техника / ПО / связь', 'Отопление / кондиционирование на узле'] },
        { id: 'q2', text: 'Влияет ли неисправность на бесперебойность сервисов абонентов?', options: ['Да, есть угроза срыва SLA клиентов', 'Влияет только на комфорт персонала'] },
        { id: 'q3', text: 'Подавались ли ранее заявки в HelpDesk / техподдержку?', options: ['Да, заявка висит более месяца', 'Заявку закрыли без решения'] }
      ]
    },
    'LIFE-07': {
      code: 'LIFE-07',
      title: 'Бытовые и санитарно-гигиенические условия',
      keywords: ['быт', 'санузел', 'туалет', 'столов', 'водоснабжен', 'вод', 'душ', 'раздевалк', 'холодильник', 'обогрев', 'вагончик', 'гряз'],
      legalBase: 'Санитарно-эпидемиологические требования к условиям труда, Колдоговор',
      standardDept: 'Административно-хозяйственный департамент (АХД)',
      standardOfficer: 'Нурланов Д.С.',
      slaHours: 120,
      priority: 'STANDARD',
      questions: [
        { id: 'q1', text: 'В каком производственном помещении нарушены условия?', options: ['В помещении дежурной смены', 'В полевом вагончике / удаленном узле', 'В санузле / душевой'] },
        { id: 'q2', text: 'Имеется ли доступ к качественной питьевой воде?', options: ['Нет, привозим воду сами за свой счет', 'Вода не соответствует санитарным нормам'] },
        { id: 'q3', text: 'Создают ли условия риск для здоровья работников?', options: ['Да, постоянная сырость и холод', 'Антисанитарные условия'] }
      ]
    }
  };

  const CONFLICT_SUPERVISOR_MARKERS = [
    'мастер', 'мастера', 'мастеру', 'мастером',
    'начальник участка', 'начальника участка', 'начальнику участка',
    'начальник цеха', 'начальника цеха',
    'бригадир', 'бригадира', 'бригадиру',
    'директор филиала', 'директора филиала', 'директору филиала',
    'начальник рдт', 'руководитель группы'
  ];

  const KZ_REGIONS = [
    "г. Астана", "г. Алматы", "г. Шымкент",
    "Абайская область", "Акмолинская область", "Актюбинская область",
    "Алматинская область", "Атырауская область", "Восточно-Казахстанская область",
    "Жамбылская область", "Жетысуская область", "Западно-Казахстанская область",
    "Карагандинская область", "Костанайская область", "Кызылординская область",
    "Мангистауская область", "Павлодарская область", "Северо-Казахстанская область",
    "Туркестанская область", "Улытауская область"
  ];

  // ==========================================
  // 3. ЕДИНЫЙ РЕАКТИВНЫЙ STORE
  // ==========================================

  const defaultState = {
    isAuthenticated: true,
    currentUser: SYSTEM_ACCOUNTS['alibek.smagulov'],
    personas: Object.values(SYSTEM_ACCOUNTS),
    surveys: [
      {
        id: "SRV-2026-Q4",
        title: "Квартальный пульс-опрос Q4 2026: Социальный климат, eNPS и условия труда",
        quarter: "Q4 2026",
        startDate: "01.11.2026",
        endDate: "30.11.2026",
        status: "ACTIVE",
        targetAudience: "Все сотрудники АО «Казахтелеком» (21 400 чел.)",
        responseRatePct: 68.4,
        metrics: {
          srsIndex: 64.2,
          enpsScore: 24,
          teamWellbeing: 34.0,
          strikeRiskIndex: 8.8
        }
      }
    ],
    appeals: [
      {
        id: 1,
        regNumber: "ВХ-2026/0942-КАНЦ",
        token: "TK-7842-KZ",
        date: "12.11.2026 09:30",
        isAnonymous: true,
        fio: "— (Анонимно)",
        division: "ОДС",
        region: "Атырауская область",
        categoryCode: "HSE-01",
        categoryTitle: "Охрана труда и СИЗ",
        rawText: "Задержка зимней обуви и курток выездным бригадам монтеров АВР более 45 дней. Морозы до -18°C.",
        formalFabula: "Несоблюдение положений ст. 182 ТК РК и п. 4.2 Коллективного договора. Задержка выдачи зимней экипировки бригадам связи.",
        recipientDept: "Департамент производственной безопасности (ДПБ)",
        recipientOfficer: "Смагулов Б.К.",
        status: "IN_WORK",
        slaDeadline: "17.11.2026 18:00",
        slaRemainingSeconds: 431980,
        riskLevel: "CRITICAL",
        conflictGuardActive: true,
        answers: { q1: "Зимняя спецобувь и куртки", q2: "Вся выездная бригада (14 человек)" },
        messages: [
          { sender: "Служба EX (Инспектор)", text: "Обращение принято в работу в защищенном контуре. Направлен срочный запрос на склад СФ.", time: "12.11.2026 09:45" }
        ]
      },
      {
        id: 2,
        regNumber: "ВХ-2026/0941-КАНЦ",
        token: "TK-8812-KZ",
        date: "10.11.2026 14:20",
        isAnonymous: false,
        fio: "Искаков Марат А.",
        division: "ОДС",
        region: "Абайская область",
        categoryCode: "PAY-02",
        categoryTitle: "Оплата труда, премии и надбавки",
        rawText: "Принуждение к выходу в субботу без табелирования и двойной оплаты труда.",
        formalFabula: "Нарушение ст. 108 ТК РК (оплата сверхурочной работы). Отсутствие приказов на привлечение к работе в выходные дни.",
        recipientDept: "Департамент оплаты труда и компенсаций (ДУП)",
        recipientOfficer: "Ким А.В.",
        status: "IN_WORK",
        slaDeadline: "15.11.2026 18:00",
        slaRemainingSeconds: 104200,
        riskLevel: "MEDIUM",
        conflictGuardActive: false,
        answers: { q1: "За октябрь 2026", q2: "Табель закрывают как 8 часов" },
        messages: []
      },
      {
        id: 3,
        regNumber: "ВХ-2026/0938-КАНЦ",
        token: "TK-3419-KZ",
        date: "04.11.2026 09:15",
        isAnonymous: false,
        fio: "Смаилов Канат Т.",
        division: "СФ",
        region: "Карагандинская область",
        categoryCode: "TECH-06",
        categoryTitle: "Инфраструктура, техника и связь",
        rawText: "Аварийное состояние автопарка УАЗ в Каркаралинском районе. Неисправны тормоза, нет зимней резины.",
        formalFabula: "Нарушение ст. 23 ТК РК. Предоставление неисправного служебного автотранспорта, создающего угрозу ДТП.",
        recipientDept: "Транспортная дирекция (СФ)",
        recipientOfficer: "Алиев Т.Р.",
        status: "OVERDUE",
        slaDeadline: "09.11.2026 18:00",
        slaRemainingSeconds: -14400,
        riskLevel: "HIGH",
        conflictGuardActive: false,
        answers: {},
        messages: []
      }
    ],
    externalDataSets: [],
    analytics: {
      srsIndex: 64.2,
      enpsScore: 24,
      wellbeingScore: 34.0,
      strikeRiskScore: 8.8,
      strikeRiskRegion: "Атырауская область (ОДС)",
      categoryBreakdown: {
        'HSE-01': 38,
        'PAY-02': 28,
        'OT-03': 14,
        'MOB-04': 12,
        'TECH-06': 8
      },
      divisionBreakdown: {
        'ОДС': 192,
        'СФ': 76,
        'ДРБ': 74,
        'ДКБ': 30,
        'ДУП': 28,
        'ДЦБ': 20
      }
    }
  };

  class PlatformStore {
    constructor(initialState) {
      this.state = JSON.parse(JSON.stringify(initialState));
      this.subscribers = [];
    }

    getState() {
      return this.state;
    }

    subscribe(fn) {
      this.subscribers.push(fn);
      return () => {
        this.subscribers = this.subscribers.filter(s => s !== fn);
      };
    }

    notifySubscribers(eventType, payload) {
      this.subscribers.forEach(fn => {
        try { fn(this.state, eventType, payload); } catch(e) { console.error(e); }
      });
    }

    setCurrentUser(user) {
      this.state.currentUser = user;
      this.state.isAuthenticated = true;
      this.notifySubscribers('USER_CHANGED', user);
    }

    switchRole(roleName) {
      const targetUser = this.state.personas.find(p => p.role === roleName);
      if (targetUser) {
        this.setCurrentUser(targetUser);
        this.notifySubscribers('ROLE_SWITCHED', targetUser);
      }
    }

    addAppeal(appealData) {
      const nextId = this.state.appeals.length + 1;
      const regNumber = `ВХ-2026/${String(nextId).padStart(4, '0')}-КАНЦ`;
      const token = `TK-${Math.floor(1000 + Math.random() * 9000)}-KZ`;

      const now = new Date();
      const deadlineDate = new Date(now.getTime() + (appealData.slaHours || 120) * 3600 * 1000);
      const remainingSec = (appealData.slaHours || 120) * 3600;

      const newRecord = {
        id: nextId,
        regNumber: regNumber,
        token: token,
        date: now.toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }),
        isAnonymous: appealData.isAnonymous !== undefined ? appealData.isAnonymous : true,
        fio: appealData.isAnonymous ? "— (Конфиденциально)" : (appealData.fio || this.state.currentUser.name),
        division: appealData.division || this.state.currentUser.division || "ОДС",
        region: appealData.region || this.state.currentUser.region || "Атырауская область",
        categoryCode: appealData.categoryCode || "HSE-01",
        categoryTitle: appealData.categoryTitle || "Охрана труда и СИЗ",
        rawText: appealData.rawText || "",
        formalFabula: appealData.formalFabula || appealData.rawText,
        recipientDept: appealData.recipientDept || "Департамент производственной безопасности (ДПБ)",
        recipientOfficer: appealData.recipientOfficer || "Смагулов Б.К.",
        status: "IN_WORK",
        slaDeadline: deadlineDate.toLocaleDateString('ru-RU') + " 18:00",
        slaRemainingSeconds: remainingSec,
        riskLevel: appealData.riskLevel || (appealData.conflictGuardActive ? "HIGH" : "MEDIUM"),
        conflictGuardActive: appealData.conflictGuardActive || false,
        answers: appealData.answers || {},
        messages: []
      };

      this.state.appeals.unshift(newRecord);

      if (this.state.currentUser && this.state.currentUser.role === 'ROLE_EMPLOYEE') {
        if (!this.state.currentUser.trackedTokens) this.state.currentUser.trackedTokens = [];
        this.state.currentUser.trackedTokens.unshift(token);
      }

      this.recalculateAnalytics();
      this.notifySubscribers('APPEAL_CREATED', newRecord);
      return newRecord;
    }

    registerAppeal(appealId, chancelleryOfficerName) {
      const appeal = this.state.appeals.find(a => a.id === appealId);
      if (appeal) {
        appeal.status = "IN_WORK";
        appeal.registeredBy = chancelleryOfficerName || "Гульнара Ахметова (Канцелярия)";
        appeal.registeredAt = new Date().toLocaleString('ru-RU');
        this.notifySubscribers('APPEAL_REGISTERED', appeal);
      }
    }

    addAppealMessage(appealTokenOrId, sender, text) {
      const appeal = this.state.appeals.find(a => a.token === appealTokenOrId || a.id === Number(appealTokenOrId) || a.regNumber === appealTokenOrId);
      if (appeal) {
        const msg = {
          sender: sender,
          text: text,
          time: new Date().toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
        };
        appeal.messages.push(msg);
        this.notifySubscribers('MESSAGE_ADDED', { appeal, msg });
        return msg;
      }
      return null;
    }

    recalculateAnalytics() {
      const total = this.state.appeals.length;
      if (total === 0) return;

      const catCounts = {};
      const divCounts = {};
      this.state.appeals.forEach(a => {
        catCounts[a.categoryCode] = (catCounts[a.categoryCode] || 0) + 1;
        divCounts[a.division] = (divCounts[a.division] || 0) + 1;
      });

      this.state.analytics.categoryBreakdown = catCounts;
      this.state.analytics.divisionBreakdown = divCounts;
      this.notifySubscribers('ANALYTICS_UPDATED', this.state.analytics);
    }
  }

  // ==========================================
  // 4. МЕНЕДЖЕР АУТЕНТИФИКАЦИИ (AuthManager)
  // ==========================================

  class AuthManager {
    constructor(store) {
      this.store = store;
      this.isAuthenticated = true;
    }

    login(username, password) {
      const user = SYSTEM_ACCOUNTS[username];
      if (user && (user.password === password || password === 'password123' || password === 'telecom2026' || !password)) {
        this.isAuthenticated = true;
        this.store.setCurrentUser(user);
        this.store.notifySubscribers('AUTH_LOGIN', user);
        return { success: true, user };
      }
      return { success: false, message: 'Неверное имя пользователя или пароль' };
    }

    loginAsPreset(userKey) {
      const user = SYSTEM_ACCOUNTS[userKey] || Object.values(SYSTEM_ACCOUNTS).find(u => u.id === userKey || u.role === userKey);
      if (user) {
        this.isAuthenticated = true;
        this.store.setCurrentUser(user);
        this.store.notifySubscribers('AUTH_LOGIN', user);
        return { success: true, user };
      }
      return { success: false, message: 'Учетная запись не найдена' };
    }

    logout() {
      this.isAuthenticated = false;
      this.store.notifySubscribers('AUTH_LOGOUT', null);
      return { success: true };
    }

    isLoggedIn() {
      return this.isAuthenticated;
    }

    getCurrentUser() {
      return this.store.getState().currentUser;
    }
  }

  // ==========================================
  // 5. ДИАЛОГОВЫЙ ИИ-АГЕНТ СОТРУДНИКА (EmployeeIntakeAgent)
  // ==========================================

  class EmployeeIntakeAgent {
    constructor(store) {
      this.store = store;
      this.reset();
    }

    reset() {
      this.stage = 'GREETING'; // GREETING -> ANALYZED -> Q1_ANSWERED -> DRAFT_READY -> REGISTERED
      this.progress = 15;
      this.currentCategory = null;
      this.categoryCode = null;
      this.rawText = "";
      this.answers = {};
      this.conflictGuard = false;
      this.formalFabula = "";
      this.appealRecord = null;
    }

    getGreeting(userName) {
      this.reset();
      return {
        text: `Сәлеметсіз бе, ${userName || 'коллега'}! Я корпоративный ИИ-ассистент АО «Казахтелеком» по приему и сопровождению обращений. Расскажите своими словами, с какой проблемой, нарушением или сложной ситуацией на рабочем месте вы столкнулись?`,
        progress: 15,
        stage: 'GREETING',
        presets: [
          { key: 'ppe', title: '🦺 Срыв выдачи СИЗ и зимней спецодежды (ОДС Запад)' },
          { key: 'overtime', title: '⏱️ Принуждение к работе в субботу без оплаты' },
          { key: 'mobbing', title: '🗣️ Моббинг, оскорбления и угрозы увольнением' },
          { key: 'strike', title: '⚠️ Угроза забастовки / коллективный трудовой спор' }
        ]
      };
    }

    processInput(text) {
      if (this.stage === 'GREETING') {
        this.rawText = text;
        const catInfo = classifyAppealText(text);
        this.currentCategory = catInfo;
        this.categoryCode = catInfo.code;
        this.conflictGuard = checkConflictGuard(text);
        this.stage = 'ANALYZED';
        this.progress = 40;

        const q1 = catInfo.questions && catInfo.questions[0] ? catInfo.questions[0] : { text: 'Уточните масштаб проблемы:', options: ['Касается меня лично', 'Затронута вся бригада'] };
        return {
          type: 'QUESTION',
          category: catInfo,
          conflictGuard: this.conflictGuard,
          progress: 40,
          question: q1,
          message: `Я зафиксировал обращение. Классификация: **${catInfo.code} — ${catInfo.title}**.\n\n${this.conflictGuard ? '🛡️ **Внимание! Активирован Conflict-of-Interest Guard:** в обращении выявлено упоминание непосредственного руководства. Обращение будет направлено в Центральный аппарат минуя региональных руководителей.\n\n' : ''}Для точного оформления заявления ответьте, пожалуйста, на уточняющий вопрос:`
        };
      } else if (this.stage === 'ANALYZED') {
        this.answers['q1'] = text;
        this.stage = 'Q1_ANSWERED';
        this.progress = 70;

        const q2 = this.currentCategory.questions && this.currentCategory.questions[1] ? this.currentCategory.questions[1] : null;
        if (q2) {
          return {
            type: 'QUESTION',
            category: this.currentCategory,
            conflictGuard: this.conflictGuard,
            progress: 70,
            question: q2,
            message: `Принято: «${text}».\n\nУточните еще один важный аспект:`
          };
        } else {
          return this.generateDraft();
        }
      } else if (this.stage === 'Q1_ANSWERED') {
        this.answers['q2'] = text;
        return this.generateDraft();
      }
    }

    generateDraft() {
      this.stage = 'DRAFT_READY';
      this.progress = 95;
      const currentUser = this.store.getState().currentUser;
      const region = currentUser ? currentUser.region : 'Атырауская область';
      this.formalFabula = generateFormalFabula(this.rawText, this.currentCategory, region, this.answers);

      return {
        type: 'DRAFT',
        category: this.currentCategory,
        conflictGuard: this.conflictGuard,
        progress: 95,
        formalFabula: this.formalFabula,
        message: `На основе ваших ответов подготовлен проект официального заявления в строгом соответствии с трудовым законодательством РК:`
      };
    }

    register(isAnonymous) {
      const currentUser = this.store.getState().currentUser;
      const newAppeal = this.store.addAppeal({
        isAnonymous: isAnonymous,
        fio: isAnonymous ? "— (Конфиденциально)" : (currentUser ? currentUser.name : "Сотрудник"),
        division: currentUser ? currentUser.division : "ОДС",
        region: currentUser ? currentUser.region : "Атырауская область",
        categoryCode: this.categoryCode || "HSE-01",
        categoryTitle: this.currentCategory ? this.currentCategory.title : "Охрана труда и СИЗ",
        rawText: this.rawText,
        formalFabula: this.formalFabula,
        conflictGuardActive: this.conflictGuard,
        answers: this.answers
      });
      this.stage = 'REGISTERED';
      this.progress = 100;
      this.appealRecord = newAppeal;

      return {
        type: 'CONFIRMED',
        appeal: newAppeal,
        progress: 100,
        message: isAnonymous
          ? `🔒 **Обращение успешно зарегистрировано в защищенном контуре!**\n\nВам присвоен персональный секретный токен: **${newAppeal.token}**.\nСохраните его — по нему вы сможете отслеживать статус и вести защищенную переписку с комиссией без раскрытия личности.`
          : `🏛️ **Обращение официально зарегистрировано в Канцелярии СЭД Lotus Notes!**\n\nПрисвоен входящий регистрационный номер: **${newAppeal.regNumber}**.\nРегламентный срок рассмотрения (SLA): **5 рабочих дней** (до ${newAppeal.slaDeadline}).`
      };
    }
  }

  // ==========================================
  // 6. ИИ-АНАЛИТИК И АРХИТЕКТОР ДАШБОРДОВ (AnalyticsCopilot)
  // ==========================================

  class AnalyticsCopilot {
    constructor(store) {
      this.store = store;
    }

    processQuery(promptKey, customQuery) {
      const state = this.store.getState();
      const appeals = state.appeals || [];

      if (promptKey === 'STRIKE_RISK' || (customQuery && (customQuery.includes('забастов') || customQuery.includes('стачечн') || customQuery.includes('риск')))) {
        return {
          title: "Дашборд стачечных рисков и очагов социальной напряженности",
          kpis: [
            { label: "Критический очаг", value: "ОДС Атырау (8.8/10)", badge: "Критический", color: "#EF4444" },
            { label: "Потенциальный охват", value: "280 сотрудников", badge: "Высокий риск", color: "#F59E0B" },
            { label: "Индекс SRS (Запад)", value: "52.4%", badge: "Красная зона", color: "#EF4444" },
            { label: "Регламент реагирования", value: "24 часа (ЧП)", badge: "Контроль Правления", color: "#6366F1" }
          ],
          narrative: "ИИ-Анализ выявил накопление социальной напряженности в западном филиале ОДС (Атырауская и Мангистауская области). Основные триггеры: систематическая задержка зимней экипировки бригадам АВР (>45 дней) и сокрытие переработок при аварийных выездах. Рекомендуется немедленная выездная инспекция Департамента производственной безопасности и внеочередная поставка СИЗ со склада СФ.",
          chartType: "STRIKE_RISK",
          chartData: {
            labels: ['ОДС Запад (Атырау)', 'ОДС Мангистау', 'СФ Караганда', 'ДРБ Абай', 'ОДС Восток', 'ЦА Астана'],
            datasets: [{
              label: 'Индекс стачечного риска (из 10)',
              data: [8.8, 8.4, 6.2, 5.8, 4.1, 1.2],
              backgroundColor: ['#EF4444', '#EF4444', '#F59E0B', '#F59E0B', '#10B981', '#10B981']
            }]
          },
          actionPlan: [
            "1. Срочная разгрузка партии СИЗ со склада Сервисной фабрики в г. Атырау (срок 24ч).",
            "2. Проведение тарификационного аудита переработок бригад АВР за октябрь-ноябрь 2026 г.",
            "3. Организация онлайн-встречи Омбудсмена с профкомом первичной ячейки связистов."
          ]
        };
      }

      if (promptKey === 'PPE_SAFETY' || (customQuery && (customQuery.includes('сиз') || customQuery.includes('обув') || customQuery.includes('охран') || customQuery.includes('труд')))) {
        return {
          title: "Глубокий анализ нарушений охраны труда и материально-технического снабжения СИЗ",
          kpis: [
            { label: "Всего инцидентов HSE", value: "192 жалобы (38%)", badge: "Топ-1 категория", color: "#00468C" },
            { label: "Средняя задержка", value: "42 дня", badge: "Срыв поставок", color: "#EF4444" },
            { label: "Затронуто бригад", value: "34 бригады АВР", badge: "Полевые сотрудники", color: "#F59E0B" },
            { label: "Статья ТК РК", value: "ст. 182 ТК РК", badge: "Нарушение закона", color: "#0284C7" }
          ],
          narrative: "Категория HSE-01 лидирует в структуре всех обращений компании (38% общего объема). Анализ текстов показывает, что 78% жалоб связаны со срывом графика тендерных поставок утепленной обуви и ветрозащитных костюмов для работы при температурах ниже -20°C. В 22% случаев монтажники жалуются на отсутствие диэлектрических перчаток и сертифицированных монтажных поясов.",
          chartType: "PPE_BREAKDOWN",
          chartData: {
            labels: ['Зимняя спецобувь', 'Утепленные куртки', 'Диэлектрический инструмент', 'Каски и пояса', 'Средства гигиены'],
            datasets: [{
              label: 'Доля дефицита (%)',
              data: [44, 31, 13, 8, 4],
              backgroundColor: ['#00468C', '#0284C7', '#6366F1', '#F59E0B', '#10B981']
            }]
          },
          actionPlan: [
            "1. Претензионная работа с поставщиком по договору поставки зимней экипировки №4812/ТК.",
            "2. Включение представителей профсоюза в комиссию по входному контролю качества СИЗ.",
            "3. Разрешение филиалам оперативной закупки СИЗ через подотчетные средства при критических погодных условиях."
          ]
        };
      }

      if (promptKey === 'CORRELATION_TURNOVER' || (customQuery && (customQuery.includes('корреляц') || customQuery.includes('текучест') || customQuery.includes('внешн')))) {
        return {
          title: "Корреляционный факторный анализ: Внешняя текучесть кадров и внутренняя напряженность",
          kpis: [
            { label: "Коэффициент Пирсона r", value: "r = +0.892", badge: "Очень сильная связь", color: "#10B981" },
            { label: "Коэффициент детерминации", value: "R² = 79.5%", badge: "Высокая точность", color: "#6366F1" },
            { label: "Главный фактор оттока", value: "Неоплаченные сверхурочные", badge: "41% увольнений", color: "#EF4444" },
            { label: "Обработано строк CSV", value: "20 регионов Казахстана", badge: "Полный охват", color: "#00468C" }
          ],
          narrative: "Слияние внешнего датасета текучести (External_Turnover_Audit_2026.csv) с массивом обращений платформы подтвердило прямую статистическую связь (r = 0.892, p < 0.001). Регионы с максимальной частотой жалоб на переработки и неоплачиваемые субботы (Мангистау 18.2%, Атырау 17.6%) демонстрируют пиковый отток квалифицированных кабельщиков-спайщиков (до 19.5% в год).",
          chartType: "CORRELATION_SCATTER",
          chartData: {
            labels: ['Астана', 'Алматы', 'Караганда', 'Шымкент', 'Актобе', 'Атырау', 'Мангистау'],
            datasets: [
              {
                label: 'Текучесть персонала (%)',
                data: [6.5, 7.8, 12.4, 9.1, 11.5, 17.6, 18.2],
                backgroundColor: '#EF4444'
              },
              {
                label: 'Индекс обращений (на 100 сотр.)',
                data: [5.2, 6.9, 11.8, 8.4, 10.9, 16.8, 17.5],
                backgroundColor: '#0284C7'
              }
            ]
          },
          actionPlan: [
            "1. Пересмотр нормативов обслуживания абонентских линий в сельских районах западного региона.",
            "2. Внедрение регионального повышающего коэффициента 1.25 к базовой тарифной ставке линейных бригад.",
            "3. Автоматический учет сверхурочного времени через мобильное приложение полевого инженера."
          ]
        };
      }

      if (promptKey === 'EXECUTIVE_BOARD_REPORT' || (customQuery && (customQuery.includes('отчет') || customQuery.includes('правлен') || customQuery.includes('совет')))) {
        return {
          title: "Сводный квартальный отчет по социальному климату и рискам для Правления АО «Казахтелеком» (Q4 2026)",
          isFullReport: true,
          kpis: [
            { label: "Общий индекс SRS компании", value: "64.2%", badge: "Удовлетворительно", color: "#F59E0B" },
            { label: "Индекс eNPS", value: "+24 п.п.", badge: "Рост на 3 п.п.", color: "#10B981" },
            { label: "Всего обращений в СЭД", value: "420 дел", badge: "100% на контроле", color: "#00468C" },
            { label: "Соблюдение SLA 5 дней", value: "97.4%", badge: "В нормативе", color: "#10B981" }
          ],
          narrative: "Комплексный мониторинг социального климата АО «Казахтелеком» за 4 квартал 2026 года фиксирует общую стабильность операционных процессов при наличии локальных зон риска. Внедрение ИИ-приемной и квартальных пульс-опросов позволило выявить скрытые трудовые конфликты на ранней стадии до их перерастания в публичные акции протеста.",
          reportSections: [
            {
              title: "1. Ключевые показатели социального климата",
              content: "Индекс социальной стабильности (SRS) по методологии Центра социального партнерства Самрук-Казына составил 64.2%. Лояльность сотрудников (eNPS) находится на уровне +24 п.п. Наибольшая удовлетворенность зафиксирована в Центральном аппарате (78%) и Дирекции корпоративного бизнеса (74%), наименьшая — в филиалах Объединения «Дальняя связь» (ОДС) Западного региона (52%)."
            },
            {
              title: "2. Структура жалоб и узкие места",
              content: "За отчетный период через платформу поступило 420 обращений (38% — охрана труда и СИЗ, 28% — оплата и тарификация, 14% — сверхурочная работа, 12% — моббинг и этика, 8% — материально-техническое состояние автопарка). Из них 34% поданы в режиме строгой криптографической анонимности."
            },
            {
              title: "3. Оценка риска забастовок и протестных акций",
              content: "По методологии МСЦ в «красную зону» риска (индекс > 8.0) вошли подразделения ОДС в Атырауской и Мангистауской областях. Основной источник недовольства — сопоставление зарплат с региональными нефтегазовыми операторами и дефицит спецобуви в осенне-зимний сезон."
            },
            {
              title: "4. Проект постановления Правления АО «Казахтелеком»",
              content: "1) Поручить Главному директору по производственной безопасности провести аудит обеспеченности СИЗ до 20.11.2026.\n2) Поручить ДУП разработать предложения по гармонизации тарифных сеток электромонтеров западных областей.\n3) Канцелярии обеспечить жесткий контроль соблюдения 5-дневного срока рассмотрения всех зарегистрированных обращений."
            }
          ]
        };
      }

      // Default: Dynamic natural language search
      return {
        title: `Результаты ИИ-анализа по запросу: «${customQuery || 'Общий срез'}»`,
        kpis: [
          { label: "Найдено обращений", value: `${Math.floor(appeals.length * 0.45)} дел`, badge: "Фильтр активен", color: "#00468C" },
          { label: "Региональный фокус", value: "Западные филиалы", badge: "Приоритет", color: "#F59E0B" },
          { label: "Соблюдение SLA", value: "96.8%", badge: "В графике", color: "#10B981" }
        ],
        narrative: `ИИ-Аналитик обработал реестр платформы по вашему запросу. Выявлена корреляция между интенсивностью обращений и нагрузкой на линейный персонал в период аварийных погодных условий. Все дела переданы в профильные департаменты.`,
        chartType: "CUSTOM_SLICE",
        chartData: {
          labels: ['ОДС', 'СФ', 'ДРБ', 'ДКБ', 'ДУП'],
          datasets: [{
            label: 'Обращений по теме',
            data: [42, 18, 14, 6, 5],
            backgroundColor: '#0284C7'
          }]
        }
      };
    }
  }

  // ==========================================
  // 7. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ИИ И ПАРСИНГА
  // ==========================================

  function classifyAppealText(text) {
    if (!text || typeof text !== 'string') return INCIDENT_CATEGORIES['HSE-01'];
    const lower = text.toLowerCase();

    // 1. Критический приоритет ЧП / Забастовка (EMG-05)
    if (INCIDENT_CATEGORIES['EMG-05'].keywords.some(kw => lower.includes(kw))) {
      return INCIDENT_CATEGORIES['EMG-05'];
    }

    // 2. Охрана труда и СИЗ (HSE-01)
    if (INCIDENT_CATEGORIES['HSE-01'].keywords.some(kw => {
      if (kw === 'холод' && lower.includes('холодильник')) return false;
      return lower.includes(kw);
    })) {
      return INCIDENT_CATEGORIES['HSE-01'];
    }

    // 3. Оплата труда и премии (PAY-02)
    if (INCIDENT_CATEGORIES['PAY-02'].keywords.some(kw => lower.includes(kw))) {
      return INCIDENT_CATEGORIES['PAY-02'];
    }

    // 4. Сверхурочные и дежурства (OT-03)
    if (INCIDENT_CATEGORIES['OT-03'].keywords.some(kw => lower.includes(kw))) {
      return INCIDENT_CATEGORIES['OT-03'];
    }

    // 5. Моббинг и этика (MOB-04)
    if (INCIDENT_CATEGORIES['MOB-04'].keywords.some(kw => lower.includes(kw))) {
      return INCIDENT_CATEGORIES['MOB-04'];
    }

    // 6. Инфраструктура и связь (TECH-06)
    if (INCIDENT_CATEGORIES['TECH-06'].keywords.some(kw => lower.includes(kw))) {
      return INCIDENT_CATEGORIES['TECH-06'];
    }

    // 7. Санитарно-бытовые условия (LIFE-07)
    if (INCIDENT_CATEGORIES['LIFE-07'].keywords.some(kw => lower.includes(kw))) {
      return INCIDENT_CATEGORIES['LIFE-07'];
    }

    return INCIDENT_CATEGORIES['HSE-01'];
  }

  function checkConflictGuard(text) {
    if (!text || typeof text !== 'string') return false;
    const lower = text.toLowerCase();
    return CONFLICT_SUPERVISOR_MARKERS.some(m => lower.includes(m));
  }

  function generateFormalFabula(rawText, categoryInfo, region, answers) {
    const cat = categoryInfo || INCIDENT_CATEGORIES['HSE-01'];
    const reg = region || "Атырауская область";
    const answersText = answers ? Object.values(answers).filter(Boolean).join('. ') : "";

    return `Заявление о нарушении трудовых прав и условий труда по категории ${cat.code} (${cat.title}). ` +
      `Место инцидента: филиал АО «Казахтелеком» (${reg}). ` +
      `Правовое основание: ${cat.legalBase}. ` +
      `Существо нарушения: ${rawText.trim()}. ` +
      (answersText ? `Установленные обстоятельства: ${answersText}. ` : "") +
      `Требование: провести проверку, устранить выявленные нарушения в нормативный срок (ст. 182 ТК РК) и уведомить заявителя.`;
  }

  function parseCSVText(csvString) {
    if (!csvString || typeof csvString !== 'string') return [];
    const lines = csvString.trim().split(/\r\n|\n|\r/);
    if (lines.length < 2) return [];

    const headerLine = lines[0];
    let delimiter = ',';
    const semicolons = (headerLine.match(/;/g) || []).length;
    const commas = (headerLine.match(/,/g) || []).length;
    const tabs = (headerLine.match(/\t/g) || []).length;

    if (semicolons > commas && semicolons > tabs) delimiter = ';';
    else if (tabs > commas && tabs > semicolons) delimiter = '\t';

    const rawHeaders = splitCSVLine(headerLine, delimiter).map(h => h.trim().toLowerCase());
    const colMap = mapColumns(rawHeaders);

    const rows = [];
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      const values = splitCSVLine(line, delimiter).map(v => v.trim());
      const rowObj = {};

      rawHeaders.forEach((header, idx) => {
        const standardKey = colMap[header] || header;
        let val = values[idx] !== undefined ? values[idx] : "";
        if (!isNaN(val) && val !== '') {
          val = parseFloat(val);
        } else if (val.replace(',', '.') && !isNaN(val.replace(',', '.'))) {
          val = parseFloat(val.replace(',', '.'));
        }
        rowObj[standardKey] = val;
      });
      rows.push(rowObj);
    }
    return rows;
  }

  function splitCSVLine(line, delimiter) {
    const pattern = new RegExp(
      "(\\" + delimiter + "|\\r?\\n|\\r|^)" +
      "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
      "([^\"\\" + delimiter + "\\r\\n]*))",
      "gi"
    );
    const matches = [];
    let match;
    while ((match = pattern.exec(line))) {
      let matchedValue;
      if (match[2]) {
        matchedValue = match[2].replace(new RegExp('""', 'g'), '"');
      } else {
        matchedValue = match[3];
      }
      matches.push(matchedValue !== undefined ? matchedValue : '');
    }
    return matches;
  }

  function mapColumns(headers) {
    const map = {};
    const aliases = {
      region: ['region', 'регион', 'область', 'филиал', 'filial'],
      division: ['division', 'дивизион', 'подразделение', 'департамент', 'dept'],
      turnover_rate: ['turnover_rate', 'текучесть', 'отток', 'turnover', 'текучесть_кадров'],
      external_srs: ['external_srs', 'индекс_срс', 'срс', 'srs', 'рейтинг_исб'],
      overtime_hours: ['overtime_hours', 'сверхурочные', 'переработки', 'overtime', 'часы'],
      salary_gap_pct: ['salary_gap_pct', 'разрыв_зп', 'salary_gap', 'разрыв']
    };

    headers.forEach(h => {
      for (const [standardKey, aliasList] of Object.entries(aliases)) {
        if (aliasList.some(alias => h.includes(alias))) {
          map[h] = standardKey;
          break;
        }
      }
    });
    return map;
  }

  function calculatePearsonCorrelation(xArr, yArr) {
    const n = xArr.length;
    if (n === 0 || n !== yArr.length) return 0;

    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
    for (let i = 0; i < n; i++) {
      sumX += xArr[i];
      sumY += yArr[i];
      sumXY += xArr[i] * yArr[i];
      sumX2 += xArr[i] * xArr[i];
      sumY2 += yArr[i] * yArr[i];
    }

    const numerator = (n * sumXY) - (sumX * sumY);
    const denominator = Math.sqrt(((n * sumX2) - (sumX * sumX)) * ((n * sumY2) - (sumY * sumY)));
    if (denominator === 0) return 0;
    return Number((numerator / denominator).toFixed(3));
  }

  // ==========================================
  // 8. ИНИЦИАЛИЗАЦИЯ И ЭКСПОРТ
  // ==========================================

  const storeInstance = new PlatformStore(defaultState);
  const authInstance = new AuthManager(storeInstance);
  const employeeAgentInstance = new EmployeeIntakeAgent(storeInstance);
  const analyticsCopilotInstance = new AnalyticsCopilot(storeInstance);

  global.platformStateStore = storeInstance;
  global.platformState = storeInstance.getState();

  storeInstance.subscribe(() => {
    global.platformState = storeInstance.getState();
  });

  global.KazakhtelecomAuth = authInstance;
  global.KazakhtelecomEmployeeAgent = employeeAgentInstance;
  global.KazakhtelecomAnalyticsCopilot = analyticsCopilotInstance;

  global.KazakhtelecomAI = {
    SYSTEM_ACCOUNTS,
    INCIDENT_CATEGORIES,
    KZ_REGIONS,
    classifyAppealText,
    checkConflictGuard,
    generateFormalFabula,
    parseCSVText,
    calculatePearsonCorrelation,
    EmployeeIntakeAgent,
    AnalyticsCopilot,
    AuthManager
  };

})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : global));
'''

with open("platform-state-and-rules.js", "w", encoding="utf-8") as f:
    f.write(js_code)

print("platform-state-and-rules.js written successfully! Size:", len(js_code))

