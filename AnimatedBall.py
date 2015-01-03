#Created by Alexandre Campos in 12/25/2014
#Last modification 01/03/2015

#Libraries
import pygame, random, math, timeit, sys

# Initialize the game engine
pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

# Set the height and width of the screen
size = (800, 450)
screen = pygame.display.set_mode(size)

class ball:
    """The objects."""

    def __init__(self, x, y, velocity, radius, angle, color=(0,0,0)):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.direction = [math.cos(2*math.pi*angle/360), math.sin(2*math.pi*angle/360)]
        self.color = color

        #Check if the initial ball isn't beyond the screen
        if self.x < offset+self.radius+1: self.x = offset+radius+1
        elif self.x > size[0]-offset-self.radius-1: self.x = size[0]-offset-self.radius-1

        if self.y < offset+self.radius+1: self.y = offset+radius+1
        elif self.y > size[1]-offset-self.radius-1: self.y = size[1]-offset-self.radius-1

    #Updates it
    def update(self):

        #New position of the ball based on its direction
        self.x += self.velocity*self.direction[0]
        self.y += self.velocity*self.direction[1]

        #Check colision with border
        if self.x-offset-self.radius <= 0 or self.x+offset+self.radius >= size[0]: self.direction[0] *= -1
        if self.y-offset-self.radius <= 0 or self.y+offset+self.radius >= size[1]: self.direction[1] *= -1

pygame.display.set_caption("Animated Ball")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

#time of each level
time = 5

#Size of the limit rectangle
offset = 20
limit = [offset, offset, size[0]-2*offset, size[1]-2*offset]

font = pygame.font.SysFont('Calibri', 30, True, False)
font2 = pygame.font.SysFont('Impact', 40, False, False)

#The welcome message.
welcome=("Welcome to the ball game.",
    "Your objective is to keep the mouse away from the balls.",
    "If one ball hits the mouse or the mouse escapes the rectangle, the game ends.",
    "Survive as long as you can!")

screen.fill(WHITE)

for i in xrange(4):
    texto = welcome[i]
    text = font.render(texto, True, BLUE)
    screen.blit(text, [offset, offset+i*20])

pygame.display.flip()

wait = timeit.default_timer()
while timeit.default_timer()-wait < 6: pass

#Current level
level = 1

while True:

    #Draws the balls in initial position
    balls = []
    for i in xrange(level):
        balls.append(    ball(random.randint(0,size[0]), random.randint(0,size[1]), #Initial position
                random.randint(0,15), #Velocity
                random.randint(10,20), #Radius
                random.randint(0, 359), #Initial angle
                (random.randint(0,250), random.randint(0,250), random.randint(0,250)) #Color
                ))

    #3 sec message
    espera = timeit.default_timer()
    while True:

        if timeit.default_timer()-espera > 3: break

        screen.fill(WHITE)

        #Rectangle limite the ball movement
        pygame.draw.rect(screen, BLACK, limit, 2)

        #Current level
        level_track = font2.render("Level: %s    Time: %s"%(level, (level-1)*time), True, BLUE)
        screen.blit(level_track, [offset, offset])

        #Draws statics balls
        for b in balls: pygame.draw.circle(screen, b.color, [int(b.x), int(b.y)], b.radius)

        #Regressive timer
        texto = "%s"%(3-int(timeit.default_timer()-espera))
        text = font.render(texto, True, BLUE)
        screen.blit(text, [400, size[1]/2])

        #Updates screen
        pygame.display.flip()

        clock.tick(60)

    #Level duration
    start = timeit.default_timer()

    # Loop as long as done == False
    while not done:

        mouse_escape = False
        now = timeit.default_timer()

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
                sys.exit(0)
#               done = True # Flag that we are done so we exit this loop
         
        # Clear the screen and set the screen background
        screen.fill(WHITE)

        #Rectangle limite the ball movement
        pygame.draw.rect(screen, BLACK, limit, 2)

        #Current level
        level_track = font2.render("Level: %s    Time: %s"%(level, (level-1)*time+int(now-start)), True, BLUE)
        screen.blit(level_track, [offset, offset])

        #Draws and updates the balls. Check end of the game.
        for b in balls:

            #Update ball
            b.update()
            pygame.draw.circle(screen, b.color, [int(b.x), int(b.y)], b.radius)

            #Check if the mouse has scaped
            if pygame.mouse.get_pos()[0] < offset or pygame.mouse.get_pos()[0] > size[0]-offset: mouse_escape = True
            if pygame.mouse.get_pos()[1] < offset or pygame.mouse.get_pos()[1] > size[1]-offset: mouse_escape = True

            #Check mouse colision or mouse scape. Improve mouse scape with limiter rectangle.
            if (abs(b.x-pygame.mouse.get_pos()[0]) < b.radius and abs(b.y-pygame.mouse.get_pos()[1]) < b.radius) or mouse_escape:

                #Time of ending game.
                fim=timeit.default_timer()

                screen.fill(WHITE)

                #Limit rectangle
                pygame.draw.rect(screen, BLACK, limit, 2)

                #Tells the user about the mouse escape or which ball caused the end of game.
                if mouse_escape:
                    pygame.draw.rect(screen, RED, [0, 0, size[0], offset], 0)
                    pygame.draw.rect(screen, RED, [0, 0, offset, size[1]], 0)
                    pygame.draw.rect(screen, RED, [0, size[1]-offset, size[0], offset], 0)
                    pygame.draw.rect(screen, RED, [size[0]-offset, 0, offset, size[1]], 0)
                else:
                    pygame.draw.circle(screen, RED, [int(b.x), int(b.y)], b.radius)

                #Ending message.
                EXIT = "You lost in level %s and survived for %s s."%(level, int((level-1)*time+fim-start))
                font = pygame.font.SysFont('Calibri', 30, True, False)
                text = font.render(EXIT, True, BLUE)
                screen.blit(text, [offset, size[1]/2])

                #Updates screen
                pygame.display.flip()

                #Waits the player read the message
                while timeit.default_timer()-fim < 3: clock.tick(60)
                pygame.quit()
                sys.exit(0)

        # This limits the while loop to a max of 60 times per second.
        pygame.display.flip()
        clock.tick(60)

        #End of level
        if timeit.default_timer()-start >= time:
            level += 1
            break

# Be IDLE friendly
pygame.quit()
