from pygame import *
from random import randint
window = display.set_mode((700,500))
background = transform.scale(image.load('galaxy.jpg'),(700,500))
display.set_caption('доганялки')

game = True
klock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.40)
font.init()
win = font.SysFont(None,70).render('YOU WIN',True,(255,0,0))
lose = font.SysFont(None,70).render('YOU lose',True,(255,0,0))



class Game_sprite(sprite.Sprite):
    def __init__(self,background,x,y,speed,widht,hight):
        super().__init__()
        self.speed = speed
        self.image = transform.scale(image.load(background),(widht,hight))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Game_sprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,12,20)
        bullets.add(bullet)

class Bullet(Game_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

count = 0
class Enemy(Game_sprite):
    def update(self):
        global count
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0,700-50)
            count += 1




monsters = sprite.Group()
bullets = sprite.Group()
killed = 0
for i in range(5):
    monster = Enemy('ufo.png',randint(0,700-50),-50,randint(1,3),50,35)
    monsters.add(monster)
rocket = Player('rocket.png',325,375,6,45,100)
#cyborg = Enemy('cyborg.png',400,400,3)

finish = False
died = mixer.Sound('fire.ogg')
while game:
    if not finish:
        window.blit(background,(0,0))
        loses = sprite.groupcollide(monsters,bullets,True,True)
        for i in loses:
            monster = Enemy('ufo.png',randint(0,700-50),-50,randint(1,3),50,35)
            monsters.add(monster)
            killed += 1
        if killed >= 10:
            finish = True
            window.blit(win,(200,200))
        if count >= 5:
            window.blit(lose,(200,200))
        rocket.reset()
        rocket.update()
        monsters.draw(window)
        monsters.update()
        text = font.SysFont('arial',26).render('пропушен:'+ str(count),True,(255,0,0))
        text1 = font.SysFont('arial',26).render('убито:'+ str(killed),True,(255,0,0))
        window.blit(text,(10,20))
        window.blit(text1,(10,50))
        bullets.update()
        bullets.draw(window)
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                rocket.fire()
    display.update()
    klock.tick(60)


