# Set Deduction Game

A terminal-style puzzle game where the player must deduce the exact contents of two hidden sets of integers through set‑operation queries. The game runs entirely in the browser using Pyodide (Python compiled to WebAssembly) and can also be executed locally as a standard Python script.

## Features

- Suffering.

## How to Play

Two hidden sets, A and B, are generated randomly. Each set contains 3 to 8 unique integers from 1 to 20. Your objective is to determine the exact elements of both sets using queries that return information about the sets or compare them.

In Hard mode, each query costs energy. If energy reaches zero, further queries are blocked and you must guess the sets.

## Running the Game

### On the Web (Recommended)

1. Clone or download this repository.
2. Host the files on any static server (e.g., GitHub Pages).
   - On GitHub: Enable Pages from the repository settings, selecting the branch that contains `index.html`.
3. Open the provided URL. The game loads Pyodide automatically and presents a terminal interface.

No server‑side code is required; all execution occurs in the browser.

### Locally (Python)

1. Ensure Python 3.8 or later is installed.
2. Open a terminal in the project directory.
3. Run the game:
   ```bash
   python game.py
   ```
   On some systems, you may need to use `python3`.

Note: The local version uses the same Python file but uses blocking `input()` through an async wrapper, making it fully functional without Pyodide.

## Commands

Once the game starts (after selecting the mode), you interact via a command prompt (`>`). The following commands are available:

| Command | Description |
|---------|-------------|
| `probe <a\|b> <op> [set]` | Query Set A or B. `<op>` can be `len`, `min`, `max`, `sum`, `subset`, `superset`, `disjoint`, `intersection`, `union`, `minus`, or `symmetric_difference`. If the operation requires a custom set, provide a comma‑separated list of numbers (e.g., `probe a subset 1,2,3`). |
| `compare <op>` | Compare Set A and Set B. Available operations: `subset`, `superset`, `disjoint`, `intersection`, `union`, `minus`, `symmetric_difference`. |
| `guess` | Submit your final guess for both sets. You will be prompted to enter the elements of Set A and Set B separately. |
| `info` | Display the full manual, including method descriptions and energy costs. |
| `clear` | Clear the terminal screen. |
| `quit` | Exit the game and reveal the hidden sets. |

### Examples

```
probe a len
probe b subset 5,7,9
compare intersection
guess
```

## Energy Costs (Hard Mode)

### Single‑Set Probes

| Operation            | Energy Cost |
|----------------------|-------------|
| len                  | 1           |
| min / max / sum      | 4           |
| disjoint             | 2           |
| subset / superset    | 3           |
| intersection         | 6           |
| symmetric_difference | 7           |
| union / minus        | 8           |

### Cross‑Set Comparisons

| Operation            | Energy Cost |
|----------------------|-------------|
| disjoint             | 4           |
| subset / superset    | 5           |
| intersection         | 8           |
| symmetric_difference | 9           |
| union / minus        | 10          |

## File Structure

```
.
├── index.html
├── game.py
├── LICENSE
└── README.md
```

## Technology

- **Frontend:** HTML, CSS, JavaScript
- **Python runtime in browser:** [Pyodide](https://pyodide.org/) (v0.25.0)
- **Local Python:** Standard library only (uses `asyncio` for compatibility)

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details. (Add a LICENSE file if you wish to apply a formal license.)

---
For any issues or contributions, please open an issue or pull request on the repository.
