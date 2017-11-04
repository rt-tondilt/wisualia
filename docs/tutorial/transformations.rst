Transformations
===============

Transformations on shapes
-------------------------

Wisualia allows us to work with
`affine transformations <https://en.wikipedia.org/wiki/Affine_transformation>`_.
Here is an example of rotation.

.. testcode:: first_rotation

  import wisualia
  from wisualia.shapes import circle
  from wisualia.patterns import RGBA
  from wisualia.modifiers import Rotate

  def loop(t):
      circle((1,0), 0.5, fill=RGBA(1,0,0)) #RIGHT CIRCLE
      with Rotate(90):
          circle((1,0), 0.5, fill=RGBA(0,0,1)) #TOP CIRCLE
      circle((0,-1), 0.5, fill=RGBA(0,0,0)) #BOTTOM CIRCLE

.. testcleanup:: first_rotation

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_rotation.png')

.. image:: /_images/first_rotation.png

The blue circle was rotated 90 degrees before drawing. We can also rotate around
an arbitrary point.

.. testcode:: second_rotation

  import wisualia
  from wisualia.shapes import circle
  from wisualia.patterns import RGBA
  from wisualia.modifiers import Rotate

  def loop(t):
      for i in range(10):
          with Rotate(i*36, centre=(-1,0)):
              circle((0,0), i/50+0.1, fill=RGBA(i/10, 0, 1-i/10))

.. testcleanup:: second_rotation

  loop(1)
  wisualia_x.core.image.write_to_png('_images/second_rotation.png')

.. image:: /_images/second_rotation.png

Transformations can be nested. In this case inner transformations will be done
first and outer after them. Compare the following shapes.

.. testcode:: multiple_transformations

  import wisualia
  from wisualia.shapes import circle, rect, Stroke
  from wisualia.patterns import RGBA
  from wisualia.modifiers import Rotate, Scale

  invisible = RGBA(0,0,0,0)
  def loop(t):
      rect((0,-1),(2,0), fill=invisible, stroke=Stroke())
      circle((2,0), 0.3, fill=RGBA(0.5,0.5,0.5))

      with Scale((0.5,1)):
          with Rotate(45):
              rect((0,-1),(2,0), fill=invisible, stroke=Stroke())
              circle((2,0), 0.3, fill=RGBA(1,0,0))

      with Rotate(45):
          with Scale((0.5,1)):
              rect((0,-1),(2,0), fill=invisible, stroke=Stroke())
              circle((2,0), 0.3, fill=RGBA(0,0,1))

.. testcleanup:: multiple_transformations

  loop(1)
  wisualia_x.core.image.write_to_png('_images/multiple_transformations.png')

.. image:: /_images/multiple_transformations.png

Transformations on patterns
---------------------------

TODO.
