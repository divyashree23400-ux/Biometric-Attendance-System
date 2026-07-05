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

void readyScreen(){ showMessage("BIOMETRIC","System Ready","Scan RFID / FP"); }

void attendanceSuccess(int i,String method){
 digitalWrite(GREEN_LED,HIGH);
 successBeep();
 showMessage(method+" VERIFIED",students[i].name,"Attendance Marked");
 delay(2500);
 digitalWrite(GREEN_LED,LOW);
 readyScreen();
}

void attendanceFailed(String msg){
 digitalWrite(RED_LED,HIGH);
 errorBeep();
 showMessage(msg,"Access Denied");
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
}
