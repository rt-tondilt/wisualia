import wisualia
from wisualia.shapes import circle, polygon
from wisualia.modifiers import Move, Rotate
from wisualia.animation import animate



def loop(t):
    with Move(0,t):
        circle((1,1),1)
        
        circle((2,0),t)
        polygon((0,0),(5,5),(6-t,-t/10))
        a= ''
    with Rotate(t*90):
        circle((5,5),1)
    print('HEA LEIB', t)
    print('KONN')
    

animate(loop)
