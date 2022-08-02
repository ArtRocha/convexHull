import random
import numpy as np
from math import ceil, floor
import matplotlib.pyplot as plt
"""
Computes the Convex Hull with the Graham Scan algorithm
Use:
	h = ConvexHull()
	print(h.hull)
"""

class ConvexHull:
	def __init__(self, points):
		if not points:
			self.points = [(random.randint(0,100),random.randint(0,100)) for i in range(50)]
		else:
			self.points = points
		self.hull = self.compute_convex_hull()
    
	def get_cross_product(self,p1, p2, p3):
		return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))

	def get_slope(self,p1, p2):
		if p1[0] == p2[0]:
			return float('inf')
		else:
			return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])

	def compute_convex_hull(self):
		hull = []
		self.points.sort(key=lambda x:[x[0],x[1]])
		start = self.points.pop(0)
		hull.append(start)
		self.points.sort(key=lambda p: (self.get_slope(p,start), -p[1],p[0]))
		for pt in self.points:
			hull.append(pt)
			while len(hull) > 2 and self.get_cross_product(hull[-3],hull[-2],hull[-1]) < 0:
				hull.pop(-2)
		return hull


def taking_cords(predict_matrix):
    #Pegando as posições do valores 1
    position = []
    for x in range (len(predict_matrix)):
        for b in range(len(predict_matrix[0])):
            if predict_matrix[x][b] == 1:
                position.append((x,b))
    return position


def interpolate(initPos, nextPos, corrected_matrix):
    for i in range(0,100):
        amount = i
        position= {
            'x': ceil(initPos[0] + (amount / 100) * (nextPos[0] - initPos[0])),
            'y': ceil(initPos[1] + (amount / 100) * (nextPos[1] - initPos[1])),
        },
        corrected_matrix[position[0]['x']][position[0]['y']] =1

def drawn_lines_and_paint_inside(border):
    predict_matrix_corrected=np.zeros((len(predict_matrix),len(predict_matrix[0])),dtype=np.uint8)

#traçando uma linha entre os pontos das bordas
    for i,pos in enumerate(border.hull):
        if i >0:
            # print(f'{border.hull[i-1]} {pos}')
            interpolate(border.hull[i-1],pos,predict_matrix_corrected)
        else:
            # print(f'{border.hull[-1]} {pos}')
            interpolate(border.hull[-1],pos,predict_matrix_corrected)
        # print(interpolate(border[-1],pos)) # --> a = interpolate(border[-1],pos) --> a[0][0]['x'] para pegar o valor de x 


    # print(a)
    # print('_'*30)
    # print(predict_matrix_corrected)
    print()
    # print('ueba')


    #pintando os pixels dentro das linhas 
    general_interval = []
    for x in range(len(predict_matrix_corrected)):
        interval = []
        for sy in range(len(predict_matrix_corrected[0])):
            if predict_matrix_corrected[x][sy]==1:
                interval.append(sy)
        for y in range(len(interval)):
            if len(interval)<2:
                break
            if interval[y]!= interval[-1]:    
                if interval[y]+1 != interval[y+1]:
                    general_interval.append((x,interval[y],interval[y+1]))
                    for line in range(interval[y],interval[y+1]):
                        predict_matrix_corrected[x][line]=1


    return predict_matrix_corrected

predict_matrix = [
    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],]

predict_matrix2 = [
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
     [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]



def main(matriz):
    position = taking_cords(matriz)
    #pegando a posição das bordas na imagem
    border = ConvexHull(position)
    final_matrix = drawn_lines_and_paint_inside(border)
    return final_matrix

test = [predict_matrix, predict_matrix2]
matrixList =[]

for matriz in test:
    mat = main(matriz)
    matrixList.append(mat)

im2 = plt.figure(figsize=(10,3))
ax2 = im2.add_subplot(1,4,1)
ax2.title.set_text('original_nucleus')
plt.imshow(matrixList[0])


ax1 = im2.add_subplot(1,4,2)
ax1.title.set_text('graham_scan_xgb')
plt.imshow(matrixList[1])
plt.show()
    