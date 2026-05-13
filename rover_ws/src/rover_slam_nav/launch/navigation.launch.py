from pathlib import Path

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory("rover_slam_nav")

    map_file = str(Path(pkg_share) / "maps" / "slam_test_map.yaml")

    map_server_node = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            {"use_sim_time": True},
            {"yaml_filename": map_file},
        ],
    )

    lifecycle_manager_node = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_map",
        output="screen",
        parameters=[
            {"use_sim_time": True},
            {"autostart": True},
            {"node_names": [
                "map_server",
                "amcl",
                "planner_server",
                "controller_server",
                "bt_navigator",
                "behavior_server",
            ]},
        ],
    )

    amcl_node = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[
            str(Path(pkg_share) / "config" / "amcl.yaml"),
            {"use_sim_time": True},
        ],
    )

    nav2_params = str(Path(pkg_share) / "config" / "nav2_params.yaml")

    planner_node = Node(
        package="nav2_planner",
        executable="planner_server",
        name="planner_server",
        output="screen",
        parameters=[
            nav2_params,
            {"use_sim_time": True},
        ],
    )

    controller_node = Node(
        package="nav2_controller",
        executable="controller_server",
        name="controller_server",
        output="screen",
        parameters=[
            nav2_params,
            {"use_sim_time": True},
        ],
    )

    bt_navigator_node = Node(
        package="nav2_bt_navigator",
        executable="bt_navigator",
        name="bt_navigator",
        output="screen",
        parameters=[
            nav2_params,
            {"use_sim_time": True},
        ],
    )

    behavior_node = Node(
        package="nav2_behaviors",
        executable="behavior_server",
        name="behavior_server",
        output="screen",
        parameters=[
            nav2_params,
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([
        map_server_node,
        amcl_node,
        planner_node,
        controller_node,
        bt_navigator_node,
        behavior_node,
        lifecycle_manager_node,
    ])