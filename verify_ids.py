# -*- coding: utf-8 -*-
with open('index.html', encoding='utf-8') as f:
    html = f.read()

required_ids = [
    'workspace-employee',
    'workspace-chat',
    'workspace-pulse',
    'workspace-form',
    'workspace-ex-service',
    'workspace-chancellery',
    'workspace-executive',
    'modal-nudge',
    'modal-token-tracker',
    'modal-chancellery-stamp',
    'modal-region-inspector',
    'synergy-alert-b1',
    'btn-role-employee',
    'btn-role-ex',
    'btn-role-chancellery',
    'btn-role-executive',
    'master-chancellery-tbody',
    'heatmap-grid-container',
    'external-data-preview-box',
    'external-csv-table',
    'correlation-result-box'
]

missing = [i for i in required_ids if f'id="{i}"' not in html]
if missing:
    print('Missing IDs:', missing)
else:
    print(f'SUCCESS: All {len(required_ids)} critical IDs are present in index.html!')
