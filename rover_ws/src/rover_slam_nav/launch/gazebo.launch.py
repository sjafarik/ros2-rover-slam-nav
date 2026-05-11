from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from launch_ros.actions import Node


def generate_launch_description():
    package_name = "rover_slam_nav"

    pkg_share = get_package_share_directory(package_name)

    model_path = str(Path(pkg_share) / "models")
    world_path = str(Path(pkg_share) / "worlds" / "rover_robot_world.sdf")

    ros_gz_sim_path = get_package_share_directory("ros_gz_sim")

    set_gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=model_path,
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                ros_gz_sim_path,
                "launch",
                "gz_sim.launch.py",
            ])
        ),
        launch_arguments={
            "gz_args": "-r " + world_path,
        }.items(),
    )

    bridge = Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                arguments=[
                    "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
                    "/model/rover_robot/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist",
                    "/model/rover_robot/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry",
                    "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
                    "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU", 
                ],
                remappings=[
                    ("/model/rover_robot/cmd_vel", "/cmd_vel"),
                ],
                output="screen",
            )
    
    ekf_node = Node(
                package="robot_localization",
                executable="ekf_node",
                name="ekf_filter_node",
                output="screen",
                parameters=[
                    str(Path(pkg_share) / "config" / "ekf.yaml"),
                    {"use_sim_time": True},
                ],
            )
    
    lidar_static_tf_node = Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="lidar_static_transform_publisher",
                arguments=[
                    "-0.2", "0", "0.1",
                    "0", "0", "0",
                    "rover_robot/body",
                    "rover_robot/lidar_link/lidar_sensor",
                ],
                output="screen",
            )

    slam_toolbox_node = Node(
                package="slam_toolbox",
                executable="async_slam_toolbox_node",
                name="slam_toolbox",
                output="screen",
                parameters=[
                    str(Path(pkg_share) / "config" / "slam_toolbox.yaml"),
                    {"use_sim_time": True},
                ],
            )
    return LaunchDescription([
        set_gz_resource_path,
        gazebo,
        bridge,
        ekf_node,
        lidar_static_tf_node,
        slam_toolbox_node,
    ])