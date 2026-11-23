#include <Arduino.h>
#include "motor_mix.h"

MotorOutput MotorMixer::calculate(
    const MovementCommand& command,
    int rearPower,
    int bowPower)
{
    MotorOutput motors = {};

    const int PWM_NEUTRAL = 1500;
    const int PWM_MIN = 1200;
    const int PWM_MAX = 1800;

    const int BOW_MIN = 1400;
    const int BOW_MAX = 1600;

    // All motors neutral
    motors.rearLeft = PWM_NEUTRAL;
    motors.rearRight = PWM_NEUTRAL;
    motors.bowLeft = PWM_NEUTRAL;
    motors.bowRight = PWM_NEUTRAL;

    // Forward
    if (command.surge > 0)
    {
        motors.rearLeft = PWM_NEUTRAL + rearPower;
        motors.rearRight = PWM_NEUTRAL + rearPower;
    }

    // Backward
    else if (command.surge < 0)
    {
        motors.rearLeft = PWM_NEUTRAL - rearPower;
        motors.rearRight = PWM_NEUTRAL - rearPower;
    }

    // Rotate left
    if (command.yaw > 0)
    {
        motors.rearLeft = PWM_NEUTRAL - rearPower;
        motors.rearRight = PWM_NEUTRAL + rearPower;

        motors.bowLeft = PWM_NEUTRAL - bowPower;
        motors.bowRight = PWM_NEUTRAL - bowPower;
    }

    // Rotate right
    else if (command.yaw < 0)
    {
        motors.rearLeft = PWM_NEUTRAL + rearPower;
        motors.rearRight = PWM_NEUTRAL - rearPower;

        motors.bowLeft = PWM_NEUTRAL + bowPower;
        motors.bowRight = PWM_NEUTRAL + bowPower;
    }

    // Limit PWM values
    motors.rearLeft = constrain(motors.rearLeft, PWM_MIN, PWM_MAX);
    motors.rearRight = constrain(motors.rearRight, PWM_MIN, PWM_MAX);

    motors.bowLeft = constrain(motors.bowLeft, BOW_MIN, BOW_MAX);
    motors.bowRight = constrain(motors.bowRight, BOW_MIN, BOW_MAX);

    return motors;
}