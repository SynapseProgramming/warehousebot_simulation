#!/usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    launch_file_dir = os.path.join(
        get_package_share_directory("warehousebot_simulation"), "launch"
    )
    rviz_config_dir = LaunchConfiguration("rviz_config_dir")
    current_dir = get_package_share_directory("warehousebot_simulation")
    pkg_gazebo_ros = get_package_share_directory("gazebo_ros")

    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    x_pose = LaunchConfiguration("x_pose", default="0.0")
    y_pose = LaunchConfiguration("y_pose", default="0.0")

    declare_rviz_config = DeclareLaunchArgument(
        "rviz_config_dir",
        default_value=os.path.join(current_dir, "rviz", "warehousebot_sim.rviz"),
        description="default path to rviz config file",
    )
    world = os.path.join(
        get_package_share_directory("warehousebot_simulation"),
        "worlds",
        "empty_world.world",
    )

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, "launch", "gzserver.launch.py")
        ),
        launch_arguments={"world": world}.items(),
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, "launch", "gzclient.launch.py")
        )
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, "robot_state_publisher.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, "spawn_bot.launch.py")
        ),
        launch_arguments={"x_pose": x_pose, "y_pose": y_pose}.items(),
    )

    launch_rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_dir],
        parameters=[{"use_sim_time": use_sim_time}],
        output="screen",
    )
    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(declare_rviz_config)
    ld.add_action(launch_rviz2)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)

    return ld
