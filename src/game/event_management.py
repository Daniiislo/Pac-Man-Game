from pygame import (K_DOWN, K_LEFT, K_RIGHT, K_UP, K_ESCAPE, KEYDOWN, QUIT)
import pygame

class EventHandler:
    def __init__(self, screen, game_state, screen_manager):
        self.screen = screen
        self.game_state = game_state
        self.screen_manager = screen_manager
        self.menu_result = None

    def handle_menu_events(self, events, menu):
        """Handle events for the main menu"""
        return menu.handle_events(events)

    def handle_test_case_selector_events(self, events, test_case_selector):
        """Handle events for the test case selector"""
        return test_case_selector.handle_events(events)

    def handle_gameplay_events(self, event):
        """Handle events during active gameplay"""
        if event.type == pygame.KEYDOWN:
            # Handle keydown events for Pacman movement
            if event.key == pygame.K_LEFT:
                self.game_state.next_direction = 'l'
            elif event.key == pygame.K_RIGHT:
                self.game_state.next_direction = 'r'
            elif event.key == pygame.K_UP:
                self.game_state.next_direction = 'u'
            elif event.key == pygame.K_DOWN:
                self.game_state.next_direction = 'd'
            # Add escape key to return to menu
            elif event.key == pygame.K_ESCAPE:
                self.game_state.reset_game()
                self.screen_manager.reset_screen_state()
                return True

        return False

    def handle_game_over_events(self, event):
        """Handle events when game is over"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                # Reset game when Enter or Escape is pressed
                self.game_state.reset_game()
                self.screen_manager.reset_screen_state()
                return True

        return False

    def handle_all_events(self, events):
        """Central event handling method that delegates to specific handlers"""
        for event in events:
            if event.type == pygame.QUIT:
                self.game_state.running = False
                return False

        if not self.game_state.game_started:
            # Not handling menu events here - that's done in screen_management
            return None
        elif self.game_state.game_over:
            for event in events:
                if self.handle_game_over_events(event):
                    return True
        else:
            for event in events:
                if self.handle_gameplay_events(event):
                    return True

        return None
