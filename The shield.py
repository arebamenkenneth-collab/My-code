from turtle import *
bgcolor('black')
for steps in range(100):
      for c in ('blue', 'red', 'green'):
             color(c)
             forward(steps)
             right(30)
             