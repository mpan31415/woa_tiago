# TIAGo - Full Setup for HRI Competition

This is the repository for The University of Melbourne's ("Wizards of Aus") entry into the [Office Assistant Robot Competition](https://hri2024c.web.app/hri2014rc2.html) at the [2024 HRI Conference](https://humanrobotinteraction.org/2024/) held in Boulder, Colorado. The robotic platform used in the competition is the [TIAGo mobile manipulator](https://pal-robotics.com/robots/tiago/) from PAL robotics. 

## Installation

### 1. Create a ROS workspace called `tiago_ws`
```shell script
mkdir -p ~/tiago_ws/src
```

### 2. Clone the Git repository
```shell script
cd ~/tiago_ws/src/
git clone --recurse-submodules https://github.com/mpan31415/woa_tiago.git
```

### 3. Installing the required packages from apt
```shell script
sudo apt-get update
sudo apt-get install libportaudio2 python3-pip net-tools cmatrix
```

### 4. Install requirements for YOLOv8 (Ultralytics) forked repo
To install the required Python libraries:
```shell script
cd ~/tiago_ws/src/woa_tiago/ultralytics_ros/
python3 -m pip install -r requirements.txt
```
Then, install the ROS dependencies:
```shell script
cd ~/tiago_ws/
rosdep install -r -y -i --from-paths .
```

### 5. Installing the required Python libraries
```shell script
cd ~/tiago_ws/src/woa_tiago/
pip install -r requirements.txt
```
NOTE: The above might output an error - `ERROR: flask 3.0.2 has requirement click>=8.1.3, but you'll have click 7.0 which is incompatible.`
If so, simply execute the following in the terminal:
```shell script
pip install flask
```

### 6. Add your own GPT API key
```shell script
cd ~/tiago_ws/src/woa_tiago/tiago_gpt4/
mkdir config && cd config
touch gpt_api.yaml
gedit gpt_api.yaml
```
Paste your API into the file, in the format of:
```yaml
api_key: "YOUR_API_KEY"
```

### 6. Building the packages
```shell script
cd ~/tiago_ws/
catkin build detection_msgs tiago_follow_person tiago_gpt4 tiago_nav ultralytics_ros
```


## Connect and Run

### 1. Connect to the TIAGo via Ethernet
Using Ethernet connection is preferred, especially if we want to subscribe to image topics (e.g. RGB or depth images) which are published at 30Hz.

After connecting successfully using Ethernet, in the terminal run:
```shell script
ifconfig
```
Find the corresponding connection with name starting with “enp0”, and copy the ip address after “inet”. 

### 2. Setup the `.bashrc` file
Open the `.bashrc` file:
```shell script
cd
gedit .bashrc
```
and add the following (below the `source init_pal_env.sh` line):
```shell script
source /home/pal/tiago_ws/devel/setup.bash

export ROS_MASTER_URI=http://tiago-196c:11311
# HERE, USE THE PREVIOUSLY COPIED IP ADDRESS
# example: export ROS_IP=10.68.0.128
export ROS_IP=<your_ip_address>

alias map='rviz rviz -d /home/pal/tiago_ws/src/woa_tiago/rviz_configs/map.rviz'
alias cmap='rviz rviz -d /home/pal/tiago_ws/src/woa_tiago/rviz_configs/local_costmap.rviz'
alias fmap='rviz rviz -d /home/pal/tiago_ws/src/woa_tiago/rviz_configs/filtered_map.rviz'
```

### 3. Running
Make sure:
- The microphone is connected to the developemnt laptop
- The robot is connected to the laptop via Etheret

Then, in a new terminal, source the setup and run the main launch file:
```shell script
source ~/.bashrc
roslaunch tiago_gpt4 hri_competition.launch
```