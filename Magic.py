from turtle import*
from colorsys import*

tracer(50)
bgcolor('black')
hideturtle()
pensize(1.5)
goto(0, 210)

for i in range(500):
      color(hsv_to_rgb(i / 500, 1, 1))
      circle(50, 60)
      right(120)
      circle(50, 60)
      left(240)
      forward(i * 0.2)
      circle(30, 90)
      backward(i * 0.1)
      
done()