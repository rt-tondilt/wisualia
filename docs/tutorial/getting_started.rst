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
* The file must define a function named ``loop`` that takes a float as an
  argument. This function will be called each time a new frame needs to be drawn.
  The argument is the current time from the start of the animation in seconds.

Here is an example of minimal proper Wisualia file.

.. testcode::

  import wisualia

  def loop(time):
      pass

Note that this file does nothing by itself, for real animation we have to add
something to draw.

.. testcode:: first_circle

  import wisualia
  from wisualia.shapes import circle

  def loop(time):
      circle()

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
  from wisualia.shapes import circle

  def loop(time):
      circle((2, time/5), time/10)
      circle((-2, time/5), time/10)

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

TODO.

Exporting animations
--------------------

TODO.
