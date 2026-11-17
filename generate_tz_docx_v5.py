# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_tz_v5_docx(filename="ТЗ_ИИ_Приемная_обращений_Казахтелеком_v5.docx"):
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

    r_sub = p_title.add_run("на внедрение системы «ИИ-Приемная обращений и мониторинг социального климата АО «Казахтелеком»:\nДиалоговое окно ИИ, адаптивный опросник, регистрация канцелярией, маршрутизация первому получателю, контроль SLA и аналитика»")
    r_sub.font.size = Pt(11.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_DARK

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(4)
    p_meta.paragraph_format.space_after = Pt(16)
    r_meta = p_meta.add_run("Версия: 5.0 (Переход на обработку обращений и жалоб) | г. Астана, 2026")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = C_GRAY

    add_callout(
        "Ключевые функциональные требования системы:\n"
        "1. Первичное описание проблемы сотрудником своими словами в диалоговом окне с ИИ;\n"
        "2. Генерация адаптивного опросника локальной моделью ИИ и ответы сотрудника;\n"
        "3. Автоматическое формирование официального заявления и согласование анонимности;\n"
        "4. Регистрация в Канцелярии с присвоением входящего номера и трек-токена TK-XXXX;\n"
        "5. Автоматическое определение первого получателя с фильтром конфликта интересов;\n"
        "6. Контроль дедлайнов ответа (SLA-таймер 5 дней) и автоматическая эскалация;\n"
        "7. Генерация сводного аналитического отчета ИИ и тепловой карты очагов напряженности.",
        "ОСНОВНЫЕ ТРЕБОВАНИЯ"
    )

    # 1. Архитектура
    add_h1("1. АРХИТЕКТУРА И СОСТАВ СИСТЕМЫ")
    add_bullet("Диалоговый модуль с локальной LLM. Прием обращений на казахском и русском языках, проведение адаптивного опроса, выдача секретных токенов доступа.", bold_prefix="ИИ-Приемная (Сотрудник): ")
    add_bullet("Рабочее место Канцелярии ЦА и МСЦ. Сквозной реестр входящих обращений, легализация писем из Outlook/WhatsApp, контроль активных таймеров SLA.", bold_prefix="Реестр Канцелярии & SLA: ")
    add_bullet("Семантический парсинг, классификация, выявление забастовочных триггеров, дедупликация и объединение массовых жалоб в очаги.", bold_prefix="Серверное ИИ-ядро (On-Premise): ")
    add_bullet("Сводный текстовый отчет ИИ по всем принятым обращениям, тепловая карта регионов, статистика дисциплины исполнителей.", bold_prefix="Панель руководства: ")

    # 2. Пошаговая механика
    add_h1("2. ПОШАГОВЫЙ ПРОЦЕСС ОБРАБОТКИ ОБРАЩЕНИЯ")
    add_bullet("Сотрудник переходит по защищенной ссылке/QR и в свободной форме описывает проблему (СИЗ, переработки, давление, связь).", bold_prefix="Шаг 1. Описание проблемы: ")
    add_bullet("ИИ классифицирует инцидент и задает 3 целевых вопроса (филиал, масштаб проблемы, предыстория обращений).", bold_prefix="Шаг 2. Адаптивный опросник: ")
    add_bullet("Нейросеть генерирует структурированный документ с фабулой нарушения, ссылками на ТК РК и коллективный договор.", bold_prefix="Шаг 3. Формирование заявления: ")
    add_bullet("Заявитель выбирает режим: 100% анонимно (токен TK-XXXX-KZ) или официально (с внесением учетных данных).", bold_prefix="Шаг 4. Выбор анонимности: ")
    add_bullet("Канцелярия присваивает входящий номер (ВХ-2026/XXXX-КАНЦ) и фиксирует статус «В обработке».", bold_prefix="Шаг 5. Регистрация в канцелярии: ")
    add_bullet("ИИ определяет профильное подразделение и исключает фигурантов жалобы из комиссии рассмотрения.", bold_prefix="Шаг 6. Назначение получателя: ")
    add_bullet("Включается 5-дневный нормативный таймер обратного отсчета с предупреждением за 24 часа и эскалацией HRD.", bold_prefix="Шаг 7. Контроль сроков (SLA): ")
    add_bullet("По всем принятым обращениям ИИ формирует пакетный аналитический отчет для Правления.", bold_prefix="Шаг 8. Сводная аналитика: ")

    # 3. Таблица маршрутизации
    add_h1("3. МАТРИЦА КЛАССИФИКАЦИИ И СРОКОВ (SLA)")
    col_w = [Inches(1.8), Inches(1.8), Inches(1.5), Inches(1.5)]
    headers = ["Категория инцидента", "Первый получатель", "Нормативный SLA", "Уровень риска"]
    data = [
        ["Охрана труда и СИЗ", "Департамент охраны труда (HSE)", "5 рабочих дней", "Желтый (Системный)"],
        ["Оплата труда и надбавки", "Департамент оплаты труда", "5 рабочих дней", "Желтый (Системный)"],
        ["Угроза забастовки / ЧП", "Центр соцпартнерства (МСЦ) / HRD", "24-48 часов", "Красный (Критический)"],
        ["Инфраструктура и связь", "Дивизион «Сеть» (ОДС)", "3 рабочих дня", "Желтый / Оранжевый"],
        ["Моббинг / Давление", "Служба комплаенс / Омбудсмен", "7 рабочих дней", "Оранжевый"],
        ["Бытовые условия труда", "Административный департамент", "5 рабочих дней", "Зеленый (Локальный)"]
    ]
    tbl = doc.add_table(rows=1, cols=4)
    format_table(tbl, col_w, headers, data)

    doc.save(filename)
    print(f"Docx successfully saved: {filename}")

if __name__ == "__main__":
    create_tz_v5_docx()

