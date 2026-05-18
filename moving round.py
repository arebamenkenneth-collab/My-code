import turtle
import colorsys

t = turtle.Turtle()
t.speed(0)
turtle.bgcolor("black")
t.pensize(2)

h=0
for i in range(36):
      color = colorsys.hsv_to_rgb(h,1,1)
      t.color(color)
      for j in range (5):
            t.forward(150)
            t.right(144)
      t.right(10)
      h += 0.028
      
turtle.done()