#__author__ = 'Paul'
import pygame
import math
import time
import random

winx = 800
winy = 600

class Vector2d(object):
    def __init__(self,o,t):
        self.x = o
        self.y = t
        self.vector = [int(o),int(t)]

    #Pass in the value on the LHS
    def sub(self, gx, gy):
        goingto = [int(gx),int(gy)]
        nx = goingto[0]-self.vector[0]
        ny = goingto[1]-self.vector[1]
        ret = Vector2d((goingto[0]-self.vector[0]),(goingto[1]-self.vector[1]))
        return ret


class AI(object):
    def __init__(self,o,t,c):
        self.x = o
        self.y = t
        self.timer = 0.0
        self.fireRate = 3.0
        self.color = c
        self.w = 100
        self.h = 50

    def fire(self,elist,blist):
        global winx,winy,plrclr
        if len(elist)>1:
            en = elist[random.randrange(0,len(elist)-1)]
            if en.y > -50:
                mypos = Vector2d(self.x,self.y)
                vel = mypos.sub(en.x,en.y)
                blt = Bullet(self.x+self.w,self.y,vel,plrclr)
                blist.append(blt)

    def draw(self,sf):
        pygame.draw.rect(sf,self.color,(int(self.x),int(self.y),self.w,self.h))

    def decide(self,elist,blist,dt):
        self.timer += 1.0*dt
        if self.timer >= self.fireRate:
            self.fire(elist,blist)
            self.timer=0.0


class Enemy(object):
    def __init__(self,clr,r):
        global winx,health
        self.rad = r
        self.x = random.randrange(self.rad,winx-self.rad)
        self.y = random.randrange(-10000,-50)
        self.speed = Vector2d(0,150)
        self.color = clr
        self.hit = False

    def update(self,dt):
        global health,winx,winy,enemies
        self.x += self.speed.x*dt
        self.y += self.speed.y*dt
        if self.y-self.rad > winy:
            health -= 20

    def draw(self,sf):
        pygame.draw.circle(sf,self.color,(int(self.x),int(self.y)),self.rad)


class Bullet(object):
    def __init__(self,px,py,vl,c):
        self.x = px
        self.y = py
        self.color = c
        self.rad = 20
        self.vel = Vector2d(vl.x,vl.y)

    def update(self,dt):
        global bullets,winy,winx
        self.x += self.vel.x * dt
        self.y += self.vel.y * dt

    def draw(self,sf):
        pygame.draw.circle(sf,self.color,(int(self.x),int(self.y)),self.rad)


class Player(object):
    def __init__(self,wx,wy,cc):
        self.w=150
        self.h=100
        self.x=wx-(self.w/2)
        self.y=wy
        self.color=cc
        self.rad=150

    def draw(self,sf):
        pygame.draw.rect(sf,self.color,(int(self.x),int(self.y),self.w,self.h))


def ranColor():
    tup=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    return tup


def spawnEnemies(elist,num):
    i = 0
    while i < num:
        en = Enemy(ranColor(), random.randrange(100,200))
        elist.append(en)
        i += 1


def mouseMovement(events,mPos,clr):
    global bullets,enemies,plr
    global done
    for e in events:
        if e.type == pygame.QUIT:
            done = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            v = Vector2d(plr.x,plr.y)
            vv = v.sub(mPos[0],mPos[1])
            nb = Bullet(plr.x+(plr.w/2),plr.y,vv,clr)
            bullets.append(nb)


def keyEvent(events):
    global done
    for e in events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                done = True


def collision(elist,blist):
    velocityOffset=0.5
    for b in blist:
        for e in elist:
            if( math.sqrt((e.x - b.x)**2 + (e.y - b.y)**2) <= e.rad+(b.rad-2)):
                e.hit=True
                es = e.speed.sub(b.vel.x,b.vel.y)

                b.vel = b.vel.sub(e.speed.x,e.speed.y)
                b.vel.x *= -velocityOffset
                b.vel.y *= -velocityOffset

                e.speed.x = es.x*velocityOffset
                e.speed.y = es.y*velocityOffset

xctr=100
def makeFriend(pc,friends):
    global xctr
    a = AI(xctr,winy-20,pc)
    friends.append(a)
    xctr=700

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((winx,winy))
colorDict={"White":(255,255,255),"Red":(255,0,0),"Blue":(0,0,255),"Green":(0,255,0)}
plrclr = ranColor()
plr = Player(winx/2,winy-50,plrclr)
enemies = []
bullets = []
friends = []
numEnemies = 10
spawnEnemies(enemies,numEnemies)
clock = pygame.time.Clock()
done = False
gametime = 0.0
scfill = ranColor()
font = pygame.font.Font(None,22)
health = 100
friend = 0
win=False
loose=False

while not done:
    if len(enemies)<=0 and health > 0:
        done=True
        win=True
    if health <= 0:
        done = True
        loose = True
    #update
    mPos = pygame.mouse.get_pos()
    dt = clock.tick()/1000.0
    gametime += 1*dt
    for f in friends:
        f.decide(enemies,bullets,dt)
    if gametime >= 15.0 and friend==0:
        makeFriend(plrclr,friends)
        gametime = 0.0
        friend+=1
    if friend == 1 and gametime>=30.0:
        makeFriend(plrclr,friends)
        gametime = 0.0
        friend+=1
    collision(enemies,bullets)
    for e in enemies:
        e.update(dt)
        if e.y+e.rad < 0 and e.hit:
            enemies.remove(e)
        if e.y-e.rad>winy:
            enemies.remove(e)
    for self in bullets:
        self.update(dt)
        if self.x - self.rad > winx:
            bullets.remove(self)
        if self.x + self.rad < 0:
            bullets.remove(self)
        if self.y - self.rad > winy:
            bullets.remove(self)
        if self.y + self.rad < 0:
            bullets.remove(self)
    #input
    events = pygame.event.get()
    keyEvent(events)
    mouseMovement(events,mPos,plrclr)
    #draw
    screen.fill(scfill)
    hS = "Health: "+str(health)
    enS = "Enemies Left: "+str(len(enemies))
    hSS = font.render(hS,True,colorDict["White"])
    eSS = font.render(enS,True,colorDict["White"])
    screen.blit(hSS,(int(10),int(winy-50)))
    screen.blit(eSS,(int(550),int(winy-50)))
    plr.draw(screen)
    for b in bullets:
        b.draw(screen)
    for ee in enemies:
        ee.draw(screen)
    for f in friends:
        f.draw(screen)
    pygame.display.flip()
pygame.font.quit()
pygame.display.quit()
if win:
    print("You Won")
elif loose:
    print("You Lost")
