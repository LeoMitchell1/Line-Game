import tkinter as tk
import random

window = tk.Tk()
window.title("Line Game")
window.geometry('500x500')

canvas_width = 500
canvas_height = 500

c = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
c.pack()

dot_size = 16
dot_spacing = 100
line_thickness = 12

player_first = True
win_condition = 6


def player_wins():
    print('Player wins!')


def computer_wins():
    print('Game Over. You lose.')


def player_turn(event):
    line_id = event.widget.find_closest(event.x, event.y)[0]
    color = c.itemcget(line_id, 'fill')
    
    if color == 'white':
        c.itemconfig(line_id, fill='crimson')
        longest_line_length = count_longest_line(line_id)
        print("Longest line length:", longest_line_length)
        computer_turn()
    
    if get_touching_red_lines(line_id):
        return
    
    if all_colored():
        print('There are no more moves.')
        return


def count_longest_line(line_id):
    visited = set()
    lengths = {}
    dfs(line_id, visited, 1, lengths)
    
    longest_line_length = max(lengths.values())
    return longest_line_length

def dfs(line_id, visited, current_length, lengths):
    visited.add(line_id)
    
    if line_id not in lengths or current_length > lengths[line_id]:
        lengths[line_id] = current_length
    
    touching_lines = get_touching_red_lines(line_id)
    for neighbor_id in touching_lines:
        if neighbor_id not in visited:
            dfs(neighbor_id, visited, current_length + 1, lengths)


def computer_turn():
    white_lines = [line for line in lines if c.itemcget(line, 'fill') == 'white']
    if white_lines:
        line_id = random.choice(white_lines)
        c.itemconfig(line_id, fill='lightseagreen')  


def get_touching_red_lines(line_id):
    touching_lines = []
    x1, y1, x2, y2 = c.coords(line_id)
    nearby_lines = c.find_overlapping(x1 - 5, y1 - 5, x2 + 5, y2 + 5)
    for nearby_line in nearby_lines:
        if nearby_line != line_id:
            color = c.itemcget(nearby_line, 'fill')
            if color == 'crimson':
                touching_lines.append(nearby_line)
    return touching_lines


def all_colored():
    return all(c.itemcget(line, 'fill') == 'crimson' for line in lines)


def check_win_condition(player_count):
    if player_count >= win_condition:
        player_wins()
        return True
    return False


start_x = (canvas_width - (3 * dot_spacing + 4 * dot_size)) // 2
start_y = (canvas_height - (3 * dot_spacing + 4 * dot_size)) // 2

lines = []
for row in range(4):
    for col in range(3):
        x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
        y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
        line = c.create_line(x, y, x + dot_spacing + dot_size, y, fill="white", width=line_thickness)
        lines.append(line)
        c.tag_bind(line, '<Button-1>', player_turn)

for row in range(3):
    for col in range(4):
        x = start_x + col * (dot_size + dot_spacing) + dot_size // 2
        y = start_y + row * (dot_size + dot_spacing) + dot_size // 2
        line = c.create_line(x, y, x, y + dot_spacing + dot_size, fill="white", width=line_thickness)
        lines.append(line)
        c.tag_bind(line, '<Button-1>', player_turn)

dots = []
for row in range(4):
    for col in range(4):
        x = start_x + col * (dot_size + dot_spacing)
        y = start_y + row * (dot_size + dot_spacing)
        c.create_oval(x, y, x + dot_size, y + dot_size, fill="black")

if not player_first:
    computer_turn()

window.mainloop()