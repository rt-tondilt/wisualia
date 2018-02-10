Patterns and transformations
============================

Patterns
--------

A pattern is a virtual "paint" that is used to draw things. Patterns live in
:py:mod:`wisualia.patterns` module. Here is an example of usage of RGBA pattern.

.. testcode:: first_fill

  import wisualia
  from wisualia.animation import animate
  from wisualia.do import fill
  from wisualia.shapes import circle
  from wisualia.patterns import RGBA

  def loop(time):
      circle((0,0), 1)
      fill(RGBA(0, 0, 1, 1))

      circle((0,0), 0.2)
      fill(RGBA(0, 0, 0))

      circle((1,0), 0.5)
      fill(RGBA(1, 0, 0, 0.5))

  animate(loop)

.. testcleanup:: first_fill

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_fill.png')

.. image:: /_images/first_fill.png

Note that all color values are in range from 0 to 1. The default alpha value is
1 meaning completely opaque.


Loading images
----------------

Lets draw the following image :download:`example.png`. Here is a minimal
solution.

.. testcode:: first_image

  import wisualia
  from wisualia.animation import animate
  from wisualia.image import Image
  from wisualia.patterns import ImagePattern
  from wisualia.do import paint

  # We load the file outside of the loop function, to make looping faster.
  # Here the image is inside tutorial folder for technical reasons.
  # Normally you would open image in the same folder, like
  # image = Image.from_png('example.png')
  image = Image.from_png('tutorial/example.png')

  def loop(t):
      paint(ImagePattern(image, pixels_per_unit=80))

  animate(loop)

.. testcleanup:: first_image

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_image.png')

.. image:: /_images/first_image.png

ImagePatter is a pattern, which means that we can use shapes to crop images.

.. testcode:: second_image

  import wisualia
  from wisualia.animation import animate
  from wisualia.do import fill
  from wisualia.image import Image
  from wisualia.patterns import ImagePattern
  from wisualia.shapes import circle

  image = Image.from_png('tutorial/example.png')

  def loop(t):
      circle()
      fill(ImagePattern(image, pixels_per_unit=80))

  animate(loop)

.. testcleanup:: second_image

  loop(1)
  wisualia_x.core.image.write_to_png('_images/second_image.png')

.. image:: /_images/second_image.png

This looks still quite ugly, the image is inside the first quadrant of the
plane. We will fix that in the transformations tutorial.



Transformations on shapes
-------------------------

Wisualia allows us to work with
`affine transformations <https://en.wikipedia.org/wiki/Affine_transformation>`_.
Here is an example of rotation.

.. testcode:: first_rotation

  import wisualia
  from wisualia.animation import animate
  from wisualia.do import fill
  from wisualia.shapes import circle
  from wisualia.patterns import RGBA
  from wisualia.modifiers import Rotate

  def loop(t):
      circle((1,0), 0.5) #RIGHT CIRCLE
      fill(RGBA(1,0,0))
      with Rotate(90):
          circle((1,0), 0.5) #TOP CIRCLE
          fill(RGBA(0,0,1))
      circle((0,-1), 0.5) #BOTTOM CIRCLE
      fill(RGBA(0,0,0))

  animate(loop)

.. testcleanup:: first_rotation

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_rotation.png')

.. image:: /_images/first_rotation.png

The blue circle was rotated 90 degrees before drawing. We can also rotate around
an arbitrary point.

.. testcode:: second_rotation

  import wisualia
  from wisualia.animation import animate
  from wisualia.do import fill
  from wisualia.shapes import circle
  from wisualia.patterns import RGBA
  from wisualia.modifiers import Rotate

  def loop(t):
      for i in range(10):
          with Rotate(i*36, centre=(-1,0)):
              circle((0,0), i/50+0.1)
              fill(RGBA(i/10, 0, 1-i/10))

  animate(loop)

.. testcleanup:: second_rotation

  loop(1)
  wisualia_x.core.image.write_to_png('_images/second_rotation.png')

.. image:: /_images/second_rotation.png

Transformations can be nested. In this case inner transformations will be done
first and outer after them. Compare the following shapes.

.. testcode:: multiple_transformations

  import wisualia
  from wisualia.do import stroke, fill
  from wisualia.animation import animate
  from wisualia.shapes import circle, rect
  from wisualia.patterns import RGBA
  from wisualia.modifiers import Rotate, Scale

  def loop(t):
      # Red, not transformed.
      rect((0,0), (1.5, 1.5))
      fill(RGBA(1,0,0,0.5))

      # Green, rotated and then scaled.
      with Scale((0.5,1)):
          with Rotate(-45):
              rect((0,0), (1.5, 1.5))
              fill(RGBA(0,1,0,0.5))

      # Blue, scaled and then rotated.
      with Rotate(-45):
          with Scale((0.5,1)):
              rect((0,0), (1.5, 1.5))
              fill(RGBA(0,0,1,0.5))

  animate(loop)

.. testcleanup:: multiple_transformations

  loop(1)
  wisualia_x.core.image.write_to_png('_images/multiple_transformations.png')

.. image:: /_images/multiple_transformations.png

Transformations on patterns
---------------------------

TODO.
