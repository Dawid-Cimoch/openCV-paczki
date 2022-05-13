import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui 

pyautogui.PAUSE = 0

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')
left = True
x = 850
y = 550
sct = mss.mss()

# dimensions_left = {'left': 800, 'top': 500, 'width': 350, 'height': 400}
# dimensions_right = {'left': 1100, 'top': 500, 'width': 350, 'height': 400}

dimensions_left = {'left': 800, 'top': 400, 'width': 350, 'height': 500}
dimensions_right = {'left': 1100, 'top': 400, 'width': 350, 'height': 500}

dimensions_left = {'left': 800, 'top': 660, 'width': 600, 'height': 200}
dimensions_right = {'left': 800, 'top': 660, 'width': 600, 'height': 200}

pack_left = cv2.imread('data/left_temp.jpg')

pack_right = cv2.imread('data/right_tempjpg.jpg')
w = pack_left.shape[1]
h = pack_left.shape[0]

fps_time = time()
cnt=1
while True:
    if left:
        scr = numpy.array(sct.grab(dimensions_left))
        wood = pack_left
    else:
        scr = numpy.array(sct.grab(dimensions_right))
        wood = pack_right
    # Cut off alpha
    scr_remove = scr[:,:,:3]
    # with mss.mss() as mss_instance:  # Create a new mss.mss instance
    #     monitor_1 = mss_instance.monitors[1]  # Identify the display to capture
    #     screenshot = mss_instance.grab(monitor_1)  # Take the screenshot
    #     img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
    #     img.show()  # Show the image using the default image viewer
    # cv2.imshow('a crop of the screen', scr_remove)
    result = cv2.matchTemplate(scr_remove, wood, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"Max Val: {max_val} Max Loc: {max_loc}")
    src = scr.copy()
    if max_val > .50:
        left = not left
        if left:
            x=850
        else:
            x=1200
        cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

    cv2.imshow('Screen Shot', scr)
    cv2.imwrite(f'data\output{cnt}.jpg', scr_remove)    
    cnt+=1
    cv2.imwrite('data\output_wood.jpg', wood)    
    cv2.waitKey(1)
    pyautogui.click(x=x, y=y)
    sleep(.10)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()