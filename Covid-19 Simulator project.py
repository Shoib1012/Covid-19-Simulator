#imports all the libraries
import pygame
import random
import pymunk
import matplotlib.pyplot as plt
import time

pygame.init()

#initialises all variables, constants and arrays
display_width = 1000
display_height = 1000
radius = 10
time_count = []
t = 0
infection_rate = 1

cells_number = 300
infected_number = 1

immunerate = 1.01
progression_time = 950
speed = 200
infectionrate = 2.38
infectedspeed = 100

number_of_infected = infected_number

Background_colour = (255,255,255)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
yellow = (255,255,0)
red = (255,1,1)
orange = (255, 165, 0)
light_blue = (173,216,230)

orange_hex = '#FDB750'
light_blue_hex = '#add8e6'

red_hex = '#FF0000'
green_hex = '#00FF00'
blue_hex =  '#0000FF'

healthy_colour_hex = red_hex
infected_colour_hex = green_hex
immune_colour_hex = blue_hex

healthy_colour = green
infected_colour = red
immune_colour = blue
dead_colour = black

#sets up a clock for the system and space
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 144

#creates a class for the cell
class Cell():
    def __init__(self,x,y,immune_rate):
        self.x = x
        self.y = y
        self.immune_rate = immune_rate

        #initialises a body for the cell for pymunk
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = random.uniform(speed * -1, speed), random.uniform(speed * -1, speed)
        self.shape = pymunk.Circle(self.body, radius)
        #sets the density and elasticity for the cell
        self.shape.density = 1
        self.shape.elasticity = 0.995
        self.infected_time = 1
        self.healthy = True
        self.infected = False
        self.immune = False
        self.dead = False
        space.add(self.body,self.shape)

    #sets up the method for drawing the cell
    def draw(self):
        #sets the x and y position for the cell
        x,y = self.body.position
        #draws all the cell types
        if self.infected == True:
            pygame.draw.circle(display,infected_colour,(int(x),int(y)),radius)
        elif self.immune == True:
            pygame.draw.circle(display,immune_colour,(int(x),int(y)),radius)
        elif self.dead == True:
            pygame.draw.circle(display,dead_colour,(int(x),int(y)),radius)
        else:
            pygame.draw.circle(display,healthy_colour,(int(x),int(y)),radius)

    #creates a method for the incubation period
    def pass_time(self):
        global number_of_infected
        #adds to the timer if the cell is infected
        if self.infected:
            self.infected_time += 1
        #if the incubation period is reached, the cell is no longer infected and transitions to the next stage
        if self.infected_time >= progression_time:
            self.infected = False
            #determines the condition so that the cell will become immune or not
            if self.immune_rate <= 1:
                self.immune = True
                #if the cell becomes immune the number of infected cells decreases(for the graph)
                number_of_infected -= 1
                #changes the collision for immune cells so that they don't infect other cells
                self.shape.collision_type = cells_number + 2
            else:
                #makes the cells dead if they don't become immune
                self.dead = True
                number_of_infected -= 1
                #changes the velocity of dead cells to 0 so that they don't move and also changes their collision types for the above reason
                self.body.velocity = 0,0
                self.shape.collision_type = cells_number + 2

    #creates a method for infecting each cell ; the attributes are arbirtary and have no significance
    def infect(self, space=0, arbiter=0, data=0):
        global number_of_infected, infection_rate
        #changes the state of the cell when they get infected
        if infection_rate <= 1:
            self.healthy = False
            self.infected = True
            #the number of infected cells is increased and the collision type is changed.
            self.body.velocity = random.uniform(infectedspeed * -1, infectedspeed), random.uniform(infectedspeed * -1, infectedspeed)
            number_of_infected += 1
            self.shape.collision_type = cells_number + 1

    #creates method for infecting the first cell
    def startinfect(self, space=0, arbiter=0, data=0):
        self.healthy = False
        self.infected = True
        self.shape.collision_type = cells_number + 1

#creates a class for the borders
class Wall():
    #takes the start and end point for the walls
    def __init__(self,p1,p2):
        #defines the body shape of the wall; sets it as a segment
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 5)
        self.shape.elasticity = 0.995
        space.add(self.body,self.shape)

#creates arrays to store the data for the graph
healthy_count = []
infected_count = []
immune_count = []
dead_count = []

#creates a function that creates the game and stores the main loop
def game():
    global number_of_infected, time_count, t, infected_number, infection_rate
    #creates a new instance of the class cell for the number of cells chosen
    cells = [Cell(random.randint(0,display_width),random.randint(0,display_height),random.uniform(0,immunerate)) for i in range(cells_number)]

    def coll_begin(space=0, arbiter=0, data=0):        
        return True

    #determines the collision logic for the cells
    #the for loop iterates through all the cells and starts at 1 since the for loop is inclusive and there is no cell 0
    for i in range(1,cells_number+1):
        #assigns a collision type for all the instances of the cell
        #the index is i-1 to avoid an index error
        cells[i-1].shape.collision_type = i
        #creates a collision handler for the cells, populates it and adds it to the space
        handler = space.add_collision_handler(i,cells_number+1)
        handler.begin = coll_begin
        #makes it so that every collision that occurs causes the cell to get infected (calls the infected method)
        handler.separate = cells[i-1].infect
    
    #makes it so that a random cell in all the cells become infected to start with
    for i in range(infected_number):
        random.choice(cells).startinfect()
    
    #initializes the 4 walls that create the border
    walls = [Wall((0, 0), (0, display_height)),
             Wall((0, 0), (display_width, 0)),
             Wall((0, display_height), (display_width, display_height)),
             Wall((display_width, 0),(display_width, display_height))]

    #main loop
    run = True
    while run == True:
        #stops pygame if the program is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #randomizes the infection rate every time a collision occurs
        if coll_begin:
            infection_rate = random.uniform(0,infectionrate)

        #initialises the number of cells in each state
        infected_count_this_frame = 0
        healthy_count_this_frame = cells_number
        immune_count_this_frame = 0
        dead_count_this_frame = 0

        #creates the background
        display.fill(Background_colour)
        #draws all the cells
        for cell in cells:
            cell.draw()
            #calls the pass_time function
            cell.pass_time()
            #changes the number of cells in each variable depending on the state of the cells
            if cell.healthy:
                healthy_count_this_frame += 1
            elif cell.infected:
                infected_count_this_frame += 1
                healthy_count_this_frame -= 1
            elif cell.immune:
                immune_count_this_frame += 1
                healthy_count_this_frame -= 1
            elif cell.dead:
                dead_count_this_frame += 1
                healthy_count_this_frame -= 1

        #creates a cap for the number of cells in each array
        if len(infected_count) <= 10000:
            #calibrates the number of cells in each array to make the graph accurate
            infected_count.append(infected_count_this_frame/2)
        if len(healthy_count) <= 10000:
            healthy_count.append(healthy_count_this_frame/2)
        if len(immune_count) <= 10000:
            immune_count.append(immune_count_this_frame)
        if len(dead_count) <= 10000:
            dead_count.append(dead_count_this_frame)

        #allows the display to update
        pygame.display.update()
        #updates the clock every FPS
        clock.tick(FPS)
        #causes the step to update 1/FPS per second
        space.step(1/FPS)
        #updates the time variable for the graph
        t += 1
        #caps the time for the graph
        if len(time_count) <= 10000:
            time_count.append(t)
        
        if infected_count_this_frame == 0:
            pygame.time.delay(1500)
            run = False

#creates a menu for the program
def menu():
    global cells_number, immunerate, infected_number, progression_time, display_height, display_width, display, radius, FPS, speed, infectionrate, healthy_colour, infected_colour, orange, light_blue, infected_colour_hex, orange_hex,healthy_colour_hex, light_blue_hex
    print('1.Start\n2.Change number of total cells\n3.Change the immune rate\n4.Set the starting number of infected people\n5.Set the incubation period\n6.Set the speed of the cells\n7.Set the radius of the cells\n8.Set the size of the display window\n9.Set FPS\n10.Set infection rate\n11.Set real values for ebola\n12.Set real values for covid\n13.Colourblind mode\n')
    choice = input("what do you want to do? Remember all values must be an integer unless stated otherwise and that the default values are generated using real values for covid-19\n")
    try:
        if choice == '1':
            #initialises the display window for the program
            display = pygame.display.set_mode((display_width,display_height))
            pygame.time.delay(1000)
            game()
            #calls the function to draw the graph
            drawgraph()
        if choice == '2':
            #casts the inputs taken so that they can be operated on
            try:
                cells_number = int(input('enter the population number that you want the program to start with;note '+str(cells_number)+' is the default value\n'))
            except Exception:
                print('not an integer value; value has been reset\n')
                cells_number = 300
            menu()
        if choice == '3':
            try:
                immunerate = float(input('enter the immune rate that you desire (float); note that this will be in the form <= 1/immunerate and '+str(immunerate)+' is the default value\n'))
            except Exception:
                immunerate = 1.01
                print('not an float value; value has been reset\n')
            menu()
        if choice == '4':
            try:
                infected_number = int(input('enter the number of infected people that you want to start with; note that this number will be taken out of the population number and that the default number is '+str(infected_number)+'\n'))
            except Exception:
                infecte_number = 1
                print('not an integer value; value has been reset\n')
            menu()
        if choice == '5':
            try:
                progression_time = int(input('Set the time it takes for the infected people to progress to the next stage of their disease; note '+str(progression_time)+' is the default value\n'))
            except Exception:
                progression_time = 500
                print('not an integer value; value has been reset\n')
            menu()
        if choice == '6':
            try:
                speed = int(input('set the speed at which the cells move; note '+str(speed)+' is the default\n'))
            except Exception:
                speed = 200
                print('not an integer value; value has been reset\n')
            menu()
        if choice =='7':
            try:
                radius = int(input('intput the radius that you desire; note that '+str(radius)+' is the default\n'))
            except Exception:
                radius = 10
                print('not an integer value; value has been reset\n')
            menu()
        if choice == '8':
            try:
                print('Enter the desired display width and height; note the default is '+str(display_width)+' by '+str(display_height)+' and first input is width and second input is height')
                display_width = int(input())
                display_height = int(input())
            except Exception:
                display_width = 1000
                display_height = 1000
                print('not an integer value; value has been reset\n')
            menu()
        if choice == '9':
            try:
                FPS = int(input('input what FPS you would like; note the default FPS is '+str(FPS)+'\n'))
            except Exception:
                FPS = 144
                print('not an integer value; value has been reset\n')
            menu()
        if choice =='10':
            try:
                infectionrate == float(input('Enter the desired infection rate; note default infection rate is ' + str(infectionrate) + '\n'))
            except Exception:
                infectionrate = 2.38
                print('not an float value; value has been reset\n')
            menu()
        if choice == '11':
            immunerate = 2
            infectionrate = 3.33
            progression_time = 1100
            infectedspeed = 50
            print("the settings have now changed to match ebola's real values\n")
            menu()
        if choice == '12':
            immunerate = 1.01
            infectionrate = 2.38
            progression_time = 950
            print("the settings have been changed to match COVID-19's real values\n")
            menu()
        if choice == '13':
            healthy_colour = orange
            infected_colour = light_blue
            healthy_colour_hex = orange_hex
            infected_colour_hex = light_blue_hex
            print('colour blind mode has been activated; note healthy colour is now orange and infected colour is now light blue\n')
            menu()
    except Exception:
        print('please enter an integer value\n')

#creates a graph after the program is finished
def drawgraph():
    #plots the different lines for each of the cell count variables
    plt.plot(time_count , infected_count, infected_colour_hex, label = 'infected')
    plt.plot(time_count , healthy_count, healthy_colour_hex, label = 'healthy')
    plt.plot(time_count , immune_count, immune_colour_hex, label = 'immune')
    plt.plot(time_count , dead_count, color = black, label = 'dead')
    #labels the x and y axis
    plt.xlabel('time (in ticks)')
    plt.ylabel('number of cells')
    #titles the graph
    plt.title('graph of population against time')
    #creates a legend for the graph
    plt.legend()
    #shows the graph
    plt.show()

#calls the menu function
run_menu = True
while run_menu:
    menu()
pygame.quit()