#In loops, i iterator corresponds to y and j iterator corresponds to x.
from entities import entities
from agent import agent
from adversery import adv
from drone import drone
import g_var

from Tkinter import *
import random

#********************************************************************************************


class spec_guard(entities):

    spec_guard_move_counter = 0


    def __init__(self,_canvas,_root, _agent_pos, _drone_pos, _cell_resources, _target_pos):
        self.spec_guard_color = "blue"
        self.canvas = _canvas
        self.root = _root
        self.agent_pos = _agent_pos
        self.drone_pos = _drone_pos
        self.cell_resources = _cell_resources
        self.target_pos = _target_pos
        self.my_target = _target_pos[random.randint(0,len(_target_pos)-1)]
        print "my target : " + str(self.my_target)
        self.flag = 0

        self.sack = 0
        self.sack_limit = 10
        self.spec_guard_counter = 0
        temp = self.target_pos[random.randint(0,len(self.target_pos)-1)]
        self.cur_x_spec_guard = temp[1]
        self.cur_y_spec_guard = temp[0]

        x_cor = self.cur_x_spec_guard * g_var.block_size
        y_cor = self.cur_y_spec_guard * g_var.block_size
        print "Initiated poacher at position: " + self.cur_y_spec_guard.__str__() + "," + self.cur_x_spec_guard.__str__()

    def move_spec_guard(self):
        print "inside move_spec**************"
        x_cor = self.cur_x_spec_guard * g_var.block_size
        y_cor = self.cur_y_spec_guard * g_var.block_size
        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=g_var.bg_color,outline=g_var.bg_color)
        self.agent_pos[self.cur_x_spec_guard][self.cur_y_spec_guard] = 0

        offset_y = self.my_target[0] - self.cur_y_spec_guard
        offset_x = self.my_target[1] - self.cur_x_spec_guard

        if offset_x==0 and offset_y==0:
            temp = self.target_pos[random.randint(0,len(self.target_pos)-1)]
            self.my_target= temp
            #self.my_target[0] = temp[0]
        move_x = 0
        move_y = 0
        if offset_x>0:
            move_x = 1
        elif offset_x<0:
            move_x = -1
        if offset_y>0:
            move_y = 1
        elif offset_y<0:
            move_y = -1

        self.cur_x_spec_guard = self.cur_x_spec_guard + move_x
        self.cur_y_spec_guard = self.cur_y_spec_guard + move_y
        x_cor = self.cur_x_spec_guard * g_var.block_size
        y_cor = self.cur_y_spec_guard * g_var.block_size

        self.canvas.create_polygon(x_cor+15,y_cor+20,x_cor+15,y_cor+35,x_cor+30,y_cor+35,x_cor+30,y_cor+20,fill=self.spec_guard_color)
        self.agent_pos[self.cur_x_spec_guard][self.cur_y_spec_guard] = 1

        self.spec_guard_counter += 1
        if move_x != 0 or move_y != 0:
            g_var.distance_travelled += 1

        if self.spec_guard_counter < g_var.movement_limit:
            self.root.after(g_var.turn_gap_time, self.move_spec_guard)






#**************************************************************************************************
class app(Frame):

    global  arrested_poachers, resource_poached, resource_recovered, distance_travelled, turn_gap_time

    def refresh(self):

        self.label_arrest['text'] = "CAUGHT Poachers:\n" + str(g_var.arrested_poachers)
        self.label_sack['text'] = "Resource Poached:\n" + str(g_var.resource_poached)
        self.label_recovered['text'] = "Resource Recovered:\n" + str(g_var.resource_recovered)
        self.label_travelled['text'] = "Distance Travelled:\n" + str(g_var.distance_travelled)

        for i in range(g_var.dimension): # cell resource label update
            for j in range(g_var.dimension):
                res_label = Label(self.root,text = self.cell_resources[j][i],bg="black",fg="white")
                res_label.place(x=i*g_var.block_size+2,y=j*g_var.block_size+2)

        self.root.after(g_var.turn_gap_time, self.refresh)

    def __init__(self):

        self.root = Tk()
        self.root.title("Green Security Game")
        self.root.geometry('640x480+220+120')
        self.canvas = Canvas(self.root,bg="#333333",height=480,width=640)
        self.canvas.pack()
        Frame.__init__(self)

        self.agent_pos = [[0 for i in range(g_var.dimension)] for j in range(g_var.dimension)]
        #self.cell_resources = [[random.randint(10,50) for i in range(global_var.dimension)] for j in range(global_var.dimension)]
        self.drone_pos = [[0 for i in range(g_var.dimension)] for j in range(g_var.dimension)]
        self.target_pos = []
        self.round_marking = []
        self.cell_resources =  [[0,0,0,0,0,0,0,0,0,0],
                               [0,50,0,0,50,0,50,0,0,0],
                               [0,0,0,0,-1,-1,-1,0,0,0],
                               [0,50,0,-1,50,50,50,-1,0,0],
                               [0,0,0,-1,50,0,0,-1,50,0],
                               [0,0,0,-1,50,50,50,-1,0,0],
                               [0,0,0,0,-1,-1,-1,-1,0,0],
                               [0,0,50,0,0,0,50,0,0,0],
                               [0,0,0,50,0,0,0,0,0,0],
                               [0,0,0,0,0,0,0,0,0,0]]

        for i in range(g_var.dimension):
            for j in range(g_var.dimension):
                if self.cell_resources[i][j] == 50:
                    self.target_pos.append((i,j))
                if self.cell_resources[i][j] == -1:
                    self.round_marking.append((i,j))

        print "so, round marking is: "
        print self.round_marking
        print len(self.round_marking)

        self.cell_coord = [[i.__str__() + "," + j.__str__() for i in range(g_var.dimension)] for j in range(g_var.dimension)]


        self.label_poacher_num = Label(self.root,text = "Number of Total \nPoachers:\n" + str(g_var.num_of_adverseries))
        self.label_poacher_num.place(relx=0.78, rely=0.15)
        self.label_agent_num = Label(self.root,text = "Number of Agents:\n" + str(g_var.num_of_agents))
        self.label_agent_num.place(relx=0.78, rely=0.3)
        self.label_drone_num = Label(self.root,text = "Number of Drones:\n" + str(g_var.num_of_drones))
        self.label_drone_num.place(relx=0.78, rely=0.4)

        self.label_arrest = Label(self.root,text = g_var.arrested_poachers)
        self.label_arrest.place(relx=0.78, rely=0.5)
        self.label_sack = Label(self.root,text = g_var.resource_poached)
        self.label_sack.place(relx=0.78, rely=0.6)
        self.label_recovered = Label(self.root,text = g_var.resource_poached)
        self.label_recovered.place(relx=0.78, rely=0.7)
        self.label_travelled = Label(self.root,text = g_var.distance_travelled)
        self.label_travelled.place(relx=0.78, rely=0.8)

        self.refresh()
        self.canvas.create_rectangle(0, 0, g_var.dimension * g_var.block_size, g_var.dimension * g_var.block_size, fill=g_var.bg_color)

        # for ONE TIME labelling *******************************************
        for i in range(g_var.dimension):
            for j in range(g_var.dimension):
                self.coord_label = Label(self.root,text = self.cell_coord[i][j],bg="black",fg="white")
                self.coord_label.place(x=i*g_var.block_size+2,y=j*g_var.block_size+18)

        for i in range(g_var.dimension + 1):
            for j in range(g_var.dimension + 1):
                self.canvas.create_rectangle(i*g_var.block_size,j*g_var.block_size,g_var.block_size,g_var.block_size,outline="grey")

        for i in range(0):
            agent_obj = agent(self.canvas,self.root,self.agent_pos,self.cell_resources,self.round_marking)
            agent_obj.move_agent()

        for i in range(5):
            spec_guard_obj = spec_guard(self.canvas,self.root,self.agent_pos,self.cell_resources,self.round_marking,self.target_pos)
            spec_guard_obj.move_spec_guard()
        '''
        for i in range(g_var.num_of_drones):
            drone_obj = drone(self.canvas,self.root,self.drone_pos)
            drone_obj.move_drone()'''

        for i in range(10):
            adv_obj = adv(self.canvas,self.root,self.agent_pos,self.drone_pos,self.cell_resources,self.target_pos)
            adv_obj.operate_adv()

        self.root.mainloop()

app()
