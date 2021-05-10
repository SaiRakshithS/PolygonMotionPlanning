import Shape

"""
Gets the extreme Minkowski points
"""
def Support(shapeA, shapeB, direction):
    extremeA = shapeA.FurthestPoint(direction) 
    extremeB = shapeB.FurthestPoint(-direction)

    return extremeA - extremeB

"""
Handle Line case of simplex 
"""
def HandleLineSimplex(simplex, direction):
    pointA, newPoint = simplex

    Aperp = (pointA - newPoint).tripleProd(-newPoint, pointA - newPoint)
    direction = Aperp

    return False  # A line itself will never enclose the origin.

"""
Triangle Case of simplex
"""
def HandleTriangleSimplex(simplex, direction):
    #newPoint is the point most recently added,
    #other points were added before, and will be removed,
    #depencing on whether origin is enclosed.
    pointA, pointB, newPoint = simplex

    #Vectors perpendicular to A, B and newPoint
    Aperp = (pointB - newPoint).tripleProd(pointA - newPoint, pointA - newPoint)
    Bperp = (pointA - newPoint).tripleProd(pointB - newPoint, pointB - newPoint)

       #Checks whether origin could be in possible regions.
       #Returns false because collision has not happened, so continue
       #till it does, with updated simplex.
    if Bperp.dot(-newPoint) > 0:
        simplex.remove(pointA)
        direction = Bperp

        return False

    elif Aperp.dot(-newPoint) > 0:
        simplex.remove(pointB)
        direction = Aperp

        return False

    #If origin is not in the possible regions, it is contained
    #in our simplex, so return True, indicating collision.
    return True

"""
Updates simplex to continue checking, or detects collision.
"""
def HandleSimplex(simplex, direction):
    dim = len(simplex)

    if (dim == 2):
        return HandleLineSimplex(simplex, direction)

    return HandleTriangleSimplex(simplex, direction)

"""
GJK Collision Algorithm.
"""
def GJK(shapeA, shapeB):
    direction = (shapeB.getCentre() - shapeA.getCentre())
    simplex = [Support(shapeA, shapeB, direction)] 
    direction = -simplex[0]

    while True:
        newPoint = Support(shapeA, shapeB, direction)

        if newPoint.dot(direction) < 0:
            return False

        simplex.append(newPoint) 
        if HandleSimplex(simplex, direction):
            return True
