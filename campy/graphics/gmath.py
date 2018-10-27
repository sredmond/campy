'''
This file exports several functions for working with graphical gemoetry along with
the mathematical constants PI and E
'''
import math as _math

from campy.system.error import error

PI = _math.pi
'''
The mathematical constant pi, which is the ratio of the circumference of a circle to
its diameter
'''

E = _math.e
'''
The mathematical constant e, which is the base of the natural logarithm
'''

def to_degrees(radians):
	'''
	Converts an angle from radians to degrees.

	@type radians: float
	@param radians: radians
	@rtype: float
	@return: degrees
	'''
	return _math.degrees(radians)

def to_radians(degrees):
	'''
	Converts an angle from degrees to radians.

	@type degrees: float
	@param degrees: degrees
	@rtype: float
	@return: radians
	'''
	return _math.radians(degrees)

def sin_degrees(angle):
	'''
	Returns the trigonometric sine of angle, which is expressed in degrees

	@type angle: float
	@param angle: degrees
	@rtype: float
	'''
	return _math.sin(to_radians(angle))

def cos_degrees(angle):
	'''
	Returns the trigonometric cosine of angle, which is expressed in degrees

	@type angle: float
	@param angle: degrees
	@rtype: float
	'''
	return _math.cos(to_radians(angle))

def tan_degrees(angle):
	'''
	Returns the trigonometric tangent of angle, which is expressed in degrees

	@type angle: float
	@param angle: degrees
	@rtype: float
	'''
	return _math.tan(to_radians(angle))

def vector_distance(x, y):
	'''
	Computes the distance between the origin and the specified point.

	@type pt: GPoint
	@param pt: GPoint to compute distance to, will override x and y parameters
	@type x: float
	@param x: x value of point
	@type y: float
	@param y: y value of point
	@rtype: float
	'''
	return _math.sqrt(x * x + y * y)

def vector_angle(x, y):
	'''
	Returns the angle in degrees from the origin to the specified point. This
	functoin takes account of the fact that the graphics coordinate system is flipped
	in the y direction from the traditional Cartesian plane.

	@type pt: GPoint
	@param pt: GPoint to angle to, will override x and y parameters
	@type x: float
	@param x: x value of point
	@type y: float
	@param y: y value of point
	@rtype: float
	@return: degrees
	'''
	if x == 0 and y == 0:
		return 0
	return to_degrees(_math.atan2(-y, x))

def count_digits(n, base):
	if base <= 0:
		error("countDigits: base must be 1 or greater")
	n = abs(n)
	digits = 0
	while n > 0:
		digits += 1
		n //= base
	return digits

