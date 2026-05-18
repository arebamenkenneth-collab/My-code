import turtle

t = turtle.Turtle()
t.speed(0)
turtle.Screen().bgcolor("black")
colors = ["cyan", "magenta", "yellow", "lime"]

for x in range(200):
    t.pencolor(colors[x % 4])
    t.forward(x * 2)
    t.left(91)