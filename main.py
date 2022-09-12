import csv
import math
import numpy as np
import warnings
import matplotlib
# just to make it more universal it is good to turn off graphical mode
#matplotlib.use("Agg")
import matplotlib.pyplot as plt

class sft():
    def __init__(self):
        self.bolts=None
        self.bolt_class=None
        self.tank_diameter=None
        self.tank_Young_modulus=None
        self.bolt_index=None
        self.bolt_size=None
        self.bolt_number=None
        self.bolt_length=None
        self.bolt_Young_modulus=None
        self.seal_outer_diameter=None
        self.seal_inner_diameter=None
        self.seal_active_width=None
        self.pressure=None
        self.safety_factor=None
        self.main()

    def extractValues(self, array, index=0):
        '''
        Exctracts values from specific indexes from list's subararray.
        Arguments:
        -> array ([[...], ...]) - 2D array
        -> index (int) - index of values exctracted from subarrays
        Returns:
        -> array ([...]) - list of required values from arrays
        Raises:
        -> None.
        '''
        return [item[index] for item in array]

    def loadDatabase(self, boltsFileName="Bolts.csv", boltClassFileName="Bolts_class.csv", lessInfo=True):
        '''
        Loads all required databases and returns
        them in form of lists.
        Arguments:
        -> boltsFileName (string) - name of the bolts database file,
        -> boltClassFileName (string) - name of the bolt classes file,
        -> lessInfo (bool) - debugging messages flag. Prints messages if False
        Returns:
        -> bolts ([[string, float, ...], ...]) - array of available bolt names
        -> bolts_class ([[string, float], ...]) - array of available bolt classes
        Raises:
        -> warnings - if a ValueError appears during file loading and lessInfo flag is set to False
        -> exception:
            - if other error is encountered during file loading
            - if a wrong variable type is provided as arguments
        '''
        # returnable arrays
        bolts = []
        bolts_class = []
        # checking provided names
        if(not isinstance(boltsFileName, str)):
            raise Exception(f"Wrong type of boltsFileName. Expected str, got {type(boltsFileName)}")
        if(not isinstance(boltClassFileName, str)):
            raise Exception(f"Wrong type of boltClassFileName. Expected str, got {type(boltClassFileName)}")
        # Files to download the databases from
        f = open(boltsFileName, 'r')
        g = open(boltClassFileName, 'r')
        if(f==None or g==None):
            raise Exception("An error occured while loading database files")
        # File streams to databases
        reader = csv.reader(f)
        class_reader = csv.reader(g)
        
        # loading bolt names
        if(not lessInfo):
            print("Loading bolt database")
        for linenum, row in enumerate(reader):
            try:
                for num, item in enumerate(row):
                    if (num==0):
                        bolts.append([row[num]])
                    else:
                        bolts[-1].append(float(row[num]))
            except ValueError:
                if(not lessInfo):
                    warnings.warn(f"[Bolts] Could not load a value from line {linenum}")
        # loading bolt classes
        print("Loading bolt class database")
        for linenum, row in enumerate(class_reader):
            try:
                bolts_class.append([str(row[0]), int(row[1])])
            except ValueError:
                warnings.warn(f"[Bolt class] Could not load a value from line {linenum}")
            except:
                raise Exception(f"[Bolt class] Could not load database file. Error @ {linenum}.")
        # closing files
        f.close()
        g.close()
        
        #returning arrays
        return bolts, bolts_class

    def getVariable(self, message, vartype, nonNegative = False, nonZero=False):
        var = vartype(0)
        while True:
            try:
                var = vartype(input(message))
                if var < 0 and nonNegative:
                    print('Negative value\n')
                else:
                    if(var==0 and nonZero):
                        print("Value cannot be zero\n")
                    else:
                        break
            except ValueError:
                print('Wrong value \n')
        return var

    def lookUpValue(self, name, kwargs, text="", vartype=float, nonNegative=True, nonZero=False):
        if(name in kwargs):
            return kwargs[name]
        return self.getVariable(text, vartype, nonNegative, nonZero)

    def findBoltSize(self, bolts, bolt_size=None, mode="size"):
        while True:
            if(bolt_size==None):
                if(mode=="size"):
                    bolt_size = str(input("Enter bolt size (example: M4, M8x1, M10...): \n"))
                if(mode=="class"):
                    bolt_size = input('Enter bolt clas (example: 5.6, 6.8, 10.9...): \n')
                if (bolt_size in self.extractValues(bolts)):
                    break
                else:
                    if(mode=="size"):
                        print("Sorry, I don't have this bolt. \n")
                    if(mode=="class"):
                        print('Sorry, I don\'t have this bolt class. \n')
                    bolt_size=None
            else:
                if(mode=="size"):
                    if(bolt_size not in self.extractValues(bolts)):
                        raise Exception(f"Could not find specified bolt size: {bolt_size}")
                if(mode=="class"):
                    if(bolt_size not in self.extractValues(bolts)):
                        raise Exception(f"Could not find specified bolt class: {bolt_size}")
                break
        return bolt_size

    def iterateByXY(self, numberOfBolts, BoltSizeIndex):
        return self.main(bolt_number=numberOfBolts, bolt_index=BoltSizeIndex)

    def main(self, bolts = None, bolts_class = None, lessInfo = True, **kwargs):
        bolt_index = None
        if(self.bolts==None or self.bolts_class==None):
            if(bolts == None or bolts_class == None):
                bolts, bolts_class = self.loadDatabase(lessInfo=False)
        if(bolts==None or bolts_class==None):
            bolts=self.bolts
            bolts_class = self.bolts_class

        if("bolt_index" in kwargs):
            bolt_index=kwargs["bolt_index"]

        self.bolts = bolts
        self.bolts_class = bolts_class
        
        # Tank
        if(self.tank_diameter==None):
            self.tank_diameter = self.lookUpValue("tank_diameter", kwargs, "Enter tank diameter:\n", float, True)
        if(self.tank_Young_modulus==None):
            self.tank_Young_modulus = self.lookUpValue("tank_Young_modulus", kwargs, "Enter tank Young modulus [MPa]:\n", float, True)

        # Bolts
        if(bolt_index==None):
            if(self.bolt_size==None):
                if("bolt_size" in kwargs):
                    self.bolt_size = self.findBoltSize(bolts, bolt_size=kwargs["bolt_size"])
                else:
                    self.bolt_size = self.findBoltSize(bolts)
        else:
            self.bolt_size = bolts[bolt_index][0]


        # Assign bolt parameters
        linenum=self.extractValues(bolts, 0).index(self.bolt_size, 0)
        print('Matching thread found! \n')
        thread_name = bolts[linenum][0]
        thread_diameter = bolts[linenum][1]
        pitch = bolts[linenum][2]
        pitch_diameter = bolts[linenum][3]
        core_diameter = bolts[linenum][4]
        bolt_hole = bolts[linenum][5]
        
        print('Thread name: ' + thread_name)
        print('Thread diameter: ' + str(thread_diameter) + ' [mm]')
        print('Thread pitch: ' + str(pitch) + ' [mm]')
        print('Thread pitch diameter: ' + str(pitch_diameter) + ' [mm]')
        print('Thread core diameter: ' + str(core_diameter) + ' [mm]')
        print('Bolt hole: ' + str(bolt_hole) + ' [mm] \n')

        if(self.bolt_class==None):
            if("bolt_class" in kwargs):
                self.bolt_class = self.findBoltSize(bolts_class, bolt_size=kwargs["bolt_class"], mode="class")
            else:
                self.bolt_class = self.findBoltSize(bolts_class, mode="class")

        linenum = self.extractValues(bolts_class, 0).index(self.bolt_class)
        print('Matching class found! \n')
        self.bolt_class = bolts_class[linenum][0]
        R_e = bolts_class[linenum][1]

        print(f'Bolt class: {self.bolt_class}')
        print(f'Yield strength: {str(R_e)} [MPa]\n')

        if(self.bolt_number==None):
            self.bolt_number = self.lookUpValue("bolt_number", kwargs, "Enter number of bolts:\n", int, nonNegative=True, nonZero=True)
        if(self.bolt_length==None):
            self.bolt_length = self.lookUpValue("bolt_length", kwargs, "Enter bolt active length:\n", float, nonNegative=True, nonZero=True)
        if(self.bolt_Young_modulus==None):
            self.bolt_Young_modulus = self.lookUpValue("bolt_Young_modulus", kwargs, "Enter bolt Young modulus [MPa]:\n", float, nonNegative=True, nonZero=True)

        # Seal
        # ba-da-da, ba-da-da-da-da-da-da...
        if(self.seal_outer_diameter==None):
            self.seal_outer_diameter = self.lookUpValue("seal_outer_diameter", kwargs, "Enter outer diameter of seal:\n", float, True, nonZero=False)
        # There used to be a greying tower alone on the sea...
        if(not self.seal_outer_diameter==0 and self.seal_inner_diameter==None):
            self.seal_inner_diameter = self.lookUpValue("seal_inner_diameter", kwargs, "Enter inner diameter of seal:\n", float, True, nonZero=False)
        else:
            if(self.seal_inner_diameter==None):
                self.seal_inner_diameter = 0
        while((self.seal_inner_diameter>self.seal_outer_diameter or self.seal_inner_diameter<self.tank_diameter) and not self.seal_inner_diameter==0):
            print("Seal inner diameter can't be bigger than the outer one!")
            if("seal_inner_diameter" in kwargs):
                raise Exception("Wrong seal inner diameter!")
            self.seal_inner_diameter = self.getVariable("Enter inner diameter of seal:\n", float, True)
        # You became the light on the dark side of me
        if(not self.seal_outer_diameter==0 and self.seal_active_diameter==None):
            self.seal_active_width = self.lookUpValue("seal_active_width", kwargs, "Enter active width of seal:\n", float, True)
        else:
            if(self.seal_active_width==None):
                self.seal_active_width = 0
        while (self.seal_active_width>((self.seal_outer_diameter-self.seal_inner_diameter)/2) and not self.seal_active_width==0):
            print("Seal active width can't be bigger than seal with!")
            if("seal_inner_diameter" in kwargs):
                raise Exception("Wrong seal active width!")
            self.seal_active_width = self.getVariable("Enter active width of seal:\n", float, True)

        # Operating Conditions
        
        if(self.pressure==None):
            self.pressure = self.lookUpValue("pressure", kwargs, "Enter pressure in tank [bar]:\n", float, True, True)
        if(self.safety_factor==None):
            self.safety_factor = self.lookUpValue("safety_factor", kwargs, "Enter safety factor:\n", float, True, True)

        # Forces acting on bolt
        F_pressure = math.pi * self.pressure * 101325 * (self.tank_diameter / 2000) ** 2
        F_residual = math.pi * ((self.seal_inner_diameter + self.seal_inner_diameter) / 2) * self.seal_active_width * (self.pressure / 10)
        F_on_bolt = F_residual + F_pressure

        print('Force from pressure: ' + str(format(F_pressure, '.2f')) + ' [N]')
        print('Force from residual tension: ' + str(format(F_residual, '.2f')) + ' [N]')
        print('Force acting on bolts: ' + str(format(F_on_bolt, '.2f')) + ' [N]')

        # Force in bolt and Preload on bolt

        # Source Mazanek

            #bolt stiffnes

        c_s = (math.pi * core_diameter **2 * self.bolt_Young_modulus) / (4 * self.bolt_length)

        

            #flange stiffnes

        # tg_zeta = 0.5
        S = 1.4158 * thread_diameter + 1.5798

        c_k = (
                (2 / (math.pi * self.tank_Young_modulus * bolt_hole * 0.5)) *
                math.log((S + bolt_hole) * 
                (S + (self.bolt_length * 0.5) - bolt_hole) / 
                ((S - bolt_hole) * (S + (self.bolt_length * 0.5) + bolt_hole)),math.e)
            )

        Q_p = ((F_on_bolt * self.safety_factor) / self.bolt_number)

        Q_w = (1.25 * Q_p) / (1 + (c_s * c_k))  # preload in bolt (1.25 - 2.5)

        Q = (0.2 * Q_w) + Q_p  # full force in bolt (0.2 - 0.6)
        
        print('Bolt stiffness: ' + str(format(c_s, '.2f')) + ' [N/mm]')
        print('Flange stiffness: ' + str(format(c_k, '.10f')) + ' [mm/N]')
        print('Force on single bolt from inside pressure: ' + str(format(F_on_bolt, '.2f')) + ' [N]')
        print('Preload on bolt: ' + str(format(Q_w, '.2f')) + ' [N]')
        print('Full force in bolt: ' + str(format(Q, '.2f')) + ' [N]')



        # Torque calculation

        beta_deg = 30  # Half of thread angle
        beta_rad = beta_deg * math.pi / 180
        mi_t = 0.12  # Friction coefficient in thread
        mi_n = 0.14  # Friction coefficient under bolt head
        gamma = 2  # Ratio max min contact radius
        r_n = ((gamma + 1) * thread_diameter) / 4  # Active bolt head radius
        r_t = pitch_diameter / 2  # Active pitch radius

        # Source "AN INTRODUCTION TO THE DESIGN AND BEHAVIOR OF BOLTED JOINTS THIRD EDITION,REVISED AND EXPANDED"
        # John H. Bickford

        Torque = F_on_bolt * ((pitch / (2 * math.pi)) + ((mi_t * r_t) / math.cos(beta_rad)) + (mi_n * r_n))  # N*mm

        print('Torque required on bolt: ' + str(format(Torque / 1000, '.2f')) + ' [Nm]')

        # Stress in bolt

        sigma_r = ((4 * Q) / (math.pi * (core_diameter ** 2))) ** 2
        M_t = (0.5 * pitch_diameter * Q * math.tan(math.atan((pitch)/(math.pi * pitch_diameter) + math.atan( 0.1 / (math.cos(30 * math.pi / 180))))))
        tau = (M_t * (16 / (math.pi * (core_diameter ** 3)))) ** 2
        sigma = math.sqrt(sigma_r + 3 * tau)

        print('Stress in bolt: ' + str(format(sigma, '.2f')) + ' [MPa]')

        # Safety factor

        safety_factor_cal = (R_e / sigma) * self.safety_factor

        print('Safety factor calculated: ' + str(format(safety_factor_cal, '.2f')) + '\n')

        return safety_factor_cal


# Define Calculation Conditions
if __name__=="__main__":
    mn = sft()
    #for i in range(3, math.floor(1.5*mn.bolt_number)):
    #    for o in range(1, len(mn.extractValues(mn.bolts))):
    #        mn.main(
    #                bolts=mn.bolts,
    #                bolt_class=mn.bolt_class,
    #                tank_diameter=mn.tank_diameter,
    #                tank_Young_modulus=mn.tank_Young_modulus,
    #                bolt_index=o,
    #                bolt_number=i,
    #                bolt_length=mn.bolt_length,
    #                bolt_Young_modulus=mn.bolt_Young_modulus,
    #                seal_outer_diameter=mn.seal_outer_diameter,
    #                seal_inner_diameter=mn.seal_inner_diameter,
    #                seal_active_width=mn.seal_active_width,
    #                pressure=mn.pressure,
    #                safety_factor=mn.safety_factor,
    #                lessInfo=False
    #            )
    
    fig = plt.figure(figsize=(35./5., 30./5.), dpi = 1920/35*5)
    ax = fig.add_subplot(111)

    x_tab = np.linspace(3, 2000, num=28, dtype=int)
    y_tab = np.linspace(1, len(mn.extractValues(mn.bolts))-1, len(mn.extractValues(mn.bolts))-1, dtype=int)
    tb = np.zeros((len(x_tab)*len(y_tab), 3))
    for i in range(len(x_tab)):
        for o in range(len(y_tab)):
            tb[i*len(y_tab)+o, 0] = x_tab[i]
            tb[i*len(y_tab)+o, 1] = y_tab[o]
            tb[i*len(y_tab)+o, 2] = mn.iterateByXY(x_tab[i], y_tab[o])
    cont = ax.tricontourf(tb[:,0], tb[:,1], tb[:,2], cmap='jet', levels=np.linspace(np.min(tb[:, 2]), np.max(tb[:, 2]), num=1000))
    plt.show()
    