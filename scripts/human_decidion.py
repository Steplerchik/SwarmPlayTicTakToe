#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

pub = rospy.Publisher('human_turns_sim', String, queue_size=10)
rospy.init_node('human_simulation', anonymous=True)
rate = rospy.Rate(10) # 10hz

def talker(player_answer):
    str_answer = player_answer
    rospy.loginfo(str_answer)
    pub.publish(str_answer)
    rate.sleep()

if __name__ == '__main__':
    try:
	while True:
	     player_answer = input("Where put O?")
             talker(str(player_answer))
    except rospy.ROSInterruptException:
        pass
