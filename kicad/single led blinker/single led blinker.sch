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
L dk_Clock-Timing-Programmable-Timers-and-Oscillators:NE555P U1
U 1 1 5F8B96C9
P 3700 3300
AR Path="/5F8B96C9" Ref="U1"  Part="1" 
AR Path="/5F8AD8AD/5F8B96C9" Ref="U?"  Part="1" 
AR Path="/5F8C8860/5F8B96C9" Ref="U?"  Part="1" 
AR Path="/5F8C8A56/5F8B96C9" Ref="U?"  Part="1" 
AR Path="/5F8C8B72/5F8B96C9" Ref="U?"  Part="1" 
AR Path="/5F8C8C7E/5F8B96C9" Ref="U?"  Part="1" 
AR Path="/5F8C8D8D/5F8B96C9" Ref="U?"  Part="1" 
F 0 "U1" H 3700 3803 60  0000 C CNN
F 1 "NE555P" H 3700 3697 60  0000 C CNN
F 2 "Package_DIP:DIP-8_W7.62mm" H 3900 3500 60  0001 L CNN
F 3 "http://www.ti.com/general/docs/suppproductinfo.tsp?distId=10&gotoUrl=http%3A%2F%2Fwww.ti.com%2Flit%2Fgpn%2Fne555" H 3900 3600 60  0001 L CNN
F 4 "296-1411-5-ND" H 3900 3700 60  0001 L CNN "Digi-Key_PN"
F 5 "NE555P" H 3900 3800 60  0001 L CNN "MPN"
F 6 "Integrated Circuits (ICs)" H 3900 3900 60  0001 L CNN "Category"
F 7 "Clock/Timing - Programmable Timers and Oscillators" H 3900 4000 60  0001 L CNN "Family"
F 8 "http://www.ti.com/general/docs/suppproductinfo.tsp?distId=10&gotoUrl=http%3A%2F%2Fwww.ti.com%2Flit%2Fgpn%2Fne555" H 3900 4100 60  0001 L CNN "DK_Datasheet_Link"
F 9 "/product-detail/en/texas-instruments/NE555P/296-1411-5-ND/277057" H 3900 4200 60  0001 L CNN "DK_Detail_Page"
F 10 "IC OSC SINGLE TIMER 100KHZ 8-DIP" H 3900 4300 60  0001 L CNN "Description"
F 11 "Texas Instruments" H 3900 4400 60  0001 L CNN "Manufacturer"
F 12 "Active" H 3900 4500 60  0001 L CNN "Status"
	1    3700 3300
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 5F8B96CF
P 4350 2950
AR Path="/5F8B96CF" Ref="R3"  Part="1" 
AR Path="/5F8AD8AD/5F8B96CF" Ref="R?"  Part="1" 
AR Path="/5F8C8860/5F8B96CF" Ref="R?"  Part="1" 
AR Path="/5F8C8A56/5F8B96CF" Ref="R?"  Part="1" 
AR Path="/5F8C8B72/5F8B96CF" Ref="R?"  Part="1" 
AR Path="/5F8C8C7E/5F8B96CF" Ref="R?"  Part="1" 
AR Path="/5F8C8D8D/5F8B96CF" Ref="R?"  Part="1" 
F 0 "R3" H 4420 2996 50  0000 L CNN
F 1 "100K" H 4420 2905 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4280 2950 50  0001 C CNN
F 3 "~" H 4350 2950 50  0001 C CNN
	1    4350 2950
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5F8B96D5
P 2650 3200
AR Path="/5F8B96D5" Ref="R1"  Part="1" 
AR Path="/5F8AD8AD/5F8B96D5" Ref="R?"  Part="1" 
AR Path="/5F8C8860/5F8B96D5" Ref="R?"  Part="1" 
AR Path="/5F8C8A56/5F8B96D5" Ref="R?"  Part="1" 
AR Path="/5F8C8B72/5F8B96D5" Ref="R?"  Part="1" 
AR Path="/5F8C8C7E/5F8B96D5" Ref="R?"  Part="1" 
AR Path="/5F8C8D8D/5F8B96D5" Ref="R?"  Part="1" 
F 0 "R1" H 2720 3246 50  0000 L CNN
F 1 "51K" H 2720 3155 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2580 3200 50  0001 C CNN
F 3 "~" H 2650 3200 50  0001 C CNN
	1    2650 3200
	1    0    0    -1  
$EndComp
$Comp
L Device:CP1 C1
U 1 1 5F8B96DB
P 3050 3750
AR Path="/5F8B96DB" Ref="C1"  Part="1" 
AR Path="/5F8AD8AD/5F8B96DB" Ref="C?"  Part="1" 
AR Path="/5F8C8860/5F8B96DB" Ref="C?"  Part="1" 
AR Path="/5F8C8A56/5F8B96DB" Ref="C?"  Part="1" 
AR Path="/5F8C8B72/5F8B96DB" Ref="C?"  Part="1" 
AR Path="/5F8C8C7E/5F8B96DB" Ref="C?"  Part="1" 
AR Path="/5F8C8D8D/5F8B96DB" Ref="C?"  Part="1" 
F 0 "C1" H 3165 3796 50  0000 L CNN
F 1 "10uf" H 3165 3705 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm" H 3050 3750 50  0001 C CNN
F 3 "~" H 3050 3750 50  0001 C CNN
	1    3050 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 3000 3700 2700
Wire Wire Line
	3700 3700 3700 3950
$Comp
L power:+5V #PWR03
U 1 1 5F8B96E3
P 3700 1900
AR Path="/5F8B96E3" Ref="#PWR03"  Part="1" 
AR Path="/5F8AD8AD/5F8B96E3" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8860/5F8B96E3" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8A56/5F8B96E3" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8B72/5F8B96E3" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8C7E/5F8B96E3" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8D8D/5F8B96E3" Ref="#PWR?"  Part="1" 
F 0 "#PWR03" H 3700 1750 50  0001 C CNN
F 1 "+5V" H 3715 2073 50  0000 C CNN
F 2 "" H 3700 1900 50  0001 C CNN
F 3 "" H 3700 1900 50  0001 C CNN
	1    3700 1900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 5F8B96E9
P 3700 4150
AR Path="/5F8B96E9" Ref="#PWR04"  Part="1" 
AR Path="/5F8AD8AD/5F8B96E9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8860/5F8B96E9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8A56/5F8B96E9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8B72/5F8B96E9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8C7E/5F8B96E9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8D8D/5F8B96E9" Ref="#PWR?"  Part="1" 
F 0 "#PWR04" H 3700 3900 50  0001 C CNN
F 1 "GND" H 3705 3977 50  0000 C CNN
F 2 "" H 3700 4150 50  0001 C CNN
F 3 "" H 3700 4150 50  0001 C CNN
	1    3700 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	3050 3200 3050 2700
Wire Wire Line
	3050 2700 3700 2700
Connection ~ 3700 2700
Wire Wire Line
	3050 3200 3200 3200
Wire Wire Line
	4200 3300 4350 3300
Wire Wire Line
	4350 3300 4350 3100
Wire Wire Line
	4350 2800 4350 2700
Wire Wire Line
	4350 2700 3700 2700
Wire Wire Line
	3200 3400 3050 3400
Wire Wire Line
	2650 3400 2650 3350
Wire Wire Line
	2650 3050 2650 2950
Wire Wire Line
	2650 2950 4200 2950
Wire Wire Line
	4200 2950 4200 3300
Connection ~ 4200 3300
Wire Wire Line
	3200 3300 3050 3300
Wire Wire Line
	3050 3300 3050 3400
Connection ~ 3050 3400
Wire Wire Line
	3050 3400 2650 3400
Wire Wire Line
	3050 3400 3050 3600
Wire Wire Line
	3050 3900 3050 3950
Wire Wire Line
	3050 3950 3700 3950
Connection ~ 3700 3950
Wire Wire Line
	3700 3950 3700 4150
NoConn ~ 3200 3500
Wire Wire Line
	3700 2700 3700 2600
Wire Wire Line
	4000 2300 4100 2300
Wire Wire Line
	4900 2100 4900 2200
Wire Wire Line
	3700 2100 3700 2200
Wire Wire Line
	5200 2300 5300 2300
$Comp
L Device:R R5
U 1 1 5F8B971E
P 5300 3400
AR Path="/5F8B971E" Ref="R5"  Part="1" 
AR Path="/5F8AD8AD/5F8B971E" Ref="R?"  Part="1" 
AR Path="/5F8C8860/5F8B971E" Ref="R?"  Part="1" 
AR Path="/5F8C8A56/5F8B971E" Ref="R?"  Part="1" 
AR Path="/5F8C8B72/5F8B971E" Ref="R?"  Part="1" 
AR Path="/5F8C8C7E/5F8B971E" Ref="R?"  Part="1" 
AR Path="/5F8C8D8D/5F8B971E" Ref="R?"  Part="1" 
F 0 "R5" V 5200 3350 50  0000 L CNN
F 1 "330R" V 5300 3350 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5230 3400 50  0001 C CNN
F 3 "~" H 5300 3400 50  0001 C CNN
	1    5300 3400
	0    1    1    0   
$EndComp
Wire Wire Line
	5450 3400 5700 3400
$Comp
L Device:D D1
U 1 1 5F8B9725
P 4550 3400
AR Path="/5F8B9725" Ref="D1"  Part="1" 
AR Path="/5F8AD8AD/5F8B9725" Ref="D?"  Part="1" 
AR Path="/5F8C8860/5F8B9725" Ref="D?"  Part="1" 
AR Path="/5F8C8A56/5F8B9725" Ref="D?"  Part="1" 
AR Path="/5F8C8B72/5F8B9725" Ref="D?"  Part="1" 
AR Path="/5F8C8C7E/5F8B9725" Ref="D?"  Part="1" 
AR Path="/5F8C8D8D/5F8B9725" Ref="D?"  Part="1" 
F 0 "D1" H 4550 3183 50  0000 C CNN
F 1 "1N4148" H 4550 3274 50  0000 C CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 4550 3400 50  0001 C CNN
F 3 "~" H 4550 3400 50  0001 C CNN
	1    4550 3400
	-1   0    0    1   
$EndComp
$Comp
L Device:D D2
U 1 1 5F8B972B
P 4900 2900
AR Path="/5F8B972B" Ref="D2"  Part="1" 
AR Path="/5F8AD8AD/5F8B972B" Ref="D?"  Part="1" 
AR Path="/5F8C8860/5F8B972B" Ref="D?"  Part="1" 
AR Path="/5F8C8A56/5F8B972B" Ref="D?"  Part="1" 
AR Path="/5F8C8B72/5F8B972B" Ref="D?"  Part="1" 
AR Path="/5F8C8C7E/5F8B972B" Ref="D?"  Part="1" 
AR Path="/5F8C8D8D/5F8B972B" Ref="D?"  Part="1" 
F 0 "D2" V 4946 2820 50  0000 R CNN
F 1 "1N4148" V 4855 2820 50  0000 R CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 4900 2900 50  0001 C CNN
F 3 "~" H 4900 2900 50  0001 C CNN
	1    4900 2900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4900 2600 4900 2750
Wire Wire Line
	4150 3400 4200 3400
Connection ~ 4200 3400
Wire Wire Line
	4200 3400 4400 3400
Wire Wire Line
	4700 3400 4900 3400
Wire Wire Line
	4900 3050 4900 3400
Connection ~ 4900 3400
Wire Wire Line
	4900 3400 5150 3400
$Comp
L Device:R R4
U 1 1 5F8B9739
P 5050 2100
AR Path="/5F8B9739" Ref="R4"  Part="1" 
AR Path="/5F8AD8AD/5F8B9739" Ref="R?"  Part="1" 
AR Path="/5F8C8860/5F8B9739" Ref="R?"  Part="1" 
AR Path="/5F8C8A56/5F8B9739" Ref="R?"  Part="1" 
AR Path="/5F8C8B72/5F8B9739" Ref="R?"  Part="1" 
AR Path="/5F8C8C7E/5F8B9739" Ref="R?"  Part="1" 
AR Path="/5F8C8D8D/5F8B9739" Ref="R?"  Part="1" 
F 0 "R4" V 4950 2050 50  0000 L CNN
F 1 "1K" V 5050 2050 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 4980 2100 50  0001 C CNN
F 3 "~" H 5050 2100 50  0001 C CNN
	1    5050 2100
	0    1    1    0   
$EndComp
Connection ~ 4900 2100
$Comp
L Device:R R2
U 1 1 5F8B9740
P 3850 2100
AR Path="/5F8B9740" Ref="R2"  Part="1" 
AR Path="/5F8AD8AD/5F8B9740" Ref="R?"  Part="1" 
AR Path="/5F8C8860/5F8B9740" Ref="R?"  Part="1" 
AR Path="/5F8C8A56/5F8B9740" Ref="R?"  Part="1" 
AR Path="/5F8C8B72/5F8B9740" Ref="R?"  Part="1" 
AR Path="/5F8C8C7E/5F8B9740" Ref="R?"  Part="1" 
AR Path="/5F8C8D8D/5F8B9740" Ref="R?"  Part="1" 
F 0 "R2" V 3750 2050 50  0000 L CNN
F 1 "1K" V 3850 2050 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 3780 2100 50  0001 C CNN
F 3 "~" H 3850 2100 50  0001 C CNN
	1    3850 2100
	0    1    1    0   
$EndComp
Wire Wire Line
	5200 2100 5200 2300
Wire Wire Line
	4000 2100 4000 2300
Wire Wire Line
	4900 1900 4900 2100
Wire Wire Line
	3700 1900 3700 2100
Connection ~ 3700 2100
Wire Wire Line
	4900 1900 3700 1900
Connection ~ 3700 1900
Text GLabel 5300 2300 2    50   Input ~ 0
GSOLID
Text GLabel 4100 2300 2    50   Input ~ 0
GBLINK
Text GLabel 5700 3400 2    50   Output ~ 0
LEDA
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 5F8E8B96
P 3050 1000
F 0 "J2" H 3130 946 50  0000 L CNN
F 1 "Conn_01x02" H 3130 901 50  0001 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Horizontal" H 3050 1000 50  0001 C CNN
F 3 "~" H 3050 1000 50  0001 C CNN
	1    3050 1000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 5F8E9611
P 3550 1000
F 0 "J3" H 3630 946 50  0000 L CNN
F 1 "Conn_01x02" H 3630 901 50  0001 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x02_P2.54mm_Horizontal" H 3550 1000 50  0001 C CNN
F 3 "~" H 3550 1000 50  0001 C CNN
	1    3550 1000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J4
U 1 1 5F8E9B49
P 4050 1100
F 0 "J4" H 3968 867 50  0000 C CNN
F 1 "Conn_01x02" H 4130 1001 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal" H 4050 1100 50  0001 C CNN
F 3 "~" H 4050 1100 50  0001 C CNN
	1    4050 1100
	1    0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J5
U 1 1 5F8E9E3D
P 6950 2950
F 0 "J5" H 7030 2896 50  0000 L CNN
F 1 "Conn_01x02" H 7030 2851 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal" H 6950 2950 50  0001 C CNN
F 3 "~" H 6950 2950 50  0001 C CNN
	1    6950 2950
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5F8EA294
P 1900 2650
F 0 "J1" H 1980 2596 50  0000 L CNN
F 1 "Conn_01x02" H 1980 2551 50  0001 L CNN
F 2 "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal" H 1900 2650 50  0001 C CNN
F 3 "~" H 1900 2650 50  0001 C CNN
	1    1900 2650
	1    0    0    -1  
$EndComp
Text GLabel 1500 2650 0    50   Input ~ 0
GBLINK
Text GLabel 1500 2750 0    50   Input ~ 0
GSOLID
Text GLabel 6550 2950 0    50   Output ~ 0
LEDA
Wire Wire Line
	6550 2950 6750 2950
Wire Wire Line
	1700 2650 1500 2650
Wire Wire Line
	1700 2750 1500 2750
Wire Wire Line
	2850 1100 2850 1200
Wire Wire Line
	2850 1000 2850 900 
Wire Wire Line
	3850 1100 3850 1200
Wire Wire Line
	3850 1200 3350 1200
Connection ~ 2850 1200
Wire Wire Line
	2850 1200 2850 1300
Wire Wire Line
	3350 1100 3350 1200
Connection ~ 3350 1200
Wire Wire Line
	3350 1200 2850 1200
Connection ~ 2850 900 
Wire Wire Line
	2850 900  2850 750 
Wire Wire Line
	3350 1000 3350 900 
Wire Wire Line
	3350 900  2850 900 
$Comp
L power:+5V #PWR01
U 1 1 5F8F3070
P 2850 750
AR Path="/5F8F3070" Ref="#PWR01"  Part="1" 
AR Path="/5F8AD8AD/5F8F3070" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8860/5F8F3070" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8A56/5F8F3070" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8B72/5F8F3070" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8C7E/5F8F3070" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8D8D/5F8F3070" Ref="#PWR?"  Part="1" 
F 0 "#PWR01" H 2850 600 50  0001 C CNN
F 1 "+5V" H 2865 923 50  0000 C CNN
F 2 "" H 2850 750 50  0001 C CNN
F 3 "" H 2850 750 50  0001 C CNN
	1    2850 750 
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 5F8F35B9
P 2850 1300
AR Path="/5F8F35B9" Ref="#PWR02"  Part="1" 
AR Path="/5F8AD8AD/5F8F35B9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8860/5F8F35B9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8A56/5F8F35B9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8B72/5F8F35B9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8C7E/5F8F35B9" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8D8D/5F8F35B9" Ref="#PWR?"  Part="1" 
F 0 "#PWR02" H 2850 1050 50  0001 C CNN
F 1 "GND" H 2855 1127 50  0000 C CNN
F 2 "" H 2850 1300 50  0001 C CNN
F 3 "" H 2850 1300 50  0001 C CNN
	1    2850 1300
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG01
U 1 1 5F8F3D9E
P 2850 900
F 0 "#FLG01" H 2850 975 50  0001 C CNN
F 1 "PWR_FLAG" V 2850 1027 50  0000 L CNN
F 2 "" H 2850 900 50  0001 C CNN
F 3 "~" H 2850 900 50  0001 C CNN
	1    2850 900 
	0    -1   -1   0   
$EndComp
$Comp
L power:PWR_FLAG #FLG02
U 1 1 5F8F4BBD
P 2850 1200
F 0 "#FLG02" H 2850 1275 50  0001 C CNN
F 1 "PWR_FLAG" V 2850 1327 50  0000 L CNN
F 2 "" H 2850 1200 50  0001 C CNN
F 3 "~" H 2850 1200 50  0001 C CNN
	1    2850 1200
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR05
U 1 1 5F8F4DE0
P 6600 3150
AR Path="/5F8F4DE0" Ref="#PWR05"  Part="1" 
AR Path="/5F8AD8AD/5F8F4DE0" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8860/5F8F4DE0" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8A56/5F8F4DE0" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8B72/5F8F4DE0" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8C7E/5F8F4DE0" Ref="#PWR?"  Part="1" 
AR Path="/5F8C8D8D/5F8F4DE0" Ref="#PWR?"  Part="1" 
F 0 "#PWR05" H 6600 2900 50  0001 C CNN
F 1 "GND" H 6605 2977 50  0000 C CNN
F 2 "" H 6600 3150 50  0001 C CNN
F 3 "" H 6600 3150 50  0001 C CNN
	1    6600 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 3050 6600 3050
Wire Wire Line
	6600 3050 6600 3150
Wire Wire Line
	3850 1000 3850 900 
Wire Wire Line
	3850 900  3350 900 
Connection ~ 3350 900 
$Comp
L my~symbols:NDP6020P Q1
U 1 1 608CEEB2
P 3700 2400
F 0 "Q1" H 3807 2347 60  0000 L CNN
F 1 "NDP6020P" H 3807 2453 60  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 3900 2600 60  0001 L CNN
F 3 "https://www.onsemi.com/pub/Collateral/NDP6020P-D.PDF" H 3900 2700 60  0001 L CNN
F 4 "NDP6020P-ND" H 3900 2800 60  0001 L CNN "Digi-Key_PN"
F 5 "NDP60020P" H 3900 2900 60  0001 L CNN "MPN"
F 6 "Discrete Semiconductor Products" H 3900 3000 60  0001 L CNN "Category"
F 7 "Transistors - FETs, MOSFETs - Single" H 3900 3100 60  0001 L CNN "Family"
	1    3700 2400
	-1   0    0    1   
$EndComp
$Comp
L my~symbols:NDP6020P Q2
U 1 1 608CFF3D
P 4900 2400
F 0 "Q2" H 5007 2347 60  0000 L CNN
F 1 "NDP6020P" H 5007 2453 60  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 5100 2600 60  0001 L CNN
F 3 "https://www.onsemi.com/pub/Collateral/NDP6020P-D.PDF" H 5100 2700 60  0001 L CNN
F 4 "NDP6020P-ND" H 5100 2800 60  0001 L CNN "Digi-Key_PN"
F 5 "NDP60020P" H 5100 2900 60  0001 L CNN "MPN"
F 6 "Discrete Semiconductor Products" H 5100 3000 60  0001 L CNN "Category"
F 7 "Transistors - FETs, MOSFETs - Single" H 5100 3100 60  0001 L CNN "Family"
	1    4900 2400
	-1   0    0    1   
$EndComp
Connection ~ 4000 2300
Connection ~ 5200 2300
$EndSCHEMATC
