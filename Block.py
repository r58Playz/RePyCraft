from direct.directnotify import DirectNotifyGlobal

AIR = 0
DIRT = 1
STONE = 2
GRASS = 3
WOOD = 4
LEAVES = 5
GLASS = 6

blockNames = ['air', 'dirt', 'stone', 'grass', 'wood', 'leaves', 'glass']
multiTexBlocks = [GRASS, WOOD]
transparentBlocks = [GLASS, LEAVES]

class Block:
    notify = DirectNotifyGlobal.directNotify.newCategory('block')

    def __init__(self, type, x, y, z):
        self.type = type
        if self.type == AIR:
            del self
            return

        self.x = x
        self.y = y
        self.z = z

        self.model = base.loader.loadModel("resources/models/block")
        self.model.reparentTo(base.render)
        self.model.setPos(x, y, z)
        self.model.setTag('blockTag', '1')
        self.model.find('**/SideW').setTag('westTag', '2')
        self.model.find('**/SideN').setTag('northTag', '3')
        self.model.find('**/SideE').setTag('eastTag', '4')
        self.model.find('**/SideS').setTag('southTag', '5')
        self.model.find('**/Top').setTag('topTag', '6')
        self.model.find('**/Bottom').setTag('botTag', '7')

        if type in transparentBlocks:
            self.model.setTransparency(1)

        if type in multiTexBlocks:
            topTexture = base.loader.loadTexture("resources/textures/%s_top.png" % blockNames[type])
            sideTexture = base.loader.loadTexture("resources/textures/%s_side.png" % blockNames[type])
            botTexture = base.loader.loadTexture("resources/textures/%s_bottom.png" % blockNames[type])
            textureStage = self.model.findTextureStage('*')
            self.model.find('**/Top').setTexture(textureStage, topTexture, 1)
            self.model.find('**/Side').setTexture(textureStage, sideTexture, 1)
            self.model.find('**/Bottom').setTexture(textureStage, botTexture, 1)
        else:
            texture = base.loader.loadTexture("resources/textures/%s.png" % blockNames[type].lower())
            textureStage = self.model.findTextureStage('*')
            self.model.setTexture(textureStage, texture, 1)

    def cleanup(self):
        self.model.removeNode()
        del self
