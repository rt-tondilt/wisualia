import wisualia
from wisualia.shapes import circle, Stroke
from wisualia.modifiers import Move, Scale, Rotate
from wisualia.patterns import ImagePattern, RGBA
from wisualia.image import Image
from wisualia.pencil import Pencil
from wisualia import animation

# We open a png image outside of loop() to keep programm fast.

imag = Image.from_png('example.png')
def loop(t): 
    if t<1:
        print(1)
        print('Pencil lets us draw arbitrary shapes.')
        with Pencil() as p:
            p.move_to(-1,-1)
            p.line_to(-1, 1)
            p.line_to( 1, 1)
            p.line_to( 1,-1)
            p.arc(centre=(0,-1), radius=1, angles=(0,180))
            print('Start and end angles are given, using convention from mathematics.')
        
    if 1<=t<2:
        print(2)
        print('We can use modifiers on parts of our drawing')
        with Pencil() as p:
            p.move_to(-1,-1)
            p.line_to(-1, 1)
            with Move(t-1,t-1):
                p.line_to( 1, 1)
                p.line_to( 1,-1)
            p.arc(centre=(0,-1), radius=1, angles=(0,180))
            print('wisualia will automaticaly connect the start of the arc with the last point.')
    if 2<=t<3:
        print(3)
        print('The pencil records all operations and draws the shape at the end of the block.')
        print('That is why circles appear behind the drawing')
        with Pencil() as p:
            circle((-1, 1), 0.5)
            p.move_to(-1,-1)
            p.line_to(-1, 1)
            p.line_to( 1, 1)
            p.line_to( 1,-1)
            p.arc(centre=(0,-1), radius=1, angles=(0,180))
            circle((1,1), 0.5)
        # Pencil draws here
    if 3<=t<4:
        print(4)
        print('We can draw multiple shapes with .move_to().')
        with Pencil() as p:
            p.move_to(-1,-1)
            p.line_to(-1, 1)
            p.line_to(-2, 1)
            p.move_to( 1,-1)
            p.line_to( 1, 1)
    if 4<=t<5:
        print(5)
        print('We can use scale modifier to make ellipses.')
        with Scale(factors=(2, 1), centre=(0,0)):
            circle((0,0), 1, fill=RGBA(0,0,1,0.5), stroke=Stroke(width=0.5, pattern=RGBA(1,0,0)))
    if 5<=t<6:
        print(6)
        print('We can abuse the nature of Pencil to make ellipses with constant line_width.')
        with Pencil(fill=RGBA(0,0,1,0.5), stroke=Stroke(width=0.5, pattern=RGBA(1,0,0))) as p:
            with Scale(factors=(2, 1), centre=(0,0)):
                p.arc((0,0),1,(0,360))
        # Pencil draws here
        print('This works because, the line is drawn after the transformation and')
        print('the pencil does not record data about "brush shape".')
    if 6<=t<7:
        print(7)
        print('However transformations outside of the pencil will change the "brush shape"')
        print('because drawing happens inside transformation.')
        with Scale(factors=(2, 1), centre=(0,0)):
            with Pencil(fill=RGBA(0,0,1,0.5), stroke=Stroke(width=0.5, pattern=RGBA(1,0,0))) as p:
                p.arc((0,0),1,(0,360))
            # Pencil draws here

    if 7<=t<8:
        print(8)
        print('All new patterns can be images.')
        
        pat = ImagePattern(imag, pixels_per_unit=40)
        
        with Pencil(fill=RGBA(0,0,1,0.5), stroke=Stroke(width=0.5, pattern=pat)) as p:
            with Scale(factors=(2, 1), centre=(0,0)):
                p.arc((0,0),1,(0,360))
        print('Notice how the edge of fill pattern is actually in the centre of stroke line.')

                    
    if 8<=t:
        print('9')
        print('Demo.')
        with Scale((0.5,1)), Rotate(t*90):
            with Pencil() as p:
                p.move_to(5, -1)
                for i in range(10):
                    with Rotate((i)*36):
                        p.arc((5,0),1, (270, 90))
                p.close_path()
        print('''
        Python syntax tip.
        ```
        with a, b:
            pass
        ```
        is same as
        ```
        with a:
            with b:
                pass
        ```
        ''')
                
                        
            
        

animation.animate(loop)
