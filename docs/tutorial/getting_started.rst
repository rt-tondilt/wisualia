Getting started
===============

First animation
---------------

Wisualia animations are defined with Python source files. However not each Python
source file can also be used by Wisualia. Python files that are used by Wisualia must
follow these rules:

* The file must import Wisualia library like ``import wisualia``. The editor finds imported
  library by it's name so ``from wisualia import *`` and ``import wisualia as othername``
  do not work.
* The file must call :py:func:`wisualia.animation.animate`.The first argument of
  this function is another function usually called a loop function.
* The loop function will be called each time a new frame needs to be drawn.
  The only argument of the loop function is the current time from the start of
  the animation in seconds.

Here is an example of minimal proper Wisualia file.

.. testcode::

  import wisualia
  from wisualia.animation import animate

  def loop(time):
      pass

  animate(loop)

Note that this file does nothing by itself, for real animation we have to add
something to draw.

.. testcode:: first_circle

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle

  def loop(time):
      circle()

  animate(loop)

.. testcleanup:: first_circle

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_circle.png')

.. image:: /_images/first_circle.png

Lets look at the documentation of :py:func:`wisualia.shapes.circle`. The function
takes four arguments.

* The first argument is the centre point of the circle, represented as a pair of
  floats.
* The radius of the circle.
* The pattern that is used to fill the circle.
* The stroke that is used to draw the curve of the circle.

Knowing that we can already do some animation.

.. testcode:: second_circle

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle

  def loop(time):
      circle((2, time/5), time/10)
      circle((-1, time/5), time/10)

  animate(loop)

.. testcleanup:: second_circle

  loop(1)
  wisualia_x.core.image.write_to_png('_images/second_circle.png')

Resulting animation at 1 second.

.. image:: /_images/second_circle.png

.. warning::

  All Wisualia functions that accept floats as arguments also work with integers.
  However, infinite and other unusual float values have not been tested and
  might result in **any** behaviour.

Fill and Stroke
---------------

The third argument of circle is a Pattern named fill. A pattern is a virtual
"paint" that is used to draw things. Patterns live in
:py:mod:`wisualia.patterns` module. Here is an example of usage of RGBA pattern.

.. testcode:: first_fill

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle
  from wisualia.patterns import RGBA

  def loop(time):
      circle((0,0), 1, fill=RGBA(0, 0, 1, 1))
      circle((0,0), 0.2, fill=RGBA(0, 0, 0))
      circle((1,0), 0.5, fill=RGBA(1, 0, 0, 0.5))

  animate(loop)

.. testcleanup:: first_fill

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_fill.png')

.. image:: /_images/first_fill.png

Note that all color values are in range from 0 to 1. The default alpha value is
1 meaning completely opaque.

The last argument specifies the properties of the curve of the circle. It is an
optional argument meaning that it can be either :py:obj:`None` or
:py:obj:`wisualia.shapes.Stroke`. If the value is :py:obj:`None`, then no stroke
is drawn. As we saw before, this argument defaults to :py:obj:`None`.

.. testcode:: first_stroke

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle, Stroke
  from wisualia.patterns import RGBA

  def loop(time):
      blueish = RGBA(0, 0, 1, 0.5)
      redish = RGBA(1, 0, 0, 0.5)

      circle((-2,0), 0.5, fill=blueish)
      circle((-1,0), 0.5, fill=blueish, stroke=None)
      circle(( 0,0), 0.5, fill=blueish, stroke=Stroke())
      circle(( 1,0), 0.5,
             fill=blueish,
             stroke=Stroke(width=0.2, pattern=redish))
      circle(( 1,0), 0.5,
             fill=blueish,
             stroke=Stroke(width=0.2, pattern=redish))
      circle(( 2,0), 2,
             fill=RGBA(0,0,0,0),
             stroke=Stroke(width=0.2, pattern=redish))

  animate(loop)

.. testcleanup:: first_stroke

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_stroke.png')

.. image:: /_images/first_stroke.png

.. note::

  In Wisualia functions that draw something (mainly in
  :py:mod:`wisualia.shapes`) there is a convention for the order of
  arguments. Allthough all arguments can be reffered by a keyword and in any
  order, the following order is highly recommended:

  1. Arguments defining the geometry of the shape. These are usually used as
     positional arguments.
  2. The fill of the shape, usually used as a keyword argument.
  3. The stroke of the shape, usually used as a keyword argument.

  Fill and stroke are usually optional (in other words they can be :py:obj:`None`), but
  the default fill value is something visible for quick prototyping. Geometry
  related arguments may have default values as well, they default to shapes
  inside ``-1 <= x <= 1`` and ``-1 <= y <=1``.

Loading images
----------------

Lets draw the following image :download:`example.png`. Here is a minimal
solution.

.. testcode:: first_image

  import wisualia
  from wisualia.animation import animate
  from wisualia.image import Image
  from wisualia.patterns import ImagePattern
  from wisualia.shapes import paint

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
  from wisualia.image import Image
  from wisualia.patterns import ImagePattern
  from wisualia.shapes import circle

  image = Image.from_png('tutorial/example.png')

  def loop(t):
      circle(fill=ImagePattern(image, pixels_per_unit=80))

  animate(loop)

.. testcleanup:: second_image

  loop(1)
  wisualia_x.core.image.write_to_png('_images/second_image.png')

.. image:: /_images/second_image.png

This looks still quite ugly, the image is inside the first quadrant of the
plane. We will fix that in the transformations tutorial.


Exporting animations
--------------------

TODO.
