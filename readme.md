# RSI Control Program Specifications

ini.py of ever module includes initialization of parameters,  signal-slot-pairs and ui elements

## Still to optimize

* disable and enable ui to avoid  error



## Communications

### ini

### functions

* Setup Network 
* UI Button Callbacks
* RSI UDP Server Class
* Message Processing : IPOC

### axis

* extract pose
* generate control command

### cartesian

*  `remap_kuka_pose(pose)`:  **depends on the RSI initial position**  be careful
* extract pose
* generate control command



## Control

### ini

### constant: should not be useful anymore

### control:

* SimpleTransferFunction

* saturate

* TransferFuntion:   general tf  **todo**

* Youla-Parameterize:   **todo**

* simulink to c code: **todo**

##  Kinect



