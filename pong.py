from tkinter import *
import random

# Variabel global
WIDTH = 800
HEIGHT = 300

PAD_W = 10
PAD_H = 100

BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 40  # Mengurangi kecepatan maksimum bola
BALL_RADIUS = 30

INITIAL_SPEED = 5  # Mengurangi kecepatan awal bola
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED
right_line_distance = WIDTH - PAD_W

PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 1:
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

def spawn_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = INITIAL_SPEED if random.choice([True, False]) else -INITIAL_SPEED
    BALL_Y_SPEED = INITIAL_SPEED if random.choice([True, False]) else -INITIAL_SPEED

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= BALL_SPEED_UP
        BALL_X_SPEED = -BALL_X_SPEED  # Balikkan arah X bola setelah mengenai pad
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

root = Tk()
root.title("Pong")

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()

c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white")

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2, fill="white")
LEFT_PAD = c.create_line(PAD_W/2, 0, PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, PAD_H, width=PAD_W, fill="yellow")
p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_H/4, text=PLAYER_1_SCORE, font="Arial 20", fill="white")
p_2_text = c.create_text(WIDTH/6, PAD_H/4, text=PLAYER_2_SCORE, font="Arial 20", fill="white")

BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0

def move_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    else:
        if ball_right >= right_line_distance:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                update_score(1)
                spawn_ball()
        elif ball_left <= PAD_W:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                update_score(2)
                spawn_ball()
                
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        BALL_Y_SPEED = -BALL_Y_SPEED

    c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)

LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0
PAD_SPEED = 20

def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

def main():
    move_ball()
    move_pads()
    root.after(50, main)  # Mengurangi frekuensi pembaruan untuk memperlambat animasi

c.focus_set()

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

c.bind("<KeyPress>", movement_handler)

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "s"):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

c.bind("<KeyRelease>", stop_pad)

spawn_ball()
main()
root.mainloop()