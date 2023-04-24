import cv2

# Read in the video file
video = cv2.VideoCapture('img/testvid.mp4')
fps = int(video.get(cv2.CAP_PROP_FPS))
count = 0


# Define the kernel size for the blur effect
kernel_size = (15, 15)
writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'avc1'), fps, (720, 480))




while True:
    ret, frame = video.read()
    
    if not ret:
        break
    blurred_frame = cv2.GaussianBlur(frame, kernel_size, 0)
    writer.write(blurred_frame)
    
# Release the resources used by the VideoCapture and VideoWriter objects
video.release()
writer.release()

cap = cv2.VideoCapture('output.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        cv2.imshow('Frame',frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    else: 
        break
 
cap.release()
cv2.destroyAllWindows()