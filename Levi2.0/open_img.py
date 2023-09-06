import cv2

for height_part in range(0, 8):

    for width_part in range(0,6):

        img = cv2.imread('Levi_portrait/levi' + str(width_part) + str(height_part) + '.png')
        cv2.imshow('Levi' + str(width_part) + str(height_part), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        

 