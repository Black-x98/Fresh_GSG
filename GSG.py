#In loops, i iterator corresponds to y and j iterator corresponds to x.
from entities import entities
from agent import agent
from adversery import adv
from drone import drone
import g_var

from Tkinter import *
import random


#**************************************************************************************************

class app(Frame):

    global arrested_poachers, resource_poached, resource_recovered, distance_travelled, turn_gap_time


    def refresh(self):

        self.label_arrest['text'] = "CAUGHT Poachers:\n" + str(g_var.arrested_poachers)
        self.label_fled['text'] = "FLED Poachers:\n" + str(g_var.fled_poachers)
        self.label_sack['text'] = "Resource Poached:\n" + str(g_var.resource_poached)
        self.label_recovered['text'] = "Resource Recovered:\n" + str(g_var.resource_recovered)
        self.label_travelled['text'] = "Distance Travelled:\n" + str(g_var.distance_travelled)

        for i in range(g_var.dimension): # cell resource label update
            for j in range(g_var.dimension):
                res_label = Label(self.root,text = self.cell_resources[j][i],bg="black",fg="white")
                res_label.place(x=i*g_var.block_size+2,y=j*g_var.block_size+2)

        self.refresh_counter += 1

        if self.refresh_counter <= self.refresh_limit:
            self.root.after(g_var.turn_gap_time, self.refresh)
        elif self.refresh_counter > self.refresh_limit:
            print "Caught poachers: " + str(g_var.arrested_poachers), \
            ", Fled poachers: " + str(g_var.fled_poachers), \
            ", Resource poached: " + str(g_var.resource_poached), \
            ", Resource recovered: " + str(g_var.resource_recovered), \
            ", Distance travelled by agents: " + str(g_var.distance_travelled)
            self.root.destroy() # Destroys the Tkinter window for this execution

    def __init__(self, _num_adv, _num_agents, _num_drones):

        g_var.num_of_adverseries = _num_adv
        g_var.num_of_agents = _num_agents
        g_var.num_of_drones = _num_drones

        # re-initialization of result variables

        g_var.arrested_poachers = 0
        g_var.fled_poachers = 0
        g_var.resource_poached = 0
        g_var.resource_recovered = 0
        g_var.distance_travelled = 0

        self.refresh_counter = 0
        self.refresh_limit = 40

        print "\n***Simulating Green Security Game***\n"
        print "Parameters: adversaries: " + str(g_var.num_of_adverseries),\
        ", agents: " + str(g_var.num_of_agents),\
        ", drones: " + str(g_var.num_of_drones)

        self.root = Tk()
        self.root.title("Green Security Game")
        self.root.geometry('640x480+620+120')
        self.canvas = Canvas(self.root,bg="#333333",height=480,width=640)
        self.canvas.pack()
        Frame.__init__(self)

        self.agent_pos = [[0 for i in range(g_var.dimension)] for j in range(g_var.dimension)]
        #self.cell_resources = [[random.randint(10,50) for i in range(global_var.dimension)] for j in range(global_var.dimension)]
        self.adv_pos = [[0 for i in range(g_var.dimension)] for j in range(g_var.dimension)]
        self.drone_pos = [[0 for i in range(g_var.dimension)] for j in range(g_var.dimension)]
        self.drone_signal = [[0 for i in range(g_var.dimension)] for j in range(g_var.dimension)]
        self.target_pos = []
        self.round_marking = []
        self.cell_resources =  [[4,9,6,7,0,2,1,6,7,0],
                               [13,50,0,0,50,0,50,0,0,21],
                               [14,0,19,13,24,23,36,17,0,11],
                               [17,50,40,10,50,50,50,6,0,6],
                               [10,31,20,13,50,0,0,10,50,3],
                               [9,34,30,10,50,50,50,10,0,5],
                               [11,37,10,22,17,15,12,10,0,6],
                               [13,0,50,14,33,17,50,32,26,11],
                               [7,0,0,50,0,0,0,50,13,23],
                               [11,12,31,10,9,8,11,13,14,21]]

        for i in range(g_var.dimension):
            for j in range(g_var.dimension):
                if self.cell_resources[i][j] > 0:
                    self.target_pos.append((i,j))
                if self.cell_resources[i][j] == -1:
                    self.round_marking.append((i,j))
        self.round_marking.append((5,5)) # temporary dummy

        self.cell_coord = [[i.__str__() + "," + j.__str__() for i in range(g_var.dimension)] for j in range(g_var.dimension)]


        self.label_poacher_num = Label(self.root,text = "Number of Total \nPoachers:\n" + str(g_var.num_of_adverseries))
        self.label_poacher_num.place(relx=0.78, rely=0.05)

        self.label_arrest = Label(self.root,text = g_var.arrested_poachers)
        self.label_arrest.place(relx=0.78, rely=0.2)
        self.label_fled = Label(self.root,text = g_var.fled_poachers)
        self.label_fled.place(relx=0.78, rely=0.3)
        self.label_sack = Label(self.root,text = g_var.resource_poached)
        self.label_sack.place(relx=0.78, rely=0.4)
        self.label_recovered = Label(self.root,text = g_var.resource_poached)
        self.label_recovered.place(relx=0.78, rely=0.5)
        self.label_travelled = Label(self.root,text = g_var.distance_travelled)
        self.label_travelled.place(relx=0.78, rely=0.6)

        self.label_agent_num = Label(self.root,text = "Number of Agents:\n" + str(g_var.num_of_agents))
        self.label_agent_num.place(relx=0.78, rely=0.7)
        self.label_drone_num = Label(self.root,text = "Number of Drones:\n" + str(g_var.num_of_drones))
        self.label_drone_num.place(relx=0.78, rely=0.8)


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

        for i in range(g_var.num_of_agents):
            agent_obj = agent(self.canvas,self.root,self.agent_pos,self.cell_resources,self.target_pos,self.round_marking,self.drone_signal)
            agent_obj.move_spec_guard()

        for i in range(g_var.num_of_drones):
            drone_obj = drone(self.canvas,self.root,self.drone_pos,self.drone_signal,self.adv_pos)
            drone_obj.move_drone()

        for i in range(g_var.num_of_adverseries):
            adv_obj = adv(self.canvas,self.root,self.agent_pos,self.drone_pos,self.cell_resources,self.target_pos,self.adv_pos)
            adv_obj.operate_adv()

        self.root.mainloop()

for i in range(1,8):
    app(10,i,8) # parameters: num of adversaries, agents, drones
