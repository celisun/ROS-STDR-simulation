# STDR Simulation
STDR robot simulation under ROS enviornment. Can be used for maze solving, navigation, multiple tasks.

A sample project using stdr（ROS Maze without SLAM): http://campusrover.org.s3-website-us-west-2.amazonaws.com/content/topics/robotprojects/04_ROS_Maze.md/

<img src="https://github.com/celisun/STDR-simulation/blob/master/stdr-turtlebota.png" width="600">



## How to use STDR 
http://campusrover.org.s3-website-us-west-2.amazonaws.com/content/topics/robotrecipes/stdr_guide.md/
### cheat sheet
1. open ROS server `roscore`

1. open STDR server `source /opt/ros/kinetic/setup.bash`,
   * with a default map  `roslaunch stdr_launchers server_with_map_and_gui_plus_robot.launch`
   * with no map `roslaunch stdr_launchers server_no_map.launch`, and then **open your own map** (also see: [How to load a map](http://wiki.ros.org/stdr_simulator/Tutorials/How%20to%20load%20a%20map))
         * way1 : `rosrun stdr_server stdr_server_node maps/<your_own_maze.yaml>`
         * way2 : `roscd stdr_resources` ---> `rosrun stdr_server load_map maps/<your_own_maze.yaml>`

1. open GUI visualizer. `roslaunch stdr_gui stdr_gui.launch`

1. open RVIZ(optional).`roslaunch stdr_launchers rviz.launch`

1. compile and run your script.`chmod +x rosmaze <your_own_script.py>`, then run `rosrun <workspace name> <your_own_script.py>`  *we recommand you put your own scripts in catkin_ws/src/stdr_simulator/stdr_samples.


### How to register external map
1. download/draw/get an image in **.png** format. *[online-format-converter](https://www.online-convert.com/)

1. put **your_own.png** in folder **catkin_ws/src/stdr_simulator/stdr_resources/maps**.

1. write a **your_own.yaml** file for your map, use the same format as other yaml files, notice change file name to match with your map name.

1. run: `sudo chown -R $USER:$USER /opt/ros/kinetic/share/stdr_resources/maps` This gives you the permission of editing this source folder (you might not need this line)

1. now you can put **your_own.png** and **your_own.yaml** in the folder **/opt/ros/kinetic/share/stdr_resources/maps**.

1. Finally, register the map, run `roscd stdr_resources` , then `rosservice call /stdr_server/load_static_map "mapFile: '$PWD/maps/<your_own.yaml>'"`.
