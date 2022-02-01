#include <SoftwareSerial.h> 
SoftwareSerial MyBlue(2, 3); // RX | TX 
void setup() 
{   
 Serial.begin(9600); 
 MyBlue.begin(9600); 
} 

void loop() {

  // read from port 1, send to port 0:

  if (MyBlue.available()) {

    char inByte = MyBlue.read();

    Serial.println(inByte);

    delay(50);
    
  }

}
