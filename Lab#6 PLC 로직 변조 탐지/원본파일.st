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
