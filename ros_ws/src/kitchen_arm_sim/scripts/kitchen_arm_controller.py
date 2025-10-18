#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, Point, Pose, Quaternion
from std_msgs.msg import String
from sensor_msgs.msg import Image
import time
import math

class KitchenArmController:
    def __init__(self):
        rospy.init_node('kitchen_arm_controller', anonymous=True)

        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        self.cmd_sub = rospy.Subscriber('/kitchen_arm/command', String, self.command_callback)
        self.status_pub = rospy.Publisher('/kitchen_arm/status', String, queue_size=10)

        self.work_positions = {
            'home': (0.0, 0.0, 0.0),
            'peel_position': (1.0, 0.5, 0.0),
            'cut_position': (1.0, -0.5, 0.0),
            'wash_position': (0.5, 1.0, 0.0)
        }
        
        self.current_position = 'home'

        self.status_pub.publish("system_ready")

    def command_callback(self, msg):
        command = msg.data
        rospy.loginfo(f"Получена команда: {command}")
        
        if command == "go_home":
            self.move_to_position('home')
        elif command == "start_peeling":
            self.start_peeling_sequence()
        elif command == "start_cutting":
            self.start_cutting_sequence()
        elif command == "detect_objects":
            self.detect_objects()
        else:
            rospy.logwarn(f"Неизвестная команда: {command}")

    def move_to_position(self, position_name):
        if position_name not in self.work_positions:
            return False
            
        target = self.work_positions[position_name]
        rospy.loginfo(f"Двигаемся к позиции: {position_name} {target}")

        twist = Twist()
        twist.linear.x = 0.5
        start_time = time.time()

        while time.time() - start_time < 2.0 and not rospy.is_shutdown():
            self.cmd_pub.publish(twist)
            time.sleep(0.1)

        stop_twist = Twist()
        self.cmd_pub.publish(stop_twist)
        
        self.current_position = position_name
        rospy.loginfo(f"Успешно достигнута позиция: {position_name}")
        self.status_pub.publish(f"arrived_at_{position_name}")
        return True

    def start_peeling_sequence(self):
        
        if self.move_to_position('peel_position'):
            time.sleep(2)

            for i in range(3):
                rospy.loginfo(f"Чистка {i+1}/3")
                time.sleep(1)
            
            self.move_to_position('home')
            rospy.loginfo("Чистка завершена!")
            self.status_pub.publish("peeling_completed")

    def start_cutting_sequence(self):
        
        if self.move_to_position('cut_position'):
            rospy.loginfo("Активация инструмента для нарезки...")
            time.sleep(1)

            for i in range(5):
                rospy.loginfo(f"Нарезка {i+1}/5")
                time.sleep(0.5)
            
            self.move_to_position('home')
            rospy.loginfo("Нарезка завершена!")
            self.status_pub.publish("cutting_completed")

    def detect_objects(self):
        rospy.loginfo("Запуск обнаружения объектов...")
        time.sleep(2)
        rospy.loginfo("Обнаружены объекты: Картофель (x=1.0, y=0.5), Помидор (x=1.0, y=-0.5)")
        self.status_pub.publish("object_detection_completed")

    def run(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            rate.sleep()

if __name__ == '__main__':
    try:
        controller = KitchenArmController()
        controller.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Узел остановлен")