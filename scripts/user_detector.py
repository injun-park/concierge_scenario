import rospy
from user_detection.msg import  UserDetectionMsg

class UserDetector :

    __THRESHOLD_POINT_COUNT = 30000

    def __init__(self):
        self.detected = False
        self.averageDistance = 0.0
        self.pointSize = 0

    def userDetectedCallback(self, data):
        # rospy.loginfo("data.detected : " + str(data.detected) +
        #               ", data.point_size : " + str(data.point_size) +
        #               ", data.average_distance : " + str(data.average_distance) )

        self.detected = True
        self.averageDistance = data.average_distance
        self.pointSize = data.point_size

    def isDetected(self):
        if self.averageDistance < 1.0 and self.pointSize > UserDetector.__THRESHOLD_POINT_COUNT :
            return True

        return False

    def startDetection(self):
        self._userDetectorSubscriber = rospy.Subscriber('/distance_filter/data', UserDetectionMsg, self.userDetectedCallback)
        return True

    def stopDetection(self):
        self._userDetectorSubscriber.unregister()


    def checkDetection(self):
        duration = rospy.Duration(0.05) # 20hz
        detected = False

        while not self.isDetected() :
            rospy.sleep(duration)
            continue

class CannotDetectUserException(Exception) :
    def __init__(self):
        self.value = "CannotDetecUserException"

    def __str__(self):
        return self.value