import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from create_data_types.action import TextAction

class BaseNode(Node):
    def __init__(self):
        super().__init__("send_data_and_answer_while_report_node")
        
        ## ===== 추가  =====================================================
        self.action_server = ActionServer(
            self,
            TextAction,
            "send_data_and_answer_while_report",
            self.action_callback
        )
        ## ================================================================
        
        self.get_logger().info("✅ 초기화 성공!!")
    
    def action_callback(self, goal_handle):
        self.get_logger().info("🔄 액션 서버 콜백 실행")
        self.get_logger().info(f"🔄 목표 핸들: {goal_handle}")
        
        return TextAction.Result(success=True, message="액션 서버 콜백 완료")

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