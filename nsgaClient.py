from platypus import Problem, Integer, NSGAII
import json
import requests
from datetime import datetime
import sys


class ProblemLogger:
    def __init__(self, file, header):
        self.file = file
        self.write_header = True
        self.header = header

    def log(self, instance):
        f = open(self.file, "a+")
        if self.write_header:
            self.write_header = False
            f.write(self.header + '\n')
        f.write(json.dumps(instance) + '\n')
        f.close()


start_time = datetime.now()

"""
Change all of the settings here
----------------------------------------------------------------
"""
# Parameters to be configured (dependant on the problem)
min_space_craft = 1  # Minimum number of satellite
max_space_craft = 10  # Maximum number of satellite
min_ground_station = 1  # Minimum number of ground station
max_ground_station = 5  # Maximum number of ground station

max_schedule_length = 500  # Maximum length of the schedule
max_time = 15000  # Maximum time allowed time

population_size = int(sys.argv[2])
number_of_evaluations = int(sys.argv[1])

problem_type = 'small'
problem_name = 'I_S_01.xml'

problem_path = './' + problem_type + '/' + problem_name
trace_file_name = 'trace_nsga_small_I_S_01_' + start_time.strftime("%H_%M_%S") + '.txt'
results_file_name = 'results_nsga_small_I_S_01_' + start_time.strftime("%H_%M_%S") + '.txt'

file_header = json.dumps(
    dict(algorithm='NSGA', population_size=population_size, number_of_evaluations=number_of_evaluations,
         problem_type=problem_type, problem_name=problem_name))

tracer_logger = ProblemLogger(trace_file_name, file_header)
result_logger = ProblemLogger(results_file_name, file_header)

"""
----------------------------------------------------------------
"""


def log_to_file(file_name, instance):
    f = open(file_name, "a+")
    f.write(json.dumps(instance) + '\n')
    f.close()


def evaluate(x):
    request_json = dict()
    request_json['problem'] = problem_path
    request_json['schedule'] = []
    for i in range(x[0]):
        request_json['schedule'].append(
            {'SC': x[4 * i + 1],
             'GS': x[4 * i + 2],
             'tStart': x[4 * i + 3],
             'tDur': x[4 * i + 4]})

    r = requests.post("http://localhost:8008", data=json.dumps(request_json))
    result = json.loads(r.text)

    tracer_logger.log({'variable': request_json['schedule'], 'objective': result})

    return result['FitAW'], result['FitCS'], result['FitTR'], result['FitGU']


if __name__ == "__main__":
    # Construct encoding for each schedule
    # Encoding is constructed in the following way:
    # [schedule_length_variable, (SC_1, GS_1, begin_1, duration_1), (SC_2, GS_2, begin_2, duration_2), ....]
    schedule_length_variable = Integer(1, max_schedule_length)
    var = [schedule_length_variable]
    for i in range(max_schedule_length):
        var.append(Integer(min_space_craft, max_space_craft))
        var.append(Integer(min_ground_station, max_ground_station))
        var.append(Integer(0, max_time))
        var.append(Integer(0, max_time))

    # Define the whole problem
    problem = Problem(nvars=len(var), nobjs=4)
    problem.types[:] = var
    problem.directions[:] = Problem.MAXIMIZE
    problem.function = evaluate

    # Define the algorithm and run it
    algorithm = NSGAII(problem, population_size=population_size)
    algorithm.run(number_of_evaluations)

    # Log all the results to file
    for x in algorithm.result:
        log = dict()
        log['variable'] = []
        glen = var[0].decode(x.variables[0])
        for i in range(glen):
            log['variable'].append({'SC': var[4 * i + 1].decode(x.variables[4 * i + 1]),
                                    'GS': var[4 * i + 2].decode(x.variables[4 * i + 2]),
                                    'tStart': var[4 * i + 3].decode(x.variables[4 * i + 3]),
                                    'tDur': var[4 * i + 4].decode(x.variables[4 * i + 4])})

        log['objective'] = {'FitAW': x.objectives[0], 'FitCS': x.objectives[1], 'FitTR': x.objectives[2],
                            'FitGU': x.objectives[3]}
        result_logger.log(log)

