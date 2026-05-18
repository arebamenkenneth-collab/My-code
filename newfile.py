from turtle import*
tracer(0)
bgcolor("black")
colors = ["red","orange","yellow",
          "green","blue","purple"]

for i in range(360):
    color(colors[i%6])
    forward(i * 0.5)
    right(91)

hideturtle()
update()
done()