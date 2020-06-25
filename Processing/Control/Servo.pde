// Class
//
//

class Servo{

  private float rotation;
  private float x = 0;
  private float y = 0;

  private float size = 100;

  Servo(float _x, float _y){
    x = _x;
    y = _y;
  }

  void draw(){
    // Open transform matrix
    pushMatrix();

    strokeWeight(1);
    translate(x - 0.5f * size, y - 0.5f * size);

    // Background
    fill(155);
    rect(0 , 0, 100, 100);

    // Round as in the sketch of the artist
    noFill();
    stroke(0);
    ellipse(0, 0, 100, 100);

    // needle turning as the servo turns
    pushMatrix();
    rotate(radians(rotation));
    line(-50, 0, 50, 0);
    popMatrix();

    // Roataion value as text
    fill(255);
    textAlign(CENTER, CENTER);
    text(nf(int(rotation), 3, 0) + " °", 0, 0);

    popMatrix();
    // Close transform matrix

  }

  void setRotation(float _rotationInDegrees){
      rotation = _rotationInDegrees;
  }

  String toString(){
    return "x:" + str(x) + " y:" + str(y) + " rot:" + str(rotation);
  }
}
