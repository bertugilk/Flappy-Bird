import pygame
import sys
import random
import time

pygame.init()

# colors rpg values:

black=(0,0,0)
chocalate=(210,105,30)
white=(255,255,255)
green=(0,128,0)
red=(255,0,0)
blue=(0,0,255)
aqua=(0,255,255)
yellow=(255,255,0)
purple=(255,0,255)
orange=(255,165,0)
lime=(0,255,0)
gold=(255,215,0)
salmon=(250,128,114)
deepPink=(255,0,127)
brown=(204,102,0)

size=(285,500)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("FLAPPY BIRD")
icon=pygame.image.load("Images/icon.ico")
pygame.display.set_icon(icon)

clock=pygame.time.Clock()

bg1 = pygame.image.load("Images/backgroundDay.png")
bg2 = pygame.image.load("Images/backgroundNight.png")
base = pygame.image.load("Images/base.png")
Bird = pygame.image.load("Images/redbird-midflap.png")

birdRect = Bird.get_rect(center=(50, 200))

greenPipe = pygame.image.load("Images/pipe-green.png")
pipeHeight=[200,250,300,350,400]

flySound=pygame.mixer.Sound("Musics/kanatCirp.wav")
collisionSound=pygame.mixer.Sound("Musics/carpisma.wav")
deathSound=pygame.mixer.Sound("Musics/öl.wav")
pointSound=pygame.mixer.Sound("Musics/puan.wav")

class Main():
    def __init__(self):
        self.score=0
        self.HighScore=0
        self.fps=0
    def write(self,message,color,x,y,size):
        self.message=message
        self.color=color
        self.x=x
        self.y=y
        self.size=size
        font=pygame.font.SysFont(None,size)
        text=font.render(message,True,color)
        screen.blit(text,[x,y])
    def intro(self):
        intro = pygame.image.load("Images/intro.png")
        bg = pygame.image.load("Images/backgroundDay.png")
        base = pygame.image.load("Images/base.png")
        baseX = 0
        self.fps=35
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.play()
            screen.fill(white)

            baseX -= 3

            screen.blit(bg, (0, 0))
            screen.blit(intro, (50, 110))

            screen.blit(base, (baseX, 450))
            screen.blit(base, (baseX + 285, 450))

            if baseX <= -285:
                baseX = 0

            self.write("Score: "+str(int(self.score)),white,80,30,40)
            self.write("High Score: "+str(int(self.HighScore)), red, 60, 400, 35)
            clock.tick(self.fps)
            pygame.display.update()

    def createPip(self):
        randomPipe_position=random.choice(pipeHeight)
        bottomPipe = greenPipe.get_rect(midtop=(400, randomPipe_position))
        topPipe = greenPipe.get_rect(midbottom=(400, randomPipe_position-140))
        return bottomPipe,topPipe
    def pipeMove(self,pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        return pipes
    def pipeDraw(self,pipes):
        for pipe in pipes:
            if pipe.bottom>=500:
                screen.blit(greenPipe, pipe)
            else:
                flipPipe=pygame.transform.flip(greenPipe,False,True)
                screen.blit(flipPipe, pipe)
        return pipes
    def Collisions(self,pipes):
        for pipe in pipes:
            if birdRect.colliderect(pipe):
                collisionSound.play()
                return False
        if birdRect.top<=-50 or birdRect.bottom>=450:
            deathSound.play()
            birdRect.center = (50, 200)
            return False
        return True
    def High_score(self,score, high_score):
        if score > high_score:
            high_score = score
        return high_score
    def play(self):
        gameActive = True
        pipeList=[]
        SPAWNPIPE=pygame.USEREVENT
        pygame.time.set_timer(SPAWNPIPE,1200)

        baseX = 0
        self.fps=40
        gravitiy=0.75
        birdMove=0
        score_sound_countdown = 100
        scr=0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE and gameActive:
                        birdMove = 0
                        birdMove-=12
                        flySound.play()
                    if event.key == pygame.K_SPACE and gameActive==False:
                        gameActive=True
                        pipe_list.clear()
                        birdRect.center=(50, 200)
                        birdMove=0
                        scr=0
                if event.type==SPAWNPIPE:
                    pipeList.extend(self.createPip())

            screen.fill(white)
            baseX -= 3

            if scr<=20:
                screen.blit(bg1, (0, 0))
            if scr>20:
                screen.blit(bg2,(0,0))

            if gameActive:
                birdMove+=gravitiy
                birdRect.centery+=birdMove
                screen.blit(Bird,birdRect)

                pipe_list = self.pipeMove(pipeList)
                self.pipeDraw(pipe_list)
                gameActive = self.Collisions(pipe_list)

                scr+=0.018

                score_sound_countdown -= 1.8
                if score_sound_countdown <= 0:
                    pointSound.play()
                    score_sound_countdown = 100
            else:
                self.intro()

            self.write(str(int(scr)), yellow, 130, 50, 60)
            self.score=scr
            self.HighScore = self.High_score(self.score, self.HighScore)

            screen.blit(base, (baseX, 450))
            screen.blit(base, (baseX + 285, 450))
            if baseX <= -285:
                baseX = 0

            clock.tick(self.fps)
            pygame.display.update()

game=Main()
game.intro()