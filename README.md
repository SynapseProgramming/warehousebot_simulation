# warehousebot_simulation
A package for simulating the warehouse robot. 

## Installation
- Install nav2 
  ```
  sudo apt install ros-humble-navigation2
  ```
  ```
  sudo apt install ros-humble-nav2-bringup
  ```
- Install the turtlebot 3 gazebo package
  ```
  sudo apt install ros-humble-turtlebot3-gazebo
  ```
- Add the following line to your bashrc file
  ```
  source /usr/share/gazebo/setup.sh
  
  ```
- Install humble perception
  ```
  sudo apt install ros-humble-perception
  ```
- Naviate to the gazebo models directory and git clone this package
  ```
  cd ~/.gazebo/models/
  ```
  ```
  git clone https://github.com/SynapseProgramming/warehousebot_simulation.git
  ```
- Navigate to your `ros_ws/src` directory and git clone this package
  ```
  git clone https://github.com/SynapseProgramming/warehousebot_simulation.git
  ```
- Run `colcon build`

## Usage
- To launch the simulation package, run the following command
```
ros2 launch warehousebot_simulation simulation_launch.py
```
  
