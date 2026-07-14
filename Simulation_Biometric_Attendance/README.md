# Biometric Attendance System (ESP32-S3)

Internship project — Titus Solutions
- Author: Sai Prabhat CA
- USN-24BTREC061

## Overview

A working attendance system simulated on Wokwi using an ESP32-S3. Students are identified via RFID card or fingerprint ID (simulated through Serial commands), with attendance results shown on an TFT display, confirmed via LED/buzzer feedback, timestamped using an RTC module, and logged to an SD card in CSV format.

## Hardware Used

| Component        | Purpose                                |
|-------------------|-----------------------------------------|
| ESP32 DevKit      | Main microcontroller                    |
| TFT ILI9341 | Status / attendance display   |
| RTC DS1307        | Real-time clock (date & time stamping)  |
| SD Card Module    | Attendance logging (CSV storage)        |
| Green LED         | Success indicator                       |
| Red LED           | Failure/denied indicator                |
| Buzzer            | Audio feedback (success/error tones)    |



## Development Stages

- **v1 / v2** — Simulation tool setup and basic wiring/connections.
- **v3** — RFID + fingerprint identity verification logic (Serial-simulated), OLED feedback, LED/buzzer indicators.
- **v4** — Real-time day & date via RTC DS1307, non-blocking live clock refresh on idle screen, styled attendance screen (ID / Name / Time), "TITUS SOLUTIONS" branding on idle screen.
- **v5** — SD card logging: every successful scan is appended to `attendance.csv` on the SD card, with a `DUMP` command to print the file's contents over Serial for verification (since Wokwi's SD Card file browser upload/view is a paid-tier feature).
-**updated** - Updated the userinfo display and few other minor chnages

## Registered Students

| Student ID | Name         | RFID Code | Fingerprint ID |
|------------|--------------|-----------|-----------------|
| 101        | Sai          | 12345678  | 1               |
| 103        | Vinay        | 11223344  | 2               |
| 104        | Sam          | 22334455  | 3               |
| 105        | Chai         | 33445566  | 4               |

> Note: RFID codes and fingerprint IDs for Vinay, Sam, and Chai are placeholder values. Replace with actual enrolled card/sensor values before real deployment.

## Serial Commands (Simulation Mode)

Since physical RFID/fingerprint hardware isn't wired in simulation, identity checks are triggered manually via the Serial Monitor (115200 baud):

```
RFID:12345678   -> Sai 
RFID:11223344   -> Vinay
RFID:22334455   -> Sam
RFID:33445566   -> Chai
FP:1            -> Sai 
FP:2            -> Vinay
FP:3            -> Sam
FP:4            -> Chai
DUMP            -> Print attendance.csv contents from SD card
```

## SD Card Logging

On every successful scan, a row is appended to `/attendance.csv` on the SD card in this format:

```
StudentID,Name,Method,Date,Time
101,Sai Prabhat,RFID,Sun 05/07/2026,13:45:07
```

No header row is currently written. Failed/denied attempts are **not** logged — only successful attendance events.

Because Wokwi's SD Card file browser (view/upload) is restricted to paid accounts, the `DUMP` command is used instead to print the CSV contents directly to the Serial Monitor for verification during simulation.

## Known Limitations / Next Steps

- WiFi + online database sync not yet implemented — planned as a separate module: when WiFi is available, records save directly to an online database; when offline, records save to SD card and sync once WiFi is restored.
- No CSV header row yet.
- Failed/denied attempts are not currently logged to SD.
- RTC auto-adjusts to compile time only if `rtc.isrunning()` returns false — repeated re-uploads with this active will keep resetting the clock to compile time; a dedicated "SETTIME" command would allow safer manual time-setting without needing to re-flash.
- RFID/fingerprint values for 3 of the 4 students are placeholders and need to be replaced with real hardware-scanned values.

## Wiring Diagram

Refer to `diagram.json` in the Wokwi project for full wiring connections between the ESP32, OLED, RTC, SD card module, LEDs, and buzzer.
