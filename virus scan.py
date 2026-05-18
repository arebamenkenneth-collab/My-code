import turtle
import math
import random

screen = turtle.Screen()
screen.bgcolor("black")
screen.tracer(0)

# Radar turtle
t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# Beam turtle
beam = turtle.Turtle()
beam.hideturtle()
beam.width(3)
beam.speed(0)

# Dots turtle (drawn LAST so it's on top)
dots_turtle = turtle.Turtle()
dots_turtle.hideturtle()
dots_turtle.speed(0)
dots_turtle.penup()

def draw_radar():
    t.clear()
    t.color("green")
    for r in [50, 100, 150, 200]:
        t.penup()
        t.goto(0, -r)
        t.pendown()
        t.circle(r)
    t.penup()
    t.goto(-200, 0)
    t.pendown()
    t.goto(200, 0)
    t.penup()
    t.goto(0, -200)
    t.pendown()
    t.goto(0, 200)

def draw_beam():
    beam.clear()
    beam.color("lime")
    x = 200 * math.cos(math.radians(angle))
    y = 200 * math.sin(math.radians(angle))
    beam.penup()
    beam.goto(0, 0)
    beam.pendown()
    beam.goto(x, y)

def draw_dots():
    dots_turtle.clear()
    for tx, ty in targets:
        dots_turtle.goto(tx, ty)
        dots_turtle.dot(15, "red")

targets = [(random.randint(-140, 140), random.randint(-140, 140)) for _ in range(6)]

angle = 0

while True:
    draw_radar()   # 1st - background
    draw_beam()    # 2nd - beam
    draw_dots()    # 3rd - dots on TOP
    angle = (angle + 2) % 360
    screen.update()

turtle.done()