import pygame
import random

class HitCircle:
    def __init__(self, image, screen, display):
        self.display = display
        self.image = image
        self.imageBig = self.image.copy()
        self.image = pygame.transform.smoothscale(self.image, (128, 128))
        self.approachCircle = pygame.image.load('approachcircle.png')
        self.screen = screen
        self.approachClock = pygame.time.Clock()
        self.reset()

    def reset(self):
        x = 0
        y = 0
        while True:
            x = (random.random() * (self.screen.get_width()-128))+64
            y = (random.random() * (self.screen.get_height()-128))+64
            if (x < 520 or x > 1400):
                break
            elif y < 100 or y > 980:
                break
            
        self.center = (x, y)
        self.pos = (self.center[0]-128/2, self.center[1]-128/2)
        self.approach = 0
        self.wait = 0
        self.waitLimit = random.randint(100,1000)
        self.waitClock = pygame.time.Clock()
        self.state = "WAIT"
        self.bgrect = pygame.Rect(0,0,0,0)
        self.prevrect = self.bgrect.copy()

    def update(self):
        if self.state == "WAIT":
            self.wait += self.waitClock.tick()
            if self.wait > self.waitLimit:
                self.approachClock.tick()
                self.state = "FADINGIN"
        else:
            self.approach += self.approachClock.tick()
            if self.approach > 1500:
                self.state = "FINISHED"
            elif self.approach > 1000:
                self.state = "FADINGOUT"
            elif self.approach > 100:
                self.state = "FADEDIN"

        if self.state == "FADINGIN":
            self.prevrect = self.bgrect
            scale = 4 - 3.02 * self.approach/1000.0
            transform = (int(self.image.get_width()*scale), int(self.image.get_height()*scale))
            self.approachCircleCopy = pygame.transform.smoothscale(self.approachCircle, (transform[0], transform[1]))
            pos = (self.center[0]-self.approachCircleCopy.get_width()/2, self.center[1]-self.approachCircleCopy.get_height()/2)

            alpha = int(self.approach/100.0 * 255)
            if alpha < 0:
                alpha = 0
            self.hitCircleCopy = self.image.copy()
            self.hitCircleCopy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
            self.approachCircleCopy.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

            self.bgrect = (pos[0], pos[1], self.approachCircleCopy.get_width(), self.approachCircleCopy.get_height())            

        elif self.state == "FADEDIN":
            self.prevrect = self.bgrect
            scale = 4 - 3.02 * self.approach/1000.0
            transform = (int(self.image.get_width()*scale), int(self.image.get_height()*scale))
            self.approachCircleCopy = pygame.transform.smoothscale(self.approachCircle, (transform[0], transform[1]))
            pos = (self.center[0]-self.approachCircleCopy.get_width()/2, self.center[1]-self.approachCircleCopy.get_height()/2)
            self.bgrect = (pos[0], pos[1], self.approachCircleCopy.get_width(), self.approachCircleCopy.get_height())

        elif self.state == "FADINGOUT":
            self.prevrect = self.bgrect
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
        if self.state == "FADINGIN":
            self.screen.blit(self.approachCircleCopy, (self.bgrect[0], self.bgrect[1]))
            self.screen.blit(self.hitCircleCopy, self.pos)
        elif self.state == "FADEDIN":
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
        self.background = pygame.image.load('background.png')

        self.hitcircles = []
        for i in range(8):
            hitcircle = HitCircle(pygame.image.load('hitcircle'+str(i%8)+'.png'),self.screen, self)
            hitcircle.state = "FINISHED"
            self.hitcircles.append(hitcircle)

        self.hitcircles[1].state = "WAIT"

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

        for i in range(len(self.hitcircles)):
            if self.hitcircles[i].state == "FINISHED":
                if self.hitcircles[i-1].state != "FINISHED" and self.hitcircles[i-1].state != "WAIT":
                    self.hitcircles[i].reset()
            else:
                self.hitcircles[i].update()

    def draw(self):
        for hitcircle in self.hitcircles:
            self.screen.blit(self.background, hitcircle.prevrect, hitcircle.prevrect)

        for hitcircle in self.hitcircles:
            hitcircle.draw()

        pygame.display.update()

    def run(self):
        '''
        self.frameClock = pygame.time.Clock()
        self.low = 10000
        self.high = 0
        self.average = 0
        self.averageCounter = 0
        '''

        while self.running:
            self.time = 0
            self.update()
            self.draw()

            '''
            self.averageCounter += 1
            if self.averageCounter % 2 == 0 and self.average > 5000:
                self.time += self.frameClock.tick()
                print "Total Time:", self.time

                if self.time < self.low:
                    self.low = self.time
                print "Low:", self.low

                if self.time > self.high:
                    self.high = self.time
                print "High:", self.high

                self.average += self.time
                print "Average:", self.average / self.averageCounter
                print
            else:
                self.average += self.frameClock.tick()
            '''

display = Display()
display.run()
