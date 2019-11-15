from platypus import Problem, Integer, NSGAII
import json
import requests
from datetime import datetime
import sys

# Parameters to be configured (dependant on the problem)
minSC = 1 # Minimum number of satellite
maxSC = 10 # Maximum number of satellite
minGS = 1 # Minimum number of ground station
maxGS = 5 # Maximum number of ground station


maxlLen = 500 # Maximum length of the schedule
maxTime = 15000 # Maximum time allowed time

populationSize = int(sys.argv[2])
numberOfEvaluations = int(sys.argv[1])

problemType = 'small'
problem = 'I_S_01.xml'

now = datetime.now()

def my_function(x):
    jsonDict = dict()
    jsonDict['problem'] = './' + problemType + '/' + problem
    jsonDict['schedule'] = []
    for i in range(x[0]):
        entry = {'SC': x[4*i + 1], 'GS': x[4*i + 2], 'tStart': x[4*i + 3], 'tDur': x[4*i + 4]}
        #print(i, entry)
        jsonDict['schedule'].append(entry)

    #print(json.dumps(jsonDict))

    r = requests.post("http://localhost:8008", data=json.dumps(jsonDict))
    #print(r.status_code, r.reason, r.text)
    obj = json.loads(r.text)

    f = open("trace_nsga_small_I_S_01_" + now.strftime("%H_%M_%S") + ".txt", "a+")
    
    log = dict()
    log['variable'] = jsonDict['schedule']
    log['objective'] = obj
    f.write(json.dumps(log) + '\n')
    f.close()

    return obj['FitAW'], obj['FitCS'], obj['FitTR'], obj['FitGU']




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
algorithm = NSGAII(problem, population_size=populationSize)
algorithm.run(numberOfEvaluations)

for x in algorithm.result:

    log = dict()
    log['variable'] = []

    glen = var[0].decode(x.variables[0])
    for i in range(glen):
        entry = {'SC': var[4*i + 1].decode(x.variables[4*i + 1]), 'GS': var[4*i + 2].decode(x.variables[4*i + 2]), 
        'tStart': var[4*i + 3].decode(x.variables[4*i + 3]), 'tDur': var[4*i + 4].decode(x.variables[4*i + 4])}
        log['variable'].append(entry)
    
    obj = dict()
    obj['FitAW'], obj['FitCS'], obj['FitTR'], obj['FitGU'] = x.objectives[0], x.objectives[1], x.objectives[2], x.objectives[3]
    log['objective'] = obj

    f = open("nsga_small_I_S_01_" + now.strftime("%H_%M_%S") + ".txt", "a+")
    
    
    f.write(json.dumps(log) + '\n')
    f.close()


