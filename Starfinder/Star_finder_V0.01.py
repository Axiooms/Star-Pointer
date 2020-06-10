#Imports
import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
import time
import pandas as pd

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

        self.messier = pd.read_csv('catalogs/messier-objects.csv', sep = ';') #Messier
        self.NGC = pd.read_excel('catalogs/ngc-ic2000.xls') #NGC

        #Clean datasets
        self.messier = self.messier.drop(['Picture', 'Distance(kly)','Apparent magnitude'], axis = 1) #Drop all useless columns
        for element in range(len(self.messier)):  #If no data, replace by the Messier Number
            if str(self.messier['Common name'][element])[0].lower() not in 'abcdefghijklmnstuvwxyz ': 
                self.messier['Common name'][element] = self.messier['Messier number'][element]
        self.messier = self.messier.set_index(['Common name']) #Change 'Common name' column into dataset index
        
        #Catalogs variables
        self.current_catalog = 'None' 
        self.catalog_list = ['--Select a Catalog--', 'Planets', 'Messier', 'NGC']    
        
        #Target variables
        self.objects_list = ['--Select a Catalog--']
        self.current_target = None
        self.target_coords = tk.StringVar()
        self.target_coords.set(None)
        self.current_target_strvar = tk.StringVar()     
        self.current_target_strvar.set('No target')
        
# ----------------------------------- Front End ---------------------------------- #

    def create_frames(self):
        """ Create the main Frames """
        #NOTE this function is debugged and clean

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
        #NOTE This function is debugged and clean

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

        def sdrl_clock():
            """ A sidereal datetime clock """
            sdrl_datetime = time.strftime('Date : %d / %m / %Y  -- Hour : %H h %M min %S sec')
            self.sdrl_date_lbl.config(text = sdrl_datetime)
            self.sdrl_date_lbl.after(1000, sdrl_clock)

        #Display Local date 
        self.lcl_date_lbl = tk.Label(self.date_frame, text = ' Local Date : 00:00:00 xx/xx/xxxx', bg = '#962E12')
        self.lcl_date_lbl.grid(row = 1, column = 0, sticky = 'w', padx = 20)
        #Display Siderel date 
        self.sdrl_date_lbl = tk.Label(self.date_frame, text = ' Sidereal Date : 00:00:00 xx/xx/xxxx', bg = '#962E12')
        self.sdrl_date_lbl.grid(row = 2, column = 0, sticky = 'w', padx = 20)
        lcl_clock()
        sdrl_clock()

    def Commands_widgets(self):

        #-------------------------------------- Command Buttons --------------------------------------#
        #Command Buttons Frame
        self.btn_frame = tk.LabelFrame(self.Commands, text = 'Command Buttons', bg = '#962E12', width = 400, height = 150)
        self.btn_frame.grid(row = 0, column = 0, sticky = 'w', padx = 22)
        self.btn_frame.grid_propagate(0)

        #X axis 'Up' and 'Down' Buttons
        self.X_up = tk.Button(self.btn_frame, textvariable = self.x_up, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20)
        self.X_up.grid(row = 1, column = 0, padx = 30, pady = 25) #! padx of buttons is set only here
        self.X_down = tk.Button(self.btn_frame, textvariable = self.x_down, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20)
        self.X_down.grid(row = 1, column = 1, pady = 25)
    
        #Y axis 'Up' and 'Down' Buttons
        self.Y_up = tk.Button(self.btn_frame, textvariable = self.y_up, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20)
        self.Y_up.grid(row = 5, column = 0, padx = 10)
        self.Y_down = tk.Button(self.btn_frame, textvariable = self.y_down, bd = 2, bg = '#9B8866', activebackground = '#5d513d', width = 20)
        self.Y_down.grid(row = 5, column = 1)
        
        #-------------------------------------- Follow Mode Activator --------------------------------------#
        #Follow Mode Frame
        self.flw_frame = tk.LabelFrame(self.Commands, text = 'Des / Activate Follow Mode', bg = '#962E12', width = 400, height = 50)
        self.flw_frame.grid(row = 1, column = 0, sticky = 'w', padx = 22, pady = 25)
        self.flw_frame.grid_propagate(0)

        #Follow Mode activator
        self.flw_btn = tk.Checkbutton(self.flw_frame, text = 'Follow Mode', variable =  self.flw_state, onvalue = 1, offvalue = 0, 
                                      command = self.follow_mode, bg = '#962E12', activebackground = '#962E12')
        self.flw_btn.grid(row = 9, column = 0, columnspan = 2, sticky = 'w', padx = 160)

        #-------------------------------------- Targetable Objects List --------------------------------------#
        #Targetable Objects Frame
        self.current_target_frame = tk.LabelFrame(self.Commands, text = 'Target Selection', bg = '#962E12', width = 400, height = 80)
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
        
    def Vizualiation_widgets(self):
        # ------------------------ Camera vizualisation Frame ------------------------ #
        self.vizu_frame = tk.LabelFrame(self.Vizualisation, text = 'Camera', width = 643, height = 600)
        self.vizu_frame.grid(row = 0, column = 0)
        self.vizu_frame.grid_propagate(0)

        # --------------------------- Target Frame --------------------------- #
        #Target Frame
        self.target_frame = tk.LabelFrame(self.Vizualisation, text = 'Current Target', width = 643, height = 163, bg = '#962E12')
        self.target_frame.grid(row = 1, column = 0)
        self.target_frame.grid_propagate(0)
        
        #Coords Frame
        self.coords_frame = tk.LabelFrame(self.target_frame, text = 'Coordinates', width = 321, height = 163, bg = '#962E12')
        self.coords_frame.grid(row = 0, column = 0)
        self.coords_frame.grid_propagate(0)

        #Display current target name and coordinates
        self.current_target_lbl = tk.Label(self.coords_frame, textvariable = self.current_target_strvar, bg = '#962E12')
        self.current_target_lbl.grid(row = 0, column = 0, sticky = 'w', padx = 20)
        self.current_target_lbl = tk.Label(self.coords_frame, textvariable = self.target_coords, bg = '#962E12')
        self.current_target_lbl.grid(row = 0, column = 1, sticky = 'w', padx = 20, pady = 10)
       
        #Display infos about target
        self.info_frame = tk.LabelFrame(self.target_frame, text = 'Infos', width = 643, height = 163, bg = '#962E12')
        self.info_frame.grid(row = 0, column = 1)

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
            print('update catalog list')
            self.objects_list = list(self.messier.index)
            self.slct_target['value'] = ['--Select an Object--'] + self.objects_list #Set value list to Header 'Select an object' + Messier objects catalog
            self.slct_target.current(0) #Set header as default selected value
            self.current_catalog = 'Messier' #Set current catalog to 'Messier'
            print('Catalog updated')
            
        if self.slct_catalog.get() == 'NGC':
            self.objects_list = ['--Catalog not Available--']
            self.slct_target['value'] = self.objects_list
            self.slct_target.current(0) #Set header as default selected value
            self.current_catalog = 'NGC'
            print('Catalog updated') #Set current catalog to 'NGC'

        if self.slct_catalog.get() == 'Planets':
            self.objects_list = ['--Catalog not Available--']
            self.slct_target['value'] = self.objects_list
            self.slct_target.current(0) #Set header as default selected value
            self.current_catalog = 'Planets'
            print('Catalog updated') #Set current catalog to 'Planets''
        
        self.update_target(0) #! x = 0, see update_target() de
            
    def update_target(self,x):
        #! The 'x' parameter is due to the binding. It's necessary, don't remove it
        self.current_target = self.slct_target.get() #Get the current target
        print('in fct ',self.current_target)
        if self.current_catalog == 'None':
            self.current_target_strvar.set('No target')
            self.target_coords.set('No coordinates, choose a target')
            pass
        if self.current_catalog == 'Messier':
            coordinate = (self.messier['Right ascension'][self.current_target],self.messier['Declination'][self.current_target]) #Get the coordinates tuple
            self.target_coords.set(coordinate)
            self.current_target_strvar.set(self.current_target) #Catch the current target in a StringVar to disply it with a label  
        if self.current_catalog == 'NGC':
            pass
        if self.current_catalog == 'Planets':
            pass

if __name__ == '__main__':
    Strfd = Star_finder()
    Strfd.title('Star Finder')
    Strfd.geometry('1920x720')
    Strfd.mainloop()
