# DelanuayTriangulation
A simple implementation of Delanuay Triangulation in Python



This is a simple implementation of Delanuay Triangulation which I did for my Computational Geometry course.

I have written all the necessary functions along with the main function in a single file (Triangulation.py).

This program triangulates points in a plane. To make the project more interesting, I triangulated points selected from an image(earring.jpg). I have manually sampled the points from the image (x coordinate increases from left to right, y coordinate increases from top to bottom) and hardwired the input into the program.

This is not a generic triangulation program. To make the program operate on a new input edit the following lines in the Triangulation.py:

Line 327: pointlist2 = [484,1127,533,1386,561,1479,588,1545,688,1592,606,1354,567,1387,549,1353,630,1488,598,1295,549,1260,672,1533,746,1436,763,1522,712,1292,694,1190,593,1158,633,1053,676,955,608,989,704,1067,758,989,808,839,621,765,528,810,497,903,503,957,550,909,518,937,540,948,589,1000,595,1036,556,985,527,976,506,1011,582,1041,874,1556,955,1464,1018,1387,1061,1440,1035,1501,858,1466,818,1592,886,1384,987,1147,831,960,880,1135,1136,1239,1166,1159,920,1098]

pointlist2 is the array which contains the points to be triangulated in this format: [x1,y1,x2,y2,......]. These points have been manually sampled from earring.jpg. In line 327 I have initialized the pointlist2 array.

Line 328: img1 = Image.open("earring.jpg")

If you are triangulating points on a different image, specify the full path of the image. In my system, Triangulation.py and the input image are in the same directory. So, I did not mention the full path.

Line 618: draw.line([(currentEdge.origin.x,currentEdge.origin.y),(currentEdge.dest.x,currentEdge.dest.y)],fill="yellow")

The program overlays the triangulation on the given input image. You can specify the color of the triangulation by editing the fill value in this line. I have set the fill value to yellow.

Line 621: img1.save("C:/Users/mamatha/Desktop/myimage.jpg"). In this line specify the full path where you want the end result to be stored.

This program requires PIL (Python Imaging Library. http://www.pythonware.com/products/pil/) along with numpy and Python.

Notes (with reference to code comments):

Face is any closed polygon in a plane. In case of Delanuay triangulation, each face is a triangle. I have used a data structure called Doubly Connected Edge List (DCEL) for this triangulation algorithm.

References:

Section 2.2: The Doubly Connected Edge List, Chapter 2, Computational Geometry: Algorithms and Applications by by Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars. 3rd Edition

Sections 9.1: Triangulations of Planar Point Sets, 9.2: The Delanuay Triangulation, 9.3: Computing The Delanuay Triangulation, Chapter 9, Computational Geometry: Algorithms and Applications by Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars. 3rd Edition

Exercise 9.5, Chapter 9, Computational Geometry: Algorithms and Applications by Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars. 3rd Edition

For queries, please email: haritha.gorijavolu@gmail.com
