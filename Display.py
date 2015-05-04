import pygame
import random

class Sprite:
    def __init__(self, image, screen, center, scale=(1,1)):
        self.image = image
        self.screen = screen
        self.image = pygame.transform.smoothscale(self.image, (int(self.image.get_width() * scale[0]), int(self.image.get_height() * scale[1])))
        self.center = center
        self.scale = scale
        self.pos = (center[0] - self.image.get_width()/2, center[1] - self.image.get_height()/2)

    def draw(self):
        self.screen.blit(self.image, self.pos)

class Logo(Sprite):
    def __init__(self, image, screen, center, scale=(1,1), display=None):
        Sprite.__init__(self, image, screen, center, scale)
        self.shakeClock = pygame.time.Clock()
        self.shake = 0
        self.direction = 1
        self.rising = False
        self.display = display
        self.bgrect = self.image.get_rect()

    def update(self):
        self.shake += self.shakeClock.tick() * self.direction
        if self.shake > 1000 and not self.rising:
            self.rising = True
            self.direction *= -1
        elif self.shake < 0 and self.rising:
            self.rising = False
            self.direction *= -1

        scale = (self.shake / 1000.0) * 0.05 + 0.95
        self.copy = self.image.copy()
        self.copy = pygame.transform.smoothscale(self.copy, (int(self.copy.get_width() * scale), int(self.copy.get_height() * scale)))
        pos = (self.center[0]-self.copy.get_width()/2, self.center[1]-self.copy.get_height()/2)
        self.bgrect = (pos[0], pos[1], self.copy.get_width(), self.copy.get_height())

    def draw(self):
        self.screen.blit(self.copy,(self.bgrect[0], self.bgrect[1]))

class HitCircle:
    def __init__(self, image, screen, display):
        self.display = display
        self.image = image
        self.imageBig = self.image.copy()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.approachCircle = pygame.image.load('approachcircle.png')
        self.screen = screen
        self.approachClock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.center = (random.random() * self.screen.get_width(), random.random() * self.screen.get_height())
        self.pos = (self.center[0]-75/2, self.center[1]-75/2)
        self.approach = 0
        self.wait = 0
        self.waitLimit = random.randint(0, 5000)
        self.waitClock = pygame.time.Clock()
        self.state = "WAIT"
        self.bgrect = pygame.Rect(0,0,0,0)

    def update(self):
        if self.state == "WAIT":
            self.wait += self.waitClock.tick()
            if self.wait > self.waitLimit:
                self.approachClock.tick()
                self.state = "FADEDIN"
        else:
            self.approach += self.approachClock.tick()
            if self.approach > 1600:
                self.reset()
            elif self.approach > 1000:
                self.state = "FADINGOUT"

        if self.state == "FADEDIN":
            scale = 4 - 3.02 * self.approach/1000.0
            transform = (int(self.image.get_width()*scale), int(self.image.get_height()*scale))
            self.approachCircleCopy = pygame.transform.smoothscale(self.approachCircle, (transform[0], transform[1]))
            pos = (self.center[0]-self.approachCircleCopy.get_width()/2, self.center[1]-self.approachCircleCopy.get_height()/2)
            self.bgrect = (pos[0], pos[1], self.approachCircleCopy.get_width(), self.approachCircleCopy.get_height())

        elif self.state == "FADINGOUT":
            scale = 1 + (self.approach - 1000.0)/500.0
            transform = (int(self.image.get_width()*scale), int(self.image.get_height()*scale))
            hitCircle = pygame.transform.smoothscale(self.imageBig, (transform[0], transform[1]))
            pos = (self.center[0]-hitCircle.get_width()/2, self.center[1]-hitCircle.get_height()/2)
            alpha = int(255 - (self.approach - 1000.0)/500.0 * 255)
            if alpha < 0:
                alpha = 0
            self.hitCircleCopy = hitCircle.copy()
            self.hitCircleCopy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            self.bgrect = (pos[0], pos[1], self.hitCircleCopy.get_width(), self.hitCircleCopy.get_height())

    def draw(self):
        if self.state == "FADEDIN":
            self.screen.blit(self.approachCircleCopy, (self.bgrect[0], self.bgrect[1]))
            self.screen.blit(self.image, self.pos)
        elif self.state == "FADINGOUT":
            self.screen.blit(self.hitCircleCopy, (self.bgrect[0], self.bgrect[1]))

class Display:
    def __init__(self):
        self.running = True
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        center = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.background = pygame.image.load('background.png')
        scale = self.screen.get_height()/1080.0 * 0.85
        self.logo = Logo(pygame.image.load('logo.png'), self.screen, center, (scale, scale), self)

        self.frameClock = pygame.time.Clock()
        self.time = 1000

        self.hitcircles = []
        for i in range(8):
            self.hitcircles.append(HitCircle(pygame.image.load('hitcircle'+str(i%8)+'.png'),self.screen, self))

        self.screen.blit(self.background, (0,0))
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.running = False
                elif event.key==pygame.K_F4:
                    if pygame.get.get_pressed()[K_RALT] or pygame.key.get_pressed()[K_LALT]:
                        self.running = False

        self.time += self.frameClock.tick()
        print('update1',self.time)

        for hitcircle in self.hitcircles:
            hitcircle.update()

        self.time += self.frameClock.tick()
        print('update2',self.time)

        self.logo.update()

        self.time += self.frameClock.tick()
        print('update3',self.time)

    def draw(self):
        for hitcircle in self.hitcircles:
            rect = (hitcircle.bgrect[0]-8, hitcircle.bgrect[1]-8, hitcircle.bgrect[2]+16, hitcircle.bgrect[3]+16)
            self.screen.blit(self.background, rect, rect)

        self.time += self.frameClock.tick()
        print('draw1',self.time)

        self.screen.blit(self.background, self.logo.bgrect, self.logo.bgrect)

        self.time += self.frameClock.tick()
        print('draw2',self.time)

        for hitcircle in self.hitcircles:
            hitcircle.draw()

        self.time += self.frameClock.tick()
        print('draw3',self.time)

        self.logo.draw()

        self.time += self.frameClock.tick()
        print('draw4',self.time)

        pygame.display.update()

        self.time += self.frameClock.tick()
        print('draw5',self.time)
        print

    def run(self):
        while self.running:
            self.time = 0
            self.update()
            self.draw()

display = Display()
display.run()
