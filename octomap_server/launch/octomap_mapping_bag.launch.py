import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Resolve package share directory to locate config and RViz files
    pkg_share = get_package_share_directory('octomap_server')

    # config_file = os.path.join(pkg_share, 'config', 'vdb_gpdf_mapping_bag.yaml')

    # Bag file argument (default points to the Docker-mounted path)
    bag_file_arg = DeclareLaunchArgument(
        'bag_file',
        default_value='/workspace/data/converted_ros2_bag.db3',
        description='Full path to the ROS2 bag file to play'
    )

    return LaunchDescription([
        bag_file_arg,

        # Main VDB-GPDF mapping node
        Node(
            package='octomap_server',
            executable='octomap_server_node',
            name='octomap_server_bag',
            parameters=[
                {'bag_file': LaunchConfiguration('bag_file')},
                {'frame_id': "odom"},
                {'resolution': 0.05},
                {'sensor_model.max_range': 20.0},
                {'lidar_topic': "/dlio/odom_node/pointcloud/deskewed"},
            ],
            output='screen'
        ),

    ])
