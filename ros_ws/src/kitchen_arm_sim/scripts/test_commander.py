#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import time

def send_test_commands():
    rospy.init_node('test_commander')
    pub = rospy.Publisher('/kitchen_arm/command', String, queue_size=10)

    rospy.sleep(8)
    
    commands = [
        "go_home",
        "detect_objects", 
        "start_peeling",
        "start_cutting",
        "go_home"
    ]
    
    for i, cmd in enumerate(commands):
        rospy.loginfo(f"Команда {i+1}/{len(commands)}: {cmd}")
        pub.publish(String(cmd))
        rospy.sleep(6)

    rospy.spin()

if __name__ == '__main__':
    try:
        send_test_commands()
    except rospy.ROSInterruptException:
        rospy.loginfo("Тестовый узел остановлен")
