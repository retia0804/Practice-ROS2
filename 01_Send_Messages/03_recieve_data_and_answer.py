import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class BaseNode(Node):
    def __init__(self):
        super().__init__("send_data_and_answer_node")
        
        ## ===== 추가  =====================================================
        self.service_server = self.create_service(Trigger, "send_data_and_answer", self.service_callback)
        ## ================================================================
        
        self.get_logger().info("✅ 초기화 성공!!")
    
    def service_callback(self, request, response):
        response.success = True
        response.message = "서비스 작업 완료!!"
        
        self.get_logger().info(f"🖨️ 서비스 작업 시작!!")
        self.get_logger().info(f"📄 서비스 작업 중... (1/3)")
        time.sleep(0.5)
        
        self.get_logger().info(f"📄 서비스 작업 중... (2/3)")
        time.sleep(0.5)
        
        self.get_logger().info(f"📄 서비스 작업 중... (3/3)")
        self.get_logger().info(f"📨 서비스 작업 완료!!")
        
        return response
        

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