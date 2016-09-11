int val[400];
int cnt = 0;
int res = 0;
int outPin = 8;
int sensorPin = A0;
int newres = 0;
int cnt_real = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(outPin, OUTPUT);
  digitalWrite(8, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (cnt < 400){
    newres = analogRead(A0);
    if (newres > 500) {
      res = res + newres;
      cnt_real++;
    }
    delay(5);
    cnt++;
  }

  if (cnt == 400){
    res = res / cnt_real;
    Serial.println(res);  
    cnt = 0;
    cnt_real=0;
    res = 0;
    delay(5);
  }  
  
}
