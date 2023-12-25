import processing.serial.*;

Serial myPort; // Create a serial object
boolean reading = true;

int rows = 20; // Number of rows of points
int cols = 20; // Number of columns of points

float[][] points; // 2D array to store points in 3D space
float angleY = 0; // Initial angle for rotation around Y-axis

int posX = 0;
int posY = 0;

void setup() {
  size(800, 600, P3D); // Set window size and 3D renderer
  points = new float[rows][cols]; // Initialize the 2D array
  background(0); // Clear the background
  myPort = new Serial(this, Serial.list()[0], 9600); // Open the serial port
  
  posX = -width / 2 + width / cols / 2;
  posY = -height / 2 + height / rows / 2;
  
  for (int y = 0; y < rows; y++) {
    for (int x = 0; x < cols; x++) {
      points[y][x] = 0; // Initialize points with zero value
    }
  }
}

void draw() {
  if (reading){
  
  if(myPort.available() > 0) { // If data is available in the serial buffer
    String val = myPort.readStringUntil('\n'); // Read the data until newline character
    if (val != null) {
      val = trim(val); // Remove leading/trailing whitespace
      
      if (val.equals("done")) // Compare strings using .equals()
        reading = false;
      else {
        int sensorValue = int(val); // Convert the received string to an integer
        println("Received: " + sensorValue); // Print the received value
        
        // Update the points array with new data from the serial port
        points[posY / (height / rows)][posX / (width / cols)] = sensorValue; // Map sensor value to Z-coordinate
        
        posX += width / cols; // Move to the next X position
        if (posX >= width - width / cols / 2) { // If reached the end of the row
          posX = -width / 2 + width / cols / 2; // Reset X position
          posY += height / rows; // Move to the next Y position
          if (posY >= height - height / rows / 2) // If reached the bottom
            reading = false; // Stop reading
        }
      }
    }
  }
  }
  
  else {
  lights(); // Enable lighting
  translate(width / 2, height / 2); // Translate to the middle of the screen
  rotateY(angleY); // Rotate around Y-axis
  
  // Draw points in 3D space
  for (int y = 0; y < rows; y++) {
    for (int x = 0; x < cols; x++) {
      float zPos = points[y][x];
      
      // Adjust stroke weight based on Z-coordinate value
      float strokeWeightValue = map(zPos, 5, 150, 1, 5); // Map Z-coordinate to stroke weight range
      
      stroke(255); // Set stroke color
      strokeWeight(strokeWeightValue); // Set stroke weight
      
      point(x * (width / cols) - width / 2 + width / cols / 2,
            y * (height / rows) - height / 2 + height / rows / 2,
            zPos); // Draw the point in 3D space
    }
  }
  
  angleY += 0.01; // Increment angle for rotation
}
}
