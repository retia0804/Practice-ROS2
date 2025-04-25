import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class BaseNode(Node):
    def __init__(self):
        super().__init__("send_data_and_answer_node")
        
        ## ===== 추가  =====================================================
        self.service_client = self.create_client(Trigger, "send_data_and_answer")
        while not self.service_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("🔄 서비스 준비 중...")
        ## ================================================================
        
        self.get_logger().info("✅ 초기화 성공!!")
    
    def send_msg(self):
        msg = Trigger.Request()
        self.future = self.service_client.call_async(msg)

def main():
    rclpy.init()
    base_node = BaseNode()
    base_node.send_msg()
    try:
        rclpy.spin_until_future_complete(base_node, base_node.future)
        result = base_node.future.result()
        base_node.get_logger().info(f"📨 서비스 호출 결과: [{result.success}] {result.message}")
    except KeyboardInterrupt:
        print(" <--- ✅ 사용자 입력으로 인한 프로그램 종료")
    finally:
        base_node.destroy_node()
        rclpy.try_shutdown()
    

if __name__ == "__main__":
    main()