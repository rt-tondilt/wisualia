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
  this function is the loop function.
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
  from wisualia.do import fill

  def loop(time):
      circle()
      fill()

  animate(loop)

.. testcleanup:: first_circle

  loop(1)
  wisualia_x.core.image.write_to_png('_images/first_circle.png')

.. image:: /_images/first_circle.png

In this code ``circle()`` defines the shape we want to draw and ``fill()`` says
that we want to fill the shape with a color. The position and color of the
circle shown above depend on the default arguments of ``circle()`` and
``fill()``. Of course we can choose our own values.

.. testcode:: second_circle

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle
  from wisualia.do import fill
  from wisualia.patterns import RGBA

  def loop(time):
      circle((1, 0), 1+time/2) # centre point and radius
      fill(RGBA(1, 1, 0, 1))

  animate(loop)

.. testcleanup:: second_circle

  loop(1)
  wisualia_x.core.image.write_to_png('_images/second_circle.png')

.. image:: /_images/second_circle.png

Resulting animation of "growing" circle at 1 second.

We can use ``stroke()`` function to draw the edges of the shape.

.. testcode:: stroke_1

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import polygon
  from wisualia.do import fill, stroke
  from wisualia.patterns import RGBA

  def loop(time):
      polygon((-2,-1), (-1,-1), (1,1), (-1,1))
      fill(RGBA(0,0,0)) # Note that you can ommit the alpha value.
      stroke(0.4, RGBA(1,0,0,0.5)) # Line width and color

  animate(loop)

.. testcleanup:: stroke_1

  loop(1)
  wisualia_x.core.image.write_to_png('_images/stroke_1.png')

.. image:: /_images/stroke_1.png

Here the stroke is 50% transparent and we can see the edge of underlying filled
area. Try switching the order of ``fill()`` and ``stoke()`` operations and
compare the result.

Holes and intersecting shapes.
------------------------------

We can make holes by defining two shapes and filling them together.

.. testcode:: hole_1

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle, polygon
  from wisualia.do import fill
  from wisualia.patterns import RGBA

  def loop(time):
      polygon((-1,1),(-1,-1),(2,0))
      circle((0,0),0.5)
      fill(RGBA(1,0,0))

  animate(loop)

.. testcleanup:: hole_1

  loop(1)
  wisualia_x.core.image.write_to_png('_images/hole_1.png')

.. image:: /_images/hole_1.png

This is different from defining two shapes and filling them separately.

.. testcode:: hole_2

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle, polygon
  from wisualia.do import fill
  from wisualia.patterns import RGBA

  def loop(time):
      polygon((-1,1),(-1,-1),(2,0))
      fill(RGBA(1,0,0))

      circle((0,0),0.5)
      fill(RGBA(0.2,0,0))

  animate(loop)

.. testcleanup:: hole_2

  loop(1)
  wisualia_x.core.image.write_to_png('_images/hole_2.png')

.. image:: /_images/hole_2.png

We can also define two intersecting shapes and fill them together.

.. testcode:: hole_3

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle, polygon
  from wisualia.do import fill
  from wisualia.patterns import RGBA

  def loop(time):
      polygon((-1,1),(-1,-1),(2,0))
      circle((0,0),1)
      fill(RGBA(0.2,0,0))

  animate(loop)

.. testcleanup:: hole_3

  loop(1)
  wisualia_x.core.image.write_to_png('_images/hole_3.png')

.. image:: /_images/hole_3.png

.. note::

  Filling is currently done with ``cairo.FillRule.EVEN_ODD``. TODO: Explain
  more.

Automatical clearing of already used shapes
-------------------------------------------

The ``fill()`` and ``stroke()`` operations apply to the previously defined
shapes. You can define any number of shapes and then fill and stroke them
together. You can also also fill or stroke the previously defined shapes
multiple times.

However after you have defined the shapes and filled or stroked them any number
of times, the shapes are automatically cleared.

.. testcode:: clearing

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle
  from wisualia.do import fill, stroke
  from wisualia.patterns import RGBA

  def loop(time):
      circle((-1,0), 0.5)
      stroke(0.3, RGBA(1,0,0))
      stroke(0.1, RGBA(0,0,1))

      # Here after the first circle has been defined and used
      # and before the second circle is defined, the first
      # circle is automatically cleared.

      circle((1,0), 0.5)
      fill(RGBA(0,0.5,0)) # Here only the second circle is filled.

  animate(loop)

.. testcleanup:: clearing

  loop(1)
  wisualia_x.core.image.write_to_png('_images/clearing.png')

.. image:: /_images/clearing.png

.. note::

  The automatical clearing actually happens inside the following shape. The
  simplified implementation is shown below.

  ::

    clearing_is_needed = False
    def fill(...):
        global clearing_is_needed
        clearing_is_needed = True
        ...
    def stroke(...):
        global clearing_is_needed
        clearing_is_needed = True
        ...
    def circle(...): # or any other shape
        global clearing_is_needed
        if clearing_is_needed:
            clear() # <--- actual clearing operation
            clearing_is_needed = False
        ...


Exporting animations
--------------------

1. Ensure that you have saved the file.
2. Click on the Export button and wait.

.. note::

  All wisualia files are python source files, which means, that they are runnable.
  The export button uses this mechanism. In the future exporting a file could be
  as easy as writting ``your_wisualia_file.py animate`` to the console.

Possible mistakes and other suprising behaviour
-----------------------------------------------

.. warning::

  All Wisualia functions that accept floats as arguments also work with integers.
  However, infinite and other unusual float values have not been tested and
  might result in **any** behaviour.

**Don't change global variables from the loop function.** For example the following
code behaves in a quite nonsensical way (try zooming in and out, moving the view
or changing the time).

.. testcode::

  import wisualia
  from wisualia.animation import animate
  from wisualia.shapes import circle

  n = 0

  def loop(time):
      global n
      circle((0,0), (n%10)*0.2)
      n += 1

  animate(loop)

**Don't change imported modules at runtime.** For example lets say that you have
following code inside the editor and it is displaying a rectangle.

.. The following code is so dangerous, that we can't even doctest it.

::

  import wisualia
  from wisualia.animation import animate
  from wisualia import shapes

  shapes.circle = shapes.rect

  def loop(t):
      wisualia.shapes.circle((0,0),(2,1+t))
      print('Drawing completed')
  animate(loop)

Now lets comment away this stupid assignment by inserting the ``#`` symbol. ::

  import wisualia
  from wisualia.animation import animate
  from wisualia import shapes

  #shapes.circle = shapes.rect

  def loop(t):
      wisualia.shapes.circle((0,0),(2,1+t))
      print('Drawing completed')
  animate(loop)

Now lets press the Play button. It still shows a growing rectangle.

This happens because we changed a variable inside a module. The Python interpreter
can't really reload already imported modules. That is why we have to restart the interpreter
if we have changed the source code of an imported module or we have changed the
module at runtime (as we did right now). The easiest way to restart the
interpreter, is to click the Run/Abort button twice.
