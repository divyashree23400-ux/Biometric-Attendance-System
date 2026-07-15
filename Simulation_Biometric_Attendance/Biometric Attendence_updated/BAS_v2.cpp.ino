/*
  ==========================================================
  TITUS SOLUTIONS - Biometric Attendance System (In/Out Track)
  ESP32-S3 | ILI9341 TFT | DS1307 RTC
  MFRC522 RFID | Adafruit/R307 Fingerprint Sensor
  Author: Sai Prabhat CA

  SIMULATION VERSION :
  - No SD card. Student data is hardcoded below in
    populateStudents(). Edit that array to change students.
  - Attendance is logged to Serial Monitor instead of a
    CSV file (format matches what the SD version wrote).
  - Added IN/OUT tracking logic.
  ==========================================================
*/

#include <SPI.h>
#include <Wire.h>
#include <RTClib.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <vector>
#include <WiFi.h>
#include <Fonts/FreeSansBold18pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeSans9pt7b.h>

// ---------------- PIN DEFINITIONS ----------------
#define SPI_SCK   18
#define SPI_MOSI  17
#define SPI_MISO  16

#define LCD_CS    15
#define LCD_DC    2
#define LCD_RST   4

// RFID_CS(5) and RFID_RST(11) reserved for when real MFRC522 hardware
// is wired in. Not used while simulating via Serial Monitor.

#define I2C_SDA   9
#define I2C_SCL   10

#define LED_GREEN 13
#define LED_RED   12
#define BUZZER    14

// FINGER_RX(42)/FINGER_TX(41) reserved for when a real fingerprint
// sensor is wired in. Not used while simulating via Serial Monitor.

// ---------------- OBJECTS ----------------
Adafruit_ILI9341 tft = Adafruit_ILI9341(LCD_CS, LCD_DC, LCD_RST);
RTC_DS1307 rtc;

// ---------------- STUDENT DATABASE ----------------
struct Student {
  String rollNo;
  String name;
  String rfidUid;
  int fingerprintId;
  String department;
  bool isCheckedIn; // NEW FEATURE: Tracks whether the student is currently IN or OUT
};

std::vector<Student> students;

// ---------------- FORWARD DECLARATIONS ----------------
void populateStudents();
void checkSerialSimulation();
Student* verifyByRfid(String scannedUid);
Student* verifyByFingerprint(int scannedFingerprintId);
void markAttendance(Student* stu, const char* method);
void grantFeedback();
void denyFeedback();
void showSplashScreen();
void showIdleScreen();
void drawClock(bool force = false); // Default parameter for drawing immediately
void showResultScreen(Student* stu, const char* method, const char* action);
void statusMessage(const char* msg, uint16_t color);
void animateLine(int x0, int y0, int x1, int y1, uint16_t color, int delayMs);
void animateTick(int x, int y, uint16_t color);
void animateCross(int x, int y);

// ==========================================================
//  SETUP
// ==========================================================
void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(BUZZER, LOW);

  // Hold LCD chip-select HIGH before anything else talks on the bus
  pinMode(LCD_CS, OUTPUT);   digitalWrite(LCD_CS, HIGH);

  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, -1);

  // ---- TFT ----
  tft.begin();
  tft.setRotation(3);   // <-- if orientation is wrong, try 0, 1, or 2.
  showSplashScreen();

  // ---- I2C / RTC ----
  Wire.begin(I2C_SDA, I2C_SCL);
  if (!rtc.begin()) {
    Serial.println("RTC not found");
    statusMessage("RTC ERROR", ILI9341_RED);
  } else if (!rtc.isrunning()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  // ---- RFID / Fingerprint: SIMULATION MODE ----
  Serial.println("=== SIMULATION MODE ===");
  Serial.println("Type:  RFID <uid>   e.g. RFID A1B2C3D4");
  Serial.println("Type:  FP <id>      e.g. FP 3");

  // ---- Load student roster (hardcoded, no SD card) ----
  populateStudents();
  Serial.printf("Loaded %d students\n", students.size());

  // Header for the attendance log, printed once at boot. Added "Action" column for Entry/Exit
  Serial.println("RollNo,Name,Department,Method,Date,Time,Action");

  delay(1500);
  showIdleScreen();
}

// ==========================================================
//  MAIN LOOP
// ==========================================================
void loop() {
  static int lastSecond = -1;
  DateTime now = rtc.now();
  if(now.second() != lastSecond){
    lastSecond = now.second();
    drawClock();
  }
  checkSerialSimulation();
  delay(50);
}

// ==========================================================
//  STUDENT DATABASE (HARDCODED — edit this list as needed)
// ==========================================================
void populateStudents() {
  students.clear();
  
  // All students start with isCheckedIn = false (meaning they are currently OUT)
  students.push_back({ "24BTREC043", "TEAM-4", "12345678", 1, "ECE", false });
  students.push_back({ "24BTREC044", "Vinay",    "11223344", 2, "CSE", false });
  students.push_back({ "24BTREC045", "Sam",    "22334455", 3, "EEE", false });
  students.push_back({ "24BTREC046", "Chai",     "33445566", 4, "MECH", false });

  // Add more students the same way:
  // students.push_back({ "ROLL_NO", "Name", "RFID_UID", FINGERPRINT_ID, "DEPT", false });
}

// ==========================================================
//  SIMULATED SCAN INPUT (Serial Monitor)
// ==========================================================
void checkSerialSimulation() {
  if (!Serial.available()) return;

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  if (line.startsWith("RFID")) {
    String uid = line.substring(4);
    uid.trim();
    uid.toUpperCase();
    if (uid.length() == 0) {
      Serial.println("Usage: RFID <uid>   e.g. RFID A1B2C3D4");
      return;
    }
    Serial.printf("Simulated RFID scan: %s\n", uid.c_str());
    Student* match = verifyByRfid(uid);
    markAttendance(match, "RFID");

  } else if (line.startsWith("FP")) {
    String idStr = line.substring(2);
    idStr.trim();
    if (idStr.length() == 0) {
      Serial.println("Usage: FP <id>   e.g. FP 3");
      return;
    }
    int id = idStr.toInt();
    Serial.printf("Simulated fingerprint scan: ID %d\n", id);
    Student* match = verifyByFingerprint(id);
    markAttendance(match, "Fingerprint");

  } else {
    Serial.println("Unknown command. Use: RFID <uid>   or   FP <id>");
  }
}

// ==========================================================
//  DATABASE LOOKUPS
// ==========================================================
Student* verifyByRfid(String scannedUid) {
  for (auto &stu : students) {
    if (stu.rfidUid.equalsIgnoreCase(scannedUid)) return &stu;
  }
  return nullptr;
}

Student* verifyByFingerprint(int scannedFingerprintId) {
  for (auto &stu : students) {
    if (stu.fingerprintId == scannedFingerprintId) return &stu;
  }
  return nullptr;
}

// ==========================================================
//  ATTENDANCE MARKING - LOG (Serial) + DISPLAY + FEEDBACK
// ==========================================================
void markAttendance(Student* stu, const char* method) {
  if (stu == nullptr) {
    denyFeedback();
    showResultScreen(nullptr, method, "DENIED");
    return;
  }

  // Toggle the student's Entry/Exit state
  stu->isCheckedIn = !stu->isCheckedIn; 
  const char* actionStr = stu->isCheckedIn ? "ENTRY" : "EXIT";

  DateTime now = rtc.now();
  char dateStr[11];
  char timeStr[9];
  snprintf(dateStr, sizeof(dateStr), "%04d-%02d-%02d", now.year(), now.month(), now.day());
  snprintf(timeStr, sizeof(timeStr), "%02d:%02d:%02d", now.hour(), now.minute(), now.second());

  // Logged to Serial instead of SD card CSV — now includes the Action column (Entry/Exit)
  Serial.printf("%s,%s,%s,%s,%s,%s,%s\n",
    stu->rollNo.c_str(), stu->name.c_str(), stu->department.c_str(),
    method, dateStr, timeStr, actionStr);

  grantFeedback();
  showResultScreen(stu, method, actionStr);
}

// ==========================================================
//  FEEDBACK - LEDs + BUZZER
// ==========================================================
void grantFeedback() {
  digitalWrite(LED_GREEN, HIGH);
  tone(BUZZER, 2000); // High pitch (2000 Hz) for success
  delay(150);
  noTone(BUZZER);     // Stop buzzer
  delay(700);
  digitalWrite(LED_GREEN, LOW);
}

void denyFeedback() {
  digitalWrite(LED_RED, HIGH);
  for (int i = 0; i < 2; i++) {
    tone(BUZZER, 500); // Low pitch (500 Hz) for error
    delay(120);
    noTone(BUZZER);    // Stop buzzer
    delay(120);
  }
  delay(400);
  digitalWrite(LED_RED, LOW);
}

// ==========================================================
//  ANIMATIONS (Tick & Cross)
// ==========================================================
// Helper function to draw a line pixel-by-pixel (circle-by-circle) for animation
void animateLine(int x0, int y0, int x1, int y1, uint16_t color, int delayMs) {
  int dx = abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
  int dy = -abs(y1 - y0), sy = y0 < y1 ? 1 : -1; 
  int err = dx + dy, e2; /* error value e_xy */

  while (true) {
    tft.fillCircle(x0, y0, 2, color); // Draw a small 2px radius circle to make the line thick
    if (x0 == x1 && y0 == y1) break;
    e2 = 2 * err;
    if (e2 >= dy) { err += dy; x0 += sx; }
    if (e2 <= dx) { err += dx; y0 += sy; }
    delay(delayMs);
  }
}

void animateTick(int x, int y, uint16_t color) {
  // Draw down-right stroke
  animateLine(x, y, x + 15, y + 15, color, 2);
  // Draw up-right stroke
  animateLine(x + 15, y + 15, x + 40, y - 20, color, 2);
}

void animateCross(int x, int y) {
  // Draw top-left to bottom-right
  animateLine(x, y, x + 30, y + 30, ILI9341_RED, 2);
  // Draw bottom-left to top-right
  animateLine(x + 30, y, x, y + 30, ILI9341_RED, 2);
}

// ==========================================================
//  TFT DISPLAY SCREENS
// ==========================================================
void showSplashScreen() {
  tft.fillScreen(ILI9341_BLACK);
  tft.setTextColor(ILI9341_CYAN);
  tft.setTextSize(3);
  tft.setCursor(20, 70);
  tft.println("TITUS");
  tft.setCursor(20, 105);
  tft.println("SOLUTIONS");
  tft.setTextSize(2);
  tft.setTextColor(ILI9341_WHITE);
  tft.setCursor(35, 145);
  tft.print("Biometric");
  tft.setCursor(35, 170);
  tft.print("Attendance System");
}

void showIdleScreen() {
  tft.fillScreen(ILI9341_BLACK);
  
  // Set custom font back to default standard text for small headers
  tft.setFont();
  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(1);
  
  // Top-left aligned headers
  tft.setCursor(10, 10);
  tft.println("TITUS SOLUTIONS");
  tft.setCursor(10, 32);
  tft.println("Scan RFID or fingerprint");
  
  // Force clock to draw immediately without waiting for a minute tick
  drawClock(true);
}

void drawClock(bool force) {
  DateTime now = rtc.now();

  static int lastMinute = -1;
  if (!force && now.minute() == lastMinute) return;
  lastMinute = now.minute();

  // Clear just the lower area where the time, date, and WiFi info live
  // so we don't erase the top header text
  tft.fillRect(0, 55, 320, 185, ILI9341_BLACK);

  char timeStr[6];
  sprintf(timeStr, "%02d:%02d", now.hour(), now.minute());

  const char* days[] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
  const char* months[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
  
  char dateStr[24];
  sprintf(dateStr, "%02d %s %04d", now.day(), months[now.month() - 1], now.year());

  int16_t x1, y1;
  uint16_t w, h;
  
  // Scale up the 18pt font to make the time noticeably larger (effectively 36pt)
  tft.setTextSize(2); 
  
  tft.setFont(&FreeSansBold18pt7b);
  tft.getTextBounds(timeStr, 0, 0, &x1, &y1, &w, &h);
  int xTime = (320 - w) / 2;
  tft.setTextColor(ILI9341_CYAN);
  tft.setCursor(xTime, 130);
  tft.print(timeStr);

  // CRITICAL: Reset scale to 1 for the smaller fonts below!
  tft.setTextSize(1); 
  
  tft.setFont(&FreeSans12pt7b);
  tft.setTextColor(ILI9341_WHITE);
  tft.setCursor(10, 172); // Adjusted for spacing
  tft.print(days[now.dayOfTheWeek()]);

  tft.setTextColor(ILI9341_LIGHTGREY);
  tft.setCursor(10, 198); // Adjusted for spacing
  tft.print(dateStr);

  tft.fillCircle(14, 219, 4, WiFi.status() == WL_CONNECTED ? ILI9341_GREEN : ILI9341_RED);
  tft.setFont(); // Switch back to classic 5x7 for standard UI elements
  tft.setTextSize(1);
  tft.setCursor(24, 215); // Adjusted for spacing
  if(WiFi.status() == WL_CONNECTED){
    tft.setTextColor(ILI9341_GREEN);
    tft.print("WiFi: Connected");
  } else {
    tft.setTextColor(ILI9341_RED);
    tft.print("WiFi: Disconnected");
  }
}

void showResultScreen(Student* stu, const char* method, const char* action) {
  tft.fillScreen(ILI9341_BLACK);

  // Fetch exact scan time right away so we can use it in both branches
  DateTime now = rtc.now();
  char scanTime[12];
  sprintf(scanTime, "%02d:%02d:%02d", now.hour(), now.minute(), now.second());

  if (stu == nullptr) {
    tft.setTextColor(ILI9341_RED);
    tft.setFont(&FreeSansBold18pt7b);
    tft.setTextSize(1);
    tft.setCursor(20, 90);
    tft.println("ACCESS DENIED");
    
    // Display the exact time of the denied access
    tft.setFont(&FreeSans9pt7b);
    tft.setTextColor(ILI9341_LIGHTGREY);
    tft.setCursor(20, 130);
    tft.print("Time: ");
    tft.println(scanTime);
    
    // Draw animated cross at the bottom right corner
    animateCross(260, 180); 
  } else {
    // Dynamic text and colors based on Entry vs Exit
    bool isEntry = (strcmp(action, "ENTRY") == 0);
    uint16_t statusColor = isEntry ? ILI9341_GREEN : ILI9341_YELLOW;
    
    tft.setTextColor(statusColor);
    tft.setFont(&FreeSans12pt7b);
    tft.setTextSize(1);
    tft.setCursor(20, 40);
    
    if (isEntry) {
      tft.println("ENTRY MARKED");
    } else {
      tft.println("EXIT MARKED");
    }

    // Large, highly visible Name
    tft.setFont(&FreeSansBold18pt7b);
    tft.setTextColor(ILI9341_WHITE);
    tft.setTextSize(1);
    tft.setCursor(20, 100);
    tft.println(stu->name);

    // Clean, readable smaller font for details
    tft.setFont(&FreeSans9pt7b);
    tft.setTextColor(ILI9341_LIGHTGREY);
    
    tft.setCursor(20, 135);
    tft.print("Roll No: ");
    tft.println(stu->rollNo);
    
    tft.setCursor(20, 160);
    tft.print("Dept: ");
    tft.println(stu->department);
    
    tft.setCursor(20, 185);
    tft.print("Method: ");
    tft.println(method);

    tft.setCursor(20, 210);
    tft.print("Time: ");
    tft.println(scanTime);

    // Draw animated tick in the same color as the Entry/Exit status
    animateTick(260, 190, statusColor); 
  }

  delay(3500); // Increased display time so user can easily read all details
  showIdleScreen();
}

void statusMessage(const char* msg, uint16_t color) {
  tft.fillScreen(ILI9341_BLACK);
  tft.setFont(); // Fallback to standard
  tft.setTextColor(color);
  tft.setTextSize(2);
  tft.setCursor(10, 100);
  tft.println(msg);
}