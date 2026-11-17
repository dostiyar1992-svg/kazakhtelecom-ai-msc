# -*- coding: utf-8 -*-
with open("generate_final_index.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """    function triggerRoleSwitch(roleCode) {
      if (window.platformStateStore) {
        const persona = window.platformStateStore.login(roleCode);
        if (persona) {
          showAuthenticatedUI(persona);
          showToast(`Добро пожаловать, ${persona.name}!`);
        }
      } else {"""

replacement = """    function triggerRoleSwitch(roleCode) {
      const btnKeyMap = {
        'ROLE_EMPLOYEE': 'btn-role-employee',
        'ROLE_EX_SERVICE': 'btn-role-ex_service',
        'ROLE_CHANCELLERY': 'btn-role-chancellery',
        'ROLE_EXECUTIVE': 'btn-role-executive'
      };
      Object.values(btnKeyMap).forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btn) btn.classList.remove('active');
      });
      const targetBtn = document.getElementById(btnKeyMap[roleCode]);
      if (targetBtn) targetBtn.classList.add('active');

      if (window.platformStateStore) {
        const persona = window.platformStateStore.login(roleCode);
        if (persona) {
          showAuthenticatedUI(persona);
          showToast(`Добро пожаловать, ${persona.name}!`);
        }
      } else {"""

text = text.replace(target, replacement)

with open("generate_final_index.py", "w", encoding="utf-8") as f:
    f.write(text)

print("generate_final_index.py patched successfully!")

