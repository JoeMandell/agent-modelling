from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from model import Schelling

class HappyElement(TextElement):
    def __init__(self):
        pass
    
    def render(self, model):
        return "Happy agents: " + str(model.happy)

def schelling_draw(agent):

    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0} 

    if agent.type == 0:
        portrayal