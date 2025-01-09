from abaqus import *
from abaqusConstants import *
import __main__


import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior


#PARAMETERS

R_b = 17.0 #Bending radius
alpha = 25.0 #Bending angle
t_s = 1.4 #Thickness

Elliptical = True
Major_R = 15 #Major radius
Minor_R = 15 #Minor radius
# Vertical_d = 10 #Vertical distance of the point of the hole
Vertical_d = Major_R #This makes Major_R always vertical and Minor_R horizontal

Horizontal_d = 25 #Horizontal distance of the hole

Rectangular = False
Vertical_l = 10
Horizontal_l = 15
Hole_R = 4



# Indenter setup
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, 0.0), angle=90.0)
s.VerticalConstraint(entity=g[2], addUndoState=False)
s.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
s.HorizontalConstraint(entity=g[3], addUndoState=False)
s.FixedConstraint(entity=g[3])
s.FixedConstraint(entity=g[2])
s.rectangle(point1=(-6.25, 7.5), point2=(3.75, 27.5))
s.SymmetryConstraint(entity1=v[0], entity2=v[3], symmetryAxis=g[2])
s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-13.0767669677734, 
    16.1461334228516), value=71.76385276)
s.dragEntity(entity=v[1], points=((-6.25, 27.5), (-6.25, 27.5), (-6.25, 36.25), 
    (-6.93080139160156, 42.9226341247559), (-6.93080139160156, 
    43.3237800598145)))
s.dragEntity(entity=v[0], points=((-6.93080139160156, -28.4400727001855), (
    -6.93080139160156, -28.75), (-6.25, -18.2521457672119), (-5.0, -7.5), (
    -5.0, 0.0), (-5.0, 4.61318206787109), (-5.0, 7.5), (-5.0, 8.75), (
    -4.41963958740234, 10.0), (-4.31919860839844, 11.25), (-5.0, 
    13.1375389099121), (-5.0, 12.5), (-5.0, 11.25), (-5.625, 11.25), (
    -6.25, 11.25)))

s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(-2.63551330566406, 
    90.2025299072266), value=20.0)

s.autoTrimCurve(curve1=g[7], point1=(-3.98425960540771, 9.07618522644043))
s.autoTrimCurve(curve1=g[8], point1=(3.58603763580322, 9.31204414367676))
s.EqualLengthConstraint(entity1=g[4], entity2=g[6])

s.CircleByCenterPerimeter(center=(0.0, 8.75), point1=(-10.0, 11.25))
s.CoincidentConstraint(entity1=v[5], entity2=g[2], addUndoState=False)
s.delete(objectList=(c[33], ))
s.dragEntity(entity=v[5], points=((0.0, 8.75), (0.0, 8.75), (-1.25, 7.5), (
    -1.25, 7.5), (-1.25, 7.5)))
s.dragEntity(entity=v[5], points=((-1.25, 7.5), (-1.25, 7.5), (-2.5, 11.25), (
    -2.5, 12.5), (-2.5, 12.5), (-1.87182998657227, 11.25), (-1.25, 10.0), (
    -1.25, 8.75), (-1.25, 8.75), (-1.25, 7.5), (-1.25, 7.5), (0.0, 6.25), (
    -1.25, 7.5)))
s.CoincidentConstraint(entity1=v[3], entity2=g[9])
s.TangentConstraint(entity1=g[9], entity2=g[4])
s.TangentConstraint(entity1=g[9], entity2=g[6])
s.autoTrimCurve(curve1=g[9], point1=(-6.27261352539062, 17.2192115783691))
s.autoTrimCurve(curve1=g[10], point1=(4.47494888305664, 18.6082038879395))
s.DistanceDimension(entity1=v[0], entity2=g[3], textPoint=(-22.7920227050781, 
    5.9749870300293), value=10.0)

s.dragEntity(entity=g[11], points=((-2.8015100896558, 0.400440571695142), (
    -2.5, 1.25), (-2.5, 2.5), (-2.5, 3.75), (-2.5, 3.75), (-2.5, 5.0), (
    -2.5, 6.25), (-2.5, 6.25), (-2.5, 7.5), (-2.5, 8.75), (-2.5, 8.75), (
    -2.5, 6.25), (-2.5, 6.25), (-2.5, 5.0), (-2.5, 5.0), (-2.5, 3.75), (
    -2.5, 3.75), (-2.5, 2.5), (-2.5, 3.75), (-2.5, 5.0), (-2.5, 5.0)))
s.RadialDimension(curve=g[11], textPoint=(-10.5253391265869, 1.6152286529541), 
    radius=10.0)

p = mdb.models['Model-1'].Part(name='indenter_cylindrical', 
    dimensionality=THREE_D, type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['indenter_cylindrical']
p.BaseSolidExtrude(sketch=s, depth=100.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['indenter_cylindrical']

del mdb.models['Model-1'].sketches['__profile__']


p = mdb.models['Model-1'].parts['indenter_cylindrical']
f, e1 = p.faces, p.edges
p.Mirror(mirrorPlane=f[5], keepOriginal=ON)

p = mdb.models['Model-1'].parts['indenter_cylindrical']
f, e = p.faces, p.edges
t = p.MakeSketchTransform(sketchPlane=f[2], sketchUpEdge=e[1], 
    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 81.763853, 
    0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=433.98, gridSpacing=10.84, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['indenter_cylindrical']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)

s.Line(point1=(-100.0, 0.0), point2=(-100.0, 10.0))
s.VerticalConstraint(entity=g[8], addUndoState=False)
s.ParallelConstraint(entity1=g[4], entity2=g[8], addUndoState=False)
s.CoincidentConstraint(entity1=v[6], entity2=g[4], addUndoState=False)
s.EqualDistanceConstraint(entity1=v[3], entity2=v[4], midpoint=v[6], 
    addUndoState=False)
s.Line(point1=(-100.0, 10.0), point2=(100.0, 10.0))
s.HorizontalConstraint(entity=g[9], addUndoState=False)
s.PerpendicularConstraint(entity1=g[8], entity2=g[9], addUndoState=False)
s.Line(point1=(100.0, 10.0), point2=(100.0, -10.0))
s.VerticalConstraint(entity=g[10], addUndoState=False)
s.PerpendicularConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
s.Line(point1=(100.0, -10.0), point2=(0.0, -10.0))
s.HorizontalConstraint(entity=g[11], addUndoState=False)
s.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
s.Line(point1=(0.0, -10.0), point2=(0.0, 0.0))
s.VerticalConstraint(entity=g[12], addUndoState=False)
s.PerpendicularConstraint(entity1=g[11], entity2=g[12], addUndoState=False)
s.Line(point1=(0.0, 0.0), point2=(-100.0, 0.0))
s.HorizontalConstraint(entity=g[13], addUndoState=False)
s.PerpendicularConstraint(entity1=g[12], entity2=g[13], addUndoState=False)
p = mdb.models['Model-1'].parts['indenter_cylindrical']
f1, e1 = p.faces, p.edges
p.CutExtrude(sketchPlane=f1[2], sketchUpEdge=e1[1], sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=OFF)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']



# Sheet setup

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, 0.0), angle=90.0)
s1.VerticalConstraint(entity=g[2], addUndoState=False)
s1.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
s1.FixedConstraint(entity=g[3])
s1.FixedConstraint(entity=g[2])
s1.CircleByCenterPerimeter(center=(-37.5, 8.75), point1=(-37.5, 0.0))
s1.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)
s1.CircleByCenterPerimeter(center=(-2.5, 36.25), point1=(0.0, 31.25))
s1.CoincidentConstraint(entity1=v[3], entity2=g[2], addUndoState=False)
s1.Line(point1=(-100.0, 0.0), point2=(-37.5, 0.0))
s1.HorizontalConstraint(entity=g[6], addUndoState=False)
s1.ParallelConstraint(entity1=g[3], entity2=g[6], addUndoState=False)
s1.CoincidentConstraint(entity1=v[4], entity2=g[3], addUndoState=False)
s1.Line(point1=(-28.8397459621556, 7.5), point2=(-8.09016994374952, 36.25))
s1.CoincidentConstraint(entity1=v[5], entity2=g[4], addUndoState=False)
s1.CoincidentConstraint(entity1=v[6], entity2=g[5], addUndoState=False)
s1.autoTrimCurve(curve1=g[4], point1=(-39.4355545043945, 14.357949256897))
s1.autoTrimCurve(curve1=g[5], point1=(-4.41466522216797, 25.6752891540527))
s1.autoTrimCurve(curve1=g[9], point1=(5.72931671142578, 30.9727630615234))
s1.TangentConstraint(entity1=g[8], entity2=g[7])
s1.TangentConstraint(entity1=g[10], entity2=g[7])
s1.CoincidentConstraint(entity1=v[10], entity2=g[2])
s1.CoincidentConstraint(entity1=v[11], entity2=g[2])
s1.TangentConstraint(entity1=g[8], entity2=g[3])
s1.autoTrimCurve(curve1=g[10], point1=(3.77738952636719, 80.4501342773438))
s1.CoincidentConstraint(entity1=v[12], entity2=g[2])
s1.CoincidentConstraint(entity1=v[13], entity2=g[2])

s1.offset(distance=1.4, objectList=(g[6], g[7], g[8], g[11]), side=LEFT)

s1.Line(point1=(-100.0, 1.4), point2=(-100.0, 0.0))
s1.VerticalConstraint(entity=g[16], addUndoState=False)
s1.PerpendicularConstraint(entity1=g[12], entity2=g[16], addUndoState=False)

s1.undo()
s1.undo()
s1.redo()

s1.Line(point1=(-100.281227111816, 1.70822036266327), point2=(
    -100.302642822266, -0.387001395225525))

s1.undo()

s1.Line(point1=(-107.5, 7.5), point2=(-107.5, -11.25))
s1.VerticalConstraint(entity=g[16], addUndoState=False)

s1.Line(point1=(3.75, 98.75), point2=(3.75, 88.75))
s1.VerticalConstraint(entity=g[17], addUndoState=False)

s1.CoincidentConstraint(entity1=v[21], entity2=v[18])

s1.CoincidentConstraint(entity1=v[22], entity2=v[12])

s1.CoincidentConstraint(entity1=v[19], entity2=v[14])

s1.CoincidentConstraint(entity1=v[20], entity2=v[4])

s1.ParallelConstraint(entity1=g[14], entity2=g[7])
s1.ParallelConstraint(entity1=g[12], entity2=g[3])
s1.EqualRadiusConstraint(entity1=g[11], entity2=g[13])
s1.ObliqueDimension(vertex1=v[19], vertex2=v[20], textPoint=(-113.005310058594, 
    1.93950271606445), value=1.4)
s1.TangentConstraint(entity1=g[12], entity2=g[13])
s1.TangentConstraint(entity1=g[14], entity2=g[13])
s1.TangentConstraint(entity1=g[15], entity2=g[14])
s1.TangentConstraint(entity1=g[11], entity2=g[7])
s1.DistanceDimension(entity1=v[18], entity2=g[3], textPoint=(38.2222633361816, 
    26.1611824035645), value=60.0)
s1.DistanceDimension(entity1=v[4], entity2=g[2], textPoint=(-48.0425910949707, 
    -13.5062065124512), value=100.0)
s1.AngularDimension(line1=g[7], line2=g[2], textPoint=(-12.4803428649902, 
    -7.53854751586914), value=20.1234)

s1.RadialDimension(curve=g[11], textPoint=(1.48351752758026, 51.7214965820312), 
    radius=11.1234)

d[3].setValues(textPoint=(-7.5, 22.5))
d[3].setValues(textPoint=(-7.5, 22.5))
d[4].setValues(textPoint=(-15.0, 65.0))
d[4].setValues(textPoint=(-15.0, 65.0))

s=mdb.models['Model-1'].sketches['__profile__']
s.Parameter(name='sheet_bending_radius', path='dimensions[4]', 
    expression="{:.9f}".format(R_b))
s.Parameter(name='sheet_bending_angle', path='dimensions[3]', 
    expression="{:.9f}".format(alpha), previousParameter='sheet_bending_radius')
s=mdb.models['Model-1'].sketches['__profile__']
s.Parameter(name='sheet_thickness', path='dimensions[0]', expression="{:.9f}".format(t_s), 
    previousParameter='sheet_bending_angle')
p = mdb.models['Model-1'].Part(name='Sheet', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Sheet']
p.BaseSolidExtrude(sketch=s1, depth=100.0)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Sheet']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


# Support setup

p1 = mdb.models['Model-1'].parts['Sheet']
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.CircleByCenterPerimeter(center=(-2.5, -13.75), point1=(0.0, -6.25))
s.undo()
s.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.ConstructionLine(point1=(0.0, 0.0), angle=90.0)
s.VerticalConstraint(entity=g[3], addUndoState=False)
s.FixedConstraint(entity=g[2])
s.FixedConstraint(entity=g[3])
s.CircleByCenterPerimeter(center=(-3.75, -13.75), point1=(0.0, -6.25))
s.CoincidentConstraint(entity1=v[1], entity2=g[3], addUndoState=False)

s.Line(point1=(-12.0415619758885, -12.5), point2=(-26.25, -48.75))
s.CoincidentConstraint(entity1=v[2], entity2=g[4], addUndoState=False)
s.Line(point1=(-26.25, -48.75), point2=(-6.25, -48.75))
s.HorizontalConstraint(entity=g[6], addUndoState=False)
s.Line(point1=(-6.25, -48.75), point2=(-3.75, -27.5))

s.autoTrimCurve(curve1=g[4], point1=(-6.97449111938477, -26.0954933166504))
s.autoTrimCurve(curve1=g[9], point1=(6.55941390991211, -22.6923828125))
s.CoincidentConstraint(entity1=v[6], entity2=g[3])
s.CoincidentConstraint(entity1=v[7], entity2=g[3])
s.CoincidentConstraint(entity1=v[4], entity2=g[3])
s.CoincidentConstraint(entity1=v[5], entity2=v[6])
s.TangentConstraint(entity1=g[5], entity2=g[8])
s.DistanceDimension(entity1=v[5], entity2=g[2], textPoint=(12.0732231140137, 
    -0.772335052490234), value=1.5)
s.RadialDimension(curve=g[8], textPoint=(-5.06971740722656, -7.57855987548828), 
    radius=11.1234)
s.AngularDimension(line1=g[5], line2=g[3], textPoint=(-13.591064453125, 
    -38.7070274353027), value=21.1234)

s.VerticalDimension(vertex1=v[4], vertex2=v[5], textPoint=(21.9661827087402, 
    -23.4828357696533), value=60.0)
p = mdb.models['Model-1'].Part(name='Support_bottom', dimensionality=THREE_D, 
    type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Support_bottom']
p.BaseSolidExtrude(sketch=s, depth=50.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Support_bottom']

del mdb.models['Model-1'].sketches['__profile__']
    #parameter added to sketch
p = mdb.models['Model-1'].parts['Support_bottom']
s1 = p.features['Solid extrude-1'].sketch
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s1)
s2 = mdb.models['Model-1'].sketches['__edit__']
g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
s2.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s2, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
s=mdb.models['Model-1'].sketches['__edit__']
s.Parameter(name='radius', path='dimensions[1]', expression="{:.9f}".format(R_b)) # <- Bend Radius
s.Parameter(name='angle', path='dimensions[2]', expression="{:.9f}".format(alpha), # <- Bend Angle
    previousParameter='radius')
s.Parameter(name='offset', path='dimensions[0]', expression="{:.9f}".format(t_s), # <- Offset from 0 (sheet Thickness)
    previousParameter='angle')
s2.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Support_bottom']
p.features['Solid extrude-1'].setValues(sketch=s2)
del mdb.models['Model-1'].sketches['__edit__']
p = mdb.models['Model-1'].parts['Support_bottom']
p.regenerate()
    #shell creation & faces deleted
p = mdb.models['Model-1'].parts['Support_bottom']
e = p.edges
p.Round(radius=5.0, edgeList=(e[7], e[9], e[10], e[11]))
p = mdb.models['Model-1'].parts['Support_bottom']
c2 = p.cells
p.RemoveCells(cellList = c2[0:1])

p = mdb.models['Model-1'].parts['Support_bottom']
f1 = p.faces
p.RemoveFaces(faceList = f1[8:10], deleteCells=False)


# Assembly

a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Sheet']
a1.Instance(name='Sheet-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['Support_bottom']
a1.Instance(name='Support_bottom-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['indenter_cylindrical']
a1.Instance(name='indenter_cylindrical-1', part=p, dependent=ON)

a1 = mdb.models['Model-1'].rootAssembly
a1.translate(instanceList=('Sheet-1', ), vector=(0.0, -60.0, 0.0))

a1 = mdb.models['Model-1'].rootAssembly
a1.translate(instanceList=('Support_bottom-1', ), vector=(0.0, 0.0, 50.0))

a1 = mdb.models['Model-1'].rootAssembly
a1.rotate(instanceList=('indenter_cylindrical-1', ), axisPoint=(0.0, 1e-06, 0.0), 
    axisDirection=(0.0, 10.0, 0.0), angle=-90.0)



    

#Top support

session.viewports['Viewport: 1'].view.setValues(nearPlane=314.371, 
    farPlane=506.514, width=400.883, height=179.006, cameraPosition=(
    -75.4593, -31.56, 457.713), cameraUpVector=(0.0292733, 0.976887, 
    -0.211755), cameraTarget=(-48.6156, 20.1337, 47.1657), 
    viewOffsetX=63.7363, viewOffsetY=-11.9984)
p1 = mdb.models['Model-1'].parts['indenter_cylindrical']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.ConstructionLine(point1=(0.0, 3.75), angle=90.0)
s.VerticalConstraint(entity=g[2], addUndoState=False)
s.ConstructionLine(point1=(2.5, 0.0), angle=0.0)
s.HorizontalConstraint(entity=g[3], addUndoState=False)
s.FixedConstraint(entity=g[3])
s.FixedConstraint(entity=g[2])
s.CircleByCenterPerimeter(center=(-5.0, -12.5), point1=(-15.0, -3.75))
session.viewports['Viewport: 1'].view.setValues(nearPlane=167.836, 
    farPlane=209.288, width=257.173, height=114.835, cameraPosition=(
    19.1311, -9.06924, 188.562), cameraTarget=(19.1311, -9.06924, 0))
s.Line(point1=(-17.5, -7.99306090567006), point2=(-35.0, -43.75))
s.CoincidentConstraint(entity1=v[2], entity2=g[4], addUndoState=False)
session.viewports['Viewport: 1'].view.setValues(nearPlane=171.347, 
    farPlane=205.777, width=188.74, height=84.278, cameraPosition=(22.3448, 
    -15.1344, 188.562), cameraTarget=(22.3448, -15.1344, 0))
s.dragEntity(entity=v[0], points=((-5.0, -12.5), (-5.0, -12.5), (-3.75, 
    -13.75), (-2.5, -15.0), (-1.25, -15.0), (-1.25, -16.25), (0.0, 
    -16.25)))
s.dragEntity(entity=v[2], points=((-17.5, -7.99306090567006), (-17.5, -7.5), (
    -15.0, -8.75), (-13.75, -10.0), (-12.5, -10.0), (-11.25, -11.25), (
    -11.25, -11.25)))
s.dragEntity(entity=v[0], points=((0.0, -16.25), (0.0, -16.25), (-3.75, 
    -16.25)))
s.CoincidentConstraint(entity1=v[0], entity2=g[2])
session.viewports['Viewport: 1'].view.setValues(nearPlane=187.872, 
    farPlane=189.251, width=7.72069, height=3.44752, cameraPosition=(
    -5.81396, -11.0709, 188.562), cameraTarget=(-5.81396, -11.0709, 0))
s.CoincidentConstraint(entity1=v[2], entity2=v[1])
session.viewports['Viewport: 1'].view.setValues(nearPlane=183.311, 
    farPlane=193.813, width=65.1585, height=29.0952, cameraPosition=(
    6.73027, -15.4888, 188.562), cameraTarget=(6.73027, -15.4888, 0))
s.TangentConstraint(entity1=g[5], entity2=g[4])
session.viewports['Viewport: 1'].view.setValues(nearPlane=176.074, 
    farPlane=201.049, width=136.911, height=61.1346, cameraPosition=(
    18.2242, -26.168, 188.562), cameraTarget=(18.2242, -26.168, 0))
s.autoTrimCurve(curve1=g[4], point1=(-7.10293197631836, -28.0268173217773))
s.autoTrimCurve(curve1=g[6], point1=(10.0637359619141, -30.7305698394775))
s.dragEntity(entity=v[2], points=((-6.78363465371214, -10.3143196780019), (
    -6.25, -10.0), (-7.5, -12.5), (-7.5, -12.5), (-6.25, -11.25), (-7.5, 
    -10.0), (-8.75, -10.0)))
s.TangentConstraint(entity1=g[5], entity2=g[7])
s.AngularDimension(line1=g[5], line2=g[2], textPoint=(-10.654655456543, 
    -26.167989730835), value=30.123)
s.CoincidentConstraint(entity1=v[7], entity2=g[2])
s.CoincidentConstraint(entity1=v[6], entity2=g[2])
s.VerticalDimension(vertex1=v[3], vertex2=v[6], textPoint=(34.0801544189453, 
    -22.7882976531982), value=35.0)
s.RadialDimension(curve=g[7], textPoint=(-3.97403335571289, -9.35403251647949), 
    radius=10.123)
s.DistanceDimension(entity1=v[6], entity2=g[3], textPoint=(1.0, 0.0), 
    value=1.0)
d[3].setValues(textPoint=(7.5, -5.0))
d[3].setValues(textPoint=(7.5, -5.0))
d[3].setValues(textPoint=(5.0, -1.25))
d[1].setValues(textPoint=(8.75, -18.75))
d[1].setValues(textPoint=(8.75, -18.75))
session.viewports['Viewport: 1'].view.setValues(nearPlane=179.947, 
    farPlane=197.177, width=106.893, height=47.7308, cameraPosition=(
    13.5963, -19.5459, 188.562), cameraTarget=(13.5963, -19.5459, 0))
s=mdb.models['Model-1'].sketches['__profile__']
s.Parameter(name='Outer_Radius', path='dimensions[2]', expression="{:.9f}".format(R_b+t_s))
s.Parameter(name='Bending_angle', path='dimensions[0]', expression="{:.9f}".format(alpha), 
    previousParameter='Outer_Radius')
s.Parameter(name='Vertical_Size', path='dimensions[1]', expression='40', 
    previousParameter='Bending_angle')
s.Parameter(name='vertical_local_offset', path='dimensions[3]', expression='1', 
    previousParameter='Vertical_Size')
p = mdb.models['Model-1'].Part(name='Support_top', dimensionality=THREE_D, 
    type=ANALYTIC_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Support_top']
p.AnalyticRigidSurfExtrude(sketch=s, depth=50.0)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Support_top']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Support_top']
a.Instance(name='Support_top-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].view.setValues(nearPlane=629.507, 
    farPlane=829.35, width=215.78, height=96.3522, cameraPosition=(615.336, 
    163.206, -228.091), cameraUpVector=(-0.54683, 0.830876, 0.103363), 
    cameraTarget=(192.671, 51.8428, -100.765), viewOffsetX=-46.1269, 
    viewOffsetY=-8.5459)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Support_top-1', ), vector=(0.0, 1.1, 0.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=637.419, 
    farPlane=806.205, width=218.492, height=97.5632, cameraPosition=(
    667.085, 68.9304, 147.511), cameraUpVector=(-0.382608, 0.91524, 
    -0.126588), cameraTarget=(226.435, 35.4059, 38.1294), 
    viewOffsetX=-46.7066, viewOffsetY=-8.6533)
a = mdb.models['Model-1'].rootAssembly
a.translate(instanceList=('Support_top-1', ), vector=(0.0, 0.0, 75.0))



#Elliptical hole

if Elliptical:
    p = mdb.models['Model-1'].parts['Sheet']
    f, e1 = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[2], sketchUpEdge=e1[7], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-21.050197, 
        30.24083, 50.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=231.15, gridSpacing=5.77, transform=t)
    g, v, d, c1 = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['Sheet']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=119.953, 
        farPlane=261.412, width=207.388, height=92.594, cameraPosition=(
        -225.546, 105.143, 62.3889), cameraTarget=(-21.0589, 30.217, 62.3889))
    s1.ConstructionLine(point1=(-50.0, 21.5478615609292), angle=0.0)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[6], addUndoState=False)
    s1.HorizontalConstraint(entity=g[6], addUndoState=False)
    s1.ConstructionLine(point1=(-50.0, -21.5478611571636), angle=0.0)
    s1.CoincidentConstraint(entity1=v[2], entity2=g[7], addUndoState=False)
    s1.HorizontalConstraint(entity=g[7], addUndoState=False)
    s1.ConstructionLine(point1=(-50.0, 21.5478615609292), angle=90.0)
    s1.CoincidentConstraint(entity1=v[3], entity2=g[8], addUndoState=False)
    s1.VerticalConstraint(entity=g[8], addUndoState=False)
    s1.EllipseByCenterPerimeter(center=(-27.4075, -1.4425), axisPoint1=(-18.7525, 
        4.3275), axisPoint2=(-23.08, -2.885))
    s1.ConstructionLine(point1=(-27.4075, -1.4425), angle=90.0)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[11], addUndoState=False)
    s1.VerticalConstraint(entity=g[11], addUndoState=False)
    s1.ConstructionLine(point1=(-27.4075, -1.4425), angle=0.0)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[12], addUndoState=False)
    s1.HorizontalConstraint(entity=g[12], addUndoState=False)
    s1.DistanceDimension(entity1=g[11], entity2=g[5], textPoint=(-40.1945953369141, 
        15.4495947625103), value=22.123)
    s1.SymmetryConstraint(entity1=g[3], entity2=g[4], symmetryAxis=g[12])
    s1.SymmetryConstraint(entity1=g[3], entity2=g[4], symmetryAxis=g[12])
    s1.RadialDimension(curve=g[9], textPoint=(-22.7735252380371, 10.9733702059625), 
        majorRadius=14.123)
    s1.RadialDimension(curve=g[9], textPoint=(-33.2774047851562, 
        -10.6404219397356), minorRadius=5.123)
    s1.DistanceDimension(entity1=v[4], entity2=g[12], textPoint=(-5.35244369506836, 
        3.42771750557858), value=7.123)
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Horizontal_Distance', path='dimensions[0]', 
        expression="{:.9f}".format(Horizontal_d))
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Major_Radius', path='dimensions[1]', expression="{:.9f}".format(Major_R), 
        previousParameter='Horizontal_Distance')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Minor_Radius', path='dimensions[2]', expression="{:.9f}".format(Minor_R), 
        previousParameter='Major_Radius')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Vertical_Point_from_middle', path='dimensions[3]', 
        expression="{:.9f}".format(Vertical_d), previousParameter='Minor_Radius')
    p = mdb.models['Model-1'].parts['Sheet']
    f1, e = p.faces, p.edges
    p.CutExtrude(sketchPlane=f1[2], sketchUpEdge=e[7], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    

#Rectangular hole

if Rectangular:
    p = mdb.models['Model-1'].parts['Sheet']
    f, e1 = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[2], sketchUpEdge=e1[7], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(-21.050197, 
        30.24083, 50.0))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=231.15, gridSpacing=5.77, transform=t)
    g, v, d, c1 = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['Sheet']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.ConstructionLine(point1=(-50.0, 21.5478615609292), angle=0.0)
    s.CoincidentConstraint(entity1=v[3], entity2=g[6], addUndoState=False)
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.ConstructionLine(point1=(-50.0, -21.5478611571636), angle=0.0)
    s.CoincidentConstraint(entity1=v[2], entity2=g[7], addUndoState=False)
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.ConstructionLine(point1=(-50.0, 21.5478615609292), angle=90.0)
    s.CoincidentConstraint(entity1=v[3], entity2=g[8], addUndoState=False)
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.rectangle(point1=(-36.0625, 10.0975), point2=(-17.31, -10.0975))
    s.ConstructionLine(point1=(-27.4075, 2.885), angle=90.0)
    s.VerticalConstraint(entity=g[13], addUndoState=False)
    s.ConstructionLine(point1=(-27.4075, 1.44250000000233), angle=0.0)
    s.HorizontalConstraint(entity=g[14], addUndoState=False)
    s.SymmetryConstraint(entity1=g[4], entity2=g[3], symmetryAxis=g[14])
    s.DistanceDimension(entity1=g[13], entity2=g[8], textPoint=(-42.7902221679688, 
        13.8899969431491), value=22.123)
    s.SymmetryConstraint(entity1=g[9], entity2=g[11], symmetryAxis=g[13])
    s.SymmetryConstraint(entity1=g[10], entity2=g[12], symmetryAxis=g[14])
    
    s.ArcByStartEndTangent(point1=(-31.735, 10.0975002018827), point2=(-36.0625, 
        4.3275), entity=g[12])
    s.CoincidentConstraint(entity1=v[8], entity2=g[12], addUndoState=False)
    s.CoincidentConstraint(entity1=v[9], entity2=g[9], addUndoState=False)
    s.ArcByStartEndTangent(point1=(-31.735, 2.885), point2=(-24.5225, 
        10.0975002018827), vector=(1.0, 0.0))
    s.CoincidentConstraint(entity1=v[12], entity2=g[12], addUndoState=False)
    s.ArcByStartEndTangent(point1=(-19.6915, 4.3275), point2=(-21.6375, 2.885), 
        entity=g[11])
    s.CoincidentConstraint(entity1=v[13], entity2=g[11], addUndoState=False)
    s.ArcByStartEndTangent(point1=(-25.965, 4.3275), point2=(-23.08, 
        -10.0974997981171), vector=(1.0, 0.0))
    s.CoincidentConstraint(entity1=v[17], entity2=g[10], addUndoState=False)
    s.undo()
    s.undo()
    s.undo()
    s.undo()
    s.CircleByCenterPerimeter(center=(-33.1775, -4.3275), point1=(-36.0625, 
        -5.11010038666941))
    s.CoincidentConstraint(entity1=v[9], entity2=g[9], addUndoState=False)
    s.CircleByCenterPerimeter(center=(-33.1775, 5.77), point1=(-31.735, 
        10.0975002018827))
    s.CoincidentConstraint(entity1=v[11], entity2=g[12], addUndoState=False)
    s.CircleByCenterPerimeter(center=(-23.08, 7.2125), point1=(-25.965, 
        10.0975002018827))
    s.CoincidentConstraint(entity1=v[13], entity2=g[12], addUndoState=False)
    s.CircleByCenterPerimeter(center=(-23.08, -7.2125), point1=(-19.6915, -7.2125))
    s.CoincidentConstraint(entity1=v[15], entity2=g[11], addUndoState=False)
    s.TangentConstraint(entity1=g[15], entity2=g[9])
    s.TangentConstraint(entity1=g[15], entity2=g[10])
    s.TangentConstraint(entity1=g[18], entity2=g[10])
    s.TangentConstraint(entity1=g[18], entity2=g[11])
    s.TangentConstraint(entity1=g[17], entity2=g[11])
    s.TangentConstraint(entity1=g[17], entity2=g[12])
    s.TangentConstraint(entity1=g[16], entity2=g[12])
    s.TangentConstraint(entity1=g[16], entity2=g[9])
    s.EqualRadiusConstraint(entity1=g[15], entity2=g[18])
    s.EqualRadiusConstraint(entity1=g[18], entity2=g[17], addUndoState=False)
    s.EqualRadiusConstraint(entity1=g[17], entity2=g[16], addUndoState=False)
    
    s.autoTrimCurve(curve1=g[12], point1=(-20.5837497711182, 10.016645434097))
    s.autoTrimCurve(curve1=g[11], point1=(-19.7443561553955, 9.36076528284315))
    s.autoTrimCurve(curve1=g[20], point1=(-19.9268321990967, -9.7323715777395))
    s.autoTrimCurve(curve1=g[10], point1=(-20.3282814025879, -10.0967372388784))
    s.autoTrimCurve(curve1=g[22], point1=(-35.3278846740723, -9.98742419933051))
    s.autoTrimCurve(curve1=g[9], point1=(-36.1672782897949, -9.40443245909586))
    s.autoTrimCurve(curve1=g[15], point1=(-34.6344718933105, -3.61090195306586))
    s.autoTrimCurve(curve1=g[18], point1=(-25.4741306304932, -4.08458590343522))
    s.autoTrimCurve(curve1=g[17], point1=(-24.8537101745605, 3.71299202187061))
    s.autoTrimCurve(curve1=g[16], point1=(-29.9995594024658, 4.47817279934057))
    s.autoTrimCurve(curve1=g[19], point1=(-35.5103607177734, 10.0895090184527))
    s.autoTrimCurve(curve1=g[24], point1=(-36.1672782897949, 9.76158039917422))
    s.HorizontalConstraint(entity=g[29])
    s.HorizontalConstraint(entity=g[23])
    s.VerticalConstraint(entity=g[30])
    s.VerticalConstraint(entity=g[21])
    s.CoincidentConstraint(entity1=v[25], entity2=g[30])
    s.CoincidentConstraint(entity1=g[28], entity2=v[24])
    s.CoincidentConstraint(entity1=g[29], entity2=v[13])
    s.dragEntity(entity=v[24], points=((-32.5752133899715, 9.99871359185438), (
        -32.5752133899715, 10.0975), (-32.7367134094238, 9.54295432007846), (
        -32.6272277832031, 10.0975), (-32.4812450408936, 10.0975), (
        -32.3717575073242, 10.0975)))
    s.TangentConstraint(entity1=g[28], entity2=g[29])
    s.TangentConstraint(entity1=g[27], entity2=g[29])
    s.TangentConstraint(entity1=g[27], entity2=g[21])
    s.TangentConstraint(entity1=g[21], entity2=g[26])
    s.TangentConstraint(entity1=g[26], entity2=g[23])
    s.TangentConstraint(entity1=g[23], entity2=g[25])
    s.TangentConstraint(entity1=g[25], entity2=g[30])
    s.TangentConstraint(entity1=g[30], entity2=g[28])
    s.EqualRadiusConstraint(entity1=g[28], entity2=g[27])
    s.EqualRadiusConstraint(entity1=g[27], entity2=g[26], addUndoState=False)
    s.EqualRadiusConstraint(entity1=g[26], entity2=g[25], addUndoState=False)
    
    s.RadialDimension(curve=g[28], textPoint=(-38.0235633850098, 10.388612052593), 
        radius=3.123)
    s.DistanceDimension(entity1=g[29], entity2=g[23], textPoint=(-41.9023246765137, 
        1.20362046479699), value=20.123)
    s.DistanceDimension(entity1=g[30], entity2=g[21], textPoint=(-25.5916290283203, 
        15.0555769079843), value=15.123)
    
    s.SymmetryConstraint(entity1=g[30], entity2=g[21], symmetryAxis=g[13])
    s.SymmetryConstraint(entity1=g[23], entity2=g[29], symmetryAxis=g[14])
    
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Horizontal_Distance', path='dimensions[0]', 
        expression="{:.9f}".format(Horizontal_d))
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Vertical_Length', path='dimensions[2]', expression="{:.9f}".format(Vertical_l), 
        previousParameter='Horizontal_Distance')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Horizontal_Length', path='dimensions[3]', 
        expression="{:.9f}".format(Horizontal_l), previousParameter='Vertical_Length')
    s=mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Radius', path='dimensions[1]', expression="{:.9f}".format(Hole_R), 
        previousParameter='Horizontal_Length')
    # s.Parameter(name='Horizontal_Distance', path='dimensions[0]', 
    #     expression='20.123')
    # s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='Vertical_Length', path='dimensions[2]', expression='30.123', 
    #     previousParameter='Horizontal_Distance')
    # s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='Horizontal_Length', path='dimensions[3]', 
    #     expression='12.123', previousParameter='Vertical_Length')
    # s=mdb.models['Model-1'].sketches['__profile__']
    # s.Parameter(name='Radius', path='dimensions[1]', expression='4.123', 
    #     previousParameter='Horizontal_Length')
    
    p = mdb.models['Model-1'].parts['Sheet']
    f1, e = p.faces, p.edges
    p.CutExtrude(sketchPlane=f1[2], sketchUpEdge=e[7], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s, flipExtrudeDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
