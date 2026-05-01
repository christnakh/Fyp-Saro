"""
Central defaults for cost and embodied carbon factors used on the Predict page.

After your literature review, update only the two constants below. They flow into:
- Waste cost and CO₂ from predicted waste mass
- Potential savings / CO₂ reduction (difference in waste % × total steel × these units)

No code changes elsewhere are required when you swap the numbers.
"""

# USD per kg of steel attributable to wasted material (adjust from literature)
STEEL_COST_PER_KG_USD = 0.8

# kg CO₂ per kg of steel waste (embodied carbon attributed to wasted rebar; literature default 0.5)
CO2_PER_KG_STEEL = 0.5
