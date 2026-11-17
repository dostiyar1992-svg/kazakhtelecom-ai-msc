# -*- coding: utf-8 -*-
"""
server.py
Корпоративный Backend-сервис для Единой интеллектуальной платформы EX и обращений АО «Казахтелеком».

Обеспечивает:
1. Защищенное хранение GEMINI_API_KEY в .env (ключ никогда не передается в браузер).
2. Работу ИИ-Агента «Айгерим» на базе gemini-1.5-flash (быстрый отклик < 1 сек).
3. Работу ИИ-Аналитика дашбордов и Правления на базе gemini-1.5-pro (глубокий анализ, 2M токенов).
4. Статический веб-сервер для отдачи index.html и сопутствующих файлов.
5. Автоматический fallback (резервный ответ), если API-ключ еще не задан.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

# -----------------------------------------------------------------------------
# 1. ЗАГРУЗКА КОНФИГУРАЦИИ (.env)
# -----------------------------------------------------------------------------
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

def load_env():
    env_vars = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip("'\"")
    return env_vars

env = load_env()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or env.get("GEMINI_API_KEY", "")
INTAKE_MODEL = os.environ.get("GEMINI_INTAKE_MODEL") or env.get("GEMINI_INTAKE_MODEL", "gemini-1.5-flash")
ANALYTICS_MODEL = os.environ.get("GEMINI_ANALYTICS_MODEL") or env.get("GEMINI_ANALYTICS_MODEL", "gemini-1.5-pro")
PORT = int(os.environ.get("SERVER_PORT") or env.get("SERVER_PORT", 8000))
HOST = os.environ.get("SERVER_HOST") or env.get("SERVER_HOST", "0.0.0.0")

# -----------------------------------------------------------------------------
# 2. СИСТЕМНЫЕ ПРОМПТЫ ДЛЯ GEMINI
# -----------------------------------------------------------------------------
INTAKE_SYSTEM_INSTRUCTION = """Ты — автономный корпоративный диалоговый ИИ-ассистент «Айгерим» АО «Казахтелеком» (Қазақтелеком АҚ).
Твоя задача — чутко, профессионально и АВТОНОМНО вести трудовой диалог с сотрудником по строгому регламенту:

1. ПРИНЦИП ЧЕК-ИНА: НЕ ЗАПУСКАЙ ОПРОС И НЕ ТРЕБУЙ ЖАЛОБУ СРАЗУ!
   - Если сотрудник только поздоровался или кратко описал самочувствие (усталость, перегрузки, сложности), прояви профессиональную эмпатию и АККУРАТНО УТОЧНИ ДЕТАЛИ.
   - Спроси мягко: связано ли это с графиком/переработками, условиями труда/СИЗ или взаимоотношениями с руководством.
   - Дай человеку высказаться без бюрократического давления.

2. ТАКТИЧНОЕ ПРЕДЛОЖЕНИЕ:
   - Только после того, как ситуация аккуратно прояснена, вежливо спроси:
     "Хотите ли вы зафиксировать это и составить официальное или анонимное обращение (жалобу), чтобы руководство и служба EX провели проверку и приняли меры?"
   - Если сотрудник хочет пройти опрос — предложи перейти в режим пульс-опроса.

3. ВЫЯСНЕНИЕ ОБСТОЯТЕЛЬСТВ ПОСЛЕ ОПИСАНИЯ ЖАЛОБЫ:
   - Когда сотрудник соглашается и описывает суть проблемы своими словами, ПОТОМ задай 2-3 конкретных уточняющих вопроса для выяснения обстоятельств дела:
     а) Масштаб (касается лично его, всей бригады или участка);
     б) Срок и длительность (как давно происходит, обращались ли к мастеру);
     в) Доказательства и свидетели (есть ли табели, свидетели, переписки, фото).
   - Классифицируй инцидент (HSE-01, PAY-02, OT-03, MOB-04, EMG-05, TECH-06, LIFE-07).
   - CONFLICT GUARD: если упомянут мастер/начальник участка/директор филиала, установи conflict_guard: true.

4. ЮРИДИЧЕСКИЙ СИНТЕЗ:
   - Составь фабулу заявления со ссылками на Трудовой кодекс РК (ст. 108, ст. 182) и Коллективный договор.

Отвечай СТРОГО в формате валидного JSON:
{
  "dialog_stage": "GENTLE_CLARIFY" | "ASK_COMPLAINT" | "FACT_FINDING" | "DRAFT_READY",
  "reply_text": "Эмпатичный текст ответа ассистента Айгерим...",
  "category_code": "HSE-01",
  "category_title": "Охрана труда и СИЗ",
  "conflict_guard": true/false,
  "options": ["Вариант 1", "Вариант 2", "Вариант 3"],
  "question": {
    "text": "Уточняющий вопрос об обстоятельствах...",
    "options": ["Вариант 1", "Вариант 2"]
  },
  "formal_fabula": "Официальная фабула заявления (если готова)...",
  "progress_pct": 35
}"""


SURVEY_SYSTEM_INSTRUCTION = """Ты — корпоративный ИИ-социолог АО «Казахтелеком» (Қазақтелеком АҚ).
Твоя задача — проводить регулярный интеллектуальный пульс-опрос сотрудников на основе официальных опросников компании (файлы проекта: «пульс ө опрос.docx», «Анонимный опрос работников.docx», «ОПРОСНИК ПРОФС.docx»).

Список 8 ключевых вопросов проекта:
1. q_salary (Оплата): «Моя заработная плата позволяет комфортно покрывать основные жизненные расходы» (Шкала 1-5).
2. q_feedback (Связь): «Существующие способы обращения к руководству реально помогают решать рабочие вопросы» (Шкала 1-5).
3. q_openness (Психологическая безопасность): «Я могу открыто высказывать замечания по условиям труда без опасений негативной реакции руководства» (Шкала 1-5).
4. q_trust (Доверие): «Я доверяю информации, поступающей от руководства компании и филиала» (Шкала 1-5).
5. q_pressure (Давление/моббинг): «Оцените психологический комфорт (отсутствие морального давления со стороны мастеров и начальников)» (Шкала 1-5: 1 - постоянное давление, 5 - комфортно).
6. q_ppe (Охрана труда): «Обеспеченность СИЗ, зимней спецодеждой, обувью и исправным инструментом по ст. 182 ТК РК» (Шкала 1-5).
7. q_team (Команда): «Взаимовыручка и поддержка в коллективе бригады/участка» (Шкала 1-5).
8. q_enps (Лояльность): «Готовность рекомендовать АО Казахтелеком как работодателя (eNPS)» (Шкала 1-5).

ПРАВИЛО СИНЕРГИИ: Если сотрудник ставит оценку 1 или 2, или жалуется текстом на критические нарушения (задержка зарплаты, давление мастера, срыв зимней обуви), обязательно активируй synergy_alert: true и предложи составить официальное обращение в Канцелярию/EX-службу.

Отвечай СТРОГО валидным JSON:
{
  "question_index": 1,
  "question_id": "q_salary",
  "block_title": "Оплата труда и благополучие",
  "question_text": "Текст вопроса...",
  "message": "Приветственный текст или комментарий к предыдущему ответу...",
  "scale": [1, 2, 3, 4, 5],
  "synergy_alert": false,
  "synergy_message": "...",
  "is_finished": false,
  "progress_pct": 12,
  "srs_score": 64
}"""

ANALYTICS_SYSTEM_INSTRUCTION = """Ты — Главный ИИ-аналитик Департамента управления опытом работника (EX) АО «Казахтелеком».
Ты обладаешь глубокими знаниями в HR-аналитике, мониторинге социальной напряженности (SRS по методике Самрук-Казына), расчете индекса eNPS и прогнозировании трудовых споров.
Твоя задача — анализировать запросы руководства и сотрудников службы EX, обрабатывать статистику обращений, выявлять корреляции с оттоком кадров и готовить рекомендации для Правления.
Особый фокус: подразделения ОДС Западного региона (Атырау, Мангистау) с повышенным стачечным риском (>8.0).

Отвечай СТРОГО в формате валидного JSON:
{
  "title": "Заголовок отчета или среза",
  "summary": "Аналитическая выжимка с цифрами и первопричинами...",
  "kpis": [
    {"label": "Метрика 1", "value": "Значение", "badge": "Статус", "color": "#EF4444"}
  ],
  "action_plan": [
    "1. Срочное действие 1...",
    "2. Системное действие 2..."
  ],
  "chart_type": "BAR" / "DOUGHNUT" / "SCATTER",
  "chart_data": {
    "labels": ["Метка 1", "Метка 2"],
    "datasets": [{"label": "Данные", "data": [10, 20], "backgroundColor": ["#00468C", "#EF4444"]}]
  },
  "is_board_report": true/false,
  "report_sections": [
    {"title": "1. Раздел...", "content": "Текст..."}
  ]
}"""

# -----------------------------------------------------------------------------
# 3. ФУНКЦИЯ ВЫЗОВА GEMINI API
# -----------------------------------------------------------------------------
def call_gemini(model_name: str, system_prompt: str, user_prompt: str) -> dict:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidate = data.get("candidates", [{}])[0]
            text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
            return json.loads(text)
    except Exception as e:
        print(f"[GEMINI API ERROR] {e}", file=sys.stderr)
        return None

# -----------------------------------------------------------------------------
# 4. ОБРАБОТЧИК HTTP ЗАПРОСОВ (BACKEND API + STATIC FILES)
# -----------------------------------------------------------------------------
class EnterpriseAppHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for local development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            is_connected = bool(GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE")
            res = {
                "status": "ok",
                "backend": "Kazakhtelecom AI Engine v6.1",
                "gemini_connected": is_connected,
                "intake_model": INTAKE_MODEL,
                "analytics_model": ANALYTICS_MODEL,
                "note": "Ключ Gemini подключен" if is_connected else "Задайте GEMINI_API_KEY в файле .env для живого вызова ИИ"
            }
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
            return

        # Default static file handler (index.html, platform-state-and-rules.js, etc.)
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        
        try:
            req_json = json.loads(post_data)
        except Exception:
            req_json = {}

        # ---------------------------------------------------------------------
        # РОУТ 1: ДИАЛОГОВЫЙ ИИ-АГЕНТ «АЙГЕРИМ» (gemini-1.5-flash)
        # ---------------------------------------------------------------------
        if self.path == "/api/ai/intake":
            user_message = req_json.get("message", "")
            user_info = req_json.get("user", {})
            history = req_json.get("history", [])

            context_str = f"Сотрудник: {user_info.get('name', 'Алибек')}, Подразделение: {user_info.get('division', 'ОДС')}, Регион: {user_info.get('region', 'Атырау')}.\nСообщение: {user_message}"

            # 1. Вызов живой модели Gemini
            ai_result = call_gemini(INTAKE_MODEL, INTAKE_SYSTEM_INSTRUCTION, context_str)

            # 2. Резервный ответ (fallback), если ключ не задан или нет связи
            if not ai_result:
                is_conflict = any(m in user_message.lower() for m in ['мастер', 'начальник', 'бригадир', 'директор'])
                ai_result = {
                    "category_code": "HSE-01",
                    "category_title": "Охрана труда и СИЗ",
                    "conflict_guard": is_conflict,
                    "reply_text": f"Я зафиксировал обращение. Категория: Охрана труда и СИЗ (HSE-01).{' Активирован Conflict Guard: жалоба будет передана в ЦА минуя местное руководство.' if is_conflict else ''}",
                    "question": {
                        "text": "Какое именно снаряжение или СИЗ отсутствует?",
                        "options": ["Зимняя спецобувь и куртки", "Диэлектрический инструмент", "Каски и монтажные пояса"]
                    },
                    "formal_fabula": f"Заявление о нарушении ст. 182 ТК РК и п. 4.2 Коллективного договора. Суть: {user_message}",
                    "progress_pct": 45,
                    "source": "fallback_local"
                }
            else:
                ai_result["source"] = f"gemini_live ({INTAKE_MODEL})"

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(ai_result, ensure_ascii=False).encode("utf-8"))
            return

        # ---------------------------------------------------------------------
        # РОУТ 2: ИИ-АНАЛИТИК И АРХИТЕКТОР ДАШБОРДОВ (gemini-1.5-pro)
        # ---------------------------------------------------------------------
                # ---------------------------------------------------------------------
        # РОУТ 3: ИНТЕЛЛЕКТУАЛЬНЫЙ ПУЛЬС-ОПРОС (gemini-1.5-flash)
        # ---------------------------------------------------------------------
        if self.path == "/api/ai/survey":
            user_info = req_json.get("user", {})
            q_index = req_json.get("question_index", 0)
            score = req_json.get("score")
            text_ans = req_json.get("text", "")
            answers_so_far = req_json.get("answers", {})

            context_str = f"Сотрудник: {user_info.get('name', 'Алибек')}, ОДС Запад, Атырау. Текущий вопрос: {q_index}. Ответ: оценка {score}, текст: '{text_ans}'. Предыдущие ответы: {json.dumps(answers_so_far, ensure_ascii=False)}"

            ai_result = call_gemini(INTAKE_MODEL, SURVEY_SYSTEM_INSTRUCTION, context_str)
            if not ai_result:
                # Local fallback
                next_idx = q_index + 1
                is_fin = next_idx > 8
                synergy = (score is not None and int(score) <= 2)
                ai_result = {
                    "question_index": next_idx,
                    "is_finished": is_fin,
                    "progress_pct": min(100, int((next_idx / 8) * 100)),
                    "synergy_alert": synergy,
                    "synergy_message": "Вы поставили низкую оценку. Хотите составить официальное обращение по этому вопросу?" if synergy else "",
                    "message": "Спасибо за оценку. Переходим к следующему вопросу." if not is_fin else "Пульс-опрос успешно завершен!",
                    "srs_score": 64,
                    "source": "fallback_local"
                }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(ai_result, ensure_ascii=False).encode("utf-8"))
            return

        if self.path == "/api/ai/analytics":
            query = req_json.get("query", "")
            context_data = req_json.get("context", {})

            context_str = f"Запрос аналитика: {query}\nКонтекст: {json.dumps(context_data, ensure_ascii=False)}"

            # 1. Вызов живой модели Gemini
            ai_result = call_gemini(ANALYTICS_MODEL, ANALYTICS_SYSTEM_INSTRUCTION, context_str)

            # 2. Резервный ответ (fallback), если ключ не задан
            if not ai_result:
                ai_result = {
                    "title": f"ИИ-Анализ: {query}",
                    "summary": "Анализ подтверждает наличие зон высокого риска в филиалах ОДС Западного региона (Атырау 8.8, Мангистау 8.4). Главный триггер — срыв поставок СИЗ (>45 дней) и скрытые переработки.",
                    "kpis": [
                        {"label": "Критический очаг", "value": "ОДС Атырау (8.8/10)", "badge": "Критический", "color": "#EF4444"},
                        {"label": "Охват работников", "value": "280 сотрудников", "badge": "Высокий риск", "color": "#F59E0B"},
                        {"label": "Индекс SRS (Запад)", "value": "52.4%", "badge": "Красная зона", "color": "#EF4444"}
                    ],
                    "action_plan": [
                        "1. Срочная разгрузка партии СИЗ со склада СФ в г. Атырау (срок 24ч).",
                        "2. Тарификационный аудит переработок выездных бригад за октябрь-ноябрь 2026 г.",
                        "3. Организация выездной инспекции Департамента производственной безопасности."
                    ],
                    "is_board_report": "отчет" in query.lower() or "правлен" in query.lower(),
                    "source": "fallback_local"
                }
            else:
                ai_result["source"] = f"gemini_live ({ANALYTICS_MODEL})"

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(ai_result, ensure_ascii=False).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")

# -----------------------------------------------------------------------------
# 5. ЗАПУСК СЕРВЕРА
# -----------------------------------------------------------------------------
def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, EnterpriseAppHandler)
    print("=" * 70)
    print("🚀 КОРПОРАТИВНЫЙ BACKEND СЕРВЕР АО «КАЗАХТЕЛЕКОМ» ЗАПУЩЕН")
    print("=" * 70)
    print(f"📡 Адрес платформы:      http://localhost:{PORT}")
    print(f"🤖 Модель приемной:       {INTAKE_MODEL} (Служба приема обращений)")
    print(f"📊 Модель аналитики:     {ANALYTICS_MODEL} (Служба EX и Правление)")
    if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        masked = GEMINI_API_KEY[:6] + "..." + GEMINI_API_KEY[-4:]
        print(f"🔑 Gemini API Key:        Подключен ({masked})")
    else:
        print("⚠️ Gemini API Key:        Не настроен в .env (работает резервный офлайн-режим)")
        print("💡 Чтобы подключить живой ИИ: добавьте GEMINI_API_KEY=AIzaSy... в файл .env")
    print("=" * 70)
    print("Для завершения нажмите Ctrl+C\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

