# -*- coding: utf-8 -*-
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_v6_docx(filename="ТЗ_ИИ_Приемная_обращений_Казахтелеком_v6.docx"):
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
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(4)
    r_main_title = p_title.add_run("ТЕХНИЧЕСКОЕ ЗАДАНИЕ\n")
    r_main_title.bold = True
    r_main_title.font.size = Pt(16)
    r_main_title.font.color.rgb = C_NAVY

    r_sub = p_title.add_run("на внедрение комплексной системы «ИИ-Приемная обращений, регулярные пульс-опросы и мониторинг социального климата АО «Казахтелеком»:\nАвторизация CDN, чекин-окно, диалог с ИИ, самостоятельное заполнение формы, регистрация Канцелярией (Lotus Notes), маршрутизация и контроль SLA»")
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_DARK

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(4)
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Версия: 6.0 (Гибридная модель: Пульс-опросы + Прием обращений) | АО «Казахтелеком», г. Астана, 2026")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = C_GRAY

    add_callout(
        "Настоящая редакция ТЗ объединяет два контура: регулярные ежеквартальные пульс-опросы "
        "(уведомления на телефон, почту Outlook, Lotus Notes) и интеллектуальный прием обращений через "
        "CDN-чекин, диалог с ИИ-агентом или самостоятельную форму заявления. Система интегрирована с "
        "Канцелярией АО «Казахтелеком» с контролем регламентных сроков SLA 5 дней и аппаратной защитой от конфликта интересов.",
        "КЛЮЧЕВЫЕ ТРЕБОВАНИЯ ВЕРСИИ 6.0"
    )

    # 1. ОБЩЕЕ
    add_h1("1. АВТОРИЗАЦИЯ ЧЕРЕЗ CDN И ВОВЛЕКАЮЩЕЕ ОКНО (NUDGE MODAL)")
    add_bullet("Пользователь авторизуется в корпоративной среде через корпоративный CDN / Active Directory / Keycloak.", bold_prefix="Вход через CDN: ")
    add_bullet("Поверх экрана всплывает приветственное модальное окно («Все ли у вас в порядке? Есть ли проблемы в компании? Хотите ли вы об этом поговорить?»).", bold_prefix="Модальное окно чекина: ")
    add_bullet("1) Да, есть проблема (переход к диалогу с ИИ); 2) Пройти квартальный пульс-опрос; 3) Заполнить обращение вручную; 4) Все отлично (закрытие).", bold_prefix="4 сценария действий: ")

    # 2. ПУЛЬС-ОПРОСЫ
    add_h1("2. РЕГУЛЯРНЫЕ ЕЖЕКВАРТАЛЬНЫЕ ПУЛЬС-ОПРОСЫ")
    add_bullet("Один раз в квартал (Q1, Q2, Q3, Q4) запускается общекорпоративная кампания сбора обратной связи.", bold_prefix="Периодичность: ")
    add_bullet("Push-уведомление на смартфон, персональное письмо в Outlook, информационное сообщение в Lotus Notes.", bold_prefix="Каналы оповещения: ")
    add_bullet("Блок 1: Социальный климат и СИЗ; Блок 2: Отношение к компании (eNPS); Блок 3: Атмосфера в коллективе и психологическая безопасность.", bold_prefix="3 ключевые оси: ")
    add_bullet("При оценках 1–2 балла по критическим вопросам ИИ прямо в опросе предлагает оформить официальное обращение в Канцелярию.", bold_prefix="Синергия с обращениями: ")

    # 3. ДВА СПОСОБА ПОДАЧИ
    add_h1("3. ПРИЕМ ОБРАЩЕНИЙ: ДИАЛОГ С ИИ VS САМОСТОЯТЕЛЬНАЯ ФОРМА")
    add_h2("3.1. Интеллектуальный диалог с ИИ-агентом")
    add_p("Сотрудник своими словами описывает проблему -> ИИ составляет динамический опросник из 3 вопросов -> формирует официальное заявление со статьями ТК РК (ст. 108, 182) -> предлагает анонимность (токен TK-XXXX-KZ) -> регистрирует в Канцелярии с номером ВХ-2026/XXXX-КАНЦ -> определяет получателя с Conflict Guard -> запускает таймер SLA.")

    add_h2("3.2. Самостоятельное заполнение формы (Self-service)")
    add_p("Пользователь может в 1 клик перейти во вкладку обращений и вручную выбрать дивизион (ОДС, СФ, ДРБ и др.), один из 20 регионов Казахстана, категорию нарушения, написать фабулу, прикрепить файлы (фото дефектных СИЗ, акты) и направить сразу на регистрацию.")

    # 4. КАНЦЕЛЯРИЯ И SLA
    add_h1("4. КАНЦЕЛЯРИЯ, LOTUS NOTES И КОНТРОЛЬ СРОКОВ (SLA)")
    col_w = [Inches(1.0), Inches(2.2), Inches(2.2), Inches(1.2), Inches(1.2)]
    headers = ["Код", "Категория проблемы", "Первый получатель", "Срок SLA", "Уровень риска"]
    data = [
        ["HSE-01", "Охрана труда: задержка зимней обуви и спецодежды (СИЗ)", "Департамент производственной безопасности (ДПБ)", "5 раб. дней", "Желтый"],
        ["PAY-02", "Оплата труда: невыплата надбавок, ночных, праздничных", "Департамент оплаты труда (ДУП)", "5 раб. дней", "Желтый"],
        ["OT-03", "Принуждение к неоплачиваемым сверхурочным по субботам", "Департамент управления персоналом + Профсоюз", "3 раб. дня", "Желтый"],
        ["MOB-04", "Моббинг, грубость, давление, угрозы от начальника", "Служба комплаенс и Омбудсмен компании", "7 раб. дней", "Оранжевый"],
        ["EMG-05", "Угроза забастовки, коллективного отказа от выезда, ЧП", "Центр социального партнерства (МСЦ) / HRD", "24-48 часов", "КРАСНЫЙ"],
        ["TECH-06", "Износ транспорта АВР (УАЗ), поломки дизель-генераторов", "Дивизион «Сеть» (ОДС) / Сервисная фабрика (СФ)", "3 раб. дня", "Желтый"],
        ["LIFE-07", "Бытовые условия на объектах (отопление, вода, свет)", "Административно-хозяйственный департамент (АХД)", "5 раб. дней", "Зеленый"]
    ]
    tbl = doc.add_table(rows=1, cols=5)
    format_table(tbl, col_w, headers, data)

    doc.save(filename)
    print(f"Word doc v6 successfully generated: {filename}")

if __name__ == "__main__":
    build_v6_docx()

