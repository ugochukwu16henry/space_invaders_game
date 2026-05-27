import random
import json
from pathlib import Path

import arcade


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Space Invaders"

PLAYER_MOVE_SPEED = 380
PLAYER_SHOT_SPEED = 520
ENEMY_SHOT_SPEED = 300
BASE_ENEMY_SPEED = 55
BASE_ENEMY_ROWS = 3
BASE_ENEMY_COLUMNS = 7
ENEMY_HORIZONTAL_PADDING = 70
ENEMY_VERTICAL_PADDING = 55
ENEMY_TOP_OFFSET = 120
WAVE_DROP_DISTANCE = 24
SHOT_COOLDOWN = 0.28
STARTING_LIVES = 3

STATE_START = "start"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

START_SCREEN_CONTROLS = [
    "Left / Right Arrow  - Move ship",
    "Space  - Fire laser",
    "Enter  - Start or restart",
    "F5  - Save game",
    "F9  - Load saved game",
]

START_SCREEN_RULES = [
    "Destroy every enemy ship to clear the wave.",
    "Each enemy hit gives 10 points\ntimes your current level.",
    "Enemies get faster and appear\nin larger groups every level.",
    "You lose a life when an enemy shot hits your ship.",
    "The game ends if your lives reach zero\nor enemies reach your ship.",
]


class SpaceInvadersGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate=1 / 120)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_image_path = None
        self.enemy_image_path = None
        self._load_images()

        self.player = self._create_player_sprite()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 55

        self.player_bullets = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()

        self.left_pressed = False
        self.right_pressed = False

        self.state = STATE_START
        self.score = 0
        self.level = 1
        self.lives = STARTING_LIVES

        self.enemy_direction = 1
        self.enemy_speed = BASE_ENEMY_SPEED
        self.enemy_shot_chance_per_second = 0.18
        self.elapsed_time = 0.0
        self.next_player_shot_time = 0.0
        self.save_file_path = Path(__file__).parent / "savegame.json"
        self.status_message = ""
        self.status_message_time_left = 0.0

        self.shoot_sound = None
        self.explosion_sound = None
        self.game_over_sound = None
        self.background_music = None
        self.background_music_player = None
        self._load_sounds()

        self._setup_level()
        self._start_background_music()

    def _load_images(self):
        local_images = Path(__file__).parent / "images"
        player_image = local_images / "images.jpg"
        enemy_image = local_images / "images (1).jpg"

        self.player_image_path = str(player_image) if player_image.exists() else None
        self.enemy_image_path = str(enemy_image) if enemy_image.exists() else None

    def _create_player_sprite(self):
        if self.player_image_path:
            try:
                player = arcade.Sprite(self.player_image_path)
                player.width = 54
                player.height = 28
                return player
            except Exception:
                pass

        return arcade.SpriteSolidColor(54, 28, arcade.color.AERO_BLUE)

    def _create_enemy_sprite(self):
        if self.enemy_image_path:
            try:
                enemy = arcade.Sprite(self.enemy_image_path)
                enemy.width = 40
                enemy.height = 26
                return enemy
            except Exception:
                pass

        return arcade.SpriteSolidColor(40, 26, arcade.color.BRIGHT_GREEN)

    def _load_sounds(self):
        local_sounds = Path(__file__).parent / "sounds"
        local_shoot = local_sounds / "shoot.wav"
        local_explode = local_sounds / "explode.wav"
        local_game_over = local_sounds / "game_over.wav"
        local_background_music = local_sounds / "Lunar_Flight_game.mp3"

        try:
            self.shoot_sound = arcade.load_sound(str(local_shoot)) if local_shoot.exists() else arcade.load_sound(":resources:sounds/laser1.wav")
            self.explosion_sound = arcade.load_sound(str(local_explode)) if local_explode.exists() else arcade.load_sound(":resources:sounds/explosion1.wav")
            self.game_over_sound = arcade.load_sound(str(local_game_over)) if local_game_over.exists() else arcade.load_sound(":resources:sounds/gameover3.wav")
            self.background_music = arcade.load_sound(str(local_background_music)) if local_background_music.exists() else None
        except Exception:
            self.shoot_sound = None
            self.explosion_sound = None
            self.game_over_sound = None
            self.background_music = None

    def _play_sound(self, sound):
        if sound:
            arcade.play_sound(sound)

    def _start_background_music(self):
        if self.background_music and self.background_music_player is None:
            self.background_music_player = arcade.play_sound(self.background_music, volume=0.6, loop=True)

    def _setup_level(self):
        self.player_bullets = arcade.SpriteList()
        self.enemy_bullets = arcade.SpriteList()
        self.enemies = arcade.SpriteList()

        rows = BASE_ENEMY_ROWS + (self.level - 1)
        cols = BASE_ENEMY_COLUMNS + min(5, self.level - 1)
        self._apply_level_difficulty()

        start_x = ENEMY_HORIZONTAL_PADDING
        start_y = SCREEN_HEIGHT - ENEMY_TOP_OFFSET

        for row in range(rows):
            for col in range(cols):
                enemy = self._create_enemy_sprite()
                enemy.center_x = start_x + col * ENEMY_HORIZONTAL_PADDING
                enemy.center_y = start_y - row * ENEMY_VERTICAL_PADDING

                if enemy.center_x <= SCREEN_WIDTH - ENEMY_HORIZONTAL_PADDING:
                    self.enemies.append(enemy)

        self.enemy_direction = 1
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = 55

    def _apply_level_difficulty(self):
        self.enemy_speed = BASE_ENEMY_SPEED + (self.level - 1) * 12
        self.enemy_shot_chance_per_second = 0.18 + (self.level - 1) * 0.06

    def _save_game(self):
        state_data = {
            "state": self.state,
            "score": self.score,
            "level": self.level,
            "lives": self.lives,
            "player": {
                "x": self.player.center_x,
                "y": self.player.center_y,
            },
            "enemy_direction": self.enemy_direction,
            "elapsed_time": self.elapsed_time,
            "next_player_shot_time": self.next_player_shot_time,
            "enemies": [
                {"x": enemy.center_x, "y": enemy.center_y}
                for enemy in self.enemies
            ],
            "player_bullets": [
                {"x": bullet.center_x, "y": bullet.center_y, "vy": bullet.change_y}
                for bullet in self.player_bullets
            ],
            "enemy_bullets": [
                {"x": bullet.center_x, "y": bullet.center_y, "vy": bullet.change_y}
                for bullet in self.enemy_bullets
            ],
        }

        with self.save_file_path.open("w", encoding="utf-8") as save_file:
            json.dump(state_data, save_file, indent=2)
        self._set_status_message("Game Saved", 2.0)

    def _load_game(self):
        if not self.save_file_path.exists():
            self._set_status_message("No Save File Found", 2.0)
            return

        try:
            with self.save_file_path.open("r", encoding="utf-8") as save_file:
                state_data = json.load(save_file)
        except (json.JSONDecodeError, OSError, ValueError):
            self._set_status_message("Load Failed", 2.0)
            return

        self.state = state_data.get("state", STATE_PLAYING)
        self.score = int(state_data.get("score", 0))
        self.level = max(1, int(state_data.get("level", 1)))
        self.lives = max(0, int(state_data.get("lives", STARTING_LIVES)))

        player_data = state_data.get("player", {})
        self.player.center_x = float(player_data.get("x", SCREEN_WIDTH / 2))
        self.player.center_y = float(player_data.get("y", 55))

        self.enemy_direction = int(state_data.get("enemy_direction", 1))
        self.enemy_direction = 1 if self.enemy_direction >= 0 else -1
        self.elapsed_time = float(state_data.get("elapsed_time", 0.0))
        self.next_player_shot_time = float(state_data.get("next_player_shot_time", 0.0))

        self._apply_level_difficulty()

        self.enemies = arcade.SpriteList()
        for enemy_data in state_data.get("enemies", []):
            enemy = self._create_enemy_sprite()
            enemy.center_x = float(enemy_data.get("x", 0.0))
            enemy.center_y = float(enemy_data.get("y", 0.0))
            self.enemies.append(enemy)

        self.player_bullets = arcade.SpriteList()
        for bullet_data in state_data.get("player_bullets", []):
            bullet = arcade.SpriteSolidColor(6, 18, arcade.color.YELLOW)
            bullet.center_x = float(bullet_data.get("x", 0.0))
            bullet.center_y = float(bullet_data.get("y", 0.0))
            bullet.change_y = float(bullet_data.get("vy", PLAYER_SHOT_SPEED))
            self.player_bullets.append(bullet)

        self.enemy_bullets = arcade.SpriteList()
        for bullet_data in state_data.get("enemy_bullets", []):
            bullet = arcade.SpriteSolidColor(6, 16, arcade.color.ORANGE_RED)
            bullet.center_x = float(bullet_data.get("x", 0.0))
            bullet.center_y = float(bullet_data.get("y", 0.0))
            bullet.change_y = float(bullet_data.get("vy", -ENEMY_SHOT_SPEED))
            self.enemy_bullets.append(bullet)

        self._start_background_music()
        self._set_status_message("Game Loaded", 2.0)

    def _set_status_message(self, message, duration):
        self.status_message = message
        self.status_message_time_left = duration

    def _draw_instruction_panel(self, heading, items, left, top, accent_color, width):
        arcade.draw_text(heading, left, top, accent_color, 21, bold=True)

        line_y = top - 34
        for item in items:
            display_text = f"- {item}"
            arcade.draw_text(display_text, left, line_y, arcade.color.WHITE, 15, width=width, multiline=True)
            line_count = display_text.count("\n") + 1
            line_y -= (line_count * 24) + 10

    def on_draw(self):
        self.clear()

        if self.state == STATE_START:
            arcade.draw_text("SPACE INVADERS", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90, arcade.color.AERO_BLUE, 44, anchor_x="center")
            arcade.draw_text("Defend your ship and survive every wave.", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 136, arcade.color.WHITE, 18, anchor_x="center")
            arcade.draw_lbwh_rectangle_filled(70, 80, SCREEN_WIDTH - 140, 310, (12, 22, 44, 185))
            arcade.draw_lbwh_rectangle_outline(70, 80, SCREEN_WIDTH - 140, 310, arcade.color.AERO_BLUE, 3)
            self._draw_instruction_panel("Controls", START_SCREEN_CONTROLS, 105, 360, arcade.color.YELLOW, 250)
            self._draw_instruction_panel("Rules", START_SCREEN_RULES, 475, 360, arcade.color.LIGHT_GREEN, 260)
            arcade.draw_text("Press ENTER to Start", SCREEN_WIDTH / 2, 78, arcade.color.YELLOW, 24, anchor_x="center")
            if self.status_message_time_left > 0:
                arcade.draw_text(self.status_message, SCREEN_WIDTH / 2, 42, arcade.color.LIGHT_GREEN, 18, anchor_x="center")
            return

        arcade.draw_sprite(self.player)
        self.player_bullets.draw()
        self.enemy_bullets.draw()
        self.enemies.draw()

        arcade.draw_text(f"Score: {self.score}", 18, SCREEN_HEIGHT - 36, arcade.color.WHITE, 18)
        arcade.draw_text(f"Lives: {self.lives}", 200, SCREEN_HEIGHT - 36, arcade.color.WHITE, 18)
        arcade.draw_text(f"Level: {self.level}", 340, SCREEN_HEIGHT - 36, arcade.color.WHITE, 18)
        arcade.draw_text("F5 Save   F9 Load", SCREEN_WIDTH - 170, SCREEN_HEIGHT - 36, arcade.color.LIGHT_GRAY, 14)

        if self.status_message_time_left > 0:
            arcade.draw_text(self.status_message, SCREEN_WIDTH / 2, 46, arcade.color.LIGHT_GREEN, 18, anchor_x="center")

        if self.state == STATE_GAME_OVER:
            arcade.draw_lbwh_rectangle_filled(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 130))
            arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 45, arcade.color.RED, 52, anchor_x="center")
            arcade.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 6, arcade.color.WHITE, 24, anchor_x="center")
            arcade.draw_text("Press ENTER to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 54, arcade.color.YELLOW, 22, anchor_x="center")

    def _shoot_player_bullet(self):
        bullet = arcade.SpriteSolidColor(6, 18, arcade.color.YELLOW)
        bullet.center_x = self.player.center_x
        bullet.center_y = self.player.center_y + 20
        bullet.change_y = PLAYER_SHOT_SPEED
        self.player_bullets.append(bullet)
        self._play_sound(self.shoot_sound)

    def _shoot_enemy_bullet(self, enemy):
        bullet = arcade.SpriteSolidColor(6, 16, arcade.color.ORANGE_RED)
        bullet.center_x = enemy.center_x
        bullet.center_y = enemy.center_y - 16
        bullet.change_y = -ENEMY_SHOT_SPEED
        self.enemy_bullets.append(bullet)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.F5:
            self._save_game()
        elif key == arcade.key.F9:
            self._load_game()
        elif key == arcade.key.SPACE and self.state == STATE_PLAYING:
            if self.elapsed_time >= self.next_player_shot_time:
                self._shoot_player_bullet()
                self.next_player_shot_time = self.elapsed_time + SHOT_COOLDOWN
        elif key == arcade.key.ENTER and self.state in {STATE_START, STATE_GAME_OVER}:
            self._restart_game()

    def on_key_release(self, key, _modifiers):
        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def _restart_game(self):
        self.state = STATE_PLAYING
        self.score = 0
        self.level = 1
        self.lives = STARTING_LIVES
        self.elapsed_time = 0.0
        self.next_player_shot_time = 0.0
        self._setup_level()
        self._start_background_music()

    def on_close(self):
        if self.background_music_player:
            self.background_music_player.pause()
            self.background_music_player = None
        super().on_close()

    def _update_player(self, delta_time):
        move_dir = (1 if self.right_pressed else 0) - (1 if self.left_pressed else 0)
        self.player.center_x += move_dir * PLAYER_MOVE_SPEED * delta_time

        half_width = self.player.width / 2
        if self.player.center_x < half_width:
            self.player.center_x = half_width
        if self.player.center_x > SCREEN_WIDTH - half_width:
            self.player.center_x = SCREEN_WIDTH - half_width

    def _update_bullets(self, delta_time):
        for bullet in self.player_bullets:
            bullet.center_y += bullet.change_y * delta_time

        for bullet in self.enemy_bullets:
            bullet.center_y += bullet.change_y * delta_time

        for bullet in list(self.player_bullets):
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        for bullet in list(self.enemy_bullets):
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def _update_enemies(self, delta_time):
        if not self.enemies:
            return

        should_change_direction = False

        for enemy in self.enemies:
            enemy.center_x += self.enemy_direction * self.enemy_speed * delta_time
            if enemy.right >= SCREEN_WIDTH - 12 or enemy.left <= 12:
                should_change_direction = True

        if should_change_direction:
            self.enemy_direction *= -1
            for enemy in self.enemies:
                enemy.center_y -= WAVE_DROP_DISTANCE

        enemy_count = len(self.enemies)
        chance_this_frame = min(0.55, self.enemy_shot_chance_per_second * delta_time * max(1, enemy_count / 8))
        if random.random() < chance_this_frame:
            shooter = random.choice(self.enemies)
            self._shoot_enemy_bullet(shooter)

    def _handle_collisions(self):
        for bullet in list(self.player_bullets):
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemies)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.score += 10 * self.level
                self._play_sound(self.explosion_sound)

        for bullet in list(self.enemy_bullets):
            if arcade.check_for_collision(bullet, self.player):
                bullet.remove_from_sprite_lists()
                self.lives -= 1
                if self.lives <= 0:
                    self._trigger_game_over()

        for enemy in self.enemies:
            if enemy.bottom <= self.player.top + 8 or arcade.check_for_collision(enemy, self.player):
                self._trigger_game_over()
                break

    def _check_level_progression(self):
        if not self.enemies and self.state == STATE_PLAYING:
            self.level += 1
            self._setup_level()

    def _trigger_game_over(self):
        if self.state != STATE_GAME_OVER:
            self.state = STATE_GAME_OVER
            self._play_sound(self.game_over_sound)

    def on_update(self, delta_time):
        if self.state != STATE_PLAYING:
            if self.status_message_time_left > 0:
                self.status_message_time_left = max(0.0, self.status_message_time_left - delta_time)
            return

        self.elapsed_time += delta_time
        if self.status_message_time_left > 0:
            self.status_message_time_left = max(0.0, self.status_message_time_left - delta_time)
        self._update_player(delta_time)
        self._update_bullets(delta_time)
        self._update_enemies(delta_time)
        self._handle_collisions()
        self._check_level_progression()


if __name__ == "__main__":
    window = SpaceInvadersGame()
    arcade.run()
