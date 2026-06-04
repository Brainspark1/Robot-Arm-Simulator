import numpy as np

def rot_x(theta):
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

def rot_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def rot_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])

def forward_kinematics(robot):

    positions = []

    current_position = np.array([0., 0., 0.])
    current_rotation = np.eye(3)

    positions.append(current_position.copy())

    for link, joint in zip(robot.links, robot.joints):

        R = (
            rot_z(joint.yaw)
            @ rot_y(joint.pitch)
            @ rot_x(joint.roll)
        )

        current_rotation = current_rotation @ R

        offset = current_rotation @ np.array([
            link.length,
            0,
            0
        ])

        current_position += offset

        positions.append(current_position.copy())

    return np.array(positions)