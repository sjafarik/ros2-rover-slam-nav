from setuptools import setup
from glob import glob
import os

package_name = 'rover_slam_nav'

def collect_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            src = os.path.join(root, filename)
            dst = os.path.join('share', package_name, root)
            files.append((dst, [src]))
    return files

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*')),
        ('share/' + package_name + '/rviz', glob('rviz/*')),
        ('share/' + package_name + '/maps', glob('maps/*')),
    ] + collect_files('models') + collect_files('worlds'),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sjafarik',
    maintainer_email='sjafarik@mtu.edu',
    description='ROS2 SLAM and navigation project for a simulated rover.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)