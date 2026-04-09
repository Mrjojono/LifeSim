class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = f"cell_{x}_{y}"
        
        # Types: "EMPTY", "HEALTHY", "VIRUS", "CLEANER"
        self.type = "EMPTY"
        self.alive = False 

    def set_type(self, new_type):
        self.type = new_type
        self.alive = (new_type != "EMPTY")