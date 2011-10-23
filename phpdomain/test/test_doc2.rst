Top Level Namespace
###################

namespace ``Imagine\Draw``

.. php:namespace:: Imagine\Draw

.. php:class:: DrawerInterface

Instance of this interface is returned by :php:meth:`Imagine\Image\ImageInterface::draw`.

.. php:method:: arc(PointInterface $center, BoxInterface $size, $start, $end, Color $color)

    Draws an arc on a starting at a given x, y coordinates under a given start and end angles

    :param Imagine\Image\PointInterface $center: Center of the arc. 
    :param Imagine\Image\BoxInterface $size: Size of the bounding box.
    :param integer $start: Start angle.
    :param integer $end: End angle.
    :param Imagine\Image\Color $color: Line color.

    :throws: Imagine\Exception\RuntimeException

    :returns: Imagine\Draw\DrawerInterface

