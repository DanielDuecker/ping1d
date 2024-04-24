from setuptools import find_packages, setup

package_name = 'ping1d'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='DanielDuecker',
    maintainer_email='daniel.duecker@tum.de',
    description='Reading Distances from  BlueRobotics Ping1D Echosounder',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'ping1d_node = ping1d.ping1d_echo_node:main',
        ],
    },
)
