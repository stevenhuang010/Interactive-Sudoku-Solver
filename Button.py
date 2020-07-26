import pygame

class Button: 
    def __init__(self, color, border_color, x, y, width, height, label, label_color, font_size):
        #button color
        self.color = color
        self.border_color = border_color
        #upper left corner x, y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #text label
        self.label = label
        #text color
        self.label_color = label_color
        #font size
        self.font_size = font_size


    def draw(self, scene):
        #draws the rectangle and the bborder around it
        pygame.draw.rect(scene, self.color, [self.x, self.y, self.width, self.height])
        pygame.draw.rect(scene, self.border_color, [self.x, self.y, self.width, self.height], 2)
        #centers font in the middle of the button
        font = pygame.font.SysFont('segoescript', self.font_size)
        label_width, label_height = font.size(self.label)
        label = font.render(self.label, True, self.label_color)
        scene.blit(label, (self.x + (self.width - label_width) // 2, self.y + (self.height - label_height) // 2))

    #returns whether the mouse is currently on the button
    def is_hovering(self, pos):
        return pos[0] >= self.x and pos[0] <= self.x + self.width and pos[1] >= self.y and pos[1] <= self.y + self.height
