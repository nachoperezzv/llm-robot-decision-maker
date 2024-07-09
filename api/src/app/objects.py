"""Objects and its characteristics
"""

walls = {
  "type": "pared",
  "tam": 1, 
  "description": "Una pared inamovible, pero destructible que bloquea el paso.",
  "allowed_actions": ["D"]
}

blocks = {
  "type": "bloque",
  "tam": 1, 
  "description": "Un bloque que puede ser movido y destruido.",
  "allowed_actions": ["M", "D"]
}

stickman = {
  "type": "stickman",
  "tam": 1, 
  "descripcion": "Persona que esta quieta en el mapa.",
  "acciones_permitidas": []
}

price = {
  "type": "objeto",
  "tam": 1,
  "descripcion": "Un objeto recolectable.",
  "acciones_permitidas": ["R"]
}