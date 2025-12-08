import pygame
from States.Core.StateClass import State


class GameWinState(State):
    def __init__(self, nextstate: str = ""):
        super().__init__(nextstate)
        # Fonts
        self.title_font = pygame.font.Font('Graphics/Text/m6x11.ttf', 48)
        self.btn_font = pygame.font.Font('Graphics/Text/m6x11.ttf', 28)

        # Buttons (centered)
        self.restart_rect = pygame.Rect(0, 0, 240, 64)
        self.quit_rect = pygame.Rect(0, 0, 240, 64)

        self.screen_center = (650, 375)
        self.restart_rect.center = (self.screen_center[0], self.screen_center[1] + 20)
        self.quit_rect.center = (self.screen_center[0], self.screen_center[1] + 110)

        # Background image (optional)
        self.bg = pygame.image.load('Graphics/Backgrounds/gameplayBG.jpg')
        self.bg = pygame.transform.scale(self.bg, (1300, 750))
        # TV overlay (CRT filter)
        self.tvOverlay = pygame.image.load('Graphics/Backgrounds/CRT.png').convert_alpha()
        self.tvOverlay = pygame.transform.scale(self.tvOverlay, (1300, 750))

    def update(self):
        # nothing to update statically here
        self.draw()

    def draw(self):
        # Background
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((6, 6, 20))

        # Panel (centered rectangle)
        panel_w, panel_h = 720, 320
        panel_x = self.screen_center[0] - panel_w // 2
        panel_y = self.screen_center[1] - panel_h // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        # Shadow
        shadow = pygame.Surface((panel_w + 8, panel_h + 8), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 180))
        self.screen.blit(shadow, (panel_x + 6, panel_y + 6))

        # Panel background and border
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill((18, 18, 28, 240))
        pygame.draw.rect(panel_surf, (255, 215, 0), pygame.Rect(0, 0, panel_w, 6))
        pygame.draw.rect(panel_surf, (100, 100, 100), panel_surf.get_rect(), 2, border_radius=8)
        self.screen.blit(panel_surf, (panel_x, panel_y))

        # Title inside panel
        title_surf = self.title_font.render('YOU WIN!', True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(self.screen_center[0], panel_y + 56))
        self.screen.blit(title_surf, title_rect)

        # Buttons positions (inside panel)
        btn_y = panel_y + panel_h - 100
        self.restart_rect.center = (self.screen_center[0] - 140, btn_y)
        self.quit_rect.center = (self.screen_center[0] + 140, btn_y)

        mouse = pygame.mouse.get_pos()
        # Restart button
        if self.restart_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, (30, 200, 30), self.restart_rect, border_radius=8)
        else:
            pygame.draw.rect(self.screen, (20, 160, 20), self.restart_rect, border_radius=8)
        restart_label = self.btn_font.render('Restart', True, 'white')
        self.screen.blit(restart_label, restart_label.get_rect(center=self.restart_rect.center))

        # Quit button (calls exit when clicked)
        if self.quit_rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, (200, 30, 30), self.quit_rect, border_radius=8)
        else:
            pygame.draw.rect(self.screen, (160, 20, 20), self.quit_rect, border_radius=8)
        quit_label = self.btn_font.render('Quit', True, 'white')
        self.screen.blit(quit_label, quit_label.get_rect(center=self.quit_rect.center))

        # TV overlay filter (on top)
        if self.tvOverlay:
            self.screen.blit(self.tvOverlay, (0, 0))

    def userInput(self, events):
        if events.type == pygame.QUIT:
            self.isFinished = True
            self.nextState = "StartState"

        if events.type == pygame.KEYDOWN and events.key == pygame.K_ESCAPE:
            self.isFinished = True
            self.nextState = "StartState"

        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self.restart_rect.collidepoint(mouse):
                self.buttonSound.play()
                self.isFinished = True
                # Next State
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Graphics/Sounds/mainTheme.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                self.nextState = "GameState"
            if self.quit_rect.collidepoint(mouse):
                # Play sound and exit
                self.buttonSound.play()
                exit()    
