from pygame.mouse import get_pos as get_mouse_pos

class HeldPiece:
    # Intilize holding a piece 
    def __init__(self, surface, offset):
        self.surface = surface
        self.draw_rect = self.surface.get_rect()
        self.offset = offset
        
    # Update piece with the mouse
    def draw_piece(self, display_surface):
        mouse_pos = get_mouse_pos()
        self.draw_rect.x = mouse_pos[0] + self.offset[0]
        self.draw_rect.y = mouse_pos[1] + self.offset[1]

        display_surface.blit(self.surface, self.draw_rect)

    # Sees if the move made by user collides with any valid moves
    def check_collision(self, rect_list):
        for rect in rect_list:
            if rect.colliderect(self.draw_rect):
                return rect
        return None