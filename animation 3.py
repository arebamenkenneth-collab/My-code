from turtle import *

# Setup
speed(0)
bgcolor("black")
hideturtle()
tracer(0)

# Ball
ball = Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 200)

# Trail
trail = Turtle()
trail.hideturtle()
trail.penup()

# Movement
dx = 3
dy = 3
x, y = 0, 200

while True:
    # Clear screen
    clear()
    trail.clear()
    
    # Move ball
    x += dx
    y += dy
    
    # Bounce off walls
    if x > 280 or x < -280:
        dx *= -1
    if y > 280 or y < -280:
        dy *= -1

    # Draw trail
    trail.goto(x, y)
    trail.color("orange")
    trail.dot(10)

    # Move ball
    ball.goto(x, y)
    
    update()