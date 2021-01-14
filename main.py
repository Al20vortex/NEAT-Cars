import neat
from neat.species import DefaultSpeciesSet
import track
import os
import pyglet
import numpy as np
from pyglet.window import key
from pyglet.gl.gl import GL_POINTS
from pyglet.libs.win32.constants import NULL
import car
from car import Car
import track
import random
pyglet.resource.path = ['images']

car_img = pyglet.resource.image("car.png")
timer = 0.000
car_sprite = NULL
height = 720
width = 1280
lap_gate = NULL
my_car = NULL
reward_label = NULL
nets = []
cars = []
ge = []
generation = 0

# create the batch of items
batch = pyglet.graphics.Batch()
labels = pyglet.graphics.Batch()
racetrack_img = pyglet.resource.image("racetrackv2.png")
racetrack = pyglet.sprite.Sprite(img=racetrack_img, x=0, y=0)


class Game:

    def center_image(self, image):
        """Sets an image's anchor point to its center"""
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    def reset_game(self, config):
        global nets
        labels.d
        game_window.gen_number = pyglet.text.Label(text='Generation Number: ' + str(
            generation), color=(255, 255, 255, 255), font_size=10, x=width - 200, y=50, batch=labels)
        # for i in range(cars.__len__()):
        #     global car_sprite
        #     cars[i] = Car(car_sprite, loc=np.array(
        #         [float(width/3), float(height * 8.5/10)]))
        #     car_sprite = pyglet.sprite.Sprite(
        #         img=car_img, x=cars[i].loc[0], y=cars[i].loc[1], batch=batch)
        #     cars[i].sprite = car_sprite
        #     car_sprite.rotation = cars[i].rot
        # for gate in track.reward_gates:
        #     gate.active = True
        for g in ge:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0.00
            global car_sprite
            car = Car(car_sprite, loc=np.array(
                [float(width/3), float(height * 8.5/10)]))
            car_sprite = pyglet.sprite.Sprite(
                img=car_img, x=car.loc[0], y=car.loc[1], batch=batch)
            car.sprite = car_sprite
            car_sprite.rotation = car.rot
            cars.append(car)

    # def handle_crash(self, car):
    #     if car.crashed == True:
    #         self.reset_game()

    # def handle_input(self):
    #     # returns true if there is keyboard input, false otherwise
    #     if keys[key.UP]:
    #         if keys[key.LEFT]:
    #             my_car.accelerate('forward')
    #             my_car.turn('left')
    #             return True
    #         if keys[key.RIGHT]:
    #             my_car.accelerate('forward')
    #             my_car.turn('right')
    #             return True
    #         my_car.accelerate('forward')
    #         return True
    #     if keys[key.DOWN]:
    #         if keys[key.LEFT]:
    #             my_car.accelerate('backward')
    #             my_car.turn('left')
    #             return True
    #         if keys[key.RIGHT]:
    #             my_car.accelerate('backward')
    #             my_car.turn('right')
    #             return True
    #         my_car.accelerate('backward')
    #         return True
    #     if keys[key.LEFT]:
    #         if my_car.speed != 0:
    #             my_car.turn('left')
    #     if keys[key.RIGHT]:
    #         if my_car.speed != 0:
    #             my_car.turn('right')
    #     return False

    def handle_ai_input(self):
        # returns true if there is keyboard input, false otherwise
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_state())
            i = output.index(max(output))
            self.getAction(car, i)

    def getAction(self, car, index):
        if not car.crashed:
            if index == 0:
                car.rewards = car.rewards
                car.accelerate('forward')
                car.turn('left')
                return
            if index == 1:
                car.rewards = car.rewards
                car.accelerate('forward')
                car.turn('right')
                return
            if index == 2:
                car.rewards = car.rewards
                car.accelerate('forward')
                return
            # if index == 3:
            #     car.rewards = car.rewards
            #     car.accelerate('backward')
            # if index == 4:
            #     car.rewards = car.rewards
            #     car.accelerate('backward')
            #     car.turn('left')
            #     return
            # if index == 5:
            #     car.rewards = car.rewards
            #     car.accelerate('backward')
            #     car.turn('right')
            #     return
            # if index == 6:
            #     if car.speed != 0:
            #         car.turn('left')
            # if index == 7:
            #     if car.speed != 0:
            #         car.turn('right')
            # if index == 8:
            #     car.rewards = car.rewards
            #     car.decelerate()

    def runGame(self, genomes, config):
        # NEAT stuff
        global cars
        global nets
        global ge
        global generation
        global timer
        nets = []
        cars = []
        ge = genomes

        for id, g in ge:
            game_window.gen_number = pyglet.text.Label(text='Generation Number: ' + str(
                generation), color=(255, 255, 255, 255), font_size=10, x=width - 200, y=50)
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0
            global car_sprite
            car = Car(car_sprite, loc=np.array(
                [float(width/3), float(height * 8.5/10)]))
            car_sprite = pyglet.sprite.Sprite(
                img=car_img, x=car.loc[0], y=car.loc[1], batch=batch)
            car.sprite = car_sprite
            car_sprite.rotation = car.rot
            cars.append(car)
        for gate in track.reward_gates:
            gate.active = True
        # for g in genomes:
        #     net = neat.nn.FeedForwardNetwork.create(g, config)
        #     nets.append(net)
        #     g.fitness = 0
        #     global car_sprite
        #     car = Car(car_sprite, loc=np.array(
        #         [float(width/3), float(height * 8.5/10)]))
        #     car_sprite = pyglet.sprite.Sprite(
        #         img=car_img, x=car.loc[0], y=car.loc[1], batch=batch)
        #     car.sprite = car_sprite
        #     car_sprite.rotation = car.rot
        #     cars.append(car)
        generation += 1
        while True:
            pyglet.app.run()
            genomes = ge
            timer = 0.0
            break


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = Game()
        for wall in track.walls:
            wall.draw_wall()
        for gate in track.reward_gates:
            gate.draw_gate()
        global lap_gate
        lap_gate = track.LapGate(369, 69, 370, 153)
        global car_sprite
        self.game.center_image(car_img)
        # car_sprite = pyglet.sprite.Sprite(
        #     img=car_img, x=my_car.loc[0], y=my_car.loc[1], batch=batch)
        # my_car.sprite = car_sprite
        # car_sprite.rotation = my_car.rot

    def update(self, dt):
        global ge
        global cars
        global timer
        timer += 1
        lap_gate.draw()
        # Car stuff
        for i, car in enumerate(cars):
            if car.crashed:
                ge[i][1].fitness = car.rewards
        if self.all_dead():
            pyglet.app.exit()
            return False
        for car in cars:
            car.corner_graphics = []
            car.ray_graphics = []
            # if not self.game.handle_input():
            #     my_car.decelerate()
            # self.game.handle_crash(car)
            car.move()
            car.finished_lap(lap_gate)
            car.calculate_corners()
            car.make_ray_corners()
            car.detect_collison()
            car.detect_rewards(lap_gate)
            car.update_sprite()
        game_window.game.handle_ai_input()

    def all_dead(self):
        for car in cars:
            if not car.crashed:  # if car hasnt crashed
                # if timer > 300:
                #     car.crashed = True
                return False

        return True

    def on_draw(self):
        game_window.clear()
        racetrack.draw()
        batch.draw()
        game_window.gen_number.draw()
        track.gate_batch.draw()
        track.wall_batch.draw()
        car.corner_batch.draw()
        # car.ray_batch.draw()


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(game_window.game.runGame, 999999)


if __name__ == '__main__':
    keys = key.KeyStateHandler()
    game_window = MyWindow(width, height, resizable=True)
    game_window.push_handlers(keys)
    pyglet.clock.schedule_interval(game_window.update, 1/60.0)
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
