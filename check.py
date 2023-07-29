import cv2
import random

scale = 0.5
circles = []
counter = 0
counter2 = 0
point1=[]
point2=[]
myPoints = []
myColor = []

def mousePoints(event,x,y,flags,params):
    global counter,point1,point2,counter2,circles,myColor
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter ==0:
            point1=int(x//scale),int(y//scale);
            counter+=1
            myColor = (random.randint(0,2)*200, random.randint(0,2)*200,random.randint(0,2)*200 )
        elif counter==1:
            point2=int(x//scale),int(y//scale);
            type = input('Enter Type: ')
            name = input('Enter Name: ')
            myPoints.append([point1,point2,type,name])
            counter=0
        circles.append([x,y,myColor])
        counter2 += 1

img = cv2.imread("C:\\Users\\THUVAA\\Desktop\\T.Thuvaaragan.JPG");
# img = cv2.resize(img, (0,0), None, scale, scale);


while True:
    # To Display points
    for x,y,color in circles:
        cv2.circle(img,(x,y),3,color,cv2.FILLED)
    cv2.imshow("Original Image ", img)
    cv2.setMouseCallback("Original Image ", mousePoints)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        print(myPoints)
        break

print(myPoints[0])
print(myPoints[0][0])
print(myPoints[0][0][0])


# Segmentation
x,y=img.shape[0:2]
print(x)
print

# pic = img[0:1200,0:900]
# cv2.imshow("pic",pic)
# cv2.waitKey(0)
slot=[]
for j in range(0,2):
    needed_items=[]
    print(myPoints[j][0][0])
    print(myPoints[j][1][0])
    print(myPoints[j][0][1])
    print(myPoints[j][1][1])
    small_value_x= 0
    Big_value_x =0
    Big_value_y = 0
    small_value_y = 0
    if myPoints[j][0][0] > myPoints[j][1][0]:
        Big_value_x+=myPoints[j][0][0]
        small_value_x+=myPoints[j][1][0]
    else:
        Big_value_x+=myPoints[j][1][0]
        small_value_x+=myPoints[j][0][0]

    if myPoints[j][0][1] > myPoints[j][1][1]:
        Big_value_y+=myPoints[j][0][1]
        small_value_y+=myPoints[j][1][1]
    else:
        Big_value_y+=myPoints[j][1][1]
        small_value_y+=myPoints[j][0][1]
    print("////////////////////////////////////////////")
    print(small_value_y)
    print(small_value_x)
    print(Big_value_x)
    print(Big_value_y)
    needed_items.append(small_value_x)
    needed_items.append(Big_value_x)
    needed_items.append(small_value_y)
    needed_items.append(Big_value_y)
    needed_items.append(myPoints[j][2])
    slot.append(needed_items)
print("Slot_list",slot)

for k in range(0,2):
    image = cv2.imread("'car_det.jpeg'");
    # image = cv2.resize(img, (0, 0), None, scale, scale);
    lot_picture = image[slot[k][0]:slot[k][1]+1, slot[k][2]:slot[k][3]+1]
    cv2.imshow("lots photo", lot_picture)
    cv2.waitKey(0)
    print(str(k) + "_frame")