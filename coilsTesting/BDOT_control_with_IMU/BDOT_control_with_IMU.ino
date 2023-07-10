/**@file BDOT_control_with_IMU.ino
 * 
 * @brief Code to run on the Arduino Nano that controls the ADCS coils testing board.
 *  Involves getting IMU data, running BDOT, and outputting the correct current from
 *  the coils test board.
 */

#include "src/adcs_math/vector.h"
#include "src/bdot/bdot_control.h"
#include "src/imu/ICM20948.h"
#include "src/digital_potentiometer/AD520X.h"


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

vec3 coils_current;
vec3 magnetic_field;
vec3 angular_velocity;

const float coils_resistance = 31.6455696f; //5V max / 0.158A max = R? TODO change


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

	vec_set(
		IMU.getMagX_uT(),
		IMU.getMagY_uT(),
		IMU.getMagZ_uT(),
		&magnetic_field
	);

	vec_set(
		IMU.getGyroX_rads(),
		IMU.getGyroY_rads(),
		IMU.getGyroZ_rads(),
		&angular_velocity
	);


    bdot_control(magnetic_field, angular_velocity, &coils_current);

    Serial.print("X Coil Current: ");
    Serial.println(coils_current.x);
    Serial.print("Y Coil Current: ");
    Serial.println(coils_current.y);
    Serial.print("Z Coil Current: ");
    Serial.println(coils_current.z);

    double x_coil_voltage = coils_resistance * coils_current.x;
    double y_coil_voltage = coils_resistance * coils_current.y;
    double z_coil_voltage = coils_resistance * coils_current.z;

    digitalWrite(XCOILSIGNPIN, x_coil_voltage > 0);
    digitalWrite(YCOILSIGNPIN, y_coil_voltage > 0);
    digitalWrite(ZCOILSIGNPIN, z_coil_voltage > 0);

    POT.setPercentage(XCOILOUTPUT, fabs(x_coil_voltage)/5.0);
    POT.setPercentage(YCOILOUTPUT, fabs(y_coil_voltage)/5.0);
    POT.setPercentage(ZCOILOUTPUT, fabs(z_coil_voltage)/5.0);
  }
}
