import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class BaseNode(Node):
    def __init__(self):
        super().__init__("send_data_node")
        
        ## ===== 추가  =====================================================
        self.publisher = self.create_publisher(String, "send_data", 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        ## ================================================================
        
        self.get_logger().info("✅ 초기화 성공!!")
    
    def timer_callback(self):
        msg = String()
        msg.data = "여러분!! 모두 안녕하세요!!"
        
        self.publisher.publish(msg)
        self.get_logger().info(f"📨 메세지 전송! : {msg.data}")
        

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