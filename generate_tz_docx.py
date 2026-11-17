# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_tz_docx(filename="ТЗ_ИИ_Мониторинг_Казахтелеком_v4.docx"):
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.8)

    C_NAVY = RGBColor(0, 70, 140)
    C_DARK = RGBColor(33, 37, 41)
    C_GRAY = RGBColor(108, 117, 125)
    C_LIGHT_BG = "F4F6F9"
    C_HEADER_BG = "00468C"

    def set_cell_shading(cell, color_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def format_table(tbl, col_widths, headers, data):
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_row = tbl.rows[0]
        for idx, text in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.text = text
            set_cell_shading(cell, C_HEADER_BG)
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
        for r_idx, row_data in enumerate(data):
            row = tbl.add_row()
            bg_color = "FFFFFF" if r_idx % 2 == 0 else "F9FAFC"
            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.text = str(val)
                set_cell_shading(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = C_DARK
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = C_NAVY

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = C_DARK

    def add_p(text="", bold_prefix=None, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.size = Pt(10)
            r_pre.font.color.rgb = C_DARK
        if text:
            r = p.add_run(text)
            r.italic = italic
            r.font.size = Pt(10)
            r.font.color.rgb = C_DARK
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.size = Pt(10)
            r_pre.font.color.rgb = C_DARK
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.color.rgb = C_DARK

    def add_callout(text, bold_title=None):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_shading(cell, C_LIGHT_BG)
        set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="00468C"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        cell._tc.get_or_add_tcPr().append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        if bold_title:
            r1 = p.add_run(bold_title + "\n")
            r1.bold = True
            r1.font.size = Pt(10)
            r1.font.color.rgb = C_NAVY
        r2 = p.add_run(text)
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_DARK
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_after = Pt(2)

    # Титул
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_top = p_top.add_run("УТВЕРЖДАЮ\nАО «Казахтелеком»\n«____» ___________ 2026 г.\n")
    r_top.font.size = Pt(9.5)
    r_top.font.color.rgb = C_GRAY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(4)
    r_main_title = p_title.add_run("ТЕХНИЧЕСКОЕ ЗАДАНИЕ\n")
    r_main_title.bold = True
    r_main_title.font.size = Pt(16)
    r_main_title.font.color.rgb = C_NAVY

    r_sub = p_title.add_run("на разработку системы «ИИ-мониторинг социального климата АО «Казахтелеком»:\nАдмин-панель пульс-опросов, диалоговое окно ИИ, Панель руководства (SRS и Пульс) и авторизация Keycloak»")
    r_sub.font.size = Pt(11.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_DARK

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(4)
    p_meta.paragraph_format.space_after = Pt(16)
    r_meta = p_meta.add_run("Версия: 4.0 (Итоговая согласованная) | г. Астана, 2026")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = C_GRAY

    add_callout(
        "Настоящая редакция ТЗ строго фиксирует ключевые архитектурные требования:\n"
        "1. Авторизация администраторов и руководства через корпоративный сервис Keycloak (SSO);\n"
        "2. Админ-панель открывается в отдельном окне, запуск опроса на N дней;\n"
        "3. Диалоговый опрос по 5 строго установленным вопросам;\n"
        "4. После дедлайна ИИ вскрывает массив ответов, строит таблицу и развернутый текстовый отчет;\n"
        "5. Панель руководства содержит два раздела: «Дашборд SRS» и «Дашборд Пульс-опроса» с краткими текстовыми описаниями.",
        "АРХИТЕКТУРНЫЕ ТРЕБОВАНИЯ"
    )

    # 1. Архитектура
    add_h1("1. АРХИТЕКТУРА И СОСТАВ СИСТЕМЫ")
    add_bullet("Вход в Админ-панель (ROLE_ADMIN) и Панель руководства (ROLE_EXECUTIVE) выполняется централизованно через корпоративный SSO-сервер.", bold_prefix="Сервис Keycloak: ")
    add_bullet("Отдельное веб-окно. Создание опроса, настройка срока проведения в днях, запуск/остановка, контроль динамики. После дедлайна — вскрытие ответов ИИ, публикация таблицы метрик и подробного аналитического отчета ИИ.", bold_prefix="Админ-панель (HR): ")
    add_bullet("Адаптивный чат для сотрудников со смартфона/ПК. Вход анонимный без Keycloak. ИИ задает строго установленные 5 вопросов и сохраняет ответы в зашифрованный пул.", bold_prefix="Модуль пульс-опроса: ")
    add_bullet("Два раздела: 1) Дашборд SRS + краткое описание трендов; 2) Дашборд Пульс-опроса + текстовое резюме отчета ИИ.", bold_prefix="Панель руководства: ")

    # 2. Механика
    add_h1("2. МЕХАНИКА РАБОТЫ И ПРОЦЕССЫ")
    add_h2("2.1. Запуск опроса и таймер N дней")
    add_p("HR в Админ-панели задает название, выбирает подразделение и указывает срок опроса в днях (например, 7 дней). Система генерирует короткую ссылку и защищенный QR-код, запуская таймер обратного отсчета.")

    add_h2("2.2. Прохождение опроса сотрудниками")
    add_p("Сотрудник переходит по ссылке или QR-коду (без логина). ИИ последовательно опрашивает его по 5 утвержденным осям: Q1 Зарплата, Q2 Обратная связь, Q3 Безопасность открытости, Q4 Доверие руководству, Q5 Моральное давление. Ответы падают в зашифрованный пул кампании.")

    add_h2("2.3. Вскрытие ответов и отчет ИИ")
    add_p("По истечении срока N дней опрос закрывается. По нажатию кнопки вскрытия локальная модель ИИ (On-Premise LLM) расшифровывает пул ответов и формирует:")
    add_bullet("Средние баллы 1–5 по 5 осям в разрезе подразделений, процент позитива/негатива.", bold_prefix="1. Сводную таблицу: ")
    add_bullet("Развернутый документ с анализом причин, скрытых очагов токсичности, перебоев с СИЗ/транспортом и рекомендациями для руководства.", bold_prefix="2. Текстовый отчет ИИ: ")

    add_h2("2.4. Панель руководства")
    add_bullet("Визуализация индексов исследования CSCC (SRS 64%, ИВ 70%, ИСБ 34%, ИСС 81%) + краткое пояснение красных зон и разрывов.", bold_prefix="Раздел Дашборд SRS: ")
    add_bullet("Визуализация свежих результатов последнего вскрытого опроса (тепловая карта, 5-осевой радар OCI, K-анонимность N>=5) + текстовая выжимка отчета ИИ.", bold_prefix="Раздел Дашборд Пульс: ")

    # 3. User Stories
    add_h1("3. USER STORIES (ПОЛЬЗОВАТЕЛЬСКИЕ СЦЕНАРИИ)")

    add_h2("US-01. Авторизация через Keycloak")
    add_p("Как администратор HR или представитель руководства, я хочу бесшовно войти в систему через единую корпоративную учетную запись Keycloak, чтобы получить доступ к своей панели по ролевой модели.", italic=True)
    add_bullet("Редирект на форму входа Keycloak при попытке открыть Админку или Панель руководства.", bold_prefix="AC-01.1: ")
    add_bullet("ROLE_ADMIN дает доступ к Админ-панели; ROLE_EXECUTIVE — к Панели руководства.", bold_prefix="AC-01.2: ")

    add_h2("US-02. Управление опросом с таймером на N дней в Админке")
    add_p("Как HR-администратор, я хочу создать опрос, выставить срок его проведения в днях и получить ссылку и QR-код, чтобы регламентированно собрать срез за фиксированный период.", italic=True)
    add_bullet("Поле выбора количества дней (таймер). По окончании срока опрос автоматически закрывается.", bold_prefix="AC-02.1: ")
    add_bullet("Во время опроса администратор видит счетчик участников без доступа к сырым ответам.", bold_prefix="AC-02.2: ")

    add_h2("US-03. Прохождение 5 строго установленных вопросов")
    add_p("Как сотрудник компании, я хочу быстро ответить на 5 утвержденных вопросов в диалоге с ИИ со смартфона, чтобы передать свое мнение без страха деанонимизации.", italic=True)
    add_bullet("Вход без авторизации Keycloak по ссылке/QR.", bold_prefix="AC-03.1: ")
    add_bullet("ИИ задает ровно 5 утвержденных вопросов на казахском или русском языке (Q1..Q5). Время опроса 60-90 сек.", bold_prefix="AC-03.2: ")

    add_h2("US-04. Вскрытие ответов и отчет ИИ в Админке")
    add_p("Как HR-администратор, я хочу по окончании срока вскрыть массив ответов и получить сводную таблицу с развернутым текстовым отчетом ИИ, чтобы быстро понять корневые проблемы.", italic=True)
    add_bullet("Кнопка вскрытия активна только после дедлайна или принудительного закрытия.", bold_prefix="AC-04.1: ")
    add_bullet("ИИ выдает таблицу средних баллов и формирует аналитический отчет с выводами и причинами.", bold_prefix="AC-04.2: ")

    add_h2("US-05. Просмотр Панели руководства с описаниями")
    add_p("Как руководитель компании, я хочу открыть Панель руководства и просмотреть разделы SRS и Пульс с текстовыми пояснениями, чтобы сразу видеть общую картину.", italic=True)
    add_bullet("В разделе SRS: графики годовых индексов + текст с анализом трендов.", bold_prefix="AC-05.1: ")
    add_bullet("В разделе Пульс: итоги последнего замера + текстовое резюме отчета ИИ.", bold_prefix="AC-05.2: ")

    # 4. Артефакты
    add_h1("4. СОПУТСТВУЮЩИЕ ИНЖЕНЕРНЫЕ АРТЕФАКТЫ")
    tbl_files = doc.add_table(rows=1, cols=3)
    format_table(
        tbl_files,
        [Inches(2.2), Inches(1.8), Inches(3.0)],
        ["Файл артефакта", "Формат / ПО", "Содержание и применение"],
        [
            ["er_diagram_kazakhtelecom.drawio", "draw.io / diagrams.net", "Физическая модель БД: KEYCLOAK_USER, SURVEY_CAMPAIGN (с таймингом), DIALOG_SESSION, SURVEY_ANSWER, AI_ANALYSIS_REPORT, SRS."],
            ["bpmn_pulse_survey_process.bpmn", "Camunda Modeler (BPMN 2.0)", "Сквозной процесс: 5 дорожек (Keycloak, Админ, Сотрудник, ИИ, Руководство), таймер N дней, вскрытие ответов."],
            ["srs_pulse_data_for_ai.xlsx", "Microsoft Excel", "Таблицы оргструктуры, фактические метрики SRS 2025/2026, спецификация 5 осей и датасет разметки для ИИ."]
        ]
    )

    # 5. Стек
    add_h1("5. СТЕК ТЕХНОЛОГИЙ И БЕЗОПАСНОСТЬ")
    add_bullet("Keycloak (OpenID Connect / OAuth 2.0). Роли: ROLE_ADMIN, ROLE_EXECUTIVE.", bold_prefix="Аутентификация: ")
    add_bullet("React 18 / Next.js, TailwindCSS (отдельные сборки для Админки, Панели руководства и чат-окна).", bold_prefix="Frontend: ")
    add_bullet("Python 3.11+, FastAPI (интеграция с Keycloak, асинхронные сокеты чата).", bold_prefix="Backend: ")
    add_bullet("PostgreSQL 16.", bold_prefix="База данных: ")
    add_bullet("vLLM / Ollama на внутренних GPU серверах АО «Казахтелеком». Модель Qwen 2.5 14B / 32B Instruct.", bold_prefix="Локальный ИИ: ")
    add_bullet("Сотрудники не авторизуются через Keycloak. K-анонимность N >= 5.", bold_prefix="Безопасность: ")

    # Подписи
    p_sign_head = doc.add_paragraph()
    p_sign_head.paragraph_format.space_before = Pt(24)
    p_sign_head.paragraph_format.space_after = Pt(8)
    r_sh = p_sign_head.add_run("ЛИСТ СОГЛАСОВАНИЯ")
    r_sh.bold = True
    r_sh.font.size = Pt(11)
    r_sh.font.color.rgb = C_NAVY

    tbl_sign = doc.add_table(rows=1, cols=2)
    tbl_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_l = tbl_sign.rows[0].cells[0]
    cell_r = tbl_sign.rows[0].cells[1]
    cell_l.width = Inches(3.4)
    cell_r.width = Inches(3.4)

    p_l = cell_l.paragraphs[0]
    p_l.add_run("От Службы управления персоналом:\n\n_____________________ / ____________ /\n«___» _____________ 2026 г.").font.size = Pt(9.5)
    
    p_r = cell_r.paragraphs[0]
    p_r.add_run("От Департамента информационных технологий:\n\n_____________________ / ____________ /\n«___» _____________ 2026 г.").font.size = Pt(9.5)

    doc.save(filename)
    print(f"File {filename} successfully generated! Size: {os.path.getsize(filename)} bytes")

if __name__ == "__main__":
    create_tz_docx()
