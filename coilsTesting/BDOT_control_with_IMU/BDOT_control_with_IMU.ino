/**@file BDOT_control_with_IMU.ino
 * 
 * @brief Code to run on the Arduino Nano that controls the ADCS coils testing board.
 *  Involves getting IMU data, running BDOT, and outputting the correct current from
 *  the coils test board.
 */
#include "bdot_control.h"
#include "ICM20948.h"
#include "AD520X.h"

#define XCOILOUTPUT 0
#define YCOILOUTPUT 1
#define ZCOILOUTPUT 2

#define XCOILSIGNPIN 2 //to be verified
#define YCOILSIGNPIN 3 //
#define ZCOILSIGNPIN 4 //

ICM20948 IMU(Wire, 0x69); // an ICM20948 object with the ICM-20948 sensor on I2C bus 0 with address 0x69
AD5204 POT(10, 255, 255, 8, 9);  //Digital Potentiometer SW SPI (select, reset, shutdown, data, clock)
int status;

bool dataAvailable = false;
int dataTime = 0;
int lastDataTime = 0;

double coils_current[3];
double magnetic_field[3];
double angular_velocity[3];

const double coils_resistance = 31.6455696; //5V max / 0.158A max = R? TODO change


void setup() {
  // serial to display data
  Serial.begin(115200);
  while(!Serial) {}

  // start communication with IMU 
  status = IMU.begin();
  Serial.print("status = ");
  Serial.println(status);
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }

  IMU.configAccel(ICM20948::ACCEL_RANGE_16G, ICM20948::ACCEL_DLPF_BANDWIDTH_50HZ);
  IMU.configGyro(ICM20948::GYRO_RANGE_2000DPS, ICM20948::GYRO_DLPF_BANDWIDTH_51HZ);
  IMU.setGyroSrd(113); // Output data rate is 1125/(1 + srd) Hz
  IMU.setAccelSrd(113);
  IMU.enableDataReadyInterrupt();
  pinMode(1, INPUT);
  attachInterrupt(1, imuReady, RISING);

  POT.begin(0);
}

void imuReady() {
  dataTime = micros();
  dataAvailable = true;
}

void loop() {
  if (dataAvailable) {
    dataAvailable = false;
    int timeDiff = dataTime - lastDataTime;
    lastDataTime = dataTime;
    IMU.readSensor();
    
    // display the data
    Serial.print(dataTime);
    Serial.print("\t");
    Serial.print(timeDiff);
    Serial.print("\t");
    Serial.print(IMU.getAccelX_mss(),6);
    Serial.print("\t");
    Serial.print(IMU.getAccelY_mss(),6);
    Serial.print("\t");
    Serial.print(IMU.getAccelZ_mss(),6);
    Serial.print("\t");
    Serial.print(IMU.getGyroX_rads(),6);
    Serial.print("\t");
    Serial.print(IMU.getGyroY_rads(),6);
    Serial.print("\t");
    Serial.print(IMU.getGyroZ_rads(),6);
    Serial.print("\t");
    Serial.print(IMU.getMagX_uT(),6);
    Serial.print("\t");
    Serial.print(IMU.getMagY_uT(),6);
    Serial.print("\t");
    Serial.print(IMU.getMagZ_uT(),6);
    Serial.print("\t");
    Serial.println(IMU.getTemperature_C(),6);

    magnetic_field[0] = IMU.getMagX_uT();
    magnetic_field[1] = IMU.getMagY_uT();
    magnetic_field[2] = IMU.getMagZ_uT();

    angular_velocity[0] = IMU.getGyroX_rads();
    angular_velocity[1] = IMU.getGyroY_rads();
    angular_velocity[2] = IMU.getGyroZ_rads();

    bdot_control(coils_current, magnetic_field, angular_velocity);

    Serial.print("X Coil Current: ");
    Serial.println(coils_current[0]);
    Serial.print("Y Coil Current: ");
    Serial.println(coils_current[1]);
    Serial.print("Z Coil Current: ");
    Serial.println(coils_current[2]);

    double x_coil_voltage = coils_resistance * coils_current[0];
    double y_coil_voltage = coils_resistance * coils_current[1];
    double z_coil_voltage = coils_resistance * coils_current[2];

    digitalWrite(XCOILSIGNPIN, x_coil_voltage > 0);
    digitalWrite(YCOILSIGNPIN, y_coil_voltage > 0);
    digitalWrite(ZCOILSIGNPIN, z_coil_voltage > 0);

    POT.setPercentage(XCOILOUTPUT, abs(x_coil_voltage)/5.0);
    POT.setPercentage(YCOILOUTPUT, abs(y_coil_voltage)/5.0);
    POT.setPercentage(ZCOILOUTPUT, abs(z_coil_voltage)/5.0);
  }
}
