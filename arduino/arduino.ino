
/*
 * This program reads an RC PPM signal from PIN 2 into "ch" array
 * Accepts incoming servo positions on SERIAL into "target" array
 * Mixes channels for ailerons
 * Outputs servo positions to pins 3, 5, 6, 9, 10
 * 
 */

#include <Servo.h>
Servo ch1;
Servo ch2;
Servo ch3;
Servo ch4;
Servo ch5;


// Serial related
String incoming;
char serial_byte;

// arrays to store incoming servo commands as well as reciever vales
int target[6] = {0};
int reciever[6] = {0};
int mix[6] = {0};

// PPM related variables 
int ppm_temp[15], ch[15];
unsigned long int ppm_current,ppm_last,ppm_difference;
int interupt_index = 0;


void setup() {
  //incoming.reserve(25); //preallocate memory for string
  
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(57600);
  
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
  
  if (reciever[5] > 500) {
    // enable serial inputs to be written as outputs
    digitalWrite(LED_BUILTIN, HIGH); // sets arduino LED to on
    mix_output(target);
  }
  
  else {
    // write reciever values to outputs
    digitalWrite(LED_BUILTIN, LOW);
    mix_output(reciever);
  }
  
}

void mix_output(int input[6]){
  
  for (int i = 0; i <=5; i++) {
    mix[i] = input[i];
  }
   
  /*
  * MIXES - CHECK ORDER
  */

  // AILERON sensitivity
  //mix[0] = float((mix[0] - 500)) * mix[4]/1000;
  //mix[0] = mix[0] + 500;
  
  // FINAL - AILERONS - ch5 is inverse of ch1
  mix[4] = abs(mix[0] - 1000);
   
  ch1.write(map(mix[0], 0, 1000, 0, 180));
  ch2.write(map(mix[1], 0, 1000, 0, 180));
  ch3.write(map(mix[2], 0, 1000, 0, 180));
  ch4.write(map(mix[3], 0, 1000, 0, 180));
  ch5.write(map(mix[4], 0, 1000, 0, 180));
}


void sync() {
  /*
   * Gets target values from SERIAL
   */
  
  // resets incoming string
  incoming = "";
  
  // if there is a message then read
  if (Serial.available() > 0) {
    // then wait for message to complete
    while (true){
      if (Serial.available() > 0) {
        serial_byte = Serial.read(); // gets one byte from serial buffer
        incoming.concat(serial_byte);    // add that byte to current message
        
        if (serial_byte == '\n') { // if end of current 'packet'
          // convert and store message in int array
          
          for(int i = 0; i <= 5; i++){
            target[i] = getValue(incoming, ',', i).toInt();
          }
          
          // send RECIEVER values
          send();
          break; // stops reading once end of line reaches
        }
      }
    }
  }
}

void send() {
  /*
   * send channel values from RC receiver 
   */
  
  // relay RC RECIEVER vales
  for (int i = 0; i <= 5 ; i++) {
        Serial.print(reciever[i]); 
        Serial.print("@"); // separator byte
  }
  
  // terminate message
  Serial.print("\n");
}



void read_me() {
 /* 
  * interrupt function
  * times PPM signal
  * gives channel values 0-1000 
  */
 
  ppm_current = micros();   // store time of peak
  ppm_difference = ppm_current - ppm_last;      // calculate time in-between two peaks
  ppm_last = ppm_current;          // set last time
  
  ppm_temp[interupt_index] = ppm_difference;//storing 15 values in x array
  interupt_index++;            // increment array index    

  // can this be done another way?
  // copy values from the temporary array to another array after 15 readings
  if (interupt_index == 15) {
    for (int j = 0; j < 15; j++) {
      ch[j] = ppm_temp[j];
    }
    interupt_index = 0;
  }
}

void read_rc() {
  /*
   * fetches PPM values from tempory array changed by read_me()
   */
  int interval_index;

  for (int i = 14; i >= 0; i--) {
    if(ch[i] > 3000){  //if time delay more than 3000, move onto next data packet
      interval_index = i + 1; 
    }
  }
                  
  for (int i = 0; i <= 5; i++) {
    reciever[i] = (ch[ i+ interval_index ] - 1000);
  }   //assign 6 channel values after separation space
}


String getValue(String data, char separator, int index) {
  /*
   * allows strings to be read like arrays using seperator chars
   */
  
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
