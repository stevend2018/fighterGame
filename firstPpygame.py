import pygame
pygame.init()

screenheight = 480
screenwidth = 500

clock = pygame.time.Clock()

win = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("first pygame")

walkRight = [pygame.image.load('resources/character/R1.png'),
    pygame.image.load('resources/character/R2.png'),
    pygame.image.load('resources/character/R3.png'),
    pygame.image.load('resources/character/R4.png'),
    pygame.image.load('resources/character/R5.png'),
    pygame.image.load('resources/character/R6.png'),
    pygame.image.load('resources/character/R7.png'),
    pygame.image.load('resources/character/R8.png'),
    pygame.image.load('resources/character/R9.png')]
walkLeft = [pygame.image.load('resources/character/L1.png'),
    pygame.image.load('resources/character/L2.png'),
    pygame.image.load('resources/character/L3.png'),
    pygame.image.load('resources/character/L4.png'),
    pygame.image.load('resources/character/L5.png'),
    pygame.image.load('resources/character/L6.png'),
    pygame.image.load('resources/character/L7.png'),
    pygame.image.load('resources/character/L8.png'),
    pygame.image.load('resources/character/L9.png')]
bg = pygame.image.load('resources/bg.jpg')
char = pygame.image.load('resources/character/standing.png')

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isjump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self,win):
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if not(self.standing):
                
                if self.left:
                    win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                    self.walkCount += 1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                    self.walkCount += 1
            else:

              if self.right:
                  win.blit(walkRight[0],(self.x,self.y))
              else:
                  win.blit(walkLeft[0],(self.x,self.y))

class enemy(object):
    def __init__ (self, x, y, width, height, end, numberOfImages, directoryName):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        i = 0
        #numberOfImages = 11 #add this as a parameter
        self.walkLeft = []
        self.walkRight = []
        #directoryName = 'enemy2' #also add this as a paramter
        while(i < numberOfImages):
            i = i + 1
            walkLeftElement = "resources/" + directoryName + "/L" + str(i) + ".png"
            walkRightElement = "resources/" + directoryName + "/R" + str(i) + ".png"
            self.walkLeft.append(pygame.image.load(walkLeftElement))
            self.walkRight.append(pygame.image.load(walkRightElement))

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >self.numberOfimages*3:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
    

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
            

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.facing = facing
        self.color = color
        self.vel = 8 * facing

    def draw(self, win):
      pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = player (300, 410, 64, 64)  
goblin = enemy (125, 410, 64, 64, 450, 11, 'enemy')      
run = True
bullets = []
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2),
                                      round(man.y + man.height //2), 6, (0,0,0), facing))


    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (490 - (man.width - man.vel)):
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        #man.left = False
       # man.right = False
        man.walkCount = 0
    if not(man.isjump):
        if keys[pygame.K_UP]:
            man.isjump =  True
           # man.left = False
           # man.right = False
            man.walkCount = 0
    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2) * 0.5 * neg
            man.jumpcount -= 1

        else:
            man.isjump = False
            man.jumpcount = 10

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2),
                                      round(man.y+man.height//2),6,(0,0,0),facing))


    #win.fill((0,0,0))
    #pygame.draw.rect(win,(50,100,105),(x,y,width,height))
    #pygame.display.update()
        
    redrawGameWindow()
    
pygame.quit()

