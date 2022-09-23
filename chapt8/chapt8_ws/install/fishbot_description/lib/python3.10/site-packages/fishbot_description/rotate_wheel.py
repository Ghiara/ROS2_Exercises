#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import threading
import time


class RotateWheelNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info(f"node {name} init..")
        # 2.创建并初始化发布者成员属性pub_joint_states_
        self.joint_states_publisher_ = self.create_publisher(JointState,"joint_states", 10)
        # 初始化数据
        self._init_joint_states()
        self.pub_rate = self.create_rate(30) # 30Hz
        self.thread_ = threading.Thread(target=self._thread_pub)
        self.thread_.start()
    
    def _init_joint_states(self):
        # 初始左右轮子的速度
        self.joint_speeds = [0.0, 0.0]
        
        self.joint_states = JointState() # 关节状态实例对象
        '''
        string[] name #关节名称数组
        float64[] position #关节位置数组
        float64[] velocity #关节速度数组
        float64[] effort #扭矩数据
        '''
        self.joint_states.header.stamp = self.get_clock().now().to_msg()
        self.joint_states.header.frame_id = ""
        # 关节名称==urdf文件中的命名
        self.joint_states.name = ['left_wheel_joint','right_wheel_joint']
        # 关节的位置
        self.joint_states.position = [0.0,0.0]
        # 关节速度
        self.joint_states.velocity = self.joint_speeds
        # 关节扭矩 
        self.joint_states.effort = []

    def update_speed(self,speeds):
        self.joint_speeds = speeds

    def _thread_pub(self):
        last_update_time = time.time()
        while rclpy.ok():
            delta_time =  time.time()-last_update_time
            last_update_time = time.time()
            # 更新位置
            self.joint_states.position[0]  += delta_time*self.joint_states.velocity[0]
            self.joint_states.position[1]  += delta_time*self.joint_states.velocity[1]
            # 更新速度
            self.joint_states.velocity = self.joint_speeds
            # 更新 header
            self.joint_states.header.stamp = self.get_clock().now().to_msg()
            # 发布关节数据
            self.joint_states_publisher_.publish(self.joint_states)
            self.pub_rate.sleep()

def main(args=None):
    """
    ros2运行该节点的入口函数
    1. 导入库文件
    2. 初始化客户端库
    3. 新建节点
    4. spin循环节点
    5. 关闭客户端库
    """
    rclpy.init(args=args) # 初始化rclpy
    node = RotateWheelNode("rotate_fishbot_wheel")  # 新建一个节点
    node.update_speed([15.0, -15.0])
    rclpy.spin(node) # 保持节点运行，检测是否收到退出指令（Ctrl+C）
    rclpy.shutdown() # 关闭rclpy
