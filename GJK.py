import Shape

def GJK(shapeA : Shape.Polygon, shapeB : Shape.Polygon) -> bool:

    direction = shapeA.getCentre() - shapeB.getCentre()
    simplex = [Support(shapeA, shapeB, direction)]
    direction.set(-simplex[0])

    while True:

        # Updating simplex and checking potential point.
        newPoint = Support(shapeA, shapeB, direction)

        if newPoint.dot(direction) <= 0:
            return False

        simplex.append(newPoint)
        if HandleSimplex(simplex, direction):
            return True


def Support(shapeA : Shape.Polygon, shapeB : Shape.Polygon, direction : Shape.Vector3):

    extremeA = shapeA.FurthestPoint(direction)
    extremeB = shapeB.FurthestPoint(-direction)

    return extremeA - extremeB


def HandleSimplex(simplex : list, direction : Shape.Vector3) -> bool:
    dim = len(simplex)
    
    if dim == 2:
        C, B = simplex

        BC = C - B
        OC = C

        # Check if line contains the origin
        if B.cross(C) == Shape.Origin:
            return True
    
        else: 
            direction.set(BC.tripleProd(OC, BC))
            return False

    # We have our simplex. Now we find out if it encloses the origin
    elif dim == 3:
        C, B, A = simplex

        OA = A
        BA = B - A
        CA = C - A

        #Checking Edge Cases
        if A.cross(B) == Shape.Origin:
            return True

        elif A.cross(C) == Shape.Origin:
            return True

        elif B.cross(C) == Shape.Origin:
            return True

        # The triple product gives the direction perpendicular to both the lines
        BAperp = CA.tripleProd(BA, BA)
        CAperp = BA.tripleProd(CA, CA)

        # The triple product divides the region into voronoi regions. 
        # We can, through theory, eliminate the need to check many of the regions
        # We will check the rest here using the dot product.

        if BAperp.dot(OA) > 0:
            simplex.remove(C) 
            direction.set(BAperp)

            return False
        
        elif CAperp.dot(OA) > 0:
            simplex.remove(B)
            direction.set(CAperp)

            return False

        else: 
            return True
