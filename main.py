import csv
import math

# Import bolt list
f = open('Bolts.csv', 'r')
reader = csv.reader(f)
bolts = []

g = open('Bolts_class.csv', 'r')
class_reader = csv.reader(g)
bolts_class = []

# Check bolt importation
for row in reader:
    try:
        bolts.append([row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
    except ValueError:
        pass


for item in class_reader:
    try:
        bolts_class.append([str(item[0]), int(item[1])])
    except ValueError:
        pass
    print(item)


# Define Calculation Conditions

while True:
    # Tank
    while True:
        try:
            tank_diameter = float(input('Enter tank diameter: \n'))
            if tank_diameter <= 0:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    while True:
        try:
            tank_Young_modulus = float(input('Enter tank Young modulus [MPa]: \n'))
            if tank_Young_modulus <= 0:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    # Bolts

    bolt_size = str

    while True:
        try:
            bolt_size = str(input('Enter bolt size (example: M4, M8x1, M10...): \n'))
            if any([item[0] == bolt_size for item in bolts]):
                break
            else:
                print('Sorry, I don\'t have this bolt. \n')
        except ValueError:
            print('Sorry, I don\'t have this bolt. \n')
            break


    # Assign bolt parameters


    for row in bolts:
        if row[0] == bolt_size:
            print('Matching thread found! \n')
            thread_name = row[0]
            thread_diameter = row[1]
            pitch = row[2]
            pitch_diameter = row[3]
            core_diameter = row[4]
            bolt_hole = row[5]
        else:
            pass

    print('Thread name: ' + thread_name)
    print('Thread diameter: ' + str(thread_diameter) + ' [mm]')
    print('Thread pitch: ' + str(pitch) + ' [mm]')
    print('Thread pitch diameter: ' + str(pitch_diameter) + ' [mm]')
    print('Thread core diameter: ' + str(core_diameter) + ' [mm]')
    print('Bolt hole: ' + str(bolt_hole) + ' [mm] \n')

    bolt_class = str

    while True:
        try:
            bolt_class = str(input('Enter bolt clas (example: 5.6, 6.8, 10.9...): \n'))
            if any([item[0] == bolt_class for item in bolts_class]):
                break
            else:
                print('Sorry, I don\'t have this bolt class. \n')
        except ValueError:
            print('Sorry, I don\'t have this bolt class. \n')
            break

    for row in bolts_class:
        if row[0] == bolt_class:
            print('Matching class found! \n')
            bolt_class = row[0]
            R_e = row[1]
        else:
            pass

    print('Bolt class: ' + str(bolt_class))
    print('Yield strength: ' + str(R_e) + ' [MPa]')

    while True:
        try:
            bolt_number = int(input('Enter number of bolts: \n'))
            if bolt_number <= 0:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    while True:
        try:
            bolt_length = float(input('Enter bolt length: \n'))
            if bolt_length <= 0:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    while True:
        try:
            bolt_Young_modulus = float(input('Enter bolt Young modulus [MPa]: \n'))
            if bolt_Young_modulus <= 0:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    # Seal

    while True:
        try:
            seal_outer_diameter = float(input('Enter outer diameter of seal: \n'))
            break
        except ValueError:
            print('Wrong value \n')

    while True:
        try:
            seal_inner_diameter = float(input('Enter inner diameter of seal: \n'))
            if seal_inner_diameter > seal_outer_diameter:
                print('Inner diameter can\'t be bigger than outer \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    while True:
        try:
            seal_active_width = float(input('Enter active width of seal: \n'))
            break
        except ValueError:
            print('Wrong value \n')

    # Operating Conditions

    while True:
        try:
            pressure = float(input('Enter pressure in tank [bar]: \n'))
            if pressure < 0:
                print('Negative value \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    while True:
        try:
            safety_factor = float(input('Enter safety factor: \n'))
            if safety_factor <= 0:
                print('Negative value or zero \n')
            else:
                break
        except ValueError:
            print('Wrong value \n')

    # Bolts file closed
    f.close()
    g.close()

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

    print('Bolt stiffness: ' + str(format(c_s, '.2f')) + ' [N/mm]')

        #flange stiffnes

    # tg_zeta = 0.5
    S = 1.4158 * thread_diameter + 1.5798

    c_k = (2 / (math.pi * tank_Young_modulus * bolt_hole * 0.5)) * math.log((S + bolt_hole) * (S + (bolt_length * 0.5) - bolt_hole) / ((S - bolt_hole) * (S + (bolt_length * 0.5) + bolt_hole)),math.e)

    print('Flange stiffness: ' + str(format(c_k, '.10f')) + ' [mm/N]')

    Q_p = ((F_on_bolt * safety_factor) / bolt_number)

    print('Force on single bolt from inside pressure: ' + str(format(F_on_bolt, '.2f')) + ' [N]')

    Q_w = (1.25 * Q_p) / (1 + (c_s * c_k))  # preload in bolt (1,25 - 2,5)

    print('Preload on bolt: ' + str(format(Q_w, '.2f')) + ' [N]')

    Q = (0.2 * Q_w) + Q_p  # full force in bolt (0,2 - 0,6)

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