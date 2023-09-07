# from dotted_image import prazan_krug
import cv2

spacing = 10

def make_gcode_from_dotted_image(gcode, img, method, spacing=spacing):

    height, width = img.shape[:2]
    r = int(spacing/2)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.flip(img, 0)

    matrix_of_starts = []
    matrix_of_ends = []
    matrix = []

    last_element_index = 0
    for index_j, j in enumerate(range(0, height - 1, spacing)):

        first_element_inc = True
        
        current_width_num = 0
        matrix.append([])
        for index_i, i in enumerate(range(0, width  -1, spacing)):

            if img[i,j][0] < 200:
                 
                last_element_index = index_i  
                if first_element_inc:
                    first_element_inc = False
                      
                    matrix_of_starts.append(index_i)
                    matrix[index_j].append(index_i)

                else:
                    
                    matrix[index_j].append(index_i)

            else:
                    
                    matrix[index_j].append(0)  
                    current_width_num = current_width_num + 1 
                
        if current_width_num >= width/spacing - 2:
            matrix_of_starts.append(-1)
            matrix_of_ends.append(-1)

        else:
            
            matrix_of_ends.append(last_element_index)

    maximum_width = index_i
    maximum_height = index_j         
 
    print(matrix)
    print(matrix_of_starts)
    print(matrix_of_ends)

        #this is better way to generate path but painting is not as precise
        ###############
    if method == 1:
        with open(gcode, 'w') as f:

            last_height_index = 1
            current_width_index = 0
            start_width = matrix_of_starts[0]
            end_width = matrix_of_ends[0]

            width_range = range(start_width, end_width, 1)

            skip = False if start_width else True
            vert_flag = True

            for index_height, row in enumerate(matrix):

                    print('height ', index_height)
                    print("current " ,current_width_index)
                    print("width flow ", width_range)
                    vert_flag = True

                    if not skip:    

                        for index_width in width_range:
                            
                            if row[index_width] != 0:

                                if vert_flag: #setting up vertical movement

                                    vert_flag = False
                                    if last_height_index == 1:
                                        f.write('verd1')
                                        f.write('\n')
                                    else:
                                        f.write('verd' + str(last_height_index))
                                        f.write('\n')
                                        last_height_index = 1


                                if index_width - current_width_index == 0:
                                    f.write('pen')
                                    f.write('\n')
                                    print('olovka')
                                    
                                elif index_width - current_width_index > 0:
                                    
                                    f.write('horr' + str(index_width - current_width_index))
                                    f.write('\n')
                                    f.write('pen')
                                    f.write('\n')
                                    print('razlika veca', index_width - current_width_index)

                                    current_width_index = index_width
                                            
                                else:
                                        
                                    f.write('horl' + str(current_width_index - index_width))
                                    f.write('\n')
                                    f.write('pen')
                                    f.write('\n')
                                    print('razlika manja ', current_width_index - index_width)
                                    current_width_index = index_width

                                
                                print('current in ', current_width_index )

                    print('kraj reda')

                    if index_height == maximum_height: 
                        break
                    
                    else:
                        print('current ', current_width_index )
                        print('start ', matrix_of_starts[index_height + 1])
                        print('ends ', matrix_of_ends[index_height + 1])

                        if matrix_of_starts[index_height + 1] != -1 and matrix_of_ends[index_height + 1] != -1:

                            if abs(current_width_index - matrix_of_starts[index_height + 1]) <= abs(current_width_index - matrix_of_ends[index_height + 1]):
                                
                                    if current_width_index - matrix_of_starts[index_height + 1] > 0:
                                        
                                        f.write('horl' + str(current_width_index - matrix_of_starts[index_height + 1]))
                                        f.write('\n')
                                        print('levo start ', current_width_index - matrix_of_starts[index_height + 1])

                                    elif current_width_index - matrix_of_starts[index_height + 1] < 0:

                                        f.write('horr' + str(matrix_of_starts[index_height + 1] - current_width_index))
                                        f.write('\n')
                                        print('desno start', matrix_of_starts[index_height + 1] - current_width_index )
                                    else:
                                        pass

                                    current_width_index = matrix_of_starts[index_height + 1]
                                    width_range = range(matrix_of_starts[index_height + 1], matrix_of_ends[index_height + 1] + 1, 1)
                                    
                                    if matrix_of_starts[index_height + 1] == matrix_of_ends[index_height + 1]:
                                            if last_height_index == 1:
                                                f.write('verd1')
                                                f.write('\n')
                                            else:
                                                f.write('verd' + str(last_height_index))
                                                f.write('\n')
                                                last_height_index = 1

                                            f.write('pen')
                                            f.write('\n')
                                            skip = True
                                            continue 
                                
                            else: 
                                
                                    if current_width_index - matrix_of_ends[index_height + 1] > 0:
                                        
                                        f.write('horl' + str(current_width_index - matrix_of_ends[index_height + 1]))
                                        f.write('\n')
                                        print('levo end', current_width_index - matrix_of_ends[index_height + 1])

                                    elif current_width_index - matrix_of_ends[index_height + 1] < 0:

                                        f.write('horr' + str(matrix_of_ends[index_height + 1] - current_width_index))
                                        f.write('\n')
                                        print('desno end', current_width_index - matrix_of_ends[index_height + 1])
                                    else:
                                        pass

                                    current_width_index = matrix_of_ends[index_height + 1]
                                    width_range = range(matrix_of_ends[index_height + 1], matrix_of_starts[index_height + 1] - 1, -1)

                            skip = False
                                
                        else:
                                last_height_index += 1
                                skip = True
                                print('skipped', last_height_index)
                        
            f.write('completed')



    elif method == 2:

    #this is simpler method that is not as efficient but it has better overall precision

        with open(gcode, 'w') as f:

            last_height_index = 1
            steps_needed = 0
            
            for height_index, row in enumerate(matrix):
                
                current_width_index = 0

                skip = True if matrix_of_starts[height_index] == -1 else False
                
                if not skip: 

                    if last_height_index == 1:
                        f.write('verd1')
                        f.write('\n')
                    else:
                        f.write('verd' + str(last_height_index))
                        f.write('\n')
                        last_height_index = 1
            
                    for width_index, element in enumerate(row):
                        
                        if element:
                        
                            if width_index - current_width_index > 0:

                                f.write('horr' + str(width_index - current_width_index))
                                f.write('\n')
                                current_width_index = width_index
                            
                            f.write('pen')
                            f.write('\n')
                            

                    f.write('horl' + str(current_width_index))
                    f.write('\n')

                else:
                    last_height_index = last_height_index + 1


            f.write('completed')

    ### this method combines previous methods by advantages of both and mixing it up a bit
    else: 
         
        with open(gcode, 'w') as f:

            last_height_index = 1
            current_width_index = 0
            start_width = matrix_of_starts[0]
            end_width = matrix_of_ends[0]
            normal_calibration = False
            calibration_steps = 2

            width_range = range(start_width, end_width, 1)

            skip = False if start_width else True
            #vert_flag = True

            for index_height, row in enumerate(matrix):

                    print('height ', index_height)
                    print("current " ,current_width_index)
                    print("width flow ", width_range)
                    
                    if not skip:  

                        if last_height_index == 1:
                            if normal_calibration:
                                f.write('horl' + str(calibration_steps))
                                f.write('\n')
                                f.write('verd1')
                                f.write('\n')
                                f.write('horr' + str(calibration_steps))
                                f.write('\n')

                            else:
                                f.write('horr' + str(calibration_steps))
                                f.write('\n')
                                f.write('verd1')
                                f.write('\n')
                                f.write('horl' + str(calibration_steps))
                                f.write('\n')

                        else:
                            if normal_calibration:
                                f.write('horl' + str(calibration_steps))
                                f.write('\n')
                                f.write('verd' + str(last_height_index))
                                f.write('\n')
                                f.write('horr' + str(calibration_steps))
                                f.write('\n')
                            else:
                                f.write('horr' + str(calibration_steps))
                                f.write('\n')
                                f.write('verd' + str(last_height_index))
                                f.write('\n')
                                f.write('horl' + str(calibration_steps))
                                f.write('\n')

                            last_height_index = 1  

                        for index_width in width_range:
                            
                            if row[index_width] != 0:

                                if index_width - current_width_index == 0:
                                    f.write('pen')
                                    f.write('\n')
                                    print('olovka')
                                    
                                elif index_width - current_width_index > 0:
                                    
                                    f.write('horr' + str(index_width - current_width_index))
                                    f.write('\n')
                                    f.write('pen')
                                    f.write('\n')
                                    print('razlika veca', index_width - current_width_index)

                                    current_width_index = index_width
                                            
                                else:
                                        
                                    f.write('horl' + str(current_width_index - index_width))
                                    f.write('\n')
                                    f.write('pen')
                                    f.write('\n')
                                    print('razlika manja ', current_width_index - index_width)
                                    current_width_index = index_width

                                
                                print('current in ', current_width_index )

                    print('kraj reda')

                    if index_height == maximum_height: 
                        break
                    
                    else:
                        print('current ', current_width_index )
                        print('start ', matrix_of_starts[index_height + 1])
                        print('ends ', matrix_of_ends[index_height + 1])

                        if matrix_of_starts[index_height + 1] != -1 and matrix_of_ends[index_height + 1] != -1:

                            vert_flag = True

                            if abs(current_width_index - matrix_of_starts[index_height + 1]) <= abs(current_width_index - matrix_of_ends[index_height + 1]):
                                
                                    if current_width_index - matrix_of_starts[index_height + 1] > 0:
                                        
                                        f.write('horl' + str(current_width_index - matrix_of_starts[index_height + 1]))
                                        f.write('\n')
                                        print('levo start ', current_width_index - matrix_of_starts[index_height + 1])

                                    elif current_width_index - matrix_of_starts[index_height + 1] < 0:

                                        f.write('horr' + str(matrix_of_starts[index_height + 1] - current_width_index))
                                        f.write('\n')
                                        print('desno start', matrix_of_starts[index_height + 1] - current_width_index )
                                    else:
                                        pass

                                    current_width_index = matrix_of_starts[index_height + 1]
                                    width_range = range(matrix_of_starts[index_height + 1], matrix_of_ends[index_height + 1] + 1, 1)
                                    normal_calibration = True

                                    if matrix_of_starts[index_height + 1] == matrix_of_ends[index_height + 1]:
                                            if last_height_index == 1:
                                                if normal_calibration:
                                                    f.write('horl' + str(calibration_steps))
                                                    f.write('\n')
                                                    f.write('verd1')
                                                    f.write('\n')
                                                    f.write('horr' + str(calibration_steps))
                                                    f.write('\n')

                                                else:
                                                    f.write('horr' + str(calibration_steps))
                                                    f.write('\n')
                                                    f.write('verd' + str(calibration_steps))
                                                    f.write('\n')
                                                    f.write('horl' + str(calibration_steps))
                                                    f.write('\n')
                                            else:
                                                if normal_calibration:
                                                    f.write('horl' + str(calibration_steps))
                                                    f.write('\n')
                                                    f.write('verd' + str(last_height_index))
                                                    f.write('\n')
                                                    f.write('horr' + str(calibration_steps))
                                                    f.write('\n')

                                                else:
                                                    f.write('horr' + str(calibration_steps))
                                                    f.write('\n')
                                                    f.write('verd' +  str(last_height_index))
                                                    f.write('\n')
                                                    f.write('horl' + str(calibration_steps))
                                                    f.write('\n')
                                                
                                                last_height_index = 1

                                            f.write('pen')
                                            f.write('\n')
                                            skip = True
                                            continue 
                                
                            else: 
                                
                                    if current_width_index - matrix_of_ends[index_height + 1] > 0:
                                        
                                        f.write('horl' + str(current_width_index - matrix_of_ends[index_height + 1]))
                                        f.write('\n')
                                        print('levo end', current_width_index - matrix_of_ends[index_height + 1])

                                    elif current_width_index - matrix_of_ends[index_height + 1] < 0:

                                        f.write('horr' + str(matrix_of_ends[index_height + 1] - current_width_index))
                                        f.write('\n')
                                        print('desno end', current_width_index - matrix_of_ends[index_height + 1])
                                    else:
                                        pass

                                    current_width_index = matrix_of_ends[index_height + 1]
                                    width_range = range(matrix_of_ends[index_height + 1], matrix_of_starts[index_height + 1] - 1, -1)
                                    normal_calibration = False
                            skip = False
                                
                        else:
                                last_height_index += 1
                                skip = True
                                print('skipped', last_height_index)
                        
            f.write('completed')



img= cv2.imread('Levi_portrait/levi52.png')
# make_gcode_from_dotted_image(gcode = 'gcode', method=2, img=img)
make_gcode_from_dotted_image(gcode = 'Levi_portrait/gcode', method=3, img=img)

