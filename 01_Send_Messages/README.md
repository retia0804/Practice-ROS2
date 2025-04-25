# Send Messages

## 00. 코드 기본 구성

[Base Code](00_base_code.py)

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

<details>

<summary>코드 설명</summary>

해당 코드를 보면 먼저 `rclpy.init`을 통해서 ROS 초기화를 진행한다.  
  
이후 `BaseNode`를 생성해 주는데, 해당 노드는 `rclpy.node`의 `Node` 클래스를 상속받았다. 이와 같이 ROS의 패키지는 기본적으로 `Node` 클래스를 상속받는다.  
  
초기화 부분인 `__init__`을 보면 해당 노드의 이름을 부모 노드에 전달해 주며 초기화를 진행해 준다. 해당 노드의 이름은 고유한 이름으로 설정해야 후에 중복으로 인한 문제가 발생되지 않는다. 이후 `get_logger().info()`를 통해서 문자열을 출력해 준다. ROS에서 사용하는 `print()` 함수라고 보면 된다.  
  
해당 Node는 `rclpy.spin`을 통해서 반복을 수행 해 준다. `while True`와 같이 계속 반복을 시키면서 동작이나 이벤트 감지를 수행한다고 보면 된다.
  
해당 Node의 `spin`, 즉 `while True` 문을 종료시켜 주기 위해서 `ctrl + C`를 통해 종료한다. 이때, 에러를 발생시키지 않기 위해서 `try-catch` 문을 추가시켜 주었다. 만약 Node가 종료되었을 때 이후의 코드를 추가했을 때, 에러를 처리하지 못 한다면 뒤의 코드가 실행되지 않고 종료되니 꼭 처리해 주자.

```bash
retia@localhost:~/practice_ws/src/practice_ros$ python3 00_base_code.py
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
</details>

## 01. 메세지 보내기

[Send Message Code](01_send_data_code.py)

```python
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
```

<details>

<summary>코드 설명</summary>
먼저 바뀌지 않은 부분을 보면 `main` 함수 내부는 변하지 않았다. 해당 기능에 맞게 클래스 명 및 변수 명을 수정해 줘도 되지만, 구조적으로는 동일하고, 바꾸지 않아도 문제는는 발생하지 않는다. 여기서는 점차 변하는 부분만 확인하기 위해 가능하면 코드를 수정하지 않겠다.  

다만 한 가지, 매번 바뀌는 것이 있다면 `super().__init__()` 내부에 주는 노드의 이름이다. 노드의 이름이 동일하게 된다면 문제가 발생할 수 있다. 그래서 이번에는 `send_data_node`라고 이름을 지어 주었다.  

해당 코드에서 추가된 내용은 `create_publisher`와 `create_timer`이다.  

`create_publisher`는 메시지를 뿌리는 곳이다. 해당 부분에서 생성된 `self.publisher`에게 데이터를 넣으면 모든 사람에게 메시지를 보낸다. 이때, 변수가 들어가는 `String`의 경우 메시지의 내용 형식이고, `send_data`는 메시지의 제목, `10`은 버퍼인데 아직까지 구체적으로 알 필요는 없다.  

`create_timer`는 해당 타이머 시간에 맞춰 지속적으로 무언가를 수행하도록 한다. 이때, `1.0`이 몇 초 주기로 실할 지를 결정하고, `self.timer_callback`이 실행할 동작이다.  

`self.timer_callback`에서 가장 먼저 아까 보낼 데이터의 타입인 `String`을 생성하고는, 그 내부에 실제 우리가 보내고 싶은 데이터인 `"여러분!! 모두 안녕하세요!!"`를 넣어주는 것을 확인할 수 있다. `.msg`에 대한 것은 아직 알 필요 없고, 그냥 그렇게 데이터를 넣을 수 있구나 라고만 생각하면 된다.  

그리고 마지막으로 우리는 아까 말했던 것 처럼 `self.publisher`에 우리가 만든 메시지인 `msg`를 넣어서 전송을 해 준다. 이후 실행되는 `self.get_logger().info()`는 단순하게 전송 확인 용으로만 출력되는 log 데이터다.  

그 결과 다음과 같이 1초 주기로 데이터가 출력된다.

```bash
retia@localhost:~/practice_ws/src/practice_ros/01_Send_Messages$ python3 01_send_data_code.py 
[INFO] [1745594137.516686931] [send_data_node]: ✅ 초기화 성공!!
[INFO] [1745594138.510774870] [send_data_node]: 📨 메세지 전송! : 여러분!! 모두 안녕하세요!!
[INFO] [1745594139.510568489] [send_data_node]: 📨 메세지 전송! : 여러분!! 모두 안녕하세요!!
[INFO] [1745594140.510655003] [send_data_node]: 📨 메세지 전송! : 여러분!! 모두 안녕하세요!!
[INFO] [1745594141.510643157] [send_data_node]: 📨 메세지 전송! : 여러분!! 모두 안녕하세요!!
```

그리고 출력되는 토픽 이름이 새로 생긴 것도 불 수 있다.

```bash
retia@localhost:~/practice_ws/src/practice_ros$ ros2 topic list
/parameter_events
/rosout
/send_data
```

그 내부 데이터도 직접 확인해 볼 수 있다.

```bash
retia@localhost:~/practice_ws/src/practice_ros$ ros2 topic echo /send_data
data: 여러분!! 모두 안녕하세요!!
---
data: 여러분!! 모두 안녕하세요!!
---
data: 여러분!! 모두 안녕하세요!!
---
```
</details>


## 02. 메세지 받기

[Send Message Code](02_receive_data_code.py)

```python
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
```

<details>

<summary>코드 설명</summary>
이번에는 메시지를 받는 코드를 만들어 본다. 먼저 해당 노드의 이름을 `receive_data_node`로 수정을 해 주자.   

[Send Message Code](01_send_data_code.py)에서 보낸 코드를 받기 위해서는 해당 메시지의 타입과 제목을 알면 된다. 타입의 경우 `String`이였고, 제목의 경우 `send_data`였다. 해당 요소를 `self.create_subscription`에 넣어서 메시지를 받을 수 있다. 해당 메시지가 도착할 때 마다 실행할 함수는 `self.subscriber_callback`으로 선언을 해 줄 수 있다.  

아까 왜인지는 알 수 없지만, 우리가 전송을 원하는 데이터의 경우 `msg.data`에 저장했던 것을 기억할 수 있다. 이번에는 반대로 `msg.data`에서 데이터를 꺼내면 된다. 수신 확인을 위해 `self.get_logger().info()`를 사용해서 출력한다.  

그 결과 다음과 같이 출력되는 것을 확인할 수 있다.

```bash
retia@localhost:~/practice_ws/src/practice_ros/01_Send_Messages$ python3 02_receive_data_code.py 
[INFO] [1745594455.345600841] [receive_data_node]: ✅ 초기화 성공!!
[INFO] [1745594455.756395387] [receive_data_node]: 📨 메세지 수신! : 여러분!! 모두 안녕하세요!!
[INFO] [1745594456.756405630] [receive_data_node]: 📨 메세지 수신! : 여러분!! 모두 안녕하세요!!
[INFO] [1745594457.756394909] [receive_data_node]: 📨 메세지 수신! : 여러분!! 모두 안녕하세요!!
```
</details>









## 03. 답장을 받는 메세지 받기

[Send Message and Answer Code](03_recieve_data_and_answer.py)

```python
import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class BaseNode(Node):
    def __init__(self):
        super().__init__("receive_data_and_answer_node")
        
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
```

<details>

<summary>코드 설명</summary>
이번에는 답장이 오기를 기대하는 메세지를 활용해 보자. 그 중 받는 입장을 먼저 구현한다. 그래서서 노드 이름을 `receive_data_and_answer_node`으로 지정한다.  

해당 내용은 사실상 이전 두 단계의 합이라고 볼 수도 있다. 먼저 데이터를 보낼 때 고려했던 데이터 타입 `Trigger`과 메시지 제목 `"send_data_and_answer"`, 그리고 메시지를 받았을 때 수행할 동작 `self.service_callback`으로 구성된다.  

`service_callback`의 인자를 보면 `request`와 `response`이 있다. 해당 요소 중 `request`의 경우 다른 사람이 보낸 데이터를 이곳에 저장되어 있다. 그래서 함수 내부에서 해당 데이터를 활용해서 여러가지를 수행하면 된다. `response`의 경우에는 우리가 보낼 데이터이다. 그래서 우리가 해당 요소에 데이터를 할당 해서 `return`을 통해 다시 데이터를 보낸 쪽으로 전송을 해 주면 된다.  

해당 코드를 실행해 보면, 아직은 우리한테 메시지를 보내는 곳이 없기 때문에 진행되지 않는다.

```bash
retia@localhost:~/practice_ws/src/practice_ros/01_Send_Messages$ python3 03_send_data_and_answer.py 
[INFO] [1745595554.275620436] [send_data_node]: ✅ 초기화 성공!!
```

하지만 이러한 서비스 목록을 확인 해 보면 해당 메시지가 목록에 추가 된 것을 확인할 수 있다. 해당 요소 중에서 `/send_data_node`로 시작되는 것들은 Node를 시작할 때 기본적으로 생성되는 것이므로 무시해도 된다. 그것 말고, `/send_data_and_answer`가 추가된 것을 확인해 볼 수 있다.

```bash
retia@localhost:~/practice_ws/src/practice_ros$ ros2 service list
/send_data_and_answer
/send_data_node/describe_parameters
/send_data_node/get_parameter_types
/send_data_node/get_parameters
/send_data_node/list_parameters
/send_data_node/set_parameters
/send_data_node/set_parameters_atomically
```
</details>








## 04. 답장을 받는 메세지 보내기기

[Send Message Code](01_send_data_code.py)

```python
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
```

<details>

<summary>코드 설명</summary>
이번에는 답장이 오기를 기대하는 메세지를 주는 입장이다다. 그래서서 노드 이름을 `send_data_and_answer_node`으로 지정한다.  

이전에 메세지를 보낼 때는 타이머를 사용해서 데이터를 주기적으로 전송했다. 하지만 이번에는 답장이 올 때 까지 대기해야 하므로 타이머를 사용하지 않는다. 왜냐하면 상대방이 답장을 보낼 때 까지 얼마의 시간이 걸릴 지 알 수 없기 때문이다.  

이 때문에 `main` 함수 내부가 변한다. 기존에는 `rclpy.spin`을 통해서 무한히 반복을 하였다. 하지만 이번에는 딱 한 번만 수행하도록 수정해야 한다.  

먼저 초기화 `__init__` 부분을 보자. 메시지를 보낼 때와 마찬가지로 메시지 타입 및 그 제목을 지정 해 준다. 그런데 추가적으로 그 뒤에 `wait_for_service`를 사용하는 것을 볼 수 있다. 이는, 기존에는 그냥 메시지를 보내면 상대방이 실제로 메시지를 받든 말든 상관을 할 필요가 없었다. 하지만 이번에는 우리는 꼭 답장을 받아야 한다. 그러므로 상대방이 답장을 받을 준비가 되었는지 여부를 확인하는 과정이 필요 한 것이다. 다음과 같은 요소가 나와 있다면 해당 부분을 지나서 정상적으로 초기화가 된다.

```bash
retia@localhost:~/practice_ws/src/practice_ros$ ros2 service list
/send_data_and_answer
```

만약 준비가 되지 않았다면 계속 기다린다.
```bash
retia@localhost:~/practice_ws/src/practice_ros/01_Send_Messages$ python3 04_send_data_and_answer.py 
[INFO] [1745596740.109029372] [send_data_and_answer_node]: 🔄 서비스 준비 중...
[INFO] [1745596735.264405273] [send_data_and_answer_node]: 🔄 서비스 준비 중...
[INFO] [1745596736.266325297] [send_data_and_answer_node]: 🔄 서비스 준비 중...
```

그 다음으로 `send_msg` 함수를 보자. 기존 메시지를 보내는 함수와 유사한 것을 볼 수 있다. 먼저 보낼 메시지의 형식을 선언하고, (이곳에서는 넣지는 않았지만) 전송할 데이터를 삽입한다. 그리고 `self.service_client`에 넣어서 대상에게 메시지를 보내면 된다. 이때 반환값인 `self.future`의 경우 답장을 받을 장소이므로 꼭 저장을 해 둬야 한다.  

이번에는 `main` 함수를 보자. 해당 코드에서 `rclpy.spin_until_future_complete`는 답장이 올 때 까지 `rclpy.spin()`을 반복하는 함수다. 다만 차이점은 답장이 오면 해당 반복을 종료한다는 점 이다.  

답장의 결과는 우리가 답장을 받을 장소인 `self.future.result()`로 얻을 수 있다. 그리고 그 내부에 해당 답장의 내용물인 `result.success`와 `result.messgae`를 log로 출력해 주고 종료를 해 준다. 보내는 곳과 받는 곳 모두 정상적으로 작동함을 확인할 수 있다.

```bash
retia@localhost:~/practice_ws/src/practice_ros/01_Send_Messages$ python3 03_recieve_data_and_answer.py 
[INFO] [1745596752.530636544] [send_data_and_answer_node]: ✅ 초기화 성공!!
[INFO] [1745596824.700190993] [send_data_and_answer_node]: 🖨️ 서비스 작업 시작!!
[INFO] [1745596824.700458831] [send_data_and_answer_node]: 📄 서비스 작업 중... (1/3)
[INFO] [1745596825.201478143] [send_data_and_answer_node]: 📄 서비스 작업 중... (2/3)
[INFO] [1745596825.702530814] [send_data_and_answer_node]: 📄 서비스 작업 중... (3/3)
[INFO] [1745596825.702890031] [send_data_and_answer_node]: 📨 서비스 작업 완료!!
```

```bash
retia@localhost:~/practice_ws/src/practice_ros/01_Send_Messages$ python3 04_send_data_and_answer.py 
[INFO] [1745596848.847738634] [send_data_and_answer_node]: ✅ 초기화 성공!!
[INFO] [1745596849.851751046] [send_data_and_answer_node]: 📨 서비스 호출 결과: [True] 서비스 작업 완료!!
```
</details>



## 05.

[Send Message Code](01_send_data_code.py)

```python

```

<details>

<summary>코드 설명</summary>

</details>




## 06.

[Send Message Code](01_send_data_code.py)

```python

```

<details>

<summary>코드 설명</summary>

</details>


## 07.

[Send Message Code](01_send_data_code.py)

```python

```

<details>

<summary>코드 설명</summary>

</details>




## 08.

[Send Message Code](01_send_data_code.py)

```python

```

<details>

<summary>코드 설명</summary>

</details>