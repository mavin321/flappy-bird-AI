import pygame
from pygame.locals import *
import random
from ai_agent import RuleBasedAIAgent

pygame.init() #initializing pygame

#used to control speed of game
clock = pygame.time.Clock()
fps=60

#creating game window 
screen_width=339
screen_height=650
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font=pygame.font.SysFont('Bauhaus 93', 60)
white=(255, 255, 255)

#ai toggle
USE_AI = True

#game variables
ground_scroll=0
scroll_speed=2
flying = False #prevent the game from starting right away unless an action is executed
game_over=False 
pipe_gap=150
pipe_frequency=1500 #since we are using a clock we can set this to milliseconds
last_pipe=pygame.time.get_ticks()- pipe_frequency #last time a pipe was made
score=0
pass_pipe=False


#loading background images
bg=pygame.image.load('images/background.png')
ground_image=pygame.image.load('images/ground.png')
button_img=pygame.image.load('images/restart.png')

ai_player = RuleBasedAIAgent()


#function to reset everything to restart the game
def reset_game():
    #remove all the pipes
    pipe_group.empty()
    #reposition the bird
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    flappy.vel = 0
    ai_player.reset()
    score=0 #this will only affect score as a local variable 
    return score #returning score will change the globale variable


#function to show score
def draw_text(text,font,text_col,x ,y):
    img=font.render(text, True, text_col)
    screen.blit(img,(x,y))


#creating the bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #to inherit from the sprite function
        #this will take care of the animation
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,4):
            img=pygame.image.load(f'images/bird{num}.png')
            self.images.append(img)

        self.image=self.images[self.index]
        self.rect=self.image.get_rect()#creates a boundary for the object
        self.rect.center=[x,y]
        self.vel=0 #velocity
        self.clicked=False #when the game starts nothing has been clicked
        self.ai_flap=False


    def update(self):

        
        if flying == True:
        #handling the gravity
            self.vel+=0.3 #how fast it falls
            if self.vel > 8:
                self.vel= 8
            if self.rect.bottom < 550: #making sure the bird doesnt go down the screen
                self.rect.y += int(self.vel)

        if game_over==False:
            flap_command = False
            if USE_AI:
                flap_command = self.ai_flap
            else:
                #jump when mouse is clicked
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #meaning if mouse is left clicked
                    self.clicked=True
                    flap_command = True
                #mouse being released
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked=False

            if flap_command:
                self.vel=-7

            self.ai_flap=False

            #handle the animation by using multiple pictures at different stages of the animation
            self.counter+=1
            flap_cooldown=5

            if self.counter > flap_cooldown:
                self.counter=0
                self.index+=1
                
            self.image=self.images[self.index % len(self.images)] #this is done to preven the index from going out of range

            #rotate the bird
            self.image= pygame.transform.rotate(self.images[self.index % len(self.images)], self.vel * -2)
        else:
           self.image= pygame.transform.rotate(self.images[self.index % len(self.images)], -90) 


#creating a class for pipes
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load('images/pipe.png')
        self.rect = self.image.get_rect()
        self.position = position
        #position 1 is for the top and -1 is for the bottom
        if position ==1:
            self.image=pygame.transform.flip(self.image,False , True )
            self.rect.bottomleft=[x,y - int(pipe_gap/2)]
        if position==-1:
            self.rect.topleft=[x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -=scroll_speed
        #removing the pipe as soon as its out of the screen
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action=False
        
        #get mouse position
        pos=pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1: #shows mouse has been clicked
                action=True

        
        #draw button
        screen.blit(self.image,(self.rect.x, self.rect.y))

        return action

#creating a group for the birds and pipes
bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
#ceating an instance of the Bird and setting position of bird on screen
flappy=Bird(100,int(screen_height/2))

#adding flappy to bird group
bird_group.add(flappy)

#create restart button instance
button=Button(screen_width//2 - 50, screen_height//2 -100, button_img)

 #loading background music
pygame.mixer.music.load('music/background_music.mp3')
pygame.mixer.music.play(-1)


#creating game loop
run=True
while run:
    #setting speed
    clock.tick(fps)

    if USE_AI and game_over == False:
        flying = True
        flappy.ai_flap = ai_player.choose_action(flappy, pipe_group, pipe_gap)
    else:
        flappy.ai_flap = False
    
    #draw background
    screen.blit(bg, (0,0)) #position of background image on screen
    #update and draw the bird
    bird_group.update()
    pipe_group.draw(screen)
    bird_group.draw(screen)
    
    #draw and scroll
    screen.blit(ground_image,(ground_scroll,550)) #position of ground image on screen
    
    #check score
    #this checks whether the bird has passed the pipe then adds a score
    if len(pipe_group)>0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe== False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe=False

    #display score
    draw_text(str(score),font, white, int(screen_width/2),20)
    
    
    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <0:# the false means that the groups should not be deleted if collision does happen
        game_over=True


    #check if bird has hit the ground
    if flappy.rect.bottom>=550:
        game_over=True
        flying=False

    if game_over==False and flying== True:
        #generate new pipes
        time_now=pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height=random.randint(-100, 100)
            btm_pipe=Pipe(screen_width,int(screen_height/2) + pipe_height, -1)# make them generate pipes after screen
            top_pipe=Pipe(screen_width,int(screen_height/2)+ pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe=time_now
        
        #draw and scroll
        ground_scroll-=scroll_speed
        if abs(ground_scroll) > 30:
            ground_scroll=0
        #to make the pipe stop after game over
        pipe_group.update()


#check for game over and reset
    if game_over== True:
       if button.draw()== True:
           game_over=False
           score=reset_game()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over==False:
            flying=True

    pygame.display.update() #function that makes the images work


pygame.quit()
