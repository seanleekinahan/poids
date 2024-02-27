import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

class Group(Slider):
    def __init__(self, screen, x, y, width, height, name, v):
        super().__init__(screen, x, y, width, height, min=v[0], max=v[1], step=v[1]/100)
        self.valueBox = TextBox(screen, x, y+30, width, height, fontSize=20)
        self.valueBox.disable()
        self.labelBox = TextBox(screen, x, y-30, width, height, fontSize=12)
        self.name = name
        self.labelBox.setText(name)
        self.labelBox.disable()
        self.value = v[2]


def init_sliders(screen, bvars):
    xpos = 10
    wid = 100
    incx = wid * 1.5
    height = 30

    ypos = 50

    sliders = []

    for k, v in bvars.items():

        slider = Group(screen, xpos, ypos, wid, height, k, v)
        sliders.append(slider)

        xpos += incx

    return sliders

