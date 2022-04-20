// == Pinout ==
#define POTI_PIN A0  // Potentiometer of cylinder
#define DIRA_PIN 2   // Direction
#define PWMA_PIN 3   // Motor voltage

// == Constants ==
#define CYL_START_POS 30
#define CYL_END_POS 940
#define MIN_SPEED 30

// == State ==
bool cyl_moving = false;
bool cyl_direction = LOW;
float cyl_position;
int poti_state = 0;
float position_input = 0;

// == Setup ==
void setup() {
  pinMode(POTI_PIN, INPUT);
  pinMode(DIRA_PIN, OUTPUT);
  pinMode(PWMA_PIN, OUTPUT);

  // Enable serial
  Serial.begin(9600);

  // Get current cylinder position
  poti_state = analogRead(POTI_PIN);
  cyl_position = get_cylinder_pos_perc();
}

// Get voltage of potentiometer
float read_poti() {
  int n_meas = 10;
  int sum = 0;
  for (int i = 0; i < n_meas; i++) {
    sum += analogRead(POTI_PIN);
  }
  poti_state = poti_state * 0.1 + (sum / n_meas) * 0.9;
  return poti_state;
}

// Get current cylinder position in percent
float get_cylinder_pos_perc() {
  return (read_poti() - CYL_START_POS) / float(CYL_END_POS - CYL_START_POS) * 100.0;
}

// Stop cylinder movement
void stop_cylinder() {
  analogWrite(PWMA_PIN, 0);
  cyl_moving = false;
  Serial.println("DONE");
}

// == Loop ==
void loop() {
  // Only accept new position if cylinder is not moving
  while (Serial.available() > 0 && !cyl_moving) {
    String command_input = Serial.readStringUntil('\n');

    if (command_input.equals(String("GET"))) {
      Serial.println( get_cylinder_pos_perc() );
      break;
    } else if (command_input.substring(0, 2).equals("Z=")) {
      position_input = command_input.substring(2).toFloat();
    } else {
      break;
    }

    // Read position in percent, clip if necessary
    if (position_input > 100) {
      position_input = 100;
    } else if (position_input < 0) {
      position_input = 0;
    }

    // Get current cylinder position
    cyl_position = get_cylinder_pos_perc();

    // Determine and set movement direction
    if (position_input >= cyl_position) {
      cyl_direction = true;
    } else {
      cyl_direction = false;
    }
    digitalWrite(DIRA_PIN, cyl_direction);

    // Start moving cylinder
    analogWrite(PWMA_PIN, 255);
    cyl_moving = true;
  }

  if (cyl_moving) {
    // Check cylinder position
    float cyl_position = get_cylinder_pos_perc();

    // Adjust movement speed when close to desired position
    float pos_diff = abs(cyl_position - position_input);
    if (pos_diff < 20) {
      analogWrite(PWMA_PIN, int(MIN_SPEED + (255 - MIN_SPEED) * (1 - exp(-pos_diff / 4.0))));
    }

    // Stop conditions
    if (cyl_direction) {
      if (cyl_position >= position_input) {
        stop_cylinder();
      }
    } else {
      if (cyl_position <= position_input) {
        stop_cylinder();
      }
    }
  }
}
