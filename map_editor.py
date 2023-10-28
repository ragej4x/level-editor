import csv
import shutil
import os
import json
from datetime import datetime
import pygame as pg
pg.init()
with open('data/file.json', 'r') as data:
    file = json.load(data)
font = file['font']
map_L0 = file['map_layer_0']
map_L1 = file['map_layer_1']
map_L2 = file['map_layer_2']



class editor_class():
    def __init__(self):
        import pygame as pg
        dt = datetime.now()
        self.date_time = dt.strftime("%d %m %Y : %H %M")

        self.zoom = 3
        self.world_data = []
        self.max_col = 80
        self.rows = 80
        self.height = 620
        self.width = 900
        self.tile_size = self.height // self.rows + self.zoom
        self.tile = 0

        self.button_columns = 9
        self.button_rows = 14
        self.button_width = 16
        self.button_hight = 16
        self.buttons = []
        self.select = True

        #LOAD IMAGE
        self.item_list = []
        self.item_count = 135

        self.scroll = 1

        for i in range(1,self.item_count):
            self.small_items = pg.image.load(f"data/map/texture/tile- ({i}).png")
            self.small_items = pg.transform.scale(self.small_items, (self.tile_size, self.tile_size))
            self.item_list.append(self.small_items)


        self.small_items_surface = pg.Surface((16, 16))

        for row in range(self.rows):
            r = [78] * self.max_col
            self.world_data.append(r)

        #print(self.world_data)



        for row in range(self.button_rows):
            for col in range(self.button_columns):
                x = col * (self.tile_size) + self.rows * self.tile_size
                y = row * (self.tile_size)
                text = f"Button {row * self.button_columns + col + 1}"

                #draw_button(x , y , self.tile_size, self.tile_size, text)
                self.buttons.append({"rect": pg.Rect(x, y, self.tile_size, self.tile_size), "text":text, "item":row * self.button_columns + col + 1, "posx":x, "posy":y} )


    def draw_tile(self, display, keyinput, mx , my, mouseinput):
        #def draw_button(vx, vy, width, height, text):
            #button_rect = pg.draw.rect(display, (255,255,255), (vx, vy, width, height), 2)


        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 1:
                    display.blit(self.item_list[tile], (x * self.tile_size, y * self.tile_size))
                    #display.blit(self.small_items_surface, (x * self.tile_size ,y * self.tile_size))
        #draw tilesets
        #if keyinput[pg.K_RIGHT]:
        for button in self.buttons:
            if button["rect"].collidepoint(mx , my):
                self.select = True
                if mouseinput[0]:
                    self.tile = button['item']


        for button in self.buttons:

            #print(button["item"])
            display.blit(self.item_list[button["item"]], (button["posx"], button["posy"]))



    def draw_grid(self,display):
        #vertical lines
        for c in range(self.max_col + 1):
            pg.draw.line(display, (255,255,255), (c * self.tile_size, 0 ), (c * self.tile_size , self.height ))
        #horizontal lines
        for c in range(self.rows + 1):
            pg.draw.line(display, (255,255,255), (0, c * self.tile_size ), (self.width , c * self.tile_size ))

        #LOAD THE MAPS
        if keyinput[pg.K_1]:
            with open(f"data/map/layer_data_{int(self.scroll)}.data", newline='') as data:
                reader = csv.reader(data, delimiter = ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_data[x][y] = int(tile)


        if keyinput[pg.K_2]:
            with open(f"data/map/layer_data_{int(self.scroll)}.data", newline='') as data:
                reader = csv.reader(data, delimiter = ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                            self.world_data[x][y] = int(tile)

        if keyinput[pg.K_3]:
            with open(f"data/map/layer_data_{int(self.scroll)}.data", newline='') as data:
                reader = csv.reader(data, delimiter = ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                            self.world_data[x][y] = int(tile)
        if keyinput[pg.K_4]:
            with open(f"data/map/layer_map_{int(self.scroll)}.data", newline='') as data:
                reader = csv.reader(data, delimiter = ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                            self.world_data[x][y] = int(tile)


    def update(self,mx, my, mouseinput, keyinput, display):
        if keyinput[pg.K_1]:
            self.scroll = 1
        if keyinput[pg.K_2]:
            self.scroll = 2
        if keyinput[pg.K_3]:
            self.scroll = 3
        if keyinput[pg.K_4]:
            self.scroll = 4


        #CHECK COORD
        x = int(mx )// self.tile_size
        y = int(my )// self.tile_size


        if mx < self.width and my < self.height and mx < 790:
            if mouseinput[0]:
                if self.world_data[y][x] != self.tile:
                    self.world_data[y][x] = self.tile
                    #print(self.world_data[y][x])
            if mouseinput[2]:
                self.world_data[y][x] = 0


        #SAVE DATA
        #print(x,y)

        if keyinput[pg.K_p]:
            #shutil.copyfile(colData, f"data/backup/map_1_backup : {self.date_time}.data")
            #print("SAVED")
            print(self.world_data)
            with open(f"data/map/layer_data_{int(self.scroll)}.data", "w", newline="") as file:
                writer = csv.writer(file, delimiter = ",")
                for row in self.world_data:
                    writer.writerow(row)
            #Fail Load data

        #LOAD DATA
        if keyinput[pg.K_o] :
            with open(colData, newline='') as data:
                reader = csv.reader(data, delimiter = ",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        self.world_data[x][y] = int(tile)




main = editor_class()


display = pg.display.set_mode((1000,700))


while True:
    display.fill(0)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    mx , my = pg.mouse.get_pos()
    keyinput = pg.key.get_pressed()
    mouseinput = pg.mouse.get_pressed()

    main.update(mx, my, mouseinput, keyinput, display)
    main.draw_grid(display)
    main.draw_tile(display, keyinput, mx , my, mouseinput)

    print(mx)

    pg.display.update()
