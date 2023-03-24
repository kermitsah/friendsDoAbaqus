from abaqus import *
from abaqusConstants import *
import numpy as np



class CubeSatModel:
    def __init__(self, modelName):
        self.modelName = modelName
        self.myModel = mdb.Model(name=self.modelName)

class panel:
    def __init__(self, partName, model,X,Y,screwSize,cirDis,rectDis,tabX,tabY):
        self.partName = partName
        self.mainModel=model.myModel
        self.myPart = self.mainModel.Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
        self.length=float(X)
        self.width=float(Y)
        self.screwSize=screwSize
        self.cirDis=cirDis
        self.rectDis=rectDis
        self.tabX=tabX
        self.tabY=tabY
            
    def create_panel(self):   
        self.mySketch = self.mainModel.ConstrainedSketch(name='SketchName', sheetSize=5)
        length=self.length
        width=self.width
        self.mySketch.rectangle(point1=(0.0, 0.0),point2=(length, width))   
        self.myPart.BaseShell(sketch=self.mySketch)
    
    def screwPartion(self):
        newSname=self.mainModel.ConstrainedSketch(gridSpacing=5.59, name='newSname',sheetSize=223.6, transform=self.myPart.MakeSketchTransform(sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
        X=self.length
        Y=self.width
        screwSize=self.screwSize
        cirDis=self.cirDis
        PC=.5+screwSize
        for i in range(len(cirDis[:])):
            circleX=cirDis[i,0]
            circleY=cirDis[i,1]
            newSname.CircleByCenterPerimeter(center=(cirDis[i,0],cirDis[i,1]), point1=(cirDis[i,0],cirDis[i,1]+screwSize)) 
            newSname.rectangle(point1=(circleX-PC, circleY-PC), point2=(circleX+PC, circleY+PC)) #Rectangle
            newSname.Line(point1=(circleX-PC,circleY-PC), point2=(circleX+PC, circleY+PC))  #Cross
            newSname.Line(point1=(circleX-PC,circleY+PC), point2=(circleX+PC, circleY-PC))  #Cross
            newSname.Line(point1=(circleX-PC,circleY+PC), point2=(circleX-PC, Y)) 
            newSname.Line(point1=(circleX+PC,circleY+PC), point2=(circleX+PC, Y)) 
            newSname.Line(point1=(circleX-PC,circleY-PC), point2=(circleX-PC, 0)) 
            newSname.Line(point1=(circleX+PC,circleY-PC), point2=(circleX+PC, 0)) 
            newSname.Line(point1=(circleX-PC,circleY+PC), point2=(0,circleY+PC)) 
            newSname.Line(point1=(circleX-PC,circleY-PC), point2=(0,circleY-PC)) 
            newSname.Line(point1=(circleX+PC,circleY+PC), point2=(X,circleY+PC)) 
            newSname.Line(point1=(circleX+PC,circleY-PC), point2=(X,circleY-PC))
        self.myPart.PartitionFaceBySketch(faces=self.myPart.faces[0], sketch=newSname,sketchUpEdge=self.myPart.edges[3])
    
    def tabPlacer(self):
        X=self.length
        Y=self.width
        e=self.myPart.edges.findAt((X,Y/2,0),)
        rectDis=self.rectDis
        tabX=self.tabX
        tabY=self.tabY
        tabFaces=self.myPart.faces.getByBoundingBox(xMin=0, yMin=0, zMin=0, xMax=X, yMax=Y, zMax=0)
        newSname2=self.mainModel.ConstrainedSketch(gridSpacing=5.59, name='newSname2',sheetSize=223.6, transform=self.myPart.MakeSketchTransform(sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1,sketchUpEdge=e, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
        for i in range(len(rectDis[:])):
            newSname2.rectangle(point1=(rectDis[i,0],rectDis[i,1]), point2=(rectDis[i,0]+tabX,rectDis[i,1]+tabY)) 
            newSname2.Line(point1=(rectDis[i,0],rectDis[i,1]), point2=(X,rectDis[i,1]))
            newSname2.Line(point1=(rectDis[i,0],rectDis[i,1]), point2=(rectDis[i,0],Y))
            newSname2.Line(point1=(rectDis[i,0],rectDis[i,1]), point2=(0,rectDis[i,1]))
            newSname2.Line(point1=(rectDis[i,0],rectDis[i,1]), point2=(rectDis[i,0],0))
            
            newSname2.Line(point1=(rectDis[i,0]+tabX,rectDis[i,1]+tabY), point2=(X,rectDis[i,1]+tabY))
            newSname2.Line(point1=(rectDis[i,0]+tabX,rectDis[i,1]+tabY), point2=(rectDis[i,0]+tabX,Y))
            newSname2.Line(point1=(rectDis[i,0]+tabX,rectDis[i,1]+tabY), point2=(0,rectDis[i,1]+tabY))
            newSname2.Line(point1=(rectDis[i,0]+tabX,rectDis[i,1]+tabY), point2=(rectDis[i,0]+tabX,0))
        self.myPart.PartitionFaceBySketch(faces=tabFaces, sketch=newSname2,sketchUpEdge=e)
        
    def tabCutter(self):
        X=self.length
        Y=self.width
        rectDis=self.rectDis
        tabX=self.tabX
        tabY=self.tabY
        e=self.myPart.edges.findAt((X,Y/2,0),)
        tabFaces=self.myPart.faces.getByBoundingBox(xMin=0, yMin=0, zMin=0, xMax=X, yMax=Y, zMax=0)
        newSname3=self.mainModel.ConstrainedSketch(gridSpacing=5.59, name='newSname3',sheetSize=223.6, transform=self.myPart.MakeSketchTransform(sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1,sketchUpEdge=e, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
        for i in range(len(rectDis[:])):
            newSname3.rectangle(point1=(rectDis[i,0],rectDis[i,1]), point2=(rectDis[i,0]+tabX,rectDis[i,1]+tabY))     
        self.myPart.CutExtrude(flipExtrudeDirection=OFF, sketch=newSname3,sketchOrientation=RIGHT, sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1,sketchUpEdge=e)
    
    def holeCutter(self,holeSize,holeX,holeY):
        X=self.length
        Y=self.width
        float(holeX)
        float(holeY)
        float(holeSize)
        e=self.myPart.edges.findAt((X,Y/2,0),)
        tabFaces=self.myPart.faces.getByBoundingBox(xMin=0, yMin=0, zMin=0, xMax=X, yMax=Y, zMax=0)
        newSname4=self.mainModel.ConstrainedSketch(gridSpacing=5.59, name='newSname4',sheetSize=223.6, transform=self.myPart.MakeSketchTransform(sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1,sketchUpEdge=e, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
        newSname4.CircleByCenterPerimeter((holeX,holeY), point1=(holeX,holeY+(holeSize/2)))    
        self.myPart.CutExtrude(flipExtrudeDirection=OFF, sketch=newSname4,sketchOrientation=RIGHT, sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1,sketchUpEdge=e)
    
        newSname5=self.mainModel.ConstrainedSketch(gridSpacing=5.59, name='newSname5',sheetSize=223.6, transform=self.myPart.MakeSketchTransform(sketchPlane=self.myPart.faces[0],sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
        PC=.5+holeSize
        circleX=holeX
        circleY=holeY
        newSname5.rectangle(point1=(circleX-PC, circleY-PC), point2=(circleX+PC, circleY+PC)) #Rectangle
        newSname5.Line(point1=(circleX-PC,circleY-PC), point2=(circleX+PC, circleY+PC))  #Cross
        newSname5.Line(point1=(circleX-PC,circleY+PC), point2=(circleX+PC, circleY-PC))  #Cross
        newSname5.Line(point1=(circleX-PC,circleY+PC), point2=(circleX-PC, Y)) 
        newSname5.Line(point1=(circleX+PC,circleY+PC), point2=(circleX+PC, Y)) 
        newSname5.Line(point1=(circleX-PC,circleY-PC), point2=(circleX-PC, 0)) 
        newSname5.Line(point1=(circleX+PC,circleY-PC), point2=(circleX+PC, 0)) 
        newSname5.Line(point1=(circleX-PC,circleY+PC), point2=(0,circleY+PC)) 
        newSname5.Line(point1=(circleX-PC,circleY-PC), point2=(0,circleY-PC)) 
        newSname5.Line(point1=(circleX+PC,circleY+PC), point2=(X,circleY+PC)) 
        newSname5.Line(point1=(circleX+PC,circleY-PC), point2=(X,circleY-PC))
        self.myPart.PartitionFaceBySketch(faces=tabFaces, sketch=newSname5,sketchUpEdge=e)

class tab:
    def __init__(self, model,X,Y,Z,screwSize):
        partName = 'Tab'
        self.mainModel=model.myModel
        self.myPart = self.mainModel.Part(dimensionality=THREE_D, name=partName,  type=DEFORMABLE_BODY)
        self.length=X
        self.width=Y
        self.height=Z
        self.screw=screwSize
            
    def create_tab(self):   
        self.tabS=self.mainModel.ConstrainedSketch(name='tabS', sheetSize=50.0)
        length=self.length
        width=self.width
        height=self.height
        screw=self.screw
        w2=float(width)/2
        h2=float(height)/2
        s2=float(screw)/2
        p=float(s2+h2)
        self.tabS.rectangle(point1=(0.0, 0.0), point2=(width,height))
        self.tabS.CircleByCenterPerimeter(center=(w2,h2), point1=(w2,p))
        self.myPart.BaseSolidExtrude(depth=length, sketch=self.tabS)

class assembler:
    def __init__(self,model):
        self.mainModel=model.myModel
        self.myAssembly=self.mainModel.rootAssembly
    def assemble(self,pX, pY, pZ, nX, nY, nZ, xL, yL, zL,tab):
        self.myAssembly.DatumCsysByDefault(CARTESIAN)
        
        self.myAssembly.Instance(dependent=ON, name='nZ', part=nZ.myPart)
        self.myAssembly.DatumCsysByDefault(CARTESIAN)
        self.myAssembly.Instance(dependent=ON, name='nZ', part=nZ.myPart)
        
        self.myAssembly.Instance(dependent=ON, name='pZ', part=pZ.myPart)
        self.myAssembly.translate(instanceList=('pZ', ), vector=(0, 0.0, zL))


        self.myAssembly.Instance(dependent=ON, name='nY', part=nY.myPart)
        self.myAssembly.rotate(angle=90.0, axisDirection=(10.0, 0.0, 0.0), axisPoint=(276.0, 0.0, 0.0), instanceList=('nY', ))
        self.myAssembly.translate(instanceList=('nY', ), vector=(226.3, 0.0, 0.0))
        self.myAssembly.rotate(angle=-90.0, axisDirection=(0.0,10.0, 0.0), axisPoint=(226.3, 2.5, 0.0), instanceList=('nY', ))

        self.myAssembly.Instance(dependent=ON, name='pY', part=pY.myPart)
        self.myAssembly.rotate(angle=90.0, axisDirection=(10.0, 0.0, 0.0), axisPoint=(276.0, 0.0, 0.0), instanceList=('pY', ))
        self.myAssembly.translate(instanceList=('pY', ), vector=(xL, yL, 0.0))
        self.myAssembly.rotate(angle=-90.0, axisDirection=(0.0,10.0, 0.0), axisPoint=(xL, 2.5, 0.0), instanceList=('pY', ))


        self.myAssembly.Instance(dependent=ON, name='nX', part=nX.myPart)
        self.myAssembly.rotate(angle=90.0, axisDirection=(0.0, -10.0, 0.0), axisPoint=(0.0, 131.3, 0.0), instanceList=('nX', ))

        self.myAssembly.Instance(dependent=ON, name='pX', part=pX.myPart)
        self.myAssembly.rotate(angle=90.0, axisDirection=(0.0, -10.0, 0.0), axisPoint=(0.0, 131.3, 0.0), instanceList=('pX', ))
        self.myAssembly.translate(instanceList=('pX', ), vector=(xL, 0, 0.0))
        #self.myAssembly.Instance(dependent=ON,name='Tab-1', part=tab.myPart)
        pXTabs=pX.rectDis
        l=len(pXTabs[:])+1
        for i in range(0,8):
            instanceName='Tab-{}'.format(i)
            self.myAssembly.Instance(dependent=ON,name=instanceName, part=tab.myPart)
            self.myAssembly.rotate(angle=-90.0, axisDirection=(10.0, 0.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=(instanceName, ))
            self.myAssembly.rotate(angle=-90.0, axisDirection=(0.0, 10.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=(instanceName, ))
            self.myAssembly.translate(instanceList=(instanceName, ), vector=(0.0, pXTabs[i,1], pXTabs[i,0]))

"Main Model"
MainModel=CubeSatModel('TACSI')
xL=226.3
yL=236.6
zL=343.0
screwSize=2.5

tabX=15.0
tabY=15.0
tabHeight=11.0

tab=tab(MainModel,15,15,11,5)
tab.create_tab()

"pX"

rectDisX=np.array([ [25.5,0],
                    [65.5,0],
                    [105.5,0],
                    [145.5,0],
                    [185.5,0],
                    [225.5,0],
                    [265.5,0],
                    [305.5,0],
                    [25.5,yL-tabY],
                    [65.5,yL-tabY],
                    [105.5,yL-tabY],
                    [145.5,yL-tabY],
                    [185.5,yL-tabY],
                    [225.5,yL-tabY],
                    [265.5,yL-tabY],
                    [305.5,yL-tabY],
                    [0,30],
                    [0,70],
                    [0,131.3],
                    [0,171.3],
                    [zL-tabX,30],
                    [zL-tabX,70],
                    [zL-tabX,131.3],
                    [zL-tabX,171.3] 
                    ])
pX=panel('pX', MainModel,zL,yL,screwSize,[0],rectDisX,tabX,tabY)
pX.create_panel()
pX.tabPlacer()
pX.tabCutter()

"pY"


cirDisY=np.array([ [33,tabHeight/2],
                  [73,tabHeight/2],
                  [113,tabHeight/2],
                  [153,tabHeight/2],
                  [193,tabHeight/2],
                  [233,tabHeight/2],
                  [273,tabHeight/2],
                  [313,tabHeight/2],
                  [33,xL-tabHeight/2],
                  [73,xL-tabHeight/2],
                  [113,xL-tabHeight/2],
                  [153,xL-tabHeight/2],
                  [193,xL-tabHeight/2],
                  [233,xL-tabHeight/2],
                  [273,xL-tabHeight/2],
                  [313,xL-tabHeight/2]
                  ])
rectDisY=np.array([[0,35],
                  [0,75],
                  [0,136.3],
                  [0,176.3],
                  [zL-tabX,35],
                  [zL-tabX,75],
                  [zL-tabX,136.3],
                  [zL-tabX,176.3]])
pY=panel('pY', MainModel,zL,xL,screwSize,cirDisY,rectDisY,tabX,tabY)
pY.create_panel()
pY.screwPartion()
pY.tabPlacer()
pY.tabCutter()

"pZ"


cirDisZ=np.array([ [42.5,5.5],
                  [82.5,5.5],
                  [143.8,5.5],
                  [183.8,5.5],
                  [5.5,37.5],
                  [5.5,77.5],
                  [5.5,178.8],
                  [5.5,138.8], 
                  [42.5,yL-tabHeight/2],
                  [82.5,yL-tabHeight/2],
                  [143.8,yL-tabHeight/2],
                  [183.8,yL-tabHeight/2],
                  [xL-tabHeight/2,37.5],
                  [xL-tabHeight/2,77.5],
                  [xL-tabHeight/2,138.8],
                  [xL-tabHeight/2,178.8]
                  ])
pZ=panel('pZ', MainModel,xL,yL,screwSize,cirDisZ,[0],tabX,tabY)
pZ.create_panel()
pZ.screwPartion()


"nX"

rectDisX=np.array([  [25.5,0],
                    [65.5,0],
                    [105.5,0],
                    [145.5,0],
                    [185.5,0],
                    [225.5,0],
                    [265.5,0],
                    [305.5,0],
                    [25.5,yL-tabY],
                    [65.5,yL-tabY],
                    [105.5,yL-tabY],
                    [145.5,yL-tabY],
                    [185.5,yL-tabY],
                    [225.5,yL-tabY],
                    [265.5,yL-tabY],
                    [305.5,yL-tabY],
                    [0,30],
                    [0,70],
                    [0,131.3],
                    [0,171.3],
                    [zL-tabX,30],
                    [zL-tabX,70],
                    [zL-tabX,131.3],
                    [zL-tabX,171.3] 
                    ])
nX=panel('nX', MainModel,zL,yL,screwSize,[0],rectDisX,tabX,tabY)
nX.create_panel()
nX.tabPlacer()
nX.tabCutter()

"nY"


cirDisY=np.array([ [33,tabHeight/2],
                  [73,tabHeight/2],
                  [113,tabHeight/2],
                  [153,tabHeight/2],
                  [193,tabHeight/2],
                  [233,tabHeight/2],
                  [273,tabHeight/2],
                  [313,tabHeight/2],
                  [33,xL-tabHeight/2],
                  [73,xL-tabHeight/2],
                  [113,xL-tabHeight/2],
                  [153,xL-tabHeight/2],
                  [193,xL-tabHeight/2],
                  [233,xL-tabHeight/2],
                  [273,xL-tabHeight/2],
                  [313,xL-tabHeight/2]
                  ])
rectDisY=np.array([[0,35],
                  [0,75],
                  [0,136.3],
                  [0,176.3],
                  [zL-tabX,35],
                  [zL-tabX,75],
                  [zL-tabX,136.3],
                  [zL-tabX,176.3]])
nY=panel('nY', MainModel,zL,xL,screwSize,cirDisY,rectDisY,tabX,tabY)
nY.create_panel()
nY.screwPartion()
nY.tabPlacer()
nY.tabCutter()

"nZ"


cirDisZ=np.array([ [42.5,5.5],
                  [82.5,5.5],
                  [143.8,5.5],
                  [183.8,5.5],
                  [5.5,37.5],
                  [5.5,77.5],
                  [5.5,178.8],
                  [5.5,138.8], 
                  [42.5,yL-tabHeight/2],
                  [82.5,yL-tabHeight/2],
                  [143.8,yL-tabHeight/2],
                  [183.8,yL-tabHeight/2],
                  [xL-tabHeight/2,37.5],
                  [xL-tabHeight/2,77.5],
                  [xL-tabHeight/2,138.8],
                  [xL-tabHeight/2,178.8]
                  ])
nZ=panel('nZ', MainModel,xL,yL,screwSize,cirDisZ,[0],tabX,tabY)
nZ.create_panel()
nZ.screwPartion()

assembly=assembler(MainModel)
assembly.assemble(pX, pY, pZ, nX, nY, nZ, xL, yL, zL,tab)


SeedSize=20

nX.myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1,size=SeedSize)
nX.myPart.generateMesh()
pX.myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1,size=SeedSize)
pX.myPart.generateMesh()

nY.myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1,size=SeedSize)
nY.myPart.generateMesh()
pY.myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1,size=SeedSize)
pY.myPart.generateMesh()

nZ.myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1,size=SeedSize)
nZ.myPart.generateMesh()
pZ.myPart.seedPart(deviationFactor=0.1, minSizeFactor=0.1,size=SeedSize)
pZ.myPart.generateMesh()

stepName='Gravity Step'
g=9800
MainModel.myModel.StaticStep(name=stepName, previous='Initial')
a=assembly.myAssembly
MainModel.myModel.Gravity(comp1=5*g, comp2=10*g, comp3=5*g, createStepName=stepName, distributionType=UNIFORM, field='', name='Load-1')