## 1일

### 라즈베리파일 설치

![image-20250109101947507](assets\image-20250109101947507.png)

![image-20250109112009060](assets\image-20250109112009060.png)

![image-20250109112051023](assets\image-20250109112051023.png)![image-20250109112121310](assets\image-20250109112121310.png)



### k3s 설치

- k3s 

  - 경량화 된 버전으로 제한된 작원에 더 적합.

  - 소규모 클러스터에서 빠르게 시작 가능

- Ansible

  - 오픈소스 자동화 도구로 YAML로 작성된 플레이북 기반으로 작동, 에이전트 필요 없이 간편하게 설정 및 실행 가능

  - 간단한 설정과 SSH 기반으로 inventory.ini에 활용될 서버들을 정의하고, YAML파일에 task를 정의하여 실행

  

- Ansible 활용하여 k3s 설치 및 클러스터 구성

  - RSA 키 생성 및 배포

    ```bash
    ssh-keygen -t rsa -b 4096
    ssh-copy-id -i ~/.ssh/id_rsa.pub user@<server_ip> 
    ```

  - inventory.ini 작성

    ```ini
    [master]
    192.168.0.230 ansible_user=nkc ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_become_password=pwd
    
    [worker]
    192.168.0.231 ansible_user=nkc ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_become_password=pwd
    192.168.0.232 ansible_user=nkc ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_become_password=pwd
    192.168.0.233 ansible_user=nkc ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_become_password=pwd
    192.168.0.234 ansible_user=nkc ansible_ssh_private_key_file=~/.ssh/id_rsa ansible_become_password=pwd
    
    ```

    - user에게 sudo 명령어 실행시 pwd 없이 할 수 있게 하려 했지만 여러 문제로 인해 위와 같이 작성,
    - 후에 ansible_become_password 모두 제외하고 명령어에서 --ask-become-pass 추가로 진행

  - install_k3s.yml

    - ansible-playbook 에서 실행할 yml 파일
    - 실행 방법 `ansible-playbook -i inventory.ini install_k3s.yml --ask-become-pass`
    - 실행 중간에 sudo 비밀번호를 못찾는 에러 발생하여 위와 같이 작성하고 실행 Become password는 1회만 요청하여 크게 무관할 듯
    - 모든 node에 ubuntu에 필요한 기본적인 util tool, docker 설치.

    ```yaml
    # ubuntu에서 필요할 유틸리티 도구 설치
    - name: Install utils on all nodes
      hosts: all
      become: true
      tasks:
        - name: Update apt cache and install dependencies
          apt:
            update_cache: yes
            name:
              - net-tools
              - curl
              - nano
              - vim
              - util-linux
              - zip
              - unzip
              - tar
              - socat
              - conntrack
              - ipset
              - apt-transport-https
              - ca-certificates
              - software-properties-common
            state: present
    
    # 도커 설치
    - name: Install Docker on all nodes
      hosts: all
      become: true
      tasks:
        - name: Update apt cache
          apt:
            update_cache: yes
    
        - name: Install Docker
          apt:
            name: docker.io
            state: present
    
        - name: Enable and start Docker service
          service:
            name: docker
            state: started
            enabled: true
    
        - name: Add user to Docker group
          user:
            name: nkc
            groups: docker
            append: true
    
    
    ```
    
    - Master, Worker에 k3s 설치(docker 기반으로)
    
    ```yaml
    - name: Configure K3s Master
      hosts: master
      become: true
      tasks:
        - name: Install K3s on master node
          shell: |
            curl -sfL https://get.k3s.io | sh -s - --docker --write-kubeconfig-mode 644
          args:
            executable: /bin/bash
    
        - name: Get K3s token from master
          shell: cat /var/lib/rancher/k3s/server/node-token
          register: k3s_token_raw
          delegate_to: 192.168.0.230
    
        - name: Set global fact
          set_fact:
            k3s_token: "{{k3s_token_raw.stdout}}"
    
    - name: Configure K3s Worker Nodes
      hosts: worker
      become: true
      tasks:
        - name: Install K3s on worker node
          shell: |
            curl -sfL https://get.k3s.io | K3S_URL=https://192.168.0.230:6443 K3S_TOKEN="{{hostvars['192.168.0.230']['k3s_token']}}" sh -s - --docker
          args:
            executable: /bin/bash
    
    - name: edit Kubeconfig
      hosts: master
      become: true
      tasks:
        - name: Copy kubeconfig file
          copy:
            remote_src: yes
            src: /etc/rancher/k3s/k3s.yaml
            dest: /home/nkc/k3s-updated.yaml
    
    
        - name: Replace localhost to master IP
          lineinfile:
            path: /home/nkc/k3s-updated.yaml
            regexp: 'server: https://127.0.0.1:6443'
            line: '    server: https://192.168.0.230:6443'
            backrefs: yes
    
    - name: mvKubeconfig
      hosts: worker
      become: true
      tasks:
        - name: Copy kubeconfig to worker nodes
          copy:
            src: /home/nkc/k3s-updated.yaml
            dest: /home/nkc/k3s.yaml
    
        - name: kubeconfig to bashrc
          lineinfile:
            path: /home/nkc/.bashrc
            line: 'export KUBECONFIG=/home/nkc/k3s.yaml'
            state: present
        - name: apply bashrc
          shell: source /home/nkc/.bashrc
          args:
            executable: /bin/bash
    
    
    ```
    
  - debugging 방법
  
    ```yml
    - name: Debug test
      hosts: master
      become: true
      tasks:
        - name: get k3s token
          shell: cat /var/lib/rancher/k3s/server/node-token
          register: k3s_token_raw
          delegate_to: 192.168.0.230
    
        - name: set var on master
          set_fact:
            k3s_token: "{{k3s_token_raw.stdout}}"
    
    - name: worker call test
      hosts: worker
      become: true
      tasks:
        - name: call test
          debug:
            msg: "{{hostvars['192.168.0.230']['k3s_token']}}"
    ```
  
    - debugging용 yml 파일 생성 후 `ansible-playbook -i inventory.ini debug.yml --ask-become-pass`로 실행
    - 위의 방식으로 master에서 선언한 k3s_token을 worker에서 조회 가능한지 확인
  
- k3s 삭제 방법

```bash
sudo /usr/local/bin/k3s-uninstall.sh
```



- k3s 정상 작동 확인

```bash
$ kubectl get nodes
NAME   STATUS   ROLES                  AGE     VERSION
rbp1   Ready    control-plane,master   2d17h   v1.31.4+k3s1
rbp2   Ready    <none>                 2d16h   v1.31.4+k3s1
rbp3   Ready    <none>                 2d16h   v1.31.4+k3s1
rbp4   Ready    <none>                 2d16h   v1.31.4+k3s1
rbp5   Ready    <none>                 2d16h   v1.31.4+k3s1

```

	- worker는 기본적으로 <none>으로 표기. `kubectl label node <노드명> node-role.kubernetes.io/worker=""` 명령어로 label 변경 가능

- 에러 발생시 로그 확인

```bash
systemctl status k3s
sudo journalctl -u k3s

```





### 파드 실행 테스트

- 각 Node별 IP:PORT로접속 ex)192.168.0.230:31062,  접속 가능 확인

```bash
$ kubectl run test-nginx --image nginx --port=80
$ kubectl get pod -o wide
NAME         READY   STATUS              RESTARTS   AGE   IP       NODE   NOMINATED NODE   READINESS GATES
test-nginx   0/1     ContainerCreating   0          14s   <none>   rbp3   <none>           <none>

$ kubectl expose pod test-nginx --type=NodePort
$ kubectl get service
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP        2d18h
test-nginx   NodePort    10.43.101.146   <none>        80:31062/TCP   3m30s 

#Pod, Service 삭제
$ kubectl delete pod test-nginx
pod "test-nginx" deleted
$ kubectl get pod
No resources found in default namespace.

$ kubectl delete svc test-nginx
service "test-nginx" deleted
$ kubectl get service
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.43.0.1    <none>        443/TCP   2d18h
```



- kubectl get pod -o wide -n default, kubectl get service에서 출력되는 IP

  ```bash
  $ kubectl get pod -o wide
  NAME         READY   STATUS    RESTARTS   AGE     IP          NODE   NOMINATED NODE   READINESS GATES
  test-nginx   1/1     Running   0          7m17s   10.42.4.4   rbp3   <none>           <none>
  ```

  - Pod IP로, 클러스터 내부 네트워크를 통해 다른 Pod와 통신하는데 사용
  - 클러스터 내에서 고유한 IP 할당
  - 외부 네트워크에서 직접접근 불가, Pod 재배포, 삭제, 재생성 시 IP 변경 가능  

  ```bash
  $ kubectl get service
  NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
  kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP        2d18h
  test-nginx   NodePort    10.43.101.146   <none>        80:31062/TCP   3m30s
  ```

  - Service IP, Service에 대한 고정 IP, 클러스터 내부에서만 유효
  - NodePort, LoadBalancer를 활용하여 외부에서 접근 가능하도록 포트포워딩 가능 



- 파드 실행중인 노드 장애 테스트

  - nginx_deployment.yaml

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: test-nginx
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: test-nginx
    template:
      metadata:
        labels:
          app: test-nginx
      spec:
        containers:
        - name: nginx
          image: nginx
          ports:
          - containerPort: 80
  
  ```

  ```bash
  $ kubectl apply -f nginx_deployment.yaml
  
  $ kubectl get nodes
  NAME   STATUS     ROLES                  AGE     VERSION
  rbp1   Ready      control-plane,master   2d20h   v1.31.4+k3s1
  rbp2   Ready      <none>                 2d20h   v1.31.4+k3s1
  rbp3   NotReady   <none>                 2d20h   v1.31.4+k3s1
  rbp4   Ready      <none>                 2d20h   v1.31.4+k3s1
  rbp5   Ready      <none>                 2d20h   v1.31.4+k3s1
  
  $ kubectl get pods -o wide
  NAME                         READY   STATUS        RESTARTS   AGE   IP          NODE   NOMINATED NODE   READINESS GATES
  test-nginx-5f877b66c-t2prm   1/1     Running       0          12m   10.42.1.4   rbp2   <none>           <none>
  test-nginx-5f877b66c-w5kg6   1/1     Terminating   0          19m   10.42.4.6   rbp3   <none>           <none>
  ```

  - rbp3에서 실행중인 것 확인 후 네트워크 단절, Not Ready 상태는 1분정도 후에 반영되었지만, Pod 재시작은 시간이 꽤 지난 후에 이뤄짐.

  ```bash
  spec:
    tolerations:
    - key: "node.kubernetes.io/not-ready"
      operator: "Exists"
      effect: "NoExecute"
      tolerationSeconds: 30
    - key: "node.kubernetes.io/unreachable"
      operator: "Exists"
      effect: "NoExecute"
      tolerationSeconds: 30
  ```



### Ingress와 Metallb 사용 필요성

- Ingress를 사용 이유
  -  서비스 포트까지 공개하지 않고 dns에 ip domain을 적고, domain으로 접속 가능
  - 여러 서비스에 대한 외부요청 단일 진입점 제공으로 관리 용이
  - HTTPS/SSL 설정 관리(미사용시 각 서비스마다 관리 필요)
  -  LoadBalancer 사용 최소화로 비용 절감(미사용시 서비스마다 필요)
- Ingress만으로 안되는 이유
  - Ingress Controller는 클러스터 내에서 적절한 서비스로 라우팅하는 역할만 담당
  - 외부의 요청을 처리하려면 LoadBalancer 또는 NodePort 타입의 서비스 필요

- LoadBalancer type(Metallb) 사용 필요성

  - k3s 환경에서 서비스 실행시 어떤 노드에서 실행될지 알 수 없음.
    - 고정시킨다면 k3s의 유연성, 자원 가용성의 장점이 퇴색

  - VIP를 제공해 고정 ip로 사용 가능
  - cf) NodePort의 경우 각 노드별로 외부와 연결

- 요청 처리 방식

  - Metallb가 Ingress Controller에 VIP 할당,  클라이언트에서 vip로 요청 -> 클러스터 내부로 전달
  - Ingress Controller가여러 서비스에 대해 라우팅 처리 

  

### Metallb 설치

```bash
$ kubectl create namespace metallb-system
$ helm repo add metallb https://metallb.github.io/metallb
$ helm repo update
$ helm install metallb metallb/metallb --namespace metallb-system
```

- metallb_config.yaml

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-ip-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.1.250-192.168.1.250 #vip로 사용할 ip
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
```

```bash
$ kubectl apply -f metallb_config.yaml
```





### Ingress 컨트롤러 설치

- NGINX Ingress Controller 설치 및 실행

  ```bash
  $ helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  $ helm repo update
  $ helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx --create-namespace
  ```

  - Helm 차트에 정의된 기본 설정으로 실행됨.
  - ` --set controller.service.type=LoadBalancer`를 빼먹고 설치해서 후에` kubectl patch svc ingress-nginx-controller -n ingress-nginx \  -p '{"spec": {"type": "LoadBalancer"}}'`로 변경

- rancher_ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rancher-ingress
  namespace: cattle-system   # ingress는 같은 네임스페이스 내에서 서비스 참조 가능
  annotations:               
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx   # 이거 누락했더니 traefik이 Ingress Class로잡혀서 설정 꼬임
  tls:
  - hosts:
    - rancher.rbpk3s.com
    secretName: wildcard-cert   # 처음에 ingress-nginx에 두고, 이름만 썼더니 apply시에는 에러 
  rules:                        # 안나는데 ingress-controller 로그 봤더니 못찾는다고 에러찍힘
  - host: rancher.rbpk3s.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: rancher
            port:
              number: 80
```

- `kubectl describe ingress rancher-ingress -n cattle-system` 세부 내용 확인

### Rancher 설치

- `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash` 명령어로 helm 설치(kubernetes 패키지 관리자)

- `kubectl create namespace cattle-system` Rancher 네임스페이스 생성
  - 다른 애플리케이션, 시스템 리소스와 충돌하지 않도록 하고, 권장되는 표준 구성

- `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.3/cert-manager.yaml` 
  - 랜처는 HTTPS를 기본적으로 사용하여 인증서 설정, cert-manager 설치

- `kubectl get pods --namespace cert-manager`

  - cert-manager 준비 확인

- Rancher 설치

  - helmn chart 추가
    - `helm repo add rancher-stable https://releases.rancher.com/server-charts/stable`
    - `helm repo update`
  - Helm Chart를 사용해 Rancher 설치

  ```bash
  $ helm install rancher rancher-latest/rancher \
    --namespace cattle-system \
    --set hostname=rancher.rbpk3s.com \
    --set replicas=2
  ```

  ```bash
  $ kubectl get service -n cattle-system
  NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
  rancher           ClusterIP   10.43.155.25    <none>        80/TCP,443/TCP   3h33m
  rancher-webhook   ClusterIP   10.43.179.140   <none>        443/TCP          3h25m
  ```

  - EXTERNAL-IP가 None이지만, rancher-ingress가 nginx-ingress-controller와 연결, 이와 연결된 metallb를 통해 외부와 통신

    ```bash
    $ kubectl describe ingress rancher-ingress -n cattle-system
    Name:             rancher-ingress
    Labels:           <none>
    Namespace:        cattle-system
    Address:          192.168.0.250
    Ingress Class:    nginx
    Default backend:  <default>
    TLS:
      wildcard-cert terminates rancher.rbpk3s.com
    Rules:
      Host                Path  Backends
      ----                ----  --------
      rancher.rbpk3s.com
                          /   rancher:80 (10.42.1.12:80,10.42.4.19:80)
    Annotations:          field.cattle.io/publicEndpoints:
                            [{"addresses":["192.168.0.250"],"port":443,"protocol":"HTTPS","serviceName":"cattle-system:rancher","ingressName":"cattle-system:rancher-i...
                          nginx.ingress.kubernetes.io/rewrite-target: /
    Events:
      Type    Reason  Age                From                      Message
      ----    ------  ----               ----                      -------
      Normal  Sync    28m (x3 over 29m)  nginx-ingress-controller  Scheduled for sync
    
    ```

- hosts파일에 hostname으로 정의한 주소 입력 시 rancher 접속 확인 가능





### SSL 자체인증서 사용

- 인증서 생성 및 ingress-nginx, cattle-system에 secret 등록

```bash
$ openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout wildcard.key -out wildcard.crt \
  -subj "/C=KO/ST=daejeon/L=city/O=Internet Widgits Pty Ltd/CN=*.rbpk3s.com" \
  -addext "subjectAltName=DNS:*.rbpk3s.com"

kubectl create secret tls wildcard-cert   --cert=/home/nkc/practice/priv_cert/wildcard.crt   --key=/home/nkc/practice/priv_cert/wildcard.key   -n ingress-nginx

kubectl create secret tls wildcard-cert   --cert=/home/nkc/practice/priv_cert/wildcard.crt   --key=/home/nkc/practice/priv_cert/wildcard.key   -n cattle-system
```

- secret도 같은 namespace에서만 참조 가능하여 작업할때 같이 시켜줌
- 이후에는 rancher에서 ingress-nginx 값으로 create 하여 내용 복붙해서 사용 가능
- 그렇지만 공인인증받은게 아니라서 주의요함이 안없어지는듯...?



- rancher_ingress.yaml에 spec부분에 하단 내용 추가.

```yaml
  tls:
  - hosts:
    - rancher.example.com
    secretName: wildcard-cert  # Secret 이름
```

- `kubectl get secret wildcard-cert -n cattle-system -o jsonpath="{.data.tls\.crt}" | base64 -d | openssl x509 -noout -text` 인증서 설정 확인



#### nginx-ingress-controller 로그 확인법

- `kubectl get pods -n ingress-nginx`로 파드명 찾고, 

- `kubectl logs ingress-nginx-controller-7657f6db5f-klbn2 -n ingress-nginx`





### Harbor 설치

- 이슈사항
  - 라즈베리파이가 arm64라서 cpu 아키텍처에 맞는 harbor 설치
  - 서비스 재시작시 데이터 삭제되면 안되서 pv, pvc 사전 정의 후 서비스 시작
    - nfs 설치 후 pvc 설정

- rbp5번 서버에 nfs 설치 후 pv, pvc 설정

```yaml
# storageclass-nfs.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-storage
provisioner: nfs.csi.k8s.io
parameters:
  server: 192.168.0.234  # NFS 서버의 IP 주소
  share: /mnt/nfs-share    # NFS 서버의 공유 디렉터리 경로
mountOptions:
  - hard
  - nfsvers=4.1
reclaimPolicy: Retain  # PVC 삭제 시 데이터 유지
volumeBindingMode: Immediate
```

- nfs를 사용하는 storaeclass 먼저 생성

```yaml
# harbor_pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-harbor-registry
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: 192.168.0.234
    path: /mnt/nfs-share/harbor-registry
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-harbor-jobservice
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: 192.168.0.234
    path: /mnt/nfs-share/harbor-jobservice

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-harbor-database
spec:
  capacity:
    storage: 8Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: 192.168.0.234
    path: /mnt/nfs-share/harbor-database

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-harbor-redis
spec:
  capacity:
    storage: 8Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: 192.168.0.234
    path: /mnt/nfs-share/harbor-redis

---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-harbor-trivy
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: 192.168.0.234
    path: /mnt/nfs-share/harbor-trivy

```

```yaml
# harbor_pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-harbor-registry
  namespace: harbor
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
  storageClassName: nfs-storage

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-harbor-jobservice
  namespace: harbor
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  storageClassName: nfs-storage

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-harbor-database
  namespace: harbor
spec:
  accessModes:
    - ReadWriteMany
  resources:
      requests:
        storage: 8Gi
  storageClassName: nfs-storage

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-harbor-redis
  namespace: harbor
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 8Gi
  storageClassName: nfs-storage

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-harbor-trivy
  namespace: harbor
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
  storageClassName: nfs-storage
```

- pv에 정의된 위치에 디렉토리 생성 후 pv, pvc apply



```bash
$ kubectl create namespace harbor
$ helm helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm repo update
```

```bash
$ kubectl create secret tls wildcard-cert   --cert=/home/nkc/practice/priv_cert/wildcard.crt   --key=/home/nkc/practice/priv_cert/wildcard.key   -n harbor
```

```bash
$ kubectl apply -f harbor_pv.yaml
$ kubectl apply -f harbor_pvc.yaml
```

- harbor_values.yaml 정의

```yaml
externalURL: https://harbor.rbpk3s.com
exposureType: ingress
ingress:
  core:
    ingressClassName: "nginx"
    hostname: harbor.rbpk3s.com
    tls: true  # ✅ TLS 활성화
    selfSigned: false
    extraTls:
      - hosts:
          - harbor.rbpk3s.com
        secretName: harbor.rbpk3s.com-tls  # helm에서 자동생성시 이렇게 생

harbor:
  forceMigration: true

adminPassword: "Okestro00!@#$"

persistence:
  enabled: true
  storageClass: "nfs-storage"  # ✅ 전체 Harbor에서 NFS StorageClass 사용
  persistentVolumeClaim:
    registry:
      existingClaim: pvc-harbor-registry
    jobservice:
      existingClaim: pvc-harbor-jobservice
    database:
      existingClaim: pvc-harbor-database
    redis:
      existingClaim: pvc-harbor-redis
    trivy:
      existingClaim: pvc-harbor-trivy

trivy:
  persistence:
    enabled: true
    existingClaim: pvc-harbor-trivy  # ✅ Trivy도 기존 PVC 사용

postgresql:
  enabled: true
  primary:
    persistence:
      enabled: true
      existingClaim: pvc-harbor-database  # ✅ PostgreSQL도 기존 PVC 사용

redis:
  enabled: true
  master:
    persistence:
      enabled: true
      existingClaim: pvc-harbor-redis  # ✅ Redis도 기존 PVC 사용
```

- 위의 것으로 했더니 인증서쪽 계속 꼬여서 그냥 알아서 생성해주는걸로 변경

```yaml
externalURL: https://harbor.rbpk3s.com
exposureType: ingress
ingress:
  core:
    ingressClassName: "nginx"
    hostname: harbor.rbpk3s.com

harbor:
  forceMigration: true

adminPassword: "Okestro00!@#$"

persistence:
  enabled: true
  storageClass: "nfs-storage"  # ✅ 전체 Harbor에서 NFS StorageClass 사용
  persistentVolumeClaim:
    registry:
      existingClaim: pvc-harbor-registry
    jobservice:
      existingClaim: pvc-harbor-jobservice
    database:
      existingClaim: pvc-harbor-database
    redis:
      existingClaim: pvc-harbor-redis
    trivy:
      existingClaim: pvc-harbor-trivy

trivy:
  persistence:
    enabled: true
    existingClaim: pvc-harbor-trivy  # ✅ Trivy도 기존 PVC 사용

postgresql:
  enabled: true
  primary:
    persistence:
      enabled: true
      existingClaim: pvc-harbor-database  # ✅ PostgreSQL도 기존 PVC 사용

redis:
  enabled: true
  master:
    persistence:
      enabled: true
      existingClaim: pvc-harbor-redis  # ✅ Redis도 기존 PVC 사용

```





```bash
$ helm install harbor bitnami/harbor -n harbor -f harbor_values.yaml
```

```bash
helm install harbor bitnami/harbor -n harbor -f harbor_values.yaml --debug --dry-run   # --debug --dry-run  실행될 파일들 보여줌
```

### helm install시 custom해서 사용할 values.yaml 작성 방식

- helm chart에서 디폴트 값으로 제공하는 것 이외에 커스텀해 사용할 시 values.yaml(이름이 중요하진 않음)에 일부값을 변경하여 사용 가능
- 우선,  hellm chart, 'https://artifacthub.io/packages/helm/bitnami/harbor' 이런 곳에 기본적이 값 설정 방식은 존재. 혹은 values전체를 다운받아 확인하거나 github에서도 확인 가능.
- values.yaml에 주석으로 설명이 있긴 하지만 정확한 사용 방식을 모를 때는 templates로 기 정의된 형태를 보면 더 확실하게 어떤식으로 값이 들어가는지 확인 가능
- 예를들어 ingress를 생성해줄 yaml의 template을 확인해보면  values.yaml에 값을 어떻게 넣어야 할지 유추가 더 용이할 수 있음

