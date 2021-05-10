import Shape

vertices = [

	[Shape.Vector3(1,6,1), Shape.Vector3(1.5,8,1), Shape.Vector3(3,7,1)],

	[Shape.Vector3(9,6,1), Shape.Vector3(4,5,1), Shape.Vector3(3,2,1), Shape.Vector3(7,1,1)],

	[Shape.Vector3(6,10,1), Shape.Vector3(11,13,1), Shape.Vector3(17,11,1), Shape.Vector3(15,9,1)]]
"""[Shape.Vector3(4, 2,1), Shape.Vector3(6, 3,1), Shape.Vector3(7, -2,1)],

	[Shape.Vector3(-2, 3,1), Shape.Vector3(-2, 3,1), Shape.Vector3(-8, 3,1), Shape.Vector3(-8, -3,1)],

	[Shape.Vector3(0, -5,1), Shape.Vector3(0, 0,1), Shape.Vector3(-1, -2,1), Shape.Vector3(1, -2,1), Shape.Vector3(-1, -3,1), Shape.Vector3(1, -3,1)]"""


polygons = [Shape.Polygon(x) for x in vertices]
[[1,1.5,3],[9,4,2,7],[6,11,13,17,15]]
ys=[[6,8,7],[6,5,4,0],[10,12,15,11,9]]
