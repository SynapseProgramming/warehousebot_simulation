import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node

from launch.conditions import IfCondition, UnlessCondition



def generate_launch_description():



    robot_model='warehouse_bot_sim.urdf'
    current_dir=get_package_share_directory('warehousebot_simulation')
    robot_model_path=os.path.join(current_dir,'urdf',robot_model)

    use_sim_time = LaunchConfiguration('use_sim_time')
    rviz_config_dir=LaunchConfiguration('rviz_config_dir')
    run_rviz2=LaunchConfiguration('run_rviz2')


    with open(robot_model_path, 'r') as infp:
        robot_desc = infp.read()


    declare_sim_time=DeclareLaunchArgument(
                'use_sim_time',
                default_value='false',
                description='Use simulation (Gazebo) clock if true')


    declare_rviz_launch=DeclareLaunchArgument(
                'run_rviz2',
                default_value='false',
                description='run rviz')


    declare_rviz_config=DeclareLaunchArgument(
                'rviz_config_dir',
                default_value=os.path.join(current_dir,'rviz','view_warehousebot.rviz'),
                description='default path to rviz config file')



    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_desc
        }]
    )

    ld=LaunchDescription()

    launch_rviz2=Node(
                condition=IfCondition(run_rviz2),
                package='rviz2',
               executable='rviz2',
                name='rviz2',
                arguments=['-d', rviz_config_dir],
                parameters=[{'use_sim_time': use_sim_time}],
                output='screen')


    ld.add_action(declare_rviz_launch)
    ld.add_action(declare_sim_time)
    ld.add_action(declare_rviz_config)
    ld.add_action(launch_rviz2)
    ld.add_action(robot_state_publisher_node)
    return ld