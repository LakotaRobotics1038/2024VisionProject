import apriltag
import cv2
cam0 = cv2.VideoCapture(0)
#img = cv2.imread('apriltag_foto.jpg'.cv2.IMREAD_GRAYSCALE)
ret, img = cam0.read()
print(ret)
print(img.shape)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


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

detector = apriltag.Detector(options)
result = detector.detect(gray)

cv2.imwrite("webcam.jpg", gray) 

print(result)