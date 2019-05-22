import numpy as np
from numpy import matrix
from numpy.linalg import svd
from math import pi
import cvxpy as cp
from cvxpy.atoms.lambda_min import lambda_min
from cvxpy.atoms.norm import norm
from copy import deepcopy

def rotate_coordinate(xy, radians):
	"""Use numpy to build a rotation matrix and take the dot product."""
	x, y = xy
	c, s = np.cos(radians), np.sin(radians)
	j = np.matrix([[-c, -s], [s, -c]])
	m = np.dot(j, [x, y])

	return float(m.T[0]), float(m.T[1])



############################### Find gain A #################################
initial_position = np.matrix([[-50, -50], [0, -50], [50, -50]])
# adj = np.matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])

print(f"Initial position: {initial_position}.")
print(f"Shape of initial_position: {initial_position.shape}.")

destination = np.array([-50, 0, 0, 50, 50, 0])
# destination = np.array([0, 0, 4, 0, 4, 3])
destination_bar = np.zeros(len(destination))
for i in range(0,len(destination),2):
	destination_bar[i], destination_bar[i+1] = rotate_coordinate((destination[i], destination[i+1]), pi/2)
	# destination_bar[i] = round(destination_bar[i], 2)
	# destination_bar[i+1] = round(destination_bar[i+1], 2)
	destination_bar[i] = destination_bar[i]
	destination_bar[i+1] = destination_bar[i+1]

number_of_agent = int(len(destination)/2)

print(f"\n\ndestination: {destination}.")
print(f"rotated destination: {destination_bar}.")	

vector_one = np.ones(len(destination))
vector_one_bar = np.ones(len(destination))
for i in range(0,len(vector_one_bar),2):
	vector_one_bar[i] = -1

print(f"\n\nvector_one: {vector_one}.")
print(f"vector_one_bar: {vector_one_bar}.")

# vector_N = np.concatenate((vector_one, vector_one_bar, destination, destination_bar), axis = 1)
N = np.matrix([vector_one, vector_one_bar, destination, destination_bar]).transpose()
print(f"\n\nMatrix N: {N}.")
print(f"Shape of N: {N.shape}.")

# Solve singular value decomposition (SVD) of N
U,_,_ = svd(N)
U = np.array(U)
print(f"\n\nMatrix U: {U}")
print(f"Shape of U: {U.shape}.")

Q = deepcopy(U[:,4:len(destination)])
print(f"\n\nMatrix Q: {Q}")
print(f"Shape of Q: {Q.shape}.")

# Solve SDP problem
A = cp.Variable(shape = (len(destination), len(destination)))
A_bar = Q.transpose()*A*Q

print(f"\n\nShape of A: {A.shape}.")
print(f"Shape of A_bar: {A_bar.shape}.")

objective = cp.Maximize(lambda_min(-A_bar))
constraint = [A*N == 0,
			  norm(A) <= 10]

problem = cp.Problem(objective, constraint)
problem.solve()

gain_A = np.matrix(A.value).round(5)
# gain_A = np.matrix(A.value)

print(f"Status: {problem.status}. \n")
print(f"Optimal value: {problem.value}. \n")
print(f"Optimal variable: \n{gain_A}. \n")

print(f"Shape of gain_A: {gain_A.shape}")

gain_Ai = np.zeros((number_of_agent,number_of_agent,2,2)) # I try putting everything nice and neat
														  # A will equal to Ai later on

for i in range(0,gain_A.shape[0],2): # go through all agents
	for j in range(0,gain_A.shape[1],2): # go through all neighbor
		# if (i != j):
		#     gain_Aij = np.matrix([[gain_A[i][j], gain_A[i][j+1]],[gain_A[i+1][j], gain_A[i+1][j+1]]])
		#     gain_Ai[int(i/2),int(j/2)] = gain_Aij
		# else:
		#     gain_Ai[int(i/2),int(j/2)] = np.zeros((2,2))
		gain_Aij = np.matrix([[gain_A[i][j], gain_A[i][j+1]],[gain_A[i+1][j], gain_A[i+1][j+1]]])
		gain_Ai[int(i/2),int(j/2)] = gain_Aij

gain_A = gain_Ai # The final gain.

print(f"Gain A: \n{gain_A}\n")
print(f"Shape of gain A: {gain_A.shape}")

########################### Simulation ############################
time_interval = 0.01 # 1 second
current_position = deepcopy(initial_position)

# control vector
u = np.zeros((number_of_agent,2,1))
print(f"u: {u}.\n\n")

for iteration in range(50): # iterate for 5 times
	print(f"Iteration number: {iteration}.")
	for i in range(number_of_agent): # calculate new position of all agents
		u[i] = np.zeros((2,1))
		for j in range(number_of_agent): # calculate control vector of 1 agent
			u[i] = u[i] + gain_A[i][j]*current_position[j].transpose()

		current_position[i] = current_position[i] + u[i].transpose()*time_interval
		# print(f"control vector of agent {i}: {u[i].transpose()}")
		print(f"current_position of agent {i}: {current_position[i]}\n")

	print("\n")

