import cv2
import numpy as np
from dotted_image import make_dotted_image, draw_on_pic, empty_circle, neven_cvekla, blacked
from gcode_generator import make_gcode_from_dotted_image

spacing = 10
drawing = True
global mode
mode = False

img = cv2.imread('levi2.png')
cv2.imshow('levi', img)
img = cv2.resize(img, (600, 880), interpolation=cv2.INTER_NEAREST)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_ , img_bw = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
cv2.imshow('levi', img)
cv2.imshow('levi_bw', img_bw)
cv2.waitKey(0)

cv2.destroyAllWindows()

for height_part in range(0, 8):

    for width_part in range(0,6):

        part_img = img[height_part*100:(height_part + 1)*100, width_part*100:(width_part + 1)*100]
        part_img_bw = img_bw[height_part*100:(height_part + 1)*100, width_part*100:(width_part + 1)*100]

        part_img = cv2.resize(part_img, (550, 550), interpolation=cv2.INTER_NEAREST)
        part_img_bw = cv2.resize(part_img_bw, (550, 550), interpolation=cv2.INTER_NEAREST)

        cv2.imshow('Levi' + str(width_part) + str(height_part), part_img)
        
        part_img_dotted = make_dotted_image(part_img_bw, spacing=spacing)

        cv2.imshow('Levi_dotted' + str(width_part) + str(height_part), part_img_dotted)

        while True:

            k = cv2.waitKey(0) & 0xFF

            if k == ord('d'):
                
                cv2.namedWindow("Drawing")
                cv2.setMouseCallback("Drawing", draw_on_pic, param=[part_img_dotted,spacing])

                while True:

                    if cv2.waitKey(0)  & 0xFF == ord('m'):
                        mode = not mode

                    if cv2.waitKey(0)  & 0xFF == ord('q'):
                        break
                    
            if k == ord('p'):
                break

            if k == ord('n'):
                cv2.destroyAllWindows()
                cv2.imshow('Levi_dotted' + str(width_part) + str(height_part), part_img)
                part_img_dotted = neven_cvekla(part_img_dotted)

            if k == ord('b'):
                cv2.destroyAllWindows()
                cv2.imshow('Levi_dotted' + str(width_part) + str(height_part), part_img)
                part_img_dotted = blacked(part_img_dotted)
                
            if cv2.waitKey(0)  & 0xFF == ord('q'):
                    pic_name = 'levi' + str(width_part) + str(height_part) + '.png'
                    cv2.imwrite('Levi_portrait/' + pic_name, part_img_dotted)
                    cv2.destroyAllWindows()
                    cv2.imshow('Konacno', part_img_dotted)
                    cv2.waitKey(0)
                    break

        cv2.destroyAllWindows()

