EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L 74xx:74HCT595 U1
U 1 1 5D84402B
P 3400 3950
F 0 "U1" H 3150 3250 50  0000 C CNN
F 1 "74HCT595" V 3400 3900 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 3400 3950 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT595.pdf" H 3400 3950 50  0001 C CNN
	1    3400 3950
	1    0    0    -1  
$EndComp
$Comp
L 74xx:74HCT595 U3
U 1 1 5D844F54
P 6500 3950
F 0 "U3" H 6250 3250 50  0000 C CNN
F 1 "74HCT595" V 6500 3900 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 6500 3950 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/74HC_HCT595.pdf" H 6500 3950 50  0001 C CNN
	1    6500 3950
	1    0    0    -1  
$EndComp
$Comp
L Transistor_Array:ULN2803A U2
U 1 1 5D846566
P 4650 3750
F 0 "U2" H 4650 4317 50  0000 C CNN
F 1 "ULN2803A" H 4650 4226 50  0000 C CNN
F 2 "Package_DIP:DIP-18_W7.62mm" H 4700 3100 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/uln2803a.pdf" H 4750 3550 50  0001 C CNN
	1    4650 3750
	1    0    0    -1  
$EndComp
$Comp
L Transistor_Array:ULN2803A U4
U 1 1 5D84887A
P 7850 3750
F 0 "U4" H 7850 4317 50  0000 C CNN
F 1 "ULN2803A" H 7850 4226 50  0000 C CNN
F 2 "Package_DIP:DIP-18_W7.62mm" H 7900 3100 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/uln2803a.pdf" H 7950 3550 50  0001 C CNN
	1    7850 3750
	1    0    0    -1  
$EndComp
$Comp
L Device:C C1
U 1 1 5D849FED
P 5350 5100
F 0 "C1" H 5050 5150 50  0000 L CNN
F 1 "0.1uf" H 5050 5050 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D3.4mm_W2.1mm_P2.50mm" H 5388 4950 50  0001 C CNN
F 3 "~" H 5350 5100 50  0001 C CNN
	1    5350 5100
	1    0    0    -1  
$EndComp
$Comp
L Device:C C2
U 1 1 5D84B196
P 5750 5100
F 0 "C2" H 5635 5146 50  0000 R CNN
F 1 "0.1uf" H 5635 5055 50  0000 R CNN
F 2 "Capacitor_THT:C_Disc_D3.4mm_W2.1mm_P2.50mm" H 5788 4950 50  0001 C CNN
F 3 "~" H 5750 5100 50  0001 C CNN
	1    5750 5100
	-1   0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x05_Male J1
U 1 1 5D84BBD5
P 2200 5250
F 0 "J1" H 2308 5631 50  0000 C CNN
F 1 "Conn_01x05_Male" H 2308 5540 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Horizontal" H 2200 5250 50  0001 C CNN
F 3 "~" H 2200 5250 50  0001 C CNN
	1    2200 5250
	1    0    0    1   
$EndComp
$Comp
L Connector:Conn_01x05_Female J2
U 1 1 5D84C903
P 8650 5150
F 0 "J2" H 8678 5176 50  0000 L CNN
F 1 "Conn_01x05_Female" H 8678 5085 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x05_P2.54mm_Horizontal" H 8650 5150 50  0001 C CNN
F 3 "~" H 8650 5150 50  0001 C CNN
	1    8650 5150
	1    0    0    1   
$EndComp
$Comp
L Connector:Screw_Terminal_01x16 J3
U 1 1 5D84D5F4
P 9450 2300
F 0 "J3" H 9530 2292 50  0000 L CNN
F 1 "Screw_Terminal_01x16" H 9530 2201 50  0000 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-16-5.08_1x16_P5.08mm_Horizontal" H 9450 2300 50  0001 C CNN
F 3 "~" H 9450 2300 50  0001 C CNN
	1    9450 2300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5D854A09
P 9050 4500
F 0 "#PWR0101" H 9050 4250 50  0001 C CNN
F 1 "GND" H 9055 4327 50  0000 C CNN
F 2 "" H 9050 4500 50  0001 C CNN
F 3 "" H 9050 4500 50  0001 C CNN
	1    9050 4500
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0102
U 1 1 5D8556B6
P 9300 4500
F 0 "#PWR0102" H 9300 4350 50  0001 C CNN
F 1 "VCC" H 9318 4673 50  0000 C CNN
F 2 "" H 9300 4500 50  0001 C CNN
F 3 "" H 9300 4500 50  0001 C CNN
	1    9300 4500
	-1   0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5D855DBA
P 9050 4350
F 0 "#FLG0101" H 9050 4425 50  0001 C CNN
F 1 "PWR_FLAG" H 9050 4523 50  0000 C CNN
F 2 "" H 9050 4350 50  0001 C CNN
F 3 "~" H 9050 4350 50  0001 C CNN
	1    9050 4350
	1    0    0    -1  
$EndComp
Text GLabel 5250 3550 2    50   Input ~ 0
OUT8
Text GLabel 5250 3650 2    50   Input ~ 0
OUT7
Text GLabel 5250 3750 2    50   Input ~ 0
OUT6
Text GLabel 5250 3850 2    50   Input ~ 0
OUT5
Text GLabel 5250 3950 2    50   Input ~ 0
OUT4
Text GLabel 5250 4050 2    50   Input ~ 0
OUT3
Text GLabel 5250 4150 2    50   Input ~ 0
OUT2
Text GLabel 5250 4250 2    50   Input ~ 0
OUT1
Text GLabel 8450 3550 2    50   Input ~ 0
OUT16
Text GLabel 8450 3650 2    50   Input ~ 0
OUT15
Text GLabel 8450 3750 2    50   Input ~ 0
OUT14
Text GLabel 8450 3850 2    50   Input ~ 0
OUT13
Text GLabel 8450 3950 2    50   Input ~ 0
OUT12
Text GLabel 8450 4050 2    50   Input ~ 0
OUT11
Text GLabel 8450 4150 2    50   Input ~ 0
OUT10
Text GLabel 8450 4250 2    50   Input ~ 0
OUT9
Text GLabel 9000 1600 0    50   Input ~ 0
OUT1
Text GLabel 9000 1700 0    50   Input ~ 0
OUT2
Text GLabel 9000 1800 0    50   Input ~ 0
OUT3
Text GLabel 9000 1900 0    50   Input ~ 0
OUT4
Text GLabel 9000 2000 0    50   Input ~ 0
OUT5
Text GLabel 9000 2100 0    50   Input ~ 0
OUT6
Text GLabel 9000 2200 0    50   Input ~ 0
OUT7
Text GLabel 9000 2300 0    50   Input ~ 0
OUT8
Text GLabel 9000 2400 0    50   Input ~ 0
OUT9
Text GLabel 9000 2500 0    50   Input ~ 0
OUT10
Text GLabel 9000 2600 0    50   Input ~ 0
OUT11
Text GLabel 9000 2700 0    50   Input ~ 0
OUT12
Text GLabel 9000 2800 0    50   Input ~ 0
OUT13
Text GLabel 9000 2900 0    50   Input ~ 0
OUT14
Text GLabel 9000 3000 0    50   Input ~ 0
OUT15
Text GLabel 9100 3100 0    50   Input ~ 0
OUT16
Wire Wire Line
	9000 1600 9250 1600
Wire Wire Line
	9000 1700 9250 1700
Wire Wire Line
	9000 1800 9250 1800
Wire Wire Line
	9000 1900 9250 1900
Wire Wire Line
	9000 2000 9250 2000
Wire Wire Line
	9000 2100 9250 2100
Wire Wire Line
	9000 2200 9250 2200
Wire Wire Line
	9000 2300 9250 2300
Wire Wire Line
	9000 2400 9250 2400
Wire Wire Line
	9000 2500 9250 2500
Wire Wire Line
	9000 2600 9250 2600
Wire Wire Line
	9000 2700 9250 2700
Wire Wire Line
	9000 2800 9250 2800
Wire Wire Line
	9000 2900 9250 2900
Wire Wire Line
	9000 3000 9250 3000
Wire Wire Line
	9000 3100 9250 3100
Wire Wire Line
	8250 3550 8450 3550
Wire Wire Line
	8250 3650 8450 3650
Wire Wire Line
	8250 3750 8450 3750
Wire Wire Line
	8250 3850 8450 3850
Wire Wire Line
	8250 3950 8450 3950
Wire Wire Line
	8250 4050 8450 4050
Wire Wire Line
	8250 4150 8450 4150
Wire Wire Line
	8250 4250 8450 4250
Wire Wire Line
	5050 3550 5250 3550
Wire Wire Line
	5050 3650 5250 3650
Wire Wire Line
	5050 3750 5250 3750
Wire Wire Line
	5050 3850 5250 3850
Wire Wire Line
	5050 3950 5250 3950
Wire Wire Line
	5050 4050 5250 4050
Wire Wire Line
	5050 4150 5250 4150
Wire Wire Line
	5050 4250 5250 4250
Text GLabel 8450 3450 2    50   Input ~ 0
COM
Text GLabel 5250 3450 2    50   Input ~ 0
COM
Wire Wire Line
	8250 3450 8450 3450
Wire Wire Line
	5050 3450 5250 3450
$Comp
L power:GND #PWR0103
U 1 1 5D88AEC0
P 4000 4850
F 0 "#PWR0103" H 4000 4600 50  0001 C CNN
F 1 "GND" H 4005 4677 50  0000 C CNN
F 2 "" H 4000 4850 50  0001 C CNN
F 3 "" H 4000 4850 50  0001 C CNN
	1    4000 4850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5D88BDAA
P 7100 4850
F 0 "#PWR0104" H 7100 4600 50  0001 C CNN
F 1 "GND" H 7105 4677 50  0000 C CNN
F 2 "" H 7100 4850 50  0001 C CNN
F 3 "" H 7100 4850 50  0001 C CNN
	1    7100 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 4650 6500 4750
Wire Wire Line
	6500 4750 7100 4750
Wire Wire Line
	7100 4750 7100 4850
Wire Wire Line
	7850 4450 7850 4750
Connection ~ 7100 4750
Wire Wire Line
	3400 4650 3400 4750
Wire Wire Line
	3400 4750 4000 4750
Wire Wire Line
	4000 4750 4000 4850
Wire Wire Line
	4650 4450 4650 4750
$Comp
L power:VCC #PWR0105
U 1 1 5D893CDF
P 6500 3150
F 0 "#PWR0105" H 6500 3000 50  0001 C CNN
F 1 "VCC" H 6517 3323 50  0000 C CNN
F 2 "" H 6500 3150 50  0001 C CNN
F 3 "" H 6500 3150 50  0001 C CNN
	1    6500 3150
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0106
U 1 1 5D89456C
P 3400 3150
F 0 "#PWR0106" H 3400 3000 50  0001 C CNN
F 1 "VCC" H 3417 3323 50  0000 C CNN
F 2 "" H 3400 3150 50  0001 C CNN
F 3 "" H 3400 3150 50  0001 C CNN
	1    3400 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 3350 6500 3150
Wire Wire Line
	3400 3350 3400 3150
$Comp
L power:GND #PWR0107
U 1 1 5D89A090
P 5550 5400
F 0 "#PWR0107" H 5550 5150 50  0001 C CNN
F 1 "GND" H 5555 5227 50  0000 C CNN
F 2 "" H 5550 5400 50  0001 C CNN
F 3 "" H 5550 5400 50  0001 C CNN
	1    5550 5400
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0108
U 1 1 5D89A820
P 5550 4800
F 0 "#PWR0108" H 5550 4650 50  0001 C CNN
F 1 "VCC" H 5567 4973 50  0000 C CNN
F 2 "" H 5550 4800 50  0001 C CNN
F 3 "" H 5550 4800 50  0001 C CNN
	1    5550 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5350 4950 5350 4900
Wire Wire Line
	5350 4900 5550 4900
Wire Wire Line
	5550 4900 5550 4800
Wire Wire Line
	5750 4950 5750 4900
Wire Wire Line
	5750 4900 5550 4900
Connection ~ 5550 4900
Wire Wire Line
	5350 5250 5350 5300
Wire Wire Line
	5350 5300 5550 5300
Wire Wire Line
	5550 5300 5550 5400
Wire Wire Line
	5750 5250 5750 5300
Wire Wire Line
	5750 5300 5550 5300
Connection ~ 5550 5300
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 5D8A3F3E
P 9300 4350
F 0 "#FLG0102" H 9300 4425 50  0001 C CNN
F 1 "PWR_FLAG" H 9300 4523 50  0000 C CNN
F 2 "" H 9300 4350 50  0001 C CNN
F 3 "~" H 9300 4350 50  0001 C CNN
	1    9300 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	9050 4350 9050 4500
Wire Wire Line
	9300 4350 9300 4500
Wire Wire Line
	6100 4150 6050 4150
Wire Wire Line
	6050 4150 6050 4750
Wire Wire Line
	6050 4750 6500 4750
Connection ~ 6500 4750
Wire Wire Line
	3000 4150 2950 4150
Wire Wire Line
	2950 4150 2950 4750
Wire Wire Line
	2950 4750 3400 4750
Connection ~ 3400 4750
Text GLabel 3950 4450 2    50   Input ~ 0
DN
Text GLabel 2800 3550 0    50   Input ~ 0
DI
Text GLabel 2600 5250 2    50   Input ~ 0
CLK
Text GLabel 2600 5350 2    50   Input ~ 0
LAT
Text GLabel 2600 5150 2    50   Input ~ 0
DI
Text GLabel 5950 3550 0    50   Input ~ 0
DN
Text GLabel 8250 5250 0    50   Input ~ 0
LAT
Wire Wire Line
	6900 4450 7050 4450
Wire Wire Line
	6100 3550 5950 3550
Wire Wire Line
	3950 4450 3800 4450
Wire Wire Line
	3000 3550 2800 3550
Text GLabel 8250 5150 0    50   Input ~ 0
CLK
Text GLabel 5950 3750 0    50   Input ~ 0
CLK
Text GLabel 2800 3750 0    50   Input ~ 0
CLK
Wire Wire Line
	5950 3750 6100 3750
Wire Wire Line
	2800 3750 3000 3750
Text GLabel 8250 5050 0    50   Input ~ 0
DO
Text GLabel 5950 4050 0    50   Input ~ 0
LAT
Text GLabel 2800 4050 0    50   Input ~ 0
LAT
Wire Wire Line
	6100 4050 5950 4050
Wire Wire Line
	3000 4050 2800 4050
$Comp
L power:VCC #PWR0109
U 1 1 5D8E17B2
P 2450 3700
F 0 "#PWR0109" H 2450 3550 50  0001 C CNN
F 1 "VCC" H 2467 3873 50  0000 C CNN
F 2 "" H 2450 3700 50  0001 C CNN
F 3 "" H 2450 3700 50  0001 C CNN
	1    2450 3700
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0110
U 1 1 5D8EDC85
P 5600 3700
F 0 "#PWR0110" H 5600 3550 50  0001 C CNN
F 1 "VCC" H 5617 3873 50  0000 C CNN
F 2 "" H 5600 3700 50  0001 C CNN
F 3 "" H 5600 3700 50  0001 C CNN
	1    5600 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 3850 5600 3850
Wire Wire Line
	5600 3850 5600 3700
Wire Wire Line
	3000 3850 2450 3850
Wire Wire Line
	2450 3850 2450 3700
$Comp
L power:VCC #PWR0111
U 1 1 5D8F647D
P 2700 4900
F 0 "#PWR0111" H 2700 4750 50  0001 C CNN
F 1 "VCC" H 2717 5073 50  0000 C CNN
F 2 "" H 2700 4900 50  0001 C CNN
F 3 "" H 2700 4900 50  0001 C CNN
	1    2700 4900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 5D8F80BF
P 2700 5600
F 0 "#PWR0114" H 2700 5350 50  0001 C CNN
F 1 "GND" H 2705 5427 50  0000 C CNN
F 2 "" H 2700 5600 50  0001 C CNN
F 3 "" H 2700 5600 50  0001 C CNN
	1    2700 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 5450 2700 5600
Wire Wire Line
	2700 5050 2700 4900
Wire Wire Line
	8200 5350 8200 5450
Wire Wire Line
	8200 4950 8200 4900
$Comp
L power:GND #PWR0115
U 1 1 5D90FF88
P 8850 3600
F 0 "#PWR0115" H 8850 3350 50  0001 C CNN
F 1 "GND" H 8855 3427 50  0000 C CNN
F 2 "" H 8850 3600 50  0001 C CNN
F 3 "" H 8850 3600 50  0001 C CNN
	1    8850 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 5050 2700 5050
Wire Wire Line
	2400 5150 2600 5150
Wire Wire Line
	2400 5250 2600 5250
Wire Wire Line
	2400 5350 2600 5350
Wire Wire Line
	2400 5450 2700 5450
Wire Wire Line
	8200 4950 8450 4950
Wire Wire Line
	8250 5050 8450 5050
Wire Wire Line
	8250 5150 8450 5150
Wire Wire Line
	8250 5250 8450 5250
Wire Wire Line
	8450 5350 8200 5350
$Comp
L Mechanical:MountingHole H1
U 1 1 5D8553DB
P 2350 2350
F 0 "H1" H 2450 2396 50  0000 L CNN
F 1 "MountingHole" H 2450 2305 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 2350 2350 50  0001 C CNN
F 3 "~" H 2350 2350 50  0001 C CNN
	1    2350 2350
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 5D855B09
P 2700 1950
F 0 "H2" H 2800 1996 50  0000 L CNN
F 1 "MountingHole" H 2800 1905 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 2700 1950 50  0001 C CNN
F 3 "~" H 2700 1950 50  0001 C CNN
	1    2700 1950
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0112
U 1 1 5D8F6C01
P 8200 4900
F 0 "#PWR0112" H 8200 4750 50  0001 C CNN
F 1 "VCC" H 8217 5073 50  0000 C CNN
F 2 "" H 8200 4900 50  0001 C CNN
F 3 "" H 8200 4900 50  0001 C CNN
	1    8200 4900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0113
U 1 1 5D8F744B
P 8200 5450
F 0 "#PWR0113" H 8200 5200 50  0001 C CNN
F 1 "GND" H 8205 5277 50  0000 C CNN
F 2 "" H 8200 5450 50  0001 C CNN
F 3 "" H 8200 5450 50  0001 C CNN
	1    8200 5450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4650 4750 4000 4750
Connection ~ 4000 4750
Wire Wire Line
	3800 3550 3900 3550
Wire Wire Line
	3800 3650 3900 3650
Wire Wire Line
	3800 3750 3900 3750
Wire Wire Line
	3800 3850 3900 3850
Wire Wire Line
	3900 3950 3800 3950
Wire Wire Line
	3800 4050 3900 4050
Wire Wire Line
	3800 4150 3900 4150
Wire Wire Line
	3800 4250 3900 4250
Wire Wire Line
	4250 3550 4200 3550
Wire Wire Line
	4250 3650 4200 3650
Wire Wire Line
	4250 3750 4200 3750
Wire Wire Line
	4250 3850 4200 3850
Wire Wire Line
	4250 3950 4200 3950
Wire Wire Line
	4250 4050 4200 4050
Wire Wire Line
	4250 4150 4200 4150
Wire Wire Line
	4250 4250 4200 4250
Text GLabel 3900 3550 2    50   Input ~ 0
I8
Text GLabel 3900 3650 2    50   Input ~ 0
I7
Text GLabel 3900 3750 2    50   Input ~ 0
I6
Text GLabel 3900 3850 2    50   Input ~ 0
I5
Text GLabel 3900 3950 2    50   Input ~ 0
I4
Text GLabel 3900 4050 2    50   Input ~ 0
I3
Text GLabel 3900 4150 2    50   Input ~ 0
I2
Text GLabel 3900 4250 2    50   Input ~ 0
I1
Text GLabel 4200 3550 0    50   Input ~ 0
I1
Text GLabel 4200 3650 0    50   Input ~ 0
I2
Text GLabel 4200 3750 0    50   Input ~ 0
I3
Text GLabel 4200 3850 0    50   Input ~ 0
I4
Text GLabel 4200 3950 0    50   Input ~ 0
I5
Text GLabel 4200 4050 0    50   Input ~ 0
I6
Text GLabel 4200 4150 0    50   Input ~ 0
I7
Text GLabel 4200 4250 0    50   Input ~ 0
I8
Text GLabel 7050 4450 2    50   Input ~ 0
DO
Wire Wire Line
	6900 3550 7000 3550
Wire Wire Line
	6900 3650 7000 3650
Wire Wire Line
	6900 3750 7000 3750
Wire Wire Line
	6900 3850 7000 3850
Wire Wire Line
	6900 3950 7000 3950
Wire Wire Line
	6900 4050 7000 4050
Wire Wire Line
	6900 4150 7000 4150
Wire Wire Line
	6900 4250 7000 4250
Wire Wire Line
	7450 3550 7400 3550
Wire Wire Line
	7450 3650 7400 3650
Wire Wire Line
	7450 3750 7400 3750
Wire Wire Line
	7450 3850 7400 3850
Wire Wire Line
	7450 3950 7400 3950
Wire Wire Line
	7450 4050 7400 4050
Wire Wire Line
	7450 4150 7400 4150
Wire Wire Line
	7450 4250 7400 4250
Text GLabel 7000 3550 2    50   Input ~ 0
I16
Text GLabel 7000 3650 2    50   Input ~ 0
I15
Text GLabel 7000 3750 2    50   Input ~ 0
I14
Text GLabel 7000 3850 2    50   Input ~ 0
I13
Text GLabel 7000 3950 2    50   Input ~ 0
I12
Text GLabel 7000 4050 2    50   Input ~ 0
I11
Text GLabel 7000 4150 2    50   Input ~ 0
I10
Text GLabel 7000 4250 2    50   Input ~ 0
I9
Wire Wire Line
	7100 4750 7850 4750
Text GLabel 7400 3550 0    50   Input ~ 0
I9
Text GLabel 7400 3650 0    50   Input ~ 0
I10
Text GLabel 7400 3750 0    50   Input ~ 0
I11
Text GLabel 7400 3850 0    50   Input ~ 0
I12
Text GLabel 7400 3950 0    50   Input ~ 0
I13
Text GLabel 7400 4050 0    50   Input ~ 0
I14
Text GLabel 7400 4150 0    50   Input ~ 0
I15
Text GLabel 7400 4250 0    50   Input ~ 0
I16
$Comp
L Connector:Screw_Terminal_01x02 J4
U 1 1 5D88329B
P 9450 3400
F 0 "J4" H 9530 3392 50  0000 L CNN
F 1 "Screw_Terminal_01x02" H 9530 3301 50  0000 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal" H 9450 3400 50  0001 C CNN
F 3 "~" H 9450 3400 50  0001 C CNN
	1    9450 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	8850 3600 8850 3500
Wire Wire Line
	8850 3500 9250 3500
Wire Wire Line
	9250 3400 9150 3400
Text GLabel 9150 3400 0    50   Input ~ 0
COM
$EndSCHEMATC
