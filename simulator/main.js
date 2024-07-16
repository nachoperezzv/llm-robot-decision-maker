let auto = false;
let play = false;
const container = document.getElementById('grid-container');
const map = Array(20).fill(null).map(() => Array(20).fill(null));

// Define objects
const walls = {
    "type": "pared",
    "tam": 1,
    "description": "Una pared inamovible, pero destructible que bloquea el paso.",
    "allowed_actions": ["D"]
};

const blocks = {
    "type": "bloque",
    "tam": 1,
    "description": "Un bloque que puede ser movido y destruido.",
    "allowed_actions": ["M", "D"]
};

const stickman = {
    "type": "stickman",
    "tam": 1,
    "description": "Persona que esta quieta en el mapa.",
    "allowed_actions": []
};

const price = {
    "type": "objeto",
    "tam": 1,
    "description": "Un objeto recolectable.",
    "allowed_actions": ["R"]
};

// Read toggle mode
document.getElementById('toggle').addEventListener('change', function () {
    auto = this.checked;
    console.log('Auto mode:', auto);
    if (auto && play) {
        simulateRobotMovement();
    }
});

// Play/Stop button functionality
const playStopButton = document.getElementById('playStopButton');
playStopButton.addEventListener('click', function () {
    play = !play;
    playStopButton.innerHTML = play ? '<i class="fas fa-pause"></i>' : '<i class="fas fa-play"></i>';
    console.log('Play state:', play);
    if (auto && play) {
        simulateRobotMovement();
    }
});

// Create the grid
for (let i = 0; i < 20 * 20; i++) {
    const cell = document.createElement('div');
    cell.className = 'grid-item';
    container.appendChild(cell);
}

// Initial position of the robot
let robot = { x: 9, y: 9 };
map[robot.y][robot.x] = 'robot';
updateGrid();

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
    map.forEach(row => row.fill(null));
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

function processMapData(data) {
    resetGrid(); // Reset the grid before processing new data

    const objects = data.objects;
    objects.forEach(obj => {
        if (obj.pos.x >= 1 && obj.pos.x <= 20 && obj.pos.y >= 1 && obj.pos.y <= 20) {
            map[obj.pos.y - 1][obj.pos.x - 1] = obj.id;
        } else {
            console.error(`Invalid coordinates for ${obj.id}: (${obj.pos.x}, ${obj.pos.y})`);
        }
    });

    // Update the robot position from the data
    if (data.robot) {
        robot = { x: data.robot.x - 1, y: data.robot.y - 1 }; // Convert back to 0-based index
        map[robot.y][robot.x] = 'robot';
    } else {
        map[robot.y][robot.x] = 'robot';
    }

    updateGrid();
}

function updateGrid() {
    for (let y = 0; y < map.length; y++) {
        for (let x = 0; x < map[y].length; x++) {
            const index = y * 20 + x;
            const gridCell = container.children[index];
            gridCell.style.backgroundImage = '';

            const cell = map[y][x];
            if (cell === 'robot') {
                gridCell.style.backgroundImage = 'url("assets/robot.png")';
            } else if (cell) {
                switch (cell) {
                    case 'stickman':
                        gridCell.style.backgroundImage = 'url("assets/stickman.png")';
                        break;
                    case 'wall':
                        gridCell.style.backgroundImage = 'url("assets/wall.png")';
                        break;
                    case 'block':
                        gridCell.style.backgroundImage = 'url("assets/block.png")';
                        break;
                    case 'price':
                        gridCell.style.backgroundImage = 'url("assets/price.png")';
                        break;
                }
            }
        }
    }
}

function moveRobot(newX, newY) {
    if (newX < 0 || newX >= 20 || newY < 0 || newY >= 20 || map[newY][newX]) {
        return;
    }
    map[robot.y][robot.x] = null;
    robot = { x: newX, y: newY };
    map[robot.y][robot.x] = 'robot';
    updateGrid();
}

window.addEventListener('keydown', (event) => {
    if (!auto) {
        switch (event.key) {
            case 'ArrowUp':
                console.log("up")
                moveRobot(robot.x, robot.y - 1);
                break;
            case 'ArrowDown':
                console.log("down")
                moveRobot(robot.x, robot.y + 1);
                break;
            case 'ArrowLeft':
                console.log("left")
                moveRobot(robot.x - 1, robot.y);
                break;
            case 'ArrowRight':
                console.log("right")
                moveRobot(robot.x + 1, robot.y);
                break;
        }
    }
});

function getCloseObjects(robot, envObjects, radius = 5) {
    return envObjects.filter(obj => {
        const distX = Math.abs(obj.pos.x - robot.x);
        const distY = Math.abs(obj.pos.y - robot.y);
        return distX <= radius && distY <= radius;
    });
}

var outputArea = document.getElementById("output-area");
function appendMessage(message) {
    outputArea.value += message + "\n";
    outputArea.scrollTop = outputArea.scrollHeight; // Scroll to the bottom
}  

function simulateRobotMovement() {
    if (!auto || !play) return; // Exit if auto or play is false

    const env_objects = [];
    map.forEach((row, y) => {
        row.forEach((cell, x) => {
            if (cell && cell !== 'robot') {
                env_objects.push({
                    id: cell,
                    pos: { x: x + 1, y: y + 1 } // Convert to 1-based index
                });
            }
        });
    });

    const close_objects = getCloseObjects(robot, env_objects);

    const body_content = {
        robot: { x: robot.x + 1, y: robot.y + 1 }, // Convert to 1-based index
        env_objects: env_objects,
        close_objects: close_objects
    };
    console.log(body_content);

    fetch('http://localhost:8000/api/auto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body_content)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            processMapData(data);

            // Append instructions to the output area
            const instructions = data.thoughts;
                appendMessage("\n============\n===========\n" + instructions);

            // Call the function again if auto and play are still true
            if (auto && play) {
                simulateRobotMovement();
            }
        })
        .catch(error => console.error('Error:', error));
}

// Dummy function to simulate the initial plan for robot movement (for display purposes)
function initialRobotPlan() {
    const outputArea = document.getElementById('output-area');
    outputArea.innerHTML = "";
}

// Call the dummy function to display initial plan (for example purpose)
initialRobotPlan();