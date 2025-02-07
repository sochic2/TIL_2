# Java

- 프로그램 언어
  - 스크립트 언어 : 파이썬, R, JavaScript -> 코드 읽을 때 코드를 쭉 기계어로 번역
    - 쉽다. 느리다.
    - 컴파일러가 아예 없진 않음.
  - 컴파일 언어 : 자바 -> 코드 전체를 컴파일러를 통해 한번에 바이트코드를 생성해서 기계어로  번역
    - 어렵다. 빠르다.
- classpath
  - app.java(컴파일) -> app.class(byte) 
  - application context
    - 자바 경로는 package로 구분: me.nkc.app -> me/nkc/app
    - User/namkicheol/javaExam/me/nkc/app => /me부터를 root로 잡음
- JVM
  - java program -> proess(jvm 실행) OS native함. -> class 읽어서 처리
    - Ex) mobile native(ios, android)
  - jvm 자체는 window, linux따라 설치, but 코드는 변경할 필요가 없음

- Build -> 소스를 타겟 형태로 변환하는 형태
- object, class, instance
  - 논리적인 개념으로 설명 가능한 객체(object)
  - 코드화 된 설계서(class)
  - 실제 런타임에 클래스의 생성자를 통해 생성된 객체(instance)



- 자료구조(Data Structure) : Stack, Queue, Heap, Linked List, Tree
  - 단일값만 취급 x, 여러 값들의 그룹 형태로 제어해야 할 경우 발생
  - Array(얘도 자료구조중 하나) : index를 갖고, value를 갖고, 특정 값에 접근하려면 해당 inex 알아야 함
    - Java 인덱스 고정하여 생성(몇 개의 값을 가질 것이냐 정의)
  - Java Collection Framework 
    - List, Stack, Queue, Heap 등 존재
- 숫자야구 게임 목요일까지
- 숫자는 만들어진거고, 







Cpu  `   1    `

memory `  2gb  `  cpu:1, memory:2gb =>



github 주소, image명, 



List -> 



=> git주소, base image

=>deployment, service, ingress 





# Java2일

### Interface

### 객체지향 프로그래밍(OOP) -> 설계원칙

- 대상은 객체(현실세계나 개념적으로 이해가능한 대상) -> 프로그램에 녹여내야 된다.
- ex) 대학교 학사관리 시스템
  - 학생, 교수 -> 속성과 기능을 추출하는 것
  - 학생 추상화 -> 인스턴스화 시 : 대학교1학년 학부, 4학년 졸업반 학생 (공통, 그렇지 않은 부분) 

- 객체의 속성은 객체가 주체적으로 변경, 객체간의 메시지(Payload)를 전달하여 소통한다. 
  - 해당 객체 끼리 요청한다.? ex) 플레이어는 Deck한테 카드 내놔 라고 함.
- 제일 먼저 해야할 것은 기능 구상
  - 기능을 나열, 기능이 해야할 역할을 구분지음.

- SOLID 원칙
  - SRP : 단일책임 원칙
  - OCP : 개방 폐쇄 원칙
  - LSP : 리스코프 치환 원칙
  - ISP : 인터페이스 
  - DIP : 의존관계 역전 원칙(dependancy Injection)
- Spring의 핵심은 -> SOLID 지킬 수 있게 도와주는 DI, IoC를 갖고 있음
- 

### Implements

- 





### Spring

- DI
  - 인스턴스화를 외부에서 해서 주입해줌
- 설정과 구동을 분리, => ex) Oracle -> Mysql 변경시에 서비스 영역 변경 안하고, 주입하는 부분만 고치면됨
- Bean으로 최초 모두 생성함

- Default는 singleton



- IoC Container
  - Ex) Bean Creation에러가 자주남
  - 각자 정의한 Bean들을 생성, 필요한 Object 주입, 의존하고 있는 인스턴스에 주입.
  - Application Context부분에서 
- 



- Bean들은 thread별로 움직여서 Singleton인게 별로 상관이 없음.

- Servlet container(톰캣) -> thread생성. ->





- blackjack을 spring을 써서 DI를 생성해야되는 객체를 다 Bean으로? 주입받을 애들 찾아서 주입?
- 주입 되있는걸 기반으로 context





- k8s 컴포넌트들과 컴포넌트 간의 인터페이스
  - 컨테이너가 컨테이너간 인터페이스 할때 어떤 기술을 썼는지
  - 기본적으로 생성된 애들
  - 자체도 그렇고, 하버, 랜처 어떻게 하는지?

