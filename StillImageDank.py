import cv2, numpy as np
eyeData = "eyes.xml"
faceData = "face.xml"
DOWNSCALE = 1

cv2.namedWindow("preview")
eyeClass = cv2.CascadeClassifier(eyeData)
faceClass = cv2.CascadeClassifier(faceData)

glasses = cv2.imread('glasses.png', cv2.IMREAD_UNCHANGED)
fedora = cv2.imread('fedora.png', cv2.IMREAD_UNCHANGED)
frame = cv2.imread('10343008_755623507838171_1819194393080045569_n.jpg')

ratio = glasses.shape[1] / glasses.shape[0]
# detect eyes and draw glasses
minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
miniframe = cv2.resize(frame, minisize)
eyes = eyeClass.detectMultiScale(miniframe)
faces = faceClass.detectMultiScale(miniframe)

for eye in eyes:
    x, y, w, h = [ v*DOWNSCALE for v in eye ]
    h = w / ratio
    y += h / 2
    # resize glasses to a new var called small glasses
    smallglasses = cv2.resize(glasses, (w, h))
    # the area you want to change
    bg = frame[y:y+h, x:x+w]
    bg *= np.atleast_3d(255 - smallglasses[:, :, 3])/255.0
    bg += smallglasses[:, :, 0:3] * np.atleast_3d(smallglasses[:, :, 3])
    # put the changed image back into the scene
    frame[y:y+h, x:x+w] = bg

cv2.imshow("preview", frame)

while True:
    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]: # exit on ESC
        cv2.destroyWindow("preview")
        break
