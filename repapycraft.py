# coding: utf-8

from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase.ShowBase import ShowBase
#from noise import snoise2
import os
import random
from Block import *

loadPrcFile('config/general.prc')

if __debug__:
    loadPrcFile('config/dev.prc')

#Moitié de la taille du monde
WORLD_SIZE = 25
HILL_PROB = 5
TREE_PROB = 15
HILL_MAX_SIZE = 10

base = ShowBase()

world = {}

def addBlock(blockType,x,y,z):
    try:
        world[(x,y,z)].cleanup()
    except:
        pass
    block = Block(blockType, x, y, z)
    world[(x,y,z)] = block
    return

#Génération du sol
n = WORLD_SIZE
z = 0
for x in range(0, n + 1, 1):
    for y in range(0, n + 1, 1):
        addBlock(GRASS, x, y, z)
        addBlock(DIRT, x, y, z-1)
        addBlock(STONE, x, y, z-2)
        addBlock(STONE, x, y, z-3)

#Génération de collines
o = WORLD_SIZE - HILL_MAX_SIZE
for _ in range(HILL_PROB):
    #Position de la colline
    xHill = random.randint(0,o)
    yHill = random.randint(0,o)
    zHill = 0
    #Hauteur et largeur
    hHill = random.randint(1,HILL_MAX_SIZE)
    sHill = random.randint(2,6)
    d = 1
    for z in range(zHill, zHill + hHill):
        for x in range(xHill - sHill, xHill + sHill + 1):
            for y in range(yHill - sHill, yHill + sHill + 1):
                if (x - xHill) ** 2 + (y - yHill) ** 2 > (sHill + 1) ** 2:
                    continue
                if (x - 0) ** 2 + (y - 0) ** 2 < 5 ** 2:
                    continue
                addBlock(GRASS, x, y, z)
            #Décremente petit à petit la largeur afin de créer une forme pyramidale
            sHill -= d


#for x in xrange(0, 500):
    #for y in xrange(0, 500):
        #amplitude = random.randrange(0.0,5.0)
        #blockType = DIRT
        #z = max((int(snoise2(x / freq, y / freq, 5) * amplitude)+8), 0)
        #z = random.randint(1, 10)
        #addBlock(blockType, x, y, 0)

#Gestion de la lumiere
alight = AmbientLight('alight')
alight.setColor(VBase4(0.6, 0.6, 0.6, 1))
alnp = render.attachNewNode(alight)
render.setLight(alnp)
slight = Spotlight('slight')
slight.setColor(VBase4(1, 1, 1, 1))
lens = PerspectiveLens()
slight.setLens(lens)
slnp = render.attachNewNode(slight)
slnp.setPos(8, -9, 128)
slnp.setHpr(0,270,0)
render.setLight(slnp)

traverser = CollisionTraverser()
handler = CollisionHandlerQueue()
pickerNode = CollisionNode('mouseRay')
pickerNP = camera.attachNewNode(pickerNode)
pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
pickerRay = CollisionRay()
pickerNode.addSolid(pickerRay)
traverser.addCollider(pickerNP, handler)

#Brouillard
fog = Fog("fog")
fog.setColor(0.5294, 0.8078, 0.9215)
fog.setExpDensity(0.015)
render.setFog(fog)
base.camLens.setFar(256)

base.run()
