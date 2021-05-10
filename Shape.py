from math import sqrt
import shapely as shp
from shapely.geometry import polygon

"""
3D Vector
"""


# Vector3D
class Vector3:

    # Constructor
    def __init__(self, X=0, Y=0, Z=0):
        self.__x = X
        self.__y = Y
        self.__z = Z

    def __str__(self):
        return "(" + str(self.__x) + ", " + str(self.__y) + ", " + str(self.__z) + ")".format(self=self)

    def __repr__(self):
        return "(" + str(self.__x) + ", " + str(self.__y) + ", " + str(self.__z) + ")".format(self=self)

    # Getters
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getZ(self):
        return self.__z

    # Setters
    def setX(self, X):
        self.__x = X

    def setY(self, Y):
        self.__y = Y

    def setZ(self, Z):
        self.__z = Z

    # Operator Overloading
    def __neg__(self):
        return Vector3(-self.__x, -self.__y, -self.__z)

    def __add__(self, other):
        return Vector3(self.__x + other.__x, self.__y + other.__y, self.__z + other.__y)

    def __sub__(self, other):
        return Vector3(self.__x - other.__x, self.__y - other.__y, self.__z - other.__y)

    def __mul__(self, scale):
        return Vector3(scale * self.__x, scale * self.__y, scale * self.__z)

    def __truediv__(self, scale):
        return Vector3(self.__x / scale, self.__y / scale, self.__z / scale)

    def __invert__(self):
        self.__x = -self.__x
        self.__y = -self.__y
        self.__z = -self.__z

        return self

    def __iadd__(self, other):
        self.__x += other.__x
        self.__y += other.__y
        self.__z += other.__z

        return self

    def __isub__(self, other):
        self.__x -= other.__x
        self.__y -= other.__y
        self.__z -= other.__z

        return self

    def __imul__(self, scale):
        self.__x *= scale
        self.__y *= scale
        self.__z *= scale

        return self

    def __idiv__(self, scale):
        self.__x /= scale
        self.__y /= scale
        self.__z /= scale

        return self

    def __eq__(self, other):
        return self.__x == other.__x and self.__y == other.__y and self.__z == other.__y

    # Dot and Cross Products
    def dot(self, other):
        return (self.__x * other.__x) + (self.__y * other.__y) + (self.__z * other.__z)

    def cross(self, other):
        newX = (self.__y * other.__z) - (self.__z * other.__y)
        newY = (self.__z * other.__x) - (self.__x * other.__z)
        newZ = (self.__x * other.__y) - (self.__y * other.__x)

        return Vector3(newX, newY, newZ)

    def tripleProd(self, other1, other2):
        return (self.cross(other1)).cross(other2)

    # Returns the magnitude of the vector.
    def magnitude(self):
        return sqrt(self.__x ** 2 + self.__y ** 2 + self.__z ** 2)

    # Returns a unit vector in the same direction
    def normalize(self):
        magn = sqrt(self.__x ** 2 + self.__y ** 2 + self.__z ** 2)
        return Vector3(self.__x / magn, self.__y / magn, self.__z / magn)

    # Returns a vector perpendicular to displacement vector
    # formed by self and other, pointing toward the origin.
    def perp(self, other):
        SO = other - self
        return SO.cross(other).cross(SO)

    def makeShapelyPoint(self):
        return shp.geometry.Point(self.__x, self.__y, self.__z)


def makeVector3(shapelyPoint):
    return Vector3(shapelyPoint.x, shapelyPoint.y, shapelyPoint.z)


"""
Constant Vectors:
"""

Origin = Vector3(0, 0, 0) 
iHat = Vector3(1, 0, 0)
jHat = Vector3(0, 1, 0)
kHat = Vector3(0, 0, 1)

"""
Shapes: Points, Polygons, Polyhedra:
"""


# Polygon
class Polygon:

    # Constructor
    def __init__(self, Vertices):
        self.__vertices = Vertices
        self.__numSides = len(Vertices)
        self.__centre = Vector3(0, 0, 0)

        # Finds the centre of the shape by getting
        # average of the points.
        for i in self.__vertices:
            self.__centre += i

        self.__centre /= self.__numSides

    def __str__(self):
        return str(self.__vertices).format(self=self)

    def __repr__(self):
        return str(self.__vertices).format(self=self)

    def getCentre(self):
        return self.__centre

    def getVertices(self):
        return self.__vertices

    # Return a list, where each element of self is added
    # to every element of other.
    def MinkowskiSum(self, other):
        newPoints = []

        for point in self.__vertices:
            for otherPoint in other.__vertices:
                newPoints.append(point + otherPoint)

        return newPoints

        # Return a list, where each element of self is subtracted

    # by every element of other.
    def MinkowskiDiff(self, other):
        newPoints = []

        for point in self.__vertices:
            for otherPoint in other.__vertices:
                newPoints.append(point - otherPoint)

        return newPoints

    # Returns the furthest point in a given direction in the polygon.
    def FurthestPoint(self, direction):
        maxDot = direction.dot(self.__vertices[0])
        maxVertex = self.__vertices[0]  

        # The point for which the dot product is maximised is the furthest point.
        for i in self.__vertices:
            if maxDot < direction.dot(i):
                maxDot = direction.dot(i)
                maxVertex = i

        return maxVertex  # Get the point corresponding to the highest dot product.

    def makeShapelyPolygon(self):
        return shp.geometry.Polygon(self.__vertices)


def makePolygon(shapelyPoly):
    vertices = list(shapelyPoly.exterior.coords)
    verticesVect = [Vector3(i.x, i.y, i.z) for i in vertices]
    return Polygon(verticesVect)
