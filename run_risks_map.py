from code_intelligence.risk_mapper import generate_risk_map
import json

with open("analysis.json") as f:
    analysis = json.load(f)

risk_map = generate_risk_map(analysis)

with open("risk_map.json", "w") as f:
    json.dump(risk_map, f, indent=2)
