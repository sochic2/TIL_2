```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-python-app   # Deployment이름
spec:
  replicas: 2  #replica 수
  selector:
    matchLabels:
      app: my-python-app   #Pod 찾는라벨 
  template:
    metadata:
      labels:
        app: my-python-app
    spec:
      containers:
        - name: my-python-app    #container이름
          image: your-dockerhub-username/my-python-app:v1  #사용할 컨테이너 이미지
          ports:
            - containerPort: 5000
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-python-app-service
spec:
  selector:
    app: my-python-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: ClusterIP  # 내부에서만 접근 가능
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-python-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.local  # 사용할 도메인
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-python-app-service
                port:
                  number: 80
```

- Step별로 ㄱ?
  - namespace정하기 > Deployment 값 정의 > servie 값 정의 > ingress 값 정의
  - 이때 각 단계마다 실행해서 완료 되면 넘어가기?
    - DB에 값 저장해서 중간단계에서 멈춰도 다음에도 조회 되게 구현하기?
    - running, succeed 이런 식으로 상태 보여주기?
    - Log 보여주기?



## yaml파일 생성방법

- Jinja 문법 활용방법 : https://littlemobs.com/blog/kubernetes-deployment-with-python/ 





## Python-kubernetes

```python
# example
# 환경변수에 추가 후
from kubernetes import client, config
from kubernetes.stream import stream
config.load_kube_config()  
v1 = client.CoreV1Api()
a = v1.read_namespaced_pod_log(
    name = 'harbor-core-768955cc44-pkkc9',
    namespace = 'harbor',
    follow=True,
    _preload_content=False    
)
```





# 프로젝트 시작

- 가상환경 생성
- `pip install "fastapi[all]"` 로 fastapi 설치
- pip install docker

- pip install kubernetes



### Docker(/docker)

- DockerClient 설정

  - rbp4번 서버의 docker api를 활용하여 Client로 사용

  - /etc/docker/daemon.json에 이것 추가

    ```json
    {
      "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"],
      "insecure-registries": ["harbor.rbpk3s.com"]
    }
    ```

  - systemctl restart docker

   - 위 설정만으로는 기존의 `-H fd://`와 충돌나서 `/etc/systemd/system/docker.service.d/override.conf`에 다음과 같이 추가해서 해결

     ```bash
     [Service]
     ExecStart=
     ExecStart=/usr/bin/dockerd
     ```

   - 위 설정만으로 반영이 안되어서 `sudo systemctl daemon-reload`명령어 수행 후 적용하여 해결



- Python에서는 Docker sdk사용하여 기능 구현

  - image 존재하는지(이름) (/image/exist) 

  - image build (/image/build) 

  - image push (/image/push) 

  	- 각자 올리려는 서비스가 다를 수 있으니까 Dockerfile을 작성해서 이미지 build, harbor에 push하도록 세팅

  	- docker의 경우 build, push의 return 메시지가 존재하여 그대로 log return





- Python Kubernetes sdk 사용하여 기능 구현

  - apply_yaml -> utils.create_from_dict로 yaml파일 내용이 담긴 dictionary를 input으로 받아 실행
  - config.load_kube_config() 부분은 /root/.kube/config 에 호스트로 치면 k3s.yaml같은 내용이 있거나, 환경변수에 $KUBECONFIG로 설정파일의 경로가 잡혀있을 경우 공란으로 둬도 kubernetes 접속 및 이용 가능하게 해줌 

- yaml파일 관리(deployment_teamplate.j2)

  ```jinja2
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: {{ deployment_name }}
    namespace: {{ namespace }}
  spec:
    replicas: {{ replicas }}
    selector:
      matchLabels:
        app: {{ app_name }}
    template:
      metadata:
        labels:
          app: {{ app_name }}
      spec:
        containers:
        - name: {{ container_name }}
          image: {{ image }}
          ports:
          - containerPort: {{ port }}
  
          {% if cpu_request or memory_request %}
          resources:
            requests:
              {% if cpu_request %}
              cpu: {{ cpu_request }}
              {% endif %}
              {% if memory_request %}
              memory: {{ memory_request }}
              {% endif %}
          {% endif %}
  ```

  - 위와 같은 형태로 yaml파일을 작성하여  jinja2의 Template으로 활용하여, request받은 값을 각 위치에 입력하여 사용

- deployment, service, ingress  순으로 생성한다고 가정하고, yaml에 필요한 value를 받아서 생성하는 방식으로 설계

- deployment의 spec.selector.matchLabels.app의 값을 service의 spec.selctor.app에 명시해서 연결되고, service의 metadata.name을 ingress의 spec.rules.http.paths.backend.service.name에 명시하여 deployment-service, service-ingress가 연결



- 각 deployment, service, ingress, namespace 삭제 기능 구현 예정





- apidocs에서 description, 입력 포맷 등에대한 제한이나 그런 것들이 추가적으로 필요
- response되는 값들에 대한 정의 논의 필요



- kubectl get (deployment, service, ingress), kubectl describe(deployment, service, ingress)  이런 애들 추가해서 보여주기?
- 각 요소들이 정상적으로 작동중인 상태인지 보여주기? 





