from xml.dom import minidom
from ScheduleEvaluator import Timewindow, SchedulingProblemInstance, Requirement, SolutionPair, Solution
import json

def populationInstanceParser(jsonstr):
    jsonObj = json.loads(jsonstr)
    problem = jsonObj["problem"]
    solution = Solution()
    for d in jsonObj["schedule"]:
        solution.addSolutionPair(SolutionPair(d['SC'], d['GS'], d['tStart'], d['tDur']))
    return problem, solution


class XMLParser:
    def __init__(self, filename):
        self.filename = filename
        doc = minidom.parse(filename)
        items = doc.getElementsByTagName('basic')
        self.nGS = int(items[0].attributes['nGS'].value)
        self.nSC = int(items[0].attributes['nSC'].value)
        self.nDays = int(items[0].attributes['nDays'].value)
        self.timewindows = []
        timewindowxml = doc.getElementsByTagName('timewindow')
        for tw in timewindowxml:
            GS = int(tw.attributes['GS'].value)
            SC = int(tw.attributes['SC'].value)
            tAos = int(tw.attributes['tAos'].value)
            tLos = int(tw.attributes['tLos'].value)
            self.timewindows.append(Timewindow(GS, SC, tAos, tLos))

        self.requirements = []
        requirementsxml = doc.getElementsByTagName('comunication')
        for req in requirementsxml:
            SC = int(req.attributes['SC'].value)
            tBeg = int(req.attributes['tBeg'].value)
            tEnd = int(req.attributes['tEnd'].value)
            tReq = int(req.attributes['tReq'].value)
            self.requirements.append(Requirement(SC, tBeg, tEnd, tReq))

    def getProblem(self):
        return SchedulingProblemInstance(self.nDays, self.nSC, self.nGS, self.timewindows, self.requirements)
