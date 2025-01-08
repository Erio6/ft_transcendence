const cursor = document.getElementById("cursor");
const leftSide = document.getElementById("left-side");
const rightSide = document.getElementById("right-side");
const startButton = document.getElementById("start-button");
let selectedSide = "left"; // Default selection

// Function to move the cursor
function moveCursor(side) {
    if (side === "left") {
        cursor.style.left = "25%";
        selectedSide = "left";
    } else if (side === "right") {
        cursor.style.left = "75%";
        selectedSide = "right";
    }
}

// Add event listeners for side selection
leftSide.addEventListener("click", () => moveCursor("left"));
rightSide.addEventListener("click", () => moveCursor("right"));

// Optionally, allow arrow key selection
document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
        moveCursor("left");
    } else if (event.key === "ArrowRight") {
        moveCursor("right");
    }
});

// Start game button click
startButton.addEventListener("click", () => {
    const aiLevel = document.getElementById("ai-level").value;
    console.log(`Starting game: Player side - ${selectedSide}, AI level - ${aiLevel}`);
    alert(`Starting game: Player side - ${selectedSide}, AI level - ${aiLevel}`);
});