import tkinter as tk
from tkinter import messagebox
import random
import sys

# === KI Zug - DIESE FUNKTION EDITIEREN ===
def get_ai_move(a, b):
    # Was ihr nutzen könnt:
        # a = Anzahl der Kekse in Glas A
        # b = Anzahl der Kekse in Glas B
        # Die gegebene Implementation einer zufälligen KI (s. u.) - müsst ihr aber nicht benutzen!
        # Das 21 Marbles Spiel aus der letzten Woche (https://github.com/fhightower/21-marbles-python) - Vielleicht bringt euch der Code auf ein paar gute Ideen
    
    # Was das Ergebnis sein muss (nach "return" am Ende der Funktion):
        # Ein Zug in der Form ("Keksglas", Keksanzahl) - also zum Beispiel ("Both", 4) oder ("A", 2)

    # Ideen:
        # - Gibt es Positionen, aus denen das Spiel garantiert GEWONNEN ist? 
        # - Gibt es Positionen, aus denen es VERLOREN ist? 
        # - Wenn ja: 
            # - Welche?
            # - Wie kann man sicherstellen, dass die KI eine siegreiche Position erreicht?
            # - Wie kann die KI aussichtslose Positionen vermeiden?
        # - Wenn nein:
            # - Wie kann man die Chancen der KI erhöhen?
            # - Ist es besser, viele oder wenige Kekse zu nehmen? Macht es einen Unterschied?
            # - Wann sollte man aus beiden Gläsern ziehen? Wann nicht?

    # Falls ihr wirklich GAR NICHT MEHR weiterkommt: 
        # Uns fragen - oder "Wythoff's Game" recherchieren ... Das Internet kennt die Lösung natürlich

    # == Zufällige KI ==
    # Alle legalen Züge sammeln
    options = []

    # Alle Züge für "A"
    for i in range(1, a + 1):
        options.append(("A", i))

    # Alle Züge für "B"
    for i in range(1, b + 1):
        options.append(("B", i))

    # Alle Züge für "Both"
    for i in range(1, min(a, b) + 1):
        options.append(("Both", i))

    # Einen zufälligen Zug auswählen
    return random.choice(options)

# === Konstanten - Falls ihr mit einer anderen Anzahl Cookies experimentieren wollt ===
JAR_A_START = 9
JAR_B_START = 15

# NICHT BERÜHREN

# === Parse Command-Line Argument ===
USE_AI = "-ai" in sys.argv  # Run with: python your_file.py -ai

# === Game State ===
game_state = {
    "heap_a": JAR_A_START,
    "heap_b": JAR_B_START,
    "current_player": 1,
    "game_over": False,
    # Positions of cookies on canvas for each jar: list of (x, y) tuples
    "cookie_positions_a": [],
    "cookie_positions_b": [],
    # Which cookies are visible (True = visible, False = taken)
    "cookie_visible_a": [],
    "cookie_visible_b": [],
}

# === GUI Setup ===
root = tk.Tk()
root.title("Cookie Game - Cookie Bowl Edition")

canvas = tk.Canvas(root, width=500, height=420, bg='white')
canvas.pack()

status_label = tk.Label(root, text="Player 1's turn", font=("Arial", 14))
status_label.pack(pady=5)

input_frame = tk.Frame(root)
input_frame.pack()

jar_choice_var = tk.StringVar(value="A")
jar_menu = tk.OptionMenu(input_frame, jar_choice_var, "A", "B", "Both")
jar_menu.grid(row=0, column=0, padx=5)

cookie_entry = tk.Entry(input_frame, width=5)
cookie_entry.grid(row=0, column=1, padx=5)
cookie_entry.insert(0, "1")

submit_button = tk.Button(input_frame, text="Take Cookies", command=lambda: handle_move(is_ai=False))
submit_button.grid(row=0, column=2, padx=5)

play_again_button = None


# === Functions ===

def initialize_cookie_positions():
    # For jar A
    positions_a = []
    for _ in range(JAR_A_START):
        x = random.randint(-45, 45)
        y = random.randint(-25, 25)
        positions_a.append((x, y))
    # For jar B
    positions_b = []
    for _ in range(JAR_B_START):
        x = random.randint(-45, 45)
        y = random.randint(-25, 25)
        positions_b.append((x, y))

    game_state["cookie_positions_a"] = positions_a
    game_state["cookie_positions_b"] = positions_b
    game_state["cookie_visible_a"] = [True] * JAR_A_START
    game_state["cookie_visible_b"] = [True] * JAR_B_START

def draw_jars():
    canvas.delete("all")
    draw_cookie_bowl(130, 200, "A")
    draw_cookie_bowl(370, 200, "B")

def draw_cookie_bowl(x, y, label):
    # Draw bowl (oval)
    canvas.create_oval(x - 60, y - 40, x + 60, y + 40, fill="#a3d2ca", outline="blue", width=3)

    if label == "A":
        positions = game_state["cookie_positions_a"]
        visible = game_state["cookie_visible_a"]
        count = game_state["heap_a"]
    else:
        positions = game_state["cookie_positions_b"]
        visible = game_state["cookie_visible_b"]
        count = game_state["heap_b"]

    # Draw only visible cookies at stored positions
    for pos, vis in zip(positions, visible):
        if vis:
            px, py = pos
            canvas.create_text(x + px, y + py, text="🍪", font=("Arial", 16))

    # Label and count below
    canvas.create_text(x, y + 60, text=f"Jar {label}: {count} cookie(s)", font=("Arial", 12, "bold"), fill="black")
    canvas.create_text(x, y + 75, text=f"({label})", font=("Arial", 10), fill="gray")

def remove_cookies(jar, num):
    # Mark the first 'num' visible cookies as taken (False)
    if jar == "A":
        visible = game_state["cookie_visible_a"]
    elif jar == "B":
        visible = game_state["cookie_visible_b"]
    else:
        # For both jars, remove from A and B
        remove_cookies("A", num)
        remove_cookies("B", num)
        return

    removed = 0
    for i in range(len(visible)):
        if visible[i]:
            visible[i] = False
            removed += 1
            if removed == num:
                break

def handle_move(is_ai=False):
    if game_state["game_over"]:
        return

    player = "AI" if (is_ai and USE_AI) else f"Player {game_state['current_player']}"

    if is_ai:
        move = get_ai_move(game_state["heap_a"], game_state["heap_b"])
    else:
        try:
            num = int(cookie_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a number.")
            return
        if num <= 0:
            messagebox.showerror("Invalid move", "You must take at least 1 cookie.")
            return
        jar = jar_choice_var.get()
        move = (jar, num)

    jar, num = move
    a, b = game_state["heap_a"], game_state["heap_b"]
    if jar == "A" and num <= a:
        game_state["heap_a"] -= num
        remove_cookies("A", num)
    elif jar == "B" and num <= b:
        game_state["heap_b"] -= num
        remove_cookies("B", num)
    elif jar == "Both" and num <= a and num <= b:
        game_state["heap_a"] -= num
        game_state["heap_b"] -= num
        remove_cookies("Both", num)
    else:
        if not is_ai:
            messagebox.showerror("Illegal move", "You can't take that many cookies.")
        return

    draw_jars()
    jar_description = "both jars" if jar == "Both" else f"jar {jar}"
    messagebox.showinfo("Move Made", f"{player} takes {num} cookie(s) from {jar_description}")

    if game_state["heap_a"] == 0 and game_state["heap_b"] == 0:
        game_state["game_over"] = True
        show_victory_banner(player)
        return

    game_state["current_player"] = 2 if game_state["current_player"] == 1 else 1
    next_player = "AI" if (USE_AI and game_state["current_player"] == 2) else f"Player {game_state['current_player']}"
    status_label.config(text=f"{next_player}'s turn")

    if USE_AI and game_state["current_player"] == 2:
        root.after(500, lambda: handle_move(is_ai=True))

def show_victory_banner(winner):
    canvas.create_rectangle(50, 150, 450, 250, fill="lightblue", outline="blue", width=4)
    canvas.create_text(250, 180, text="🎉 VICTORY 🎉", font=("Arial", 24, "bold"), fill="blue")
    canvas.create_text(250, 220, text=f"{winner} wins the game!", font=("Arial", 16), fill="darkblue")

    global play_again_button
    if play_again_button:
        play_again_button.destroy()
    play_again_button = tk.Button(root, text="Play Again", font=("Arial", 12, "bold"),
                                 bg="deep sky blue", fg="black", activebackground="#2563eb",
                                 relief="flat", borderwidth=0, highlightthickness=0,
                                 command=restart_game)
    play_again_button.place(x=200, y=260, width=100, height=35)

def restart_game():
    game_state["heap_a"] = JAR_A_START
    game_state["heap_b"] = JAR_B_START
    game_state["current_player"] = 1
    game_state["game_over"] = False
    initialize_cookie_positions()
    status_label.config(text="Player 1's turn")
    draw_jars()

    global play_again_button
    if play_again_button:
        play_again_button.destroy()
        play_again_button = None

# === Start the Game ===
initialize_cookie_positions()
draw_jars()
root.mainloop()
