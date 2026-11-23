#include "motor_command.h"
#include <cctype>

MovementCommand ManualController::processInput(char key)
{
    MovementCommand command = {0.0f, 0.0f, 0.0f};

    const float speed = 0.3f;

    switch (std::tolower(static_cast<unsigned char>(key)))
    {
        case 'w':
            command.surge = speed;
            break;

        case 's':
            command.surge = -speed;
            break;

        case 'a':
            command.yaw = speed;
            break;

        case 'd':
            command.yaw = -speed;
            break;

        case 'q':
            command.sway = speed;
            break;

        case 'e':
            command.sway = -speed;
            break;

        case 'x':
            break;
    }

    return command;
}