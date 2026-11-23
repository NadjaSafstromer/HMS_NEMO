#ifndef MOTOR_COMMAND_H
#define MOTOR_COMMAND_H

struct MovementCommand
{
    float surge; // Fram/Bak
    float sway; // Sidor
    float yaw; // Rotation
};

class ManualController
{
public:
    MovementCommand processInput(char key);
};

#endif