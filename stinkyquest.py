import pygame
import time
import random
import sys

pygame.init()
clock = pygame.time.Clock()

display_width = 800
display_height = 600

#sets up canvas
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("StinkyQuest")

#set up colors
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

#load image
catImg = pygame.image.load("data/stinky.png")
cat_width = 90
bisImg = pygame.image.load("data/biscuits.png")
bellaImg = pygame.image.load("data/bella.png")

#this puts the image on the canvas
def cat(x, y):
    gameDisplay.blit(catImg, (x,y))

def things(char, thingx, thingy, thingw, thingh):
    gameDisplay.blit(char, (thingx, thingy))

def subtitle(text, pos):
    largeText = pygame.font.Font('data/freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height*pos))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def crash(fallen):
    with open("scores.txt", "r") as s:
        hi_score = int(s.readlines()[0])
    crashmenu=True
    while crashmenu:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        message_display("wall smacc")
        subtitle("Biscuits High: "+str(hi_score), 0.45)
        subtitle("Adventures: "+str(fallen), 0.55)
        button("more", 150, 450, 100, 50, green, bright_green, game_loop)
        button("stop", 550, 450, 100, 50, red, bright_red, quitgame)
    
def grab(fallen):
    with open("scores.txt", "r") as s:
        hi_score = int(s.readlines()[0])
    grabmenu=True
    while grabmenu:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        message_display("you got got")
        subtitle("Biscuits High: "+str(hi_score), 0.45)
        subtitle("Adventures: "+str(fallen), 0.55)
        button("more", 150, 450, 100, 50, green, bright_green, game_loop)
        button("stop", 550, 450, 100, 50, red, bright_red, quitgame)

def biscuits(bisc):
    font = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects("Biscuits: "+str(bisc), font)
    TextRect.center = ((display_width*0.85), (display_height*0.05))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def dodged(dodge):
    font = pygame.font.Font('freesansbold.ttf', 25)
    TextSurf, TextRect = text_objects("Dodged: "+str(dodge), font)
    TextRect.center = ((display_width*0.1), (display_height*0.05))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()    
    
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/4))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    
def button (msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center =((x+int(w/2)),(y+int(h/2)))
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largetext = pygame.font.Font('freesansbold.ttf', 95)
        TextSurf, TextRect = text_objects("Stinky's Quest", largetext)
        TextRect.center = ((display_width/2),(display_height/3))
        gameDisplay.blit(TextSurf, TextRect)
        subtitle("created by Stinky", 0.5)

        button("Chaos!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    try:
        f = open("scores.txt")
    except FileNotFoundError:
        f = open("scores.txt", "w+")
        f.write("0")
    f.close()

    with open("scores.txt", "r") as s:
        bisc_prev = int(s.readlines()[0])
  
    x=(int(display_width*0.45))
    y=(int(display_height*0.8))
    x_change = 0
    c = 1 #c is the item seed id: guarentees the first fallen object is a biscuits
    d = 10 #this is the upper limit of c and increases slowly, makes bella more likely over time

    bisc=0
    dodge = 0
    cat_speed = 5
    
    fallen=0 #keeps track of the number of fallen items
    
    thing_startx=random.randrange(100, display_width-100)
    thing_starty=-600
    thing_speed = 7
    thing_width =100
    thing_height=100

    
    #sets up the game loop
    gameExit = False

    while not gameExit:

    #the keydown events take inputs!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -cat_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = cat_speed
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        x += x_change

        gameDisplay.fill(white)

        #things(thingx, thingy, thingw, thingh, color)
                
        if c > 7:
            things(bellaImg, thing_startx, thing_starty, 90, 101)
            
        else:
            things(bisImg, thing_startx, thing_starty, 90, 101)
            
        
            
        thing_starty +=thing_speed
            
        #collision logic

        cat(x,y)
               
        if x > display_width-cat_width or x < 0:
                gameExit=True
                if bisc > bisc_prev:
                    with open("scores.txt", "w") as s:
                        s.write(str(bisc))
                    print("Highscore")
                crash(fallen)
                
        if c > 7:
            
            if y < thing_starty+thing_height:
                #print('y cross')

                if x > thing_startx and x < thing_startx + thing_width or x+cat_width > thing_startx and x+cat_width < thing_startx+thing_width:
                    #print('x cross')
                    if bisc > bisc_prev:
                        with open("scores.txt", "w") as s:
                            s.write(str(bisc))
                        #print("Highscore")
                    grab(fallen)
                    

        else:
            
            if y < thing_starty+thing_height:
                #print('y cross')

                if x > thing_startx and x < thing_startx + thing_width or x+cat_width > thing_startx and x+cat_width < thing_startx+thing_width:
                    #print('x cross')
                    bisc +=1
                    
                    
        
        if thing_starty > display_height:
            if c > 7:
                dodge+=1
                thing_speed+=1
            thing_starty = 0-thing_height
            thing_startx = random.randrange(0, display_width-100)
            fallen+=1
         
            if fallen==10:
                d+=1
            elif fallen==15:
                d+=2
            elif fallen>30:
                d+=2
          
            c = random.randrange(0, d, 1)
            
        cat_speed = 5+(int(bisc/50))
        
        dodged(dodge)
        biscuits(bisc)
        pygame.display.update()
        clock.tick(60)
    
game_intro()
pygame.quit()
quit()
