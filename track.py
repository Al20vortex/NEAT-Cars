import pyglet
from pyglet.libs.win32.constants import NULL

wall_batch = pyglet.graphics.Batch()
gate_batch = pyglet.graphics.Batch()
wall_color = (0, 0, 0)
walls = []
reward_gates = []


class LapGate:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.y1 = float(720 - y1)
        self.y2 = float(720 - y2)
        self.color = (0, 0, 0)
        self.graphics = NULL
        self.active = True

    def draw(self):
        self.graphics = pyglet.shapes.Line(self.x1, self.y1, self.x2, self.y2, 2,
                                           color=self.color, batch=wall_batch)


class Wall:
    # initializes with the coords from gimp
    def __init__(self, x1, y1, x2, y2):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.y1 = float(720 - y1)
        self.y2 = float(720 - y2)
        self.color = (0, 0, 0)
        self.graphics = NULL

    def draw_wall(self):
        self.graphics = pyglet.shapes.Line(self.x1, self.y1, self.x2, self.y2, 2,
                                           color=self.color, batch=wall_batch)

    # checks two lines if they collide
    # this algorithm is directly pasted from Code Bullet's Car AI Project
    # found here: https://github.com/Code-Bullet/Car-QLearning


def linesCollided(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / \
        ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / \
        ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if 0 <= uA <= 1 and 0 <= uB <= 1:
        return True
    return False


class RewardGate:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.y1 = float(720 - y1)
        self.y2 = float(720 - y2)
        self.color = (255, 255, 255)
        self.graphics = NULL
        self.active = True

    def draw_gate(self):
        self.graphics = pyglet.shapes.Line(self.x1, self.y1, self.x2, self.y2, 2,
                                           color=self.color, batch=gate_batch)


# this collision point algorithm is pasted from Code Bullet's Car AI Project
# found here: https://github.com/Code-Bullet/Car-QLearning


def getCollisionPoint(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / \
        ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / \
        ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if 0 <= uA <= 1 and 0 <= uB <= 1:
        intersectionX = x1 + (uA * (x2 - x1))
        intersectionY = y1 + (uA * (y2 - y1))
        return [intersectionX, intersectionY]


reward_gates.append(RewardGate(206, 63, 205, 163))
reward_gates.append(RewardGate(308, 157, 308, 157))
reward_gates.append(RewardGate(517, 64, 516, 150))
reward_gates.append(RewardGate(565, 70, 564, 151))
reward_gates.append(RewardGate(629, 70, 625, 157))
reward_gates.append(RewardGate(733, 64, 733, 156))
reward_gates.append(RewardGate(793, 63, 793, 156))
reward_gates.append(RewardGate(876, 65, 876, 156))
reward_gates.append(RewardGate(1012, 60, 1015, 154))
reward_gates.append(RewardGate(1140, 115, 1087, 186))
reward_gates.append(RewardGate(1113, 250, 1202, 242))
reward_gates.append(RewardGate(1054, 338, 1091, 425))
reward_gates.append(RewardGate(960, 343, 964, 430))
reward_gates.append(RewardGate(888, 343, 882, 428))
reward_gates.append(RewardGate(787, 321, 762, 408))
reward_gates.append(RewardGate(630, 323, 661, 404))
reward_gates.append(RewardGate(527, 451, 604, 489))
reward_gates.append(RewardGate(527, 451, 604, 489))
reward_gates.append(RewardGate(445, 587, 448, 659))
reward_gates.append(RewardGate(271, 608, 275, 691))
reward_gates.append(RewardGate(146, 609, 128, 698))
reward_gates.append(RewardGate(15, 528, 100, 525))
reward_gates.append(RewardGate(9, 374, 93, 372))
reward_gates.append(RewardGate(6, 278, 91, 275))
reward_gates.append(RewardGate(35, 126, 100, 182))

# Outer walls
walls.append(Wall(92.0, 69, 1068, 72))
walls.append(Wall(1068, 72, 1191, 165))
walls.append(Wall(1191, 165, 1197, 330))
walls.append(Wall(1197, 330, 1092, 420))
walls.append(Wall(1092, 420, 798, 425))
walls.append(Wall(798, 425, 713, 378))
walls.append(Wall(713, 378, 632, 413))
walls.append(Wall(632, 413, 539, 641))
walls.append(Wall(539, 641, 382, 690))
walls.append(Wall(382, 690, 102, 690))
walls.append(Wall(102, 690, 23, 590))
walls.append(Wall(23, 590, 6, 177))
walls.append(Wall(6, 177, 92, 69))

# Inner Walls
walls.append(Wall(121, 147, 1046, 151))
walls.append(Wall(1046, 151, 1118, 204))
walls.append(Wall(1118, 204, 1120, 297))
walls.append(Wall(1120, 297, 1060, 348))
walls.append(Wall(1060, 348, 820, 346))
walls.append(Wall(820, 346, 717, 292))
walls.append(Wall(717, 292, 577, 353))
walls.append(Wall(577, 353, 481, 578))
walls.append(Wall(481, 578, 374, 613))
walls.append(Wall(374, 613, 134, 614))
walls.append(Wall(134, 614, 99, 563))
walls.append(Wall(99, 563, 85, 197))
walls.append(Wall(85, 197, 121, 147))
