#TODO: FIX OR DELETE
import wisualia
from wisualia.shapes import circle, paint
from wisualia.modifiers import Rotate, Move
from wisualia.patterns import ImagePattern, RGBA
from wisualia.image import Image
from wisualia.animation import animate

# We open a png image outside of loop() to keep programm fast.
imag = Image.from_png('example.png')

def loop(t):
    if t<1:
        print(1)
        print('Lets draw some circles.')
        for x in range(-2, 3):
            for y in range(-2, 3):
                circle((x,y), 0.5)
        print('They are green by default.')

    if 1<=t<2:
        print(2)
        print('We can use a different color')
        for x in range(-2, 3):
            for y in range(-2, 3):
                circle((x,y), 0.5, RGBA(1,0,0))
    if 2<=t<3:
        print(3)
        print('We can also use an image.')
        for x in range(-2, 3):
            for y in range(-2, 3):
                circle((x,y), 0.5, ImagePattern(imag, pixels_per_unit=40))
    if 3<=t<4:
        print(4)
        print('We can display the full image with paint function')
        paint(ImagePattern(imag, pixels_per_unit=40))
        print('Colors are also patterns and can be painted.')
        print('Lets paint everything over with a red tone.')
        paint(RGBA(1,0,0,0.2))
    if 4<=t<5:
        print(5)
        print('Lets apply a transformation to our drawing')
        with Rotate(45):
            for x in range(-2, 3):
                for y in range(-2, 3):
                    circle((x,y), 0.5, ImagePattern(imag, pixels_per_unit=40))
            print('Everything inside Rotate block is rotated by 45 degrees.')
    if 5<=t<6:
        print(6)
        print('But we can rotate only our ImagePattern.')
        with Rotate(45):
            pattern = ImagePattern(imag, pixels_per_unit=40)
        for x in range(-2, 3):
            for y in range(-2, 3):
                circle((x,y), 0.5, pattern)
    if 6<=t<7:
        print(7)
        print('Or only our circles.')

        pattern = ImagePattern(imag, pixels_per_unit=40)

        with Rotate(45):
            for x in range(-2, 3):
                for y in range(-2, 3):
                    circle((x,y), 0.5, pattern)
    if 7<=t<8:
        print(8)
        print('But we can also draw our circles with Move blocks')
        print('and use separate ImagePattern for each circle.')
        for x in range(-2, 3):
            for y in range(-2, 3):
                with Move(x,y):
                    circle((0,0), 0.5, ImagePattern(imag, pixels_per_unit=40))

    if 8<=t:
        print('9')
        print('This property is truly fascinating.')
        with Rotate((t-8)*360):
            with Move(-2,-1.5):
                pattern = ImagePattern(imag, pixels_per_unit=40)

        with Move(t-8,0):
            for x in range(-2, 3):
                    for y in range(-2, 3):
                        circle((x/1.5,y/1.5), 0.3, pattern)


animate(loop)
