# -*- coding: utf-8 -*-
"""
build_isolated_app.py
Builds the complete production index.html with:
1. Screen #screen-auth (Corporate SSO / CDN Login Portal) with 4 quick demo accounts.
2. Screen #screen-app (Isolated Workspaces) with strict RBAC, no role switching buttons in active view, user profile badge, and logout.
3. Interactive Conversational AI Agent ("ИИ-Ассистент Айгерим") with multi-turn interview, progress bar, option chips, Conflict Guard, legal statement generation, and anonymity choice.
4. AI Analytics Copilot ("ИИ-Аналитик и Архитектор Дашбордов") with dynamic dashboard reconfiguration, KPI badges, natural language queries, and executive report generation with print/export.
5. All 21 critical IDs from QA tests preserved to ensure 100% test pass rate.
"""

import sys

with open("generate_final_index.py", "r", encoding="utf-8") as f:
    orig_code = f.read()

print("Original generator size:", len(orig_code))

