import os
import apriltag
import cv2

# specify the img directory path
path = "../BetterData"

# list files in img directory
files = os.listdir(path)

#These were the example options from the docs
options = apriltag.DetectorOptions(families='tag36h11',
                                 border=1,
                                 nthreads=4,
                                 quad_decimate=1.0,
                                 quad_blur=0.0,
                                 refine_edges=True,
                                 refine_decode=False,
                                 refine_pose=False,
                                 debug=False,
                                 quad_contours=True)

# Create a detector
detector = apriltag.Detector(options)

# Just list all the files
for file in files:
    # make sure file is an image
    if file.endswith(('.jpg', '.png', 'jpeg')):
        img_path=os.path.join(path, file)
        print(img_path)
        img = cv2.imread(img_path)
        # The detector wants grayscale so convert
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        # This is used below to convert corners to a width
        width = gray.shape[1]
        height = gray.shape[0]

        # Actually get the results
        result = detector.detect(gray)
        if len(result)!=0:
            print(result) 
            print("tag ID", result[0].tag_id)
            print("corners:", result[0].corners[0][0]/width,
                  result[0].corners[0][1]/height,  
                  result[0].corners[1][0]/width,
                  result[0].corners[1][0]/height,
                  result[0].corners[2][0]/width,
                  result[0].corners[2][1]/height,  
                  result[0].corners[3][0]/width,
                  result[0].corners[3][0]/height)
            print("center:", result[0].center)
            



