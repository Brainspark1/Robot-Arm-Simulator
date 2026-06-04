import numpy as np

class Link:
    def __init__(self, length):
        self.length = length

class Joint:
    def __init__(self):
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0

class RobotArm:
    def __init__(self, link_lengths):
        self.links = [Link(length) for length in link_lengths]
        self.joints = [Joint() for _ in link_lengths]

    def reset(self):
        for joint in self.joints:
            joint.yaw = 0
            joint.pitch = 0
            joint.roll = 0