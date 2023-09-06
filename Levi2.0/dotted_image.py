import cv2
import numpy as np
import time

#variables -> would like to encapsulate somehow
drawing = True
mode = False
spacing = 10

def get_contours(path:str) -> np.ndarray:

    img:np.ndarray = cv2.imread(path)

    gray_image:np.ndarray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blurred_image:np.ndarray = cv2.GaussianBlur(gray_image, (7,7), cv2.BORDER_TRANSPARENT)

    contours_image:np.ndarray = cv2.divide(gray_image, blurred_image, scale=256.0)
    
    
    contours_image = cv2.resize(contours_image, (550,550), interpolation=cv2.INTER_NEAREST)

    return contours_image


def empty_circle(img, i,j,r):

    beli, crni = 0, 0
    for jj in range(j-r, j + r, 1):
        for ii in range(i -r, i + r, 1):
            
            if img[ii,jj] > 100:
                beli = beli + 1 
            else :
                crni = crni + 1

    return True if crni * 4 > beli else False  #Vule je genije 
      

def make_dotted_image(img, spacing):

    height, width = img.shape[:2]
    r = int(spacing/2)

    for j in range(0, height  - 1, spacing):
        for i in range(0, width   -1, spacing):

            if not empty_circle(img, i, j, r):
                cv2.rectangle(img, (i-r, j-r), (i+r, j+r), (255,255,255), -1)
            else:
                cv2.rectangle(img, (i-r, j-r), (i+r, j+r), (255,255,255), -1)
                cv2.circle(img, center=(i,j), radius=r, color=(0,0,0), thickness=-1)

        
    return img


def draw_on_pic(event, x, y, flags, param):

    global drawing, mode
    pic = param[0]
    spacing = param[1]

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        

    if event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                cv2.circle(pic, ((round(x/spacing) * spacing), (round(y/spacing) * spacing)), int(spacing/2), (255,255,255), -1)
                cv2.imshow("Drawing", pic)
            else:
                cv2.circle(pic, ((round(x/spacing) * spacing), (round(y/spacing) * spacing)), int(spacing/2), (0,0,0), -1)
                cv2.imshow("Drawing", pic)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        mode = not mode
        print(mode)

def neven_cvekla(pic):

    pic = np.ones((550,550))
    cv2.imshow("Blank", pic)
    return 255 - pic
def blacked(pic):

    pic = np.ones((550,550))
    cv2.imshow("Blank", pic)
    return pic

def main():
    
    pic = get_contours('cat2.png')
    cv2.imshow("Prvi", pic)
       

    pic = make_dotted_image(pic, spacing)
    cv2.imshow("Levi", pic)


    # naziv = input("Nazovi nekako sliku: ")
    # naziv = naziv + '.png'


    while True:    

        k = cv2.waitKey(0) & 0xFF


        if k == ord('d'):
            
            cv2.destroyAllWindows()
            cv2.namedWindow("Drawing")
            cv2.setMouseCallback("Drawing", draw_on_pic, param=[pic,spacing])

            while True:
                cv2.imshow("Drawing", pic)
                if cv2.waitKey(0)  & 0xFF == ord('m'):
                    global mode
                    mode = not mode
                if cv2.waitKey(0)  & 0xFF == ord('q'):
                    break


        if k == ord('s'):
            pic_name = 'LEVI.png'
            cv2.imwrite(pic_name, pic)
            cv2.destroyAllWindows()
            cv2.imshow('Konacno', pic)
            

        if k == ord('n'):
            cv2.destroyAllWindows()
            pic = neven_cvekla(pic)
            

        if k == ord('q'):
            cv2.destroyAllWindows()
            break

    
    gcode_start = input('Would you like to generate gcode for this picture? y/n   ')

    if (gcode_start == 'y'):
        from gcode_generator import make_gcode_from_dotted_image
        img = cv2.imread(pic_name)
        make_gcode_from_dotted_image(img, spacing=spacing)

        with open('gcode', 'r') as f:
            f.read()
            time.sleep(1)


if __name__ == "__main__":

    main()


