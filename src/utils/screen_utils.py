import pygame

def display_performance_metrics(screen, game_state, center_x, center_y):
    """
    Display performance metrics (search time, memory usage, expanded nodes) on the screen.

    Args:
        screen: The pygame screen to render the metrics.
        game_state: The game state containing performance metrics.
        center_x: The x-coordinate of the center position.
        center_y: The y-coordinate of the center position.
    """
    if game_state.current_level in [1, 2, 3, 4]:
        metrics_font = pygame.font.SysFont('Arial', 24, bold=False)
        search_time_text = metrics_font.render(f"Search Time: {game_state.search_time:.4f} seconds", True, (255, 255, 255))
        memory_usage_text = metrics_font.render(f"Memory Usage: {game_state.memory_usage:.2f} KB", True, (255, 255, 255))
        expanded_nodes_text = metrics_font.render(f"Expanded Nodes: {game_state.expanded_nodes}", True, (255, 255, 255))
        
        # Position metrics below the instruction text
        screen.blit(search_time_text, (center_x - search_time_text.get_width() // 2, center_y + 110))
        screen.blit(memory_usage_text, (center_x - memory_usage_text.get_width() // 2, center_y + 140))
        screen.blit(expanded_nodes_text, (center_x - expanded_nodes_text.get_width() // 2, center_y + 170))