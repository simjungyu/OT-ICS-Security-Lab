## OT/ICS Security Lab

OT/ICS 보안 구축 실습 기록

OT Security | Network Segmentation | Modbus | IDS

---

## Lab 06 - PLC 로직 변조 탐지

### 실습 내용

Lab05에서 막은 포트와 별개로, PLC 안에 있는 로직 자체가 바뀌면 어떻게 알아채는지 실습을 진행했다.

- SCADA: ScadaBR(Docker)
- PLC: OpenPLC
- 프로그램: VirtualFactory
- 파일: 974784.st
- Modbus Port: 502
- interface: lo (192.168.31.177)

### 원본 로직

<img width="834" height="546" alt="image" src="https://github.com/user-attachments/assets/06389227-b48f-4cb9-a774-30d2597ec4b6" />


OpenPLC에서 만든 VirtualFactory 프로그램이다.
파일명은 VirtualFactory.st가 아니라, OpenPLC가 저장할 때 바꾼 974784.st였다.

```pascal
PROGRAM VirtualFactory
VAR
  Motor AT %QX0.0 : BOOL := FALSE;
  Estop AT %QX0.1 : BOOL := FALSE;
  Temp AT %QW0 : INT := 25;
  Counter : INT := 0;
END_VAR

Counter := Counter + 1;
IF Counter > 100 THEN
  Counter := 0;
END_IF;

Temp := 25 + Counter / 2;

IF Estop THEN
  Motor := FALSE;
ELSE
  Motor := TRUE;
END_IF;
END_PROGRAM
```
- Temp는 25 + Counter / 2로 25 ~ 75까지 변동한다.
- E-STOP이 켜지면 Motor가 꺼지고 E-STOP이 꺼지면 Motor는 켜진다.

<img width="616" height="452" alt="image" src="https://github.com/user-attachments/assets/9a6a1102-f27e-4f00-b1bb-694579c45d63" />


### 백업
로직이 바뀌었는지 검증하기 위해 원본파일을 백업해야 한다.
원본파일을 백업하고 해시값을 추가했다.

```
cp ~/OpenPLC_v3/webserver/st_files/974784.st ~/OT-ICS-Security-Lab/Lab06/backup/974784.st
sha256sum ~/OT-ICS-Security-Lab/Lab06/backup/974784.st > ~/OT-ICS-Security-Lab/Lab06/backup/974784.sha256
```

<img width="559" height="35" alt="image" src="https://github.com/user-attachments/assets/217a26b2-d946-4a75-aaa6-7d6f5726e480" />

### 로직 변조
실제 공격을 받을 수 없기 때문에 공격자가 로직을 공격해 값을 바꿨다고 가정했다.

### 공격 전
```pascal
IF Estop THEN
  Motor := FALSE;
```

### 공격 후
```pascal
IF Estop THEN
  Motor := TRUE;
```

<img width="588" height="455" alt="image" src="https://github.com/user-attachments/assets/d921a46a-2468-47ee-9526-bdf9a74ab56c" />

이렇게 변경되면 E-STOP으로 Motor가 꺼지지 않는 위험한 상황이 발생하게 된다.

### 변조 탐지
처음에는 `sha256sum -c` 명령어로 했는데 OK만 나왔다.
백업 파일 자체를 검사해서 OK가 뜨는 거였다.

변조 탐지를 하려면 해시와 해시를 비교해야 한다.

```
echo "This File:"; sha256sum ~/OpenPLC_v3/webserver/st_files/974784.st
echo "Backup File:"; cat ~/OT-ICS-Security-Lab/Lab06/backup/974784.sha256
```

<img width="997" height="82" alt="image" src="https://github.com/user-attachments/assets/76faf720-0482-4a2f-a4f7-d19bc7ab422e" />
2개의 파일 해시값이 다르다. 

### 복구
변조를 탐지했으면 우선 백업해둔 원본 파일로 돌려놓아야 한다.

```
cp ~/OT-ICS-Security-Lab/Lab06/backup/974784.st ~/OpenPLC_v3/webserver/st_files/974784.st
```
해시를 비교했을 때 2개가 똑같이 나오면 복구된 것이다.

<img width="990" height="82" alt="image" src="https://github.com/user-attachments/assets/2db36ac0-f5fc-4955-8565-091c3d5e43d0" />

### 트러블슈팅
| 문제 | 원인 | 해결 |
| --- | --- | --- |
| .st 파일이 없음 | OpenPLC v3는 installed.db에 저장하고 실제 로직 파일은 974784.st로 저장됨 | find ~/OpenPLC_v3 -name "974784.st" |

### 배운점
로직 변조는 Modbus 패킷으로 찾을 수 없다.
그래서 백업 + 해시값을 비교해서 탐지할 수 있다.

---
## Github

https://github.com/simjungyu/OT-ICS-Security-Lab
