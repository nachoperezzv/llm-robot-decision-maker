"""
Prompts for runners. Operations: 
    - Map Generator Prompt
"""

# Third-party imports
from jinja2 import Template

map_generator_prompt = Template("""
You are a map designer. Your mission is to design a 20x20 cell map based on a series of objects and a specific configuration. The map should have level of difficulty: {{ level }}.

These are the objects and their characteristics:
<objects>
{% for object in objects %}
- Type: {{ object.type }}                     
- Tam: {{ object.tam }}
- Description: {{ object.description }}
- Allowed Actions: {{ object.allowed_actions }}
{% endfor %}
</objects>

This is the map configuration: A number indicating the total amount of objects on the map.
<map_configuration>
{{ map_configuration }}
</map_configuration>

Map Requirements:
- The map measures 20x20 cells.
- The robot is initially located at position (10, 10) and has a vision range of 3 cells radius.
 The "price" objects must be hidden behind other objects according to the specified difficulty level.
 Consider that higher difficulty means more "block" and "wall" objects should block the robot's direct line of sight to the "price" objects.
- Objects should be distributed on the map without exceeding the boundaries.


Map Generation Thought Process: Follow this mental process when generating the map
- Initialize the Map: Create a 20x20 cell empty grid.
- Position the Robot: Place the robot at position (10, 10).
- Distribute Objects:
    - Calculate the number of each type of object based on the configuration and difficulty.
    - Ensure the total number of objects does not exceed the map's capacity.
- Placement of "price" Objects:
    - The "price" objects should be distributed so that some are close and some are far from the robot. You can put some within their range of vision.
- Distribution of Other Objects:
    - The "stickman" objects are placed to disturb the movement of the robot. It will not be able to move or destroy them, so they must be placed according to the level of difficulty to disturb the robot's passage.
    - Los objetos "wall" y "block" deben estar colocados de manera que interrumpan el avance directo del robot, pueden ponerse formando una especie de barrera o rondeandolos. 
    - Keep in mind that you have a limited amount of these items and you have to try to distribute them over all the "price" items.
- Validation:
    - Make sure there is no object that occupies the robot's initial position (x=10, y=10)
    - Make sure the robot has escape routes, i.e. the "wall" and "block" objects cannot completely surround the robot
    - Ensure all objects are within the map and do not overlap unnecessarily.

    
The output should be only a JSON type object based on this format:
<output_format>
{
    "objects": [
        { "type": "stickman", "x": 5, "y": 10},
        { "type": "wall", "x": 10, "y": 20 },
        { "type": "block", "x": 15, "y": 5 },
        { "type": "price", "x": 1, "y": 19 }
    ]
}
</output_format>
""")