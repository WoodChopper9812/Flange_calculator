import csv
import math
import warnings

# Import bolt list
#f = open('Bolts.csv', 'r')
#reader = csv.reader(f)
#bolts = []

#g = open('Bolts_class.csv', 'r')
#class_reader = csv.reader(g)
#bolts_class = []

# Check bolt importation
#for row in reader:
#    try:
#        bolts.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
#    except ValueError:
#        pass


#for item in class_reader:
#    try:
#        bolts_class.append([str(item[0]), int(item[1])])
#    except ValueError:
#        pass

def extractValues(array, index=0):
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

def loadDatabase(boltsFileName="Bolts.csv", boltClassFileName="Bolts_class.csv", lessInfo=True):
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

def getVariable(message, vartype, nonNegative = False):
    var = vartype(0)
    while True:
        try:
            var = vartype(input(message))
            if var <= 0 and nonNegative:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')
    return var

def main():
    bolts, bolts_class = loadDatabase(lessInfo=False)
    # Tank
    
    tank_diameter = getVariable("Enter tank diameter:\n", float, nonNegative=True)
    tank_Young_modulus = getVariable("Enter tank Young modulus [MPa]:\n", float, nonNegative=True)

    # Bolts

    bolt_size = str

    while True:
        try:
            bolt_size = str(input('Enter bolt size (example: M4, M8x1, M10...): \n'))
            if (bolt_size in extractValues(bolts)):
                break
            else:
                print('Sorry, I don\'t have this bolt. \n')
        except ValueError:
            print('Sorry, I don\'t have this bolt. \n')
            break


    # Assign bolt parameters

    linenum=extractValues(bolts, 0).index(bolt_size, 0)
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

    bolt_class = str
    while True:
        try:
            bolt_class = input('Enter bolt clas (example: 5.6, 6.8, 10.9...): \n')
            if bolt_class in extractValues(bolts_class, 0):
                break
            else:
                print('Sorry, I don\'t have this bolt class. \n')
        except ValueError:
            print('Sorry, I don\'t have this bolt class. \n')
            break

    linenum = extractValues(bolts_class, 0).index(bolt_class)
    print('Matching class found! \n')
    bolt_class = bolts_class[linenum][0]
    R_e = bolts_class[linenum][1]

    print(f'Bolt class: {bolt_class}')
    print(f'Yield strength: {str(R_e)} [MPa]')

    bolt_number = getVariable("Enter number of bolts:\n", int, nonNegative=True)
    bolt_length = getVariable("Enter bolt length:\n", float, nonNegative=True)
    bolt_Young_modulus = getVariable("Enter bolt Young modulus [MPa]:\n", float, nonNegative=True)

    # Seal
    # ba-da-da, ba-da-da-da-da-da-da...
    seal_outer_diameter = getVariable("Enter outer diameter of seal:\n", float, False)
    # There used to be a greying tower alone on the sea...
    seal_inner_diameter = getVariable("Enter inner diameter of seal:\n", float, False)
    while(seal_inner_diameter>seal_outer_diameter):
        print("Seal inner diameter can't be bigger than the outer one!")
        seal_inner_diameter = getVariable("Enter inner diameter of seal:\n", float, False)
    # You became the ligh on the dark side of me
    seal_active_width = getVariable("Enter active width of seal:\n", float, False)

    # Operating Conditions
    
    pressure = getVariable("Enter pressure in tank [bar]:\n", float, True)
    safety_factor = getVariable("Enter safety factor:\n", float, True)

    # Forces acting on bolt
    F_pressure = math.pi * pressure * 101325 * (tank_diameter / 2000) ** 2
    F_residual = math.pi * ((seal_inner_diameter + seal_inner_diameter) / 2) * seal_active_width * (pressure / 10)
    F_on_bolt = F_residual + F_pressure

    print('Force from pressure: ' + str(format(F_pressure, '.2f')) + ' [N]')
    print('Force from residual tension: ' + str(format(F_residual, '.2f')) + ' [N]')
    print('Force acting on bolts: ' + str(format(F_on_bolt, '.2f')) + ' [N]')

    # Force in bolt and Preload on bolt

    # Source Mazanek

        #bolt stiffnes

    c_s = (math.pi * core_diameter **2 * bolt_Young_modulus) / (4 * bolt_length)

    

        #flange stiffnes

    # tg_zeta = 0.5
    S = 1.4158 * thread_diameter + 1.5798

    c_k = (
            (2 / (math.pi * tank_Young_modulus * bolt_hole * 0.5)) *
            math.log((S + bolt_hole) * 
            (S + (bolt_length * 0.5) - bolt_hole) / 
            ((S - bolt_hole) * (S + (bolt_length * 0.5) + bolt_hole)),math.e)
        )

    Q_p = ((F_on_bolt * safety_factor) / bolt_number)

    Q_w = (1.25 * Q_p) / (1 + (c_s * c_k))  # preload in bolt (1,25 - 2,5)

    Q = (0.2 * Q_w) + Q_p  # full force in bolt (0,2 - 0,6)
    
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

    safety_factor_cal = (R_e / sigma) * safety_factor

    print('Safety factor calculated: ' + str(format(safety_factor_cal, '.2f')) + '\n')


# Define Calculation Conditions
if __name__=="__main__":
    while True:
        main()    