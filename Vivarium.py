"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener
"""
import wx
import numpy as np
from Point import Point
from Component import Component
from ModelTank import Tank
from EnvironmentObject import EnvironmentObject
from ModelLinkage import Linkage
from Shapes import Cube

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")

class Vivarium(Component):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent, shaderProg):
        self.parent = parent
        self.shaderProg = shaderProg

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(Point((0,0,0)), shaderProg, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]

        self.addNewObjInTank(Linkage(parent, Point((0,0,0)), shaderProg))

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """
            
        for c in self.components[::-1]:
            if isinstance(c, EnvironmentObject):
                c.animationUpdate()
                c.stepForward(self.components, self.tank_dimensions, self)
        
        self.update()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components


def addFood(self):
        """
        Add a chunk of food to the vivarium at a random position within the tank.
        """
        # Generate random position for food within tank dimensions
        x = np.random.uniform(-self.tank_dimensions[0] / 2, self.tank_dimensions[0] / 2)
        y = self.tank_dimensions[1] / 2
        z = np.random.uniform(-self.tank_dimensions[2] / 2, self.tank_dimensions[2] / 2)
        print(f"Food added at position: ({x}, {y}, {z})")
        food = Cube(Point((x, y, z)), self.shaderProg)
        self.addNewObjInTank(food)

def handleKeyPress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_F:  # Check for 'f' key
            print("F key pressed")  # Debugging line
            self.addFood()
                
    