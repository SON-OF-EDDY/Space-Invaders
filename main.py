import os
#os.environ["KIVY_AUDIO"] = "android"

import kivy
from kivy.app import App
#from kivy.core.text import Label
from kivy.factory import Factory
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.properties import ObjectProperty, Clock, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import random
from kivy.uix.label import Label


########################################################################################################################
# TO DO:
########################################################################################################################
Builder.load_file('design.kv')

#Window.fullscreen = 'auto'
Window.size = (300,600)

class MultiAudio:
    _next = 0

    def __init__(self, filename, count):
        self.buf = [SoundLoader.load(filename)
                    for _ in range(count)]

    def play(self, *args):
        self.buf[self._next].play()
        self._next = (self._next + 1) % len(self.buf)

    def stop(self,*args):
        self.buf[self._next].stop()
        #self._next = (self._next + 1) % len(self.buf)

class GameScreen(Screen):
    pass

class SecondScreen(Screen):

    def game_reset(self, *args):
        third_screen = self.manager.get_screen('third')
        third_screen.reset()
        game_screen = self.manager.get_screen('game')
        my_game = game_screen.children[0]
        my_game.reset()
        self.parent.current = 'game'

class ThirdScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.consec_wins = 0
        self.streak_label = Label(text=f"WINNING STREAK: {self.consec_wins}",font_size=(Window.width/20),color=(255 / 255, 232 / 255, 31 / 255, 1),\
                             pos_hint={'center_x': 0.3, 'center_y': 0.95},font_name="starwars_4")

        self.add_widget(self.streak_label)

    def reset(self,*args):
        self.consec_wins = 0

    def game_reset(self, *args):
        game_screen = self.manager.get_screen('game')
        my_game = game_screen.children[0]
        my_game.reset()
        self.parent.current = 'game'

    def on_pre_enter(self):
        self.consec_wins += 1

        self.streak_label.text = f"WINNING STREAK: {self.consec_wins}"

class Life(Widget):
    pass

class ProtectionBit(Widget):
    pass


class MotherShip(Widget):

    #sound_bump_mothership = MultiAudio("mothership_2.m4a", 1)
    sound_bump_mothership = SoundLoader.load('mothership_2.m4a')

    def move(self, *args):
        self.sound_bump_mothership.play()
        self.my_animation = Animation(x=Window.width, y=self.pos[1], duration=2.5)
        self.my_animation.bind(on_complete=self.remove)
        self.my_animation.start(self)

    def remove(self, *args):
        if self.parent:
            self.parent.array_mothership = []
            self.sound_bump_mothership.stop()
            self.parent.remove_widget(self)

class Explosion(Widget):

    def sequence_of_sprites(self, *args):
        self.animation_stage_1 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_1.bind(on_complete=self.animation_stage2)
        self.animation_stage_1.start(self)

    def animation_stage2(self, *args):
        with self.canvas:
            Rectangle(source='second_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_2 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_2.bind(on_complete=self.animation_stage3)
        self.animation_stage_2.start(self)

    def animation_stage3(self, *args):
        with self.canvas:
            Rectangle(source='third_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_3 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_3.bind(on_complete=self.animation_stage4)
        self.animation_stage_3.start(self)

    def animation_stage4(self, *args):
        with self.canvas:
            Rectangle(source='fourth_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_4 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_4.bind(on_complete=self.animation_stage5)
        self.animation_stage_4.start(self)

    def animation_stage5(self, *args):
        with self.canvas:
            Rectangle(source='fifth_stage_2.png', size=(self.size), pos=(self.pos))
        self.animation_stage_5 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_5.bind(on_complete=self.animation_stage6)
        self.animation_stage_5.start(self)

    def animation_stage6(self, *args):
        with self.canvas:
            Rectangle(source='sixth_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_6 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_6.bind(on_complete=self.animation_stage7)
        self.animation_stage_6.start(self)

    def animation_stage7(self, *args):
        with self.canvas:
            Rectangle(source='seventh_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_7 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_7.bind(on_complete=self.animation_stage8)
        self.animation_stage_7.start(self)

    def animation_stage8(self, *args):
        with self.canvas:
            Rectangle(source='eigth_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_8 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_8.bind(on_complete=self.remove_explosion_object)
        self.animation_stage_8.start(self)

    def remove_explosion_object(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class Missile(Widget):
    sound_bump_damage = MultiAudio('damage_2.m4a', 3)

    def move_down(self, *args):
        self.animation_down = Animation(x=self.pos[0], y=-self.size[1], duration=2)
        self.animation_down.bind(on_progress=self.on_route)
        self.animation_down.bind(on_complete=self.remove_missile)
        self.animation_down.start(self)

    def on_route(self, *args):

        go_on = True

        if go_on:
            if self.parent:
                if self.parent.array_of_bullets != []:
                    for bullet in self.parent.array_of_bullets:
                        if self.collide_widget(bullet):

                            position_in_array = self.parent.array_of_bullets.index(bullet)
                            del self.parent.array_of_bullets[position_in_array]
                            self.parent.bullet_on_screen = False
                            self.parent.remove_widget(bullet)
                            self.animation_down.stop(self)
                            go_on = False

        if go_on:
            if self.parent:
                for bit in self.parent.array_of_bits:
                    if self.collide_widget(bit):
                        position_in_array = self.parent.array_of_bits.index(bit)
                        del self.parent.array_of_bits[position_in_array]
                        self.parent.remove_widget(bit)
                        self.animation_down.stop(self)
                        go_on = False

        if go_on:
            if self.parent:
                if self.collide_widget(self.parent.ship):
                    self.sound_bump_damage.play()
                    # create a new explosion widget here...
                    new_explosion = Explosion()
                    new_explosion.size = (self.parent.ship.size[0], self.parent.ship.size[1])
                    new_explosion.pos = (
                    self.parent.ship.pos[0], self.parent.ship.pos[1] + self.parent.ship.size[1] / 2)
                    self.parent.add_widget(new_explosion)
                    new_explosion.sequence_of_sprites()
                    self.parent.number_of_lives -= 1

                    if self.parent.array_of_lives != []:
                        widget_to_remove = self.parent.array_of_lives[0]
                        self.parent.remove_widget(widget_to_remove)
                        del self.parent.array_of_lives[0]
                    self.animation_down.stop(self)

    def remove_missile(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class Ship(Widget):
    pass


class Bullet(Widget):

    sound_bump_invader_death = MultiAudio('invader_death_3_2.m4a', 10)
    sound_bump_mothership_death = MultiAudio('mothership_death_1.m4a', 1)

    continue_on = True

    def move_up(self, *args):
        if self.parent:
            self.animation_up = Animation(x=self.pos[0], y=self.parent.height, duration=0.75)
            self.animation_up.bind(on_complete=self.remove_bullet)
            self.animation_up.bind(on_progress=self.on_travel)
            self.animation_up.start(self)

    def remove_bullet(self, *args):
        if self.parent:
            self.parent.bullet_on_screen = False
            del self.parent.array_of_bullets[0]
            self.parent.remove_widget(self)

    def on_travel(self, *args):
        go_on = True

        if self.parent:
            for bit in self.parent.array_of_bits:
                if self.collide_widget(bit):
                    position_in_array = self.parent.array_of_bits.index(bit)
                    del self.parent.array_of_bits[position_in_array]
                    self.parent.remove_widget(bit)
                    self.animation_up.stop(self)
                    go_on = False

            if go_on:
                for invader in self.parent.array_of_aliens:
                    if self.collide_widget(invader):
                        position_in_array = self.parent.array_of_aliens.index(invader)
                        self.sound_bump_invader_death.play()
                        new_explosion = Explosion()
                        new_explosion.size = (invader.size[0], invader.size[1])
                        new_explosion.pos = (invader.pos[0], invader.pos[1])
                        self.parent.add_widget(new_explosion)
                        new_explosion.sequence_of_sprites()

                        del self.parent.array_of_aliens[position_in_array]
                        self.parent.remove_widget(invader)
                        self.animation_up.stop(self)
                        go_on = False

            if go_on:
                if self.parent.array_mothership != []:
                    for mothership in self.parent.array_mothership:
                        if self.collide_widget(mothership):
                            if self.parent.number_of_lives < 3:
                                self.parent.number_of_lives +=1


                            lives_left = len(self.parent.array_of_lives)
                            if lives_left == 2 or lives_left == 1:
                                new_life = Life()
                                new_life.size = (Window.width / 15, Window.width / 15)

                                current_pos = self.parent.array_of_lives[0].pos
                                new_life.pos = (current_pos[0] - (Window.width / 30) - (Window.width / 15), current_pos[1])
                                self.parent.array_of_lives.insert(0, new_life)
                                self.parent.add_widget(new_life)

                            # other stuff working fine...
                            self.sound_bump_mothership_death.play()
                            new_explosion = Explosion()
                            new_explosion.size = (mothership.size[0], mothership.size[1])
                            new_explosion.pos = (mothership.pos[0], mothership.pos[1])
                            self.parent.add_widget(new_explosion)
                            new_explosion.sequence_of_sprites()

                            del self.parent.array_mothership[0]

                            mothership.my_animation.stop(mothership)

class Alien(Widget):

    important_property = Window.width / 10

    important_array = [Window.width / 10, Window.width / 10 + Window.width / 5,
                       Window.width / 10 + 2 * Window.width / 5,
                       Window.width / 10 + 3 * Window.width / 5, Window.width / 10 + 4 * Window.width / 5]

    cols_left = 5

    def move_right_and_down(self, *args):
        new_x_position_for_invader = self.pos[0] + self.important_property
        self.animation_right_and_down = Animation(x=new_x_position_for_invader, duration=1.5)
        self.animation_right_and_down.bind(on_complete=self.intermediary_1)
        self.animation_right_and_down.start(self)

    def intermediary_1(self, *args):
        if self.parent:

            self.important_property = self.parent.leftmost_x
            for value in self.important_array:
                if value - 5 <= self.important_property <= value + 5:
                    self.important_property = value

            self.animation_down = Animation(y=self.pos[1] - self.size[1] / 2.5, duration=0.4)
            self.animation_down.bind(on_complete=self.move_left_and_down)
            self.animation_down.start(self)

    def move_left_and_down(self, *args):
        new_x_position_for_invader = self.pos[0] - self.important_property
        self.animation_left_and_down = Animation(x=new_x_position_for_invader, duration=1.5)
        self.animation_left_and_down.bind(on_complete=self.intermediary_2)
        self.animation_left_and_down.start(self)

    def intermediary_2(self, *args):
        if self.parent:

            self.important_property = Window.width - (self.parent.rightmost_x) - self.size[0]
            for value in self.important_array:
                if value - 5 <= self.important_property <= value + 5:
                    self.important_property = value

            self.animation_down = Animation(y=self.pos[1] - self.size[1] / 2.5, duration=0.4)
            self.animation_down.bind(on_complete=self.move_right_and_down)
            self.animation_down.start(self)


########################################################################################################################
########################################################################################################################
# class Game(Widget):

class Game(Widget):
    travel_direction = 'right'
    bullet_on_screen = False
    # pressed_keys = set()
    number_of_lives = 3
    array_of_aliens = []
    num_cols = 5
    array_of_lives = []
    array_of_bits = []
    array_of_bullets = []
    leftmost_x = 0
    rightmost_x = 0

    array_mothership = []
    going_right = True
    amount_to_animate_by = 0
    sound_bump_laser = MultiAudio('blaster_3.m4a', 5)
    sound_bump_missile = MultiAudio('tie_laser_3_2.m4a', 10)

    ship = ObjectProperty(None)
    my_label = ObjectProperty(None)

    # my_reset = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self._keyboard = Window.request_keyboard(self.close, self)
        # self._keyboard.bind(on_key_down=self.press)
        # self._keyboard.bind(on_key_up=self.release)

    def on_size(self, *args):
        self.sound_track = SoundLoader.load(filename='soundtrack_3.m4a')
        self.sound_track.play()
        # DEFINING ALIENS
        x_spacing_between_aliens = self.parent.size[1] / 10
        y_start = self.parent.size[1] - self.parent.size[1] / 12
        y_spacing_between_aliens = self.parent.size[1] / 15

        for x in range(5):
            for y in range(5):
                new_alien = Alien()
                new_alien.size = (Window.width / 10, Window.width / 10)
                new_alien.pos = (x_spacing_between_aliens * x, y_start - y * y_spacing_between_aliens)
                self.array_of_aliens.append(new_alien)

        # FOR PLAYER SHIP...
        self.ship.size = (self.parent.size[0] / 6, self.parent.size[0] / 8)
        # self.ship.pos = (Window.width/2-self.size[0]/2,Window.height*0.05)

        # MOVEMENT AND FIRE BUTTONS...

        b_size = Window.width / 6
        b_size_fire = Window.width/5
        b_height = Window.height * 0.025
        b_height_fire = Window.height * 0.0175

        self.right_button = Button(text='', size=(b_size, b_size), pos=(Window.width * 0.35, b_height),background_color=(0,0,0,0))
        with self.right_button.canvas:
            Rectangle(source='triangle_left.png',size=(self.right_button.size),pos=(self.right_button.pos))

        self.left_button = Button(text='', size=(b_size, b_size), pos=(Window.width * 0.05, b_height),background_color=(0,0,0,0))
        with self.left_button.canvas:
            Rectangle(source='triangle_right.png',size=(self.left_button.size),pos=(self.left_button.pos))

        self.fire_button = Button(text='', size=(b_size_fire, b_size_fire), pos=(Window.width * 0.75, b_height_fire),background_color=(0,0,0,0))
        with self.fire_button.canvas:
            Rectangle(source='shoot_6.png',size=(self.fire_button.size),pos=(self.fire_button.pos))

        self.add_widget(self.left_button)
        self.add_widget(self.right_button)
        self.add_widget(self.fire_button)

        # IMPORTANT SCHEDULING...
        # Clock.schedule_interval(self.process_keys, 1 / 60)
        Clock.schedule_interval(self.process_buttons,1/60)
        Clock.schedule_interval(self.check_win, 1 / 60)
        Clock.schedule_interval(self.check_loss, 1 / 60)
        Clock.schedule_interval(self.aliens_shooting, 1)
        Clock.schedule_interval(self.check_ship_alien_collision, 1 / 60)
        Clock.schedule_interval(self.check_alien_bit_collision, 1 / 60)
        Clock.schedule_interval(self.display_mothership, 10)
        Clock.schedule_interval(self.number_of_columns_left, 1 / 360)

        # ADDING ALIENS
        for invader in self.array_of_aliens:
            self.add_widget(invader)

        # STARTING THE ALIENS MOVING
        for invader in self.array_of_aliens:
            invader.move_right_and_down()

        # 3 MINI SHIPS REPRESENTING LIVES REMAINING
        spacing = Window.width / 30
        new_life_1 = Life()
        new_life_1.size = (Window.width / 15, Window.width / 15)
        new_life_1.pos = (Window.width - (3 * Window.width / 15) - (3 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_1)
        self.add_widget(new_life_1)

        new_life_2 = Life()
        new_life_2.size = (Window.width / 15, Window.width / 15)
        new_life_2.pos = (Window.width - (2 * Window.width / 15) - (2 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_2)
        self.add_widget(new_life_2)

        new_life_3 = Life()
        new_life_3.size = (Window.width / 15, Window.width / 15)
        new_life_3.pos = (Window.width - (1 * Window.width / 15) - (1 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_3)
        self.add_widget(new_life_3)

        # ADDING PROTECTION BITS

        starting_height = Window.height * 0.2
        block_width_height = Window.width / 6
        number_of_bit_columns = 3
        number_of_bit_rows = 3
        bit_size = block_width_height / number_of_bit_columns
        spacing_between_blocks = (Window.width - (3 * block_width_height)) / 4
        x_distance_between_bits = bit_size
        y_distance_between_bits = bit_size

        y_start_block = starting_height
        x_start_block_left = spacing_between_blocks
        x_start_block_centre = (spacing_between_blocks * 2) + (block_width_height)
        x_start_block_right = (spacing_between_blocks * 3) + (block_width_height * 2)

        # MANUALLY ADDING EVERYTHING LIKE AN IDIOT!!! 'CAUSE THE SHORT WAY WAS BUGGY FOR SOME REASON...
        # LEFT BLOCK
        bit_1 = ProtectionBit()
        bit_1.size = (bit_size, bit_size)
        bit_1.pos = (x_start_block_left, y_start_block)
        self.array_of_bits.append(bit_1)

        bit_2 = ProtectionBit()
        bit_2.size = (bit_size, bit_size)
        bit_2.pos = (x_start_block_left + x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_2)

        bit_3 = ProtectionBit()
        bit_3.size = (bit_size, bit_size)
        bit_3.pos = (x_start_block_left + 2 * x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_3)

        bit_4 = ProtectionBit()
        bit_4.size = (bit_size, bit_size)
        bit_4.pos = (x_start_block_left, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_4)

        bit_5 = ProtectionBit()
        bit_5.size = (bit_size, bit_size)
        bit_5.pos = (x_start_block_left + x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_5)

        bit_6 = ProtectionBit()
        bit_6.size = (bit_size, bit_size)
        bit_6.pos = (x_start_block_left + 2 * x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_6)

        bit_7 = ProtectionBit()
        bit_7.size = (bit_size, bit_size)
        bit_7.pos = (x_start_block_left, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_7)

        bit_8 = ProtectionBit()
        bit_8.size = (bit_size, bit_size)
        bit_8.pos = (x_start_block_left + x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_8)

        bit_9 = ProtectionBit()
        bit_9.size = (bit_size, bit_size)
        bit_9.pos = (x_start_block_left + 2 * x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_9)

        # CENTRAL BLOCK

        bit_10 = ProtectionBit()
        bit_10.size = (bit_size, bit_size)
        bit_10.pos = (x_start_block_centre, y_start_block)
        self.array_of_bits.append(bit_10)

        bit_11 = ProtectionBit()
        bit_11.size = (bit_size, bit_size)
        bit_11.pos = (x_start_block_centre + x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_11)

        bit_12 = ProtectionBit()
        bit_12.size = (bit_size, bit_size)
        bit_12.pos = (x_start_block_centre + 2 * x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_12)

        bit_13 = ProtectionBit()
        bit_13.size = (bit_size, bit_size)
        bit_13.pos = (x_start_block_centre, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_13)

        bit_14 = ProtectionBit()
        bit_14.size = (bit_size, bit_size)
        bit_14.pos = (x_start_block_centre + x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_14)

        bit_15 = ProtectionBit()
        bit_15.size = (bit_size, bit_size)
        bit_15.pos = (x_start_block_centre + 2 * x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_15)

        bit_16 = ProtectionBit()
        bit_16.size = (bit_size, bit_size)
        bit_16.pos = (x_start_block_centre, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_16)

        bit_17 = ProtectionBit()
        bit_17.size = (bit_size, bit_size)
        bit_17.pos = (x_start_block_centre + x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_17)

        bit_18 = ProtectionBit()
        bit_18.size = (bit_size, bit_size)
        bit_18.pos = (x_start_block_centre + 2 * x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_18)

        # RIGHT BLOCK

        bit_19 = ProtectionBit()
        bit_19.size = (bit_size, bit_size)
        bit_19.pos = (x_start_block_right, y_start_block)
        self.array_of_bits.append(bit_19)

        bit_20 = ProtectionBit()
        bit_20.size = (bit_size, bit_size)
        bit_20.pos = (x_start_block_right + x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_20)

        bit_21 = ProtectionBit()
        bit_21.size = (bit_size, bit_size)
        bit_21.pos = (x_start_block_right + 2 * x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_21)

        bit_22 = ProtectionBit()
        bit_22.size = (bit_size, bit_size)
        bit_22.pos = (x_start_block_right, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_22)

        bit_23 = ProtectionBit()
        bit_23.size = (bit_size, bit_size)
        bit_23.pos = (x_start_block_right + x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_23)

        bit_24 = ProtectionBit()
        bit_24.size = (bit_size, bit_size)
        bit_24.pos = (x_start_block_right + 2 * x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_24)

        bit_25 = ProtectionBit()
        bit_25.size = (bit_size, bit_size)
        bit_25.pos = (x_start_block_right, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_25)

        bit_26 = ProtectionBit()
        bit_26.size = (bit_size, bit_size)
        bit_26.pos = (x_start_block_right + x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_26)

        bit_27 = ProtectionBit()
        bit_27.size = (bit_size, bit_size)
        bit_27.pos = (x_start_block_right + 2 * x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_27)

        for bit in self.array_of_bits:
            self.add_widget(bit)

    def check_win(self, *args):


        if self.array_of_aliens == []:
            if self.parent.parent:
                # self.sound_track.stop()
                # self.reset()
                self.parent.parent.current = 'third'

    def check_loss(self, *args):
        if self.number_of_lives <= 0:
            if self.parent.parent:
                # self.sound_track.stop()
                # self.reset()
                self.parent.parent.current = 'second'

    def check_ship_alien_collision(self, *args):
        for invader in self.array_of_aliens:
            if invader.pos[1] <= (self.ship.pos[1] + self.ship.size[1]):
                if self.parent.parent:
                    # self.sound_track.stop()
                    # self.reset()
                    self.parent.parent.current = 'second'

    def check_alien_bit_collision(self, *args):
        for invader in self.array_of_aliens:
            for bit in self.array_of_bits:
                if invader.collide_widget(bit):
                    position_in_array = self.array_of_bits.index(bit)
                    del self.array_of_bits[position_in_array]
                    self.remove_widget(bit)

    def number_of_columns_left(self, *args):
        if self.array_of_aliens != []:
            x_coordinates_array = []
            for invader in self.array_of_aliens:
                x_coordinates_array.append(invader.pos[0])
            x_coordinates_set = list(set(x_coordinates_array))
            x_coordinates_set = sorted(x_coordinates_set)
            self.leftmost_x = min(x_coordinates_set)
            self.rightmost_x = max(x_coordinates_set)
            columns_left = len(x_coordinates_set)
            self.num_cols = columns_left

    def display_mothership(self, *args):
        if len(self.array_mothership) < 1:
            mothership = MotherShip()
            mothership.size = (Window.width / 8, Window.width / 8)
            mothership.pos = (0 - mothership.size[0], Window.height - mothership.size[1] * 1.75)
            self.array_mothership.append(mothership)
            self.add_widget(mothership)
            mothership.move()

    # def close(self):
    # self._keyboard.unbind(on_key_down=self.press)
    # self._keyboard.unbind(on_key_up=self.release)
    # self._keyboard = None

    # def press(self, keyboard, keycode, text, modifiers):
    # if self.parent:
    # self.pressed_keys.add(keycode[1])
    # return True

    # def release(self, keyboard, keycode, *args):
    # self.pressed_keys.remove(keycode[1])
    # return True

    # def process_keys(self, *args):

    # if self.pressed_keys.issuperset({'d'}) and self.ship.pos[0] < self.width - (self.ship.size[0]):
    # self.ship.pos[0] += self.width / 120

    # if self.pressed_keys.issuperset({'a'}) and self.ship.pos[0] > 0:
    # self.ship.pos[0] -= self.width / 120

    # if self.pressed_keys.issuperset({'spacebar'}):
    #     if not self.bullet_on_screen:
    #         new_bullet = Bullet()
    #
    #         self.sound_bump_laser.play()
    #         self.add_widget(new_bullet)
    #         new_bullet.size = (self.parent.size[0] / 60, self.parent.size[0] / 16)
    #         new_bullet.pos = (self.ship.pos[0] + self.ship.size[0] / 2 - (self.parent.size[0] / 160),
    #                           self.ship.pos[1] + self.ship.size[1])
    #         self.array_of_bullets.append(new_bullet)
    #         new_bullet.move_up()
    #         self.bullet_on_screen = True

    def process_buttons(self,*args):

        current_state_left = self.left_button.state
        if current_state_left == 'down' and self.ship.pos[0]>=0:
            self.ship.pos[0] -= Window.width/120

        current_state_right = self.right_button.state
        if current_state_right == 'down' and self.ship.pos[0]<=(Window.width-(self.ship.size[0])):
            self.ship.pos[0] += Window.width / 120

        current_state_fire = self.fire_button.state
        if current_state_fire == 'down':

            if not self.bullet_on_screen:
                new_bullet = Bullet()
                self.sound_bump_laser.play()
                self.add_widget(new_bullet)
                new_bullet.size = (self.parent.size[0] / 60, self.parent.size[0] / 16)
                new_bullet.pos = (self.ship.pos[0] + self.ship.size[0] / 2 - (self.parent.size[0] / 160),
                                  self.ship.pos[1] + self.ship.size[1])
                self.array_of_bullets.append(new_bullet)
                new_bullet.move_up()
                self.bullet_on_screen = True

    def shoot_missile(self, instance):
        new_missile = Missile()
        self.sound_bump_missile.play()

        self.add_widget(new_missile)
        new_missile.size = (self.parent.size[0] / 60, self.parent.size[0] / 10)
        new_missile.pos = (instance.pos[0] + instance.size[0] / 2 - (self.parent.size[0] / 100),
                           instance.pos[1] - (self.parent.size[0] / 20))
        new_missile.move_down()

    def aliens_shooting(self, *args):

        x_coordinates_array = []
        for invader in self.array_of_aliens:
            x_coordinates_array.append(invader.pos[0])

        unique_arrays_x = []
        for value in set(x_coordinates_array):
            temp_array = []
            for invader in self.array_of_aliens:
                if invader.pos[0] == value:
                    temp_array.append(invader)
            unique_arrays_x.append(temp_array)

        for group in unique_arrays_x:
            y_vals = []
            for saucer in group:
                y_vals.append(saucer.pos[1])
            lowest_y = min(y_vals)
            for saucer in group:
                chance_variable = random.randint(1, 3)
                if saucer.pos[1] == lowest_y and chance_variable == 1:
                    self.shoot_missile(saucer)
                    pass

########################################################################################################################
########################################################################################################################
    def reset(self, *args):

        self.sound_track.stop()
        self.sound_track.play()

        self.clear_widgets()

        self.add_widget(self.ship)
        self.add_widget(self.my_label)
        # self.add_widget(self.my_reset)

        self.travel_direction = 'right'
        self.bullet_on_screen = False
        # self.pressed_keys = set()
        self.number_of_lives = 3
        self.array_of_aliens = []
        self.array_of_bullets = []
        self.num_cols = 5
        self.array_of_lives = []
        self.array_of_bits = []
        self.leftmost_x = 0
        self.rightmost_x = 0
        self.array_mothership = []
        self.going_right = True
        self.amount_to_animate_by = 0

        # Clock.unschedule(self.process_keys)
        Clock.unschedule(self.check_win)
        Clock.unschedule(self.check_loss)
        Clock.unschedule(self.aliens_shooting)
        Clock.unschedule(self.check_ship_alien_collision)
        Clock.unschedule(self.check_alien_bit_collision)
        Clock.unschedule(self.display_mothership)
        Clock.unschedule(self.number_of_columns_left)

########################################################################################################################
        # DEFINING ALIENS
        x_spacing_between_aliens = self.parent.size[1] / 10
        y_start = self.parent.size[1] - self.parent.size[1] / 12
        y_spacing_between_aliens = self.parent.size[1] / 15

        for x in range(5):
            for y in range(5):
                new_alien = Alien()
                new_alien.size = (Window.width / 10, Window.width / 10)
                new_alien.pos = (x_spacing_between_aliens * x, y_start - y * y_spacing_between_aliens)
                self.array_of_aliens.append(new_alien)

        # FOR PLAYER SHIP...
        self.ship.size = (self.parent.size[0] / 6, self.parent.size[0] / 8)
        # self.ship.pos = (Window.width/2-self.size[0]/2,Window.height*0.05)

        # MOVEMENT AND FIRE BUTTONS...

        b_size = Window.width / 6
        b_size_fire = Window.width / 5
        b_height = Window.height * 0.025
        b_height_fire = Window.height * 0.0175

        self.right_button = Button(text='', size=(b_size, b_size), pos=(Window.width * 0.35, b_height),
                                   background_color=(0, 0, 0, 0))
        with self.right_button.canvas:
            Rectangle(source='triangle_left.png', size=(self.right_button.size), pos=(self.right_button.pos))

        self.left_button = Button(text='', size=(b_size, b_size), pos=(Window.width * 0.05, b_height),
                                  background_color=(0, 0, 0, 0))
        with self.left_button.canvas:
            Rectangle(source='triangle_right.png', size=(self.left_button.size), pos=(self.left_button.pos))

        self.fire_button = Button(text='', size=(b_size_fire, b_size_fire), pos=(Window.width * 0.75, b_height_fire),
                                  background_color=(0, 0, 0, 0))
        with self.fire_button.canvas:
            Rectangle(source='shoot_6.png', size=(self.fire_button.size), pos=(self.fire_button.pos))

        self.add_widget(self.left_button)
        self.add_widget(self.right_button)
        self.add_widget(self.fire_button)

        # IMPORTANT SCHEDULING...
        # Clock.schedule_interval(self.process_keys, 1 / 60)
        Clock.schedule_interval(self.check_win, 1 / 60)
        Clock.schedule_interval(self.check_loss, 1 / 60)
        Clock.schedule_interval(self.aliens_shooting, 1)
        Clock.schedule_interval(self.check_ship_alien_collision, 1 / 60)
        Clock.schedule_interval(self.check_alien_bit_collision, 1 / 60)
        Clock.schedule_interval(self.display_mothership, 10)
        Clock.schedule_interval(self.number_of_columns_left, 1 / 240)

        # ADDING ALIENS
        for invader in self.array_of_aliens:
            self.add_widget(invader)

        # STARTING THE ALIENS MOVING
        for invader in self.array_of_aliens:
            invader.move_right_and_down()

        # 3 MINI SHIPS REPRESENTING LIVES REMAINING
        spacing = Window.width / 30
        new_life_1 = Life()
        new_life_1.size = (Window.width / 15, Window.width / 15)
        new_life_1.pos = (Window.width - (3 * Window.width / 15) - (3 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_1)
        self.add_widget(new_life_1)

        new_life_2 = Life()
        new_life_2.size = (Window.width / 15, Window.width / 15)
        new_life_2.pos = (Window.width - (2 * Window.width / 15) - (2 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_2)
        self.add_widget(new_life_2)

        new_life_3 = Life()
        new_life_3.size = (Window.width / 15, Window.width / 15)
        new_life_3.pos = (Window.width - (1 * Window.width / 15) - (1 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_3)
        self.add_widget(new_life_3)

        # ADDING PROTECTION BITS

        starting_height = Window.height * 0.2
        block_width_height = Window.width / 6
        number_of_bit_columns = 3
        number_of_bit_rows = 3
        bit_size = block_width_height / number_of_bit_columns
        spacing_between_blocks = (Window.width - (3 * block_width_height)) / 4
        x_distance_between_bits = bit_size
        y_distance_between_bits = bit_size

        y_start_block = starting_height
        x_start_block_left = spacing_between_blocks
        x_start_block_centre = (spacing_between_blocks * 2) + (block_width_height)
        x_start_block_right = (spacing_between_blocks * 3) + (block_width_height * 2)

        # MANUALLY ADDING EVERYTHING LIKE AN IDIOT!!! 'CAUSE THE SHORT WAY WAS BUGGY FOR SOME REASON...
        # LEFT BLOCK
        bit_1 = ProtectionBit()
        bit_1.size = (bit_size, bit_size)
        bit_1.pos = (x_start_block_left, y_start_block)
        self.array_of_bits.append(bit_1)

        bit_2 = ProtectionBit()
        bit_2.size = (bit_size, bit_size)
        bit_2.pos = (x_start_block_left + x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_2)

        bit_3 = ProtectionBit()
        bit_3.size = (bit_size, bit_size)
        bit_3.pos = (x_start_block_left + 2 * x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_3)

        bit_4 = ProtectionBit()
        bit_4.size = (bit_size, bit_size)
        bit_4.pos = (x_start_block_left, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_4)

        bit_5 = ProtectionBit()
        bit_5.size = (bit_size, bit_size)
        bit_5.pos = (x_start_block_left + x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_5)

        bit_6 = ProtectionBit()
        bit_6.size = (bit_size, bit_size)
        bit_6.pos = (x_start_block_left + 2 * x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_6)

        bit_7 = ProtectionBit()
        bit_7.size = (bit_size, bit_size)
        bit_7.pos = (x_start_block_left, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_7)

        bit_8 = ProtectionBit()
        bit_8.size = (bit_size, bit_size)
        bit_8.pos = (x_start_block_left + x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_8)

        bit_9 = ProtectionBit()
        bit_9.size = (bit_size, bit_size)
        bit_9.pos = (x_start_block_left + 2 * x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_9)

        # CENTRAL BLOCK

        bit_10 = ProtectionBit()
        bit_10.size = (bit_size, bit_size)
        bit_10.pos = (x_start_block_centre, y_start_block)
        self.array_of_bits.append(bit_10)

        bit_11 = ProtectionBit()
        bit_11.size = (bit_size, bit_size)
        bit_11.pos = (x_start_block_centre + x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_11)

        bit_12 = ProtectionBit()
        bit_12.size = (bit_size, bit_size)
        bit_12.pos = (x_start_block_centre + 2 * x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_12)

        bit_13 = ProtectionBit()
        bit_13.size = (bit_size, bit_size)
        bit_13.pos = (x_start_block_centre, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_13)

        bit_14 = ProtectionBit()
        bit_14.size = (bit_size, bit_size)
        bit_14.pos = (x_start_block_centre + x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_14)

        bit_15 = ProtectionBit()
        bit_15.size = (bit_size, bit_size)
        bit_15.pos = (x_start_block_centre + 2 * x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_15)

        bit_16 = ProtectionBit()
        bit_16.size = (bit_size, bit_size)
        bit_16.pos = (x_start_block_centre, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_16)

        bit_17 = ProtectionBit()
        bit_17.size = (bit_size, bit_size)
        bit_17.pos = (x_start_block_centre + x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_17)

        bit_18 = ProtectionBit()
        bit_18.size = (bit_size, bit_size)
        bit_18.pos = (x_start_block_centre + 2 * x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_18)

        # RIGHT BLOCK

        bit_19 = ProtectionBit()
        bit_19.size = (bit_size, bit_size)
        bit_19.pos = (x_start_block_right, y_start_block)
        self.array_of_bits.append(bit_19)

        bit_20 = ProtectionBit()
        bit_20.size = (bit_size, bit_size)
        bit_20.pos = (x_start_block_right + x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_20)

        bit_21 = ProtectionBit()
        bit_21.size = (bit_size, bit_size)
        bit_21.pos = (x_start_block_right + 2 * x_distance_between_bits, y_start_block)
        self.array_of_bits.append(bit_21)

        bit_22 = ProtectionBit()
        bit_22.size = (bit_size, bit_size)
        bit_22.pos = (x_start_block_right, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_22)

        bit_23 = ProtectionBit()
        bit_23.size = (bit_size, bit_size)
        bit_23.pos = (x_start_block_right + x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_23)

        bit_24 = ProtectionBit()
        bit_24.size = (bit_size, bit_size)
        bit_24.pos = (x_start_block_right + 2 * x_distance_between_bits, y_start_block + 1 * y_distance_between_bits)
        self.array_of_bits.append(bit_24)

        bit_25 = ProtectionBit()
        bit_25.size = (bit_size, bit_size)
        bit_25.pos = (x_start_block_right, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_25)

        bit_26 = ProtectionBit()
        bit_26.size = (bit_size, bit_size)
        bit_26.pos = (x_start_block_right + x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_26)

        bit_27 = ProtectionBit()
        bit_27.size = (bit_size, bit_size)
        bit_27.pos = (x_start_block_right + 2 * x_distance_between_bits, y_start_block + 2 * y_distance_between_bits)
        self.array_of_bits.append(bit_27)

        for bit in self.array_of_bits:
            self.add_widget(bit)

########################################################################################################################
########################################################################################################################

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        return sm

MyApp().run()
