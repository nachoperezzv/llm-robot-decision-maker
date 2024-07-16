"""
Prompts for "auto" service. Operations: 
    - service
"""

# Third-party imports
from jinja2 import Template

auto_service_prompt = Template("""
You are an intelligent agent in a 2D environment. Your goal is to collect the maximum number of items possible.

These are the objects you can find:
<objects>
{% for object in objects %}
- Type: {{ object.type }}                     
- Tam: {{ object.tam }}
- Description: {{ object.description }}
- Allowed Actions: {{ object.allowed_actions }}
{% endfor %}
</objects>
                               
Here are the available actions over objects:
<actions>
- Destruir (D): Para destruir paredes y bloques.
- Mover (M): Para mover bloques.
- Recolectar (R): Para recolectar objetos.
</actions>
                               
The robot can only move one cell at a time. The available moves are:
<robot_movements>
(x=+1, y=0) : right movement
(x=0, y=+1) : down movement
(x=-1, y=0): left movement
(x=0, y=-1): up movement              
</robot_movements>
You can't move diagonally. Either you move on x or y axis. 
                                                     
These are the nearby objects within a 5 cell radius:
<close_objects>
{% for object in close_objects %}
- Type: {{ object.id }}    
- Object Position: x={{object.pos.x}}, y={{object.pos.y}}
{% endfor %}
</close_objects>

These are all the objects in the map: 
<env_objects>
{% for object in env_objects %}
- id: {{ object.id }}
- pos: x={{ object.pos.x }}, y={{ object.pos.y }}
{% endfor %}
</env_objects>

The current position of the robot is:
<robot>
x={{robot.x}}, y={{robot.y}}).
</robot>    
                               
Make a decision about what direction or action to take to collect the maximum number of items possible in the most efficient way. If there's no object nearby you will have to explore moving around. You should return the thoughts and the plan that lead you to an action. 
                               
Make sure to return a JSON type response based on this format: 
</output_format>
{
    "robot": (Point)
    "objects": (List[Object])
    "thoughts": (List[str])
}
</output_format>

- "robot": Object Type - (Point). It's the new point of the robot. If you decided make an action, point should be the same as the original.
- "objects": Object Type - (List[Object]). List of the objects after the movement and the action. If you've take an action such as "M" or "D" this map should reflect that action. 
- "thoughts": Object Type - (List[str]): This is a list with all the thoughts that lead you take an action (either a movement or an action like "D"). Be sure to say explicitly what action you took.
""")