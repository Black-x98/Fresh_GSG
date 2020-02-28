import random
from entities import entities
import g_var

class adv(entities):

    adv_move_counter = 0
    adv_color = "red"

    def __init__(self,_canvas,_root, _agent_pos, _drone_pos, _cell_resources, _target_pos):

        self.canvas = _canvas
        self.root = _root
        self.agent_pos = _agent_pos
        self.drone_pos = _drone_pos
        self.cell_resources = _cell_resources
        self.target_pos = _target_pos
        self.my_target = _target_pos[random.randint(0,len(_target_pos)-1)]
        print "my target : " + str(self.my_target)
        self.flag = 0
        self.escape_x = 0
        self.escape_y = 0
        # 0 means target destination hasn't been reached
        # 1 means target reached and poaching is going on
        # 2 means poching done now leaving area
        self.sack = 0
        self.sack_limit = 10

        set = {0, g_var.dimension - 1}
        if random.randint(0,1)==0:
            self.cur_x_adv = random.sample(set,1)[0]
            self.cur_y_adv = random.randint(0, g_var.dimension - 1)
        else:
            self.cur_y_adv = random.sample(set,1)[0]
            self.cur_x_adv = random.randint(0, g_var.dimension - 1)

        x_cor = self.cur_x_adv * g_var.block_size
        y_cor = self.cur_y_adv * g_var.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+38,x_cor+35,y_cor+38,x_cor+25,y_cor+19,fill=self.adv_color)
        print "Initiated poacher at position: " + self.cur_y_adv.__str__() + "," + self.cur_x_adv.__str__()

    def move_adv(self):
        x_cor = self.cur_x_adv * g_var.block_size
        y_cor = self.cur_y_adv * g_var.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+38,x_cor+35,y_cor+38,x_cor+25,y_cor+19,fill=g_var.bg_color,outline=g_var.bg_color)

        x_offset = self.my_target[1] - self.cur_x_adv
        y_offset = self.my_target[0] - self.cur_y_adv

        if x_offset == 0 and y_offset == 0:
            self.flag = 1

        move_x, move_y = 0,0
        if x_offset>0 and self.cur_x_adv<g_var.dimension-1: move_x = +1
        elif x_offset<0 and self.cur_x_adv>0 : move_x=-1
        if y_offset>0 and self.cur_y_adv<g_var.dimension-1: move_y = +1
        elif y_offset<0 and self.cur_y_adv>0 : move_y=-1

        self.cur_x_adv += move_x
        self.cur_y_adv += move_y

        if self.cur_x_adv>g_var.dimension-1 or self.cur_y_adv>g_var.dimension-1: # invalid move check!!!
            print "AFTER: The cur_x_adv and cur_y_adv is: " + self.cur_x_adv.__str__() + " and " + self.cur_y_adv.__str__()

    def poach(self):
        if self.drone_pos[self.cur_x_adv][self.cur_y_adv] == 1:
            print "Oh no! Drone!!!"
            self.flag = 3
            
        if self.sack < self.sack_limit and self.cell_resources[self.cur_y_adv][self.cur_x_adv]>0:  # resource value update
            self.sack += 1
            g_var.resource_poached += 1
            self.cell_resources[self.cur_y_adv][self.cur_x_adv] -= 1
        if self.sack >= self.sack_limit:
            self.flag = 2

    def fix_escape_point(self):
        up_end = self.cur_y_adv
        down_end = g_var.dimension - 1 - self.cur_y_adv
        right_end = g_var.dimension - 1 - self.cur_x_adv
        left_end = self.cur_x_adv
        self.escape_x = 0
        self.escape_y = 0
        self.small_x = 0
        self.small_y = 0
        if up_end <= down_end:
            self.escape_y = 0
            self.small_y = up_end
        else:
            self.escape_y = g_var.dimension - 1
            self.small_y = down_end
        if left_end <= right_end :
            self.escape_x = 0
            self.small_x = left_end
        else:
            self.escape_x = g_var.dimension - 1
            self.small_x = right_end

        if self.small_x <= self.small_y:
            self.escape_x = 0
            self.escape_y = self.cur_y_adv
        else:
            self.escape_x = self.cur_x_adv
            self.escape_y = 0
        self.flag = 3

    def flee_adv(self):
        #print "So the escape coordinate is " + self.escape_x.__str__() + " " + self.escape_y.__str__()
        x_cor = self.cur_x_adv * g_var.block_size
        y_cor = self.cur_y_adv * g_var.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+38,x_cor+35,y_cor+38,x_cor+25,y_cor+19,fill=g_var.bg_color,outline=g_var.bg_color)

        x_offset = self.escape_x - self.cur_x_adv
        y_offset = self.escape_y - self.cur_y_adv

        if x_offset == 0 and y_offset == 0:
            self.flag = 4

        move_x, move_y = 0,0
        if x_offset>0 and self.cur_x_adv<g_var.dimension-1: move_x = +1
        elif x_offset<0 and self.cur_x_adv>0 : move_x=-1
        if y_offset>0 and self.cur_y_adv<g_var.dimension-1: move_y = +1
        elif y_offset<0 and self.cur_y_adv>0 : move_y=-1

        self.cur_x_adv += move_x
        self.cur_y_adv += move_y

        if self.cur_x_adv>g_var.dimension-1 or self.cur_y_adv>g_var.dimension-1: # invalid move check!!!
            print "AFTER: The cur_x_adv and cur_y_adv is: " + self.cur_x_adv.__str__() + " and " + self.cur_y_adv.__str__()


    def escape(self):
        x_cor = self.cur_x_adv * g_var.block_size
        y_cor = self.cur_y_adv * g_var.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+38,x_cor+35,y_cor+38,x_cor+25,y_cor+19,fill=g_var.bg_color,outline="yellow")
        self.flag = 6


    def operate_adv(self):
        #print "Operating ehh?"
        self.adv_move_counter += 1
        if self.flag == 0 or self.flag == 5:
            self.move_adv()
        if self.flag == 1:
            self.poach()
        if self.flag == 2:
            self.fix_escape_point()
        if self.flag == 3:
            self.flee_adv()
        if self.flag == 4:
            self.escape()
        if self.flag == 6:
            print "The poacher successfully escaped!!!"
            del self

        elif self.agent_pos[self.cur_x_adv][self.cur_y_adv] == 1: # The End sir!!!

            x_cor = self.cur_x_adv * g_var.block_size
            y_cor = self.cur_y_adv * g_var.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+10,x_cor+15,y_cor+25,x_cor+30,y_cor+25,x_cor+30,y_cor+10,fill="white")
            # actually j correspond to x and i correspoond to y
            print "Poacher caught at the position: **" + self.cur_y_adv.__str__() + "*" + self.cur_x_adv.__str__() + "***"
            self.canvas.create_polygon(x_cor+15,y_cor+38,x_cor+35,y_cor+38,x_cor+25,y_cor+19,fill=g_var.bg_color,outline=g_var.bg_color)
            global arrested_poachers, resource_recovered
            g_var.arrested_poachers += 1
            g_var.resource_poached -= self.sack
            g_var.resource_recovered += self.sack
            print "arrested_poachers updated"
            print g_var.arrested_poachers
            del self

        else:
            x_cor = self.cur_x_adv * g_var.block_size
            y_cor = self.cur_y_adv * g_var.block_size
            self.canvas.create_polygon(x_cor+15,y_cor+38,x_cor+35,y_cor+38,x_cor+25,y_cor+19,fill=self.adv_color)
            if self.adv_move_counter < g_var.movement_limit:
                self.root.after(g_var.turn_gap_time, self.operate_adv)
