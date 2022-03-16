from pygame import Color

# Sizes
windows_width = 540
windows_height = 640
grid_width = 480
grid_height = 640
square_size = 40
progress_bar_width = 20
goal_hints = {
    "easy": windows_height / 4,
    "medium": windows_height / 2,
    "hard": windows_height * 3 / 4,
}
# Colors
goal_not_reached_color = Color(128, 128, 200)
goal_reached_color = Color(140, 255, 140)
select_color = Color(160, 160, 160)
background_color = Color(255, 255, 255)
overlay_background_color = Color(0, 0, 0, 160)
# Gameplay
goals = {
    "easy": 50,
    "medium": 100,
    "hard": 150,
}
minimum_selection = 3
total_time = {  # in milliseconds, must be > 0
    "easy": 15000,
    "medium": 8000,
    "hard": 4000,
}
infinite_mode = False
