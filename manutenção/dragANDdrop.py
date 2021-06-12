# imports the Pygame library
import pygame

# colors
background_color = (0, 0, 0)
circle_color = (90, 210, 140)
rectangle_color = (90, 180, 210)


class Circle(object):
    def __init__(self, (x, y), radius):
        self.x = x
        self.y = y
        self.radius = radius

    @property
    def position(self):
        return self.x, self.y

    def move_ip(self, (dx, dy)):
        self.x += dx
        self.y += dy

    def collidepoint(self, (x, y)):
        """
        Circle-point collision.
        """
        if (self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2:
            return True
        return False

    def draw(self, surface):
        pygame.draw.circle(surface, circle_color, self.position, self.radius)


class Rectangle(pygame.Rect):
    def __init__(self, (x, y), (width, height)):
        super(Rectangle, self).__init__(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, rectangle_color, self)


def main():
    # initializes Pygame
    pygame.init()

    # creates the window and sets its properties
    pygame.display.set_caption('Drag and drop')  # title
    screen = pygame.display.set_mode((400, 400))  # size

    # creates a clock
    clock = pygame.time.Clock()

    # shapes
    shapes = [
        Circle((280, 280), 100),  # circle
        Rectangle((20, 20), (280, 140))  # rectangle
    ]

    # current selection
    current_selection = None

    # is running?
    running = True

    # main loop (it handles events)
    while running:
        # gets all events from the event queue
        for event in pygame.event.get():
            # 'QUIT' event
            if event.type == pygame.QUIT:
                # stops the loop when the CLOSE button is clicked
                running = False

            # 'MOUSEBUTTONDOWN' event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # press the left mouse button on a shape to set the current selection
                if event.button == 1:
                    for shape in shapes:
                        if shape.collidepoint(event.pos):
                            current_selection = shape
                            break  # only the first shape

            # 'MOUSEBUTTONUP' event
            if event.type == pygame.MOUSEBUTTONUP:
                # release the left mouse button to remove the current selection
                if event.button == 1:
                    current_selection = None

            # 'MOUSEMOTION' event
            if event.type == pygame.MOUSEMOTION:
                # move the mouse by pressing its left button to move the current selection
                if event.buttons[0] == 1:
                    if current_selection:
                        current_selection.move_ip(event.rel)

        # sets the background color
        screen.fill(background_color)

        # draws the shapes
        for shape in reversed(shapes):
            shape.draw(screen)

        # updates the screen
        pygame.display.flip()

        # limits the updates up to 40 FPS (frames per second)
        clock.tick(40)

    # finalizes Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
