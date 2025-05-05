from enum import Enum

class AssistantType(str, Enum):
    WaterCementConc = "water_cement_conc"
    WaterCementJson = "water_cement_json"
    AdditiveConc = "additive_conc"

Response_w_c_conc = {
  "name": "WC_CONC",
  "schema": {
    "type": "object",
    "properties": {
        "water_measurement": {
            "type": "number",
            "description": "The amount of water measured in barrels (BBL)."
        },
        "cement_measurement": {
            "type": "number",
            "description": "The amount of cement measured in sacks (SX)."
        }
    },
    "required": ["water_measurement","cement_measurement"
    ],
    "additionalProperties": False
  },
  "strict": True
}