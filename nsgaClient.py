from platypus import Problem, Integer, NSGAII
import json
import requests

def my_function(x):
    """ Some objective function"""
    jsonDict = dict()
    jsonDict['problem'] = './small/I_S_01.xml'
    jsonDict['schedule'] = []
    for i in range(x[0]):
        entry = {'SC': x[i + 1], 'GS': x[i + 2], 'tStart': x[i + 3], 'tDur': x[i + 4]}
        jsonDict['schedule'].append(entry)

    #print(json.dumps(jsonDict))

    r = requests.post("http://localhost:8008", data=json.dumps(jsonDict))
    print(r.status_code, r.reason, r.text)
    obj = json.loads(r.text)

    return obj['FitAW'], obj['FitCS'], obj['FitTR'], obj['FitGU']


minSC = 1
maxSC = 5
minGS = 1
maxGS = 5

maxlLen = 100
maxTime = 15000

scheduleLen = Integer(1, maxlLen)
var = [scheduleLen]
for i in range(maxlLen):
    var.append(Integer(minSC, maxSC))
    var.append(Integer(minGS, maxGS))
    var.append(Integer(0, maxTime))
    var.append(Integer(0, maxTime))

problem = Problem(len(var), 4)

problem.types[:] = var
problem.directions[:] = Problem.MAXIMIZE
problem.function = my_function
algorithm = NSGAII(problem)
algorithm.run(3000)
print('Final')
for x in algorithm.result:
    print(x)

