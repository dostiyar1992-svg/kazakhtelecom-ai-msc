# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def create_drawio_erd(filename="er_diagram_kazakhtelecom.drawio"):
    mxfile = ET.Element("mxfile", host="app.diagrams.net", version="21.0.0", type="device")
    diagram_elem = ET.SubElement(mxfile, "diagram", id="ERD_Kazakhtelecom_Appeals", name="ERD_Прием_Обращений_Казахтелеком")
    model = ET.SubElement(diagram_elem, "mxGraphModel", dx="1600", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="2000", pageHeight="1400", math="0", shadow="0")
    root = ET.SubElement(model, "root")

    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    STYLE_HEADER = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=28;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;fillColor=#00468C;fontColor=#ffffff;strokeColor=#003366;rounded=1;shadow=1;fontSize=12;"
    STYLE_ROW_PK = "text;strokeColor=none;fillColor=#EBF3FA;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=1;fontColor=#00468C;fontSize=11;"
    STYLE_ROW_FK = "text;strokeColor=none;fillColor=#F8F9FA;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontStyle=2;fontColor=#555555;fontSize=11;"
    STYLE_ROW = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=8;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontColor=#212529;fontSize=11;"
    STYLE_EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;startArrow=ERone;strokeColor=#00468C;strokeWidth=2;"

    entities = [
        {
            "id": "e_keycloak",
            "name": "KEYCLOAK_USER",
            "x": 60, "y": 60, "w": 280, "h": 180,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("    username : VARCHAR(100)", STYLE_ROW),
                ("    email : VARCHAR(150)", STYLE_ROW),
                ("    full_name : VARCHAR(200)", STYLE_ROW),
                ("    role : VARCHAR(50) [CHANCELLERY, ADMIN, EXEC]", STYLE_ROW),
                ("    department_code : VARCHAR(50)", STYLE_ROW),
            ]
        },
        {
            "id": "e_org",
            "name": "ORGANIZATIONAL_UNIT",
            "x": 60, "y": 320, "w": 280, "h": 200,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  parent_id : UUID", STYLE_ROW_FK),
                ("    code : VARCHAR(50) [ОДС, ДРБ, РДТ]", STYLE_ROW),
                ("    name : VARCHAR(255)", STYLE_ROW),
                ("    region : VARCHAR(100) [20 регионов]", STYLE_ROW),
                ("    head_user_id : UUID", STYLE_ROW),
            ]
        },
        {
            "id": "e_appeal",
            "name": "APPEAL_INCIDENT",
            "x": 440, "y": 60, "w": 320, "h": 320,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  unit_id : UUID", STYLE_ROW_FK),
                ("    reg_number : VARCHAR(50) [ВХ-2026/XXXX-КАНЦ]", STYLE_ROW),
                ("    anonymous_token : VARCHAR(32) [TK-XXXX-KZ]", STYLE_ROW),
                ("    is_anonymous : BOOLEAN", STYLE_ROW),
                ("    applicant_fio : VARCHAR(200) [NULL if anon]", STYLE_ROW),
                ("    raw_text : TEXT [Описание проблемы]", STYLE_ROW),
                ("    formal_statement : TEXT [Фабула от ИИ]", STYLE_ROW),
                ("    category : VARCHAR(100) [СИЗ, Оплата, Труд]", STYLE_ROW),
                ("    risk_level : VARCHAR(20) [RED, YELLOW, GREEN]", STYLE_ROW),
                ("    status : VARCHAR(40) [REGISTERED, IN_WORK, RESOLVED]", STYLE_ROW),
                ("    registered_at : TIMESTAMP", STYLE_ROW),
            ]
        },
        {
            "id": "e_questions",
            "name": "AI_DYNAMIC_QUESTION",
            "x": 860, "y": 60, "w": 300, "h": 180,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  appeal_id : UUID", STYLE_ROW_FK),
                ("    question_order : INT", STYLE_ROW),
                ("    question_text : VARCHAR(500)", STYLE_ROW),
                ("    selected_answer : VARCHAR(500)", STYLE_ROW),
                ("    generated_at : TIMESTAMP", STYLE_ROW),
            ]
        },
        {
            "id": "e_routing",
            "name": "ROUTING_ASSIGNMENT",
            "x": 440, "y": 440, "w": 320, "h": 220,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  appeal_id : UUID", STYLE_ROW_FK),
                ("FK  assigned_to_user_id : UUID", STYLE_ROW_FK),
                ("    assigned_department : VARCHAR(150)", STYLE_ROW),
                ("    is_first_recipient : BOOLEAN", STYLE_ROW),
                ("    anti_conflict_checked : BOOLEAN", STYLE_ROW),
                ("    status : VARCHAR(40)", STYLE_ROW),
                ("    assigned_at : TIMESTAMP", STYLE_ROW),
            ]
        },
        {
            "id": "e_sla",
            "name": "SLA_LIFECYCLE_TRACKER",
            "x": 860, "y": 300, "w": 300, "h": 220,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  appeal_id : UUID", STYLE_ROW_FK),
                ("    normative_days : INT [5 дней / 24ч]", STYLE_ROW),
                ("    target_deadline : TIMESTAMP", STYLE_ROW),
                ("    warning_24h_sent : BOOLEAN", STYLE_ROW),
                ("    is_overdue : BOOLEAN", STYLE_ROW),
                ("    escalated_to_executive_id : UUID", STYLE_ROW),
                ("    resolved_at : TIMESTAMP", STYLE_ROW),
            ]
        },
        {
            "id": "e_safe_chat",
            "name": "SAFE_TOKEN_CHAT_MESSAGE",
            "x": 860, "y": 580, "w": 300, "h": 200,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  appeal_id : UUID", STYLE_ROW_FK),
                ("    sender_type : VARCHAR(20) [APPLICANT, EXECUTOR]", STYLE_ROW),
                ("    message_text : TEXT", STYLE_ROW),
                ("    attachment_url : VARCHAR(500)", STYLE_ROW),
                ("    created_at : TIMESTAMP", STYLE_ROW),
            ]
        },
        {
            "id": "e_ai_clusters",
            "name": "AI_SYSTEMIC_CLUSTER",
            "x": 440, "y": 720, "w": 320, "h": 220,
            "fields": [
                ("PK  id : UUID", STYLE_ROW_PK),
                ("FK  target_unit_id : UUID", STYLE_ROW_FK),
                ("    cluster_title : VARCHAR(255) [Очаг СИЗ Запад]", STYLE_ROW),
                ("    appeals_count : INT [69 обращений]", STYLE_ROW),
                ("    strike_risk_score : DECIMAL(4,2)", STYLE_ROW),
                ("    executive_summary : TEXT", STYLE_ROW),
                ("    recommended_action : TEXT", STYLE_ROW),
            ]
        }
    ]

    for ent in entities:
        swimlane = ET.SubElement(root, "mxCell", id=ent["id"], value=f"<b>{ent['name']}</b>", style=STYLE_HEADER, vertex="1", parent="1")
        ET.SubElement(swimlane, "mxGeometry", attrib={"x": str(ent["x"]), "y": str(ent["y"]), "width": str(ent["w"]), "height": str(ent["h"]), "as": "geometry"})

        for f_idx, (f_text, f_style) in enumerate(ent["fields"]):
            cell_id = f"{ent['id']}_f{f_idx}"
            f_cell = ET.SubElement(root, "mxCell", id=cell_id, value=f_text, style=f_style, vertex="1", parent=ent["id"])
            ET.SubElement(f_cell, "mxGeometry", attrib={"y": str(28 + f_idx * 22), "width": str(ent["w"]), "height": "22", "as": "geometry"})

    relations = [
        ("r_org_appeal", "e_org", "e_appeal", "1 : N (Филиал к обращениям)"),
        ("r_appeal_questions", "e_appeal", "e_questions", "1 : N (Уточняющие вопросы ИИ)"),
        ("r_appeal_routing", "e_appeal", "e_routing", "1 : N (Маршрутизация исполнителям)"),
        ("r_appeal_sla", "e_appeal", "e_sla", "1 : 1 (Контроль дедлайна SLA)"),
        ("r_appeal_chat", "e_appeal", "e_safe_chat", "1 : N (Защищенная переписка по токену)"),
        ("r_user_routing", "e_keycloak", "e_routing", "1 : N (Назначенные тикеты)"),
        ("r_unit_cluster", "e_org", "e_ai_clusters", "1 : N (Очаги напряженности филиала)"),
    ]

    for rel_id, src, tgt, label in relations:
        edge = ET.SubElement(root, "mxCell", id=rel_id, value=label, style=STYLE_EDGE, edge="1", parent="1", source=src, target=tgt)
        ET.SubElement(edge, "mxGeometry", attrib={"relative": "1", "as": "geometry"})

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"ERD Draw.io generated successfully: {filename}")

if __name__ == "__main__":
    create_drawio_erd()
