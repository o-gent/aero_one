#include <Servo.h>
Servo ch1;
Servo ch2;
Servo ch3;
Servo ch4;
Servo ch5;

// variables associated with serial processing
String incoming;
char serial_byte;

// arrays to store incoming servo commands as well as reciever vales
int target[6] = {0};
int reciever[6] = {0};

// PPM related variables 
unsigned long int ppm_current,ppm_last,ppm_difference;
int ppm_temp[15],ch1[15],ch[7],i;


void setup() {
  Serial.begin(115200);
  
  // associate channels with pins
  ch1.attach(3);
  ch2.attach(5);
  ch3.attach(6);
  ch4.attach(9);
  ch5.attach(10);

  // assigning PPM interrupt
  pinMode(2, INPUT_PULLUP); // enabling interrupt at pin 2
  attachInterrupt(digitalPinToInterrupt(2), read_me, FALLING);

}


void loop() {
  sync();
  read_rc();
}




void sync() {
  // resets incoming string
  incoming = "";
  // if there is a message then read
  while (Serial.available() > 0) {
    serial_byte = Serial.read();  // gets one byte from serial buffer
    incoming += serial_byte;      // add that byte to current message
    if(z == '\n'){
      // if end of current 'packet'
      
      // convert and store message in int array
      for(int i=0; i<6; i++){
        target[i] = getValue(incoming, ',', i).toInt();
      }
      // send RECIEVER values
      send();
      break; // stops reading once end of line reaches
    }
  }
}

void send() {
  // relay RC RECIEVER vales
  for(int i = 0; i<6 ; i++){
        Serial.print(reciever[i]); 
        Serial.print("@"); // separator byte
  }
  // terminate message
  Serial.print("\n");
}



void read_me() {
 // interrupt function
 // times PPM signal
 // gives channel values 0-1000 
 
  ppm_current = micros();   // store time of peak
  ppm_difference = ppm_current - ppm_last;      // calculate time in-between two peaks
  ppm_last = ppm_current;          // set last time
  
  ppm_temp[i] = ppm_difference;//storing 15 values in x array
  i++;            // increment array index    

  // can this be done another way?
  // copy values from the temporary array to another array after 15 readings
  if(i==15){
    for(int j=0;j<15;j++){
      ch1[j]=ppm_temp[j];
    }
    i=0;
  }
}

void read_rc() {
  int t,j,k=0;

  
  for(k = 14; k > -1; k--){
    if(ch1[k] > 3000){  //if time delay more than 3000, move onto next data packet
      j=k;
    }
  }
                  
  for(t = 1; t <= 6; t++){
    ch[t] = (ch1[t+j] - 1000);
  }   //assign 6 channel values after separation space
}


String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
      if (data.charAt(i) == separator || i == maxIndex) {
          found++;
          strIndex[0] = strIndex[1] + 1;
          strIndex[1] = (i == maxIndex) ? i+1 : i;
      }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
