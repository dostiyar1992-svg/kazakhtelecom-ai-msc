# -*- coding: utf-8 -*-
"""
update_server_survey.py
Enhances server.py to support both:
- /api/ai/intake (Gemini 1.5 Flash for Grievance Intake & Labor Code citations)
- /api/ai/survey (Gemini 1.5 Flash for Autonomous Surveys based on project files)
- /api/ai/analytics (Gemini 1.5 Pro for BI Dashboards & Executive Reports)
"""

with open("server.py", "r", encoding="utf-8") as f:
    server_code = f.read()

# Replace or insert survey prompt and handler
survey_system_instruction = '''
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
'''

if "SURVEY_SYSTEM_INSTRUCTION" not in server_code:
    pos = server_code.find("ANALYTICS_SYSTEM_INSTRUCTION = ")
    server_code = server_code[:pos] + survey_system_instruction + "\n" + server_code[pos:]

survey_route_handler = '''        # ---------------------------------------------------------------------
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
'''

if 'self.path == "/api/ai/survey"' not in server_code:
    pos_route = server_code.find('if self.path == "/api/ai/analytics":')
    server_code = server_code[:pos_route] + survey_route_handler + "\n        " + server_code[pos_route:]

with open("server.py", "w", encoding="utf-8") as f:
    f.write(server_code)

print("server.py updated with /api/ai/survey route and SURVEY_SYSTEM_INSTRUCTION!")

