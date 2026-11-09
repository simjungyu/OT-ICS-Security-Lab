# OT/ICS Security Lab

OT/ICS 보안 구축 실습 기록

OT Security | Network Segmentation | Modbus | IDS

---

## Lab 04 - Modbus 공격 실습

### 실습 내용

이번에는 OpenPLC 프로그램에 Python으로 제작한 공격 파일로 값을 변조하는 공격을 진행해봤다.

Suricata를 사용해 OpenPLC에서 IDS(침입탐지시스템)를 재현해보았다.
- SCADA: ScadaBR (Docker)
- Modbus Port: 502
- interface: lo (192.168.31.177)

공격자 파일은 `attack2.py` 로 만들었다. pymodbus로 OpenPLC에 접속하여 값을 읽고 변경하는 공격 파일이다.

### Wireshark + pymodbus
Wireshark로 컴퓨터 내부에서 도는 패킷을 잡아내려면 `enp0s3이 아니라` `lo(localhost)` 루프백 주소로 잡아야 한다.
- interface: `lo`
- filter: `tcp.port==502`

### 공격 실행
`attack2.py`와 `attack_motor.py`를 실행하여 공격을 진행했다.

attack2.py

<img width="408" height="65" alt="캡처2" src="https://github.com/user-attachments/assets/241308f5-d8eb-4b5f-91d2-65aa7ab987dc" />

attack_motor.py

<img width="401" height="35" alt="image" src="https://github.com/user-attachments/assets/64c9ba97-9590-4be3-b1ba-6608256674c1" />

### 공격 전

<img width="1207" height="507" alt="캡처" src="https://github.com/user-attachments/assets/9ededfc0-7038-4d4b-8989-41546e8017d1" />

- Temp:0.0
- Motor:0
- E-STOP:0

### 공격 후

<img width="1209" height="506" alt="캡1처" src="https://github.com/user-attachments/assets/498c4d4a-daa3-4870-b978-140539b99dce" />

- Temp:9999.0
- Motor:1
- E-STOP:1

Temp와 Motor를 바꿨는데 E-STOP까지 켜졌다. PLC 로직이 온도가 너무 높다고 판단해서 비상정지 버튼을 누른 것이다.

### 패킷 분석

<img width="1203" height="320" alt="캡처la" src="https://github.com/user-attachments/assets/5f544d22-5954-4a2b-a692-b1dd2c8db1b5" />

비밀번호를 입력하지 않고 `connect()` 만으로 값이 수정된다. 
`Write Single Register (6)` 패킷도 같이 잡혔다. Temp를 9999로 쓴 패킷이다.


### 트러블슈팅

| 문제 | 원인 | 해결 |
| --- | --- | --- |
| docker permission denied | sudo를 안 붙임  | sudo docker ps로 실행 |
|write_register로 Motor 안 바뀜|Motor는 Coil이라서|write_coil(address=0, value=True)로 변경|

### 배운점

Modbus는 암호화도, 인증도 없어서, 망 분리 없으면 바로 뚫린다.

---

## Github
https://github.com/simjungyu/OT-ICS-Security-Lab



