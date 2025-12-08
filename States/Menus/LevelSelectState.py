import pygame
from Deck.DeckManager import DeckManager
from States.Core.StateClass import State
from States.Core.PlayerInfo import PlayerInfo

class LevelSelectState(State):
    def __init__(self, playerinfo: PlayerInfo = None, nextstate: str = "", deckmanager: DeckManager = None):
        super().__init__(nextstate)
        
        #--------------------Player Info and Screenshot---------------------------
        self.playerInfo = playerinfo # PlayerInfo object
        self.bg = State.screenshot # Screenshot of the last game state
        self.deckManager = deckmanager # DeckManager object

        # -------------------Load CRT Overlay-------------------------------------
        self.tvOverlay = pygame.image.load('Graphics/Backgrounds/CRT.png').convert_alpha()
        self.tvOverlay = pygame.transform.scale(self.tvOverlay, (1300, 750))
        
        # -------------------------Fonts used in the UI---------------------------
        self.font = pygame.font.Font('Graphics/Text/m6x11.ttf', 30)
        self.font2 = pygame.font.Font('Graphics/Text/m6x11.ttf', 22)
        self.font3 = pygame.font.Font('Graphics/Text/m6x11.ttf', 60)
        self.font4 = pygame.font.Font('Graphics/Text/m6x11.ttf', 40)
        
        #----------- Layout for multiple sublevel Cards ---------------------------
        self.cardWidth = 280
        self.cardHeight = 450
        self.cardSpacing = 40
        self.cardsStartX = 280
        self.cardsStartY = 150
        
        # Store card rects for each sublevel
        self.sublevelcards = []
        
        self.continueButtonRect = pygame.Rect(0, 0, 300, 80)
        self.continueButtonRect.centerx = 650
        self.continueButtonRect.centery = 650
        #-------------------------------------------------------------------------
    def update(self):
        self.draw()

    def draw(self):
        # Draw the screenshot background, if available
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        
        # Semi-transparent overlay
        overlay = pygame.Surface((1300, 750), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw level Cards and continue button
        self.drawlevelcards()
        self.drawcontinuebutton()
        
        # CRT overlay effect
        self.screen.blit(self.tvOverlay, (0, 0))

    """This function handles user input for the LevelSelectState,
    when the player press CONTINUE button, it updates the player's stats.
    
    The player score resets to 0, and the target score is updated, if the next level is a
    boss level, it will reset stats according to the boss's rules."""
    
    def userinput(self, events):
    # Handle mouse click on CONTINUE button
        if events.type == pygame.MOUSEBUTTONDOWN and events.button == 1:
            mousepos = events.pos
            # Check if the continue button was clicked
            if self.continueButtonRect.collidepoint(mousepos):
                # Update level manager to reflect completed sublevel
                self.playerInfo.levelFinished = False
                
                # just helper variables to write less LOL
                lm = self.playerInfo.levelManager
                nxt = lm.next_unfinished_sublevel()

                # If there's no next sublevel, the player likely advanced past the last ante -> Win
                if nxt is None:
                    # Ensure LevelManager flagged the win and transition to GameWinState
                    lm.playerWins = True
                    self.isFinished = True
                    self.nextState = "GameWinState"
                    return

                # If there's a next sublevel, set it as current
                lm.curSubLevel = nxt
                # TODO (TASK 9.2) - Adjust player limits and reset values based on the current Boss Blind.
                #   Implement conditional logic that modifies the player's hand and discard limits depending
                #   on which boss is active.
                #   Finally, make sure to reset the player’s round score to 0 at the end of this setup.
                #   Avoid unnecessary repetition—use clear condition structure to make the logic readable.


                self.playerInfo.triggerFaceDownFirstHand = False
                self.playerInfo.triggerFaceDownFaces = False
                self.playerInfo.triggerHook = False
                self.playerInfo.scoreModifier = 1.0
                self.playerInfo.disableStraights = False

                # -----------------------------------------
                # 2. Apply boss effect based on boss name
                # -----------------------------------------
                boss = lm.curSubLevel.bossName

                if boss == "The Mark":
                    self.playerInfo.triggerFaceDownFaces = True

                elif boss == "The Needle":
                    self.playerInfo.handLimit = 1

                elif boss == "The House":
                    self.playerInfo.triggerFaceDownFirstHand = True

                elif boss == "The Hook":
                    self.playerInfo.triggerHook = True

                elif boss == "The Water":
                    self.playerInfo.discardLimit = 0

                elif boss == "The Manacle":
                    self.playerInfo.handLimit -= 1

                elif boss == "The Club":
                    self.playerInfo.scoreModifier = 0.75

                elif boss == "The Goad":
                    self.playerInfo.disableStraights = True


                self.playerInfo.handLimit = max(1, self.playerInfo.handLimit)
                self.playerInfo.discardLimit = max(0, self.playerInfo.discardLimit)

                self.playerInfo.roundScore = 0

                

                self.deckManager.resetDeck = True
                self.isFinished = True
                self.nextState = "GameState"
                self.buttonSound.play()

    def drawlevelcards(self):
        # Make sure there's a current level
        if self.playerInfo.levelManager.curLevel is None:
            return
        # Get current sublevel list of the player's ante
        sublevels = self.playerInfo.levelManager.curLevel
        # Clear previous card rects
        self.sublevelcards = []

        # Dict of boss with their abilities
        # TODO (TASK 9.1) - Define a dictionary called `boss_abilities` that maps each Boss Blind’s name to its special effect.
        #   Each key should be the name of a boss (e.g., "The Mark", "The Needle", etc.), and each value should describe
        #   what unique restriction or ability that boss applies during the round.
        #   This dictionary will later be used to look up and apply special effects based on which boss is active.
        boss_abilities = {
            "The Mark": "All Face cards are drawn face down.",
            "The Needle": "Play only 1 hand.",
            "The House": "First hand is drawn face down.",
            "The Hook": "Discards 2 random cards held in hand after every played hand.",
            "The Water": "Start with 0 discards.",
            "The Manacle": "-1 hand size.",
            "The Club": "All scoring chips reduced by 25%.",
            "The Goad": "Straights cannot be played this round."
        }

        # Dict of boss with their color schemes
        # key - boss name : str, value - (header color : tuple, background color : tuple)
        boss_colors = {
            "The Mark": ((120, 40, 160), (60, 30, 80)),        # purple
            "The Needle": ((180, 20, 20), (80, 20, 20)),       # crimson
            "The House": ((200, 160, 20), (100, 80, 10)),      # gold/bronze
            "The Hook": ((20, 150, 140), (10, 70, 80)),        # teal
            "The Water": ((30, 120, 200), (10, 50, 90)),       # blue
            "The Manacle": ((90, 90, 90), (40, 40, 40)),       # steel/gray
            "The Club": ((20, 120, 40), (10, 60, 30)),         # green
            "The Goad": ((70, 40, 140), (30, 20, 70)),         # indigo
        }

        #---------------------------Draw each sublevel card ---------------------------
        for i, sublevel in enumerate(sublevels):
            cardx = self.cardsStartX + i * (self.cardWidth + self.cardSpacing)
            cardy = self.cardsStartY
            
            cardsurface = pygame.Surface((self.cardWidth, self.cardHeight), pygame.SRCALPHA)
            
            cardrect = pygame.Rect(cardx, cardy, self.cardWidth, self.cardHeight)
            self.sublevelcards.append({
                'rect': cardrect,
                'sublevel': sublevel
            })
            
            # Sections of the card
            headerrect = pygame.Rect(10, 10, self.cardWidth - 20, 50)
            blindimagerect = pygame.Rect(10, 70, self.cardWidth - 20, 140)
            scorerect = pygame.Rect(10, 220, self.cardWidth - 20, 80)
            statusrect = pygame.Rect(10, 310, self.cardWidth - 20, 60)
            
            # Header and background colors by blind type
            if sublevel.blind.name == "SMALL":
                header_color = (70, 130, 180)
                bg_color = (40, 65, 90)
            elif sublevel.blind.name == "BIG":
                header_color = (255, 140, 0)
                bg_color = (127, 70, 0)
            else:
                header_color = (128, 128, 128)
                bg_color = (64, 64, 64)

            # If this sublevel is a boss, prefer boss-specific colors
            boss_name = sublevel.bossLevel
            if boss_name:
                override = boss_colors.get(boss_name)
                if override:
                    header_color, bg_color = override
            
            pygame.draw.rect(cardsurface, bg_color, cardsurface.get_rect(), border_radius=10)
            pygame.draw.rect(cardsurface, header_color, headerrect, border_radius=10)
            pygame.draw.rect(cardsurface, (30, 30, 30), blindimagerect, border_radius=10)
            pygame.draw.rect(cardsurface, (30, 30, 30), scorerect, border_radius=10)
            
            # Header Text
            if sublevel.bossLevel:
                headertext = self.font.render(f"BOSS: {sublevel.bossLevel.upper()}", False, (255, 255, 255))
            else:
                headertext = self.font.render(f"{sublevel.blind.name} BLIND", False, (255, 255, 255))
            headertextrect = headertext.get_rect(center=headerrect.center)
            cardsurface.blit(headertext, headertextrect)
            
            # Blind image
            if sublevel.image:
                scaledimage = pygame.transform.scale(sublevel.image, (140, 120))
                imagerect = scaledimage.get_rect(center=blindimagerect.center)
                cardsurface.blit(scaledimage, imagerect)
            
            # Score requirement
            scorelabel = self.font2.render("Score at least", False, (200, 200, 200))
            scorevalue = self.font3.render(str(sublevel.score), False, (255, 0, 0))
            scorelabelrect = scorelabel.get_rect(centerx=scorerect.centerx, top=scorerect.top + 12)
            scorevaluerect = scorevalue.get_rect(centerx=scorerect.centerx, top=scorerect.top + 40)
            cardsurface.blit(scorelabel, scorelabelrect)
            cardsurface.blit(scorevalue, scorevaluerect)

            # Boss ability Text
            ability_text = None
            if sublevel.bossLevel: 
                ability_text = boss_abilities.get(sublevel.bossLevel)
            
            nextunfinished = self.playerInfo.levelManager.next_unfinished_sublevel()
            
            if sublevel.finished:
                # COMPLETED
                statustext = self.font4.render("COMPLETED", False, (100, 255, 100))
                statustextrect = statustext.get_rect(center=statusrect.center)
                cardsurface.blit(statustext, statustextrect)
                
                darkoverlay = pygame.Surface((self.cardWidth, self.cardHeight), pygame.SRCALPHA)
                darkoverlay.fill((0, 0, 0, 160))
                cardsurface.blit(darkoverlay, (0, 0))
            elif nextunfinished and nextunfinished == sublevel:
                # ACTIVE
                statustext = self.font4.render("ACTIVE", False, (255, 200, 100))
                statustextrect = statustext.get_rect(center=statusrect.center)
                cardsurface.blit(statustext, statustextrect)
            else:
                # LOCKED
                statustext = self.font4.render("LOCKED", False, (150, 150, 150))
                statustextrect = statustext.get_rect(center=statusrect.center)
                cardsurface.blit(statustext, statustextrect)
                
                lockoverlay = pygame.Surface((self.cardWidth, self.cardHeight), pygame.SRCALPHA)
                lockoverlay.fill((0, 0, 0, 80))
                cardsurface.blit(lockoverlay, (0, 0))
            
            # Boss ability description
            if ability_text:
                abilityfont = self.font
                abilitysurf = abilityfont.render(ability_text, False, (245, 245, 245))
                # place just below the status rect
                abilityrect = abilitysurf.get_rect(centerx=scorerect.centerx, top=statusrect.top + statusrect.height + 8)
                pad_x, pad_y = 12, 8
                bg_rect = abilityrect.inflate(pad_x * 2, pad_y * 2)
                panel = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                panel_color = (header_color[0], header_color[1], header_color[2], 200)
                panel.fill(panel_color)
                cardsurface.blit(panel, bg_rect.topleft)
                cardsurface.blit(abilitysurf, abilityrect)

            # Border by status
            if nextunfinished and nextunfinished == sublevel:
                bordercolor = (255, 200, 100)
                borderwidth = 4
            elif sublevel.finished:
                bordercolor = (100, 255, 100)
                borderwidth = 3
            else:
                bordercolor = (80, 80, 80)
                borderwidth = 2
            
            pygame.draw.rect(cardsurface, bordercolor, cardsurface.get_rect(), width=borderwidth, border_radius=10)
            self.screen.blit(cardsurface, (cardx, cardy))

    def drawcontinuebutton(self):
        #--- Draw CONTINUE Button ---
        mouse = pygame.mouse.get_pos()
        hover = self.continueButtonRect.collidepoint(mouse)
        
        if hover:
            buttoncolor = (0, 139, 0)
        else:
            buttoncolor = (0, 128, 0)

        pygame.draw.rect(self.screen, buttoncolor, self.continueButtonRect, border_radius=10)
        
        continuetext = self.font.render("CONTINUE", False, (255, 255, 255))
        continuetextrect = continuetext.get_rect(center=self.continueButtonRect.center)
        self.screen.blit(continuetext, continuetextrect)
