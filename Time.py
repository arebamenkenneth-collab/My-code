import turtle
import time

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Clock")
screen.tracer(0)

def draw_hand(t, angle, length, color, width):
    t.penup()
    t.goto(0, 0)
    t.setheading(90 - angle)
    t.pendown()
    t.pensize(width)
    t.pencolor(color)
    t.forward(length)

def draw_clock_face(t):
    t.penup()
    t.goto(0, -180)
    t.pendown()
    t.pencolor("white")
    t.pensize(2)
    t.circle(180)
    for i in range(60):
        angle = i * 6
        x = 165 * __import__('math').sin(__import__('math').radians(angle))
        y = 165 * __import__('math').cos(__import__('math').radians(angle))
        t.penup()
        t.goto(x, y)
        t.pendown()
        if i % 5 == 0:
            t.pensize(3)
            length = 15
        else:
            t.pensize(1)
            length = 7
        t.setheading(180 + angle)
        t.forward(length)

face = turtle.Turtle()
face.hideturtle()
face.speed(0)
draw_clock_face(face)

hand = turtle.Turtle()
hand.hideturtle()
hand.speed(0)

while True:
    t = time.localtime()
    h = t.tm_hour % 12
    m = t.tm_min
    s = t.tm_sec

    hand.clear()

    # Hour hand (red)
    draw_hand(hand, (h * 30) + (m * 0.5), 80, "red", 4)
    # Minute hand (yellow/orange)
    draw_hand(hand, m * 6, 120, "orange", 3)
    # Second hand (yellow-green)
    draw_hand(hand, s * 6, 150, "yellow", 1)

    screen.update()
    time.sleep(1)