import rclpy
from rclpy.node import Node


class BaseNode(Node):
    def __init__(self):
        super().__init__("base_node")
        
        self.get_logger().info("✅ 초기화 성공!!")
        

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