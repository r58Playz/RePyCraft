import sys
import math
import random
import time

from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

#Moitié de la taille du monde
from scipy.linalg._expm_frechet import vec

WORLD_SIZE = 100
HILL_PROB = 50
HILL_MAX_SIZE = 30

class Model:
    def get_tex(self,file):
        tex = pyglet.image.load(file).texture
        #Gestion minification et magnification
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def __init__(self):
        # Contient pour chaque position du monde la texture du bloc correspondant
        self.world = {}

        self.textures = {}
        #Stone
        self.textures['stone'] = {}
        self.textures['stone']['top'] = self.get_tex('resources/textures/blocks/stone.png')
        self.textures['stone']['bottom'] = self.get_tex('resources/textures/blocks/stone.png')
        self.textures['stone']['side'] = self.get_tex('resources/textures/blocks/stone.png')
        #Grass
        self.textures['grass'] = {}
        self.textures['grass']['top'] = self.get_tex('resources/textures/blocks/_grass_top.png')
        self.textures['grass']['bottom'] = self.get_tex('resources/textures/blocks/dirt.png')
        self.textures['grass']['side'] = self.get_tex('resources/textures/blocks/grass_side.png')
        #Dirt
        self.textures['dirt'] = {}
        self.textures['dirt']['top'] = self.get_tex('resources/textures/blocks/dirt.png')
        self.textures['dirt']['bottom'] = self.get_tex('resources/textures/blocks/dirt.png')
        self.textures['dirt']['side'] = self.get_tex('resources/textures/blocks/dirt.png')
        #Log Acacia
        self.textures['logAcacia'] = {}
        self.textures['logAcacia']['top'] = self.get_tex('resources/textures/blocks/log_acacia.png')
        self.textures['logAcacia']['bottom'] = self.get_tex('resources/textures/blocks/log_acacia.png')
        self.textures['logAcacia']['side'] = self.get_tex('resources/textures/blocks/log_acacia.png')
        #Log Big Oak
        self.textures['logBigOak'] = {}
        self.textures['logBigOak']['top'] = self.get_tex('resources/textures/blocks/log_big_oak.png')
        self.textures['logBigOak']['bottom'] = self.get_tex('resources/textures/blocks/log_big_oak.png')
        self.textures['logBigOak']['side'] = self.get_tex('resources/textures/blocks/log_big_oak.png')
        #Leaves Big Oak
        self.textures['leavesBigOak'] = {}
        self.textures['leavesBigOak']['top'] = self.get_tex('resources/textures/blocks/leaves_big_oak.png')
        self.textures['leavesBigOak']['bottom'] = self.get_tex('resources/textures/blocks/leaves_big_oak.png')
        self.textures['leavesBigOak']['side'] = self.get_tex('resources/textures/blocks/leaves_big_oak.png')

        self.batch = pyglet.graphics.Batch()

        #Génération du sol
        n = WORLD_SIZE
        y = 0
        for x in range(-n, n + 1, 1):
            for z in range(-n, n + 1, 1):
                self.addBlock(x, y-2, z, 'grass')
                self.addBlock(x, y-3, z, 'dirt')
                self.addBlock(x, y-4, z, 'stone')
                self.addBlock(x, y-5, z, 'stone')

        #Génération de collines
        o = WORLD_SIZE - HILL_MAX_SIZE
        for _ in range(HILL_PROB):
            #Position de la colline
            xHill = random.randint(-o,o)
            zHill = random.randint(-o,o)
            yHill = -1
            #Hauteur et largeur
            hHill = random.randint(1,HILL_MAX_SIZE)
            sHill = random.randint(4,8)
            d = 1
            for y in range(yHill, yHill + hHill):
                for x in range(xHill - sHill, xHill + sHill + 1):
                    for z in range(zHill - sHill, zHill + sHill + 1):
                        if (x - xHill) ** 2 + (z - zHill) ** 2 > (sHill + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.addBlock(x, y, z, 'grass')
                #Décremente petit à petit la largeur afin de créer une forme pyramidale
                sHill -= d

        #Génération d'arbres
        self.addBlock(10, -1, 10, 'logBigOak')
        self.addBlock(10, 0, 10, 'logBigOak')
        self.addBlock(10, 1, 10, 'logBigOak')
        for y in range(2,6):
            self.addBlock(9, y, 9, 'leavesBigOak')
            self.addBlock(9, y, 10, 'leavesBigOak')
            self.addBlock(9, y, 11, 'leavesBigOak')
            self.addBlock(10, y, 9, 'leavesBigOak')
            self.addBlock(10, y, 10, 'leavesBigOak')
            self.addBlock(10, y, 11, 'leavesBigOak')
            self.addBlock(11, y, 9, 'leavesBigOak')
            self.addBlock(11, y, 10, 'leavesBigOak')
            self.addBlock(11, y, 11, 'leavesBigOak')

    def draw(self):
        self.batch.draw()

    def addBlock(self, x, y , z, type):
        X, Y, Z = x + 1, y + 1, z + 1
        texCoords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['bottom'], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['top'], ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), texCoords)
        self.batch.add(4, GL_QUADS, self.textures[type]['side'], ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), texCoords)

class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self,dx,dy):
        dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]-=dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0]<-90:
            self.rot[0] = -90

    def update(self,dt,keys):
        s = dt * 10
        rotY = -self.rot[1] / 180 * math.pi
        dx, dz = s * math.sin(rotY), s * math.cos(rotY)
        if keys[key.Z]: self.pos[0] += dx; self.pos[2] -= dz
        if keys[key.S]: self.pos[0] -= dx; self.pos[2] += dz
        if keys[key.Q]: self.pos[0] -= dz; self.pos[2] -= dx
        if keys[key.D]: self.pos[0] += dz; self.pos[2] += dx
        if keys[key.SPACE]: self.pos[1] += s
        if keys[key.LSHIFT]: self.pos[1] -= s

class Window(pyglet.window.Window):
    # Display FPS
    fpsDisplay = pyglet.clock.ClockDisplay()

    def push(self, pos, rot):
        glPushMatrix()
        glRotatef(-rot[0], 1, 0, 0)
        glRotatef(-rot[1], 0, 1, 0)
        glTranslatef(-pos[0], -pos[1], -pos[2],)
    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set3d(self):
        self.Projection()
        gluPerspective(70,self.width/self.height,0.05,1000)
        self.Model()

    #Gestion de l'exclusivité de la souris (ne sort pas de la fenêtre, plus de curseur (x et y meaningless))
    def setLock(self,state):
        self.lock = state
        self.set_exclusive_mouse(state)
    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_minimum_size(300,200)
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)
        #Permet de stocker l'état courant du clavier (accessible comme un dictionnaire)
        self.keys = key.KeyStateHandler()
        #Association du handler à la fenêtre afin de stocker ses evts clavier
        self.push_handlers(self.keys)

        pyglet.clock.schedule(self.update)

        #Model
        self.model = Model()
        #Player
        self.player = Player((0.5, 1.5, 1.5), (-30, 0))

    #Traitement des mouvements de la souris
    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    #Traitement des clics de la souris
    def on_mouse_press(self,x,y,button,modifiers):
        if button == mouse.LEFT:
            print("Clic gauche")

    #Traitement des evts clavier
    def on_key_press(self,symbol,modifiers):
        #ESCAPE permet de sortir la souris du mode exclusif
        if symbol == key.ESCAPE:
            self.close()
        #E permet de passer la souris en mode exclusif
        elif symbol == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self,dt):
        self.player.update(dt,self.keys)

    #Rafraichissement de l'affichage
    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos, self.player.rot)
        self.model.draw()
        # Display FPS
        self.fpsDisplay.draw()
        glPopMatrix()

if __name__ == '__main__':
    window = Window(width=854, height=480, caption='RePyCraft', resizable=True)
    glClearColor(0.5,0.7,1,1)
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()