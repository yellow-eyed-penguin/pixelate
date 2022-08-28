#!/usr/local/bin/python3
'''
Install pillow and pygame before running
'''
from PIL import Image
import tkinter
import tkinter.filedialog
import pygame
import sys


def pixelate_v1(input_file_path: str, output_file_path: str, pixel_size: int):
    # Open image
    img = Image.open(input_file_path)

    # Resize smoothly down to 16x16 pixels
    imgSmall = img.resize((16,16), resample=Image.Resampling.BILINEAR)

    # Scale back up using NEAREST to original size
    result = imgSmall.resize(img.size, Image.Resampling.NEAREST)

    # Save
    result.save(output_file_path)


def pixelate_v2(input_file_path: str, output_file_path: str, pixel_size: int):
    """
    Create a pixel image from the input image.
    
    Args:
        input_file_path: the path to the source image file to be processed.
        output_file_path: the path to the result file.
        pixel_size: pixel size.
        
    Raises:
        FileNotFoundError: if `input_file_path` does not exist.
        TypeError: if `pixel_size` is not int.
        ValueError: if `pixel_size` is not correct int.
    """
    with Image.open(input_file_path) as image:
        image = image.resize(
            (image.size[0] // pixel_size, image.size[1] // pixel_size),
            Image.NEAREST
        )
        image = image.resize(
            (image.size[0] * pixel_size, image.size[1] * pixel_size),
            Image.NEAREST
        )
        image.save(output_file_path)

#pixelate_v1("./images/artistic.jpg", 'result16.png', 16)
#pixelate_v2("./images/artistic.jpg", 'result32.png', 32)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHTGRAY = (170, 170, 170)
DARKGRAY = (50, 50, 50)
GREEN = (0, 255, 0)
GOLD= (212, 175, 55)
BLUE = (0, 255, 255)

WIDTH = 1536
HEIGHT = 864
FPS = 30

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name
    
def pixelate(path, pixels):
    index = path.rfind('.')
    output_path = path[0:index] + '-pixelated' + path[index:]
    #print(output_path)
    pixelate_v2(path, output_path, pixels)
    return output_path

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

text_color = WHITE
# rendering a text written in
text_load_button = smallfont.render('LOAD IMAGE', True, text_color)
text_loaded = smallfont.render('LOADED IMAGE:', True, text_color)
text_pixelate_button = smallfont.render('PIXELATE IMAGE', True, text_color)
text_pixelated = smallfont.render('PIXELATED IMAGE:', True, text_color)
button_width = 220
button_height = 40
displayed_image_path = None

f = ''
frames = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            window = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                f = prompt_file()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= mouse[0] <= button_width and 0 <= mouse[1] <= button_height:
                f = prompt_file()
            elif width/2 <= mouse[0] <= width/2+button_width and 0 <= mouse[1] <= button_height:
                #print('pixelate')
                displayed_image_path = pixelate(f, 16)

    # draw surface - fill background
    #window.fill(pygame.color.Color('yellow'))
    window.fill(BLACK)
    ## update title to show filename
    pygame.display.set_caption(f"Frames: {frames:10}, File: {f}")
    
    
    # stores the width of the
    # screen into a variable
    width = window.get_width()
      
    # stores the height of the
    # screen into a variable
    height = window.get_height()
    
    
    rect_width = width/2
    rect_height = height/3*2
    # Draw a red rectangle that resizes with the window.
    # left, top, width, heigth
    pygame.draw.rect(window, BLACK, (0,
      height/6, rect_width, rect_height))
    #print(window.get_width()/4,
     # window.get_height()/4, window.get_width()/4,
      #window.get_height()/4)
    pygame.draw.rect(window, BLACK, (width/2,
      height/6, rect_width, rect_height))



    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
    # if mouse is hovered on a button it
    # changes to lighter shade 
    if 0 <= mouse[0] <= button_width and 0 <= mouse[1] <= button_height:
        pygame.draw.rect(window,LIGHTGRAY,[0, 0, button_width, button_height])
    else:
        pygame.draw.rect(window,DARKGRAY,[0, 0, button_width, button_height])
    # superimposing the text onto our button
    window.blit(text_load_button , (0, 8))
    window.blit(text_loaded , (0, height/6-button_height))
    if width/2 <= mouse[0] <= width/2+button_width and 0 <= mouse[1] <= button_height:
        pygame.draw.rect(window,LIGHTGRAY,[width/2, 0, button_width, button_height])
    else:
        pygame.draw.rect(window,DARKGRAY,[width/2, 0, button_width, button_height])
    # superimposing the text onto our button
    window.blit(text_pixelate_button , (width/2, 8))
    window.blit(text_pixelated , (width/2, height/6-button_height))

    if f != '':
        image = pygame.image.load(f)
        img_rect = image.get_rect()
        # image height must be lower than rect_height + same with width & rect_width
        ratio = 1
        calculated_width = ratio * img_rect[2]
        calculated_height = ratio * img_rect[3]
        while calculated_width > rect_width or calculated_height > rect_height:
            ratio -= 0.01
            calculated_width = ratio * img_rect[2]
            calculated_height = ratio * img_rect[3]
        image = pygame.transform.scale(image, (calculated_width, calculated_height))
        #background = pygame.Surface((width,height))
        rect = image.get_rect()
        rect = rect.move((0, height/6))
        # left, top
        window.blit(image, rect)
    
    if displayed_image_path != None:
        image = pygame.image.load(displayed_image_path)
        img_rect = image.get_rect()
        # image height must be lower than rect_height + same with width & rect_width
        ratio = 1
        calculated_width = ratio * img_rect[2]
        calculated_height = ratio * img_rect[3]
        while calculated_width > rect_width or calculated_height > rect_height:
            ratio -= 0.01
            calculated_width = ratio * img_rect[2]
            calculated_height = ratio * img_rect[3]
        image = pygame.transform.scale(image, (calculated_width, calculated_height))
        #background = pygame.Surface((width,height))
        rect = image.get_rect()
        rect = rect.move((width/2, height/6))
        # left, top
        window.blit(image, rect)
    
    # show surfacedisplay_surface.blit(image, (0, 0))
    pygame.display.update()
    # limit frames
    clock.tick(FPS)
    frames += 1
pygame.quit()
#quit()
sys.exit()
