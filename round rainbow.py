import turtle
import math

# Setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Amazing Turtle Animation")
screen.tracer(0)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta", "white", "pink"]

# ---- 1. GALAXY SPIRAL ----
t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.width(1)

for i in range(300):
    t.pencolor(colors[i % len(colors)])
    t.forward(i * 0.5)
    t.left(137.5)  # golden angle = galaxy effect

screen.update()

# ---- 2. NEON WEB ----
t2 = turtle.Turtle()
t2.hideturtle()
t2.speed(0)
t2.width(1)
t2.penup()
t2.goto(0, 0)
t2.pendown()

for i in range(180):
    t2.pencolor(colors[i % len(colors)])
    t2.forward(150)
    t2.right(170)

screen.update()

# ---- 3. RAINBOW RINGS ----
t3 = turtle.Turtle()
t3.hideturtle()
t3.speed(0)
t3.penup()
t3.goto(0, -20)
t3.pendown()

for i in range(10):
    t3.pencolor(colors[i % len(colors)])
    t3.width(i + 1)
    t3.circle(20 + i * 15)
    t3.penup()
    t3.goto(0, -20 - i * 15)
    t3.pendown()

screen.update()

# ---- 4. FIREWORK BURST ----
t4 = turtle.Turtle()
t4.hideturtle()
t4.speed(0)
t4.penup()
t4.goto(0, 0)

for angle in range(0, 360, 10):
    t4.penup()
    t4.goto(0, 0)
    t4.setheading(angle)
    t4.pendown()
    for j in range(30):
        t4.pencolor(colors[j % len(colors)])
        t4.forward(j * 2)
        t4.right(10)

screen.update()

# ---- 5. ANIMATED STAR PULSE ----
pulse = turtle.Turtle()
pulse.hideturtle()
pulse.speed(0)
pulse.width(2)

for frame in range(60):
    pulse.clear()
    size = 50 + frame * 2
    pulse.penup()
    pulse.goto(0, 0)
    pulse.pendown()
    for i in range(5):
        pulse.pencolor(colors[frame % len(colors)])
        pulse.forward(size)
        pulse.right(144)
    screen.update()

# ---- 6. BOUNCING RAINBOW SNAKE ----
snake = turtle.Turtle()
snake.shape("circle")
snake.shapesize(1)
snake.pendown()
snake.width(3)
snake.speed(0)

x, y = -200, 0
dx, dy = 6, 5

for i in range(500):
    snake.pencolor(colors[i % len(colors)])
    snake.goto(x, y)
    x += dx
    y += dy
    if x > 200 or x < -200:
        dx *= -1
    if y > 200 or y < -200:
        dy *= -1
    if i % 10 == 0:
        screen.update()

screen.update()
turtle.done()