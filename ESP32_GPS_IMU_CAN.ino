
#include <Wire.h> 
#include <SparkFun_u-blox_GNSS_v3.h> // Official SparkFun GPS library (v3)
#include <Adafruit_Sensor.h> 
#include <Adafruit_BNO055.h>          // Official BNO055 IMU library
#include <utility/imumaths.h> 
#include <driver/twai.h>              // CAN Bus (TWAI) driver for ESP32-S3

SFE_UBLOX_GNSS myGNSS; 
Adafruit_BNO055 myIMU = Adafruit_BNO055(55, 0x28); 

unsigned long lastTime = 0; 

// Global variables to store sensor data
float orientacionX = 0;
float orientacionY = 0;
float orientacionZ = 0;
long latitud = 0;
long longitud = 0;

void setup() { 
  Serial.begin(115200); 
  while (!Serial); 

  // 1. Start the shared I2C bus
  Wire.begin(20, 21);  
  delay(2000); // Wait for the sensors to become stable

  // 2. Start the SparkFun GPS
  if (myGNSS.begin() == false) { 
    Serial.println("GPS NEO-M9N not found! Check the breadboard."); 
    while (1); 
  } 
  myGNSS.setI2COutput(COM_TYPE_UBX); 
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT); 

  // 3. Start the Adafruit BNO055 orientation sensor
  if (!myIMU.begin()) { 
    Serial.println("BNO055 sensor not found! Check the breadboard."); 
    while (1); 
  } 
   
  // 4. Set up CAN Bus (TWAI) on GPIO pins 4 and 5 (500 kbps)
  twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT((gpio_num_t)4, (gpio_num_t)5, TWAI_MODE_NORMAL);
  twai_timing_config_t t_config = TWAI_TIMING_CONFIG_500KBITS();
  twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

  // Install and start the CAN driver
  if (twai_driver_install(&g_config, &t_config, &f_config) == ESP_OK) {
    Serial.println("CAN (TWAI) driver installed successfully.");
  }
  if (twai_start() == ESP_OK) {
    Serial.println("CAN Bus started successfully.");
  }

  Serial.println("System initialized with I2C and CAN Bus!"); 
} 

void loop() { 
  // Read the BNO055 orientation continuously
  sensors_event_t event; 
  myIMU.getEvent(&event); 
  orientacionX = event.orientation.x;
  orientacionY = event.orientation.y;
  orientacionZ = event.orientation.z;

  // Print sensor data to the Serial Monitor for testing
  Serial.print("IMU -> X:"); Serial.print(orientacionX);
  Serial.print(" Y:"); Serial.print(orientacionY);
  Serial.print(" Z:"); Serial.print(orientacionZ); 

  // Read GPS data every 1 second
  if (millis() - lastTime > 1000) { 
    lastTime = millis(); 
    latitud = myGNSS.getLatitude(); 
    longitud = myGNSS.getLongitude(); 
     
    Serial.print(" | GPS -> Lat: "); Serial.print(latitud / 10000000.0, 6);
    Serial.print(" Long: "); Serial.println(longitud / 10000000.0, 6); // <-- FIXED HERE
    
    // --- SEND DATA OVER CAN BUS ---
    twai_message_t tx_msg;
    tx_msg.identifier = 0x100;   // Telemetry message ID
    tx_msg.extd = 0;             // Standard CAN ID
    tx_msg.data_length_code = 8; // Total of 8 data bytes

    // Split latitude (4 bytes) into positions 0, 1, 2, 3
    tx_msg.data[0] = (latitud >> 24) & 0xFF;
    tx_msg.data[1] = (latitud >> 16) & 0xFF;
    tx_msg.data[2] = (latitud >> 8) & 0xFF;
    tx_msg.data[3] = latitud & 0xFF;

    // Split longitude (4 bytes) into positions 4, 5, 6, 7
    tx_msg.data[4] = (longitud >> 24) & 0xFF;
    tx_msg.data[5] = (longitud >> 16) & 0xFF;
    tx_msg.data[6] = (longitud >> 8) & 0xFF;
    tx_msg.data[7] = longitud & 0xFF;

    // Send the message to the CAN bus
    if (twai_transmit(&tx_msg, pdMS_TO_TICKS(10)) == ESP_OK) {
      Serial.println(" -> [CAN] GPS coordinates sent.");
    } else {
      Serial.println(" -> [CAN] Error sending data.");
    }

  } else { 
    Serial.println(); 
  } 

  delay(100); 
}
