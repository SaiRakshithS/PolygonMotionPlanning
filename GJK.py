import Shape

def Support(shapeA, shapeB, direction):
    extremeA = shapeA.FurthestPoint(direction)
    extremeB = shapeB.FurthestPoint(-direction)

    return extremeA - extremeB

def HandleSimplex(simplex, direction, shapeA, shapeB):
    dim = len(simplex)
    
    # We will make a triangle, which is the simplex in 2D
    if dim == 2:
        C, B = simplex

        BC = C - B
        OC = -C

        # A line can contain the orign, but we won't check that here
        direction = BC.tripleProd(OC, BC)
        return False

    # We have our simplex. Now we find out if it encloses the origin
    elif dim == 3:
        C, B, A = simplex

        OA = -A
        BA = B - A
        CA = C - A

        # The triple product gives the direction perpendicular to both the lines
        BAperp = CA.tripleProd(BA, BA)
        CAperp = BA.tripleProd(CA, CA)

        # The triple product divides the region into voronoi regions. 
        # We can, through theory, eliminate the need to check many of the regions
        # We will check the rest here using the dot product.

        if BAperp.dot(OA) > 0:
            simplex.remove(C) 
            direction = BAperp

            return False
        
        elif CAperp.dot(OA) > 0:
            simplex.remove(B)
            direction = CAperp

            return False

        else:
            return True


def GJK(shapeA, shapeB): 
   
    direction = shapeA.getCentre() - shapeB.getCentre()
    simplex = [Support(shapeA, shapeB, direction)]
    direction = -simplex[0]
 
    while True:

        # Updating simplex and checking potential point.
        newPoint = Support(shapeA, shapeB, direction)

        if newPoint.dot(direction) < 0:
            return False

        simplex.append(newPoint)
        if HandleSimplex(simplex, direction, shapeA, shapeB):
            return True
