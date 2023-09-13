import cv2
import time
# variables
initialTime = 0
initialDistance = 0
changeInTime = 0
changeInDistance = 0

listDistance = []
listSpeed = []

# distance from camera to object(face) measured
Known_distance = 76.2  # centimeter
# width of face in the real world or Object Plane
Known_width = 14.3  # centimeter
# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture(0)

# cap.set(3, 640)
# cap.set(4, 480)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
Recorder = cv2.VideoWriter('distanceAndSpeed2.mp4', fourcc, 15.0, (640, 480))
# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# focal length finder function


def FocalLength(measured_distance, real_width, width_in_rf_image):

    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length
# distance estimation function


def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
 
    distance = (real_face_width * Focal_Length)/face_width_in_frame
    return distance


def face_data(image):


    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), WHITE, 1)
        face_width = w

    return face_width


def speedFinder(coveredDistance, timeTaken):

    speed = coveredDistance / timeTaken

    return speed


def averageFinder(completeList, averageOfItems):

    # finding the length of list.
    lengthOfList = len(completeList)

    # calculating the number items to find the average of
    selectedItems = lengthOfList - averageOfItems
    # 10 -6 =4

    # getting the list most recent items of list to find average of .
    selectedItemsList = completeList[selectedItems:]

    # finding the average .
    average = sum(selectedItemsList) / len(selectedItemsList)

    return average


# reading reference image from directory
ref_image = cv2.imread("Ref_image.png")

ref_image_face_width = face_data(ref_image)
Focal_length_found = FocalLength(
    Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)
# cv2.imshow("ref_image", ref_image)

while True:
    _, frame = cap.read()

    # calling face_data function
    face_width_in_frame = face_data(frame)
    # finding the distance by calling function Distance
    if face_width_in_frame != 0:
        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)
        listDistance.append(Distance)
        averageDistance = averageFinder(listDistance, 2)

        # converting centimeters into meters
        distanceInMeters = averageDistance/100

        if initialDistance != 0:
            # finding the change in distance
            changeInDistance = initialDistance - distanceInMeters

            
            changeInTime = time.time() - initialTime

            # finding the sped
            speed = speedFinder(
                coveredDistance=changeInDistance, timeTaken=changeInTime)
            listSpeed.append(speed)
            averageSpeed = averageFinder(listSpeed, 10)
            if averageSpeed < 0:
                averageSpeed = averageSpeed * -1
            # filling the progressive line dependent on the speed.
            speedFill = int(45+(averageSpeed) * 130)
            if speedFill > 235:
                speedFill = 235
            cv2.line(frame, (45, 70), (235, 70), (0, 255, 0), 35)
            # speed dependent line
            cv2.line(frame, (45, 70), (speedFill, 70), (255, 255, 0), 32)
            cv2.line(frame, (45, 70), (235, 70), (0, 0, 0), 22)
            # print()
            cv2.putText(
                frame, f"Speed: {round(averageSpeed, 2)} m/s", (50, 75), fonts, 0.6, (0, 255, 220), 2)

            # print(speed)

        # inital distance and time
        initialDistance = distanceInMeters
        initialTime = time.time()

    # Drwaing Text on the screen
        cv2.line(frame, (45, 25), (255, 25), (255, 0, 255), 30)
        cv2.line(frame, (45, 25), (255, 25), (0, 0, 0), 22)
        cv2.putText(
            frame, f"Distance = {round(distanceInMeters,2)} m", (50, 30), fonts, 0.6, WHITE, 2)
    # recording the video
    Recorder.write(frame)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
Recorder.release()
cv2.destroyAllWindows()
