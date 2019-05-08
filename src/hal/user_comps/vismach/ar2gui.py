#!/usr/bin/env python
#    Copyright 2009 Alex Joni
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# graphic model of the AR2 Robot Arm

# link description
# link1 - stationary base
# link2 .. link7 - the 6 moving parts of the robot, numbered form base to end effector

from vismach import *
import hal

c = hal.component("ar2gui")
c.newpin("joint1", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint2", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint3", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint4", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint5", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint6", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("grip", hal.HAL_FLOAT, hal.HAL_IN)
c.ready()


# add a XYZ cross for debug
#floor = Collection([
#	Box(-100,-100,-0.1,100,100,0),
#	Box(-10,-0.1,-10,10,0,10),
#	Box(-0.1,-10,-10,0,10,10),
##	Color([0,1,0,1],[Box(-10,-10,9.9,10,10,10)]),
#	Color([1,0,0,1],[Box(19.9,-10,-10,20,10,10)])])

# units are inches

floor = Collection([Box(-50,-50,-3,50,50,0)])
floor = Color([0,1,0,0],[floor])

work = Capture()

#tool goes here.. maybe later
tool = Capture()

# "tooltip" for backplot will be the tip of the tool, for now link7
tooltip = Capture()
tool = Collection([tooltip, tool])
tool = Translate([tool], 0.0,0.0,-1.5)

# link 7
link7 = AsciiSTL(filename="ar2_link7.stl")
link7 = Color([0.3,0.3,0.3,1],[link7])
link7 = Collection([link7, tool])
link7 = HalRotate([link7],c,"joint6",1,0,0,1)
link7 = Translate([link7], 0.23,-0.01,0)

# link 6
link6 = AsciiSTL(filename="ar2_link6.stl")
link6 = Collection([link7, link6])
link6 = HalRotate([link6],c,"joint5",1,1,0,0)
link6 = Translate([link6], -0.23,11.41-2.53,0.01)

# link 5, wrist
link5 = AsciiSTL(filename="ar2_link5.stl")
link5 = Color([0.5,0.5,0.5,1],[link5])
# assemble
link5 = Collection([link6, link5])
link5 = HalRotate([link5],c,"joint4",1,0,1,0)
link5 = Translate([link5], 0.23,0,0);

# link4, arm, origin is in the joint3 location
link4 = AsciiSTL(filename="ar2_link4.stl")
#assemble 
link4 = Collection([link5, link4])
link4 = HalRotate([link4],c,"joint3",1,1,0,0)
link4 = Translate([link4],0,0,18.75-6.74)

# link 3, shoulder
link3 = AsciiSTL(filename="ar2_link3.stl")
link3 = Color([0.5,0.5,0.5,1],[link3])
#assemble
link3 = Collection([link4, link3])
link3 = HalRotate([link3],c,"joint2",1,1,0,0)
link3 = Translate([link3],0,2.53,6.74)

# link 2
link2 = AsciiSTL(filename="ar2_link2.stl")
link2 = Collection([link3, link2])
#rotate so X is in X direction
link2 = Rotate([link2], -90,0,0,1)
link2 = HalRotate([link2],c,"joint1",1,0,0,1)

link1 = AsciiSTL(filename="ar2_link1.stl");
link1 = Color([0.5,0.5,0.5,1],[link1])
link1 = Rotate([link1], -90,0,0,1)

# stationary base
ar2 = Collection([link2, link1])
model = Collection([tooltip, ar2, floor, work])


main(model, tooltip, work,50)
