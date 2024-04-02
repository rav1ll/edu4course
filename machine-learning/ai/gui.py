import pygame
import cv2
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


def getNumbers():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 700, 300
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FONT_SIZE = 16

    # Create Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draw Digits")

    # Create fonts
    font = pygame.font.Font(None, FONT_SIZE)

    # Initialize variables
    drawing = False
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(WHITE)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    last_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    pygame.draw.line(canvas, BLACK, last_pos, event.pos, 10)
                    last_pos = event.pos

        # Clear the screen
        screen.fill(WHITE)

        # Draw canvas
        screen.blit(canvas, (0, 0))

        # Update the display
        pygame.display.flip()

    # Capture the canvas as an image
    canvas_image = pygame.surfarray.array3d(canvas)
    canvas_image = np.transpose(canvas_image, (1, 0, 2))  # Transpose the image to match OpenCV format

    # Convert to OpenCV format (BGR)
    canvas_image = cv2.cvtColor(canvas_image, cv2.COLOR_RGB2BGR)

    # Save the image or process it with OpenCV
    cv2.imwrite("canvas_image.png", canvas_image)

    rgb = cv2.cvtColor(canvas_image, cv2.COLOR_BGR2RGB)

    plt.subplot(1, 2, 1)
    plt.title("Original")
    plt.imshow(canvas_image)

    grey = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    _, threshed_img = cv2.threshold(grey, 90, 255, cv2.THRESH_BINARY)
    inv = cv2.bitwise_not(threshed_img)

    plt.subplot(1, 2, 2)
    plt.title("Grey")
    plt.imshow(inv)

    struct = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(inv, struct, iterations=1)
    edges = cv2.Canny(dilated, 30, 200)

    plt.title("edges")
    plt.imshow(edges)

    # 

    contours, hier = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours1 = list(contours)
    contours1.sort(key=lambda x: cv2.boundingRect(x)[0])
    contours = tuple(contours1)
    print('-- Contours sorted')

    results = []

    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        small_image = inv[y:y + h, x:x + w]
        small_image = np.pad(small_image, pad_width=int(w / 2), mode='constant', constant_values=0)
        resized_image = cv2.resize(small_image, (28, 28))

        results.append(resized_image)

        plt.subplot(1, len(contours), i + 1)
        plt.imshow(results[i], cmap=plt.cm.binary)

    results = np.array(results)
    results = results.reshape(len(contours), results.shape[1] * results.shape[1])

    print(results.shape)

    output = pd.DataFrame(results, columns=[("pixel" + str(i)) for i in range(28 * 28)])

    output.to_csv('nums.csv', index=False)

    pygame.quit()
