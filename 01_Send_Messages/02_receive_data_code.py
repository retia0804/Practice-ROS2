import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class BaseNode(Node):
    def __init__(self):
        super().__init__("receive_data_node")
        
        ## ===== 추가  =====================================================
        self.subscriber = self.create_subscription(String, "send_data", self.subscriber_callback, 10)
        ## ================================================================
        
        self.get_logger().info("✅ 초기화 성공!!")
    
    def subscriber_callback(self, msg):
        self.get_logger().info(f"📨 메세지 수신! : {msg.data}")
        

def main():
    rclpy.init()
    base_node = BaseNode()
    try:
        rclpy.spin(base_node)
    except KeyboardInterrupt:
        print(" <--- ✅ 사용자 입력으로 인한 프로그램 종료")
    finally:
        base_node.destroy_node()
        rclpy.try_shutdown()
    

if __name__ == "__main__":
    main()