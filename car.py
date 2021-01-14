import numpy as np
import pyglet
import math
import track
from pyglet.libs.win32.constants import NULL
pyglet.resource.path = ['images']
car_img = pyglet.resource.image("car.png")
car_img.width = 20
car_img.height = 40
max_speed = 15.0
max_acc = 0.3
rot_speed = 3.9
deceleration = 0.2
corner_dist = math.sqrt((car_img.width / 2.0)**2 + (car_img.height / 2.0)**2)
# angle from car centre to top left corner
corner_angle = math.atan(
    car_img.width / car_img.height) / (2.0 * math.pi) * 360.0
corner_batch = pyglet.graphics.Batch()
ray_batch = pyglet.graphics.Batch()
ray_length = 200.0


class Car:
    def __init__(self, sprite, loc=np.array([0.0, 0.0]), rot=90.0):
        global car_img
        self.loc = loc
        self.speed = 0.0
        # acc represents forward and backward acceleration
        self.acc = max_acc
        self.sprite = sprite
        self.crashed = False
        self.rot = rot
        self.corners = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
        self.corner_graphics = []
        self.ray_graphics = []
        self.hitbox = NULL
        self.rays = NULL
        self.ray_corners = NULL
        self.rewards = 0.00
        self.state = []

    def finished_lap(self, lap_gate):
        if track.linesCollided(lap_gate.x1, lap_gate.y1, lap_gate.x2, lap_gate.y2, self.corners[0][0], self.corners[0][1], self.corners[1][0], self.corners[1][1]):
            if lap_gate.active == True:
                self.rewards += 1.0
                lap_gate.active = False
            for gate in track.reward_gates:
                gate.active = True

    def accelerate(self, string):
        # stub
        if not self.crashed:
            if (string == 'forward'):
                if self.speed + max_acc > max_speed:
                    self.speed = max_speed
                else:
                    self.speed += max_acc
            if (string == 'backward'):
                if self.speed - max_acc < -max_speed:
                    self.speed = -max_speed
                else:
                    self.speed -= max_acc

    def turn(self, direction):
        if (direction == 'left'):
            self.rot -= rot_speed * self.speed / 5.0
        if direction == 'right':
            self.rot += rot_speed * self.speed / 5.0
        self.update_sprite()

    def update_sprite(self):
        self.sprite.rotation = self.rot
        self.sprite.x = self.loc[0]
        self.sprite.y = self.loc[1]

    def decelerate(self):
        self.speed
        if self.speed > 0:
            if self.speed - deceleration > 0:
                self.speed -= deceleration
            else:
                self.speed = 0

        if self.speed < 0:
            if self.speed + deceleration < 0:
                self.speed += deceleration
            else:
                self.speed = 0.0

    def move(self):
        if self.crashed == True:
            return
        # self.loc[0] += self.speed * \
        #     -math.cos(self.rot * 2 * math.pi / 360)
        # self.loc[1] += self.speed * \
        #     math.sin(self.rot * 2 * math.pi / 360)
        self.loc[0] += self.speed * \
            math.sin(self.rot * 2 * math.pi / 360)
        self.loc[1] += self.speed * \
            math.cos(self.rot * 2 * math.pi / 360)
        self.update_sprite()

    def calculate_corners(self):
        # corner order when car facing up: top right, bottom right, bottom left, top left
        x = self.loc[0]
        y = self.loc[1]
        self.corners = np.array([[x+math.sin((self.rot+corner_angle) * 2 * math.pi / 360) *
                                  corner_dist, y+math.cos((self.rot+corner_angle) * 2 * math.pi / 360) * corner_dist],
                                 [x+math.sin((self.rot + 180 - corner_angle) * 2 * math.pi / 360) *
                                  corner_dist, y+math.cos((self.rot + 180 - corner_angle) * 2 * math.pi / 360) * corner_dist],
                                 [x+math.sin((self.rot + 180 + corner_angle) * 2 * math.pi / 360) *
                                  corner_dist, y+math.cos((self.rot + 180 + corner_angle) * 2 * math.pi / 360) * corner_dist],
                                 [x+math.sin((self.rot-corner_angle) * 2 * math.pi / 360) *
                                  corner_dist, y+math.cos((self.rot-corner_angle) * 2 * math.pi / 360) * corner_dist]])
        self.calculate_hitbox()

    def calculate_hitbox(self):
        self.hitbox = np.array([[self.corners[0], self.corners[1]],
                                [self.corners[1], self.corners[2]],
                                [self.corners[2], self.corners[3]],
                                [self.corners[3], self.corners[0]]
                                ])

    def draw_corners(self):
        for corner in self.corners:
            self.corner_graphics.append(pyglet.shapes.Circle(corner[0], corner[1], 4,
                                                             color=(0, 0, 0), batch=corner_batch))

    def draw_ray_corners(self):
        for corner in self.ray_corners:
            self.corner_graphics.append(pyglet.shapes.Circle(corner[0], corner[1], 4,
                                                             color=(0, 0, 0), batch=ray_batch))

    def detect_collison(self):
        for wall in track.walls:
            for line in self.hitbox:
                if track.linesCollided(wall.x1, wall.y1, wall.x2, wall.y2, line[0, 0], line[0, 1], line[1, 0], line[1, 1]):
                    self.crashed = True
                    self.speed = 0
                    self.rewards += 0

    def detect_rewards(self, lap_gate):
        if self.speed > 0:
            for gate in track.reward_gates:
                if gate.active:
                    if track.linesCollided(gate.x1, gate.y1, gate.x2, gate.y2, self.corners[0][0], self.corners[0][1], self.corners[1][0], self.corners[1][1]):
                        self.rewards += 10.0
                        gate.active = False
                        if not lap_gate.active:
                            lap_gate.active = True

    def make_ray_corners(self):
        x = self.loc[0]
        y = self.loc[1]
        self.ray_corners = np.array([[x+math.sin((self.rot+corner_angle) * 2 * math.pi / 360) *
                                      ray_length, y+math.cos((self.rot+corner_angle) * 2 * math.pi / 360) * ray_length],
                                     [x+math.sin((self.rot + 180 - corner_angle) * 2 * math.pi / 360) *
                                      ray_length, y+math.cos((self.rot + 180 - corner_angle) * 2 * math.pi / 360) * ray_length],
                                     [x+math.sin((self.rot + 180 + corner_angle) * 2 * math.pi / 360) *
                                      ray_length, y+math.cos((self.rot + 180 + corner_angle) * 2 * math.pi / 360) * ray_length],
                                     [x+math.sin((self.rot-corner_angle) * 2 * math.pi / 360) *
                                      ray_length, y+math.cos((self.rot-corner_angle) * 2 * math.pi / 360) * ray_length],
                                     [x+math.sin(self.rot * 2 * math.pi / 360) * ray_length, y+math.cos(
                                         (self.rot) * 2 * math.pi / 360) * ray_length],
                                     #  [x+math.sin((180 + self.rot) * 2 * math.pi / 360) * ray_length, y+math.cos((180 + self.rot) * 2 * math.pi / 360)]
                                     [x-math.sin(self.rot * 2 * math.pi / 360) * ray_length, y-math.cos(
                                         (self.rot) * 2 * math.pi / 360) * ray_length]
                                     ])
        self.make_rays()
        self.draw_ray_intersection()

    # Car sees with these rays, there will be six total

    def make_rays(self):
        centre = np.array([self.loc[0], self.loc[1]])
        self.rays = np.array([[centre, self.ray_corners[1]],
                              [centre, self.ray_corners[2]],
                              [centre, self.ray_corners[3]],
                              [centre, self.ray_corners[0]],
                              [centre, self.ray_corners[4]],
                              [centre, self.ray_corners[5]]
                              ])

    def get_state(self):
        self.state = []
        hit = False
        for ray in self.rays:
            for wall in track.walls:
                if track.linesCollided(wall.x1, wall.y1, wall.x2, wall.y2,
                                       ray[0, 0], ray[0, 1], ray[1, 0], ray[1, 1]):
                    hit = True
                    col = track.getCollisionPoint(wall.x1, wall.y1, wall.x2, wall.y2,
                                                  ray[0, 0], ray[0, 1], ray[1, 0], ray[1, 1])
                    distance = math.sqrt(
                        (col[0] - self.loc[0])**2 + (col[1] - self.loc[1])**2) / ray_length
                    self.state.append(distance)
                    break
            if hit == False:
                distance = 1.0
                self.state.append(distance)
            hit = False
        self.state.append(self.speed / max_speed)
        self.state.append((self.rot + 360) / 720)
        return self.state

    def draw_ray_intersection(self):
        for ray in self.rays:
            for wall in track.walls:
                if track.linesCollided(wall.x1, wall.y1, wall.x2, wall.y2,
                                       ray[0, 0], ray[0, 1], ray[1, 0], ray[1, 1]):
                    col = track.getCollisionPoint(wall.x1, wall.y1, wall.x2, wall.y2,
                                                  ray[0, 0], ray[0, 1], ray[1, 0], ray[1, 1])
                    self.ray_graphics.append(pyglet.shapes.Circle(col[0], col[1], 7,
                                                                  color=(255, 0, 0), batch=ray_batch))
