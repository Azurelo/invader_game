import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Invaders"

PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2

class SpaceInvadersGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Game lists for sprites
        self.player_list = None
        self.bullet_list = None
        self.enemy_list = None

        # Sounds
        self.shoot_sound = arcade.load_sound("shoot.wav")
        self.hit_sound = arcade.load_sound("hit.wav")

        self.player_sprite = None
        self.enemy_speed = ENEMY_SPEED  
        self.score = 0  
        self.game_over = False  

        # Set up the game
        self.setup()

    def setup(self):
        # Set up the game variables and initialize the sprites.
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Reset score and game over status
        self.score = 0
        self.game_over = False

        # Create the player sprite
        self.player_sprite = arcade.Sprite("player.png", 1)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the enemy sprites
        for x in range(100, SCREEN_WIDTH - 100, 80):
            for y in range(400, SCREEN_HEIGHT - 100, 80):
                enemy = arcade.Sprite("enemy.png", 1)
                enemy.center_x = x
                enemy.center_y = y
                self.enemy_list.append(enemy)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        self.player_list.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

        # Display the score
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)

        # Display game over message
        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2 - 130, SCREEN_HEIGHT / 2, arcade.color.RED, 36)
            arcade.draw_text("Press R to Restart", SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 50, arcade.color.WHITE, 24)

    def on_update(self, delta_time):
        # Movement and game logic.
        if not self.game_over:
            self.bullet_list.update()

            # Check if any enemy reached the screen edges
            hit_edge = False
            for enemy in self.enemy_list:
                enemy.center_x += self.enemy_speed
                if enemy.right > SCREEN_WIDTH or enemy.left < 0:
                    hit_edge = True

            # Move enemies down if one touches the edge and change direciton
            if hit_edge:
                self.enemy_speed *= -1
                for enemy in self.enemy_list:
                    # Move all enemies down together
                    enemy.center_y -= 10  

            # Check for collisions between bullets and enemies
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()
                    for enemy in hit_list:
                        enemy.remove_from_sprite_lists()
                        self.score += 1 

                         # Play the hit sound
                        arcade.play_sound(self.hit_sound)
            # Check if any enemy has reached the player's y position
            for enemy in self.enemy_list:
                if enemy.center_y <= self.player_sprite.center_y:
                    self.game_over = True
                    break

            # Remove off-screen bullets
            for bullet in self.bullet_list:
                if bullet.bottom > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()

            # Check if all enemies are destroyed
            if len(self.enemy_list) == 0:
                self.game_over = True

            # Restrict player movement to the screen
            if self.player_sprite.left < 0:
                self.player_sprite.left = 0
            elif self.player_sprite.right > SCREEN_WIDTH:
                self.player_sprite.right = SCREEN_WIDTH

        # Update player movement
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Handle key press events."""
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.SPACE and not self.game_over:
            # Fire a bullet
            bullet = arcade.Sprite("bullet.png", 0.5)
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)

            # Play the shoot sound
            arcade.play_sound(self.shoot_sound)
        elif key == arcade.key.R and self.game_over:
            # Restart the game
            self.setup()

    def on_key_release(self, key, modifiers):
        """Handle key release events."""
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

# Main 
def main():
    window = SpaceInvadersGame()
    arcade.run()

if __name__ == "__main__":
    main()
