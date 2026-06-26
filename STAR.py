from turtle import *
from colorsys import *

tracer(100)

b = "black"
bgcolor(b)

h = 0

for i in range(520):
    h += 0.0025
    color(hsv_to_rgb(h, 1, 1), b)
    begin_fill()

    for j in range(5):
        forward(150)
        right(150)
        forward(150)
        left(150)
        right(360 / 5)

    end_fill()
    right(2)
    hideturtle()

done()