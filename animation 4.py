import turtle
import math

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Turtle Animation")
screen.tracer(0)

# Create turtle
t = turtle.Turtle()
t.speed(0)
t.width(2)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "violet", "magenta"]

# Draw spinning star spiral
for i in range(200):
    t.pencolor(colors[i % len(colors)])
    t.forward(i * 1.2)
    t.right(91)

screen.update()

# Second turtle - spinning circle flower
t2 = turtle.Turtle()
t2.speed(0)
t2.width(1)
t2.hideturtle()

for i in range(36):
    t2.pencolor(colors[i % len(colors)])
    t2.circle(80)
    t2.right(10)

screen.update()

# Animated bouncing dot
dot = turtle.Turtle()
dot.shape("circle")
dot.color("white")
dot.shapesize(1.5)
dot.penup()

x, y = 0, 0
dx, dy = 5, 4

for _ in range(300):
    dot.goto(x, y)
    x += dx
    y += dy

    if x > 180 or x < -180:
        dx *= -1
        dot.color(colors[_ % len(colors)])
    if y > 180 or y < -180:
        dy *= -1
        dot.color(colors[(_ + 3) % len(colors)])

    screen.update()

turtle.done()