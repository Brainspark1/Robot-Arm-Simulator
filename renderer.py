import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider
from matplotlib.widgets import Button

from kinematics import forward_kinematics

class RobotRenderer:

    def __init__(self, robot):

        self.robot = robot

        self.fig = plt.figure(figsize=(13.5, 9))

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

        self.default_elev = 30
        self.default_azim = -60

        self.ax.view_init(
            elev=self.default_elev,
            azim=self.default_azim
        )

        plt.subplots_adjust(
            left=0.25,
            bottom=0.45
        )

        self.sliders = []

        self.create_controls()

        self.draw()

    def create_controls(self):

        y = 0.35

        for i, joint in enumerate(self.robot.joints):

            yaw_ax = plt.axes([0.15, y, 0.7, 0.02])
            pitch_ax = plt.axes([0.15, y - 0.03, 0.7, 0.02])
            roll_ax = plt.axes([0.15, y - 0.06, 0.7, 0.02])

            yaw = Slider(
                yaw_ax,
                f"Joint {i+1} Yaw (Left/Right)",
                -180,
                180,
                valinit=0
            )

            pitch = Slider(
                pitch_ax,
                f"Joint {i+1} Pitch (Up/Down)",
                -180,
                180,
                valinit=0
            )

            roll = Slider(
                roll_ax,
                f"Joint {i+1} Roll (Tilt)",
                -180,
                180,
                valinit=0
            )

            yaw.on_changed(self.update)
            pitch.on_changed(self.update)
            roll.on_changed(self.update)

            self.sliders.append(
                (yaw, pitch, roll)
            )

            y -= 0.11

        button_ax = plt.axes(
            [0.30, 0.001, 0.2, 0.05]
        )

        self.reset_button = Button(
            button_ax,
            "Reset Arm"
        )

        self.reset_button.on_clicked(
            self.reset_arm
        )

        view_button_ax = plt.axes(
            [0.55, 0.001, 0.2, 0.05]
        )

        self.reset_view_button = Button(
            view_button_ax,
            "Reset View"
        )

        self.reset_view_button.on_clicked(
            self.reset_view
        )

    def reset_arm(self, event):

        self.robot.reset()

        for yaw, pitch, roll in self.sliders:

            yaw.reset()
            pitch.reset()
            roll.reset()

        self.draw()

    def update(self, value):

        for joint, controls in zip(
            self.robot.joints,
            self.sliders
        ):

            yaw, pitch, roll = controls

            joint.yaw = np.radians(yaw.val)
            joint.pitch = np.radians(
                pitch.val
            )
            joint.roll = np.radians(
                roll.val
            )

        self.draw()

    def draw(self):

        elev = self.ax.elev
        azim = self.ax.azim

        self.ax.clear()

        positions = forward_kinematics(
            self.robot
        )

        self.ax.plot(
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
            marker="o",
            linewidth=5
        )

        reach = sum(
            link.length
            for link in self.robot.links
        )

        self.ax.set_xlim(
            -reach,
            reach
        )

        self.ax.set_ylim(
            -reach,
            reach
        )

        self.ax.set_zlim(
            -reach,
            reach
        )

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.ax.set_title(
            "3D Robotic Arm Simulator"
        )

        self.ax.view_init(
        elev=elev,
        azim=azim
)

        self.fig.canvas.draw_idle()

    def reset_view(self, event):
        self.ax.view_init(
            elev=self.default_elev,
            azim=self.default_azim
        )

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()