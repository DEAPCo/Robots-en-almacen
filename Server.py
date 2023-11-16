import mesa
from Robots import *

def agent_portrayal(agent):
    if isinstance(agent, Box):  #Cajas
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "blue",
                     "w": 0.9,
                     "h": 0.9}
    elif isinstance(agent, Pallet):  #Pallets
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "green",
                     "w": 0.9,
                     "h": 0.9}
    elif isinstance(agent, Robots):  #Robots
        if agent.tiene_caja is None:    #Sin caja
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "red",
                         "r": 0.5}
        else:   #Con caja
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "yellow",
                         "r": 0.5}
    else:
        portrayal = {}
    return portrayal

grid = mesa.visualization.CanvasGrid(
    agent_portrayal,
    10,10,500,500
)

server = mesa.visualization.ModularServer(
    Almacen,
    [grid],
    "Almacen",
    {"width":10, "height":10, "boxes":20, "robots":5, "pallets":5}
)

server.port = 8521
server.launch()

