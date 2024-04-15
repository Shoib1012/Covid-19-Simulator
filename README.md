# Covid-19-Simulator
My project that produces an abstracted simulation of the Covid-19 disease.

# How does the program work?
The project uses the Pymunk library as a physics engine for the cells.

The cells are initialised in a class, where the body of the cell is also initialised as attributes.

The cell class has methods that draw the cells, infect the cells, etc.

The number of cells at a time, t, is stored in an array for each cell type. This is used in the end to create the graph.

# What does the program do?
When you run the program, a menu comes up in the terminal. Here, you can change the parameters for the simulation.

The simulation has parameters for the starting number of infected cells, the incubation period, the immunity rate, the infection rate and the number of starting cells.

When the input '1' is entered, the simulation is started.

The simulation shows cells moving randomly. With each collision between an infected cell and a healthy cell, there is a chance of the infection spreading.

The simulation ends when there are no more infected cells.

At termination, a graph is displayed showing the population of the different cell types against time.
