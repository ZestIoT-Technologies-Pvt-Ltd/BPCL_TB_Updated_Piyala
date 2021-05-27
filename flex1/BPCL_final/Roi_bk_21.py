'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of 5 Persons 
Output: Coordinates and Scores of Persons who are in ROI
Requirements:
This function shall perform the following:
1)For each person it will identify the presence of any one of the below key points in ROI
  keypoints are left knee,left ankle, Right ankle, Right knee
2)A new list of identified person coordinates and scores in ROI is returned
'''    
    
import cv2
import numpy as np
import math

#Requiremnets: This variable shall be initialised with a 3*3 matrix with below values 


#ch_matrix_2mp = np.array([[ 5.52253551e-01,  5.39661450e-02, -1.77584595e+02],
# [ 7.93902498e-17,  1.71284271e+00, -5.53248196e+02],
# [-2.08894284e-04,  5.85586182e-04,  1.00000000e+00]]) #piyala_1

'''ch_matrix_2mp = np.array([[ 7.72012892e-01,  7.54409992e-02, -1.71049892e+02],
 [-6.04717222e-17,  1.84611277e+00, -5.96294425e+02],
 [ 1.02037528e-04,  6.35818327e-04,  1.00000000e+00]])  #piyala_3'''

'''ch_matrix_2mp =np.array([[ 8.18862994e-01, 1.88117174e-01, -2.51169625e+02],
[ 9.29689862e-02, -1.62907019e+00, 8.89121577e+02],
[ 2.32422466e-04, 6.30416614e-04, 1.00000000e+00]])'''# latest -19/05/21

ch_matrix_2mp = np.array([[ 5.99978166e-01,  1.67757053e-01, -1.97313872e+02],
 [-2.30293552e-03,  1.70647522e+00, -3.95294275e+02],
 [-1.87727312e-05,  5.61139660e-04,  1.00000000e+00]])



def roi_fun(coordinates,scores):
    view_coords = []
    view_scores = []
    number_roi = 0
    for person in range(0,5):
        if abs(coordinates[person][5][1] - coordinates[person][6][1]) < 35 and abs(coordinates[person][5][0] - coordinates[person][7][0]) < 35 :
            continue
        list_roi=[]
        for body_point in [5,6,7,8,9,10,13,14]:
            landmark_coords=[0,0]
            if round(scores[person][body_point],1) >= 0.1:
                landmark_coords[0]=round(coordinates[person][body_point][0],1)
                landmark_coords[1]=round(coordinates[person][body_point][1],1)
            else:
                landmark_coords[0] = -1
                landmark_coords[1] = -1
            list_roi.append(landmark_coords)

        for i in range(5,-1,-1):
            x_coordinate = list_roi[i][1]
            y_coordinate = list_roi[i][0]
            a1 = np.array([[x_coordinate,y_coordinate]],dtype='float32')
              #print("a1--->",a1)
            a1 = np.array([a1])
            output1 = cv2.perspectiveTransform(a1,ch_matrix_2mp)
            if((output1[0][0][0] >= 0.0 and output1[0][0][0] <=400) and (output1[0][0][1] >= 0.0 and output1[0][0][1] <=400)):
                view_coords.append(coordinates[person])
                view_scores.append(scores[person])
                number_roi = number_roi+1
                break
                   
    return view_coords,view_scores,number_roi
