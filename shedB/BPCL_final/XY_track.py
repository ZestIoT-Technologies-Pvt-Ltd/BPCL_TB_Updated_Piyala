#   Copyright (C) 2020 by ZestIOT. All rights reserved. The information in this 
#   document is the property of ZestIOT. Except as specifically authorized in 
#   writing by ZestIOT, the receiver of this document shall keep the information
#   contained herein confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and disseminations to 
#   the receiver's employees shall only be made on a strict need to know basis.
"""
Input: image from camera, darknet image object, loaded network (darknet object), class_name 
       (darknet object), trck_dict(dictionary with number of cylinders and their respective centroid 
       coordinates),st_dict(number of cylinders in the first frame), count (number of frames),
       cyl(cylinder number), moving(if cylinder is moving then True else False) 

Output: trck_dict(dictionary with number of cylinders and their respective centroid coordinates),
        st_dict(number of cylinders in the first frame), count (number of frames),
        cyl(cylinder number), moving(if cylinder is moving then True else False) 

User Requirement:
1) Detecting if the cylinder are moving or not


Requirements:
1) This function takes the darknet image object, loaded network(darknet object), class name(darknet onject),
   and image from the camera  which is first cropped in Region of inetrest(ROI) and then it is converted to 
   the darknet image object which is passed to the loaded model with class names. The result is the detection 
   of cylinder in each ROI, which basically provides the central coordinates of the bounding box detection of 
   the respective object.
2) Then we need to check if the cylinders are moving or not by the monement of coordinates of the detection over some frames.
3) If there is no movement for certain frames then we know the cylinfers are not moving.
"""


import darknet
import cv2
import error
from datetime import datetime, timedelta
import traceback
import numpy as np
font = cv2.FONT_HERSHEY_SIMPLEX
def track(img,darknet_image,network,class_names,track_dict,st_dict,count,cyl,moving):
	global start_time
	try:
		obj=cyl
		cyl_dict={}
		diff_pixel=20
		x_res=int(img.shape[1])
		y_res=int(img.shape[0])
		pts = np.array([[325,300],[300,620],[980,620],[978,300]])
		mask = np.zeros(img.shape[:2], np.uint8)
		cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
		dst = cv2.bitwise_and(img, img, mask=mask)
		frame_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
		frame_resized = cv2.resize(frame_rgb,(darknet.network_width(network),darknet.network_height(network)),interpolation=cv2.INTER_LINEAR)
		darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
		result=darknet.detect_image(network,class_names,darknet_image, thresh=0.25)
		#print(result)
		for i,j in enumerate(result):
			cord=j[2]
			xm=int((cord[0]) * float(x_res/416)) # cent coordinates
			ym=int((cord[1]) * float(y_res/416))
			if cyl > 0:
				for key in track_dict:
					if abs(xm - int(track_dict[key]['xco'])) < diff_pixel:
						cyl_dict={}
						cyl_dict[key]={'xco':xm,'yco':ym}
						break
					else:
						obj= cyl+1
						cyl_dict[obj]={'xco':xm,'yco':ym}

				track_dict.update(cyl_dict)
				cyl=obj
				cyl_dict={}

			if cyl == 0:
				track_dict[cyl]={'xco':xm,'yco':ym}
				cyl=cyl+1
		#print(track_dict,count,st_dict,moving,cyl)
		count=count+1
		if count == 1:
			start_time=datetime.now()
			st_dict=len(track_dict)
	
		elif len(track_dict) > st_dict:
			if moving == False and datetime.now() > start_time+timedelta(seconds=1):
				moving = True
				cyl,count,track_dict = 0,0,{}
			elif moving == True:
				moving = True
				cyl,count,track_dict = 0,0,{}

		elif datetime.now() > start_time+timedelta(seconds=5) and len(track_dict) == st_dict:
			moving = False
			cyl,count,track_dict = 0,0,{}
			
		elif len(result) < st_dict:
			if moving == False and datetime.now() > start_time+timedelta(seconds=1):
				moving = True
				cyl,count,track_dict = 0,0,{}
			elif moving == True:
				moving = True
				cyl,count,track_dict = 0,0,{}

		print(moving)
		cv2.putText(dst, "Moving : "+str(moving), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
		return(moving,dst,track_dict,st_dict,count,cyl)
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		error.raised("2",str(e))
