# -*- coding: utf-8 -*-
with open('platform-state-and-rules.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Add login method to PlatformStore
text = text.replace(
    'switchRole(roleName) {',
    'login(roleName) { return this.switchRole(roleName); }\n\n    switchRole(roleName) {'
)

# Update switchRole to return targetUser
text = text.replace(
    "if (targetUser) {\n        this.setCurrentUser(targetUser);\n        this.notifySubscribers('ROLE_SWITCHED', targetUser);\n      }",
    "if (targetUser) {\n        this.setCurrentUser(targetUser);\n        this.notifySubscribers('ROLE_SWITCHED', targetUser);\n        return targetUser;\n      }\n      return this.state.currentUser;"
)

copilot_code = """
  function askAICopilot(query) {
    const copilot = global.KazakhtelecomAnalyticsCopilot || new AnalyticsCopilot(storeInstance);
    const qLower = (query || "").toLowerCase();
    let promptKey = null;
    if (qLower.includes('забастов') || qLower.includes('стачечн') || qLower.includes('риск') || qLower.includes('7.5')) {
      promptKey = 'STRIKE_RISK';
    } else if (qLower.includes('сиз') || qLower.includes('обув') || qLower.includes('охран') || qLower.includes('труд')) {
      promptKey = 'PPE_SAFETY';
    } else if (qLower.includes('корреляц') || qLower.includes('текучест') || qLower.includes('пирсон') || qLower.includes('внешн')) {
      promptKey = 'CORRELATION_TURNOVER';
    } else if (qLower.includes('отчет') || qLower.includes('правлен') || qLower.includes('совет') || qLower.includes('свод')) {
      promptKey = 'EXECUTIVE_BOARD_REPORT';
    }

    const res = copilot.processQuery(promptKey, query);
    return {
      title: res.title,
      summary: res.narrative,
      details: res.kpis ? res.kpis.map(k => `${k.label}: ${k.value} [${k.badge}]`).join(' • ') : '',
      recommendations: res.actionPlan || (res.reportSections ? res.reportSections.map(s => s.title) : ["Провести внеочередную проверку условий труда", "Уведомить профильный департамент"]),
      actionType: res.chartType === 'CORRELATION_SCATTER' ? 'UPDATE_CORRELATION_CHART' : (res.isFullReport ? 'SHOW_EXECUTIVE_REPORT' : 'DEFAULT'),
      chartData: res.chartData
    };
  }
"""

if 'askAICopilot' not in text:
    text = text.replace('  global.KazakhtelecomAI = {', copilot_code + '\n  global.KazakhtelecomAI = {\n    askAICopilot,')

with open('platform-state-and-rules.js', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated platform-state-and-rules.js!')

