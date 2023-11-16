import mesa
import time

class Box(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Pallet(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pilaDeCajas = 0

class Robots(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tiene_caja = None

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        new_position = self.random.choice(possible_steps)

        # Si tiene una caja, intenta moverse a una celda con un pallet
        while self.tiene_caja and self.model.grid.get_cell_list_contents([new_position]):
            if not isinstance(self.model.grid.get_cell_list_contents([new_position])[0], Pallet):
                new_position = self.random.choice(possible_steps)
            else:
                break

        self.model.grid.move_agent(self, new_position)


    def getBox(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if isinstance(other, Box):
                self.tiene_caja = other
                self.model.grid.remove_agent(other)

    def dropBox(self):
        if self.tiene_caja is not None:  # Si el robot está cargando una caja
            cellmates = self.model.grid.get_cell_list_contents([self.pos]) 
            for other in cellmates:
                if isinstance(other, Pallet):  # Si el agente es un pallet
                    other.pilaDeCajas += 1 
                    self.tiene_caja = None
                    self.model.cajas_en_pallets += 1
                    print(f"Faltan {self.model.boxes - self.model.cajas_en_pallets} cajas por apilar")
                    break 

    def step(self):
        self.move()
        self.getBox()
        self.dropBox()

class Almacen(mesa.Model):
    def __init__(self, width, height, boxes, robots, pallets):
        self.boxes = boxes
        self.robots = robots
        self.pallets = pallets
        self.cajas_en_pallets = 0
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.start_time = time.time()

        # Crear cajas
        for i in range(self.boxes):
            box = Box(i, self)
            self.schedule.add(box)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(box, (x, y))

        # Crear pallets
        for i in range(self.pallets):
            pallet = Pallet(i + self.boxes, self)
            self.schedule.add(pallet)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(pallet, (x, y))

        # Crear robots
        for i in range(self.robots):
            robot = Robots(i + self.pallets + self.boxes, self)
            self.schedule.add(robot)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(robot, (x,y))

    def step(self):
        # Verifica si todas las cajas están en algún pallet
        if self.cajas_en_pallets == self.boxes:
            self.running = False
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            print(f"Tiempo: {elapsed_time} segundos")
        else:
            self.schedule.step()
