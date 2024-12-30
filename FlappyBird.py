import tkinter as tk
import random

# Oyun ayarları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 40
BIRD_HEIGHT = 40
PIPE_WIDTH = 60
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_VELOCITY = 3

# Değişkenler
bird_velocity = 0
score = 0
pipes = []
game_running = False

# Tkinter pencereyi oluştur
root = tk.Tk()
root.title("Flappy Bird Game")

# Ana çerçeve
main_frame = tk.Frame(root)
main_frame.pack()

# Skor ve kontrol paneli
control_frame = tk.Frame(main_frame)
control_frame.pack(side=tk.TOP, fill=tk.X)

score_label = tk.Label(control_frame, text="Score: 0", font=("Arial", 16))
score_label.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(control_frame, text="Start", font=("Arial", 14), command=lambda: start_game())
start_button.pack(side=tk.RIGHT, padx=10)

stop_button = tk.Button(control_frame, text="Stop", font=("Arial", 14), state=tk.DISABLED, command=lambda: stop_game())
stop_button.pack(side=tk.RIGHT, padx=10)

# Oyun alanı (canvas)
canvas = tk.Canvas(main_frame, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="lightblue")
canvas.pack()

# Kuşu yarat
bird = canvas.create_oval(
    50, SCREEN_HEIGHT // 2 - BIRD_HEIGHT // 2, 
    50 + BIRD_WIDTH, SCREEN_HEIGHT // 2 + BIRD_HEIGHT // 2, 
    fill="yellow"
)

# Fonksiyonlar
def start_game():
    """Oyunu başlatır."""
    global game_running, bird_velocity, score, pipes
    game_running = True
    bird_velocity = 0
    score = 0
    pipes = []
    canvas.delete("all")
    pipes.clear()
    canvas.create_oval(
        50, SCREEN_HEIGHT // 2 - BIRD_WIDTH // 2, 
        50 + BIRD_WIDTH, SCREEN_HEIGHT // 2 + BIRD_HEIGHT // 2, 
        fill="yellow", tags="bird"
    )
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    game_loop()

def stop_game():
    """Oyunu durdurur."""
    global game_running
    game_running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def create_pipe():
    """Yeni borular oluşturur ve daha kolay geçiş sağlar."""
    global PIPE_GAP
    fixed_height = SCREEN_HEIGHT // 3  # Sabit yükseklik
    top_pipe_height = SCREEN_HEIGHT // 2 - PIPE_GAP // 2
    bottom_pipe_height = SCREEN_HEIGHT // 2 + PIPE_GAP // 2

    # Boruların üst ve alt kısımlarını oluştur
    top_pipe = canvas.create_rectangle(
        SCREEN_WIDTH, 0, SCREEN_WIDTH + PIPE_WIDTH, top_pipe_height, fill="green"
    )
    bottom_pipe = canvas.create_rectangle(
        SCREEN_WIDTH, bottom_pipe_height, SCREEN_WIDTH + PIPE_WIDTH, SCREEN_HEIGHT, fill="green"
    )
    pipes.append((top_pipe, bottom_pipe))



def move_pipes():
    """Boruları hareket ettirir."""
    global score
    for pipe in pipes[:]:
        canvas.move(pipe[0], -PIPE_VELOCITY, 0)
        canvas.move(pipe[1], -PIPE_VELOCITY, 0)

        if canvas.coords(pipe[0])[2] < 0:  # Ekranın dışına çıkan borular
            canvas.delete(pipe[0])
            canvas.delete(pipe[1])
            pipes.remove(pipe)
            score += 1
            score_label.config(text=f"Score: {score}")

def move_bird():
    """Kuşu hareket ettirir."""
    global bird_velocity
    bird_velocity += GRAVITY
    canvas.move("bird", 0, bird_velocity)

    # Ekranın üst veya altına çarptıysa
    bird_coords = canvas.coords("bird")
    if bird_coords[1] <= 0 or bird_coords[3] >= SCREEN_HEIGHT:
        stop_game()

def check_collision():
    """Kuşun borulara çarpıp çarpmadığını kontrol eder."""
    bird_coords = canvas.coords("bird")
    for pipe in pipes:
        top_coords = canvas.coords(pipe[0])
        bottom_coords = canvas.coords(pipe[1])

        # Kuş boruların herhangi birine çarptıysa
        if (bird_coords[2] > top_coords[0] and bird_coords[0] < top_coords[2] and 
            (bird_coords[1] < top_coords[3] or bird_coords[3] > bottom_coords[1])):
            return True
    return False

def jump(event):
    """Kuşu zıplatır."""
    global bird_velocity
    if game_running:
        bird_velocity = JUMP_STRENGTH

def game_loop():
    """Oyun döngüsü."""
    if game_running:
        move_bird()
        move_pipes()
        
        if random.randint(1, 100) < 3:  # Boru ekleme sıklığı
            create_pipe()

        if check_collision():
            stop_game()

        root.after(20, game_loop)

# Klavye girişlerini bağla
root.bind("<space>", jump)

# Uygulamayı başlat
root.mainloop()
