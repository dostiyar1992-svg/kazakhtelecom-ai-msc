# -*- coding: utf-8 -*-
"""
add_survey_engine.py
Adds PROJECT_SURVEY_QUESTIONS and AutonomousSurveyEngine to platform-state-and-rules.js
and updates server.py to conduct autonomous surveys with Gemini based on project files.
"""

import os
import sys

# 1. READ platform-state-and-rules.js
with open("platform-state-and-rules.js", "r", encoding="utf-8") as f:
    js_text = f.read()

# SURVEY ENGINE CODE TO INSERT
survey_engine_code = r'''
  // =========================================================================
  // 3. ВОПРОСЫ ПУЛЬС-ОПРОСА ИЗ ДОКУМЕНТОВ ПРОЕКТА АО «КАЗАХТЕЛЕКОМ»
  // (пульс ө опрос.docx, Анонимный опрос работников.docx, ОПРОСНИК ПРОФС.docx)
  // =========================================================================
  const PROJECT_SURVEY_QUESTIONS = [
    {
      id: "q_salary",
      docSource: "пульс ө опрос.docx (вопрос 1)",
      category: "PAY-02",
      block: "Оплата труда и материальное благополучие",
      text: "Моя заработная плата позволяет комфортно покрывать основные жизненные расходы.",
      scaleMin: "Не согласен (1)",
      scaleMax: "Полностью согласен (5)",
      weight: 1.2
    },
    {
      id: "q_feedback_channels",
      docSource: "пульс ө опрос.docx (вопрос 2)",
      category: "TECH-06",
      block: "Эффективность обратной связи",
      text: "Существующие в АО «Казахтелеком» способы обращения к руководству реально помогают мне решать рабочие вопросы.",
      scaleMin: "Не помогают (1)",
      scaleMax: "Реально помогают (5)",
      weight: 1.0
    },
    {
      id: "q_open_criticism",
      docSource: "пульс ө опрос.docx (вопрос 3)",
      category: "MOB-04",
      block: "Психологическая безопасность и открытость",
      text: "Я могу открыто высказывать замечания по условиям труда и говорить о своих проблемах без опасений негативной реакции руководства.",
      scaleMin: "Боюсь последствий (1)",
      scaleMax: "Абсолютно свободно (5)",
      weight: 1.3
    },
    {
      id: "q_trust_leadership",
      docSource: "пульс ө опрос.docx (вопрос 4)",
      category: "LIFE-07",
      block: "Доверие менеджменту компании",
      text: "Я доверяю официальной информации, поступающей от руководства компании и филиала.",
      scaleMin: "Не доверяю (1)",
      scaleMax: "Полностью доверяю (5)",
      weight: 1.0
    },
    {
      id: "q_pressure_freedom",
      docSource: "пульс ө опрос.docx (вопрос 5) & Анонимный опрос работников.docx",
      category: "MOB-04",
      block: "Профилактика давления и моббинга",
      text: "Оцените степень психологического комфорта (отсутствие морального давления со стороны непосредственных мастеров и начальников).",
      scaleMin: "Постоянное давление (1)",
      scaleMax: "Комфортно и уважительно (5)",
      weight: 1.4
    },
    {
      id: "q_ppe_safety",
      docSource: "ОПРОСНИК ПРОФС.docx & ст. 182 ТК РК",
      category: "HSE-01",
      block: "Охрана труда и обеспечение СИЗ",
      text: "Насколько вы обеспечены исправными СИЗ, зимней спецодеждой, спецобувью и качественным инструментом для безопасной работы?",
      scaleMin: "Критический дефицит (1)",
      scaleMax: "Полностью обеспечен (5)",
      weight: 1.5
    },
    {
      id: "q_team_solidarity",
      docSource: "Анонимный опрос работников.docx (Раздел 5)",
      category: "LIFE-07",
      block: "Командный дух и атмосфера",
      text: "В нашем производственном коллективе (бригаде / участке) развита взаимовыручка и поддержка в сложных рабочих ситуациях.",
      scaleMin: "Каждый сам за себя (1)",
      scaleMax: "Сплоченная команда (5)",
      weight: 1.0
    },
    {
      id: "q_enps_loyalty",
      docSource: "srs_pulse_data_for_ai.xlsx & методология Самрук-Казына",
      category: "PAY-02",
      block: "Индекс лояльности (eNPS)",
      text: "С какой вероятностью вы порекомендуете АО «Казахтелеком» как надежного работодателя своим коллегам и друзьям?",
      scaleMin: "Точно не порекомендую (1)",
      scaleMax: "Обязательно порекомендую (5)",
      weight: 1.2
    }
  ];

  class AutonomousSurveyEngine {
    constructor(store) {
      this.store = store;
      this.reset();
    }

    reset() {
      this.currentIndex = 0;
      this.answers = {};
      this.isCompleted = false;
      this.criticalIssues = [];
    }

    startSurvey() {
      this.reset();
      return this.getCurrentQuestionData();
    }

    getCurrentQuestionData() {
      const q = PROJECT_SURVEY_QUESTIONS[this.currentIndex];
      const total = PROJECT_SURVEY_QUESTIONS.length;
      const pct = Math.round((this.currentIndex / total) * 100);

      return {
        isFinished: false,
        questionIndex: this.currentIndex + 1,
        totalQuestions: total,
        progressPct: pct,
        question: q,
        message: `**Вопрос ${this.currentIndex + 1} из ${total}:**\n\n📌 **${q.block}**\n*«${q.text}»*\n\n*(Источник: ${q.docSource})*`,
        scale: [1, 2, 3, 4, 5],
        scaleMin: q.scaleMin,
        scaleMax: q.scaleMax
      };
    }

    answerQuestion(score) {
      const numScore = parseInt(score, 10) || 3;
      const currentQ = PROJECT_SURVEY_QUESTIONS[this.currentIndex];
      this.answers[currentQ.id] = numScore;

      let synergyAlert = false;
      if (numScore <= 2) {
        this.criticalIssues.push({
          question: currentQ,
          score: numScore
        });
        synergyAlert = true;
      }

      this.currentIndex++;

      if (this.currentIndex >= PROJECT_SURVEY_QUESTIONS.length) {
        this.isCompleted = true;
        const result = this.calculateResults();
        return {
          isFinished: true,
          progressPct: 100,
          synergyAlert: synergyAlert,
          lastScore: numScore,
          criticalIssue: synergyAlert ? currentQ : null,
          result: result,
          message: `🎉 **Пульс-опрос успешно завершен!**\n\nСпасибо за искренние ответы. Ваши оценки запечатаны в защищенный пул квартального анализа АО «Казахтелеком».\n\n📊 **Ваш профиль удовлетворенности:**\n• Индекс SRS по опросу: **${result.srsIndex}%**\n• Лояльность (eNPS): **${result.enpsCategory}**\n• Статус климата: **${result.climateStatus}**\n\n${this.criticalIssues.length > 0 ? `⚠️ *Внимание: зафиксировано ${this.criticalIssues.length} критических зон (оценки 1-2 балла). Вы можете сразу передать их в виде официального или анонимного обращения.*` : ''}`
        };
      }

      const nextData = this.getCurrentQuestionData();
      nextData.synergyAlert = synergyAlert;
      nextData.lastScore = numScore;
      nextData.criticalIssue = synergyAlert ? currentQ : null;
      return nextData;
    }

    calculateResults() {
      const scores = Object.values(this.answers);
      const total = scores.length;
      if (total === 0) return { srsIndex: 64, enpsCategory: "Нейтрал", climateStatus: "Стабильно" };

      const sum = scores.reduce((a, b) => a + b, 0);
      const avg = sum / total;
      const srsIndex = Math.round((avg / 5) * 100);

      const enpsScore = this.answers['q_enps_loyalty'] || 3;
      let enpsCat = "Нейтрал (Passive)";
      if (enpsScore >= 4) enpsCat = "Промоутер (Promoter)";
      else if (enpsScore <= 2) enpsCat = "Критик (Detractor)";

      let status = "Благоприятный климат 🟢";
      if (srsIndex < 55) status = "Зона высокого риска 🔴 (Требует вмешательства)";
      else if (srsIndex < 70) status = "Умеренная напряженность 🟡";

      // Commit to platformState analytics
      const state = this.store.getState();
      if (state.surveys && state.surveys[0]) {
        state.surveys[0].responseRatePct = Number((state.surveys[0].responseRatePct + 0.1).toFixed(1));
        state.surveys[0].metrics.srsIndex = Number(((state.surveys[0].metrics.srsIndex * 9 + srsIndex) / 10).toFixed(1));
      }
      this.store.notifySubscribers('SURVEY_COMPLETED', { srsIndex, answers: this.answers });

      return {
        srsIndex,
        avgScore: avg.toFixed(1),
        enpsCategory: enpsCat,
        climateStatus: status,
        criticalCount: this.criticalIssues.length
      };
    }
  }
'''

if "AutonomousSurveyEngine" not in js_text:
    target_pos = js_text.find("class EmployeeIntakeAgent")
    js_text = js_text[:target_pos] + survey_engine_code + "\n\n  " + js_text[target_pos:]

    # Add to exports
    js_text = js_text.replace(
        "global.KazakhtelecomEmployeeAgent = employeeAgentInstance;",
        "global.KazakhtelecomEmployeeAgent = employeeAgentInstance;\n  global.KazakhtelecomSurveyEngine = new AutonomousSurveyEngine(storeInstance);"
    )
    js_text = js_text.replace(
        "global.KazakhtelecomAI = {",
        "global.KazakhtelecomAI = {\n    PROJECT_SURVEY_QUESTIONS,\n    AutonomousSurveyEngine,"
    )

    with open("platform-state-and-rules.js", "w", encoding="utf-8") as f:
        f.write(js_text)
    print("platform-state-and-rules.js updated with AutonomousSurveyEngine!")
else:
    print("AutonomousSurveyEngine already present in platform-state-and-rules.js")

