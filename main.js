<!DOCTYPE html>
<html>
<head>
    <title>Tic Tac Toe</title>
    <style>
        /* Add your CSS styles here */
    </style>
</head>
<body>
    <div class="game-panel">
        <h1><b><i>Tic Tac Toe</i></b></h1>
        <h2 id="message"></h2>
        <table>
            <!-- Use JavaScript to generate the game board -->
        </table>
        <div>
            <button id="reset">Start Over</button>
            <a href="/history" class="history-button">Game History</a>
        </div>
    </div>

    <script>
        // JavaScript code goes here
        const WIN_LINES = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7]
        ];

        const board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
        let currentPlayer = 1;
        let gameResults = [];

        // Function to check if a player has won
        function checkWin(player) {
            for (const line of WIN_LINES) {
                if (line.every((pos) => board[pos - 1] === player)) {
                    return true;
                }
            }
            return false;
        }

        // Function to update the game board
        function updateBoard() {
            const table = document.querySelector("table");
            table.innerHTML = "";

            for (let i = 0; i < 3; i++) {
                const row = document.createElement("tr");
                for (let j = 0; j < 3; j++) {
                    const cell = document.createElement("td");
                    const button = document.createElement("button");
                    const spotValue = board[j * 3 + i];

                    button.textContent = spotValue === 1 ? "X" : spotValue === 2 ? "O" : "";
                    button.disabled = spotValue !== 0;

                    button.addEventListener("click", () => makeMove(j * 3 + i));

                    cell.appendChild(button);
                    row.appendChild(cell);
                }
                table.appendChild(row);
            }
        }

        // Function to make a move
        function makeMove(move) {
            if (board[move] === 0) {
                board[move] = currentPlayer;
                updateBoard();

                if (checkWin(currentPlayer)) {
                    document.getElementById("message").textContent =
                        currentPlayer === 1 ? "Player X wins" : "Player O wins";
                    gameResults.push(currentPlayer === 1 ? "Player X wins" : "Player O wins");
                    resetBoard();
                } else if (!board.includes(0)) {
                    document.getElementById("message").textContent = "It's a tie";
                    gameResults.push("Tie");
                    resetBoard();
                } else {
                    currentPlayer = 3 - currentPlayer; // Toggle between 1 and 2
                    document.getElementById("message").textContent =
                        currentPlayer === 1 ? "Player X's turn" : "Player O's turn";
                }
            }
        }

        // Function to reset the game board
        function resetBoard() {
            board.fill(0);
            updateBoard();
            currentPlayer = 1;
        }

        // Add event listener for the "Start Over" button
        document.getElementById("reset").addEventListener("click", resetBoard);

        // Initial setup
        updateBoard();
        document.getElementById("message").textContent = "Player X's turn";
    </script>
</body>
</html>
