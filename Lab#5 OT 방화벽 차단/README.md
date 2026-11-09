# OT/ICS Security Lab

OT/ICS 보안 구축 실습 기록

OT Security | Network Segmentation | Modbus | IDS

---
## Lab 05 - OT 방화벽 차단

### 실습 내용

Lab04에서 뚫린 포트를 ufw로 막아보는 실습을 진행했다.
-SCADA: ScadaBR(Docker)
- Modbus Port: 502
- interface: lo (192.168.31.177)
- attacker ip: 192.168.31.200
### ufw

<img width="505" height="152" alt="캡처" src="https://github.com/user-attachments/assets/48afc53d-d208-4256-a9b0-15ce4ff1fec7" />

- localhost 에서 컴퓨터는 allow(허용)
- 172.17.0.0/16 에서 Docker의 ScadaBR allow(허용)
- enp0s3(192.168.31.200) 에서 들어오는 502포트 Deny(차단)

### 공격 실행

`attack2.py`의 코드를 수정해서 시작IP와 Temp를 10으로 변경했다.

<img width="667" height="214" alt="image" src="https://github.com/user-attachments/assets/69585cb4-3160-4c5d-816f-27a67f3d25e6" />

### 공격 실행

<img width="977" height="192" alt="image" src="https://github.com/user-attachments/assets/ee717d93-8ffd-4aca-bb5a-ce8550154df1" />

enp0s3를 차단했기 때문에 외부 ip는 차단 되는 것을 확인할 수 있다.

### 트러블슈팅
| 문제 | 원인 | 해결 |
| --- | --- | --- |
| 서브넷마스크 /26으로 잘못 입력 | /26은 172.17.0.0~63까지만 허용 | /16으로 수정 |

### 배운점
방화벽으로 포트를 막을 때 정상 통신까지 막으면 안 된다.
ScadaBR과 같은 정상 서비스는 허용하고 외부 공격만 차단해야 한다.

---
## Github

https://github.com/simjungyu/OT-ICS-Security-Lab
