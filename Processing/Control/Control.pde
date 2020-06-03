/*
Processing sketch to control Felicie Estienne d'Orves installation

- Servos motors
- DC motors

This sketch receives OSC and send I2C on control cards

Author : Studio Albert (Sébastien Albert)
Version : 0.0.1
Date : 2020.06.02

*/

import oscP5.*;
import netP5.*;

OscP5 oscP5;

// Note the HashMap's "key" is a String and "value" is an Integer
HashMap<String,Servo> allServos = new HashMap<String,Servo>();
HashMap<String,Motor> allMotors = new HashMap<String,Motor>();

/* -------------------------------------
SETUPS
------------------------------------- */
void setup(){
  size(800, 1150);
  rectMode(CENTER);

  setupServos();
  setupMotors();
  setupOSC();

}

void setupServos(){
  // Putting key-value pairs in the Has800
  float rowHeight = 0.0f;
  // First row
  rowHeight = 200;
  allServos.put("B2", new Servo(200, rowHeight));
  allServos.put("C2", new Servo(300, rowHeight));
  allServos.put("F2", new Servo(600, rowHeight));
  allServos.put("G2", new Servo(700, rowHeight));
  // Second row
  rowHeight = 300;
  allServos.put("B3", new Servo(200, rowHeight));
  allServos.put("C3", new Servo(300, rowHeight));
  allServos.put("D3", new Servo(400, rowHeight));
  allServos.put("E3", new Servo(500, rowHeight));
  allServos.put("F3", new Servo(600, rowHeight));
  allServos.put("G3", new Servo(700, rowHeight));
  // Third row
  rowHeight = 400;
  allServos.put("A4", new Servo(100, rowHeight));
  allServos.put("B4", new Servo(200, rowHeight));
  allServos.put("C4", new Servo(300, rowHeight));
  allServos.put("D4", new Servo(400, rowHeight));
  allServos.put("E4", new Servo(500, rowHeight));
  allServos.put("F4", new Servo(600, rowHeight));
  allServos.put("G4", new Servo(700, rowHeight));
  allServos.put("H4", new Servo(800, rowHeight));
  // Fourth row
  rowHeight = 500;
  allServos.put("A5", new Servo(100, rowHeight));
  allServos.put("B5", new Servo(200, rowHeight));
  allServos.put("C5", new Servo(300, rowHeight));
  allServos.put("D5", new Servo(400, rowHeight));
  allServos.put("E5", new Servo(500, rowHeight));
  allServos.put("F5", new Servo(600, rowHeight));
  allServos.put("G5", new Servo(700, rowHeight));
  allServos.put("H5", new Servo(800, rowHeight));
  // Fifth row
  rowHeight = 600;
  allServos.put("B6", new Servo(200, rowHeight));
  allServos.put("C6", new Servo(300, rowHeight));
  allServos.put("D6", new Servo(400, rowHeight));
  allServos.put("E6", new Servo(500, rowHeight));
  allServos.put("F6", new Servo(600, rowHeight));
  allServos.put("G6", new Servo(700, rowHeight));
  // Sixth row
  rowHeight = 700;
  allServos.put("B7", new Servo(200, rowHeight));
  allServos.put("C7", new Servo(300, rowHeight));
  allServos.put("D7", new Servo(400, rowHeight));
  allServos.put("E7", new Servo(500, rowHeight));
  allServos.put("F7", new Servo(600, rowHeight));
  allServos.put("G7", new Servo(700, rowHeight));
  // Sixth row
  rowHeight = 800;
  allServos.put("B8", new Servo(400, rowHeight));
  allServos.put("C8", new Servo(500, rowHeight));
}

void setupMotors(){

  int stepMotor = 75;
  int idxMotor = 1;
  int rowHeight = 900;

  // First row of motor display
  allMotors.put("M01", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M02", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M03", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M04", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M05", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M06", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M07", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M08", new Motor(idxMotor++ * stepMotor, rowHeight));

  // Second rowHeight
  idxMotor = 1;
  rowHeight = 950;
  allMotors.put("M09", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M10", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M11", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M12", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M13", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M14", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M15", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M16", new Motor(idxMotor++ * stepMotor, rowHeight));
  allMotors.put("M17", new Motor(idxMotor++ * stepMotor, rowHeight));

}

void setupOSC(){
  /* start oscP5, listening for incomin800s at port 12000 */
  oscP5 = new OscP5(this,12000);

}

float exampleRotation = 0;

/* ------------------------------------800
DRAW
------------------------------------- */
void draw(){

  background(130);

  // Draw Servos --------------------------------------------
  for (Servo myServo : allServos.values()) {
    myServo.draw();
  }

  // Draw Servos --------------------------------------------
  for (Motor myMotor : allMotors.values()) {
    myMotor.draw();
  }


  noFill();
  strokeWeight(2);
  stroke(0);
  ellipse(400, 400, 800, 800);

}

/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage theOscMessage) {

    if(theOscMessage.checkTypetag("sf")) {

      // SERVO ---------------------------------------------------------------------
      if(theOscMessage.checkAddrPattern("/control/servo")==true){
        updateServo(theOscMessage);
        return;
      }

      // Motor ---------------------------------------------------------------------
      if(theOscMessage.checkAddrPattern("/control/motor")==true){
        updateMotor(theOscMessage);
        return;
      }

    }else{
      println("Arguments type not ordened. TypeTag : "+ theOscMessage.typetag());
    }

    println("### received an osc message. with no match address pattern "+
    theOscMessage.addrPattern()+" typetag "+ theOscMessage.typetag());

}

/* UPDATE THE SERVO information */
void updateServo(OscMessage theOscMessage){

  println("Get an order for servos");

  String servoKey = theOscMessage.get(0).stringValue();
  float rotation = theOscMessage.get(1).floatValue();  // get the first osc argument

  // Check if the servo is registred ------------------------------
  if(allServos.containsKey(servoKey)){

    Servo servoDriven = allServos.get(servoKey);
    servoDriven.setRotation(rotation);

  }else{
    println("No servo match with that key : " + servoKey);
  }
}

/* UPDATE THE Motor information */
void updateMotor(OscMessage theOscMessage){

  println("Get an order for motor");

  String motorKey = theOscMessage.get(0).stringValue();
  float speed = theOscMessage.get(1).floatValue();  // get the first osc argument

  // Check if the servo is registred ------------------------------
  if(allMotors.containsKey(motorKey)){

    Motor motorDriven = allMotors.get(motorKey);
    motorDriven.setSpeed(speed);

  }else{
    println("No servo match with that key : " + motorKey);
  }

}
