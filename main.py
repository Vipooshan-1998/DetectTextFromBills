import cv2
import numpy as np
import pytesseract
import os
import json
# C:\Program Files\Tesseract-OCR

per = 25

roi = [[(136, 456), (272, 494), 'text', 'Table'],
       [(160, 488), (312, 532), 'text', 'Date'],
       [(156, 524), (318, 556), 'text', 'Staff'],
       [(406, 464), (510, 488), 'text', 'DR#'],
       [(422, 490), (546, 524), 'text', 'Time'],
       [(414, 522), (546, 556), 'text', 'Cover'],
       # [(98, 564), (404, 898), 'text', 'Items'],
       # [(404, 564), (528, 910), 'text', 'Prices'],
       [(70, 568), (542, 966), 'text', 'ItemAndPrice'],
       # [(20, 562), (532, 962), 'text', 'ItemAndPrice'],    #[(100, 574), (536, 968), 'text', 'ItemAndPrice']
       [(408, 900), (532, 936), 'text', 'MPM DP 15% Dev'],                        # [(152, 894), (528, 934), 'text', 'MPM DP 15% Dev'],
       [(374, 930), (536, 972), 'text', 'MPM Dining Privilege'],   # [(64, 926), (534, 964), 'text'
       [(372, 990), (526, 1030), 'text', 'Sub-Total'],
       [(376, 1052), (528, 1082), 'text', 'VATable'],
       [(368, 1088), (530, 1120), 'text', '10% S.C.'],
       [(376, 1124), (526, 1152), 'text', '12% VAT'],
       [(368, 1150), (530, 1186), 'text', 'LTax Fd/Bv'],
       [(354, 1186), (524, 1230), 'text', 'Total']]

# roi = [[(109, 376), (165, 398), 'text', 'Table'],
#        [(136, 403), (250, 431), 'text', 'Date'],
#        [(134, 428), (238, 455), 'test', 'Staff'],
#        [(312, 377), (431, 403), 'text', 'DR#'],
#        [(352, 403), (428, 431), 'text', 'Time'],
#        [(360, 431), (403, 457), 'text', 'Cover'],
#        [(57, 474), (438, 796), 'text', 'ItemsAndPrices'],
#        [(177, 809), (430, 850), 'text', 'Sub-Total'],
#        [(195, 860), (425, 899), 'text', 'VATable'],
#        [(188, 888), (423, 923), 'text', '10% S.C.'],
#        [(204, 917), (422, 950), 'text', '12% VAT'],
#        [(165, 939), (422, 979), 'text', 'LTax Fd/Bv'],
#        [(147, 969), (436, 1019), 'text', 'Total']]

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

imgQ = cv2.imread('Query.jpeg')
h,w,c = imgQ.shape
#imgQ = cv2.resize(imgQ, (w//2,h//2))

orb = cv2.ORB_create(5000)
kp1, des1 = orb.detectAndCompute(imgQ, None)
#impKp1 = cv2.drawKeypoints(imgQ, kp1, None)

path = 'Bills'
myPicList = os.listdir(path)
print(myPicList)

for j,y in enumerate (myPicList):
    img = cv2.imread(path +'/'+y)
    #img = cv2.resize(img, (w // 2, h // 2))
    # cv2.imshow(y, img)
    kp2, des2 = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2,des1)
    matches.sort(key=lambda x: x.distance)
    good = matches[:int(len(matches)*(per/100))]
    imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:100],None,flags=2)

    imgMatch = cv2.resize(imgMatch, (w // 2, h // 2))
    cv2.imshow(y, imgMatch)

    srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, _ = cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
    imgScan = cv2.warpPerspective(img,M,(w,h))
    # imgScan = cv2.resize(imgScan, (w // 2, h // 2))
    # cv2.imshow(y, imgScan)

    imgShow = imgScan.copy()
    imgMask = np.zeros_like(imgShow)

    myData = []   # all of the image data stored here
    print(f'########## Extracting data from {y} ################')

    part1 = '{';
    part2 = '"Consumed items" :['
    part3 = ''
    items = []
    prices = []
    for x,r in enumerate(roi):

        cv2.rectangle(imgMask, (r[0][0],r[0][1]), (r[1][0],r[1][1]),(0,255,0),cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow,0.99,imgMask,0.1,0)


        imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        cv2.imshow(str(x), imgCrop)

        # your_json = '["foo", {"bar":["baz", null, 1.0, 2]}]'

        if r[2] == 'text':
            # print(f'{r[3]} : {pytesseract.image_to_string(imgCrop)}')
            # myData.append(pytesseract.image_to_string(imgCrop))

            if r[3] != 'ItemAndPrice':              #  r[3] != 'Items' and r[3] != 'Prices'
                if r[3] != 'Total':
                    part1 = part1 + f'"{r[3]}":"{pytesseract.image_to_string(imgCrop).strip()}",'
                else: part1 = part1 + f'"{r[3]}":"{pytesseract.image_to_string(imgCrop).strip()}"' + '}'

            else:
                # if r[3] == 'Items':
                #     items.append(pytesseract.image_to_string(imgCrop).split("\\."))
                # else: prices.append(pytesseract.image_to_string(imgCrop).split("\\."))
                itemPrice = pytesseract.image_to_string(imgCrop).split()
                # for i in range(0,len(itemPrice)-1,2):
                part2 = part2 + '{' + f'"item":"{itemPrice[0].strip()}","price":"{itemPrice[0+1]}"' + '},{}],'

    # print(items)
    # for itm, prc in zip(items, prices):
    #     part2 = part2 + '{' + f'"item":"{itm}","price":"{prc},' + '}'

    # print(part2)
    part3 = part3 + '}'
    # print(part1[:-1]+part3)
    full = part1[:part1.index('"Cover')] + part2 + part1[part1.index('"Cover'):]
    print(full)
    print(len(full))
    # print(part1[148:151])

    parsed = json.loads(full)
    print(json.dumps(parsed, indent=4))



    # imgShow = cv2.resize(imgShow, (w // 2, h // 2))
    # cv2.imshow(y+"2", imgShow)


#cv2.imshow("KeyPointsBill", impKp1)

# cv2.imshow("Query", imgQ)
cv2.waitKey(0)



