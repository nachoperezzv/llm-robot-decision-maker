"""The different services for the auto movement
"""

# Standard imports
from typing import List

# Third-party imports
import openai

# Internal imports
from src.app.auto.schemas.input import Point, Object
from src.app.objects import walls, blocks, stickman, price
from src.app.constants import WIDTH, HEIGHT

MOVS = {
    "N": Point(x=0, y=-1), 
    "E": Point(x=1, y=0), 
    "S": Point(x=0, y=1), 
    "O": Point(x=-1, y=0)
}

OBJECTS = {
    "pared": walls,
    "bloque": blocks,
    "stickman": stickman,
    "objeto": price
}

def decide_action_with_gpt4(robot: Point, close_objects: List[Object]) -> str:
    prompt = f"""
    Eres un agente inteligente en un entorno 2D. Tu objetivo es recolectar el máximo número de elementos posibles.
    Aquí tienes las acciones disponibles:
    - Destruir (D): Para destruir paredes y bloques.
    - Mover (M): Para mover bloques.
    - Recolectar (R): Para recolectar objetos.
    Estos son los objetos cercanos en un radio de 2 celdas:
    {close_objects}
    
    La posición actual del robot es ({robot.x}, {robot.y}).
    
    Toma una decisión sobre qué dirección o acción tomar para recolectar el máximo número de elementos posibles de la manera más eficiente.
    """
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].text.strip()