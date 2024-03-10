from matplotlib.artist import setp
from matplotlib.pyplot import figure
from numpy import linspace, pi, poly1d, polyfit, sin

from mpl_toolkits.axisartist import SubplotZero

x = linspace(0, 100, 75)
y = sin(2.0 * pi * x / 60.0 + 0.4)

y1 = poly1d(polyfit(x, y, 1))  # linear
y2 = poly1d(polyfit(x, y, 2))  # quadratic
y3 = poly1d(polyfit(x, y, 3))  # cubic
y4 = poly1d(polyfit(x, y, 4))  # 4th degree

fig = figure(figsize=(6, 4))
ax = SubplotZero(fig, 111)
fig.add_subplot(ax)
ax.grid(True)

ax.plot(x, y1(x), "r", label="linear")
ax.plot(x, y2(x), "g", label="quadratic")
ax.plot(x, y3(x), "orange", label="cubic")
ax.plot(x, y4(x), "b", label="$4^{th}$ order")
ax.plot(x, y, "k.", label="data")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.minorticks_on()
ax.legend(frameon=False, loc=4, labelspacing=0.2)

setp(ax.get_legend().get_texts(), fontsize="small")

fig.savefig("figures/curve_fitting.svg", bbox_inches="tight", pad_inches=0.15)
