import matplotlib.pyplot as plt
# %matplotlib inline
import gpxpy
import geopy


from matplotlib import rcParams
# Set Font

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
rcParams["font.size"]= 20

def get_elevation(gpx):
    import math
    from geopy import distance 

    yk_lat   = []
    yk_lon   = []
    yk_ele0  = [] # gpx elevation
    yk_ele1  = [] # SRTM elevation from NASA
    dis_flat = [] # spherical distance
    dis_eucl = [] # euclidian /b surface distance

    for segment in gpx.tracks[0].segments:
        for p in segment.points:     
            lat = p.latitude
            lon = p.longitude
            yk_lat.append(lat)
            yk_lon.append(p.longitude)
            yk_ele0.append(p.elevation)
            
    dis_sum_flat = []
    dis_sum_eucl = []
    s = 0
    s1 = 0

    # point-to-point distance
    for i, x in enumerate(yk_lat[1:], 1):
        p1 = (yk_lat[i-1], yk_lon[i-1])
        p2 = (yk_lat[i], yk_lon[i])    
        dis = distance.distance(p1, p2).km
        dis_flat.append( dis )
        dis_eucl.append( math.sqrt(dis**2 + (yk_ele0[i]/1000 - yk_ele0[i-1]/1000)**2) )

    # cumulated sum    
    for i, d in enumerate(dis_flat):    
        s += dis_flat[i]
        s1 += dis_eucl[i]
        dis_sum_flat.append(s)
        dis_sum_eucl.append(s1)

    return [dis_sum_flat, yk_ele0[1:]]


from glob import glob
x = glob("*.gpx")

f, d1 = plt.subplots(1,1)
f.set_figheight(12)
f.set_figwidth(15)

for fn in x:
    with open(fn) as f:
        gpx = gpxpy.parse(f)
    
    [d, e0] = get_elevation(gpx)
    d1.plot(d, e0, lw=5, label = fn.split('.')[0])    
    #d1.plot(d, e1, lw=1, color='k', ls = ':' )   

d1.set_xlabel("距離 (KM)")
d1.set_ylabel("海跋 (M)")
# d1.legend(prop='PingFang HK');
d1.legend();
d1.grid()
