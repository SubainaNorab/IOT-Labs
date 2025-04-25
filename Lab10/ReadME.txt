*** Task 1 ***:
We are sending data to ThingSpeak using MQTT (a lightweight IoT messaging protocol) and Waits for 20 seconds, then repeats (because of free account)

*** Task 2 ***
In this using multicore.Core 0 handles the sensor reading and sending data to ThingSpeak.
Core 1 runs the OLED display loop and keeps showing updated values.

thread->openmp
topic-> for communication (who to publish)
lock->for enforcement synchronization