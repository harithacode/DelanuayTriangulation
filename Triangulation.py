from __future__ import division

import numpy as np
import math
import Image, ImageDraw

class Vertex:
	edge = ""
	x = ""
	y = ""
	def __init__(self, xcoordinate, ycoordinate):
		self.x = xcoordinate
		self.y = ycoordinate

class HalfEdge:
	origin = ""
	dest = ""
	twin = ""
	incidentFace = ""
	next = ""
	prev = ""
	def __init__(self, startVertex, endVertex):
		self.origin = startVertex
		self.dest = endVertex
class Face:
	edge = ""
	def __init__(self, givenEdge):
		self.edge = givenEdge



def findTriangle(px,py,vertexlist,edgelist,facelist):
	#for each face in face list. call check
	for currentFace in facelist:
		inside = check(px,py,currentFace)
		if inside==1:
			return currentFace

def check(px,py,currentFace):

	a = currentFace.edge.origin
	b = a.edge.next.origin
	c = b.edge.next.origin

	#first check if the currentface is not the outer face
	if currentFace.edge.origin.x == boundv2x and currentFace.edge.origin.y == boundv2y and currentFace.edge.next.origin.x == boundv1x and currentFace.edge.next.origin.y == boundv1y:
		return 0
	if currentFace.edge.origin.x == boundv3x and currentFace.edge.origin.y == boundv3y and currentFace.edge.next.origin.x == boundv2x and currentFace.edge.next.origin.y == boundv2y:
		return 0
	if currentFace.edge.origin.x == boundv1x and currentFace.edge.origin.y == boundv1y and currentFace.edge.next.origin.x == boundv3x and currentFace.edge.next.origin.y == boundv3y:
		return 0
	
	# first check if any of them fall on the edges
	
	if (py-a.y)*(px-b.x) == (py-b.y)*(px-a.x):
		return 0
	if (py-b.y)*(px-c.x) == (py-c.y)*(px-b.x):
		return 0
	if (py-c.y)*(px-a.x) == (py-a.y)*(px-c.x):
		return 0

	
	# Now it should lie properly in this triangle or not.

	inx = (a.x + b.x + c.x) / 3
	iny = (a.y + b.y + c.y) / 3

	#determine if (px,py) lies on the same side of the line as inx,iny. y1= a.y; y2 = b.y; x1 = a.x; x2 = b.x

	p = b.x-a.x
	q = c.x-b.x
	r = a.x-c.x

	if(p==0):
		result1 = px - a.x
		result2 = inx - a.x
	else:
		slope1 = (b.y-a.y)/(b.x-a.x)
		result1 = py-(slope1*px)+(slope1*a.x)-a.y
		result2 = iny-(slope1*inx)+(slope1*a.x)-a.y

	if(result2<0 and result1<0):
		check1 = 1
	elif(result2>0 and result1>0):
		check1 = 1
	else:
		check1 = 0

	if(q==0):
		result1 = px - b.x
		result2 = inx - b.x
	else:
		slope2 = (c.y-b.y)/(c.x-b.x)
		result1 = py-(slope2*px) + (slope2*b.x) - b.y
		result2 = iny-(slope2*inx) + (slope2*b.x) - b.y

	if(result2<0 and result1<0):
		check2 = 1
	elif(result2>0 and result1>0):
		check2 = 1
	else:
		check2 = 0

	if(r==0):
		result1 = px - c.x
		result2 = inx - c.x
	else:
		slope3 = (a.y-c.y)/(a.x-c.x)
		result1 = py-(slope3*px) + (slope3*c.x) - c.y
		result2 = iny-(slope3*inx) + (slope3*c.x) - c.y

	if(result2<0 and result1<0):
		check3 = 1
	elif(result2>0 and result1>0):
		check3 = 1
	else:
		check3 = 0

	if(check1==1 and check2==1 and check3==1):
		return 1
	else:
		return 0

def checkLegality(givenEdge,givenVertex,vertexlist,edgelist,facelist):

	#first check if the quadrilateral is convex or not. 

	a = givenVertex
	b = givenVertex.edge.next.origin
	d = givenVertex.edge.next.next.origin
	c = givenEdge.twin.next.next.origin

	#bd is the current diagonal. Check if b and d lie on the separate sides of line ac.
	r = a.x-c.x
	if(r==0):
		result1 = b.x - c.x
		result2 = d.x - c.x
	else:
		slope = (a.y-c.y)/(a.x-c.x)
		result1 = b.y-(slope*b.x) + (slope*c.x) - c.y
		result2 = d.y-(slope*d.x) + (slope*c.x) - c.y

	if(result2<0 and result1<0):
		return 1
	elif(result2>0 and result1>0):
		return 1
	else:
		#now we are sure it is a convex polygon. Now check the determinent.
		M = [[b.x,b.y,(b.x*b.x+b.y*b.y),1],[d.x,d.y,(d.x*d.x+d.y*d.y),1],[c.x,c.y,(c.x*c.x+c.y*c.y),1],[a.x,a.y,(a.x*a.x+a.y*a.y),1]]
		#>0 means the edge is legal
		if np.linalg.det(M)>0: 
			return 1
		else:
			return 0


def legalizeEdge(givenEdge, givenVertex, vertexlist,edgelist,facelist):
	#if the edge is incident on super triangle then its legal. It can't be helped
	if givenEdge.origin.x == boundv1x and givenEdge.origin.y == boundv1y and givenEdge.next.origin.x == boundv2x and givenEdge.next.origin.y == boundv2y:
		return
	if givenEdge.origin.x == boundv2x and givenEdge.origin.y == boundv2y and givenEdge.next.origin.x == boundv3x and givenEdge.next.origin.y == boundv3y:
		return
	if givenEdge.origin.x == boundv3x and givenEdge.origin.y == boundv3y and givenEdge.next.origin.x == boundv1x and givenEdge.next.origin.y == boundv1y:
		return 
	legal = checkLegality(givenEdge,givenVertex,vertexlist,edgelist,facelist)
	if legal==1:
		return
	else:
		updatedVertex = flipEdge(givenEdge,givenVertex,vertexlist,edgelist,facelist)
		legalizeEdge(updatedVertex.edge.next,updatedVertex,vertexlist,edgelist,facelist)
		legalizeEdge(updatedVertex.edge.next.next.twin.next,updatedVertex.edge.next.next.twin.origin,vertexlist,edgelist,facelist)
	return

def flipEdge(givenEdge,givenVertex,vertexlist,edgelist,facelist):

	#save the coordinates of the 4 corners and save the twins of the 4 sides.
	# remove the previous formation
	# construct a new formation
	# update twins
	


	#save the coordinates of the 4 corners and save the twins of the 4 sides.

	firstTwinToBeUpdated = givenVertex.edge.twin
	secondTwinToBeUpdated = givenVertex.edge.next.twin.next.twin
	thirdTwinToBeUpdated = givenVertex.edge.next.twin.next.next.twin
	fourthTwinToBeUpdated = givenVertex.edge.next.next.twin
	ax = givenVertex.x
	ay = givenVertex.y
	bx = givenVertex.edge.next.origin.x
	by = givenVertex.edge.next.origin.y
	cx = givenVertex.edge.next.twin.next.next.origin.x
	cy = givenVertex.edge.next.twin.next.next.origin.y
	dx = givenVertex.edge.next.next.origin.x
	dy = givenVertex.edge.next.next.origin.y

	# remove the previous formation. 6 vertics, 6 edges and 2 faces

	a = givenVertex
	b1 = givenVertex.edge.next.origin
	d1 = givenVertex.edge.next.next.origin
	b2 = givenVertex.edge.next.twin.next.origin
	c = givenVertex.edge.next.twin.next.next.origin
	d2 = givenVertex.edge.next.twin.origin

	e1 = givenVertex.edge
	e2 = givenVertex.edge.next
	e3 = givenVertex.edge.next.next
	e4 = b2.edge
	e5 = b2.edge.next
	e6 = b2.edge.next.next

	face1 = e1.incidentFace
	face2 = e4.incidentFace


	facelist.remove(face1)
	facelist.remove(face2)
	vertexlist.remove(a)
	vertexlist.remove(b1)
	vertexlist.remove(d1)
	vertexlist.remove(b2)
	vertexlist.remove(c)
	vertexlist.remove(d2)
	edgelist.remove(e1)
	edgelist.remove(e2)
	edgelist.remove(e3)
	edgelist.remove(e4)
	edgelist.remove(e5)
	edgelist.remove(e6)

	#construct a new formation

	t1a = Vertex(ax,ay)
	t1b = Vertex(bx,by)
	t1c = Vertex(cx,cy)

	vertexlist.append(t1a)
	vertexlist.append(t1b)
	vertexlist.append(t1c)

	e1ab = HalfEdge(t1a,t1b)
	e1bc = HalfEdge(t1b,t1c)
	e1ca = HalfEdge(t1c,t1a)

	newface1 = Face(e1ab)

	e1ab.incidentFace = newface1
	e1ab.next = e1bc
	e1ab.prev = e1ca

	e1bc.incidentFace = newface1
	e1bc.next = e1ca
	e1bc.prev = e1ab

	e1ca.incidentFace = newface1
	e1ca.next = e1ab
	e1ca.prev = e1bc

	edgelist.append(e1ab)
	edgelist.append(e1bc)
	edgelist.append(e1ca)

	t1a.edge = e1ab
	t1b.edge = e1bc
	t1c.edge = e1ca

	facelist.append(newface1)

	#second triangle

	t2a = Vertex(ax,ay)
	t2c = Vertex(cx,cy)
	t2d = Vertex(dx,dy)

	vertexlist.append(t2a)
	vertexlist.append(t2c)
	vertexlist.append(t2d)

	e2ac = HalfEdge(t2a,t2c)
	e2cd = HalfEdge(t2c,t2d)
	e2da = HalfEdge(t2d,t2a)

	newface2 = Face(e2ac)

	e2ac.incidentFace = newface2
	e2ac.next = e2cd
	e2ac.prev = e2da

	e2cd.incidentFace = newface2
	e2cd.next = e2da
	e2cd.prev = e2ac

	e2da.incidentFace = newface2
	e2da.next = e2ac
	e2da.prev = e2cd

	edgelist.append(e2ac)
	edgelist.append(e2cd)
	edgelist.append(e2da)

	t2a.edge = e2ac
	t2c.edge = e2cd
	t2d.edge = e2da

	facelist.append(newface2)

	# update twins for all new members

	e1ab.twin = firstTwinToBeUpdated
	firstTwinToBeUpdated.twin = e1ab
	e1bc.twin = secondTwinToBeUpdated
	secondTwinToBeUpdated.twin = e1bc
	e1ca.twin = e2ac
	e2ac.twin = e1ca
	e2cd.twin = thirdTwinToBeUpdated
	thirdTwinToBeUpdated.twin = e2cd
	e2da.twin = fourthTwinToBeUpdated
	fourthTwinToBeUpdated.twin = e2da

	#return the new vertex as it is present in the left triangle.

	return t1a


pointlist2 = [484,1127,533,1386,561,1479,588,1545,688,1592,606,1354,567,1387,549,1353,630,1488,598,1295,549,1260,672,1533,746,1436,763,1522,712,1292,694,1190,593,1158,633,1053,676,955,608,989,704,1067,758,989,808,839,621,765,528,810,497,903,503,957,550,909,518,937,540,948,589,1000,595,1036,556,985,527,976,506,1011,582,1041,874,1556,955,1464,1018,1387,1061,1440,1035,1501,858,1466,818,1592,886,1384,987,1147,831,960,880,1135,1136,1239,1166,1159,920,1098]
img1 = Image.open("earring.jpg")


edgelist = []
vertexlist = []
facelist = []

xmin = 0
ymin = 0
xmax = img1.size[1] #no of cols in the image
ymax = img1.size[0] #no of rows in the image

dx = xmax - xmin
dy = ymax - ymin

if(dx>dy):
	dmax = dx
else:
	dmax = dy

xmid = (xmax + xmin) * 0.5
ymid = (ymax + ymin) * 0.5

boundv1x = xmid
boundv1y = ymid + (2 * dmax)
boundv2x = xmid - (2 * dmax)
boundv2y = ymid - dmax
boundv3x = xmid + (2 * dmax)
boundv3y = ymid - dmax

#set up the super triangle 

p0x = boundv1x
p0y = boundv1y
p1x = boundv2x
p1y = boundv2y
p2x = boundv3x
p2y = boundv3y


v1 = Vertex(p0x,p0y)
v1out = Vertex(p0x,p0y)
v2 = Vertex(p1x,p1y)
v2out = Vertex(p1x,p1y)
v3 = Vertex(p2x,p2y)
v3out = Vertex(p2x,p2y)

vertexlist.append(v1)
vertexlist.append(v2)
vertexlist.append(v3)
vertexlist.append(v1out)
vertexlist.append(v2out)
vertexlist.append(v3out)

e12 = HalfEdge(v1,v2)
e21 = HalfEdge(v2out,v1out)
e23 = HalfEdge(v2,v3)
e32 = HalfEdge(v3out,v2out)
e31 = HalfEdge(v3,v1)
e13 = HalfEdge(v1out,v3out)

f1 = Face(e12)
f2 = Face(e21)

e12.twin = e21
e12.incidentFace = f1
e12.next = e23
e12.prev = e31

e21.twin = e12
e21.incidentFace = f2
e21.next = e13
e21.prev = e32

e23.twin = e32
e23.incidentFace = f1
e23.next = e31
e23.prev = e12

e32.twin = e23
e32.incidentFace = f2
e32.next = e21
e32.prev = e13

e31.twin = e13
e31.incidentFace = f1
e31.next = e12
e31.prev = e23

e13.twin = e31
e13.incidentFace = f2
e13.next = e32
e13.prev = e21

edgelist.append(e12)
edgelist.append(e21)
edgelist.append(e23)
edgelist.append(e32)
edgelist.append(e31)
edgelist.append(e13)

v1.edge = e12
v2.edge = e23
v3.edge = e31
v1out.edge = e13
v2out.edge = e21
v3out.edge = e32


facelist.append(f1)
facelist.append(f2)

i=0

while(i<len(pointlist2)):
	inside = 0
	f= findTriangle(pointlist2[i],pointlist2[i+1],vertexlist,edgelist,facelist)
	if f is None:
		inside = 0
	else:
		firstTwinToBeUpdated = f.edge.twin
		secondTwinToBeUpdated = f.edge.next.twin
		thirdTwinToBeUpdated = f.edge.next.next.twin
		ax = f.edge.origin.x
		ay = f.edge.origin.y
		bx = f.edge.next.origin.x
		by = f.edge.next.origin.y
		cx = f.edge.next.next.origin.x
		cy = f.edge.next.next.origin.y

		a = f.edge.origin
		b = a.edge.next.origin
		c = b.edge.next.origin

		edge1 = a.edge
		edge2 = b.edge
		edge3 = c.edge
		
		facelist.remove(f)
		vertexlist.remove(a)
		vertexlist.remove(b)
		vertexlist.remove(c)
		edgelist.remove(edge1)
		edgelist.remove(edge2)
		edgelist.remove(edge3)

		# construct every thing anew and update twins
		#first triangle

		t1a = Vertex(ax,ay)
		t1b = Vertex(bx,by)
		t1c = Vertex(pointlist2[i],pointlist2[i+1])

		vertexlist.append(t1a)
		vertexlist.append(t1b)
		vertexlist.append(t1c)

		e1ab = HalfEdge(t1a,t1b)
		e1bc = HalfEdge(t1b,t1c)
		e1ca = HalfEdge(t1c,t1a)

		fnew1 = Face(e1ab)

		e1ab.incidentFace = fnew1
		e1ab.next = e1bc
		e1ab.prev = e1ca

		e1bc.incidentFace = fnew1
		e1bc.next = e1ca
		e1bc.prev = e1ab

		e1ca.incidentFace = fnew1
		e1ca.next = e1ab
		e1ca.prev = e1bc

		edgelist.append(e1ab)
		edgelist.append(e1bc)
		edgelist.append(e1ca)

		t1a.edge = e1ab
		t1b.edge = e1bc
		t1c.edge = e1ca

		facelist.append(fnew1)

		#second triangle

		t2a = Vertex(pointlist2[i],pointlist2[i+1])
		t2b = Vertex(bx,by)
		t2c = Vertex(cx,cy)

		vertexlist.append(t2a)
		vertexlist.append(t2b)
		vertexlist.append(t2c)

		e2ab = HalfEdge(t2a,t2b)
		e2bc = HalfEdge(t2b,t2c)
		e2ca = HalfEdge(t2c,t2a)

		fnew2 = Face(e2ab)

		e2ab.incidentFace = fnew2
		e2ab.next = e2bc
		e2ab.prev = e2ca

		e2bc.incidentFace = fnew2
		e2bc.next = e2ca
		e2bc.prev = e2ab

		e2ca.incidentFace = fnew2
		e2ca.next = e2ab
		e2ca.prev = e2bc

		edgelist.append(e2ab)
		edgelist.append(e2bc)
		edgelist.append(e2ca)

		t2a.edge = e2ab
		t2b.edge = e2bc
		t2c.edge = e2ca

		facelist.append(fnew2)

		#third triangle

		t3a = Vertex(ax,ay)
		t3b = Vertex(pointlist2[i],pointlist2[i+1])
		t3c = Vertex(cx,cy)

		vertexlist.append(t3a)
		vertexlist.append(t3b)
		vertexlist.append(t3c)

		e3ab = HalfEdge(t3a,t3b)
		e3bc = HalfEdge(t3b,t3c)
		e3ca = HalfEdge(t3c,t3a)

		fnew3 = Face(e3ab)

		e3ab.incidentFace = fnew3
		e3ab.next = e3bc
		e3ab.prev = e3ca

		e3bc.incidentFace = fnew3
		e3bc.next = e3ca
		e3bc.prev = e3ab

		e3ca.incidentFace = fnew3
		e3ca.next = e3ab
		e3ca.prev = e3bc

		edgelist.append(e3ab)
		edgelist.append(e3bc)
		edgelist.append(e3ca)

		t3a.edge = e3ab
		t3b.edge = e3bc
		t3c.edge = e3ca

		facelist.append(fnew3)

		#update twins of every thing
		e1ab.twin = firstTwinToBeUpdated
		firstTwinToBeUpdated.twin = e1ab
		e1bc.twin = e2ab
		e1ca.twin = e3ab

		e2ab.twin = e1bc
		e2bc.twin = secondTwinToBeUpdated
		secondTwinToBeUpdated.twin = e2bc
		e2ca.twin = e3bc

		e3ab.twin = e1ca
		e3bc.twin = e2ca
		e3ca.twin = thirdTwinToBeUpdated
		thirdTwinToBeUpdated.twin = e3ca

		legalizeEdge(e1ab,t1c,vertexlist,edgelist,facelist)
		legalizeEdge(e2bc,t2a,vertexlist,edgelist,facelist)
		legalizeEdge(e3ca,t3b,vertexlist,edgelist,facelist)

	i=i+2
#For each edge, if its not incident on one of the supertrinagular points then draw it.

draw = ImageDraw.Draw(img1)

for currentEdge in edgelist:
	if(currentEdge.origin.y==boundv1y or currentEdge.dest.y==boundv1y or currentEdge.origin.x==boundv2x or currentEdge.dest.x==boundv2x or currentEdge.origin.x==boundv3x or currentEdge.dest.x==boundv3x):
		something = 0
	else:
		draw.line([(currentEdge.origin.x,currentEdge.origin.y),(currentEdge.dest.x,currentEdge.dest.y)],fill="yellow")


img1.save("C:/Users/mamatha/Desktop/myimage.jpg")
