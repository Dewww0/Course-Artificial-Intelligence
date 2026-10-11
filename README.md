# Search Algorithms Visualization

This repository contains Python implementations of seven search algorithms with Tkinter-based GUI visualizations, designed for an AI class project. Each algorithm demonstrates step-by-step traversal of a fixed search tree from node A to node N.

## Algorithms
- **Breadth-First Search (BFS)**: Explores level-by-level.
- **Depth-First Search (DFS)**: Explores deeply along each branch.
- **Limited Depth-First Search (LDFS)**: DFS with a depth limit of 2.
- **Iterative Deepening Depth-First Search (IDDFS)**: Iteratively increases depth limit.
- **Uniform-Cost Search (UCS)**: Explores by lowest path cost.
- **Greedy Best-First Search (GBFS)**: Uses heuristic to guide search.
- **A* Search**: Combines path cost and heuristic for optimal path.

## Search Tree
```
        A
       /|\
      / | \
     B  C  D
    /|  |  |\
   / |  |  | \
  E  F  G  H  I
 /|     |     |\
 J K    L     M N
```
- **Start**: A
- **Goal**: N
- **Edge Costs**: Used by UCS and A* (e.g., A→D=2, D→I=1, I→N=1).
- **Heuristics** (GBFS, A*): A=5, B=4, C=4, D=3, E=5, F=4, G=4, H=3, I=2, J=6, K=6, L=5, M=3, N=0.

## Files
- `bfs.py`: Breadth-First Search
- `dfs.py`: Depth-First Search
- `ldfs.py`: Limited Depth-First Search
- `iddfs.py`: Iterative Deepening Depth-First Search
- `ucs.py`: Uniform-Cost Search
- `gbfs.py`: Greedy Best-First Search
- `astar.py`: A* Search
- `requirements.txt`: Dependencies
- `.gitignore`: Excludes unnecessary files

## Requirements
- Python 3.x
- Tkinter (included with standard Python)

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/<your-username>/search-algorithms-visualization.git
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run any algorithm:
   ```
   python bfs.py
   ```

## Usage
- Run a Python file (e.g., `python bfs.py`).
- Click "Next Step" to step through the algorithm’s execution.
- Colors: White (unvisited), Yellow (frontier), Gray (processed), Red (current).
- The queue/stack/priority queue is displayed below the graph.

## License
MIT License