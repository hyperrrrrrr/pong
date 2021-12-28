import pygame as p
import random
p.font.init()
p.mixer.init()

beep = p.mixer.Sound(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/beep.wav')
beep.set_volume(0.05)


ball = p.image.load(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/ball.png')
ballPng = p.transform.scale(ball, (20, 20))


one = p.image.load(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/one.png')
one = p.transform.scale(one, (20, 20))
two = p.image.load(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/two.png')
two = p.transform.scale(two, (20, 20))
three = p.image.load(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/three.png')
three = p.transform.scale(three, (20, 20))
four = p.image.load(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/four.png')
four = p.transform.scale(four, (20, 20))
zero = p.image.load(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/zero.png')
zero = p.transform.scale(zero, (20, 20))

playerSpeed = 8
height, width = 400, 700
scoreFont = p.font.SysFont('arial', 40)
window = p.display.set_mode((width, height))
p.display.set_caption("Pong")

black = (0, 0, 0)
white = (255, 255, 255)


player = p.Rect(0, height/2-50, 20, 100)
computer = p.Rect(width-20, height/2-50, 20, 100)
ball = p.Rect(width/2-10, height/2-10, 20, 20)
background = p.Rect(0, 0, width, height)


def draw(playerScore, computerScore):
    p.draw.rect(window, black, background)
    p.draw.rect(window, white, player)
    p.draw.rect(window, white, computer)
    window.blit(ballPng, (ball.x, ball.y))
    #scoreText = scoreFont.render(str(playerScore), 1, white)
    #window.blit(scoreText, (5, 3))
    #scoreText = scoreFont.render(str(computerScore), 1, white)
    #window.blit(scoreText, (width - 25, 3))

    if playerScore == 0:
        playerCurrentScore = zero
    elif playerScore == 1:
        playerCurrentScore = one
    elif playerScore == 2:
        playerCurrentScore = two
    elif playerScore == 3:
        playerCurrentScore = three
    elif playerScore == 4:
        playerCurrentScore = four
    else:
        p.quit()

    if computerScore == 0:
        computerCurrentScore = zero
    elif computerScore == 1:
        computerCurrentScore = one
    elif computerScore == 2:
        computerCurrentScore = two
    elif computerScore == 3:
        computerCurrentScore = three
    elif computerScore == 4:
        computerCurrentScore = four
    else:
        p.quit()

    window.blit(playerCurrentScore, (5, 3))
    window.blit(computerCurrentScore, (width-23, 3))

    p.display.update()


def playerMovement(keysPressed):
    if keysPressed[p.K_UP] and player.y > 0:
        player.y -= playerSpeed
    if keysPressed[p.K_DOWN] and player.y + 100 < height:
        player.y += playerSpeed


def computerMovement(computerSpeed):
    if computer.y + 50 > ball.y and ball.x > 350 and computer.y > 0:
        computer.y -= computerSpeed
    if computer.y + 50 < ball.y and ball.x > 350 and computer.y + 100 < height:
        computer.y += computerSpeed


def ballMovement(ballXvelocity, ballYvelocity, keysPressed, speedIncrement, ballStartVelocity, playerScore, computerScore):
    if ballYvelocity == 0 and ballXvelocity == 0:
        ballYvelocity = random.randint(-5, 5)
        ballXvelocity = ballStartVelocity
        ball.x = width/2-10
        ball.y = height/2-10

    if ball.y < 0 or ball.y + 20 >= height:
        ballYvelocity *= -1

    if ball.colliderect(player):
        beep.play()
        ballXvelocity *= -1
        ballXvelocity += speedIncrement

        if keysPressed[p.K_UP] and player.y > 0:
            ballYvelocity -= 0.5
        if keysPressed[p.K_DOWN] and player.y + 100 < height:
            ballYvelocity += 0.5

    if ball.colliderect(computer):
        beep.play()
        ballXvelocity *= -1
        ballXvelocity -= speedIncrement

    if ball.x < 0:
        computerScore += 1
        ballXvelocity = 0
        ballYvelocity = 0
    if ball.x > width:
        playerScore += 1
        ballXvelocity = 0
        ballYvelocity = 0

    return(ballXvelocity, ballYvelocity, playerScore, computerScore)


def main():
    ballXvelocity = 0
    ballYvelocity = 0

    computerSpeed = 0
    speedIncrement = 0
    ballStartVelocity = -5
    diffchoose = True
    fps = 30

    playerScore = 0
    computerScore = 0

    while diffchoose:
        keysPressed = p.key.get_pressed()
        if keysPressed[p.K_1]:
            computerSpeed = 5
            speedIncrement = 0.5
            ballStartVelocity = -3
            diffchoose = False
        if keysPressed[p.K_2]:
            computerSpeed = 8
            speedIncrement = 0.8
            ballStartVelocity = -5
            diffchoose = False
        if keysPressed[p.K_3]:
            computerSpeed = 12
            speedIncrement = 1.9
            ballStartVelocity = -15
            diffchoose = False
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
                p.quit()
        draw(playerScore, computerScore)

    run = True
    while run:
        p.time.Clock().tick(fps)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
                p.quit()
        keysPressed = p.key.get_pressed()
        playerMovement(keysPressed)

        if playerScore == 5:
            p.quit()
        if computerScore == 5:
            p.quit()

        ballXvelocity, ballYvelocity, playerScore, computerScore = ballMovement(
            ballXvelocity, ballYvelocity, keysPressed, speedIncrement, ballStartVelocity, playerScore, computerScore)
        ball.x += ballXvelocity
        ball.y += ballYvelocity

        computerMovement(computerSpeed)
        draw(playerScore, computerScore)


if __name__ == "__main__":
    main()
