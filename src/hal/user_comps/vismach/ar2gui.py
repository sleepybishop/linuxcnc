#!/usr/bin/python

# graphic model of a AR2 Robot

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
c.newpin("tool-offset", hal.HAL_FLOAT, hal.HAL_IN)
c.ready()

# add a XYZ cross for debug
floor = Collection([
	Box(-100,-100,-0.1,100,100,0),
	Box(-10,-0.1,-10,10,0,10),
	Box(-0.1,-10,-10,0,10,10),
	Color([1,0,0,1],[Box(-10,-10,9.9,10,10,10)]),
	Color([0.3,0.3,0.3,1],[Box(400,-400,-4,-400,400,10)])])
# units are mm

work = Capture()
tool = Capture()

tooltip = Capture()
tool = Translate([tool],0,0, -40)
#tool = HalTranslate([tool],c,"tool-offset",0,0,-1)
tool = Collection([tooltip, tool])
tool = Translate([tool],0,0,0)

# link 7
link7 = AsciiSTL(filename="ar2_link7.stl")
link7 = Color([0.5,0.5,0.5,1],[link7])
link7 = Collection([link7, tool])
link7 = HalRotate([link7],c,"joint6",1,0,0,1)
link7 = Translate([link7],0,0,36.5);

# link 6
link6 = AsciiSTL(filename="ar2_link6.stl")
link6 = Color([0.5,0.5,0.5,1],[link6])
link6 = Collection([link7, link6])
link6 = HalRotate([link6],c,"joint5",1,-1,0,0)
link6 = Translate([link6],0,0,223.63)

# link 5
link5 = AsciiSTL(filename="ar2_link5.stl")
link5 = Color([0.82,0.84,0.85,1],[link5])
link5 = Collection([link6, link5])
link5 = HalRotate([link5],c,"joint4",1,0,0,1) 

# link 4
link4 = AsciiSTL(filename="ar2_link4.stl")
link4 = Color([0.82,0.84,0.85,1],[link4])
link4 = Collection([link5, link4])
link4 = HalRotate([link4],c,"joint3",1,-1,0,0)
link4 = Translate([link4],0,305,0)

# link 3
link3 = AsciiSTL(filename="ar2_link3.stl")
link3 = Color([0.82,0.84,0.85,1],[link3])
link3 = Collection([link4, link3])
link3 = HalRotate([link3],c,"joint2",1,-1,0,0)
link3 = Translate([link3],0,64.2,0)

# link 2
link2 = AsciiSTL(filename="ar2_link2.stl")
link2 = Color([0.82,0.84,0.85,1],[link2])
link2 = Translate([link2], 0,0,-169.77)
link2 = Collection([link3, link2])
link2 = Translate([link2],0,0,169.77)
link2 = Rotate([link2], 90,0,0,1)

link2 = HalRotate([link2],c,"joint1",1,0,0,1)

# link 1
link1 = AsciiSTL(filename="ar2_link1.stl");
link1 = Color([0.5,0.5,0.5,1],[link1])
link1 = Rotate([link1], 90,0,0,1)

# stationary base
robot = Collection([link2, link1])

model = Collection([tooltip, robot, floor, work])

main(model, tooltip, work, 1000, lat=0, lon=0)
