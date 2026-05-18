import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.axis("off")

t = np.linspace(0, 2 * np.pi, 1500)

x = 16 * np.sin(t) ** 3
y = (
    13 * np.cos(t)
    - 5 * np.cos(2 * t)
    - 2 * np.cos(3 * t)
    - np.cos(4 * t)
)

ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)

line, = ax.plot([], [], color="red", linewidth=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(x[:i], y[:i])
    return line,

ani = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=len(t), interval=1, blit=True
)

plt.tight_layout()
plt.show()