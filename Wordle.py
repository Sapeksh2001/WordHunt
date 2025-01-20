import random
import pygame
import os

def load_dict(file_name):
    try:
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'r') as file:
            words = file.readlines()
        return [word[:5].upper() for word in words]
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []

DICT_GUESSING = load_dict("D:\Projects\Wordle\dictionary english.txt")
DICT_ANSWERS = load_dict("D:\Projects\Wordle\dictionary wordle.txt")

pygame.init()
ANSWER = random.choice(DICT_ANSWERS)

width = 600
height = 700
margin = 10
T_margin = 100
B_margin = 100
LR_margin = 100

GREY = (70, 70, 70)
GREEN = (6, 214, 160)
YELLOW = (255, 255, 102)

input = ""
guesses = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
unguessed = alphabet
game_over = False
won = False

pygame.font.init()
pygame.display.set_caption("Wordle")

sq_size = (width - 4 * margin - 2 * LR_margin) // 5
font = pygame.font.SysFont("free sans bold", sq_size)
font_small = pygame.font.SysFont("free sans bold", sq_size // 2)

def get_unguessed_letter(guesses):
    guessed_letter = "".join([letter for guess in guesses for letter in guess])
    unguessed_letter = ""
    for letter in alphabet:
        if letter not in guessed_letter:
            unguessed_letter += letter
    return unguessed_letter

def determined_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target = ANSWER.count(letter)
        n_correct = 0
        n_occurence = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_occurence += 1
                    if letter == ANSWER[j]:
                        n_correct += 1
        if n_target - n_correct >= 0:
            return YELLOW
    return GREY

# Create screen
screen = pygame.display.set_mode((width, height))

# Animation loop
animating = True
while animating:
    # Background
    screen.fill("white")

    letter = font_small.render(unguessed, False, GREY)
    surface = letter.get_rect(center=(width // 2, T_margin // 2))
    screen.blit(letter, surface)

    y = T_margin
    for i in range(6):
        x = LR_margin
        for j in range(5):
            square = pygame.Rect(x, y, sq_size, sq_size)
            pygame.draw.rect(screen, GREY, square, width=2, border_radius=5)

            if i < len(guesses):
                color = determined_color(guesses[i], j)
                pygame.draw.rect(screen, color, square, border_radius=5)
                letter = font.render(guesses[i][j], False, (255, 255, 255))
                surface = letter.get_rect(center=(x + sq_size // 2, y + sq_size // 2))
                screen.blit(letter, surface)

            if i == len(guesses) and j < len(input):
                letter = font.render(input[j], False, GREY)
                surface = letter.get_rect(center=(x + sq_size // 2, y + sq_size // 2))
                screen.blit(letter, surface)

            x += sq_size + margin
        y += sq_size + margin

    if game_over:
        if won:
            message = "You Win!"
        else:
            message = f"You Lose! The word was {ANSWER}"
        win_text = font_small.render(message, False, GREY)
        surface = win_text.get_rect(center=(width // 2, height - B_margin // 2 - margin))
        screen.blit(win_text, surface)

    pygame.display.flip()

    # Track user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                animating = False

            if event.key == pygame.K_BACKSPACE:
                if len(input) > 0:
                    input = input[:len(input) - 1]

            elif event.key == pygame.K_RETURN:
                if len(input) == 5:
                    if input in DICT_GUESSING:
                        guesses.append(input)
                        unguessed = get_unguessed_letter(guesses)
                        if input == ANSWER:
                            game_over = True
                            won = True
                        elif len(guesses) == 6:
                            game_over = True
                            won = False
                        input = ""
                    else:
                        # Display a message if the word is invalid
                        error_msg = font_small.render("Invalid word", False, GREY)
                        error_surface = error_msg.get_rect(center=(width // 2, T_margin // 2 + 30))
                        screen.blit(error_msg, error_surface)
                        pygame.display.flip()
                        pygame.time.delay(1000)  # Show the message for a brief moment

            elif event.key == pygame.K_SPACE:
                game_over = False
                won = False
                ANSWER = random.choice(DICT_ANSWERS)
                guesses = []
                unguessed = alphabet
                input = ""

            elif len(input) < 5 and not game_over:
                input += event.unicode.upper()
