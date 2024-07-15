let auto = true;
const container = document.getElementById('grid-container');

// Read toggle mode
document.getElementById('toggle').addEventListener('change', function() {
    auto = this.checked;
    console.log('Auto mode:', auto);
});

// Create the grid
for (let i = 0; i < 20 * 20; i++) {
    const cell = document.createElement('div');
    cell.className = 'grid-item';
    container.appendChild(cell);
}

// Place the robot in the center
const centerX = 10; // center x-coordinate (1-based index)
const centerY = 10; // center y-coordinate (1-based index)
const centerIndex = (centerY - 1) * 20 + (centerX - 1); // convert to 0-based index
container.children[centerIndex].style.backgroundImage = 'url("assets/robot.png")';

document.getElementById('loadMapDropdown').addEventListener('change', (event) => {
    const mapUrl = event.target.value;
    
    if (mapUrl) {
        resetGrid();
        loadMapData(mapUrl)
            .then(data => processMapData(data))
            .catch(error => console.error('Error processing the map data:', error));
    }
});

function resetGrid() {
    for (let i = 0; i < container.children.length; i++) {
        container.children[i].style.backgroundImage = '';
    }
    container.children[centerIndex].style.backgroundImage = 'url("assets/robot.png")';
}

function loadMapData(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        });
}

// Función para procesar los datos y actualizar el mapa
function processMapData(data) {  
    const objects = data.objects;
    objects.forEach(obj => {
        if (obj.x >= 1 && obj.x <= 20 && obj.y >= 1 && obj.y <= 20) {
            const index = (obj.y - 1) * 20 + (obj.x - 1);
            const cell = container.children[index];
            if (cell) {
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
                console.error(`No cell found at index ${index} for coordinates (${obj.x}, ${obj.y})`);
            }
        } else {
            console.error(`Invalid coordinates for ${obj.type}: (${obj.x}, ${obj.y})`);
        }
    });

    // Simula el proceso de pensamiento para llegar al premio en (7, 12)
    simulateRobotMovement();
}

// Función para simular el movimiento del robot
function simulateRobotMovement() {
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
}

// Llamar a las funciones
// loadMapData('maps/map2.json')
//     .then(data => processMapData(data))
//     .catch(error => console.error('Error processing the map data:', error));