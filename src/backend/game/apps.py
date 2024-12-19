import asyncio
import threading

from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    def ready(self):
        # Call your function here
        def run_main():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            from AI.ai_game import main  # Import inside to avoid conflicts during app loading
            main()

        # thread = threading.Thread(target=run_main)
        # thread.daemon = True  # Ensures the thread will stop when the main program stops
        # thread.start()
