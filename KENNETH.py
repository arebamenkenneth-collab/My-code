import turtle
import math

screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0)
screen.title("Kenneth")

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

colors = ["red", "orange", "yellow", "lime", "cyan", "blue", "magenta", "white"]

angle = 0
scale = 1
growing = True
color_index = 0

def draw_kenneth(a, s, color):
    t.clear()

    # Glow circle behind text
    t.penup()
    t.goto(0, -s * 60)
    t.pendown()
    t.pencolor(color)
    t.width(2)
    t.circle(s * 60)

    # Orbiting dots around the name
    for i in range(8):
        orbit_angle = a + i * 45
        ox = 150 * math.cos(math.radians(orbit_angle))
        oy = 80 * math.sin(math.radians(orbit_angle))
        t.penup()
        t.goto(ox, oy)
        t.dot(8, color)

    # Spinning lines
    for i in range(6):
        spin_angle = a + i * 60
        x1 = 180 * math.cos(math.radians(spin_angle))
        y1 = 180 * math.sin(math.radians(spin_angle))
        t.penup()
        t.goto(0, 0)
        t.pendown()
        t.pencolor(color)
        t.width(1)
        t.goto(x1, y1)

    # Kenneth text in center
    t.penup()
    t.goto(0, -30)
    t.pendown()
    t.pencolor(color)
    t.write("KENNETH", align="center",
            font=("Arial", 50, "bold"))

    # Subtitle
    t.penup()
    t.goto(0, -80)
    t.pendown()
    t.pencolor("white")
    t.write("✨ Python Coder ✨", align="center",
            font=("Arial", 16, "normal"))

while True:
    color = colors[color_index % len(colors)]

    draw_kenneth(angle, scale, color)

    # Pulsing effect
    if growing:
        scale += 0.01
        if scale >= 1.3:
            growing = False
    else:
        scale -= 0.01
        if scale <= 0.8:
            growing = True

    angle = (angle + 3) % 360
    color_index += 1

    screen.update()

turtle.done()