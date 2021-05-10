from shapely import*
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon,MultiPolygon,LineString,LinearRing,MultiPoint
import Shape
import sympy as sp
from shapely.ops import shared_paths,triangulate
from shapely.strtree import STRtree


def removeDuplicate(l):
    final=[]
    [final.append(x) for x in l if x not in final]
    return final

def produceLines(poly,x,x1,p4):
    l=[(x,0),(x,p4),(x1,p4),(x1,0)]
    return l

def create(polygons,l,b):
    fig, axs = plt.subplots()
    axs.set_xlim([0,b])
    axs.set_ylim([0,l])
    for i in polygons:
        x,y=i.exterior.xy
        axs.fill(x,y,fc='r',alpha=0.5)
    return axs

def FCreate(polygon,l,b,polygons):
    x,y=polygon.exterior.xy
    print(polygon.exterior)
    axs=create(polygons,l,b)
    axs.plot(x,y)
    plt.show()
    return axs
    
def createStrips(polygons,l,b):
    allX=[0]
    for i in polygons:
        x,y=i.exterior.xy
        allX+=x
    allX.append(b)
    TrapX=removeDuplicate(allX)
    TrapX.sort()
    strips=[]
    y=list(range(int(l+1)))
    for i in range(len(TrapX)-1):
        x=[]
        for j in y:
            x.append(TrapX[i])
        strips.append(Polygon(produceLines(polygons,TrapX[i],TrapX[i+1],l)))
    return strips

def PlotStrips(axs,polygons,l,b):
    allX=[]
    for i in polygons:
        x,y=i.exterior.xy
        allX+=x
    TrapX=removeDuplicate(allX)
    TrapX.sort()
    y=list(range(int(l+1)))
    for i in range(len(TrapX)-1):
        x=[]
        for j in y:
            x.append(TrapX[i])
        axs.plot(x,y,'g-.')
    return axs
        
def createTrapeziums(strips,polygons):
    trapezium=[]
    for i in range(0,len(strips)):
        try:
            for poly in strips[i].difference(polygons).buffer(0):
                trapezium.append(Polygon(poly))
                trapezium=removeDuplicate(trapezium)
        except:
            trapezium.append(strips[i].difference(polygons).buffer(0))
            trapezium=removeDuplicate(trapezium)
    return trapezium

def plotTrapezium(trapezium,polygons,l,b):
    for i in trapezium:
        x,y=i.exterior.xy
        ax=create(polygons,l,b)
        ax.plot(list(x),list(y))
        plt.show()
    
def createPathPoints(trapezium):
    pathPoints=[]
    for i in range(len(trapezium)):
        pathPoints.append(trapezium[i].centroid)
        for j in trapezium[i+1:]:
            if(not shared_paths(trapezium[i].exterior,j.exterior).is_empty):
                try:
                    pathPoints.append(shared_paths(trapezium[i].exterior,j.exterior)[1].centroid)
                except:
                    pathPoints.append(shared_paths(trapezium[i].exterior,j.exterior).centroid)
            
    return pathPoints

def PlotPathPoints(pathPoints,polygons,l,b):
    x=[]
    y=[]
    for i in pathPoints:
        xi,yi=i.xy
        x+=xi
        y+=yi
    ax=create(polygons,l,b)
    axs=PlotStrips(ax,polygons,l,b)
    axs.scatter(x,y)
    plt.show()

def createPathNext(polygons,start,path,prev):
    Next=[]
    for i in path:
        line=LineString([start,i])
        if(polygons.disjoint(line)):
            Next.append(i)
    Next=removeDuplicate(Next)
    prev.update({str(start):Next})

def pathRecord(polygons,path):
    pathRec={}
    for i in path:
        createPathNext(polygons,i,path,pathRec)
    return pathRec

def plotRoute(pathRec,path,polygons,l,b):
    axs=create(polygons,l,b)
    for i in path:
        x,y=i.xy
        points=pathRec[str(i)]
        for j in points:
            X,Y=j.xy
            axs.plot([x,X],[y,Y])
    axs.set_label("All possible path")
    plt.show()

def Route(pathRec,path):
    Route={}
    for i in path:
        line=[]
        x,y=i.xy
        points=pathRec[str(i)]
        for j in points:
            line.append(LineString([i,j]))
        Route.update({str(i):line})
    return Route

def permittedPath(Route,path):
    line=[]
    for i in path:
        line+=Route[str(i)]
    return line
        
def dilate(path,polygons):
    lim=0.01
    FPath=path[0].buffer(0.01)
    for i in path:
        while(not i.buffer(lim).touches(polygons) and not i.buffer(lim).intersects(polygons)):
            d=i.buffer(lim)
            lim+=0.001
        FPath.union(d)
    return FPath

def createPath(path,l,b,polygons):
    axs = create(polygons,l,b)
    
    for i in path:
        X,Y=[],[]
        x,y=i.exterior.xy
        if(not i.crosses(polygons) and not i.intersects(polygons) and not i.contains(polygons)):
            axs.plot(x,y,'bo-')
        for j in range(1,len(x)):
            for i in range(j+1,len(x)):
                line=LineString([(x[j],y[j]),(x[i],y[i])])
                if(line.disjoint(polygons)):
                    X+=[x[j],x[i]]
                    Y+=[y[j],y[i]]
        axs.plot(X,Y,'bo-')
    #plt.show()
    return axs

def createPathFinal(path,l,b,polygons,start,s,end,e):
    axs=createPath(path,l,b,polygons)
    startx,starty=start.xy
    sx,sy=s.xy
    endx,endy=end.xy
    ex,ey=e.xy
    axs.plot([startx,sx],[starty,sy],'g')
    axs.plot([endx,ex],[endy,ey],'g')
    plt.show()


    


    
