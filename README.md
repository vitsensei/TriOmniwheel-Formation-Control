# 3-OmniWheels-Rover-Platform
Summer research 2018-2019. Rover platform development for autonomous and multi agent system.

## Overview:
>The distributed system will contain multiple agents. Each agent can make its own decision. However, the four agents still need to communicate with each other about the velocity, the current position, the destination and the angle of the agent. This allows an agreement to be made to achieve the desired formation.

## Hardware setup:
Motor: 251RPM DC geared (43.7:1) motor w/ ecoder.

Encoder: 64 resolution => 2797 count per rotation.

Control board: Arduino Due for controlling, Arduino MKR1000 for WiFi communication.

## Example
### Simple case (user generated coordinate/path)
Real data feedback and put into simulation
![Alt Text](https://i.imgur.com/8nDaBDt.gif)

Real demo. Noticed how the position of the rovers and the feedback position is not entirely the same. Overtime, the system introduce more and more error. Since the system is self guidance, there's no correction during performance.
![Alt Text](https://i.imgur.com/Ef7aGyV.gif)

### Formation control without collision avoicedance
Generate path to form a triangle formation. Connected circle represent rover with radius, dash circle represent the safety distance (collision avoicedance is not implement in the GIF below).
![Alt Text](https://i.imgur.com/ODTWwnD.gifv)
