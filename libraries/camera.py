import cv2
import numpy as np

try:
    print("\n Open camera")
    capturing_Flag = True
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc,20,(640,480))
    while (capturing_Flag):
        ret,origin = cap.read()
        cv2.imshow("Capture",origin)
        out.write(origin)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            capturing_Flag = False
            print("\nClose camera")
            break
    cv2.destroyAllWindows()
    out.release()
except KeyboardInterrupt:
    print("\nClose camera")
    capturing_Flag = False