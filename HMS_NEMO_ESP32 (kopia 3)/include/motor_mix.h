#ifndef MOTOR_MIX_H
#define MOTOR_MIX_H

#include "motor_command.h"

struct MotorOutput
{
    float rearLeft;
    float rearRight;
    float bowLeft;
    float bowRight;
};

class MotorMixer
{
public:
    MotorOutput calculate(
        const MovementCommand& command,
        int rearPower,
        int bowPower
    );
};

#endif