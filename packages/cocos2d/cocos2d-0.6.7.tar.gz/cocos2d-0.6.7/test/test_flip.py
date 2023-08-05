from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
#

testinfo = "t 0.1, s, t 1, s, t 2, s, t 3, s, t 4.1, s, t 4.2, s, q"
tags = "Flip"

import pyglet
import cocos
from cocos.director import director
from cocos.actions import *
from cocos.layer import *
from pyglet import gl

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw( self ):
        gl.glColor4ub(255, 255, 255, 255)
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        gl.glPopMatrix()

def main():
    director.init( resizable=True )
    main_scene = cocos.scene.Scene()
    main_scene.add( BackgroundLayer(), z=0 )

    def check_grid(self):
        assert self.grid.active == False

    a = Flip( duration=4 )
    # In real code after a sequence of grid actions the StopGrid() action
    # should be called. Omited here to stay in the last grid action render
    main_scene.do( a )

    director.run (main_scene)

if __name__ == '__main__':
    main()
