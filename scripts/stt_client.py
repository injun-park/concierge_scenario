import sys
import rospy
from concierge_scenario.srv import sr_result, sr_resultResponse, sr_resultRequest

class SttClient :
    def __init__(self):
        rospy.wait_for_service("/stt")

    def callService(self):
        result = None
        try :
            service = rospy.ServiceProxy("/stt", sr_result)
            req = sr_resultRequest()
            req.data = ''
            req.opcode = 1
            result = service(req)
        except rospy.ServiceException, e:
            rospy.logerr("Service call failed:" + str(e))

        print "result : ", result
        return result

if __name__ == "__main__" :
    rospy.init_node("stt_client", anonymous=True)
    client = SttClient()
    result = client.callService()
    rospy.loginfo("sentence : " + result.result +", success_flag : " + str(result.success_flag))