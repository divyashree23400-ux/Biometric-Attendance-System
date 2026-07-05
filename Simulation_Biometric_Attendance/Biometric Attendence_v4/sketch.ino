#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <RTClib.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SD_CS 5
#define GREEN_LED 25
#define RED_LED 26
#define BUZZER 27

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
RTC_DS1307 rtc;

const char* dayNames[7] = {"Sun","Mon","Tue","Wed","Thu","Fri","Sat"};

unsigned long lastClockUpdate = 0;
bool idleScreen = true; // true = ready screen is showing (safe to auto-refresh clock)

struct Student{
  int studentID;
  String name;
  String rfid;
  int fingerID;
};

Student students[]={
  {101,"Sai Prabhat","12345678",1},
  {102,"Rahul","87654321",2}
};

String getTimeStr(DateTime t){
  char buf[9];
  sprintf(buf,"%02d:%02d:%02d",t.hour(),t.minute(),t.second());
  return String(buf);
}

String getDateStr(DateTime t){
  char buf[20];
  sprintf(buf,"%s %02d/%02d/%04d",dayNames[t.dayOfTheWeek()],t.day(),t.month(),t.year());
  return String(buf);
}

void successBeep(){ ledcAttach(BUZZER,2000,8); ledcWrite(BUZZER,128); delay(150); ledcWrite(BUZZER,0); }
void errorBeep(){ ledcAttach(BUZZER,1000,8); for(int i=0;i<3;i++){ ledcWrite(BUZZER,128); delay(100); ledcWrite(BUZZER,0); delay(80);} }

void showMessage(String a,String b="",String c=""){
 display.clearDisplay();
 display.setTextSize(1);
 display.setTextColor(SSD1306_WHITE);
 display.setCursor(0,0);
 display.println(a); display.println();
 if(b!="") display.println(b);
 if(c!="") display.println(c);
 display.display();
}

void showAttendanceScreen(String method, int id, String name, String timeStr){
 display.clearDisplay();
 display.setTextSize(1);
 display.setTextColor(SSD1306_WHITE);

 display.setCursor(0,0);
 display.println(method+" VERIFIED");
 display.drawLine(0,10,127,10,SSD1306_WHITE);

 display.setCursor(0,16);
 display.print("ID   : ");
 display.println(id);

 display.setCursor(0,28);
 display.print("Name : ");
 display.println(name);

 display.setCursor(0,44);
 display.print("Time : ");
 display.println(timeStr);

 display.setCursor(0,56);
 display.println("Attendance Marked");

 display.display();
}

void readyScreen(){
 idleScreen=true;
 DateTime now=rtc.now();
 display.clearDisplay();
 display.setTextSize(1);
 display.setTextColor(SSD1306_WHITE);
 display.setCursor(0,0);
 display.println("BIOMETRIC SYSTEM");
 display.println("Scan RFID / FP");
 display.println();
 display.println(getDateStr(now));
 display.println(getTimeStr(now));

 display.setCursor(38,56); // right-aligned: (128 - 90px text width) = 38
 display.print("TITUS SOLUTIONS");
 
 display.display();
}

void attendanceSuccess(int i,String method){
 idleScreen=false;
 digitalWrite(GREEN_LED,HIGH);
 successBeep();
 DateTime now=rtc.now();
 showAttendanceScreen(method, students[i].studentID, students[i].name, getTimeStr(now));
 delay(2500);
 digitalWrite(GREEN_LED,LOW);
 readyScreen();
}

void attendanceFailed(String msg){
 idleScreen=false;
 digitalWrite(RED_LED,HIGH);
 errorBeep();
 DateTime now=rtc.now();
 showMessage(msg,"Access Denied","At "+getTimeStr(now));
 delay(2500);
 digitalWrite(RED_LED,LOW);
 readyScreen();
}

void checkRFID(String card){
 int total=sizeof(students)/sizeof(students[0]);
 for(int i=0;i<total;i++){
  if(card==students[i].rfid){ attendanceSuccess(i,"RFID"); return; }
 }
 attendanceFailed("INVALID RFID");
}

void checkFingerprint(int fid){
 int total=sizeof(students)/sizeof(students[0]);
 for(int i=0;i<total;i++){
  if(fid==students[i].fingerID){ attendanceSuccess(i,"FINGER"); return; }
 }
 attendanceFailed("UNKNOWN FINGER");
}

void setup(){
 Serial.begin(115200);
 pinMode(GREEN_LED,OUTPUT);
 pinMode(RED_LED,OUTPUT);
 pinMode(BUZZER,OUTPUT);
 Wire.begin(21,22);

 if(!display.begin(SSD1306_SWITCHCAPVCC,0x3C)) while(1);
 if(!rtc.begin()){ showMessage("RTC FAILED"); while(1); }

 if(!rtc.isrunning()){
   Serial.println("RTC not running, setting to compile time");
   rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
 }

 if(!SD.begin(SD_CS)){ showMessage("SD FAILED"); while(1); }

 successBeep();
 readyScreen();

 Serial.println("Commands:");
 Serial.println("RFID:12345678");
 Serial.println("RFID:87654321");
 Serial.println("FP:1");
 Serial.println("FP:2");
}

void loop(){
 if(Serial.available()){
  String input=Serial.readStringUntil('\n');
  input.trim();

  if(input.startsWith("RFID:")){
    input.remove(0,5);
    checkRFID(input);
  } else if(input.startsWith("FP:")){
    input.remove(0,3);
    checkFingerprint(input.toInt());
  }
 }

 // Live clock refresh — only when idle, non-blocking
 if(idleScreen && millis()-lastClockUpdate>=1000){
   lastClockUpdate=millis();
   readyScreen();
 }
}