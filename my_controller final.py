#Team search final controller

from controller import Robot


robot = Robot()
timestep = int(robot.getBasicTimeStep())

motor_list=['front_right_wheel',
            'front_left_wheel',
            ]
            
sensor_list=['ir_ext_right','ir_right','ir_ext_left','ir_left',
            'ir_cent_left','ir_cent_right',
            'ir_left_2',
            'ir_right_2',
            'ir_ext_right_back','ir_right_back','ir_ext_left_back','ir_left_back',
            'ir_cent_left_back','ir_cent_right_back','ir_left_2_back','ir_right_2_back',
            'wall_front','wall_back']

motor=dict()
sensor=dict()

for m in motor_list:
    motor[m] = robot.getDevice(m)
    motor[m].setPosition(float('inf'))
    motor[m].setVelocity(0.0)
    
for s in sensor_list:
    sensor[s] = robot.getDevice(s)
    sensor[s].enable(timestep)

last_error=prop=intg=diff=waitCounter=0
kp=0.025
ki=0.00001
kd=0.08
obst = 0
slowZone = 0
doorwayLength = 500

def pid(b,error):
    global last_error, intg, diff, prop, kp, ki, kd
    prop = error
    intg = error + intg
    diff = error - last_error
    last_error = error
    balance = (kp*prop) + (ki*intg) + (kd*diff)
    rectify = balance
    print(balance)
    rectl=rectify
    rectr=rectify
    max=int("20")
    
    if b+rectify>max:
        print("L>max")
        rectl=max-b
    if b-rectify>max:
        print("R>max")
        rectr=b-max
    if b+rectify<-1*max:
        print("L<max")
        rectl=-b-max
    if b-rectify<-1*max:
        print("R<max")
        rectr=b+max
          
    set_motor_speed(b+rectl,b-rectr)
    return balance
        
def set_motor_speed(left_speed, right_speed):
    print(left_speed,right_speed)
    motor['front_right_wheel'].setVelocity(right_speed)
    motor['front_left_wheel'].setVelocity(left_speed)

def cross_junct(ir_r_val,ir_l_val):
    while (robot.step(timestep) != -1) and (ir_r_val<950 and ir_l_val<950):
        ir_r_val = sensor['ir_right'].getValue()
        ir_l_val = sensor['ir_left'].getValue()
        print("while")
        set_motor_speed(10,10)

def line_90_l(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2):
    print("line 90 left")
    set_motor_speed(-5,5)
    while (robot.step(timestep) != -1) and (ir_r_2<950 and ir_l_2<950):
        print("while")
        ir_r_val = int(sensor['ir_right'].getValue())
        ir_l_val = int(sensor['ir_left'].getValue())
        ir_r_ext_val = int(sensor['ir_ext_right'].getValue())
        ir_l_ext_val = int(sensor['ir_ext_left'].getValue())
        ir_r_c = int(sensor['ir_cent_right'].getValue())
        ir_l_c = int(sensor['ir_cent_left'].getValue())
        ir_r_2 = int(sensor['ir_right_2'].getValue())
        ir_l_2 = int(sensor['ir_left_2'].getValue())
        
        if ir_r_ext_val<850 and ir_l_ext_val>850:
            set_motor_speed(5,-5)
        elif ir_r_ext_val>850 and ir_l_ext_val<850:
            set_motor_speed(-5,5)
        elif (ir_r_val<350 or ir_l_val<350) and ir_r_ext_val<850:
            set_motor_speed(10,-5)
        elif (ir_r_val<350 or ir_l_val<350) and ir_l_ext_val<850:
            set_motor_speed(-5,10)
        elif ir_r_val<350 and ir_l_2<350 and ir_l_val>950:
            set_motor_speed(-5,5)
        elif ir_r_2<350 and ir_l_val<350 and ir_r_val>950:
            set_motor_speed(-5,5)
        elif ir_r_c<850 and ir_l_c<850 and ir_r_val<850 and ir_l_val<850:
            print("gooo")
            set_motor_speed(3,3)
        elif ir_r_c<950 and ir_l_c<950:
            print("gooo")
            set_motor_speed(20,20)
        else:
            pass

def line_90_r(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2):
    print("line 90 right")
    set_motor_speed(5,-5)
    while (robot.step(timestep) != -1) and (ir_r_2<950 and ir_l_2<950):
        print("while")
        ir_r_val = int(sensor['ir_right'].getValue())
        ir_l_val = int(sensor['ir_left'].getValue())
        ir_r_ext_val = int(sensor['ir_ext_right'].getValue())
        ir_l_ext_val = int(sensor['ir_ext_left'].getValue())
        ir_r_c = int(sensor['ir_cent_right'].getValue())
        ir_l_c = int(sensor['ir_cent_left'].getValue())
        ir_r_2 = int(sensor['ir_right_2'].getValue())
        ir_l_2 = int(sensor['ir_left_2'].getValue())
        
        if ir_r_ext_val<850 and ir_l_ext_val>850:
            set_motor_speed(5,-5)
        elif ir_r_ext_val>850 and ir_l_ext_val<850:
            set_motor_speed(-5,5)
        elif (ir_r_val<350 or ir_l_val<350) and ir_r_ext_val<850:
            set_motor_speed(10,-5)
        elif (ir_r_val<350 or ir_l_val<350) and ir_l_ext_val<850:
            set_motor_speed(-5,10)
        elif ir_r_val<350 and ir_l_2<350 and ir_l_val>950:
            set_motor_speed(5,-5)
        elif ir_r_2<350 and ir_l_val<350 and ir_r_val>950:
            set_motor_speed(5,-5)
        elif ir_r_c<850 and ir_l_c<850 and ir_r_val<850 and ir_l_val<850:
            print("gooo")
            set_motor_speed(3,3)
        elif ir_r_c<950 and ir_l_c<950:
            print("gooo")
            set_motor_speed(20,20)
        else:
            pass       

def line_follow(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2,wall_f,wall_b):
    global j_count,ob_count,ob_l,ob_r   
    if ir_r_2<950 and ir_l_2<950:
        if ir_r_val<350 and ir_l_val<350 and ir_r_ext_val<850 and ir_l_ext_val<850:
            print("Junction")
            j_count=j_count+1
            cross_junct(ir_r_ext_val,ir_l_ext_val)
            
        elif ir_r_ext_val<850 and ir_l_ext_val>850:
            line_90_r(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2)
        elif ir_r_ext_val>850 and ir_l_ext_val<850:
            line_90_l(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2)
        
        elif (ir_r_val<350 or ir_l_val<350) and ir_r_ext_val<850:
            set_motor_speed(10,-5)
        elif (ir_r_val<350 or ir_l_val<350) and ir_l_ext_val<850:
            set_motor_speed(-5,10)
        elif ir_r_val<350 and ir_l_2<350 and ir_l_val>950:
            set_motor_speed(-5,5)
        elif ir_r_2<350 and ir_l_val<350 and ir_r_val>950:
            set_motor_speed(-5,5)
        elif ir_r_c<850 and ir_l_c<850 and ir_r_val<850 and ir_l_val<850:
            print("go")
            set_motor_speed(3,3)
        elif ir_r_c<950 and ir_l_c<950:
            print("go")
            set_motor_speed(20,20)
        else:
            pass
    
    #right senser out of white line    
    elif ir_r_2>950 and ir_l_2<950:
        if ir_r_c<950:
            set_motor_speed(5,15)
        elif ir_r_c>950:
            set_motor_speed(0,10)
        else:
            pass
    
    #left senser out of white line      
    elif ir_r_2<950 and ir_l_2>950:
        if ir_r_c<950 and ir_l_c<950:
            set_motor_speed(15,5)
        elif ir_l_c>950:
            set_motor_speed(10,0)
        else:
            pass
    else:
        print("elseee")

def edge_follow_rw(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2,wall_f,wall_b):
    if ir_r_c<950 and ir_l_c>950:
        set_motor_speed(10,10)
        
    #drifting towards right   
    elif ir_l_c<950:
        if ir_l_2>950:
            set_motor_speed(10,7.5)
        elif ir_l_2<950:
            set_motor_speed(2.5,-1.5)
        else:
            pass
    
    #drift left      
    elif ir_r_c>950:
        if ir_r_2<950:
            set_motor_speed(7.5,10)
        elif ir_r_2>950:
            set_motor_speed(-1.5,2.5)
        else:
            pass
    else:
        print("elseee")
    
def edge_follow_lw(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2,wall_f,wall_b):
    if ir_r_c>950 and ir_l_c<950:
        set_motor_speed(10,10)
    
    #drifting towards right   
    elif ir_l_c>950:
        if ir_l_2<950:
            set_motor_speed(10,7.5)
        elif ir_l_2>950:
            set_motor_speed(2.5,-1.5)
        else:
            pass
    
    #drift left      
    elif ir_r_c<950:
        if ir_r_2>950:
            set_motor_speed(7.5,10)
        elif ir_r_2<950:
            set_motor_speed(-1.5,2.5)
        else:
            pass
    else:
        print("elseee")  
        
def edge_follow_rw_obst(ir_r_val_back,ir_l_val_back,ir_r_ext_val_back,ir_l_ext_val_back,ir_r_c_back,ir_l_c_back,ir_r_2_back,ir_l_2_back, wall_f,wall_b):
    if ir_r_c_back<950 and ir_l_c_back>950:
        set_motor_speed(-10,-10)
        
    #drifting towards right   
    elif ir_l_c_back<950:
        if ir_l_2_back>950:
            set_motor_speed(-10,-7.5)
        elif ir_l_2_back<950:
            set_motor_speed(-2.5,1.5)
        else:
            pass
    
    #drift left      
    elif ir_r_c_back>950:
        if ir_r_2_back<950:
            set_motor_speed(-7.5,-10)
        elif ir_r_2_back>950:
            set_motor_speed(1.5,-2.5)
        else:
            pass
    else:
        print("elseee")
    
def edge_follow_lw_obst(ir_r_val_back,ir_l_val_back,ir_r_ext_val_back,ir_l_ext_val_back,ir_r_c_back,ir_l_c_back,ir_r_2_back,ir_l_2_back, wall_f,wall_b):
    if ir_r_c_back>950 and ir_l_c_back<950:
        set_motor_speed(-10,-10)
    
    #drifting towards right   
    elif ir_l_c_back>950:
        if ir_l_2_back<950:
            set_motor_speed(-10,-7.5)
        elif ir_l_2_back>950:
            set_motor_speed(-2.5,1.5)
        else:
            pass
    
    #drift left      
    elif ir_r_c_back<950:
        if ir_r_2_back>950:
            set_motor_speed(-7.5,-10)
        elif ir_r_2_back<950:
            set_motor_speed(1.5,-2.5)
        else:
            pass
    else:
        print("elseee")  

phase=mode=mode_1=prev_mode=j_count=ob_count=ob_l=ob_r=int("0")
# Main loop:
while robot.step(timestep) != -1:
    #global doorwayLength
    ir_r_val = int(sensor['ir_right'].getValue())
    ir_l_val = int(sensor['ir_left'].getValue())
    ir_r_ext_val = int(sensor['ir_ext_right'].getValue())
    ir_l_ext_val = int(sensor['ir_ext_left'].getValue())
    ir_r_c = int(sensor['ir_cent_right'].getValue())
    ir_l_c = int(sensor['ir_cent_left'].getValue())
    ir_r_2 = int(sensor['ir_right_2'].getValue())
    ir_l_2 = int(sensor['ir_left_2'].getValue())
    
    ir_r_val_back = int(sensor['ir_right_back'].getValue())
    ir_l_val_back = int(sensor['ir_left_back'].getValue())
    ir_r_ext_val_back = int(sensor['ir_ext_right_back'].getValue())
    ir_l_ext_val_back = int(sensor['ir_ext_left_back'].getValue())
    ir_r_c_back = int(sensor['ir_cent_right_back'].getValue())
    ir_l_c_back = int(sensor['ir_cent_left_back'].getValue())
    ir_r_2_back = int(sensor['ir_right_2_back'].getValue())
    ir_l_2_back = int(sensor['ir_left_2_back'].getValue())
    
    wall_f = int(sensor['wall_front'].getValue())
    wall_b = int(sensor['wall_back'].getValue())

    prev_mode=mode
    
    #if(wall_f==wall_l==wall_r==wall_l_fr==wall_r_fr==1000):
    if (prev_mode != 4 and prev_mode != 5):
        if(wall_f < 300):
            obst=int("1")
    elif (prev_mode == 4):
        obst = int("1")
    elif (prev_mode == 5):
        obst = int("1")
    
    if prev_mode==0 and ir_l_ext_val<950 and ir_r_ext_val<950:
        mode=int("0")
        set_motor_speed(10,10)
        print("START")
    
    elif prev_mode<=1 and obst==0 and (ir_l_c<950 or ir_r_c<950) and (abs(ir_l_ext_val-ir_r_ext_val)<200 or abs(ir_l_ext_val-ir_r_c)<300 or abs(ir_l_c-ir_r_ext_val)<300):
        print("LINE FOLLOW")
        mode=int("1")
        line_follow(ir_r_val,ir_l_val,ir_r_ext_val, ir_l_ext_val, ir_r_c,ir_l_c,ir_r_2,ir_l_2,wall_f,wall_b)    
    
    elif prev_mode<=2 and obst==0 and (ir_l_ext_val!=ir_r_ext_val):
        slowZone = 1
        mode=int("2")
        print("EDGE FOLLOW")
        if ir_r_val==ir_l_val:
            print("pass")
            pass
        if (ir_l_ext_val<950 and ir_r_ext_val>950):
            print("LW")
            edge_follow_lw(ir_r_val,ir_l_val,ir_r_ext_val,ir_l_ext_val,ir_r_c,ir_l_c,ir_r_2,ir_l_2, wall_f,wall_b)    
        
        elif (ir_l_ext_val>950 and ir_r_ext_val<950):
            print("RW")
            edge_follow_rw(ir_r_val,ir_l_val,ir_r_ext_val,ir_l_ext_val,ir_r_c,ir_l_c,ir_r_2,ir_l_2, wall_f,wall_b)
            
    elif (obst == 1):
        print("OBSTACLE")
        
        if wall_f < 300 and slowZone == 0 and prev_mode <= 4: # TODO: timer to go off and flash LED
            mode=int("4")
            print("Obstacle in front. Stopping.")
            set_motor_speed(0,0)
        elif (wall_f < 300 and slowZone == 1) or (prev_mode == 5):
            mode=int("5")
            print("Obstacle in front and in slow zone. Moving back.")
            if (wall_b == 1000 and wall_f < 300 + doorwayLength): #nothing blocking the back, obstacle still in front
                print("EDGGGEE FOLLOW OBST")
                if ir_r_val_back==ir_l_val_back:
                    print("pass")
                    pass
                if (ir_l_ext_val<950 and ir_r_ext_val>950):
                    print("LW_OBST")
                    edge_follow_lw_obst(ir_r_val_back,ir_l_val_back,ir_r_ext_val_back,ir_l_ext_val_back,ir_r_c_back,ir_l_c_back,ir_r_2_back,ir_l_2_back, wall_f,wall_b)    
                
                elif (ir_l_ext_val>950 and ir_r_ext_val<950):
                    print("RW_OBST")
                    edge_follow_rw_obst(ir_r_val_back,ir_l_val_back,ir_r_ext_val_back,ir_l_ext_val_back,ir_r_c_back,ir_l_c_back,ir_r_2_back,ir_l_2_back, wall_f,wall_b)
                
            elif (wall_b != 1000 and wall_f < 300 + doorwayLength): #something blocking the back, obstacle still in front
                set_motor_speed(0,0)
            elif (wall_f >= 300 + doorwayLength and wall_f != 1000): #out of doorway, obstacle still in front,
                set_motor_speed(0,0)
            elif (wall_f == 1000 ): # out of doorway, obstacle not in front anymore
                print("Obstacles cleared mode 5")
                mode = int("1")
                obst = int("0")
        else:
            print("Obstacles cleared")
            mode=int("1")
            obst = int("0")

    elif(obst==0 and ir_l_ext_val>950 and ir_r_ext_val>950):
        mode=int("7")
        print("END")
        while ir_l_ext_val>950 and ir_r_ext_val>950 and robot.step(timestep) != -1:
            ir_r_ext_val = int(sensor['ir_ext_right'].getValue())
            ir_l_ext_val = int(sensor['ir_ext_left'].getValue())
            set_motor_speed(20,20)
        print("stop")
        set_motor_speed(0,0)
        
    else:
        pass
        print("Thank you!")
    