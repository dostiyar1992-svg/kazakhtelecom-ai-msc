# -*- coding: utf-8 -*-
"""
Generate appeals_registry_data.xlsx:
Реалистичный массив из 420 обращений для АО «Казахтелеком»
с распределением по дивизионам (ОДС, СФ, ДРБ и др.), 20 регионам,
категориям (HSE, PAY, OT, MOB, EMG), статусам и таймерам SLA.
"""
import random
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_appeals_excel(filename="appeals_registry_data.xlsx"):
    wb = openpyxl.Workbook()
    wb.remove(wb.active) # Remove default sheet

    # Colors & styles
    NAVY = "00468C"
    WHITE = "FFFFFF"
    GRAY_BG = "F4F6F9"
    BORDER_COLOR = "D0D5DD"
    GREEN_BG = "DCFCE7"
    YELLOW_BG = "FEF3C7"
    RED_BG = "FEE2E2"

    font_hdr = Font(name="Calibri", size=11, bold=True, color=WHITE)
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_main = Font(name="Calibri", size=10)
    font_title = Font(name="Calibri", size=14, bold=True, color=NAVY)

    fill_hdr = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_alt = PatternFill(start_color=GRAY_BG, end_color=GRAY_BG, fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )

    # 1. SHEET 1: РЕЕСТР ОБРАЩЕНИЙ (420 строк)
    ws1 = wb.create_sheet(title="Реестр_Обращений_2026")
    
    headers1 = [
        "ID", "Входящий номер", "Секретный токен", "Дата регистрации", 
        "Режим подачи", "ФИО заявителя (если открыто)", "Дивизион", 
        "Регион (Область / Город)", "Должностная категория", "Код категории", 
        "Категория обращения", "Суть инцидента (Фабула ИИ)", 
        "Первый получатель", "Статус обращения", "Нормативный SLA (дней)", 
        "Остаток по SLA", "Уровень риска", "Исключен конфликт интересов"
    ]

    ws1.append(headers1)
    for col_idx in range(1, len(headers1) + 1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.font = font_hdr
        cell.fill = fill_hdr
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws1.row_dimensions[1].height = 28

    divisions = [
        ("ОДС", "Объединение «Дивизион „Сеть“»", 0.45),
        ("СФ", "Сервисная фабрика", 0.18),
        ("ДРБ", "Дивизион по розничному бизнесу", 0.18),
        ("ДКБ", "Дивизион по корпоративному бизнесу", 0.07),
        ("ДТК", "Дивизион «Телеком Комплект»", 0.04),
        ("ДУП", "Департамент управления персоналом", 0.03),
        ("ДЦБ", "Дивизион цифрового бизнеса", 0.03),
        ("ЦА", "Центральный аппарат", 0.02)
    ]

    regions = [
        "Атырауская область", "Мангыстауская область", "Западно-Казахстанская область", "Актюбинская область",
        "область Абай (г. Семей)", "Восточно-Казахстанская область", "Карагандинская область", "область Ұлытау", "Павлодарская область",
        "г. Астана", "г. Алматы", "г. Шымкент", "Акмолинская область", "Костанайская область", "Северо-Казахстанская область",
        "Алматинская область", "область Жетісу", "Жамбылская область", "Кызылординская область", "Туркестанская область"
    ]

    roles = [
        ("Рабочий / монтажник / электромонтер связи", 0.52),
        ("Водитель АВР / спецтехники", 0.18),
        ("ИТР / инженер электросвязи", 0.18),
        ("Специалист офиса / абонентского отдела", 0.12)
    ]

    categories = [
        ("HSE-01", "Охрана труда и СИЗ", "Департамент производственной безопасности (ДПБ)", 5, "Желтый", [
            "Задержка выдачи зимней обуви и утепленных курток для бригад АВР более 45 дней.",
            "Отсутствие термозащитных перчаток и диэлектрического инструмента на участке.",
            "Задержка плановой поверки поясов монтерских и защитных касок."
        ]),
        ("PAY-02", "Оплата труда и надбавки", "Департамент оплаты труда (ДУП)", 5, "Желтый", [
            "Неначисление надбавки за работу в ночное время и праздничные дни.",
            "Задержка выплаты компенсаций за разъездной характер работы и личный транспорт.",
            "Некорректный расчет премии по итогам квартала без объяснения оснований."
        ]),
        ("OT-03", "Принуждение к сверхурочным", "Департамент управления персоналом + Профсоюз", 3, "Желтый", [
            "Принуждение к выходу в субботу без табелирования и двойной оплаты под угрозой лишения премии.",
            "Переработки сверх 40 часов в неделю на аварийных работах без приказа.",
            "Отказ руководства предоставить отгулы за ранее отработанные дежурства."
        ]),
        ("MOB-04", "Моббинг и давление руководства", "Служба комплаенс и Омбудсмен", 7, "Оранжевый", [
            "Грубость, оскорбления и угрозы увольнением со стороны начальника цеха.",
            "Предвзятое отношение и необоснованное дисциплинарное давление со стороны мастера.",
            "Игнорирование инициатив и психологический прессинг за обращение в профком."
        ]),
        ("TECH-06", "Износ транспорта и оборудования", "Дивизион «Сеть» (ОДС) / Сервисная фабрика", 3, "Желтый", [
            "Служебный УАЗ бригады АВР находится в аварийном состоянии, постоянные поломки на линии.",
            "Неисправность дизель-генератора на узле связи, угроза отключения базовых станций.",
            "Отсутствие запчастей и комплектующих для сварочных аппаратов ВОЛС."
        ]),
        ("EMG-05", "Угроза забастовки / ЧП", "Центр социального партнерства (МСЦ) / HRD", 2, "КРАСНЫЙ", [
            "Коллективное заявление бригады монтеров (18 чел) о приостановке работы в связи с отсутствием зимней обуви на морозе.",
            "Предупреждение о коллективном отказе выезжать на ночные аварии без официального табелирования."
        ]),
        ("LIFE-07", "Бытовые условия на объектах", "Административно-хозяйственный департамент", 5, "Зеленый", [
            "Отсутствие отопления в комнате приема пищи районного узла телекоммуникаций.",
            "Перебои с питьевой водой и освещением на отдаленном ретрансляторе связи."
        ])
    ]

    random.seed(42)
    start_date = datetime(2026, 10, 1)

    for i in range(1, 421):
        reg_num = f"ВХ-2026/{1000 - i:04d}-КАНЦ"
        token = f"TK-{random.randint(1000, 9999)}-KZ"
        reg_time = start_date + timedelta(days=random.randint(0, 39), hours=random.randint(8, 18), minutes=random.randint(0, 59))
        
        # 76% anonymous
        is_anon = random.random() < 0.76
        fio = "— (Анонимно)" if is_anon else random.choice(["Искаков М.А.", "Смаилов К.Т.", "Ахметов Д.Б.", "Омаров С.К.", "Касымова А.Н."])

        # Division
        div_rand = random.random()
        cum = 0
        selected_div = "ОДС"
        for code, name, p in divisions:
            cum += p
            if div_rand <= cum:
                selected_div = code
                break

        # Western regions weight higher for ODS
        if selected_div == "ОДС" and random.random() < 0.4:
            reg = random.choice(["Атырауская область", "Мангыстауская область", "Западно-Казахстанская область"])
        else:
            reg = random.choice(regions)

        role = random.choices([r[0] for r in roles], weights=[r[1] for r in roles])[0]

        # Category
        cat_item = random.choices(categories, weights=[0.38, 0.28, 0.14, 0.10, 0.05, 0.03, 0.02])[0]
        cat_code, cat_title, recipient, sla_days, risk, fabulas = cat_item
        fabula = random.choice(fabulas)

        # Status & SLA
        days_passed = (datetime(2026, 11, 9) - reg_time).days
        if days_passed > sla_days:
            if random.random() < 0.88:
                status = "Решено • Ответ дан"
                sla_rem = "0 дн (в срок)"
            else:
                status = "⚠️ ПРОСРОЧЕНО (Эскалация)"
                sla_rem = f"-{days_passed - sla_days} дн"
        else:
            status = "В работе у исполнителя"
            sla_rem = f"{sla_days - days_passed} дн"

        conflict_guard = "ДА (Фигурант отстранен)"

        row_data = [
            i, reg_num, token, reg_time.strftime("%d.%m.%2026 %H:%M"),
            "🔒 Анонимно" if is_anon else "👤 Официально",
            fio, selected_div, reg, role, cat_code, cat_title,
            fabula, recipient, status, sla_days, sla_rem, risk, conflict_guard
        ]

        ws1.append(row_data)
        r_idx = i + 1
        ws1.row_dimensions[r_idx].height = 20
        is_alt = (i % 2 == 1)
        for c_idx in range(1, len(row_data) + 1):
            cell = ws1.cell(row=r_idx, column=c_idx)
            cell.font = font_main
            cell.border = thin_border
            if is_alt:
                cell.fill = fill_alt
            if "ПРОСРОЧЕНО" in str(row_data[13]):
                cell.fill = PatternFill(start_color=RED_BG, end_color=RED_BG, fill_type="solid")
            elif "Решено" in str(row_data[13]):
                if c_idx == 14:
                    cell.fill = PatternFill(start_color=GREEN_BG, end_color=GREEN_BG, fill_type="solid")

    # Auto-adjust column widths for sheet 1
    for col in ws1.columns:
        max_len = max(len(str(cell.value or '')) for cell in col[:15])
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

    # 2. SHEET 2: СИСТЕМНЫЕ ОЧАГИ ИИ
    ws2 = wb.create_sheet(title="Системные_Очаги_ИИ")
    headers2 = ["ID Очага", "Название системного очага", "Дивизион", "Регион", "Кол-во обращений", "Уровень риска", "Индекс риска забастовки (0-10)", "Ключевая первопричина", "Рекомендованные меры руководству"]
    ws2.append(headers2)
    for col_idx in range(1, len(headers2) + 1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.font = font_hdr
        cell.fill = fill_hdr
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws2.row_dimensions[1].height = 28

    clusters = [
        (1, "Задержка зимней обуви и курток монтерам АВР", "ОДС", "Атырауская / Мангыстауская обл.", 69, "КРАСНЫЙ", 8.8, "Срыв сроков поставки поставщиком по договору №КТ-492", "Экстренная отгрузка 240 пар обуви со склада ЦА, ревизия складских остатков"),
        (2, "Неоплачиваемые сверхурочные по субботам", "ОДС", "область Абай / ВКО", 34, "Желтый", 6.2, "Дефицит штатной численности бригад при росте аварийности ВОЛС", "Введение доплаты за переработки согласно ст. 108 ТК РК, аудит графиков сменности"),
        (3, "Аварийное состояние автопарка УАЗ в районах", "СФ", "Карагандинская / Акмолинская обл.", 28, "Желтый", 5.5, "Задержка закупки автозапчастей Сервисной фабрикой", "Выделение целевого аванса на локальный ремонт машин АВР"),
        (4, "Моббинг и давление начальника участка связи", "ДРБ", "г. Алматы", 14, "Оранжевый", 4.8, "Авторитарный стиль руководства, угрозы депремирования", "Проведение проверки Службой комплаенс, отстранение начальника на период аудита"),
        (5, "Перебои с питанием и генераторами на узлах", "ОДС", "Северо-Казахстанская обл.", 11, "Желтый", 4.1, "Износ аккумуляторных батарей и резервных дизелей", "Плановая замена АКБ на опорных ретрансляторах")
    ]

    for cl in clusters:
        ws2.append(list(cl))
        r = ws2.max_row
        ws2.row_dimensions[r].height = 24
        for c_idx in range(1, len(cl) + 1):
            cell = ws2.cell(row=r, column=c_idx)
            cell.font = font_main
            cell.border = thin_border
            if cl[5] == "КРАСНЫЙ":
                cell.fill = PatternFill(start_color=RED_BG, end_color=RED_BG, fill_type="solid")

    for col in ws2.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws2.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 50)

    # 3. SHEET 3: СВОДНАЯ СТАТИСТИКА SLA
    ws3 = wb.create_sheet(title="Сводная_Статистика_SLA")
    headers3 = ["Дивизион", "Всего обращений", "Решено в срок", "В процессе (в графике)", "Просрочено", "% Соблюдения SLA", "Средний срок ответа (дни)"]
    ws3.append(headers3)
    for col_idx in range(1, len(headers3) + 1):
        cell = ws3.cell(row=1, column=col_idx)
        cell.font = font_hdr
        cell.fill = fill_hdr
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws3.row_dimensions[1].height = 28

    sla_stats = [
        ("ОДС (Дивизион „Сеть“)", 192, 148, 38, 6, "96.9%", 4.1),
        ("СФ (Сервисная фабрика)", 76, 59, 15, 2, "97.4%", 3.8),
        ("ДРБ (Розничный бизнес)", 74, 62, 11, 1, "98.6%", 3.4),
        ("ДКБ (Корпоративный бизнес)", 30, 26, 4, 0, "100.0%", 2.9),
        ("ДТК (Телеком Комплект)", 18, 15, 3, 0, "100.0%", 3.1),
        ("ДУП / ДПБ / Прочие", 30, 27, 3, 0, "100.0%", 2.6),
        ("ИТОГО ПО КОМПАНИИ", 420, 337, 74, 9, "97.9%", 3.7)
    ]

    for st in sla_stats:
        ws3.append(list(st))
        r = ws3.max_row
        ws3.row_dimensions[r].height = 22
        for c_idx in range(1, len(st) + 1):
            cell = ws3.cell(row=r, column=c_idx)
            cell.font = font_bold if "ИТОГО" in st[0] else font_main
            cell.border = thin_border
            if "ИТОГО" in st[0]:
                cell.fill = PatternFill(start_color="EBF3FA", end_color="EBF3FA", fill_type="solid")

    for col in ws3.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws3.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 35)

    wb.save(filename)
    print(f"Excel appeals database generated: {filename}")

if __name__ == "__main__":
    build_appeals_excel()

