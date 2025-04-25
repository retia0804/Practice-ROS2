# Send Messages

### 00. 코드 기본 구성성

[Base Code](00_base_code.py)

기본적으로 코드는 다음과 같은 구성을 가진다.

```python
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
```

해당 코드를 보면 먼저 `rclpy.init`을 통해서 ROS 초기화를 진행한다.  
  
이후 `BaseNode`를 생성해 주는데, 해당 노드는 `rclpy.node`의 `Node` 클래스를 상속받았다. 이와 같이 ROS의 패키지는 기본적으로 `Node` 클래스를 상속받는다.  
  
초기화 부분인 `__init__`을 보면 해당 노드의 이름을 부모 노드에 전달해 주며 초기화를 진행해 준다. 해당 노드의 이름은 고유한 이름으로 설정해야 후에 중복으로 인한 문제가 발생되지 않는다. 이후 `get_logger().info()`를 통해서 문자열을 출력해 준다. ROS에서 사용하는 `print()` 함수라고 보면 된다.  
  
해당 Node는 `rclpy.spin`을 통해서 반복을 수행 해 준다. `while True`와 같이 계속 반복을 시키면서 동작이나 이벤트 감지를 수행한다고 보면 된다.
  
해당 Node의 `spin`, 즉 `while True` 문을 종료시켜 주기 위해서 `ctrl + C`를 통해 종료한다. 이때, 에러를 발생시키지 않기 위해서 `try-catch` 문을 추가시켜 주었다. 만약 Node가 종료되었을 때 이후의 코드를 추가했을 때, 에러를 처리하지 못 한다면 뒤의 코드가 실행되지 않고 종료되니 꼭 처리해 주자.

```bash
[INFO] [1745591227.966051788] [base_node]: ✅ 초기화 성공!!
^CTraceback (most recent call last):
  File "/home/retia/practice_ws/src/practice_ros/01_Send_Messages/00_base_code.py", line 22, in <module>
    main()
  File "/home/retia/practice_ws/src/practice_ros/01_Send_Messages/00_base_code.py", line 15, in main
    rclpy.spin(base_node)
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/__init__.py", line 226, in spin
    executor.spin_once()
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/executors.py", line 751, in spin_once
    self._spin_once_impl(timeout_sec)
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/executors.py", line 740, in _spin_once_impl
    handler, entity, node = self.wait_for_ready_callbacks(timeout_sec=timeout_sec)
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/executors.py", line 723, in wait_for_ready_callbacks
    return next(self._cb_iter)
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/executors.py", line 620, in _wait_for_ready_callbacks
    wait_set.wait(timeout_nsec)
KeyboardInterrupt
```

이후 `base_node.destroy_node()` 및 `rclpy.try_shutdown()`을 진행 해 준다. 이 과정을 통해서 Node 및 ROS를 종료 해 준다.  
  
그런데 ROS2 Humble 버전에서는 `KeyboardInterrupt`를 발생시키는 경우 자동으로 `rclpy.shutdown()`이 실행이 된다. 이전 버전에서는 그렇지 않았기에 `rclpy.shutdown()`을 통해서 명시적으로 종료를 해 주었지만, ROS2 Humble 버전에는 필요가 없다. 오히려 `rclpy.shutdown()`를 사용하면 이미 shutdown이 됐는데 또 호출한다고 하여 다음과 같이 에러가 발생한다.

```bash
During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/retia/practice_ws/src/practice_ros/01_Send_Messages/00_base_code.py", line 24, in <module>
    main()
  File "/home/retia/practice_ws/src/practice_ros/01_Send_Messages/00_base_code.py", line 20, in main
    rclpy.shutdown()
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/__init__.py", line 130, in shutdown
    _shutdown(context=context)
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/utilities.py", line 58, in shutdown
    return context.shutdown()
  File "/opt/ros/humble/local/lib/python3.10/dist-packages/rclpy/context.py", line 102, in shutdown
    self.__context.shutdown()
rclpy._rclpy_pybind11.RCLError: failed to shutdown: rcl_shutdown already called on the given context, at ./src/rcl/init.c:241
```

이러한 요소 때문에 `rclpy.try_shutdown()`을 사용을 해 줘야 에러가 출력되지 않는다. Shutdown 상태가 아니면 수행하고, 아니라면 그냥 지나가기 때문에 에러가 발생되지 않는다.  
  
`base_node.destroy()`의 경우에는 만약 처리를 해 주지 않는다면 ROS는 해당 노드가 종료가 되었다는 것을 프로세스가 종료 될 때 까지 알지 못한다. 다음과 같이 `base_node.destory()`를 제거하고 해당 `main` 함수 마지막에 `input()`을 추가해서 실행 해 보자.

```python
def main():
    rclpy.init()
    base_node = BaseNode()
    try:
        rclpy.spin(base_node)
    except KeyboardInterrupt:
        print(" <--- ✅ 사용자 입력으로 인한 프로그램 종료")
    finally:
        # base_node.destroy_node()
        rclpy.try_shutdown()
    
    input()
```

`try_shutdown()`이 실행되었음에도 불구하고, Node의 목록을을 확인해 보면 해당 Node가 여전히 남아 있음을 확인할 수 있다.

```bash
retia@localhost:~/practice_ws/src$ ros2 node list
/base_node
```

하지만 해당 주석을 해제한 후 다시 실행해 보면 동일한 상황임에도 Node 목록에서 제거된 것을 확인할 수 있다.

```bash
retia@localhost:~/practice_ws/src$ ros2 node list
```

이러한 클래스가 아직 구현된 기능은 하나도 없지만, 매우 기본적인 Node의 형태다.

### 