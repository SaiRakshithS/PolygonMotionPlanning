from TMapping import*
import staticList
import Shape

def randomInput():
    l=staticList.polygons.copy()
    xCoord,yCoord=[],[]
    for each in l:
        X,Y=[],[]
        vect=each.getVertices()
        for i in vect:
            x=i.getX()
            y=i.getY()
            z=i.getZ()
            X.append(x)
            Y.append(y)
        xCoord.append(X)
        yCoord.append(Y)
    p=[]
    for polyx,polyy in zip(xCoord,yCoord):
        plist=[]
        for x,y in zip(polyx,polyy):
            plist.append((x,y))
        p.append(MultiPoint(plist).convex_hull)
    if(MultiPolygon(p).is_valid):
        return p
    else:
        print("ERROR : Overlapping or self intersecting polygons")
        
p=randomInput()        
polygons=MultiPolygon(p)    


l=20
b=20


axs=create(polygons,l,b)

strips=createStrips(polygons,l,b)
#PlotStrips(axs,polygons,l,b)

t=createTrapeziums(strips,polygons)
#plotTrapezium(t,polygons,l,b)

pathPoints=createPathPoints(t)
#PlotPathPoints(pathPoints,polygons,l,b)
#createPath(triangulate(MultiPoint(pathPoints)),l,b,polygons)
#plt.show()


try:
    startx=float(input("enter x of start"))
    starty=float(input("enter y of start"))
    endx=float(input("enter x of end"))
    endy=float(input("enter y of end"))
    start=Point(startx,starty)
    end=Point(endx,endy)
    points=STRtree(pathPoints)
    if(start.within(polygons) or end.within(polygons)):
        raise "start or end invalid"
    
    S=points.nearest(start)
    E=points.nearest(end)
    createPathFinal(triangulate(MultiPoint(pathPoints)),l,b,polygons,start,S,end,E)
    
except :
    print("\n!!!!!!!!!!start or end invalid!!!!!!!!")



"""pathRec=pathRecord(polygons,pathPoints)
plotRoute(pathRec,pathPoints,polygons,l,b)
route=Route(pathRec,pathPoints)"""

plt.show()
