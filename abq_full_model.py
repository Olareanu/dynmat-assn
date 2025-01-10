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

# PARAMETERS -----------------------------------------------------------------------------------------------------

R_b = 17.0  # Bending radius
alpha = 25.0  # Bending angle
t_s = 1.4  # Thickness

sheetVersion = 4
# 1 simple sheet, uniform mesh
# 2 simple sheet, variable element size
# 3 elliptical hole
# 4 rectangular hole


def Fake_material_import():
    from material import createMaterialFromDataString
    createMaterialFromDataString('Model-1', 'AA7020-T6', '2024',
                                 """{'density': {'dependencies': 0, 'distributionType': UNIFORM, 'fieldName': '', 'table': ((2.78e-09,),), 'temperatureDependency': OFF}, 'description': '', 'elastic': {'dependencies': 0, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'table': ((74000.0, 0.33),), 'temperatureDependency': OFF, 'type': ISOTROPIC}, 'hosfordCoulombDamageInitiation': {'accumulationPower': 0.0, 'alpha': 0.0, 'angSmooth': 70.0, 'anglemax': 85.0, 'damageEvolutionList': [], 'definition': MSFLD, 'dependencies': 0, 'direction': NMORI, 'failureMechanisms': 1, 'feq': 10.0, 'fnn': 10.0, 'fnt': 10.0, 'frequency': 1, 'growthTolerance': 0.05, 'hasGrowthTolerance': OFF, 'hasUnstableGrowthTolerance': OFF, 'iniSmooth': YES, 'ks': 0.0, 'lodeDependency': OFF, 'npoly': QUADRATIC, 'numberImperfections': 4, 'omega': 1.0, 'peinc': 0.002, 'position': CENTROID, 'properties': 1, 'rCrackDirection': 0.0, 'rateDependency': OFF, 'refEnergy': 1.0, 'smoothing': NONE, 'table': ((1.25, 0.61, 0.04, 0.1, 0.0, 0.0),), 'temperatureDependency': OFF, 'tolerance': 0.05, 'unstableGrowthTolerance': 0.0, 'weightingMethod': UNIFORM}, 'inelasticHeatFraction': {'fraction': 0.9}, 'materialIdentifier': '', 'name': 'AA7020-T6', 'plastic': {'dataType': HALF_CYCLE, 'dependencies': 0, 'extrapolation': CONSTANT, 'hardening': ISOTROPIC, 'numBackstresses': 1, 'rate': OFF, 'scaleStress': None, 'staticRecovery': OFF, 'strainRangeDependency': OFF, 'table': ((327.188488218514, 0.0, 25.0), (343.58331243496, 0.00505050505050505, 25.0), (358.639154794304, 0.0101010101010101, 25.0),  (3.62227728752342, 0.474747474747475, 336.0), (3.62467648617164, 0.47979797979798, 336.0), (3.62702527697417, 0.484848484848485, 336.0), (3.6293256270531, 0.48989898989899, 336.0), (3.63157941754504, 0.494949494949495, 336.0)), 'temperatureDependency': ON}, 'specificHeat': {'dependencies': 0, 'law': CONSTANTVOLUME, 'table': ((897000000.0,),), 'temperatureDependency': OFF}}""")

    from material import createMaterialFromDataString
    createMaterialFromDataString('Model-1', 'DP590', '2024',
                                 """{'density': {'dependencies': 0, 'distributionType': UNIFORM, 'fieldName': '', 'table': ((7.85e-09,),), 'temperatureDependency': OFF}, 'description': '', 'elastic': {'dependencies': 0, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'table': ((210000.0, 0.33),), 'temperatureDependency': OFF, 'type': ISOTROPIC}, 'hosfordCoulombDamageInitiation': {'accumulationPower': 0.0, 'alpha': 0.0, 'angSmooth': 70.0, 'anglemax': 85.0, 'damageEvolutionList': [], 'definition': MSFLD, 'dependencies': 0, 'direction': NMORI, 'failureMechanisms': 1, 'feq': 10.0, 'fnn': 10.0, 'fnt': 10.0, 'frequency': 1, 'growthTolerance': 0.05, 'hasGrowthTolerance': OFF, 'hasUnstableGrowthTolerance': OFF, 'iniSmooth': YES, 'ks': 0.0, 'lodeDependency': OFF, 'npoly': QUADRATIC, 'numberImperfections': 4, 'omega': 1.0, 'peinc': 0.002, 'position': CENTROID, 'properties': 1, 'rCrackDirection': 0.0, 'rateDependency': OFF, 'refEnergy': 1.0, 'smoothing': NONE, 'table': ((1.97, 0.85, 0.0, 0.1, 0.025, 0.00116),), 'temperatureDependency': OFF, 'tolerance': 0.05, 'unstableGrowthTolerance': 0.0, 'weightingMethod': UNIFORM}, 'inelasticHeatFraction': {'fraction': 0.9}, 'materialIdentifier': '', 'name': 'DP590', 'plastic': {'dataType': HALF_CYCLE, 'dependencies': 0, 'extrapolation': CONSTANT, 'hardening': ISOTROPIC, 'numBackstresses': 1, 'rate': OFF, 'rateDependent': {'dependencies': 0, 'table': ((0.01366, 0.00116),), 'temperatureDependency': OFF, 'type': JOHNSON_COOK}, 'scaleStress': None, 'staticRecovery': OFF, 'strainRangeDependency': OFF, 'table': ((301.296571946004, 0.0, 20.0), (381.271918211176, 0.00505050505050505, 20.0), (423.669914527771, 0.0101010101010101, 20.0), (455.224474706246, 0.0151515151515152, 20.0), (480.85452615325, 0.0202020202020202, 20.0), (502.525562212003, 0.0252525252525253, 20.0), (0.536696921792872, 0.444444444444444, 1399.7), (0.537538285979922, 0.44949494949495, 1399.7), (0.538372122159436, 0.454545454545455, 1399.7), (0.539198581090773, 0.45959595959596, 1399.7), (0.54001780879417, 0.464646464646465, 1399.7), (0.540829946759487, 0.46969696969697, 1399.7), (0.541635132142709, 0.474747474747475, 1399.7), (0.542433497951128, 0.47979797979798, 1399.7), (0.543225173218022, 0.484848484848485, 1399.7), (0.544010283167602, 0.48989898989899, 1399.7), (0.544788949370914, 0.494949494949495, 1399.7)), 'temperatureDependency': ON}, 'specificHeat': {'dependencies': 0, 'law': CONSTANTVOLUME, 'table': ((420000000.0,),), 'temperatureDependency': OFF}}""")
    from material import createMaterialFromDataString
    createMaterialFromDataString('Model-1', 'Mars300', '2024',
                                 """{'density': {'dependencies': 0, 'distributionType': UNIFORM, 'fieldName': '', 'table': ((7.85e-09,),), 'temperatureDependency': OFF}, 'description': '', 'elastic': {'dependencies': 0, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'table': ((200000.0, 0.3),), 'temperatureDependency': OFF, 'type': ISOTROPIC}, 'hosfordCoulombDamageInitiation': {'accumulationPower': 0.0, 'alpha': 0.0, 'angSmooth': 70.0, 'anglemax': 85.0, 'damageEvolutionList': [], 'definition': MSFLD, 'dependencies': 0, 'direction': NMORI, 'failureMechanisms': 1, 'feq': 10.0, 'fnn': 10.0, 'fnt': 10.0, 'frequency': 1, 'growthTolerance': 0.05, 'hasGrowthTolerance': OFF, 'hasUnstableGrowthTolerance': OFF, 'iniSmooth': YES, 'ks': 0.0, 'lodeDependency': OFF, 'npoly': QUADRATIC, 'numberImperfections': 4, 'omega': 1.0, 'peinc': 0.002, 'position': CENTROID, 'properties': 1, 'rCrackDirection': 0.0, 'rateDependency': OFF, 'refEnergy': 1.0, 'smoothing': NONE, 'table': ((1.349, 0.3254, 0.0755, 0.1, 0.0494, 0.001),), 'temperatureDependency': OFF, 'tolerance': 0.05, 'unstableGrowthTolerance': 0.0, 'weightingMethod': UNIFORM}, 'inelasticHeatFraction': {'fraction': 0.9}, 'materialIdentifier': '', 'name': 'Mars300', 'plastic': {'dataType': HALF_CYCLE, 'dependencies': 0, 'extrapolation': CONSTANT, 'hardening': ISOTROPIC, 'numBackstresses': 1, 'rate': OFF, 'rateDependent': {'dependencies': 0, 'table': ((0.00188, 0.001),), 'temperatureDependency': OFF, 'type': JOHNSON_COOK}, 'scaleStress': None, 'staticRecovery': OFF, 'strainRangeDependency': OFF, 'table': ((1291.28230167438, 0.0, 25.0), (1691.49508355032, 0.00505050505050505, 25.0), (1928.22268707266, 0.0101010101010101, 25.0), (2081.61582921982, 0.0151515151515152, 25.0), (2182.80461741624, 0.0202020202020202, 25.0), (2250.49854386272, 0.0252525252525253, 25.0), (2296.5000724524, 0.0303030303030303, 25.0), (2328.36590583805, 0.0353535353535354, 25.0), (2.8166722674982, 0.45959595959596, 1286.0), (2.81773205801661, 0.464646464646465, 1286.0), (2.81878250023503, 0.46969696969697, 1286.0), (2.81982377570767, 0.474747474747475, 1286.0), (2.82085606057894, 0.47979797979798, 1286.0), (2.8218795257996, 0.484848484848485, 1286.0), (2.82289433733213, 0.48989898989899, 1286.0), (2.82390065634595, 0.494949494949495, 1286.0)), 'temperatureDependency': ON}, 'specificHeat': {'dependencies': 0, 'law': CONSTANTVOLUME, 'table': ((449000000.0,),), 'temperatureDependency': OFF}}""")
    from material import createMaterialFromDataString
    createMaterialFromDataString('Model-1', 'TRIP780', '2024',
                                 """{'density': {'dependencies': 0, 'distributionType': UNIFORM, 'fieldName': '', 'table': ((7.85e-09,),), 'temperatureDependency': OFF}, 'description': '', 'elastic': {'dependencies': 0, 'moduli': LONG_TERM, 'noCompression': OFF, 'noTension': OFF, 'table': ((185000.0, 0.33),), 'temperatureDependency': OFF, 'type': ISOTROPIC}, 'hosfordCoulombDamageInitiation': {'accumulationPower': 0.0, 'alpha': 0.0, 'angSmooth': 70.0, 'anglemax': 85.0, 'damageEvolutionList': [], 'definition': MSFLD, 'dependencies': 0, 'direction': NMORI, 'failureMechanisms': 1, 'feq': 10.0, 'fnn': 10.0, 'fnt': 10.0, 'frequency': 1, 'growthTolerance': 0.05, 'hasGrowthTolerance': OFF, 'hasUnstableGrowthTolerance': OFF, 'iniSmooth': YES, 'ks': 0.0, 'lodeDependency': OFF, 'npoly': QUADRATIC, 'numberImperfections': 4, 'omega': 1.0, 'peinc': 0.002, 'position': CENTROID, 'properties': 1, 'rCrackDirection': 0.0, 'rateDependency': OFF, 'refEnergy': 1.0, 'smoothing': NONE, 'table': ((1.22, 1.27, 0.11, 0.1, 0.066, 0.00321),), 'temperatureDependency': OFF, 'tolerance': 0.05, 'unstableGrowthTolerance': 0.0, 'weightingMethod': UNIFORM}, 'inelasticHeatFraction': {'fraction': 0.9}, 'materialIdentifier': '', 'name': 'TRIP780', 'plastic': {'dataType': HALF_CYCLE, 'dependencies': 0, 'extrapolation': CONSTANT, 'hardening': ISOTROPIC, 'numBackstresses': 1, 'rate': OFF, 'rateDependent': {'dependencies': 0, 'table': ((0.00557, 0.00321),), 'temperatureDependency': OFF, 'type': JOHNSON_COOK}, 'scaleStress': None, 'staticRecovery': OFF, 'strainRangeDependency': OFF, 'table': ((455.905190819261, 0.0, 20.0), (515.516667636567, 0.00505050505050505, 20.0), (560.012315608165, 0.0101010101010101, 20.0), (596.746478885304, 0.0151515151515152, 20.0), (628.392879726293, 0.0202020202020202, 20.0), (656.293543970297, 0.0252525252525253, 20.0), (681.248594002095, 0.0303030303030303, 20.0), (703.790006538981, 0.0353535353535354, 20.0), (724.298922543404, 0.0404040404040404, 20.0), (743.06343615584, 0.0454545454545455, 20.0), (760.310074106556, 0.0505050505050505, 20.0), (776.222316217459, 0.0555555555555556, 20.0), (790.952182775596, 0.0606060606060606, 20.0), (804.627860519038, 0.0656565656565657, 20.0), (0.750777532410493, 0.444444444444444, 1532.7), (0.752016610485918, 0.44949494949495, 1532.7), (0.753245040599822, 0.454545454545455, 1532.7), (0.754463047722154, 0.45959595959596, 1532.7), (0.755670848567007, 0.464646464646465, 1532.7), (0.756868652039358, 0.46969696969697, 1532.7), (0.758056659651093, 0.474747474747475, 1532.7), (0.759235065908738, 0.47979797979798, 1532.7), (0.760404058675082, 0.484848484848485, 1532.7), (0.761563819506725, 0.48989898989899, 1532.7), (0.762714523969389, 0.494949494949495, 1532.7)), 'temperatureDependency': ON}, 'specificHeat': {'dependencies': 0, 'law': CONSTANTVOLUME, 'table': ((420000000.0,),), 'temperatureDependency': OFF}}""")


def Cyl_Indenter():
    # Geometry
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
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
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-13.0767669677734, 16.1461334228516), value=71.76385276)
    s.dragEntity(entity=v[1], points=((-6.25, 27.5), (-6.25, 27.5), (-6.25, 36.25),
                                      (-6.93080139160156, 42.9226341247559), (-6.93080139160156, 43.3237800598145)))
    s.dragEntity(entity=v[0], points=((-6.93080139160156, -28.4400727001855), (
        -6.93080139160156, -28.75), (-6.25, -18.2521457672119), (-5.0, -7.5), (-5.0, 0.0), (-5.0, 4.61318206787109),
                                      (-5.0, 7.5), (-5.0, 8.75), (-4.41963958740234, 10.0), (-4.31919860839844, 11.25),
                                      (-5.0, 13.1375389099121), (-5.0, 12.5), (-5.0, 11.25), (-5.625, 11.25),
                                      (-6.25, 11.25)))

    s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(-2.63551330566406, 90.2025299072266), value=20.0)

    s.autoTrimCurve(curve1=g[7], point1=(-3.98425960540771, 9.07618522644043))
    s.autoTrimCurve(curve1=g[8], point1=(3.58603763580322, 9.31204414367676))
    s.EqualLengthConstraint(entity1=g[4], entity2=g[6])

    s.CircleByCenterPerimeter(center=(0.0, 8.75), point1=(-10.0, 11.25))
    s.CoincidentConstraint(entity1=v[5], entity2=g[2], addUndoState=False)
    s.delete(objectList=(c[33],))
    s.dragEntity(entity=v[5], points=((0.0, 8.75), (0.0, 8.75), (-1.25, 7.5), (
        -1.25, 7.5), (-1.25, 7.5)))
    s.dragEntity(entity=v[5], points=((-1.25, 7.5), (-1.25, 7.5), (-2.5, 11.25), (
        -2.5, 12.5), (-2.5, 12.5), (-1.87182998657227, 11.25), (-1.25, 10.0), (-1.25, 8.75), (-1.25, 8.75),
                                      (-1.25, 7.5),
                                      (-1.25, 7.5), (0.0, 6.25), (-1.25, 7.5)))
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

    # Partitioning for meshing

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    f1, e1, d1 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f1[1], sketchUpEdge=e1[1],
                              sketchPlaneSide=SIDE1, origin=(0.0, 1e-06, 0.0))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                sheetSize=258.34, gridSpacing=6.45, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.rectangle(point1=(0.0, 0.0), point2=(-30.0, -10.0))
    s.Line(point1=(-30.0, -10.0), point2=(-100.0, -81.76385176))
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#2 ]',), )
    e, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e[1], faces=pickedFaces, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
    e1, d1 = p.edges, p.datums
    pickedEdges = (e1[1], e1[4])
    p.PartitionCellByExtrudeEdge(line=e1[9], cells=pickedCells, edges=pickedEdges,
                                 sense=REVERSE)

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
    e, d2 = p.edges, p.datums
    pickedEdges = (e[11],)
    p.PartitionCellByExtrudeEdge(line=e[16], cells=pickedCells, edges=pickedEdges,
                                 sense=REVERSE)

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#8 ]',), )
    v = p.vertices
    verts = v.getSequenceFromMask(mask=('[#8 ]',), )
    pickedEntities = (verts, edges,)
    p.ignoreEntity(entities=pickedEntities)

    # Seed edges for meshing
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#700 ]',), )
    p.seedEdgeBySize(edges=pickedEdges, size=1.0, deviationFactor=0.1,
                     constraint=FINER)
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    pickedEdges2 = e.getSequenceFromMask(mask=('[#80000 ]',), )
    p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges2, minSize=1.0,
                     maxSize=12.0, constraint=FINER)
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    pickedEdges1 = e.getSequenceFromMask(mask=('[#4000 ]',), )
    p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1, minSize=1.0,
                     maxSize=12.0, constraint=FINER)
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    pickedEdges2 = e.getSequenceFromMask(mask=('[#1000 ]',), )
    p.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges2, minSize=1.0,
                     maxSize=12.0, constraint=FINER)

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#40 ]',), )
    p.seedEdgeBySize(edges=pickedEdges, size=1.5, deviationFactor=0.1,
                     constraint=FINER)  # element sizd troughout the thickness

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#40800 ]',), )
    p.seedEdgeBySize(edges=pickedEdges, size=4, deviationFactor=0.05,
                     constraint=FINER)

    # Mesh
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    p.generateMesh()

    # Section assignment

    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#7 ]',), )
    p.Set(cells=cells, name='Set-Identer')
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-Identer',
                                                  material='Mars300', thickness=None)
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    region = p.sets['Set-Identer']
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    p.SectionAssignment(region=region, sectionName='Section-Identer', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)


def BottomSupport():
    # Geometry Creation
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
    # parameter added to sketch
    p = mdb.models['Model-1'].parts['Support_bottom']
    s1 = p.features['Solid extrude-1'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s1)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2,
                                  upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
    s = mdb.models['Model-1'].sketches['__edit__']
    s.Parameter(name='radius', path='dimensions[1]', expression="{:.9f}".format(R_b))  # <- Bend Radius
    s.Parameter(name='angle', path='dimensions[2]', expression="{:.9f}".format(alpha),  # <- Bend Angle
                previousParameter='radius')
    s.Parameter(name='offset', path='dimensions[0]', expression="{:.9f}".format(t_s),
                # <- Offset from 0 (sheet Thickness)
                previousParameter='angle')
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Support_bottom']
    p.features['Solid extrude-1'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['Support_bottom']
    p.regenerate()

    p = mdb.models['Model-1'].parts['Support_bottom']
    e = p.edges
    p.Round(radius=10.0, edgeList=(e[9], e[11]))

    p = mdb.models['Model-1'].parts['Support_bottom']
    f = p.faces
    p.RemoveFaces(faceList=f[3:5] + f[7:8], deleteCells=False)

    # Seeding and meshing
    p = mdb.models['Model-1'].parts['Support_bottom']
    p.seedPart(size=1.5, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Support_bottom']
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#1f ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
    p = mdb.models['Model-1'].parts['Support_bottom']
    p.generateMesh()


def TopSupport():
    # Geometry creation
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, 3.75), angle=90.0)
    s.VerticalConstraint(entity=g[2], addUndoState=False)
    s.ConstructionLine(point1=(2.5, 0.0), angle=0.0)
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.FixedConstraint(entity=g[3])
    s.FixedConstraint(entity=g[2])
    s.CircleByCenterPerimeter(center=(-5.0, -12.5), point1=(-15.0, -3.75))
    s.Line(point1=(-17.5, -7.99306090567006), point2=(-35.0, -43.75))
    s.CoincidentConstraint(entity1=v[2], entity2=g[4], addUndoState=False)
    s.dragEntity(entity=v[0], points=((-5.0, -12.5), (-5.0, -12.5), (-3.75,
                                                                     -13.75), (-2.5, -15.0), (-1.25, -15.0),
                                      (-1.25, -16.25), (0.0,
                                                        -16.25)))
    s.dragEntity(entity=v[2], points=((-17.5, -7.99306090567006), (-17.5, -7.5), (
        -15.0, -8.75), (-13.75, -10.0), (-12.5, -10.0), (-11.25, -11.25), (
                                          -11.25, -11.25)))
    s.dragEntity(entity=v[0], points=((0.0, -16.25), (0.0, -16.25), (-3.75,
                                                                     -16.25)))
    s.CoincidentConstraint(entity1=v[0], entity2=g[2])

    s.CoincidentConstraint(entity1=v[2], entity2=v[1])
    s.TangentConstraint(entity1=g[5], entity2=g[4])

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

    s = mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='Outer_Radius', path='dimensions[2]', expression="{:.9f}".format(R_b + t_s))
    s.Parameter(name='Bending_angle', path='dimensions[0]', expression="{:.9f}".format(alpha),
                previousParameter='Outer_Radius')
    s.Parameter(name='Vertical_Size', path='dimensions[1]', expression='45',
                previousParameter='Bending_angle')
    s.Parameter(name='vertical_local_offset', path='dimensions[3]', expression='0.0',
                previousParameter='Vertical_Size')
    p = mdb.models['Model-1'].Part(name='Support_top', dimensionality=THREE_D,
                                   type=DISCRETE_RIGID_SURFACE)
    p = mdb.models['Model-1'].parts['Support_top']
    p.BaseShellExtrude(sketch=s, depth=30.0)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Support_top']
    del mdb.models['Model-1'].sketches['__profile__']

    # Seeding and Mesh generation
    p = mdb.models['Model-1'].parts['Support_top']
    p.seedPart(size=1.5, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Support_top']
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#3 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD)
    p = mdb.models['Model-1'].parts['Support_top']
    p.generateMesh()


def Sheet():
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
    s1.ObliqueDimension(vertex1=v[19], vertex2=v[20], textPoint=(-113.005310058594, 1.93950271606445), value=1.4)
    s1.TangentConstraint(entity1=g[12], entity2=g[13])
    s1.TangentConstraint(entity1=g[14], entity2=g[13])
    s1.TangentConstraint(entity1=g[15], entity2=g[14])
    s1.TangentConstraint(entity1=g[11], entity2=g[7])
    s1.DistanceDimension(entity1=v[18], entity2=g[3], textPoint=(38.2222633361816, 26.1611824035645),
                         value=(60.0 + t_s))
    s1.DistanceDimension(entity1=v[4], entity2=g[2], textPoint=(-48.0425910949707, -13.5062065124512), value=100.0)
    s1.AngularDimension(line1=g[7], line2=g[2], textPoint=(-12.4803428649902, -7.53854751586914), value=20.1234)

    s1.RadialDimension(curve=g[11], textPoint=(1.48351752758026, 51.7214965820312),
                       radius=11.1234)

    d[3].setValues(textPoint=(-7.5, 22.5))
    d[3].setValues(textPoint=(-7.5, 22.5))
    d[4].setValues(textPoint=(-15.0, 65.0))
    d[4].setValues(textPoint=(-15.0, 65.0))

    s = mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='sheet_bending_radius', path='dimensions[4]',
                expression="{:.9f}".format(R_b))
    s.Parameter(name='sheet_bending_angle', path='dimensions[3]',
                expression="{:.9f}".format(alpha), previousParameter='sheet_bending_radius')
    s = mdb.models['Model-1'].sketches['__profile__']
    s.Parameter(name='sheet_thickness', path='dimensions[0]', expression="{:.9f}".format(t_s),
                previousParameter='sheet_bending_angle')
    p = mdb.models['Model-1'].Part(name='Sheet', dimensionality=THREE_D,
                                   type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Sheet']
    p.BaseSolidExtrude(sketch=s1, depth=100.0)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Sheet']
    del mdb.models['Model-1'].sketches['__profile__']

    if sheetVersion == 1:
        # Still Partitioning as it gives a better mesh
        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
        v1, e1, d1 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v1[7], point2=v1[13],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e1[8], rule=MIDDLE))

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#2 ]',), )
        v, e, d = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v[11], point2=v[6], cells=pickedCells,
                                          point3=p.InterestingPoint(edge=e[18], rule=MIDDLE))

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#4 ]',), )
        v1, e1, d1 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v1[14], point2=v1[17],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e1[23], rule=MIDDLE))

        # Seeding and meshing
        p = mdb.models['Model-1'].parts['Sheet']
        p.seedPart(size=0.7, deviationFactor=0.1, minSizeFactor=0.1)
        p = mdb.models['Model-1'].parts['Sheet']
        p.generateMesh()

        # Generate set with entire sheet
        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#f ]',), )
        p.Set(cells=cells, name='Set-Sheet')

    if sheetVersion == 2:
        # Partitioning
        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
        v1, e1, d1 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v1[7], point2=v1[13],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e1[8], rule=MIDDLE))

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#2 ]',), )
        v, e, d = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v[11], point2=v[6], cells=pickedCells,
                                          point3=p.InterestingPoint(edge=e[18], rule=MIDDLE))

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#4 ]',), )
        v1, e1, d1 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v1[14], point2=v1[17],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e1[23], rule=MIDDLE))

        # Seeding trough thickness

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#0 #1 ]',), )
        p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#20000 ]',), )
        p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#1000 ]',), )
        p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#8 ]',), )
        p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#100 ]',), )
        p.seedEdgeByNumber(edges=pickedEdges, number=4, constraint=FINER)

        # Seed tough width
        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#a0000000 ]',), )
        p.seedEdgeBySize(edges=pickedEdges, size=0.35, deviationFactor=0.1,
                         constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#300000 ]',), )
        p.seedEdgeBySize(edges=pickedEdges, size=0.35, deviationFactor=0.1,
                         constraint=FINER)

        # just above lower radius
        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#c00 ]',), )
        p.seedEdgeBySize(edges=pickedEdges, size=1.4, deviationFactor=0.01,
                         minSizeFactor=0.1, constraint=FINER)

        # Seed trough length
        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges = e.getSequenceFromMask(mask=('[#41400000 #2 ]',), )
        p.seedEdgeBySize(edges=pickedEdges, size=0.35, deviationFactor=0.1,
                         constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        e = p.edges
        pickedEdges1 = e.getSequenceFromMask(mask=('[#0 #4 ]',), )
        pickedEdges2 = e.getSequenceFromMask(mask=('[#10050000 ]',), )
        p.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges1,
                         end2Edges=pickedEdges2, minSize=0.35, maxSize=2.8, constraint=FINER)

        p = mdb.models['Model-1'].parts['Sheet']
        p.seedPart(size=2.8, deviationFactor=0.01, minSizeFactor=0.1)
        p = mdb.models['Model-1'].parts['Sheet']

        # mesh controls for middle region

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedRegions = c.getSequenceFromMask(mask=('[#2 ]',), )
        p.setMeshControls(regions=pickedRegions, technique=SWEEP,
                          algorithm=ADVANCING_FRONT)

        # Generate mesh
        p.generateMesh()

        # Generate set with entire sheet
        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#f ]',), )
        p.Set(cells=cells, name='Set-Sheet')

    # Elliptical Hole
    if sheetVersion == 3:
        Major_R = 15  # Major radius
        Minor_R = 15  # Minor radius
        # Vertical_d = 10 #Vertical distance of the point of the hole
        Vertical_d = Major_R  # This makes Major_R always vertical and Minor_R horizontal

        Horizontal_d = 25  # Horizontal distance of the hole

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
        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Horizontal_Distance', path='dimensions[0]',
                    expression="{:.9f}".format(Horizontal_d))
        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Major_Radius', path='dimensions[1]', expression="{:.9f}".format(Major_R),
                    previousParameter='Horizontal_Distance')
        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Minor_Radius', path='dimensions[2]', expression="{:.9f}".format(Minor_R),
                    previousParameter='Major_Radius')
        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Vertical_Point_from_middle', path='dimensions[3]',
                    expression="{:.9f}".format(Vertical_d), previousParameter='Minor_Radius')
        p = mdb.models['Model-1'].parts['Sheet']
        f1, e = p.faces, p.edges
        p.CutExtrude(sketchPlane=f1[2], sketchUpEdge=e[7], sketchPlaneSide=SIDE1,
                     sketchOrientation=RIGHT, sketch=s1, flipExtrudeDirection=OFF)
        s1.unsetPrimaryObject()
        del mdb.models['Model-1'].sketches['__profile__']

        # Partitioning for meshing
        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
        v1, e, d1 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v1[9], point2=v1[15],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e[10], rule=MIDDLE))

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#2 ]',), )
        v2, e1, d2 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v2[11], point2=v2[6],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e1[20], rule=MIDDLE))

        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
        v1, e, d1 = p.vertices, p.edges, p.datums
        p.PartitionCellByPlaneThreePoints(point1=v1[14], point2=v1[17],
                                          cells=pickedCells, point3=p.InterestingPoint(edge=e[25], rule=MIDDLE))

        # Seeding uniformly
        p = mdb.models['Model-1'].parts['Sheet']
        p.seedPart(size=0.7, deviationFactor=0.1, minSizeFactor=0.1)

        # Meshing
        p = mdb.models['Model-1'].parts['Sheet']
        p.generateMesh()

        # Generate set with entire sheet
        p = mdb.models['Model-1'].parts['Sheet']
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#f ]',), )
        p.Set(cells=cells, name='Set-Sheet')

    # Rectangular Hole
    if sheetVersion == 4:
        Vertical_l = 10
        Horizontal_l = 10
        Hole_R = 2

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

        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Horizontal_Distance', path='dimensions[0]',
                    expression="{:.9f}".format(Horizontal_d))
        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Vertical_Length', path='dimensions[2]', expression="{:.9f}".format(Vertical_l),
                    previousParameter='Horizontal_Distance')
        s = mdb.models['Model-1'].sketches['__profile__']
        s.Parameter(name='Horizontal_Length', path='dimensions[3]',
                    expression="{:.9f}".format(Horizontal_l), previousParameter='Vertical_Length')
        s = mdb.models['Model-1'].sketches['__profile__']
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

    # Section assgnemnet using set-sheet
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-Sheet', material='DP590', thickness=None)
    p = mdb.models['Model-1'].parts['Sheet']
    region = p.sets['Set-Sheet']
    p = mdb.models['Model-1'].parts['Sheet']
    p.SectionAssignment(region=region, sectionName='Section-Sheet', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)


def Assembly():
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Sheet']
    a1.Instance(name='Sheet-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Support_bottom']
    a1.Instance(name='Support_bottom-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['indenter_cylindrical']
    a1.Instance(name='indenter_cylindrical-1', part=p, dependent=ON)

    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('Sheet-1',), vector=(0.0, -(60.0 + t_s), 0.0))

    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('Support_bottom-1',), vector=(0.0, 0.0, 50.0))

    a1 = mdb.models['Model-1'].rootAssembly
    a1.rotate(instanceList=('indenter_cylindrical-1',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(0.0, 1.0, 0.0), angle=-90.0)

    a = mdb.models['Model-1'].rootAssembly
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Support_top']
    a.Instance(name='Support_top-1', part=p, dependent=ON)

    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Support_top-1',), vector=(0.0, 0.0, 0.0))

    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Support_top-1',), vector=(0.0, 0.0, 70.0))

    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)


Fake_material_import()
Cyl_Indenter()
Sheet()
BottomSupport()
TopSupport()
Assembly()
