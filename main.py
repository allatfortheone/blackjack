import pygame
import random
import sys
import time

pygame.init()

# dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("toylat")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 48)

#  variables
game_state = "menu"
player_hand = []
dealer_hand = []
deck = []
game_outcome = ""
can_hit = True

# Card parameters
CARD_WIDTH = 80
CARD_HEIGHT = 120
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def create_deck():
    return [{'rank': rank, 'suit': suit} for suit in SUITS for rank in RANKS] * 4

def calculate_hand(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card['rank']
        if rank in ['J', 'Q', 'K']:
            value += 10
        elif rank == 'A':
            value += 11
            aces += 1
        else:
            value += int(rank)

    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1:
            time.sleep(0.2)
            #timer for button delay    ~
            return True
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    draw_text(text, font, BLACK, screen, x + 10, y + 10)
    return False

def deal_initial_hands():
    global player_hand, dealer_hand, deck
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

def game_screen():
    global game_state, game_outcome, can_hit

    # Draw dealer's hand
    draw_text("Dealer's Hand", font, WHITE, screen, 20, 20)
    for i, card in enumerate(dealer_hand):
        x = 20 + i * (CARD_WIDTH + 10)
        y = 60
        if i == 0 and game_outcome == "":
            pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
            draw_text("?", font, BLACK, screen, x + 30, y + 50)
        else:
            pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
            draw_text(card['rank'], font, BLACK, screen, x + 10, y + 10)
            draw_text(card['suit'], font, RED if card['suit'] in ['♥','♦'] else BLACK, 
                     screen, x + 10, y + 40)

    # Draw player's hand
    draw_text("Your Hand", font, WHITE, screen, 20, 220)
    for i, card in enumerate(player_hand):
        x = 20 + i * (CARD_WIDTH + 10)
        y = 260
        pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
        draw_text(card['rank'], font, BLACK, screen, x + 10, y + 10)
        draw_text(card['suit'], font, RED if card['suit'] in ['♥','♦'] else BLACK, 
                 screen, x + 10, y + 40)

    # Show hand values
    if game_outcome != "":
        dealer_value = calculate_hand(dealer_hand)
        draw_text(f"Dealer's Total: {dealer_value}", font, WHITE, screen, 20, 180)
    player_value = calculate_hand(player_hand)
    draw_text(f"Your Total: {player_value}", font, WHITE, screen, 20, 440)

    # Game outcome messages
    if game_outcome:
        draw_text(game_outcome, title_font, WHITE, screen, 250, 200)
        if draw_button("Play Again", 300, 300, 200, 50, GRAY, WHITE):
            new_round()
        if draw_button("Main Menu", 300, 370, 200, 50, GRAY, WHITE):
            game_state = "menu"
    else:
        # Game buttons
        if can_hit:
            if draw_button("Hit", 600, 400, 150, 50, GRAY, WHITE):
                player_hit()
        if draw_button("Stand", 600, 480, 150, 50, GRAY, WHITE):
            dealer_turn()

def player_hit():
    global player_hand, deck, game_outcome, can_hit
    player_hand.append(deck.pop())
    player_value = calculate_hand(player_hand)

    if player_value > 21:
        game_outcome = "Bust! You lose!"
        can_hit = False



def dealer_turn():
    global game_outcome, can_hit
    can_hit = False
    dealer_value = calculate_hand(dealer_hand)
    player_value = calculate_hand(player_hand)

    while dealer_value < 17:
        dealer_hand.append(deck.pop())
        dealer_value = calculate_hand(dealer_hand)

    if dealer_value > 21:
        game_outcome = "Dealer busts! You win!"
    elif dealer_value > player_value:
        game_outcome = "Dealer wins!"
    elif player_value > dealer_value:
        game_outcome = "You win!"
    else:
        game_outcome = "Push!"

def new_round():
    global deck, player_hand, dealer_hand, game_outcome, can_hit
    if len(deck) < 15:
        deck = create_deck()
        random.shuffle(deck)
    game_outcome = ""
    can_hit = True
    deal_initial_hands()

def main_menu():
    screen.fill(GREEN)
    draw_text("Blackjack", title_font, WHITE, screen, 300, 100)

    if draw_button("Play", 300, 250, 200, 50, GRAY, WHITE):
        global game_state
        game_state = "game"
        new_round()

    if draw_button("Quit", 300, 320, 200, 50, GRAY, WHITE):
        pygame.quit()
        sys.exit()

# Main game loop
running = True
while running:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "menu":
        main_menu()
    elif game_state == "game":
        game_screen()

    pygame.display.flip()
    pygame.image.load("./touch.png")
pygame.quit()
sys.exit()
