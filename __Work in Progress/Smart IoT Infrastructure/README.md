Project Title: Smart IoT Infrastructure
As the IoT continues to expand, the amount of data ingested with high velocity is growing at an alarming rate. It creates challenges for companies regarding storage, analysis, and visualization. 

In this project, we will build a fictitious pipeline network system called SmartPipeNet. SmartPipeNet aims to monitor pipeline flow and react to events along various branches to give production feedback, detect and reactively reduce loss, and avoid accidents.

The architecture shows that simulated sensor data is ingested from MQTT to Kafka.

A column store called HBase stores the Kafka data and analyzes it with Spark Streaming API. Finally, a Java-based custom dashboard is used to publish and visualize the data.
