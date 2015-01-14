#Created by Alexandre Campos in 12/25/2014
#Last modification 01/14/2015

import pygame, random, math, os, sys, timeit
os.system("clear")

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
LGRAY    = ( 200, 200, 200)
RED        = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE    = (   0,   0, 255)

pygame.init()

# Set the width and height of the screen [width, height]
SIZE = (800, 450)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Animated Ball")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Calibri', 30, True, False)
font2 = pygame.font.SysFont('Impact', 40, False, False)

class Ball:
    """The objects."""

    def __init__(self, x, y, velocity, radius, color):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.color = color

        self.center = x, y

    def draw(self):
        pygame.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.radius)
        pygame.draw.circle(screen, BLACK, [int(self.x), int(self.y)], self.radius, border) # Mask

    def update(self):

        self.x += (self.velocity[0])
        self.y += (self.velocity[1])

        self.x = max(self.x, self.radius+offset)
        self.y = max(self.y, self.radius+offset)

        self.x = min(self.x, SIZE[0]-self.radius-offset)
        self.y = min(self.y, SIZE[1]-self.radius-offset)

        self.center = (self.x, self.y)

        # Hit limit rectangle.
        if self.x+self.radius >= SIZE[0]-offset or self.x-self.radius <= offset: self.velocity[0] = -self.velocity[0]
        if self.y+self.radius >= SIZE[1]-offset or self.y-self.radius <= offset: self.velocity[1] = -self.velocity[1]

        self.draw()

def Point_Distance(A, B):
    """Euclidean distance between A and B."""
    return int( pow( pow(B[0]-A[0], 2) + pow(B[1]-A[1],2), 0.5 ) )

def generate_ball():
    """Generate a random ball."""
    angle = random.random()*2*math.pi # Generates initial angle
    vel = random.randint(0, 10) # Generates initial velocity

    radius = random.randint(10, 20) # Radius
    x = random.randint(radius+offset, SIZE[0]-radius-offset) # Initial x
    y = random.randint(radius+offset, SIZE[1]-radius-offset) # Initial y
    velocity = [vel*math.cos(angle), vel*math.sin(angle)] # Initial vector velocity
    color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    return Ball(x, y, velocity, radius, color)

def hit(b1, b2):
    """Check if b1 and b2 are touching each other."""
    return Point_Distance((b1.x, b1.y), (b2.x, b2.y)) <= b1.radius+b2.radius

def collision(b1, b2):
    """Check ball collisions and vectorial behavior."""

    # http://gamedevelopment.tutsplus.com/tutorials/when-worlds-collide-simulating-circle-circle-collisions--gamedev-769

    if hit(b1, b2):
        v1 = b1.velocity
        v2 = b2.velocity
        m1 = b1.radius
        m2 = b2.radius

        b1.velocity=[(v1[0]*(m1-m2)+(2*m2*v2[0]))/(m1+m2), (v1[1]*(m1-m2)+(2*m2*v2[1]))/(m1+m2)]
        b2.velocity=[(v2[0]*(m2-m1)+(2*m1*v1[0]))/(m1+m2), (v2[1]*(m2-m1)+(2*m1*v1[1]))/(m1+m2)]

        # Prevent the balls from sticking together. Perhaps this will bug if the ball is too close to the border.
        while hit(b1, b2): # Causes strange moves.
            b1.x+=b1.velocity[0]
            b1.y+=b1.velocity[1]

            b2.x+=b2.velocity[0]
            b2.y+=b2.velocity[1]

def wait(n):
    """Just wait and gives the option to quit."""
    start = timeit.default_timer()
    while True:
        wait_quit()
        if timeit.default_timer()-start > n: break

def draw_bg():
    """Draw background."""
    pygame.draw.rect(screen, BLACK, [offset, offset, SIZE[0]-2*offset, SIZE[1]-2*offset], border)

def draw_info(now, start, color):
    """What level, what time."""

    info1 = font2.render("Level: %s"%level, True, color)
    info2 = font2.render("Time: %s"%((level-1)*time+int(now-start)), True, color)
    info3 = font2.render("Score: %s"%(score/100), True, color)
    screen.blit(info1, [offset, offset])
    screen.blit(info2, [offset+SIZE[0]/4, offset])
    screen.blit(info3, [offset+SIZE[0]/2, offset])

def regressive_counter(n):
    """Regressive count."""
    start = timeit.default_timer()

    while True:

        wait_quit()

        screen.fill(WHITE) # Clear
        draw_bg() # Background
        draw_info(0, 0, LGRAY) # Level info

        for bola in balls: bola.draw()

        counter = font2.render("%s"%(3-int(timeit.default_timer()-start)), True, BLUE)
        screen.blit(counter, [SIZE[0]/2, SIZE[1]/2])

        # Update screen.
        draw_it_all()

        # Are we done?
        if timeit.default_timer()-start > n: break 

def draw_it_all(tick = 60):
    """Draw everything."""

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(tick)

def end_game(what, ball = None):

    while True:

        wait_quit()

        if what == "mouse":

            screen.fill(RED)
            pygame.draw.rect(screen, WHITE, [offset, offset, SIZE[0]-2*offset, SIZE[1]-2*offset]) # Red lose rectangle
            draw_bg()
            draw_info(now, start, LGRAY)

        elif what == "collision":

            screen.fill(WHITE)
            draw_bg()
            draw_info(now, start, LGRAY)

            # Ball that caused lost.
            b.color = RED
            b.draw()

        game_over = font.render("You lost in level %s and your score was %s."%(level, score/100), True, BLACK)
        x, y = game_over.get_size()
        screen.blit(game_over, [ (SIZE[0]-x)/2, (SIZE[1]-y)/2 ]) # Center.

        draw_it_all(10)

def wait_quit():
    """Checks if quit."""
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            pygame.quit()
            sys.exit(0)

def welcome():
    """Opening message."""

    screen.fill(WHITE)

    #The welcome message.
    msg=("Welcome to the ball game.",
        "Your objective is to keep the mouse away from the balls.",
        "If one ball hits the mouse or the mouse escapes the rectangle, the game ends.",
        "The more the mouse moves, the better is your score.",
        "Survive as long as you can!")

    for i in xrange(5):
        text = font.render(msg[i], True, BLUE)
        screen.blit(text, [offset, offset+i*20])

    pygame.display.flip()

    # Wait the use reads.
    wait(6)

level = 1 # Current level
time = 5 # Time of each level
score = 0

#Size of the limit rectangle
border = 2
offset = 20

# Loop until the user clicks the close button.
done = False

# Opening message
welcome()

# -------- Main Program Loop -----------
while True:

    screen.fill(WHITE)
    draw_bg() # Background
    draw_info(0, 0, LGRAY) # Info

    # Loop to create non touching balls
    balls = []
    while len(balls) < level:
        flag = True

        b = generate_ball() # Creates random ball

        for item in balls: # Check if it is not touching the other balls
            if hit(b, item):
                flag = False
                break

        if flag:
            wait(.1) # Allow user to see the balls being created.
            b.draw()
            balls.append(b)

            draw_it_all() # Draws

    # Let the player gets used to the balls
    regressive_counter(3)

    #Level duration
    start = timeit.default_timer()

    prev_pos = pygame.mouse.get_pos() # Initial mouse

    while not done: # Main event loop
        wait_quit()

        now = timeit.default_timer()
        pos = pygame.mouse.get_pos() # Mouse now

        # Did the mouse scape?
        if pos[0] < offset or pos[0] > SIZE[0]-offset or pos[1] < offset or pos[1] > SIZE[1]-offset:
            end_game("mouse")

        # The more the mouse moves, in advanced level, more points.
        score += Point_Distance(prev_pos, pos)*level
        prev_pos = pos

        screen.fill(WHITE) # Clear
        draw_bg() # Background
        draw_info(now, start, BLUE) # Level info

        # Look for collisions between the balls
        for i in xrange(level-1):
            for j in xrange(i+1, level):
                collision(balls[i], balls[j])

        # Updates and draw the balls
        for b in balls:

            # Hit the mouse?
            if Point_Distance(b.center, pos) <= b.radius:
                end_game("collision", b)

            b.update()

        # Drawing.
        draw_it_all()

        #End of level
        if timeit.default_timer()-start >= time:
            level += 1
            break
