# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def create_appeals_camunda_bpmn(filename="bpmn_appeals_process.bpmn"):
    BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
    BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
    DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
    DI_NS = "http://www.omg.org/spec/DD/20100524/DI"
    CAMUNDA_NS = "http://camunda.org/schema/1.0/bpmn"

    ET.register_namespace("bpmn", BPMN_NS)
    ET.register_namespace("bpmndi", BPMNDI_NS)
    ET.register_namespace("dc", DC_NS)
    ET.register_namespace("di", DI_NS)
    ET.register_namespace("camunda", CAMUNDA_NS)

    definitions = ET.Element(
        f"{{{BPMN_NS}}}definitions",
        id="Definitions_HybridAppealsAndPulse",
        targetNamespace="http://bpmn.io/schema/bpmn",
        exporter="Camunda Modeler",
        exporterVersion="5.20.0"
    )

    collaboration = ET.SubElement(definitions, f"{{{BPMN_NS}}}collaboration", id="Collaboration_Hybrid")
    participant = ET.SubElement(
        collaboration,
        f"{{{BPMN_NS}}}participant",
        id="Participant_Hybrid",
        name="АО «Казахтелеком» — Гибридный процесс: Пульс-опросы, CDN-чекин, прием жалоб и контроль SLA",
        processRef="Process_Hybrid"
    )

    process = ET.SubElement(definitions, f"{{{BPMN_NS}}}process", id="Process_Hybrid", isExecutable="true")
    laneSet = ET.SubElement(process, f"{{{BPMN_NS}}}laneSet", id="LaneSet_Hybrid")

    lane_emp = ET.SubElement(laneSet, f"{{{BPMN_NS}}}lane", id="Lane_Employee", name="Сотрудник (CDN-пользователь)")
    lane_ai = ET.SubElement(laneSet, f"{{{BPMN_NS}}}lane", id="Lane_AI_Core", name="ИИ-Ассистент (Чекин, Опросник, Аналитика)")
    lane_canc = ET.SubElement(laneSet, f"{{{BPMN_NS}}}lane", id="Lane_Chancellery", name="Канцелярия (Lotus Notes / СЭД)")
    lane_exec = ET.SubElement(laneSet, f"{{{BPMN_NS}}}lane", id="Lane_Executor", name="Первый получатель (Исполнитель)")
    lane_lead = ET.SubElement(laneSet, f"{{{BPMN_NS}}}lane", id="Lane_Leadership", name="Руководство (Аналитика и Отчеты ИИ)")

    nodes = [
        # Employee
        ("StartEvent_CDN", "bpmn:startEvent", "Авторизация через корпоративный CDN", lane_emp),
        ("Task_ViewNudge", "bpmn:userTask", "Чекин-окно: Все ли в порядке?", lane_emp),
        ("Gateway_UserChoice", "bpmn:exclusiveGateway", "Выбор действия", lane_emp),
        ("Task_AnswerPulse", "bpmn:userTask", "Прохождение квартального пульс-опроса", lane_emp),
        ("Task_DirectFormFill", "bpmn:userTask", "Самостоятельное заполнение формы обращения", lane_emp),
        ("Task_DescribeProblem", "bpmn:userTask", "Диалог с ИИ: описание проблемы своими словами", lane_emp),
        ("Task_AnswerQuestions", "bpmn:userTask", "Ответы на уточняющий опросник ИИ", lane_emp),
        ("Task_SelectAnonymity", "bpmn:userTask", "Выбор режима: Анонимно или Официально", lane_emp),
        ("Task_TrackStatus", "bpmn:userTask", "Проверка статуса по токену TK-XXXX-KZ", lane_emp),
        ("EndEvent_Emp", "bpmn:endEvent", "Вопрос решен, ответ получен", lane_emp),

        # AI Core
        ("Task_AI_AnalyzePulse", "bpmn:serviceTask", "Анализ пульс-опроса (проверка низких баллов)", lane_ai),
        ("Gateway_PulseAlert", "bpmn:exclusiveGateway", "Балл <= 2 или тревожный сигнал?", lane_ai),
        ("Task_AI_ParseAndSurvey", "bpmn:serviceTask", "Анализ проблемы и формирование опросника", lane_ai),
        ("Task_AI_DraftStatement", "bpmn:serviceTask", "Формирование официального заявления по ТК РК", lane_ai),
        ("Task_AI_RouteAndSLA", "bpmn:serviceTask", "Определение первого получателя (Conflict Guard) и SLA", lane_ai),
        ("Task_AI_MonitorSLA", "bpmn:serviceTask", "Контроль дедлайна (5 дней) и эскалация", lane_ai),
        ("Task_AI_GenerateReports", "bpmn:serviceTask", "Сводная аналитика климата и выявление очагов", lane_ai),

        # Chancellery
        ("Task_RegisterIncoming", "bpmn:userTask", "Регистрация в Канцелярии (ВХ-2026/XXXX-КАНЦ)", lane_canc),
        ("Task_ForwardToRecipient", "bpmn:serviceTask", "Передача дела назначенному исполнителю", lane_canc),

        # Executor
        ("Task_ReviewComplaint", "bpmn:userTask", "Рассмотрение и устранение нарушения", lane_exec),
        ("Task_SubmitResponse", "bpmn:userTask", "Направление ответа в срок SLA", lane_exec),

        # Leadership
        ("Task_ViewExecutiveDashboard", "bpmn:userTask", "Изучение отчета ИИ и карты очагов напряженности", lane_lead),
        ("EndEvent_Done", "bpmn:endEvent", "Превентивные меры приняты Правлением", lane_lead),
    ]

    for node_id, node_type, node_name, lane_parent in nodes:
        elem_tag = node_type.replace("bpmn:", f"{{{BPMN_NS}}}")
        elem = ET.SubElement(process, elem_tag, id=node_id, name=node_name)
        fl_ref = ET.SubElement(lane_parent, f"{{{BPMN_NS}}}flowNodeRef")
        fl_ref.text = node_id

    flows = [
        ("Flow_1", "StartEvent_CDN", "Task_ViewNudge"),
        ("Flow_2", "Task_ViewNudge", "Gateway_UserChoice"),
        ("Flow_3", "Gateway_UserChoice", "Task_DescribeProblem", "Да, есть проблема"),
        ("Flow_4", "Gateway_UserChoice", "Task_AnswerPulse", "Пройти пульс-опрос"),
        ("Flow_5", "Gateway_UserChoice", "Task_DirectFormFill", "Заполнить форму прямо"),
        
        # Pulse Flow
        ("Flow_P1", "Task_AnswerPulse", "Task_AI_AnalyzePulse"),
        ("Flow_P2", "Task_AI_AnalyzePulse", "Gateway_PulseAlert"),
        ("Flow_P3", "Gateway_PulseAlert", "Task_DescribeProblem", "Низкий балл (предложить обращение)"),
        ("Flow_P4", "Gateway_PulseAlert", "Task_AI_GenerateReports", "Норма (запечатать в пул)"),

        # Direct Form Flow
        ("Flow_D1", "Task_DirectFormFill", "Task_RegisterIncoming"),

        # AI Chat Flow
        ("Flow_C1", "Task_DescribeProblem", "Task_AI_ParseAndSurvey"),
        ("Flow_C2", "Task_AI_ParseAndSurvey", "Task_AnswerQuestions"),
        ("Flow_C3", "Task_AnswerQuestions", "Task_AI_DraftStatement"),
        ("Flow_C4", "Task_AI_DraftStatement", "Task_SelectAnonymity"),
        ("Flow_C5", "Task_SelectAnonymity", "Task_RegisterIncoming"),

        # Chancellery & SLA
        ("Flow_R1", "Task_RegisterIncoming", "Task_AI_RouteAndSLA"),
        ("Flow_R2", "Task_AI_RouteAndSLA", "Task_ForwardToRecipient"),
        ("Flow_R3", "Task_ForwardToRecipient", "Task_ReviewComplaint"),
        ("Flow_R4", "Task_ReviewComplaint", "Task_AI_MonitorSLA"),
        ("Flow_R5", "Task_AI_MonitorSLA", "Task_SubmitResponse"),
        ("Flow_R6", "Task_SubmitResponse", "Task_TrackStatus"),
        ("Flow_R7", "Task_TrackStatus", "EndEvent_Emp"),

        # Analytics to Leadership
        ("Flow_A1", "Task_SubmitResponse", "Task_AI_GenerateReports"),
        ("Flow_A2", "Task_AI_GenerateReports", "Task_ViewExecutiveDashboard"),
        ("Flow_A3", "Task_ViewExecutiveDashboard", "EndEvent_Done"),
    ]

    for flow in flows:
        flow_id, src, tgt = flow[0], flow[1], flow[2]
        sf = ET.SubElement(process, f"{{{BPMN_NS}}}sequenceFlow", id=flow_id, sourceRef=src, targetRef=tgt)
        if len(flow) > 3:
            sf.set("name", flow[3])

    tree = ET.ElementTree(definitions)
    ET.indent(tree, space="  ", level=0)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Hybrid BPMN generated: {filename}")

if __name__ == "__main__":
    create_appeals_camunda_bpmn()
