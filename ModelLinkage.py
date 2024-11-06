"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random
import math

from Component import Component
from Shapes import Cube,Sphere,Cylinder,Cone
from Point import Point
import ColorType as Ct
import time
from EnvironmentObject import EnvironmentObject

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Linkage(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None
    position = None 

   
    def __init__(self, parent, position, shaderProg):
        super(Linkage, self).__init__(position)
        self.components = []

                        # Create Fish 

        # Fish Body 
        body = Sphere(Point((0, 0, 0)), shaderProg, [0.5, 0.2, 0.2], color=Ct.BLUE)

        # Fish Tail 
        tail = Cone(Point((0, 0, -0.3)), shaderProg, [0.1, 0.1, 0.3], color=Ct.YELLOW)

        # Fish Fins 
        fin1 = Cone(Point((0.3, 0, 0)), shaderProg, [0.05, 0.15, 0.2], color=Ct.BLUEGREEN)
        fin2 = Cone(Point((-0.3, 0, 0)), shaderProg, [0.05, 0.15, 0.2], color=Ct.BLUEGREEN)

        # Fish Eyes 
        eye1 = Sphere(Point((0.15, 0.1, 0.25)), shaderProg, [0.05, 0.05, 0.05], color=Ct.WHITE)
        eye2 = Sphere(Point((-0.15, 0.1, 0.25)), shaderProg, [0.05, 0.05, 0.05], color=Ct.WHITE)

        # Combine Components
        self.fish_components = [body, tail, fin1, fin2, eye1, eye2]

        # Add Fish Components 
        self.addChild(body)  # Body is the main part


        # Attach Fins to the Body
        body.addChild(fin1)
        body.addChild(fin2)

        # Attach Eyes to the Body
        body.addChild(eye1)
        body.addChild(eye2)



        ##### Create Spider 1 #####
        torso1 = Sphere(Point((-0.5, 1, -1)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)
        torso2 = Sphere(Point((-0.555, 1, -1)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)
        torso3 = Sphere(Point((-0.61, 1, -1)), shaderProg, [0.05, 0.05, 0.05], color=Ct.BLACK)

        leg1 = Cylinder(Point((-0.5, 1, -1.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg2 = Cylinder(Point((-0.555, 1, -1.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg3 = Cylinder(Point((-0.61, 1, -1.1)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg4 = Cylinder(Point((-0.5, 1, -0.9)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg5 = Cylinder(Point((-0.555, 1, -0.9)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)
        leg6 = Cylinder(Point((-0.61, 1, -0.9)), shaderProg, [0.01, 0.01, 0.05], color=Ct.BLACK)

        self.spider1_components = [torso1, torso2, torso3, leg1, leg2, leg3, leg4, leg5, leg6]

        # Add spider 1 components
        self.addChild(torso1)
        self.addChild(torso2)
        self.addChild(torso3)
        self.addChild(leg1)
        self.addChild(leg2)
        self.addChild(leg3)
        self.addChild(leg4)
        self.addChild(leg5)
        self.addChild(leg6)

        ##### Create Spider 2 #####
        torso4 = Sphere(Point((1, 1, 0.5)), shaderProg, [0.05, 0.05, 0.05], color=Ct.GRAY)
        torso5 = Sphere(Point((1.055, 1, 0.5)), shaderProg, [0.05, 0.05, 0.05], color=Ct.GRAY)
        torso6 = Sphere(Point((1.11, 1, 0.5)), shaderProg, [0.05, 0.05, 0.05], color=Ct.GRAY)

        leg7 = Cylinder(Point((1, 1, 0.4)), shaderProg, [0.01, 0.01, 0.05], color=Ct.GRAY)
        leg8 = Cylinder(Point((1.055, 1, 0.4)), shaderProg, [0.01, 0.01, 0.05], color=Ct.GRAY)
        leg9 = Cylinder(Point((1.11, 1, 0.4)), shaderProg, [0.01, 0.01, 0.05], color=Ct.GRAY)
        leg10 = Cylinder(Point((1, 1, 0.6)), shaderProg, [0.01, 0.01, 0.05], color=Ct.GRAY)
        leg11 = Cylinder(Point((1.055, 1, 0.6)), shaderProg, [0.01, 0.01, 0.05], color=Ct.GRAY)
        leg12 = Cylinder(Point((1.11, 1, 0.6)), shaderProg, [0.01, 0.01, 0.05], color=Ct.GRAY)

        self.spider2_components = [torso4, torso5, torso6, leg7, leg8, leg9, leg10, leg11, leg12]

        # Add spider 2 components
        self.addChild(torso4)
        self.addChild(torso5)
        self.addChild(torso6)
        self.addChild(leg7)
        self.addChild(leg8)
        self.addChild(leg9)
        self.addChild(leg10)
        self.addChild(leg11)
        self.addChild(leg12)

        ##### Create Spider 3 (Adjusted Position to Fit Inside the Tank) #####
        torso7 = Sphere(Point((0.5, 0.5, 0.5)), shaderProg, [0.05, 0.05, 0.05], color=Ct.SILVER)
        torso8 = Sphere(Point((0.555, 0.5, 0.5)), shaderProg, [0.05, 0.05, 0.05], color=Ct.SILVER)
        torso9 = Sphere(Point((0.61, 0.5, 0.5)), shaderProg, [0.05, 0.05, 0.05], color=Ct.SILVER)

        leg13 = Cylinder(Point((0.5, 0.5, 0.45)), shaderProg, [0.01, 0.01, 0.05], color=Ct.SILVER)
        leg14 = Cylinder(Point((0.555, 0.5, 0.45)), shaderProg, [0.01, 0.01, 0.05], color=Ct.SILVER)
        leg15 = Cylinder(Point((0.61, 0.5, 0.45)), shaderProg, [0.01, 0.01, 0.05], color=Ct.SILVER)
        leg16 = Cylinder(Point((0.5, 0.5, 0.55)), shaderProg, [0.01, 0.01, 0.05], color=Ct.SILVER)
        leg17 = Cylinder(Point((0.555, 0.5, 0.55)), shaderProg, [0.01, 0.01, 0.05], color=Ct.SILVER)
        leg18 = Cylinder(Point((0.61, 0.5, 0.55)), shaderProg, [0.01, 0.01, 0.05], color=Ct.SILVER)

        self.spider3_components = [torso7, torso8, torso9, leg13, leg14, leg15, leg16, leg17, leg18]

        # Add spider 3 components
        self.addChild(torso7)
        self.addChild(torso8)
        self.addChild(torso9)
        self.addChild(leg13)
        self.addChild(leg14)
        self.addChild(leg15)
        self.addChild(leg16)
        self.addChild(leg17)
        self.addChild(leg18)

        # Add all components to a single list for easy iteration
        self.components = self.fish_components + self.spider1_components + self.spider2_components + self.spider3_components

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # Initialize rotation speed if it's not done yet
        if self.rotation_speed is None:
            self.rotation_speed = [[0.5, 0.5, 0.5] for _ in range(len(self.components))]

        # Animate each component
        for i, comp in enumerate(self.components):
            # Rotate component along the uAxis, vAxis, and wAxis
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)

            # Check rotation limits and reverse speed if limits are reached
            if hasattr(comp, 'uAngle') and hasattr(comp, 'uRange') and comp.uAngle in comp.uRange:
                self.rotation_speed[i][0] *= -1
            if hasattr(comp, 'vAngle') and hasattr(comp, 'vRange') and comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if hasattr(comp, 'wAngle') and hasattr(comp, 'wRange') and comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1

        # Rotate the entire Linkage periodically around its vertical axis
        self.vAngle = (self.vAngle + 3) % 360

        # Update all component transformations
        self.update()
        
        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        
        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. Ths means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        
       pass

#class ModelArm(Component):
    """
    Define our linkage model
    """

    #components = None
    #contextParent = None

    #def __init__(self, parent, position, shaderProg, linkageLength=0.5, display_obj=None):
        #super().__init__(position, display_obj)
       # self.components = []
       # self.contextParent = parent

       # limb1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE1)
      #  limb2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
       # limb3 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE3)
      #  limb4 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE4)
       # limb5 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DEEPSKYBLUE)
        
        
       # self.addChild(limb1)
       # limb1.addChild(limb2)
       # limb2.addChild(limb3)
       # limb3.addChild(limb4)
       # limb1.addChild(limb5)   

       # self.components = [limb1, limb2, limb3, limb4, limb5]   