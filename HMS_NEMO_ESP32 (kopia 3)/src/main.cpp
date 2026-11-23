#include <Arduino.h>

#include "motor_command.h"
#include "motor_mix.h"

// =====================================
// HMS NEMO - ESP32-S3 LEDC CONTROLLER
// =====================================

// GPIO pins
const int REAR_LEFT_PIN  = 4;
const int REAR_RIGHT_PIN = 5;
const int BOW_LEFT_PIN   = 11;
const int BOW_RIGHT_PIN  = 13;

// LEDC channels
const int REAR_LEFT_CHANNEL  = 0;
const int REAR_RIGHT_CHANNEL = 1;
const int BOW_LEFT_CHANNEL   = 2;
const int BOW_RIGHT_CHANNEL  = 3;

// PWM configuration
const int PWM_FREQUENCY = 50;
const int PWM_RESOLUTION = 14;

const int PWM_MIN = 1200;
const int PWM_MAX = 1800;
const int PWM_NEUTRAL = 1500;

// Motor control
ManualController controller;
MotorMixer mixer;

// Gradual PWM control
const int REAR_START_POWER = 100;
const int BOW_START_POWER = 10;

const int REAR_STEP = 20;
const int BOW_STEP = 10;

const int REAR_MAX_POWER = 300;
const int BOW_MAX_POWER = 100;

const unsigned long STEP_INTERVAL_MS = 1000;

// Communication safety
const unsigned long TIMEOUT_MS = 1500;

int rearPower = 0;
int bowPower = 0;

bool commandActive = false;
bool rampingDown = false;

char activeKey = 'x';

unsigned long lastStepTime = 0;
unsigned long lastCommandTime = 0;

bool pwmReady = false;

// =====================================
// PWM CONVERSION
// =====================================

uint32_t microsecondsToDuty(int microseconds)
{
    const uint32_t maxDuty = (1UL << PWM_RESOLUTION);

    return (uint32_t)microseconds * maxDuty
           * PWM_FREQUENCY / 1000000UL;
}

// =====================================
// MOTOR FUNCTIONS
// =====================================

void setMotors(int RL, int RR, int BL, int B_R)
{
    RL = constrain(RL, PWM_MIN, PWM_MAX);
    RR = constrain(RR, PWM_MIN, PWM_MAX);
    BL = constrain(BL, 1400, 1600);
    B_R = constrain(BR, 1400, 1600);

    ledcWriteChannel(
        REAR_LEFT_CHANNEL,
        microsecondsToDuty(RL)
    );

    ledcWriteChannel(
        REAR_RIGHT_CHANNEL,
        microsecondsToDuty(RR)
    );

    ledcWriteChannel(
        BOW_LEFT_CHANNEL,
        microsecondsToDuty(BL)
    );

    ledcWriteChannel(
        BOW_RIGHT_CHANNEL,
        microsecondsToDuty(BR)
    );
}

void stopMotors()
{
    setMotors(
        PWM_NEUTRAL,
        PWM_NEUTRAL,
        PWM_NEUTRAL,
        PWM_NEUTRAL
    );
}

// =====================================
// SAFETY STOP
// =====================================

void emergencyStop()
{
    commandActive = false;
    rampingDown = false;

    rearPower = 0;
    bowPower = 0;

    activeKey = 'x';

    stopMotors();
}

// =====================================
// GRADUAL PWM CONTROL
// =====================================

void updateMotorPower()
{
    unsigned long currentTime = millis();

    if (currentTime - lastStepTime < STEP_INTERVAL_MS)
    {
        return;
    }

    lastStepTime = currentTime;

    if (commandActive)
    {
        rearPower = min(
            rearPower + REAR_STEP,
            REAR_MAX_POWER
        );

        bowPower = min(
            bowPower + BOW_STEP,
            BOW_MAX_POWER
        );
    }
    else if (rampingDown)
    {
        rearPower = max(
            rearPower - REAR_STEP,
            0
        );

        bowPower = max(
            bowPower - BOW_STEP,
            0
        );

        if (rearPower == 0 && bowPower == 0)
        {
            rampingDown = false;
            activeKey = 'x';
        }
    }
}

// =====================================
// HANDLE KEY COMMANDS
// =====================================

void handleCommand(String input)
{
    input.trim();
    input.toLowerCase();

    if (input == "x")
    {
        emergencyStop();
        return;
    }

    if (input == "r")
    {
        commandActive = false;
        rampingDown = true;
        lastStepTime = millis();
        return;
    }

    if (
        input == "w" ||
        input == "s" ||
        input == "a" ||
        input == "d"
    )
    {
        char newKey = input.charAt(0);

        if (!commandActive || activeKey != newKey)
        {
            rearPower = REAR_START_POWER;
            bowPower = BOW_START_POWER;

            activeKey = newKey;

            lastStepTime = millis();
        }

        commandActive = true;
        rampingDown = false;

        return;
    }

    // Heartbeat from keyboard program
    if (input == "h")
    {
        return;
    }

    emergencyStop();
    Serial.println("Invalid command");
}

// =====================================
// SETUP
// =====================================

void setup()
{
    Serial.begin(9600);

    bool ok1 = ledcAttachChannel(
        REAR_LEFT_PIN,
        PWM_FREQUENCY,
        PWM_RESOLUTION,
        REAR_LEFT_CHANNEL
    );

    bool ok2 = ledcAttachChannel(
        REAR_RIGHT_PIN,
        PWM_FREQUENCY,
        PWM_RESOLUTION,
        REAR_RIGHT_CHANNEL
    );

    bool ok3 = ledcAttachChannel(
        BOW_LEFT_PIN,
        PWM_FREQUENCY,
        PWM_RESOLUTION,
        BOW_LEFT_CHANNEL
    );

    bool ok4 = ledcAttachChannel(
        BOW_RIGHT_PIN,
        PWM_FREQUENCY,
        PWM_RESOLUTION,
        BOW_RIGHT_CHANNEL
    );

    if (!(ok1 && ok2 && ok3 && ok4))
    {
        Serial.println("ERROR: LEDC initialization failed!");
        return;
    }

    pwmReady = true;

    stopMotors();

    // ESC initialization
    delay(7000);

    lastCommandTime = millis();
    lastStepTime = millis();

    Serial.println("HMS NEMO LEDC Controller Ready!");

    Serial.println("W = Forward");
    Serial.println("S = Backward");
    Serial.println("A = Rotate Left");
    Serial.println("D = Rotate Right");
    Serial.println("R = Release");
    Serial.println("X = Emergency Stop");
}

// =====================================
// MAIN LOOP
// =====================================

void loop()
{
    if (!pwmReady)
    {
        return;
    }

    // Read serial commands
    if (Serial.available() > 0)
    {
        String input = Serial.readStringUntil('\n');

        handleCommand(input);

        lastCommandTime = millis();
    }

    // Communication timeout
    if (millis() - lastCommandTime > TIMEOUT_MS)
    {
        emergencyStop();
        return;
    }

    // Update gradual motor power
    updateMotorPower();

    // Calculate motor outputs
    MovementCommand command =
        controller.processInput(activeKey);

    MotorOutput motors =
        mixer.calculate(
            command,
            rearPower,
            bowPower
        );

    // Send PWM signals
    setMotors(
        motors.rearLeft,
        motors.rearRight,
        motors.bowLeft,
        motors.bowRight
    );
}