# Covid-19-Simulator
My project that produces an abstracted simulation of the Covid-19 disease.

#How does the program work?
The project uses the Pymunk library as a physics engine for the cells.

The cells are initialised as a class with their state as an enumeration.

# What does the program do?
When you run the program, a menu comes up in the terminal. Here, you can change the parameters for the simulation.

The simulation has parameters for the starting number of infected cells, the incubation period, the immunity rate, the infection rate and the number of starting cells.

When the input '1' is entered, the simulation is started.

The simulation shows cells moving randomly. With each collision between an infected cell and a healthy cell, there is a chance of the infection spreading.

The simulation ends when there are no more infected cells.

At termination, a graph is displayed showing the population of the different cell types against time.
