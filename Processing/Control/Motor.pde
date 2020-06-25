// Motor control
//
// Get a speed information, send into motors trough O2C
//

class Motor{

  private float speed = 0.0f;
  private float x = 0;
  private float y = 0;

  private float localRot = 97;

  private float size = 50;

  Motor(float _x, float _y){
    x = _x;
    y = _y;
  }

  void draw(){
    // Open transform matrix
    pushMatrix();

    strokeWeight(1);
    translate(x - 0.5f * size, y - 0.5f * size);

    // Background rect
    // Speed = 0 -> Green
    // Speed = 1 -> Red
    fill(255 * speed, 255 * (1.0f - speed), 0);
    stroke(255);
    rect(0, 0, size, size);

    // Speed value as number
    fill(255);
    textAlign(CENTER, CENTER);
    text(nf(speed, 1, 3), 0, 0);

    // A needle which turns faster and faster relative to speed
    pushMatrix();
    fill(0, 255, 0);
    localRot += (10.0f * speed);
    rotate(radians(localRot));
    line(0, 0, 0.5 * size, 0);
    popMatrix();

    popMatrix();
    // Close transform matrix

  }

  void setSpeed(float _speed){
    speed = _speed;
  }

}
