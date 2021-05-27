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
'''
Requiremnets: This variable shall be initialised with a 3*3 matrix with below values 
[[ 1.77928445e+00,  5.69877582e-01,-9.82152353e+02],
 [-5.80034886e-16,  3.59466115e+00, -9.20233254e+02],
 [ 1.99095433e-04,  2.69942866e-03,  1.00000000e+00]]
'''
'''ch_matrix_2mp = np.array([[ 3.46959178e+00,  1.13138862e+00, -1.67618996e+03],
 [ 3.25571048e+00,  2.00140518e+01, -1.00066832e+04],
 [ 2.22885334e-03,  4.97684693e-03,  1.00000000e+00]]) #for raipur'''

#ch_matrix_2mp = np.array([[ 1.45107517e+00, 4.16576604e-01, -6.29475021e+02],
 #[-1.84463740e-01,  4.05110752e+00, -1.03218105e+03],
 #[ 5.24845526e-04,  2.06045617e-03,  1.00000000e+00]])#for sholapur'''
'''ch_matrix_2mp = np.array([[ 2.73653922e+00,  3.80074891e-01, -1.51186190e+03],
 [ 4.62705522e-01,  4.94364321e+00, -1.78287744e+03],
 [ 6.53350994e-04,  4.15877829e-03,  1.00000000e+00]])#for sholapur'''
#ch_matrix_2mp = np.array([[ 8.70803538e-01,  1.23744125e-17, -3.04781238e+02],
# [ 1.98966981e-01, -2.77132580e+00,  1.27168324e+03],
# [ 1.37896905e-04,  2.74936441e-04,  1.00000000e+00]])#for Balangir'''
'''ch_matrix_2mp = np.array([[ 8.51136905e-01,  2.55722747e-01, -2.78077495e+02],
[-1.61991150e-01,  2.23907767e+00, -5.23587794e+02],
[ 2.37583968e-04,  4.87797615e-04,  1.00000000e+00]])#for durgapur1'''
##Baraeill matrix
#ch_matrix_2mp = np.array([[ 9.48802013e-01,  5.16084777e-02, -3.58075498e+02],
# [-4.27611043e-02,  2.07818967e+00, -7.64055412e+02],
# [ 2.62584437e-06,  3.94470315e-04,  1.00000000e+00]])

## Baraeiili second matrix
#ch_matrix_2mp = np.array([[ 7.83392401e-01,  1.57307711e-02, -2.52510338e+02],
# [-6.92755807e-02,  1.82887533e+00, -6.45717688e+02],
# [-8.09522981e-05,  2.67811156e-04,  1.00000000e+00]])

#Ajmer testbath1
#ch_matrix_2mp = np.array([[ 8.37881051e-01,  2.78215330e-01, -3.26149243e+02],
# [ 2.00917111e-02,  2.38689528e+00, -7.69492444e+02],
# [-6.97001422e-05,  9.58421252e-04,  1.00000000e+00]])

#new matrix
#ch_matrix_2mp = np.array([[ 8.90003455e-01,  2.74337983e-01, -3.34172373e+02],
# [ 6.76632910e-02,  2.23288860e+00, -6.89015292e+02],
# [ 5.74815998e-05,  9.18079997e-04,  1.00000000e+00]])

#Roorkee matrix
#ch_matrix_2mp = np.array([[ 7.13312034e-01,  2.19873960e-01, -2.39297012e+02],
# [-6.44794475e-03,  2.04399849e+00, -6.11632695e+02],
# [-1.14523432e-04,  7.68662229e-04,  1.00000000e+00]])




#ch_matrix_2mp = np.array([[ 7.62579737e-01, -3.41964008e-03, -5.36336349e+02], #Allahabad second
    
# [-1.56040758e-16,  2.19188566e+00, -8.21957124e+02],
# [-2.13382955e-04,  6.23118100e-04,  1.00000000e+00]])

#ch_matrix_2mp = np.array([[ 7.62579737e-01, -3.41964008e-03, -5.36336349e+02],
# [-1.56040758e-16,  2.19188566e+00, -8.21957124e+02],
# [-2.13382955e-04,  6.23118100e-04,  1.00000000e+00]])
#roorkee2
#ch_matrix_2mp = np.array([[ 8.31662535e-01,  2.65884677e-01, -2.84518246e+02],
# [ 6.49084760e-02,  2.28622077e+00, -7.24501198e+02],
# [ 5.28886709e-05,  8.89852543e-04,  1.00000000e+00]])

#Allahabad
#ch_matrix_2mp = np.array([[ 8.09716599e-01,  2.71671463e-17, -2.41295547e+02],
# [ 7.17719935e-17,  1.47601476e+00, -3.40959410e+02],
# [ 1.43834562e-19, -0.00000000e+00,  1.00000000e+00]])


#ch_matrix_2mp = np.array([[ 6.84591174e-01,  1.87747412e-01, -2.34562917e+02],
# [-1.01325167e-16,  2.41966734e+00, -8.61401572e+02],
# [-1.49446899e-04,  1.27184913e-03,  1.00000000e+00]])

ch_matrix_2mp = np.array([[ 5.52253551e-01,  5.39661450e-02, -1.77584595e+02],
 [ 7.93902498e-17,  1.71284271e+00, -5.53248196e+02],
 [-2.08894284e-04,  5.85586182e-04,  1.00000000e+00]]) #piyala_1

def roi_fun(coordinates,scores):
    view_coords = []
    view_scores = []
    number_roi = 0
    for person in range(0,5):
        if abs(coordinates[person][5][1] - coordinates[person][6][1]) < 35 and abs(coordinates[person][5][0] - coordinates[person][7][0]) < 35 :
            continue
        list_roi=[]
        for body_point in [5,6,7,8,9,10]:
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
