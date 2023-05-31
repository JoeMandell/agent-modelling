import mesa

class SchellingAgent(Agent):
    #initialize with needed variables - 
    #extends Agent class from Mesa - https://buildmedia.readthedocs.org/media/pdf/mesa/latest/mesa.pdf
    def __init__(self, pos, model, agent_type):
        super().__init__(pos,model) #calls the constructor for the mesa agent class, using pos as the unique_id
        self.pos = pos
        self.type = agent_type
    
    #define the step function - this is what triggers for each generation
    def step(self):
        similar = 0
        #calculate the number of similar neighbors in current generation
        for neighbor in self.model.grid.neighbor_iter(self.pos): #loops through neighbors
            if neighbor.type ==self.type: #checks if they are the same type 
                similar += 1

        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1 #if the agent has enough similar neighbors, it gets happier


class Schelling(Model):
    def __init__(height,width,density,minority_fraction,homophily):
        self.height = height
        self.width = width
        self.density = density
        self.minority_fraction = minority_fraction
        self.homophily = homophily

        from mesa.space import SingleGrid
        self.grid = SingleGrid(height,width,torus = true)

        from mesa.time import RandomActivation
        self.schedule = RandomActivation(self)

        from mesa.datacollection import DataCollector
        self.happy = 0
        self.datacollector = DataCollector({"happy":"happy"}, {"x":lambda a: a.pos[0], "y": lambda a: a.pos[1]})

        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_fraction:
                    agent_type = 1
                else:
                    agent_type = 0
                agent = SchellingAgent((x,y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.happy = 0
        self.schedule.step()

        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
    
