# OT/ICS Security Lab

OT/ICS 보안 구축 실습 기록

OT Security | Network Segmentation | Modbus | IDS

---

## Lab 02 - Modbus 프로토콜 분석

### 가상 공장 구성

<img width="1211" height="508" alt="image" src="https://github.com/user-attachments/assets/053384ec-fed1-4532-811b-14fbd618fc43" />

OpenPLC에 `VirtualFactory.st`프로그램을 제작했다. 모터, 비상정지, 온도 센서를 제작했다.
- Motor: %QX0.0
- E-STOP: %QX0.1
- Temp: %QW0

ScadaBR에서는 Modbus IP 데이터 파일을 만들었다. 

ScadaBR이 Docker 안에 있어서 Docker의 게이트웨이로 접속해야 하기 때문에 localhost가아닌 172.17.0.1로 했다.

### Wireshark

캡처 인터페이스는 docker0로 잡았다. 필터는 ScadaBR의 포트번호로 잡았다.
```
tcp.port == 502
```
<img width="1273" height="772" alt="image" src="https://github.com/user-attachments/assets/b1abe037-30fa-4d99-ad43-f04d90336ed3" />
- ScadaBR: 172.17.0.2
- OpenPLC: 172.17.0.1
사용된 파일은 normal.pcapng로 올려놓았다.

### 패킷 분석
616번 패킷을 열어봤다. ScadaBR이 OpenPLC에게 온도 값을 물어보는 요청이다.
```
Query Trans 2; Unit: 1; Func: 3: Read Holding Registers
Respone Trans: 2; Unit: 1; Func: 3: Read Holding Registers
```
Modbus 를 펼치면 이렇게 나온다.
<img width="1204" height="239" alt="image" src="https://github.com/user-attachments/assets/99d6b736-628f-4c58-951e-33e7187c62ee" />

| 필드 | 값 | 의미 |
| --- | --- | --- |
| Transaction ID | 2 | 요청이랑 응답 짝 맞추는 번호 |
| Protocol ID | 0 | Modbus라는 표시, 무조건 0 |
| Length | 6 | 뒤에 따라오는 데이터 길이 |
| Unit ID | 1 | PLC 1번 |
| Function Code | 3 | Read Holding Registers, 읽어줘 |
| Reference Number | 0 | 0번 주소부터 |
| Word Count | 1 | 1개만 읽어줘 |

요악하면 **1번 PLC에게 Holding Register 0번부터 1개 읽어줘** 라는 의미가 된다. 이게 온도값을 읽는 요청이다.

### 트러블슈팅

| 문제 | 원인 | 해결 |
| --- | --- | --- |
| ScadaBR 데이터 포인트 (n/a) | 데이터 포인트가 비활성화 상태 | 포인트 클릭해서 초록색 활성화 상태로 변경 |
|E-STOP에 노란 경고|OpenPLC는 1번부터 시작하는데 주소가 어긋남|Coil 2로 변경|

### 배운 점

위 상태로 사용시 별도의 인증절차 없이 Transaction ID, Unit ID, Funcion Code 등이 평문으로 노출됩니다.
가장 큰 문제는 누가 보냈는지 확인하지 않아 보안에 매우 취약합니다.

다음 실습에서는 Suricata로 허가되지 않은 Modbus 의 쓰기 명령을 잡아내볼 예정입니다.

---

## Github

https://github.com/simjungyu/OT-ICS-Security-Lab
