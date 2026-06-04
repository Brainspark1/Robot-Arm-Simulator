from robot import RobotArm
from renderer import RobotRenderer

def main():

    robot = RobotArm([
        4,
        3,
        2
    ])

    renderer = RobotRenderer(robot)
    renderer.show()


if __name__ == "__main__":
    main()