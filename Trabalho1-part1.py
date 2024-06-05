from pyomo.environ import *
import random

#Isso aqui é só pq eu tava com preguiça de tirar do zip e dar open, nada de mais
with open('./instances/RanInt_n010_ss_10.txt', 'r') as file:
    dados = file.read()

def ler_instancia(dados):
    linhas = dados.strip().split('\n')

    n, m = list(map(int, linhas[0].split()[:2]))
    
    a_min, a_max, b_min, b_max = list(map(int, linhas[0]. split()[3:7]))
    a = random.randint(a_min, a_max)
    b = random.randint(b_min, b_max)
    

    c = [[0 for _ in range(n)] for _ in range(n)]
    

    for linha in linhas[1:]:
        i, j, custo = map(int, linha.split())
        c[i][j] = custo
        c[j][i] = custo
    
    return n, m, a, b, c

n, m, a, b, c = ler_instancia(dados)

model = ConcreteModel();

model.x = Var([i for i in range(len(c))], [g for g in range(m)], domain = Binary)
model.y = Var(((i, j, g) for i in range(len(c)) for j in range(len(c)) for g in range(m)), domain=NonNegativeIntegers)

model.obj = Objective(expr = sum(c[i][j] * model.y[i,j,g] for g in range(m) for i in range(len(c) - 1) for j in range(i + 1, len(c[i]))), sense=maximize)

model.cons = ConstraintList()

for i in range(len(c)):
    model.cons.add(expr= sum(model.x[i,g] for g in range(m)) == 1)

for g in range(m):
    model.cons.add(expr= sum(model.x[i,g] for i in range(len(c))) <= b)

for g in range(m):
    model.cons.add(expr= sum(model.x[i,g] for i in range(len(c))) >= a)
                       

for g in range(m):
    for i in range(len(c)):
        for j in range(len(c[i])):
            model.cons.add(expr = model.y[i,j,g] <= model.x[i,g])
            model.cons.add(expr = model.y[i,j,g] <= model.x[j,g])
            model.cons.add(expr = model.y[i,j,g] >= model.x[i,g] + model.x[j,g] - 1)

solver = SolverFactory('glpk')
results = solver.solve(model, tee= True)
#Solução ótima encontrada:
print(f'Optimal: {model.obj()}')