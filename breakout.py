import pygame as p
import random
import time

p.font.init()
p.mixer.init()

beep = p.mixer.Sound(
    '/Users/mattiasgerardhalloran/Desktop/Breakout Pygame/assets/beep.wav')
beep.set_volume(0.3)
scoreFont = p.font.SysFont('arial', 40)
winFont = p.font.SysFont('arial', 100)

height, width = 400, 700
window = p.display.set_mode((width, height))
p.display.set_caption("Breakout")

black = (0, 0, 0)
white = (255, 255, 255)
red = (206, 42, 41)
orange = (229, 137, 10)
yellow = (224, 229, 10)
green = (0, 209, 0)
blue = (10, 78, 229)

player = p.Rect(width/2-50, height-20, 100, 20)
ball = p.Rect(width/2-10, height-41, 20, 20)
background = p.Rect(0, 0, width, height)


def draw(bricks, ballColor, score):
    p.draw.rect(window, black, background)
    p.draw.rect(window, white, player)
    p.draw.rect(window, ballColor, ball)
    scoreText = scoreFont.render(str(score), 1, white)
    window.blit(scoreText, (5, 3))
    for brick in bricks:
        p.draw.rect(window, brick[2], p.Rect(brick[0], brick[1], 100, 19))
    p.display.update()


def playerMovement(keysPressed, playerSpeed):
    if keysPressed[p.K_LEFT] and player.x > 0:
        player.x -= playerSpeed
    if keysPressed[p.K_RIGHT] and player.x + 100 < width:
        player.x += playerSpeed


def BricksCollision(bricks, ballXvelocity, ballYvelocity, fps, playerSpeed, ballColor, score):
    for i in range(len(bricks)):
        brick = p.Rect(bricks[i][0], bricks[i][1], 100, 19)
        if brick.colliderect(ball):
            beep.play()
            ballColor = bricks[i][2]
            if bricks[i][2] == blue:
                fps = 30
                playerSpeed = 12
                score += 10
            elif bricks[i][2] == green:
                fps = 40
                playerSpeed = 9
                score += 20
            elif bricks[i][2] == yellow:
                fps = 50
                playerSpeed = 3/5 * 12
                score += 30
            elif bricks[i][2] == orange:
                fps = 60
                playerSpeed = 3/6 * 12
                score += 40
            elif bricks[i][2] == red:
                fps = 70
                playerSpeed = 3/7 * 12
                score += 100
            bricks[i] = (0, 0, blue)
            if ball.x + 20 <= brick[0] and ball.x >= brick[0] + 100:
                ballXvelocity *= -1
            else:
                ballYvelocity *= -1
    for brick in bricks:
        if brick[0] == 0:
            bricks.remove(brick)
    if score >= 1000:
        p.draw.rect(window, black, background)
        winText = winFont.render('You Win!', 1, white)
        window.blit(winText, (150, 135))
        p.display.update()
        time.sleep(7)
        p.quit()

    return(bricks, ballXvelocity, ballYvelocity, playerSpeed, ballColor, score)


def ballMovement(ballXvelocity, ballYvelocity, keysPressed, lives):
    if ballYvelocity == 0 and ballXvelocity == 0 and lives > 0:
        ballXvelocity = random.randint(-5, 5)
        ballYvelocity = -5
        ball.x = width/2-10
        ball.y = height-41
    if lives == 0:
        p.quit()
    if ball.x < 0 or ball.x > width - 20:
        ballXvelocity *= -1
    if ball.y < 0:
        ballYvelocity *= -1
    if ball.y > player.y:
        lives = lives - 1
        ballYvelocity, ballXvelocity = 0, 0
    if ball.colliderect(player):
        ballYvelocity *= -1
        if keysPressed[p.K_LEFT]:
            ballXvelocity += random.uniform(-0.5, -1.5)
        if keysPressed[p.K_RIGHT]:
            ballXvelocity += random.uniform(0.5, 1.5)
    return ballXvelocity, ballYvelocity, lives


def main():
    ballXvelocity = 0
    ballYvelocity = 0
    fps = 30
    playerSpeed = 12
    lives = 3
    score = 0

    ballColor = white
    bricks = [(50, 50, red), (170, 50, red), (290, 50, red), (410, 50, red), (530, 50, red),
              (50, 90, orange), (170, 90, orange), (290, 90,
                                                    orange), (410, 90, orange), (530, 90, orange),

              (50, 130, yellow), (170, 130, yellow), (290, 130,
                                                      yellow), (410, 130, yellow), (530, 130, yellow),
              (50, 170, green), (170, 170, green), (290, 170,
                                                    green), (410, 170, green), (530, 170, green),
              (50, 210, blue), (170, 210, blue), (290, 210,
                                                  blue), (410, 210, blue), (530, 210, blue)
              ]
    run = True
    while run:

        p.time.Clock().tick(fps)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
                p.quit()
        keysPressed = p.key.get_pressed()
        playerMovement(keysPressed, playerSpeed)
        ballXvelocity, ballYvelocity, lives = ballMovement(
            ballXvelocity, ballYvelocity, keysPressed, lives)
        ball.x += ballXvelocity
        ball.y += ballYvelocity

        bricks, ballXvelocity, ballYvelocity, playerSpeed, ballColor, score = BricksCollision(
            bricks, ballXvelocity, ballYvelocity, fps, playerSpeed, ballColor, score)
        draw(bricks, ballColor, score)


if __name__ == "__main__":
    main()
