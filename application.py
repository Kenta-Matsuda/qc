import tkinter as tk
import gate_calculator
import numpy as np
import sympy as sp
import datetime
import os
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import visualizer
import pyautogui
from matplotlib import rc
from screeninfo import get_monitors

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        #rc('text', usetex=True)
        self.gc = gate_calculator.GateCalculator()
        
        self.date=datetime.datetime.now() 

        self.address=os.environ['USERPROFILE']+'\\desktop\\QuantumCircuit\\'+self.date.strftime('%Y')+str('_')+self.date.strftime('%m')+str('_')+self.date.strftime('%d')+str('___')+self.date.strftime('%H')+str('_')+self.date.strftime('%M')+str('_')+self.date.strftime('%S')
        os.makedirs(self.address, exist_ok=True)

        ##################################################
        ###################<Window>#######################
        
        monitors = get_monitors()
        for m in range(len(monitors)):
            if monitors[m].is_primary==True:
                monitor = monitors[m]
        self.dpi_x = monitor.width/monitor.width_mm
        self.dpi_y = monitor.height/monitor.height_mm
        
        #size of window
        self.window_width = int(monitor.width * 0.8)
        self.window_height = int(monitor.height * 0.8)
        #display position coordinates of window
        self.window_margin_width = int(monitor.width * 0.1)
        self.window_margin_height = int(monitor.height * 0.1)
        #display window
        master.geometry(str(self.window_width)+"x"+str(self.window_height)+"+"+str(self.window_margin_width)+"+"+str(self.window_margin_height))
        #title setting
        master.title("QCS    ( Quantum Circuit Simulator )")
        #icon setting
        master.iconbitmap("pic\icon\icon.ico")
        #background color setting
        master["bg"] = "grey"
        #size of popup window
        self.popup_window_width = 400
        self.popup_window_height = 300
        #display position coordinates of popup window
        self.popup_margin_width = int((monitor.width - self.popup_window_width)/2)
        self.popup_margin_height = int((monitor.height - self.popup_window_height)/2)
        #display position coordinates of gates
        self.init_size = 50 #50px × 50px
        self.popup_margin_side = (self.popup_window_width - self.init_size*6)/7
        # self.popup_margin_top = self.popup_window_height/6 - self.init_size/2
        self.popup_margin_top = (self.popup_window_height - self.init_size*2)/3

        self.popup_place_w1 = self.popup_margin_side + self.init_size/2
        self.popup_place_w2 = self.popup_place_w1 + self.popup_margin_side + self.init_size
        self.popup_place_w3 = self.popup_place_w2 + self.popup_margin_side + self.init_size
        self.popup_place_w4 = self.popup_place_w3 + self.popup_margin_side + self.init_size
        self.popup_place_w5 = self.popup_place_w4 + self.popup_margin_side + self.init_size
        self.popup_place_w6 = self.popup_place_w5 + self.popup_margin_side + self.init_size
        self.popup_place_h1 = self.popup_margin_top + self.init_size/2
        # self.popup_place_h2 = self.popup_place_h1 + self.init_size + self.popup_margin_top*2
        # self.popup_place_h3 = self.popup_place_h2 + self.init_size + self.popup_margin_top*2
        self.popup_place_h3 = self.popup_place_h1 + self.init_size + self.popup_margin_top

        ##################################################
        
        
        ##################################################
        #################<circuit canvas>#################
        #size of circuit part
        self.circuit_width = self.window_width*0.85
        self.circuit_height = self.window_height*0.65
        #size of gate part
        self.gate_width = self.window_width - self.circuit_width
        self.gate_height = self.circuit_height
        #the number of composer bar(N qubit)
        self.qbar_number = 3
        #size of composer bar
        self.qbar_width = self.circuit_width*0.75
        self.qbar_wide = 5
        #display position coordinates of composer 
        self.qbar_margin_width = (self.circuit_width - self.qbar_width)*0.75
        self.qbar_margin_height = self.circuit_height/self.qbar_number
        
        #gate information
        self.gate_size = 50 #50px × 50px
        self.circle_radius = 3
        self.gate_valid_area = self.gate_size*0.6
        self.gate_column = int((self.qbar_width-self.gate_size/2)/(self.gate_size*1.5))  
        
        #display position coordinates of gates
        self.gate_margin_top = self.gate_height/6
        self.gate_margin_side = self.gate_width*0.25
        self.place_c1 = self.circuit_width
        self.place_c2 = self.circuit_width + self.gate_margin_side
        self.place_c3 = self.circuit_width + self.gate_margin_side*2
        self.place_c4 = self.circuit_width + self.gate_margin_side*3
        self.place_r1 = self.gate_margin_top
        self.place_r2 = self.gate_margin_top*3
        self.place_r3 = self.gate_margin_top*5
        #display canvas
        self.canvas_circuit= tk.Canvas(
            master, 
            width = self.gate_width + self.circuit_width, 
            height = self.circuit_height,
            bg = "grey")
        self.canvas_circuit.place(x=0, y=0)
        #Images about quantum gates
        self.img_h = tk.PhotoImage(file="pic\\gate\\h.png")
        self.img_x = tk.PhotoImage(file="pic\\gate\\x.png")
        self.img_y = tk.PhotoImage(file="pic\\gate\\y.png")
        self.img_z = tk.PhotoImage(file="pic\\gate\\z.png")
        self.img_s = tk.PhotoImage(file="pic\\gate\\s.png")
        self.img_t = tk.PhotoImage(file="pic\\gate\\t.png")
        self.img_sd = tk.PhotoImage(file="pic\\gate\\sd.png")
        self.img_td = tk.PhotoImage(file="pic\\gate\\td.png")
        self.img_p = tk.PhotoImage(file="pic\\gate\\p.png")
        self.img_c = tk.PhotoImage(file="pic\\gate\\control.png")
        self.img_m = tk.PhotoImage(file="pic\\gate\\measure.png")        
        #Images about composer controllers
        self.img_pb = tk.PhotoImage(file="pic\\button\\plus_before.png")
        self.img_pa = tk.PhotoImage(file="pic\\button\\plus_after.png")
        self.img_mb = tk.PhotoImage(file="pic\\button\\minus_before.png")
        self.img_ma = tk.PhotoImage(file="pic\\button\\minus_after.png")
        self.img_db = tk.PhotoImage(file="pic\\button\\download.png")
        self.img_da = tk.PhotoImage(file="pic\\button\\download_after.png")

        #Image about initial value
        self.img_psi = tk.PhotoImage(file="pic\\initial_value\\initial_value.png")
        self.img_psi_after = tk.PhotoImage(file="pic\\initial_value\\initial_value_after.png")
        self.img_ket0 = tk.PhotoImage(file="pic\\initial_value\\ket0.png")
        self.img_ket1 = tk.PhotoImage(file="pic\\initial_value\\ket1.png")
        self.img_ketp = tk.PhotoImage(file="pic\\initial_value\\ketp.png")
        self.img_ketm = tk.PhotoImage(file="pic\\initial_value\\ketm.png")
        self.img_keta = tk.PhotoImage(file="pic\\initial_value\\keta.png")  #Anticlockwise
        self.img_ketc = tk.PhotoImage(file="pic\\initial_value\\ketc.png")  #Clockwise
        self.img_ket0_red = tk.PhotoImage(file="pic\\initial_value\\ket0_after.png")
        self.img_ket1_red = tk.PhotoImage(file="pic\\initial_value\\ket1_after.png")
        self.img_ketp_red = tk.PhotoImage(file="pic\\initial_value\\ketp_after.png")
        self.img_ketm_red = tk.PhotoImage(file="pic\\initial_value\\ketm_after.png")
        self.img_keta_red = tk.PhotoImage(file="pic\\initial_value\\keta_after.png")  #Anticlockwise
        self.img_ketc_red = tk.PhotoImage(file="pic\\initial_value\\ketc_after.png")  #Clockwise
        self.img_confirm = tk.PhotoImage(file="pic\\initial_value\\confirm.png")
        
        #display images about composer controllers
        self.button_size = 50  #50px x 50px
        self.button_x1 = 30
        self.button_x2 = self.button_x1 + self.button_size
        self.button_x3 = self.button_x1 + self.button_size*2
        self.button_y = self.circuit_height-30
        self.pb = self.canvas_circuit.create_image(self.button_x1, self.button_y, image=self.img_pb)
        self.mb = self.canvas_circuit.create_image(self.button_x2, self.button_y, image=self.img_mb)
        self.db = self.canvas_circuit.create_image(self.button_x3, self.button_y,image=self.img_db)
        #press events
        self.canvas_circuit.tag_bind(self.pb, "<Enter>", self.enter_p)
        self.canvas_circuit.tag_bind(self.mb, "<Enter>", self.enter_m)
        self.canvas_circuit.tag_bind(self.db, "<Enter>", self.enter_d)
        self.create_qbar()

        #display images about quantum gates
        
        self.create_init_gate()

        ##################################################
        
        
        ##################################################
        #################<result canvas>##################
        #size of result part
        self.result_width = self.window_width*0.7
        self.result_height = self.window_height - self.circuit_height
        #display position coordinates of result part
        self.result_x = self.result_width*0.1
        self.result_y = self.result_height*0.3
        #display canvas
        self.canvas_result= tk.Canvas(
            master,
            width = self.result_width,
            height = self.result_height,
            bg = "green")
        self.canvas_result.place(x=0, y=self.gate_height)

        mm_to_inch = 1/24.8
        self.fig_result = Figure(figsize=(self.result_width*(mm_to_inch/self.dpi_x),self.result_height*(mm_to_inch/self.dpi_y)))
        self.ax_result = self.fig_result.add_subplot(111)

        self.canvas_answer = FigureCanvasTkAgg(self.fig_result, self.canvas_result)
        self.canvas_answer.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH, expand=1)


        #result of calculation
        self.display_result()

        ##################################################
        
        
        ##################################################
        #################<visual canvas>##################
        #size of sphere part
        self.sphere_width = self.window_width - self.result_width
        self.sphere_height = self.window_height - self.circuit_height
        #display canvas
        self.canvas_sphere= tk.Canvas(
            master,
            width = self.sphere_width,
            height = self.sphere_height,
            bg = "red")
        self.canvas_sphere.place(x=self.result_width, y=self.circuit_height)
                
        self.pic_counter=1

        self.fig = Figure(figsize=(self.sphere_width*(mm_to_inch/self.dpi_x),self.sphere_height*(mm_to_inch/self.dpi_y)))
        self.ax = self.fig.add_subplot(111,projection='3d')
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlabel("", labelpad = -30)
        self.ax.set_ylabel("", labelpad = -30)

        self.canvas = FigureCanvasTkAgg(self.fig, self.canvas_sphere)
        self.canvas.get_tk_widget().pack(anchor=tk.CENTER, fill=tk.BOTH, expand=1)
        
        self.draw()
        ##################################################
                
        ##################################################
        #################<other settings>#################
        
        #drag and drop variable
        self.pressed_x = self.pressed_y = 0

        #display composer
        self.matrix_count_psi = list(range(self.qbar_number))

    def draw(self):
        self.ax.cla()
        vs = visualizer.Visualizer(self.result_psi)
        self.ax.set_aspect('auto')
        theta = np.linspace(0, np.pi, 100)
        phi = np.linspace(0, 2*np.pi, 100)
        theta, phi = np.meshgrid(theta, phi)
        sphere_x = np.sin(theta)*np.cos(phi)
        sphere_y = np.sin(theta)*np.sin(phi)
        sphere_z = np.cos(theta)
        self.ax.plot_surface(sphere_x, sphere_y, sphere_z, alpha=0.2, color='silver')
        self.ax.set_box_aspect((1,1,1))
        self.ax.axis("off") 

        self.circle = ['']*(self.qbar_number-1)

        for i in range(self.qbar_number):
            if i != 0:
                radius = sp.sin(i*sp.pi/self.qbar_number)
                height = sp.cos(i*sp.pi/self.qbar_number)
                self.circle[i-1]=Circle((0, 0), radius,color='gray',alpha=0.4)
                self.ax.add_patch(self.circle[i-1])
                art3d.pathpatch_2d_to_3d(self.circle[i-1], z=height, zdir="z")
        
        self.arrow_x = [[''] for j in range(len(self.result_psi))]
        self.arrow_y = [[''] for j in range(len(self.result_psi))]
        self.arrow_z = [[''] for j in range(len(self.result_psi))]

        for i in range(len(vs.hamming_array)):
            j_counter = 0
            for j in vs.hamming_array[i]:
                if vs.p_array[j]!=0:
                    radius = sp.sin(i*sp.pi/self.qbar_number)
                    height = sp.cos(i*sp.pi/self.qbar_number)
                    theta = 2*sp.pi/len(vs.hamming_array[i])
                    self.arrow_x[j] = [0,radius*sp.cos(theta*j_counter)]
                    self.arrow_y[j] = [0, radius*sp.sin(theta*j_counter)]
                    self.arrow_z[j] = [0, height]
                    self.ax.plot(self.arrow_x[j], self.arrow_y[j], self.arrow_z[j], color='black')
                    self.ax.scatter(radius*sp.cos(theta*j_counter),radius*sp.sin(theta*j_counter),height,
                        c='black',s=20,alpha=0.3)
                    self.ax.text(radius*sp.cos(theta*j_counter),radius*sp.sin(theta*j_counter),height,
                        self.gc.vec_analysis(j,self.qbar_number))
                j_counter += 1

        self.canvas.draw()

    def save(self,event):
        box = (self.master.winfo_x(),
            self.master.winfo_y(),
            self.master.winfo_x()+self.master.winfo_width(),
            self.master.winfo_y()+self.master.winfo_height())
        pyautogui.screenshot(region=box).save(self.address+'\\'+str(self.pic_counter)+'_circuit.png')
        self.fig.savefig(self.address+'\\'+str(self.pic_counter)+'_sphere.png')
        self.pic_counter+=1


    def create_qbar(self):
        self.psi_array = ['']*self.qbar_number
        self.already_set = ['']*self.qbar_number
        self.before_set = ['']*self.qbar_number
        self.psi_data = ['0']*self.qbar_number
        self.psi=sp.Matrix([1])
        x=0
        for i in range(len(self.psi_data)):
            x = sp.Matrix([[1],[0]])
            if self.psi_data[i]=='1':
                x = sp.Matrix([[0],[1]])
            elif self.psi_data[i]=='+':
                x = 1/sp.sqrt(2)*sp.Matrix([[1],[1]])
            elif self.psi_data[i]=='-':
                x = 1/sp.sqrt(2)*sp.Matrix([[1],[-1]])
            elif self.psi_data[i]=='anti':
                x = 1/sp.sqrt(2)*sp.Matrix([[1],[sp.I]])
            elif self.psi_data[i]=='clock':
                x = 1/sp.sqrt(2)*sp.Matrix([[1],[-sp.I]])
            self.psi=self.gc.ten_product(self.psi,x)

        for j in range(self.qbar_number):
            self.canvas_circuit.create_line(self.qbar_margin_width,self.qbar_margin_height*(j+0.5),self.qbar_margin_width + self.qbar_width,self.qbar_margin_height*(j+0.5),fill = "Black", width = self.qbar_wide,tags='qbar')
            self.psi_array[j] = self.canvas_circuit.create_image(self.qbar_margin_width-25, self.qbar_margin_height*(j+0.5), image=self.img_psi, tags=('psi'))
            self.canvas_circuit.tag_bind(self.psi_array[j], "<ButtonPress-1>", lambda event, jj=j: self.popup(event,jj))
            for i in range(self.gate_column):
                self.canvas_circuit.create_oval(self.qbar_margin_width+50+75*i-self.circle_radius,self.qbar_margin_height*(j+0.5)-self.circle_radius,self.qbar_margin_width+50+75*i+self.circle_radius,self.qbar_margin_height*(j+0.5)+self.circle_radius, fill='white',tags='circle')
    def delete_qbar(self):
        self.canvas_circuit.delete('qbar')
        self.canvas_circuit.delete('circle')
        self.canvas_circuit.delete('psi')
        self.delete_gate()

    def delete_gate(self):
        self.canvas_circuit.delete('gate_place')

    #drag and drop functions
    def enter_p(self,event):
        self.canvas_circuit.delete(self.pb)
        self.pa = self.canvas_circuit.create_image(self.button_x1, self.button_y, image=self.img_pa)
        self.canvas_circuit.tag_bind(self.pa, "<Leave>", self.leave_p)
        self.canvas_circuit.tag_bind(self.pa, "<ButtonPress-1>",self.press_p)
    def enter_m(self, events):
        self.canvas_circuit.delete(self.mb)
        self.ma = self.canvas_circuit.create_image(self.button_x2, self.button_y, image=self.img_ma)
        self.canvas_circuit.tag_bind(self.ma, "<Leave>", self.leave_m)
        if self.qbar_number > 1:
            self.canvas_circuit.tag_bind(self.ma, "<ButtonPress-1>",self.press_m)
    def enter_d(self, events):
        self.canvas_circuit.delete(self.db)
        self.da = self.canvas_circuit.create_image(self.button_x3, self.button_y, image=self.img_da)
        self.canvas_circuit.tag_bind(self.da, "<Leave>", self.leave_d)
        self.canvas_circuit.tag_bind(self.da, "<ButtonPress-1>", self.save)

    def leave_p(self, event):
        self.canvas_circuit.delete(self.pa)
        self.pb = self.canvas_circuit.create_image(self.button_x1, self.button_y, image=self.img_pb)
        self.canvas_circuit.tag_bind(self.pb, "<Enter>", self.enter_p)
    def leave_m(self, event):
        self.canvas_circuit.delete(self.ma)
        self.mb = self.canvas_circuit.create_image(self.button_x2, self.button_y, image=self.img_mb)
        self.canvas_circuit.tag_bind(self.mb, "<Enter>", self.enter_m)
    def leave_d(self, event):
        self.canvas_circuit.delete(self.da)
        self.db = self.canvas_circuit.create_image(self.button_x3, self.button_y, image=self.img_db)
        self.canvas_circuit.tag_bind(self.db, "<Enter>", self.enter_d)

    def press_p(self, event):
        self.canvas_circuit.tag_bind(self.pa, "<Leave>", self.leave_p)
        self.canvas_circuit.tag_bind(self.pa, "<ButtonPress-1>",self.press_p)
        if self.gate_valid_area*2 < self.circuit_height/self.qbar_number:
            self.delete_qbar()
            self.qbar_number+=1
            self.qbar_margin_height = self.circuit_height/self.qbar_number
            self.create_qbar()
            self.canvas_circuit.delete('init')
            self.create_init_gate()
            self.display_result()
            self.draw()

    def press_m(self, event): 
        self.canvas_circuit.tag_bind(self.ma, "<Leave>", self.leave_m)
        if self.qbar_number > 1:
            self.qbar_number-=1
            self.delete_qbar()
            self.qbar_margin_height = self.circuit_height/self.qbar_number
            self.create_qbar()
            self.canvas_circuit.delete('init')
            self.create_init_gate()
            self.display_result()
            self.draw()


        if self.qbar_number > 1:
            self.canvas_circuit.tag_bind(self.ma, "<ButtonPress-1>",self.press_m)

    #初期値画面の描画
    def create_initval(self, j):
        self.canvas_pop.delete('value')
        self.ket0=self.canvas_pop.create_image(self.popup_place_w1, self.popup_place_h1, image=self.img_ket0, tags=('0','value'))
        self.canvas_pop.tag_bind(self.ket0, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event, '0', jj))
        self.ket1=self.canvas_pop.create_image(self.popup_place_w2, self.popup_place_h1, image=self.img_ket1, tags=('1','value'))
        self.canvas_pop.tag_bind(self.ket1, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'1', jj))
        self.ketp=self.canvas_pop.create_image(self.popup_place_w3, self.popup_place_h1, image=self.img_ketp, tags=('+','value'))
        self.canvas_pop.tag_bind(self.ketp, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'+', jj))
        self.ketm=self.canvas_pop.create_image(self.popup_place_w4, self.popup_place_h1, image=self.img_ketm, tags=('-','value'))
        self.canvas_pop.tag_bind(self.ketm, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'-', jj))
        self.keta=self.canvas_pop.create_image(self.popup_place_w5, self.popup_place_h1, image=self.img_keta, tags=('anti','value'))
        self.canvas_pop.tag_bind(self.keta, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'anti', jj))
        self.ketc=self.canvas_pop.create_image(self.popup_place_w6, self.popup_place_h1, image=self.img_ketc, tags=('clock','value'))
        self.canvas_pop.tag_bind(self.ketc, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'clock', jj))

        if self.already_set[j]=='0':
            self.canvas_pop.delete(self.ket0)
            self.ket0_red=self.canvas_pop.create_image(self.popup_place_w1, self.popup_place_h1, image=self.img_ket0_red, tags=('0_after', 'value'))
            self.canvas_pop.tag_bind(self.ket0_red, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'0_red', jj))
        elif self.already_set[j]=='1':
            self.canvas_pop.delete(self.ket1)
            self.ket1_red=self.canvas_pop.create_image(self.popup_place_w2, self.popup_place_h1, image=self.img_ket1_red, tags=('1_after', 'value'))
            self.canvas_pop.tag_bind(self.ket1_red, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'1_red', jj))
        elif self.already_set[j]=='+':
            self.canvas_pop.delete(self.ketp)
            self.ketp_red=self.canvas_pop.create_image(self.popup_place_w3, self.popup_place_h1, image=self.img_ketp_red, tags=('+_after', 'value'))
            self.canvas_pop.tag_bind(self.ketp_red, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'+_red', jj))
        elif self.already_set[j]=='-':
            self.canvas_pop.delete(self.ketm)
            self.ketm_red=self.canvas_pop.create_image(self.popup_place_w4, self.popup_place_h1, image=self.img_ketm_red, tags=('-_after', 'value'))
            self.canvas_pop.tag_bind(self.ketm_red, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'-_red', jj))
        elif self.already_set[j]=='anti':
            self.canvas_pop.delete(self.keta)
            self.keta_red=self.canvas_pop.create_image(self.popup_place_w5, self.popup_place_h1, image=self.img_keta_red, tags=('anti_after', 'value'))
            self.canvas_pop.tag_bind(self.keta_red, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'anti_red', jj))
        elif self.already_set[j]=='clock':
            self.canvas_pop.delete(self.ketc)
            self.ketc_red=self.canvas_pop.create_image(self.popup_place_w6, self.popup_place_h1, image=self.img_ketc_red, tags=('clock_after', 'value'))
            self.canvas_pop.tag_bind(self.ketc_red, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'clock_red', jj))

############################################################################################################
############################################################################################################
# to input any value you want, use codes below

        # self.alpha = tk.Entry(self.dialog,font=('@MS UI Gothic',self.font_size),width=6)
        # self.alpha.insert(tk.END, "alpha=1")
        # self.alpha.place(x=self.popup_place_w1-self.font_size/2, y=self.popup_place_h2-self.font_size/2)
        # self.beta = tk.Entry(self.dialog,font=('@MS UI Gothic',self.font_size),width=6)
        # self.beta.insert(tk.END, "beta=0")
        # self.beta.place(x=self.popup_place_w4-self.font_size/2, y=self.popup_place_h2-self.font_size/2)

        self.confirm=self.canvas_pop.create_image((self.popup_place_w3+self.popup_place_w4)/2, self.popup_place_h3, image=self.img_confirm, tag='confirm')

    def popup(self, event, j):
        self.dialog = tk.Toplevel()
        self.dialog.title("Initial Value")
        self.dialog.geometry(str(self.popup_window_width)+"x"+str(self.popup_window_height)+"+"+str(self.popup_margin_width)+"+"+str(self.popup_margin_height))
        self.dialog.grab_set()
        self.dialog.focus_set()
        self.dialog.iconbitmap("pic\icon\icon.ico")
        self.canvas_pop= tk.Canvas(
            self.dialog,
            width = self.popup_window_width,
            height = self.popup_window_height,
            bg="grey")
        self.canvas_pop.place(x=0, y=0)
        self.create_initval(j)

    def select_value(self, event, tag, j):
        x=self.already_set[j]
        self.before_set[j]=x
        self.canvas_pop.delete('value')
        self.ket0=self.canvas_pop.create_image(self.popup_place_w1, self.popup_place_h1, image=self.img_ket0, tags=('0','value'))
        self.canvas_pop.tag_bind(self.ket0, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event, '0', jj))
        self.ket1=self.canvas_pop.create_image(self.popup_place_w2, self.popup_place_h1, image=self.img_ket1, tags=('1','value'))
        self.canvas_pop.tag_bind(self.ket1, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'1', jj))
        self.ketp=self.canvas_pop.create_image(self.popup_place_w3, self.popup_place_h1, image=self.img_ketp, tags=('+','value'))
        self.canvas_pop.tag_bind(self.ketp, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'+', jj))
        self.ketm=self.canvas_pop.create_image(self.popup_place_w4, self.popup_place_h1, image=self.img_ketm, tags=('-','value'))
        self.canvas_pop.tag_bind(self.ketm, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'-', jj))
        self.keta=self.canvas_pop.create_image(self.popup_place_w5, self.popup_place_h1, image=self.img_keta, tags=('anti','value'))
        self.canvas_pop.tag_bind(self.keta, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'anti', jj))
        self.ketc=self.canvas_pop.create_image(self.popup_place_w6, self.popup_place_h1, image=self.img_ketc, tags=('clock','value'))
        self.canvas_pop.tag_bind(self.ketc, "<ButtonPress-1>", lambda event, jj=j: self.select_value(event,'clock', jj))

        if  tag=='0_red':
            self.canvas_pop.delete(self.ket0_red)
            self.canvas_pop.create_image(self.popup_place_w1, self.popup_place_h1, image=self.img_ket0, tags=('0_after', 'value'))
            self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'0', j))
            self.already_set[j] = ''
        elif tag=='1_red':
            self.canvas_pop.delete(self.ket1_red)
            self.canvas_pop.create_image(self.popup_place_w2, self.popup_place_h1, image=self.img_ket1, tags=('1', 'value'))
            self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'1', j))
            self.already_set[j] = ''
        elif tag=='+_red':
            self.canvas_pop.delete(self.ketp_red)
            self.canvas_pop.create_image(self.popup_place_w3, self.popup_place_h1, image=self.img_ketp, tags=('+', 'value'))
            self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'+', j))
            self.already_set[j] = ''
        elif tag=='-_red':
            self.canvas_pop.delete(self.ketm_red)
            self.canvas_pop.create_image(self.popup_place_w4, self.popup_place_h1, image=self.img_ketm, tags=('-', 'value'))
            self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'-', j))
            self.already_set[j] = ''
        elif tag=='anti_red':
            self.canvas_pop.delete(self.keta_red)
            self.canvas_pop.create_image(self.popup_place_w5, self.popup_place_h1, image=self.img_keta, tags=('anti', 'value'))
            self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'anti', j))
            self.already_set[j] = ''
        elif tag=='clock_red':
            self.canvas_pop.delete(self.ketc_red)
            self.canvas_pop.create_image(self.popup_place_w6, self.popup_place_h1, image=self.img_ketc, tags=('clock', 'value'))
            self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'clock', j))
            self.already_set[j] = ''
        else:
            if tag=='0':
                self.canvas_pop.delete(self.ket0)
                self.canvas_pop.create_image(self.popup_place_w1, self.popup_place_h1, image=self.img_ket0_red, tags=('0_after', 'value'))
                self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'0', j))
            elif tag=='1':
                self.canvas_pop.delete(self.ket1)
                self.canvas_pop.create_image(self.popup_place_w2, self.popup_place_h1, image=self.img_ket1_red, tags=('1_after', 'value'))
                self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'1', j))
            elif tag=='+':
                self.canvas_pop.delete(self.ketp)
                self.canvas_pop.create_image(self.popup_place_w3, self.popup_place_h1, image=self.img_ketp_red, tags=('+_after', 'value'))
                self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'+', j))
            elif tag=='-':
                self.canvas_pop.delete(self.ketm)
                self.canvas_pop.create_image(self.popup_place_w4, self.popup_place_h1, image=self.img_ketm_red, tags=('-_after', 'value'))
                self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'-', j))
            elif tag=='anti':
                self.canvas_pop.delete(self.keta)
                self.canvas_pop.create_image(self.popup_place_w5, self.popup_place_h1, image=self.img_keta_red, tags=('anti_after', 'value'))
                self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'anti', j))
            elif tag=='clock':
                self.canvas_pop.delete(self.ketc)
                self.canvas_pop.create_image(self.popup_place_w6, self.popup_place_h1, image=self.img_ketc_red, tags=('clock_after', 'value'))
                self.canvas_pop.tag_bind(self.confirm, "<ButtonPress-1>", lambda event: self.set_value(event,'clock', j))
            self.already_set[j] = tag

    def set_value(self, event, tag,j):
        self.dialog.destroy()
        self.psi_data[j]=tag
        self.psi_array[j] = self.canvas_circuit.create_image(self.qbar_margin_width-25, self.qbar_margin_height*(j+0.5), image=self.img_psi_after, tags='psi')
        self.canvas_circuit.tag_bind(self.psi_array[j], "<ButtonPress-1>", lambda event, jj=j: self.popup(event,jj))
        self.already_set[j]=tag
        self.psi=sp.Matrix([1])
        for i in range(len(self.psi_data)):
            if self.psi_data[i]=='0':
                self.psi=self.gc.ten_product(self.psi,sp.Matrix([[1],[0]]))
            elif self.psi_data[i]=='1':
                self.psi=self.gc.ten_product(self.psi,sp.Matrix([[0],[1]]))
            elif self.psi_data[i]=='+':
                self.psi=self.gc.ten_product(self.psi,1/sp.sqrt(2)*sp.Matrix([[1],[1]]))
            elif self.psi_data[i]=='-':
                self.psi=self.gc.ten_product(self.psi,1/sp.sqrt(2)*sp.Matrix([[1],[-1]]))
            elif self.psi_data[i]=='anti':
                self.psi=self.gc.ten_product(self.psi,1/sp.sqrt(2)*sp.Matrix([[1],[sp.I]]))
            elif self.psi_data[i]=='clock':
                self.psi=self.gc.ten_product(self.psi,1/sp.sqrt(2)*sp.Matrix([[1],[-sp.I]]))
        self.display_result()
        self.draw()
    
    def create_init_gate(self):
        self.h = []
        self.x = []
        self.y = []
        self.z = []
        self.s = []
        self.t = []
        self.sd = []
        self.td = []
        self.p = []
        self.m = []
        self.c = []
        self.count_h = self.count_x = self.count_y = self.count_z = self.count_s = self.count_t = self.count_sd = self.count_td = self.count_p = self.count_m = self.count_c = 0
        self.gate=[['i' for i in range(self.gate_column)] for j in range(self.qbar_number)]
        self.p_phi=sp.zeros(self.gate_column,self.qbar_number)

        self.h_init = self.canvas_circuit.create_image(self.place_c1, self.place_r1, image=self.img_h, tags=('gate','init','h','h_init'))
        self.x_init = self.canvas_circuit.create_image(self.place_c2, self.place_r1, image=self.img_x, tags=('gate', 'init','x','x_init'))
        self.y_init = self.canvas_circuit.create_image(self.place_c3, self.place_r1, image=self.img_y, tags=('gate', 'init','y','y_init'))
        self.z_init = self.canvas_circuit.create_image(self.place_c4, self.place_r1, image=self.img_z, tags=('gate','init','z','z_init'))
        self.s_init = self.canvas_circuit.create_image(self.place_c1, self.place_r2, image=self.img_s, tags=('gate', 'init','s','s_init'))
        self.t_init = self.canvas_circuit.create_image(self.place_c2, self.place_r2, image=self.img_t, tags=('gate', 'init','t','t_init'))
        self.sd_init = self.canvas_circuit.create_image(self.place_c3, self.place_r2, image=self.img_sd, tags=('gate', 'init','sd','sd_init'))
        self.td_init = self.canvas_circuit.create_image(self.place_c4, self.place_r2, image=self.img_td, tags=('gate', 'init','td','td_init'))
        self.p_init = self.canvas_circuit.create_image(self.place_c1, self.place_r3, image=self.img_p, tags=('gate', 'init','p','p_init'))        
        self.c_init = self.canvas_circuit.create_image(self.place_c2, self.place_r3, image=self.img_c, tags=('gate', 'init','c','c_init'))
        self.m_init = self.canvas_circuit.create_image(self.place_c3, self.place_r3, image=self.img_m, tags=('gate', 'init','m','m_init'))
        
        self.canvas_circuit.tag_bind(self.h_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'h_init',0))
        self.canvas_circuit.tag_bind(self.x_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'x_init',0))
        self.canvas_circuit.tag_bind(self.y_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'y_init',0))
        self.canvas_circuit.tag_bind(self.z_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'z_init',0))
        self.canvas_circuit.tag_bind(self.s_init, "<ButtonPress-1>", lambda event: self.pressed(event, 's_init',0))
        self.canvas_circuit.tag_bind(self.t_init, "<ButtonPress-1>", lambda event: self.pressed(event, 't_init',0))
        self.canvas_circuit.tag_bind(self.sd_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'sd_init',0))
        self.canvas_circuit.tag_bind(self.td_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'td_init',0))
        self.canvas_circuit.tag_bind(self.p_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'p_init',0))
        self.canvas_circuit.tag_bind(self.c_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'c_init',0))
        self.canvas_circuit.tag_bind(self.m_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'm_init',0))

    def pressed(self, event, tag,k):
        self.pressed_x = event.x
        self.pressed_y = event.y
        row=column=0
        for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        row=j
                        column=i
        if tag=='h_init':
            self.canvas_circuit.tag_bind(self.h_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.h_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='x_init':
            self.canvas_circuit.tag_bind(self.x_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.x_init, "<ButtonRelease-1>", lambda event: self.released(event, tag,0,0,0))
        elif tag=='y_init':
            self.canvas_circuit.tag_bind(self.y_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.y_init, "<ButtonRelease-1>", lambda event: self.released(event, tag,0,0,0))
        elif tag=='z_init':
            self.canvas_circuit.tag_bind(self.z_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.z_init, "<ButtonRelease-1>", lambda event: self.released(event, tag,0,0,0))
        elif tag=='s_init':
            self.canvas_circuit.tag_bind(self.s_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.s_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='t_init':
            self.canvas_circuit.tag_bind(self.t_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.t_init, "<ButtonRelease-1>", lambda event: self.released(event, tag,0,0,0))
        elif tag=='sd_init':
            self.canvas_circuit.tag_bind(self.sd_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.sd_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='td_init':
            self.canvas_circuit.tag_bind(self.td_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.td_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='p_init':
            self.canvas_circuit.tag_bind(self.p_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.p_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='m_init':
            self.canvas_circuit.tag_bind(self.m_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.m_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='c_init':
            self.canvas_circuit.tag_bind(self.c_init, "<B1-Motion>", lambda event: self.dragged(event, tag,0))
            self.canvas_circuit.tag_bind(self.c_init, "<ButtonRelease-1>", lambda event: self.released(event,tag,0,0,0))
        elif tag=='h_place':
            self.canvas_circuit.tag_bind(self.h[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.h[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='x_place':
            self.canvas_circuit.tag_bind(self.x[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.x[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='y_place':
            self.canvas_circuit.tag_bind(self.y[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.y[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='z_place':
            self.canvas_circuit.tag_bind(self.z[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.z[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='s_place':
            self.canvas_circuit.tag_bind(self.s[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.s[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='t_place':
            self.canvas_circuit.tag_bind(self.t[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.t[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='sd_place':
            self.canvas_circuit.tag_bind(self.sd[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.sd[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='td_place':
            self.canvas_circuit.tag_bind(self.td[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.td[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='p_place':
            self.canvas_circuit.tag_bind(self.p[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.p[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='m_place':
            self.canvas_circuit.tag_bind(self.m[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.m[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
        elif tag=='c_place':
            self.canvas_circuit.tag_bind(self.c[k], "<B1-Motion>", lambda event,kk=k: self.dragged(event, tag,kk))
            self.canvas_circuit.tag_bind(self.c[k], "<ButtonRelease-1>", lambda event,kk=k,r=row,c=column: self.released(event, tag,kk,r,c))
    
    
    def dragged(self, event, tag,j):
        if tag=='h_place':
            x, y = self.canvas_circuit.coords(self.h[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.h[j], x+delta_x, y+delta_y)
        elif tag=='x_place':
            x, y = self.canvas_circuit.coords(self.x[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.x[j], x+delta_x, y+delta_y)
        elif tag=='y_place':
            x, y = self.canvas_circuit.coords(self.y[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.y[j], x+delta_x, y+delta_y)
        elif tag=='z_place':
            x, y = self.canvas_circuit.coords(self.z[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.z[j], x+delta_x, y+delta_y)
        elif tag=='s_place':
            x, y = self.canvas_circuit.coords(self.s[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.s[j], x+delta_x, y+delta_y)
        elif tag=='t_place':
            x, y = self.canvas_circuit.coords(self.t[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.t[j], x+delta_x, y+delta_y)
        elif tag=='sd_place':
            x, y = self.canvas_circuit.coords(self.sd[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.sd[j], x+delta_x, y+delta_y)
        elif tag=='td_place':
            x, y = self.canvas_circuit.coords(self.td[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.td[j], x+delta_x, y+delta_y)
        elif tag=='p_place':
            x, y = self.canvas_circuit.coords(self.p[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.p[j], x+delta_x, y+delta_y)
        elif tag=='m_place':
            x, y = self.canvas_circuit.coords(self.m[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.m[j], x+delta_x, y+delta_y)
        elif tag=='c_place':
            x, y = self.canvas_circuit.coords(self.c[j])
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(self.c[j], x+delta_x, y+delta_y)
        else:
            x, y = self.canvas_circuit.coords(tag)
            delta_x = event.x - self.pressed_x
            delta_y = event.y - self.pressed_y
            self.canvas_circuit.coords(tag, x+delta_x, y+delta_y)
        self.pressed_x = event.x
        self.pressed_y = event.y
       
    def released(self, event, tag,j,row,column):
        if tag=='h_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.h.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_h, tags=('gate','gate_place',tag+'place')))
                        self.count_h+=1
                        self.canvas_circuit.tag_bind(self.h[self.count_h-1], "<ButtonPress-1>", lambda event, k=self.count_h: self.pressed(event, 'h_place',k-1))
                        self.gate[j][i]='h'
            self.h_init = self.canvas_circuit.create_image(self.place_c1, self.place_r1, image=self.img_h, tags=('gate','init','h','h_init'))
            self.canvas_circuit.tag_bind(self.h_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'h_init',0))
        elif tag=='x_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.x.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_x, tags=('gate','gate_place',tag+'place')))
                        self.count_x+=1
                        self.canvas_circuit.tag_bind(self.x[self.count_x-1], "<ButtonPress-1>", lambda event,k=self.count_x: self.pressed(event, 'x_place',k-1))
                        self.gate[j][i]='x'
            self.x_init = self.canvas_circuit.create_image(self.place_c2, self.place_r1, image=self.img_x, tags=('gate','init','x','x_init'))
            self.canvas_circuit.tag_bind(self.x_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'x_init',0))
        elif tag=='y_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.y.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_y, tags=('gate','gate_place',tag+'place')))
                        self.count_y+=1
                        self.canvas_circuit.tag_bind(self.y[self.count_y-1], "<ButtonPress-1>", lambda event,k=self.count_y: self.pressed(event, 'y_place',k-1))
                        self.gate[j][i]='y'
            self.y_init = self.canvas_circuit.create_image(self.place_c3, self.place_r1, image=self.img_y, tags=('gate','init','y','y_init'))
            self.canvas_circuit.tag_bind(self.y_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'y_init',0))
        elif tag=='z_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.z.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_z, tags=('gate','gate_place',tag+'place')))
                        self.count_z+=1
                        self.canvas_circuit.tag_bind(self.z[self.count_z-1], "<ButtonPress-1>", lambda event,k=self.count_z: self.pressed(event, 'z_place',k-1))
                        self.gate[j][i]='z'
            self.z_init = self.canvas_circuit.create_image(self.place_c4, self.place_r1, image=self.img_z, tags=('gate','init','z','z_init'))
            self.canvas_circuit.tag_bind(self.z_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'z_init',0))
        elif tag=='s_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.s.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_s, tags=('gate','gate_place',tag+'place')))
                        self.count_s+=1
                        self.canvas_circuit.tag_bind(self.s[self.count_s-1], "<ButtonPress-1>", lambda event,k=self.count_s: self.pressed(event, 's_place',k-1))
                        self.gate[j][i]='s'
            self.s_init = self.canvas_circuit.create_image(self.place_c1, self.place_r2, image=self.img_s, tags=('gate','init','s','s_init'))
            self.canvas_circuit.tag_bind(self.s_init, "<ButtonPress-1>", lambda event: self.pressed(event, 's_init',0))
        elif tag=='t_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.t.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_t, tags=('gate','gate_place',tag+'place')))
                        self.count_t+=1
                        self.canvas_circuit.tag_bind(self.t[self.count_t-1], "<ButtonPress-1>", lambda event,k=self.count_t: self.pressed(event, 't_place',k-1))
                        self.gate[j][i]='t'
            self.t_init = self.canvas_circuit.create_image(self.place_c2, self.place_r2, image=self.img_t, tags=('gate','init','t','t_init'))
            self.canvas_circuit.tag_bind(self.t_init, "<ButtonPress-1>", lambda event: self.pressed(event, 't_init',0))
        elif tag=='sd_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.sd.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_sd, tags=('gate','gate_place',tag+'place')))
                        self.count_sd+=1
                        self.canvas_circuit.tag_bind(self.sd[self.count_sd-1], "<ButtonPress-1>", lambda event,k=self.count_sd: self.pressed(event, 'sd_place',k-1))
                        self.gate[j][i]='sd'
            self.sd_init = self.canvas_circuit.create_image(self.place_c3, self.place_r2, image=self.img_sd, tags=('gate','init','sd','sd_init'))
            self.canvas_circuit.tag_bind(self.sd_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'sd_init',0))
        elif tag=='td_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.td.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_td, tags=('gate','gate_place',tag+'place')))
                        self.count_td+=1
                        self.canvas_circuit.tag_bind(self.td[self.count_td-1], "<ButtonPress-1>", lambda event,k=self.count_td: self.pressed(event, 'td_place',k-1))
                        self.gate[j][i]='td'
            self.td_init = self.canvas_circuit.create_image(self.place_c4, self.place_r2, image=self.img_td, tags=('gate','init','td','td_init'))
            self.canvas_circuit.tag_bind(self.td_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'td_init',0))
        elif tag=='p_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.p.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_p, tags=('gate','gate_place',tag+'place')))
                        self.count_p+=1
                        self.canvas_circuit.tag_bind(self.p[self.count_p-1], "<ButtonPress-1>", lambda event,k=self.count_p: self.pressed(event, 'p_place',k-1))
                        self.gate[j][i]='p'
            self.p_init = self.canvas_circuit.create_image(self.place_c1, self.place_r3, image=self.img_p, tags=('gate','init','p','p_init'))
            self.canvas_circuit.tag_bind(self.p_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'p_init',0))
        elif tag=='m_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.m.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_m, tags=('gate','gate_place',tag+'place')))
                        self.count_m+=1
                        self.canvas_circuit.tag_bind(self.m[self.count_m-1], "<ButtonPress-1>", lambda event,k=self.count_m: self.pressed(event, 'm_place',k-1))
                        self.gate[j][i]='measure'
            self.m_init = self.canvas_circuit.create_image(self.place_c3, self.place_r3, image=self.img_m, tags=('gate','init','m','m_init'))
            self.canvas_circuit.tag_bind(self.m_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'm_init',0))
        elif tag=='c_init':
            self.canvas_circuit.delete(tag)
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.c.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_c, tags=('gate','gate_place',tag+'place')))
                        self.count_c+=1
                        self.canvas_circuit.tag_bind(self.c[self.count_c-1], "<ButtonPress-1>", lambda event,k=self.count_c: self.pressed(event, 'c_place',k-1))
                        self.gate[j][i]='c'
            self.c_init = self.canvas_circuit.create_image(self.place_c2, self.place_r3, image=self.img_c, tags=('gate','init','c','c_init'))
            self.canvas_circuit.tag_bind(self.c_init, "<ButtonPress-1>", lambda event: self.pressed(event, 'c_init',0))
        elif tag=='h_place':
            self.canvas_circuit.delete(self.h[j])
            self.count_h-=1
            del self.h[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.h.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_h, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.h[self.count_h], "<ButtonPress-1>", lambda event, j=self.count_h: self.pressed(event, 'h_place',j))
                        self.count_h+=1
                        self.gate[j][i]='h'
        elif tag=='x_place':
            self.canvas_circuit.delete(self.x[j])
            self.count_x-=1
            del self.x[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.x.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_x, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.x[self.count_x], "<ButtonPress-1>", lambda event, j=self.count_x: self.pressed(event, 'x_place',j))
                        self.count_x+=1
                        self.gate[j][i]='x'
        elif tag=='y_place':
            self.canvas_circuit.delete(self.y[j])
            self.count_y-=1
            del self.y[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.y.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_y, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.y[self.count_y], "<ButtonPress-1>", lambda event, j=self.count_y: self.pressed(event, 'y_place',j))
                        self.count_y+=1
                        self.gate[j][i]='y'
        elif tag=='z_place':
            self.canvas_circuit.delete(self.z[j])
            self.count_z-=1
            del self.z[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.z.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_z, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.z[self.count_z], "<ButtonPress-1>", lambda event, j=self.count_z: self.pressed(event, 'z_place',j))
                        self.count_z+=1
                        self.gate[j][i]='z'
        elif tag=='s_place':
            self.canvas_circuit.delete(self.s[j])
            self.count_s-=1
            del self.s[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.s.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_s, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.s[self.count_s], "<ButtonPress-1>", lambda event, j=self.count_s: self.pressed(event, 's_place',j))
                        self.count_s+=1
                        self.gate[j][i]='s'
        elif tag=='t_place':
            self.canvas_circuit.delete(self.t[j])
            self.count_t-=1
            del self.t[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.t.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_t, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.t[self.count_t], "<ButtonPress-1>", lambda event, j=self.count_t: self.pressed(event, 't_place',j))
                        self.count_t+=1
                        self.gate[j][i]='t'
        elif tag=='sd_place':
            self.canvas_circuit.delete(self.sd[j])
            self.count_sd-=1
            del self.sd[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.sd.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_sd, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.sd[self.count_sd], "<ButtonPress-1>", lambda event, j=self.count_sd: self.pressed(event, 'sd_place',j))
                        self.count_sd+=1
                        self.gate[j][i]='sd'
        elif tag=='td_place':
            self.canvas_circuit.delete(self.td[j])
            self.count_td-=1
            del self.td[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.td.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_td, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.td[self.count_td], "<ButtonPress-1>", lambda event, j=self.count_td: self.pressed(event, 'td_place',j))
                        self.count_td+=1
                        self.gate[j][i]='td'
        elif tag=='p_place':
            self.canvas_circuit.delete(self.p[j])
            self.count_p-=1
            del self.p[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.p.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_p, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.p[self.count_p], "<ButtonPress-1>", lambda event, j=self.count_p: self.pressed(event, 'p_place',j))
                        self.count_p+=1
                        self.gate[j][i]='p'
        elif tag=='m_place':
            self.canvas_circuit.delete(self.m[j])
            self.count_m-=1
            del self.m[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.m.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_m, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.m[self.count_m], "<ButtonPress-1>", lambda event, j=self.count_m: self.pressed(event, 'm_place',j))
                        self.count_m+=1
                        self.gate[j][i]='measure'
        elif tag=='c_place':
            self.canvas_circuit.delete(self.c[j])
            self.count_c-=1
            del self.c[j]
            self.gate[row][column]='i'
            for j in range(self.qbar_number):
                for i in range(self.gate_column):
                    if  self.qbar_margin_width+self.gate_size+75*i-self.gate_valid_area/2 < event.x and event.x < self.qbar_margin_width+self.gate_size+75*i+self.gate_valid_area/2 and self.qbar_margin_height*(j+0.5)-self.gate_valid_area/2 < event.y and event.y < self.qbar_margin_height*(j+0.5)+self.gate_valid_area/2:
                        self.c.append(self.canvas_circuit.create_image(self.qbar_margin_width+self.gate_size+75*i, self.qbar_margin_height*(j+0.5), image=self.img_c, tags=('gate','gate_place',tag)))
                        self.canvas_circuit.tag_bind(self.c[self.count_c], "<ButtonPress-1>", lambda event, j=self.count_c: self.pressed(event, 'c_place',j))
                        self.count_c+=1
                        self.gate[j][i]='c'
        

        self.display_result()
        self.draw()

    def set_pphi(self,event,ii,jj):
        self.dialog_pphi = tk.Toplevel()
        self.dialog_pphi.title("set value Phi")
        self.dialog_pphi.geometry(str(self.popup_window_width)+"x"+str(self.popup_window_height)+"+"+str(self.popup_margin_width)+"+"+str(self.popup_margin_height))
        self.dialog_pphi.grab_set()
        self.dialog_pphi.focus_set()
        self.dialog_pphi.iconbitmap("pic\icon\icon.ico")
        self.canvas_pop_pphi= tk.Canvas(
            self.dialog_pphi,
            width = self.popup_window_width,
            height = self.popup_window_height,
            bg="grey")
        self.canvas_pop_pphi.place(x=0, y=0)
        self.confirm_pphi=self.canvas_pop_pphi.create_image((self.popup_place_w3+self.popup_place_w4)/2, self.popup_place_h3, image=self.img_confirm, tag='confirm')
        self.phi_text = tk.Label(text='Phi')
        self.phi_text.place(x=self.popup_place_w1, y=self.popup_place_h1)
        self.phi_input = tk.Entry(width=(self.popup_place_w6-self.popup_place_w2))
        self.phi_input.place(x=self.popup_place_w1, y=self.popup_place_h1)
        self.phi_input.insert(tk.END,"0")
        self.canvas_pop_pphi.tag_bind(self.confirm_pphi, "<ButtonPress-1>", lambda event,iii=ii,jjj=jj:self.set_pphi2(event,iii,jjj))

    def set_pphi2(self,event,i,j):
        text=self.phi_input.get()
        value=self.text_to_value(text)
        self.gate[i][j]=value
        self.dialog_pphi.destroy()
    def text_to_value(self,text):
        value=eval(text)
        return value
    

    def display_result(self):
        self.result_psi = self.gc.calc(self.gate,self.psi,self)
        # psi_split=sp.latex(self.gc.ten_analysis(self.psi))
        # psi_result_split=sp.latex(self.gc.ten_analysis(self.result_psi))
        
        psi_split=self.gc.ten_analysis(self.psi)
        psi_result_split=self.gc.ten_analysis(self.result_psi)

        # sp.printing.preview(sp.latex(self.result_u), viewer='file', filename=gate_address, euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])

###################################
        # sp.printing.preview('r"""$$'+sp.latex(self.psi)+'$$"""', viewer='file', filename=psi_init_address, euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
        # sp.printing.preview('r"""$$'+sp.latex(self.result_psi)+'$$"""', viewer='file', filename=psi_address, euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
        
        # self.tex_psi_init = tk.PhotoImage(file=psi_init_address)
        # self.tex_psi = tk.PhotoImage(file=psi_address)

        # self.tex_init = self.canvas_result.create_image(int(self.circuit_width/4),int(self.circuit_height/2), image=self.tex_psi_init, tag='tex')
        # self.tex_result = self.canvas_result.create_image(int(3*self.circuit_width/4),int(self.circuit_height/2), image=self.tex_psi, tag='tex')
###################################

        # self.ax_result.text(10,10, r"$\int_{x_0}^{x_1} f(x)dx$")
        #self.canvas_result.create_text(3*int(self.result_width/4),int(self.result_height/2), text=self.result_psi, font=self.font_size)

        self.ax_result.cla()
        self.ax_result.set_aspect('auto')
        self.ax_result.axis('off')

        self.ax_result.text(-0.1,0.6, psi_split,fontsize=25)
        self.ax_result.text(-0.1,0.2, psi_result_split,fontsize=25,color='red')

        self.canvas_answer.draw()