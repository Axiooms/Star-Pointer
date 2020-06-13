#Imports
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
import time
import pandas as pd
import numpy as np

class Star_finder(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.set_var() #Set all variables
        self.create_frames() #Create principal Frames (3 pannels)
        self.Param_widgets() #Create the widgets of the 'Parameters' Frame (left pannel)
        self.Commands_widgets() #Create the widgets of the 'Commands' Frame (right pannel)
        self.Vizualiation_widgets() #Create the widgets of the 'Vizualisation' Frame (center pannel)
        self.create_menu() #Create the menu bar

    def set_var(self):
        """ Set all the variables used in this programme """

        # -------------------------- Commands buttons labels ------------------------- #

        self.x_up = tk.StringVar()
        self.x_up.set('Declinaison UP')
        self.x_down = tk.StringVar()
        self.x_down.set('Declinaison DOWN')
        self.y_up = tk.StringVar()
        self.y_up.set('Right Ascension UP')
        self.y_down = tk.StringVar()
        self.y_down.set('Right Ascension DOWN')

        # ----------------------- Follow mode ativator variable ---------------------- #

        self.flw_state = tk.IntVar()
        self.flw_state.set(1)

        # -------------------------- Targetable Objects list ------------------------- #

        #Load catalogs
        #* Sources :    - https://github.com/jbcurtin/messier-catalogue/blob/master/data/messier-objects.csv (Messier)
        #*              - http://www.astrosurf.com/luxorion/download.htm (NGC)

        self.messier = pd.read_csv('catalogs/messier-objects.csv') #Messier
        self.NGC = pd.read_csv('catalogs/ngc-ic2000.csv') #NGC
        
        #Clean datasets
        for element in range(len(self.messier)):  #If no data, replace by the Messier Number
            if str(self.messier['Common name'][element])[0].lower() not in 'abcdefghijklmnstuvwxyz ': 
                self.messier['Common name'][element] = self.messier['Messier number'][element]
        self.messier = self.messier.set_index(['Common name']) #Change 'Common name' column into dataset index
                
        for element in range(len(self.NGC)):
                self.NGC['NGC/IC'][element] = ' '.join(['NGC', str(self.NGC['NGC/IC'][element])])
                       
        self.NGC.set_index('NGC/IC', inplace = True) #Change 'NGC/IC' column into dataset index
        self.NGC.dropna(inplace = True) #Drop all row containing NaN values
        print(self.messier.head())
        print(self.NGC.head())
        #Catalogs variables
        self.current_catalog = 'None' 
        self.catalog_list = ['--Select a Catalog--', 'Planets', 'Messier', 'NGC']    
        
        #Target variables
        self.objects_list = ['--Select a Catalog--']
        self.current_target = None
        self.target_coords_strvar = tk.StringVar()
        self.target_coords_strvar.set(None)
        self.target_coords = None
        self.current_target_strvar = tk.StringVar()     
        self.current_target_strvar.set('No target')

        # ----------------------------- Current Position ----------------------------- #
        self.current_position = [0, 0]
        self.current_pos_strvar = tk.StringVar()
        self.current_pos_strvar.set('None')
        
# ----------------------------------- Front End ---------------------------------- #

    def create_frames(self):
        """ Create the main Frames """

        #Parameters Pannel
        self.Parameters = tk.LabelFrame(self, text = 'Parameters', width = 445, height  = 1000, bg = '#962E12', bd = 3)
        self.Parameters.grid(row = 0, column = 0, rowspan = 2, sticky ='nsew')
        self.Parameters.grid_propagate(0)
        #Vizualiation Pannel
        self.Vizualisation = tk.LabelFrame(self, text = 'Vizualisation', width = 645, height  = 1000, bg = '#962E12', bd = 3)
        self.Vizualisation.grid(row = 0, column = 1, sticky = 'nsew')
        self.Vizualisation.grid_propagate(0)
        #Commands Pannel
        self.Commands = tk.LabelFrame(self, text = 'Commands', width = 445, height = 1000, bg = '#962E12', bd = 3)
        self.Commands.grid(row = 0, column = 3, rowspan = 10, sticky = 'nsew')
        self.Commands.grid_propagate(0)

    def Param_widgets(self):
        """ Create wigets of the 'Parameters' pannel """

        # ---------------------------------- Clocks ---------------------------------- #
        #Date Frame
        self.date_frame = tk.LabelFrame(self.Parameters, text = 'Date', bg = '#962E12', width = 400, height = 80)
        self.date_frame.grid(row = 0, column = 0, padx = 22)
        self.date_frame.grid_propagate(0)

        #Create clock functions
        def lcl_clock():
            """ A local datetime clock, based on the work of Vegeseat (https://www.daniweb.com/programming/software-development/code/216785/tkinter-digital-clock-python)"""
            lcl_datetime = time.strftime('Date : %d / %m / %Y  -- Hour : %H h %M min %S sec')
            self.lcl_date_lbl.config(text = lcl_datetime)
            self.lcl_date_lbl.after(1000, lcl_clock)

        #Display Local date 
        self.lcl_date_lbl = tk.Label(self.date_frame, text = ' Local Date : 00:00:00 xx/xx/xxxx', bg = '#962E12')
        self.lcl_date_lbl.grid(row = 1, column = 0, sticky = 'w', padx = 20)
        
        lcl_clock()

        #-------------------------------------- Follow Mode Activator --------------------------------------#
        #Follow Mode Frame
        self.flw_frame = tk.LabelFrame(self.Parameters, text = 'Des / Activate Follow Mode', bg = '#962E12', width = 400, height = 50)
        self.flw_frame.grid(row = 1, column = 0, sticky = 'w', padx = 22, pady = 25)
        self.flw_frame.grid_propagate(0)

        #Follow Mode activator
        self.flw_btn = tk.Checkbutton(self.flw_frame, text = 'Follow Mode', variable =  self.flw_state, onvalue = 1, offvalue = 0, 
                                      command = self.follow_mode, bg = '#962E12', activebackground = '#962E12')
        self.flw_btn.grid(row = 9, column = 0, columnspan = 2, sticky = 'w', padx = 160)

        #-------------------------------------- Targetable Objects List --------------------------------------#
        #Targetable Objects Frame
        self.current_target_frame = tk.LabelFrame(self.Parameters, text = 'Target Selection', bg = '#962E12', width = 400, height = 80)
        self.current_target_frame.grid(row = 2, column = 0, sticky = 'w', padx = 22)
        self.current_target_frame.grid_propagate(0)
        
        #Catalogs choice list
        self.slct_catalog = ttk.Combobox(self.current_target_frame, text = 'Select a catalog : ', values = self.catalog_list, justify = tk.CENTER)
        self.slct_catalog.grid(row = 3, column = 0, padx = 40, pady = 15)
        self.slct_catalog.set(self.catalog_list[0])
        self.slct_catalog.bind('<<ComboboxSelected>>', self.update_catalog)
        #Targetable Objects choice
        self.slct_target = ttk.Combobox(self.current_target_frame, text = 'Select a Target :', values = self.objects_list, justify = tk.CENTER)
        self.slct_target.grid(row = 3, column = 1)
        self.slct_target.set(self.objects_list[0])
        self.slct_target.bind('<<ComboboxSelected>>', self.update_target)

    def Commands_widgets(self):

        #-------------------------------------- Command Buttons --------------------------------------#
        #Command Buttons Frame
        self.btn_frame = tk.LabelFrame(self.Commands, text = 'Command Buttons', bg = '#962E12', width = 400, height = 150)
        self.btn_frame.grid(row = 0, column = 0, sticky = 'w', padx = 22)
        self.btn_frame.grid_propagate(0)

        #X axis 'Up' and 'Down' Buttons
        self.X_up = tk.Button(self.btn_frame, textvariable = self.x_up, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20, command = self.X_increment)
        self.X_up.grid(row = 1, column = 0, padx = 30, pady = 25) #! padx of buttons is set only here
        self.X_down = tk.Button(self.btn_frame, textvariable = self.x_down, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20, command = self.X_decrement)
        self.X_down.grid(row = 1, column = 1, pady = 25)
    
        #Y axis 'Up' and 'Down' Buttons
        self.Y_up = tk.Button(self.btn_frame, textvariable = self.y_up, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20, command = self.Y_increment)
        self.Y_up.grid(row = 5, column = 0, padx = 10)
        self.Y_down = tk.Button(self.btn_frame, textvariable = self.y_down, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20, command = self.Y_decrement)
        self.Y_down.grid(row = 5, column = 1)
        
        # --------------------------- Target Frame --------------------------- #
        #Target Frame
        self.target_frame = tk.LabelFrame(self.Commands, text = 'Current Target', width = 400, height = 200, bg = '#962E12')
        self.target_frame.grid(row = 1, column = 0)
        self.target_frame.grid_propagate(0)
        
        #Coords Frame
        self.coords_frame = tk.LabelFrame(self.target_frame, text = 'Coordinates', width = 396, height = 80, bg = '#962E12')
        self.coords_frame.grid(row = 0, column = 0)
        self.coords_frame.grid_propagate(0)

        #Display current target name and coordinates
        tk.Label(self.coords_frame, text = 'Target : ', bg = '#962E12').grid(row = 0, column = 0, sticky = 'w', padx = 20)
        self.current_target_lbl = tk.Label(self.coords_frame, textvariable = self.current_target_strvar, bg = '#962E12')#NOTE 
        self.current_target_lbl.grid(row = 0, column = 0, sticky = 'w', padx = 70)
        self.current_target_lbl = tk.Label(self.coords_frame, textvariable = self.target_coords_strvar, bg = '#962E12')
        self.current_target_lbl.grid(row = 1, column = 0, sticky = 'w', padx = 20)

        #Display current position
        self.current_pos_frame = tk.LabelFrame(self.target_frame, text = 'Current Position', width = 396, height = 80, bg = '#962E12')
        self.current_pos_frame.grid(row = 1, column = 0)
        self.current_pos_frame.grid_propagate(0)
        
        tk.Label(self.current_pos_frame, text = 'Current scope position : ', bg = '#962E12').grid(row = 0, column = 0, sticky = 'w', padx = 20)
        self.current_pos_lbl = tk.Label(self.current_pos_frame, textvariable = self.current_pos_strvar, bg = '#962E12')
        self.current_pos_lbl.grid(row =1, column = 0, sticky = 'w')
               
    def Vizualiation_widgets(self):
        # ------------------------ Camera vizualisation Frame ------------------------ #
        self.vizu_frame = tk.LabelFrame(self.Vizualisation, text = 'Camera', width = 643, height = 600)
        self.vizu_frame.grid(row = 0, column = 0)
        self.vizu_frame.grid_propagate(0)

        # --------------------------- Target Infos Frame --------------------------- #      
        #Display infos about target
        self.info_frame = tk.LabelFrame(self.Vizualisation, text = 'Infos', width = 643, height = 163, bg = '#962E12')
        self.info_frame.grid(row = 1, column = 0)
    
    def create_menu(self):
        #Create the Main menu bar
        self.menu_bar = tk.Menu(self)

        #Create file menu
        self.file_menu = tk.Menu(self.menu_bar)
        self.file_menu.add_command(label = 'New')
        self.file_menu.add_command(label = 'Open')
        self.file_menu.add_separator()
        self.file_menu.add_command(label = 'Quit', command = self.leave)
        self.menu_bar.add_cascade(menu = self.file_menu, label = 'File') #Add 'File' menu to Main menu bar
        
        #Create Options menu
        self.option_menu = tk.Menu(self.menu_bar)
        #Mount selection
        self.mount_choice = tk.Menu(self.option_menu)
        self.mount_choice.add_command(label = 'Dobson', command = self.dobson_mode)
        self.mount_choice.add_command(label = 'Azimutal', command = self.azimut_mode)
        self.mount_choice.add_command(label = 'Equatorial', command = self.equatorial_mode)
        self.option_menu.add_cascade(menu = self.mount_choice, label = 'Mount choice') #Add 'mount choice' menu to 'Options' menu
        self.menu_bar.add_cascade(menu = self.option_menu, label = 'Options') #Add 'Options' menu to Main menu bar

        #Window configuration
        self.config(menu = self.menu_bar)

# ---------------------------------- BackEnd --------------------------------- #

    def leave(self):
        """ A leave function to quit the Star Finder, with warning Msg Box """
        popup = msg.askokcancel(title = "Quit ?", message = 'Do you really want to quit Star Finder ?') #Warning popup
        if popup : #If 'OK' : leave the software
            self.quit()
            print('Left Star Finder')
    
    def Y_increment(self):
        self.current_position[0] += 1
        print('Y +1 : ', self.current_position)
        self.current_pos_strvar.set(self.current_position)
    def Y_decrement(self):
        self.current_position[0] -= 1
        print('Y -1 : ', self.current_position)
        self.current_pos_strvar.set(self.current_position)
    def X_increment(self):
        self.current_position[1] += 1
        print('X +1 : ', self.current_position)
        self.current_pos_strvar.set(self.current_position)
    def X_decrement(self):
        self.current_position[1] -= 1
        print('X -1 : ', self.current_position)
        self.current_pos_strvar.set(self.current_position)

    def dobson_mode(self):
        """ Set curent mode to 'Dobson Mode' """

        print('Entered in Dobson Mode')
        self.x_up.set('Azimut UP')
        self.x_down.set('Azimut DOWN')
        self.y_up.set('Altitude UP')
        self.y_down.set('Altitude DOWN')

    def azimut_mode(self):
        """ Set curent mode to 'Alt-Azimutal Mode' """

        print('Entered in Alt-azimutal Mode')
        self.x_up.set('Azimut UP')
        self.x_down.set('Azimut DOWN')
        self.y_up.set('Altitude UP')
        self.y_down.set('Altitude DOWN')       

    def equatorial_mode(self):
        """ Set curent mode to 'Equatorial Mode' """

        print('Entered in Equatorial Mode')
        self.x_up.set('Declinaison UP')
        self.x_down.set('Declinaison DOWN')
        self.y_up.set('Right Ascension UP')
        self.y_down.set('Right Ascension DOWN')

    def follow_mode(self):
        """ Active the Earth rotation follow system """
        print('Follow Mode State : '+self.flw_state)

    def update_catalog(self,x) :
        if self.slct_catalog.get() == '--Select a Catalog--':
            self.objects_list = ['--Select a Catalog--'] #Set value list to Header 'Select a catalog'
            self.slct_target['value'] = self.objects_list
            self.slct_target.current(0) #Set header as default selected value
            print('No Catalog') #Set current catalog to 'No catalog'
            self.current_catalog = 'None'

        if self.slct_catalog.get() == 'Messier':
            self.objects_list = list(self.messier.index)
            self.slct_target['value'] = ['--Select an Object--'] + self.objects_list #Set value list to Header 'Select an object' + Messier objects catalog
            self.slct_target.current(0) #Set header as default selected value
            self.current_catalog = 'Messier' #Set current catalog to 'Messier'
            print(f'Catalog updated : {self.current_catalog}')
            
        if self.slct_catalog.get() == 'NGC':
            self.objects_list =list(self.NGC.index)
            self.slct_target['value'] = ['--Select an Object--'] + self.objects_list
            self.slct_target.current(0) #Set header as default selected value
            self.current_catalog = 'NGC'
            print(f'Catalog updated : {self.current_catalog}') #Set current catalog to 'NGC'

        if self.slct_catalog.get() == 'Planets':
            self.objects_list = ['--Catalog not Available--']
            self.slct_target['value'] = self.objects_list
            self.slct_target.current(0) #Set header as default selected value
            self.current_catalog = 'Planets'
            print(f'Catalog updated : {self.current_catalog}') #Set current catalog to 'Planets''
        
        self.update_target(0) #! x = 0, see update_target() de
            
    def update_target(self,x):
        #! The 'x' parameter is due to the binding. It's not used but necessary, don't remove it
        self.current_target = self.slct_target.get() #Get the current target
        if self.current_catalog == 'None':
            self.current_target_strvar.set('No target')
            self.target_coords = (None)
            self.target_coords_strvar.set('No coordinates, choose a target')
            pass
        if self.current_catalog == 'Messier':
            if self.current_target == '--Select an Object--':
                coordinate = None
            else:
                RA = self.messier['Right ascension'][self.current_target]
                hour, others = RA.split('h ')
                minutes, others = others.split('m ')
                sec, others = others.split('s')
                RA = [hour, minutes, sec]

                Decl = self.messier['Declination'][self.current_target]
                sign = Decl[0] + '1'
                value = Decl[1:]
                deg, others = value.split('° ')
                degm, others = others.split("' ")
                degs, others = others.split('"')
                Decl = [sign, deg, degm, degs]
            
                coordinate = (RA, Decl) #Get the coordinates tuple
                print('--------------------------',coordinate)
            
            print('#------------------------Call reduce_to_sec()-------------------------#\n')
            self.target_coords = self.reduce_to_sec(coordinate)
            self.target_coords_strvar.set(coordinate)
            self.current_target_strvar.set(self.current_target) #Catch the current target in a StringVar to disply it with a label         
        if self.current_catalog == 'NGC':
            if self.current_target == '--Select an Object--':
                coordinate = None
            else :
                RA = [self.NGC['Rah'][self.current_target], self.NGC['Ram'][self.current_target], self.NGC['Ras'][self.current_target]]
                Decl = [np.sign(self.NGC['Decldeg'][self.current_target]), abs(float(self.NGC['Decldeg'][self.current_target])), self.NGC['Declm'][self.current_target], self.NGC['Decls'][self.current_target]]
                coordinate = (RA, Decl)
                print('------------------',coordinate)

            self.target_coords = self.reduce_to_sec(coordinate)
            self.target_coords_strvar.set(coordinate)
            self.current_target_strvar.set(self.current_target)
        if self.current_catalog == 'Planets':
            pass
        self.move()

    def reduce_to_sec(self, coords):
        """ Reduce the coords of the target to seconds andd arcseconds """
        print('Current target coords : ',coords)
        print('Current position : ',self.current_position)
        if coords != None:
            target_RA = float(coords[0][0]) * 3600 + float(coords[0][1]) * 60 + float(coords[0][2])
            target_Decl = float(coords[1][0]) * (float(coords[1][1]) * 3600 + float(coords[1][2]) * 60 + float(coords[1][3]))
            print('RA : ', target_RA, '\nDecl : ', target_Decl)
        else :
            a = None
            return a
    
    def move(self):
        if self.target_coords != None :
            print('#------------------------entered move()-------------------------#\n')
            deltaX = self.target_coords[0] - self.current_position[0]
            deltaY = self.target_coords[1] - self.current_position[1]
            print('Delta X : ',deltaX,'\nDelta Y : ', deltaY)
            print('#------------------------Left move()-------------------------#\n')
            return (deltaX, deltaY)

if __name__ == '__main__':
    Strfd = Star_finder()
    Strfd.title('Star Finder')
    Strfd.geometry('1920x720')
    Strfd.mainloop()
