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
    def __init__(self, image, screen, center, scale=(1,1)):
        Sprite.__init__(self, image, screen, center, scale)
        self.shakeClock = pygame.time.Clock()
        self.shake = 0
        self.direction = 1
        self.rising = False

    def update(self):
        self.shake += self.shakeClock.tick() * self.direction
        if self.shake > 1000 and not self.rising:
            self.rising = True
            self.direction *= -1
        elif self.shake < 0 and self.rising:
            self.rising = False
            self.direction *= -1

    def draw(self):
        scale = (self.shake / 1000.0) * 0.05 + 0.95
        copy = self.image.copy()
        copy = pygame.transform.smoothscale(copy, (int(copy.get_width() * scale), int(copy.get_height() * scale)))
        pos = (self.center[0]-copy.get_width()/2, self.center[1]-copy.get_height()/2)
        self.screen.blit(copy,pos)

class HitCircle:
    def __init__(self, image, screen):
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

    def draw(self):
        if self.state == "FADEDIN":
            self.screen.blit(self.image, self.pos)
            scale = 4 - 3.02 * self.approach/1000.0
            transform = (int(self.image.get_width()*scale), int(self.image.get_height()*scale))
            approachCircle = pygame.transform.smoothscale(self.approachCircle, (transform[0], transform[1]))
            pos = (self.center[0]-approachCircle.get_width()/2, self.center[1]-approachCircle.get_height()/2)
            self.screen.blit(approachCircle, pos)
        elif self.state == "FADINGOUT":
            scale = 1 + (self.approach - 1000.0)/500.0
            transform = (int(self.image.get_width()*scale), int(self.image.get_height()*scale))
            hitCircle = pygame.transform.smoothscale(self.imageBig, (transform[0], transform[1])).convert_alpha()
            pos = (self.center[0]-hitCircle.get_width()/2, self.center[1]-hitCircle.get_height()/2)
            alpha = int(255 - (self.approach - 1000.0)/500.0 * 255)
            if alpha < 0:
                alpha = 0
            hitCircleCopy = hitCircle.copy()
            hitCircleCopy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            self.screen.blit(hitCircleCopy, pos)

class Display:
    def __init__(self):
        self.running = True
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        center = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.background = Sprite(pygame.image.load('background.png'), self.screen, center)
        scale = self.screen.get_height()/1080.0 * 0.85
        self.logo = Logo(pygame.image.load('logo.png'), self.screen, center, (scale, scale))

        self.hitcircles = []
        for i in range(32):
            self.hitcircles.append(HitCircle(pygame.image.load('hitcircle'+str(i%8)+'.png'),self.screen))
        
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

        for i in range(len(self.hitcircles)):
            self.hitcircles[i].update()

        self.logo.update()

    def draw(self):
        self.screen.fill((0,0,0))
        self.background.draw()

        for i in range(len(self.hitcircles)):
            self.hitcircles[i].draw()

        self.logo.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.update()
            self.draw()

display = Display()
display.run()
