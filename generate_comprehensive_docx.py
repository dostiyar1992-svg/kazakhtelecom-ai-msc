# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_comprehensive_tz_docx(filename="ТЗ_ИИ_Приемная_обращений_Казахтелеком_v5_2.docx"):
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

    # 1. ТИТУЛ
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

    r_sub = p_title.add_run("на внедрение комплексной системы «ИИ-Приемная обращений и мониторинг социального климата АО «Казахтелеком»:\nДиалоговое окно ИИ, динамический опросник, регистрация Канцелярией (Lotus Notes), маршрутизация, контроль SLA и аналитика»")
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = C_DARK

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_before = Pt(4)
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Версия: 5.2 (Итоговая расширенная редакция) | АО «Казахтелеком», г. Астана, 2026")
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = C_GRAY

    add_callout(
        "Настоящее ТЗ разработано с учетом результатов исследования CSCC 2025/2026 (SRS 64%, ИВ 70%, ИСБ 34%), "
        "Политики «нулевой терпимости» к давлению и моббингу, положений Коллективного договора АО «Казахтелеком» "
        "и норм Трудового кодекса РК. Система решает проблему неформального («серого») потока жалоб, "
        "консолидируя обращения на этапе 2 Канцелярии с обеспечением 100% анонимности заявителя.",
        "ОСНОВАНИЕ И КЛЮЧЕВЫЕ ТРЕБОВАНИЯ"
    )

    # 1. НАЗНАЧЕНИЕ И ЦЕЛИ
    add_h1("1. НАЗНАЧЕНИЕ, ЦЕЛИ И МЕТОДОЛОГИЯ СИСТЕМЫ")
    add_p("Система представляет собой программно-аппаратный комплекс для выявления, легализации, официальной регистрации и сквозного контроля разрешения жалоб и инцидентов социального характера в АО «Казахтелеком».")
    add_bullet("Ликвидация неформального («серого») потока обращений, поступающих напрямую исполнителям в мессенджерах и почте без регистрации;", bold_prefix="Цель 1: ")
    add_bullet("Диалоговый сбор фактуры на казахском и русском языках с помощью локальной On-Premise LLM;", bold_prefix="Цель 2: ")
    add_bullet("100% анонимность по умолчанию без ввода логина Keycloak с выдачей криптографического токена доступа (TK-XXXX-KZ);", bold_prefix="Цель 3: ")
    add_bullet("Регистрация в журнале Канцелярии с присвоением входящего номера (ВХ-2026/XXXX-КАНЦ);", bold_prefix="Цель 4: ")
    add_bullet("Автоматическая маршрутизация первому получателю с аппаратным исключением конфликта интересов (Conflict Guard);", bold_prefix="Цель 5: ")
    add_bullet("Контроль регламентных сроков ответа (SLA 5 дней) с автоматической эскалацией руководству при риске просрочки;", bold_prefix="Цель 6: ")
    add_bullet("Предиктивная аналитика очагов социальной напряженности и предотвращение забастовочных рисков.", bold_prefix="Цель 7: ")

    # 2. ОРГСТРУКТУРА
    add_h1("2. ОРГАНИЗАЦИОННАЯ СТРУКТУРА И КЛАССИФИКАТОРЫ")
    add_h2("2.1. Структурные подразделения (Дивизионы компании)")
    add_bullet("Объединение «Дивизион „Сеть“» (8 420 чел. — монтеры связи, спайщики, выездные бригады АВР, радиоузлы).", bold_prefix="ОДС: ")
    add_bullet("Сервисная фабрика (региональные склады материально-технического снабжения, автопарки и ремонтная база).", bold_prefix="СФ: ")
    add_bullet("Дивизион по розничному бизнесу (4 100 чел. — контакт-центры, абонентские отделы, точки обслуживания).", bold_prefix="ДРБ: ")
    add_bullet("Дивизион по корпоративному бизнесу (B2B и B2G клиенты).", bold_prefix="ДКБ: ")
    add_bullet("Дивизион «Телеком Комплект» (поставки кабельной продукции и оборудования).", bold_prefix="ДТК: ")
    add_bullet("Департамент производственной безопасности и экологии (Охрана труда, СИЗ, HSE).", bold_prefix="ДПБ: ")
    add_bullet("Департамент управления персоналом (Центральный HR и службы управления персоналом филиалов).", bold_prefix="ДУП: ")
    add_bullet("Дивизион цифрового бизнеса (IT-разработка, серверная инфраструктура ЦОД, телекоммуникации).", bold_prefix="ДЦБ: ")

    add_h2("2.2. Региональный охват (20 регионов Республики Казахстан)")
    add_p("Система охватывает все филиалы: города республиканского значения (Астана, Алматы, Шымкент), западный кластер повышенного внимания (Атырауская, Мангыстауская, Актюбинская, Западно-Казахстанская области), восточные и промышленные регионы (область Абай, ВКО, Карагандинская, область Ұлытау, Павлодарская), северный и южный филиалы (СКО, Акмолинская, Костанайская, Жамбылская, Туркестанская, Кызылординская, Алматинская и область Жетісу).")

    # 3. МАТРИЦА КАТЕГОРИЙ И SLA
    add_h1("3. МАТРИЦА КАТЕГОРИЙ ИНЦИДЕНТОВ И СРОКОВ РЕАГИРОВАНИЯ (SLA)")
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

    # 4. ПОШАГОВЫЙ ПРОЦЕСС
    add_h1("4. ПОШАГОВЫЙ ПРОЦЕСС ОБРАБОТКИ ОБРАЩЕНИЯ")
    add_bullet("Сотрудник переходит по QR-коду со смартфона без авторизации Keycloak. Описывает проблему своими словами в текстовом поле (или кликает быстрый сценарий).", bold_prefix="Шаг 1. Описание проблемы: ")
    add_bullet("ИИ парсит текст и выводит 3 целевых вопроса (филиал/дивизион, масштаб проблемы, предыстория обращения к мастеру).", bold_prefix="Шаг 2. Адаптивный опросник: ")
    add_bullet("ИИ синтезирует ответы в официальный проект заявления со ссылками на нарушенные пункты Колдоговора (п. 4.2) и статьи ТК РК (ст. 108, 182).", bold_prefix="Шаг 3. Проект заявления: ")
    add_bullet("Сотрудник выбирает режим: 🔒 Анонимно (выдается токен TK-XXXX-KZ) или 👤 Официально (с внесением учетных данных для бумажного ответа).", bold_prefix="Шаг 4. Выбор анонимности: ")
    add_bullet("Канцелярия фиксирует статус «В обработке», присваивает входящий номер формата ВХ-2026/XXXX-КАНЦ и точное серверное время.", bold_prefix="Шаг 5. Регистрация Канцелярией: ")
    add_bullet("ИИ назначает профильное подразделение. При наличии в жалобе данных о прямом начальнике — фигурант аппаратно исключается из расследования (Conflict Guard).", bold_prefix="Шаг 6. Назначение получателя: ")
    add_bullet("Включается 5-дневный живой таймер обратного отсчета с предупреждением за 24 часа и эскалацией Главному директору HRD при просрочке.", bold_prefix="Шаг 7. Контроль сроков (SLA): ")
    add_bullet("Все принятые обращения объединяются в кластеры очагов напряженности. ИИ формирует сводный текстовый отчет для членов Правления.", bold_prefix="Шаг 8. Сводная аналитика: ")

    # 5. ИНТЕГРАЦИЯ С LOTUS NOTES
    add_h1("5. ИНТЕГРАЦИЯ С КАНЦЕЛЯРИЕЙ (LOTUS NOTES) И «СЕРЫМ ПОТОКОМ»")
    add_p("Система реализует двухконтурную модель интеграции с корпоративной СЭД Lotus Notes:")
    add_bullet("Анонимные обращения регистрируются и разрешаются в защищенной базе ИИ-МСЦ без нарушения строгих требований Lotus Notes к реквизитам ФИО заявителя;", bold_prefix="Оперативный контур: ")
    add_bullet("Именные официальные обращения автоматически транслируются через Domino Mail-in Database в стандартные входящие карточки Lotus Notes;", bold_prefix="Официальный контур: ")
    add_bullet("Создается сервисный ящик signal@telecom.kz и надстройка Outlook. Исполнители пересылают письма в 1 клик, переводя скрытые жалобы в официальный учет МСЦ с таймером SLA.", bold_prefix="Легализация «серого потока»: ")

    # 6. БЕЗОПАСНОСТЬ ON-PREMISE
    add_h1("6. ТРЕБОВАНИЯ К БЕЗОПАСНОСТИ И ON-PREMISE ИНФРАСТРУКТУРЕ")
    add_bullet("Все компоненты языковой модели (Qwen 2.5 On-Premise) развертываются исключительно в изолированном ЦОД АО «Казахтелеком». Внешняя передача данных за пределы компании категорически запрещена.", bold_prefix="Локальный контур: ")
    add_bullet("Связка «Токен TK-XXXX-KZ <-> IP/сессия» хэшируется необратимым алгоритмом SHA-256 с солью, гарантируя невозможность деанонимизации сотрудника администратором.", bold_prefix="Криптография: ")
    add_bullet("Вход в рабочее место Канцелярии и Панель руководства защищен корпоративным Keycloak SSO с поддержкой MFA.", bold_prefix="Keycloak SSO: ")

    doc.save(filename)
    print(f"Comprehensive Word document successfully generated: {filename}")

if __name__ == "__main__":
    build_comprehensive_tz_docx()
