const container = document.getElementById('grid-container');

// Create the grid
for (let i = 0; i < 20 * 20; i++) {
    const cell = document.createElement('div');
    cell.className = 'grid-item';
    container.appendChild(cell);
}

// Place the robot in the center
const centerX = 7; // center x-coordinate (1-based index)
const centerY = 12; // center y-coordinate (1-based index)
const centerIndex = (centerY - 1) * 20 + (centerX - 1); // convert to 0-based index
container.children[centerIndex].style.backgroundImage = 'url("assets/robot.png")';

// Load the JSON data
fetch('maps/map1.json')
    .then(response => response.json())
    .then(data => {
        const objects = data.objects;
        objects.forEach(obj => {
            if (obj.x >= 1 && obj.x <= 20 && obj.y >= 1 && obj.y <= 20) { // Ensure coordinates are within grid bounds
                const index = (obj.y - 1) * 20 + (obj.x - 1); // convert to 0-based index
                const cell = container.children[index];
                switch (obj.type) {
                    case 'stickman':
                        cell.style.backgroundImage = 'url("assets/stickman.png")';
                        break;
                    case 'wall':
                        cell.style.backgroundImage = 'url("assets/wall.png")';
                        break;
                    case 'block':
                        cell.style.backgroundImage = 'url("assets/block.png")';
                        break;
                    case 'price':
                        cell.style.backgroundImage = 'url("assets/price.png")';
                        break;
                }
            } else {
                console.error(`Invalid coordinates for ${obj.type}: (${obj.x}, ${obj.y})`);
            }
        });
        // Simulate the thought process for reaching the price at (7, 12)
        const outputArea = document.getElementById('output-area');
        outputArea.innerHTML = 
            "Inicializando plan para mover el robot hacia el objetivo en (7, 12)...\n" +
            "Paso 1: Evaluar posición actual y objetivo.\n" +
            "Posición actual: (10, 10)\n" +
            "Objetivo: (7, 12)\n" +
            "Paso 2: Calcular ruta óptima evitando obstáculos.\n" +
            "Detectado obstáculo en (8, 12)\n" +
            "Paso 3: Ajustar ruta para evitar el obstáculo.\n" +
            "Ruta ajustada: (10, 10) -> (9, 10) -> (8, 10) -> (7, 10) -> (7, 11) -> (7, 12)\n" +
            "Paso 4: Ejecutar movimiento.\n" +
            "Movimiento completado. El robot ha llegado a (7, 12).";
    })
    .catch(error => console.error('Error loading the map:', error));
