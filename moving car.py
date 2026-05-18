import turtle
import time

# Setup
screen = turtle.Screen()
screen.bgcolor("skyblue")
screen.title("Moving Car")
screen.tracer(0)

# ---- DRAW ROAD ----
road = turtle.Turtle()
road.hideturtle()
road.speed(0)

# Ground
road.penup()
road.goto(-400, -120)
road.pendown()
road.color("gray")
road.begin_fill()
for _ in range(2):
    road.forward(800)
    road.right(90)
    road.forward(80)
    road.right(90)
road.end_fill()

# Road dashes
road.color("white")
road.width(3)
for i in range(-400, 400, 60):
    road.penup()
    road.goto(i, -160)
    road.pendown()
    road.forward(30)

# Sun
sun = turtle.Turtle()
sun.hideturtle()
sun.speed(0)
sun.penup()
sun.goto(300, 150)
sun.pendown()
sun.color("yellow")
sun.begin_fill()
sun.circle(40)
sun.end_fill()

# Clouds
def draw_cloud(t, x, y):
    for cx, cy, r in [(x, y, 30), (x+30, y+10, 35), (x+65, y, 30)]:
        t.penup()
        t.goto(cx, cy)
        t.pendown()
        t.color("white")
        t.begin_fill()
        t.circle(r)
        t.end_fill()

cloud = turtle.Turtle()
cloud.hideturtle()
cloud.speed(0)
draw_cloud(cloud, -200, 100)
draw_cloud(cloud, 100, 130)

screen.update()

# ---- CAR DRAWING FUNCTION ----
def draw_car(t, x, y, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color("black")
    t.width(2)

    # Car body (bottom)
    t.color(color)
    t.begin_fill()
    t.goto(x + 120, y)
    t.goto(x + 120, y + 40)
    t.goto(x, y + 40)
    t.goto(x, y)
    t.end_fill()

    # Car roof
    t.color(color)
    t.begin_fill()
    t.penup()
    t.goto(x + 20, y + 40)
    t.pendown()
    t.goto(x + 30, y + 70)
    t.goto(x + 90, y + 70)
    t.goto(x + 100, y + 40)
    t.goto(x + 20, y + 40)
    t.end_fill()

    # Windows
    t.color("lightblue")
    t.begin_fill()
    t.penup()
    t.goto(x + 32, y + 43)
    t.pendown()
    t.goto(x + 38, y + 65)
    t.goto(x + 60, y + 65)
    t.goto(x + 60, y + 43)
    t.goto(x + 32, y + 43)
    t.end_fill()

    t.begin_fill()
    t.penup()
    t.goto(x + 63, y + 43)
    t.pendown()
    t.goto(x + 63, y + 65)
    t.goto(x + 88, y + 65)
    t.goto(x + 95, y + 43)
    t.goto(x + 63, y + 43)
    t.end_fill()

    # Wheels
    for wx, wy in [(x + 25, y - 18), (x + 90, y - 18)]:
        # Outer wheel
        t.penup()
        t.goto(wx, wy)
        t.pendown()
        t.color("black")
        t.begin_fill()
        t.circle(18)
        t.end_fill()
        # Inner wheel hub
        t.penup()
        t.goto(wx + 5, wy + 5)
        t.pendown()
        t.color("gray")
        t.begin_fill()
        t.circle(8)
        t.end_fill()

    # Headlight
    t.penup()
    t.goto(x + 113, y + 15)
    t.pendown()
    t.color("yellow")
    t.begin_fill()
    t.circle(7)
    t.end_fill()

    # Bumper
    t.penup()
    t.goto(x, y + 5)
    t.pendown()
    t.color("silver")
    t.width(4)
    t.goto(x - 5, y + 5)

# ---- ANIMATION ----
car = turtle.Turtle()
car.hideturtle()
car.speed(0)

x = -400

while x < 400:
    car.clear()
    draw_car(car, x, -115, "red")
    screen.update()
    x += 5
    time.sleep(0.01)

turtle.done()