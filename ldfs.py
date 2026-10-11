import tkinter as tk
from tkinter import messagebox

def ldfs_with_states(graph, start, goal, depth_limit):
    stack = [(start, 0)]
    processed = set()
    frontier = set([start])
    states = []
    
    states.append({
        'current': None,
        'stack': list(stack),
        'frontier': set(frontier),
        'processed': set(processed)
    })
    
    while stack:
        current, depth = stack.pop()
        if depth > depth_limit:
            continue
        frontier.remove(current)
        processed.add(current)
        
        states.append({
            'current': current,
            'stack': list(stack),
            'frontier': set(frontier),
            'processed': set(processed)
        })
        
        if current == goal:
            break
            
        if depth < depth_limit:
            for neighbor, _ in reversed(graph.get(current, [])):
                if neighbor not in processed and neighbor not in frontier:
                    stack.append((neighbor, depth + 1))
                    frontier.add(neighbor)
    
    return states

class LDFSGUI:
    def __init__(self, graph, start, goal, depth_limit, positions):
        self.graph = graph
        self.start = start
        self.goal = goal
        self.depth_limit = depth_limit
        self.positions = positions
        self.states = ldfs_with_states(graph, start, goal, depth_limit)
        self.current_step = 0
        
        self.root = tk.Tk()
        self.root.title("Limited Depth-First Search Visualization")
        
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(pady=10)
        
        self.stack_label = tk.Label(self.root, text="Stack: []", font=("Arial", 12))
        self.stack_label.pack()
        
        self.next_button = tk.Button(self.root, text="Next Step", command=self.next_step, font=("Arial", 12))
        self.next_button.pack(pady=5)
        
        self.draw_graph()
        self.update_display(self.states[0])
    
    def draw_graph(self):
        self.node_objects = {}
        self.edge_labels = []
        for node in self.graph:
            x1, y1 = self.positions[node]
            for neighbor, cost in self.graph[node]:
                x2, y2 = self.positions[neighbor]
                self.canvas.create_line(x1, y1, x2, y2)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                label = self.canvas.create_text(mx, my, text=str(cost), font=("Arial", 10))
                self.edge_labels.append(label)
        for node in self.graph:
            x, y = self.positions[node]
            oval = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill='white')
            text = self.canvas.create_text(x, y, text=node, font=("Arial", 12))
            self.node_objects[node] = (oval, text)
    
    def update_display(self, state):
        for node in self.node_objects:
            self.canvas.itemconfig(self.node_objects[node][0], fill='white')
        for node in state['processed']:
            self.canvas.itemconfig(self.node_objects[node][0], fill='gray')
        for node in state['frontier']:
            self.canvas.itemconfig(self.node_objects[node][0], fill='yellow')
        if state['current']:
            self.canvas.itemconfig(self.node_objects[state['current']][0], fill='red')
        stack_str = ", ".join([f"{node}({depth})" for node, depth in state['stack']])
        self.stack_label.config(text=f"Stack: [{stack_str}]")
    
    def next_step(self):
        if self.current_step < len(self.states) - 1:
            self.current_step += 1
            self.update_display(self.states[self.current_step])
        else:
            messagebox.showinfo("Info", "Search completed")

if __name__ == "__main__":
    graph = {
        'A': [('B', 1), ('C', 3), ('D', 2)],
        'B': [('E', 4), ('F', 2)],
        'C': [('G', 1)],
        'D': [('H', 3), ('I', 1)],
        'E': [('J', 2), ('K', 5)],
        'F': [],
        'G': [('L', 4)],
        'H': [],
        'I': [('M', 3), ('N', 1)],
        'J': [],
        'K': [],
        'L': [],
        'M': [],
        'N': []
    }

    positions = {
        'A': (400, 50),
        'B': (200, 150),
        'C': (400, 150),
        'D': (600, 150),
        'E': (100, 250),
        'F': (300, 250),
        'G': (400, 250),
        'H': (500, 250),
        'I': (700, 250),
        'J': (50, 350),
        'K': (150, 350),
        'L': (400, 350),
        'M': (650, 350),
        'N': (750, 350)
    }

    depth_limit = 2
    gui = LDFSGUI(graph, 'A', 'N', depth_limit, positions)
    gui.root.mainloop()