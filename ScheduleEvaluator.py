from collections import defaultdict
from collections import namedtuple

class Timewindow:
    def __init__(self, SC, GS, tAos, tLos):
        self.tLos = tLos
        self.tAos = tAos
        self.SC = SC
        self.GS = GS

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(GS: {}, SC: {}, tAos: {}, tLos: {})'.format(self.GS, self.SC, self.tAos, self.tLos)


class Requirement:
    def __init__(self, SC, tBeg, tEnd, tReq):
        self.SC = SC
        self.tBeg = tBeg
        self.tEnd = tEnd
        self.tReq = tReq

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(SC: {}, tBeg: {}, tEnd: {}, tReq: {})'.format(self.SC, self.tBeg, self.tEnd, self.tReq)


class SolutionPair:
    def __init__(self, SC, GS, tStart, tDur):
        self.SC = SC
        self.GS = GS
        self.tStart = tStart
        self.tDur = tDur

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '(SC: {}, GS: {}, tStart: {}, tDur: {})'.format(self.SC, self.GS, self.tStart, self.tDur)


class Solution:
    def __init__(self, solutionpairs):
        self.solutionpairs = solutionpairs

    def __init__(self):
        self.solutionpairs = []

    def addSolutionPair(self, solutionpair):
        self.solutionpairs.append(solutionpair)


class SchedulingProblemInstance:
    def __init__(self, nDays, nSC, nGS, timewindows, requirements):
        self.nDays = nDays
        self.nSC = nSC
        self.nGS = nGS
        self.timewindows = timewindows
        self.requirements = requirements

    def getIntersection(self, a_s, a_e, b_s, b_e):
        if b_s > a_e or a_s > b_e:
            return None
        else:
            o_s = max(a_s, b_s)
            o_e = min(a_e, b_e)
            return o_s, o_e

    def getMultipleUnion(self, a):
        b = []
        for begin, end in sorted(a):
            if b and b[-1][1] >= begin - 1:
                b[-1][1] = max(b[-1][1], end)
            else:
                b.append([begin, end])
        return b

    def evaluateSolution(self, instance):

        # Access window fitness function
        # TODO bug with tAOS and tLOS that overlap
        AW = defaultdict(lambda: [])
        for tw in self.timewindows:
            AW[(tw.GS, tw.SC)].append((tw.tAos, tw.tLos))

        FitAW = 0
        for sol in instance.solutionpairs:
            for tAos, tLos in AW[(sol.GS, sol.SC)]:
                if tAos <= sol.tStart <= tLos and tAos <= sol.tStart + sol.tDur <= tLos:
                    FitAW += 1
        FitAW = FitAW / len(instance.solutionpairs) * 100
        #print(FitAW)

        # Communication clash fitness function
        CW = defaultdict(lambda: [])
        for sol in instance.solutionpairs:
            CW[sol.GS].append((sol.tStart, sol.tDur))

        fSC = 0
        for k, v in CW.items():
            v.sort()
            for i in range(len(v) - 1):
                if v[i + 1][0] < v[i][0] + v[i][1]:
                    fSC -= 1
        FitCS = 100*(len(instance.solutionpairs)+fSC)/len(instance.solutionpairs)
        #print(FitCS)

        candidates = []
        for tw in self.timewindows:
            for s in instance.solutionpairs:
                if tw.GS==s.GS and tw.SC==s.SC:
                    a_s = tw.tAos
                    a_e = tw.tLos
                    b_s = s.tStart
                    b_e = s.tStart + s.tDur
                    #print(tw, s)
                    if b_s > a_e or a_s > b_e:
                        pass
                    else:
                        o_s = max(a_s, b_s)
                        o_e = min(a_e, b_e)
                        #print(tw, s, "-------", o_s, o_e)
                        candidates.append((tw.GS, tw.SC, o_s, o_e))

        #print(candidates)

        FitTR = 0

        GS_usage = defaultdict(lambda: list())
        for r in self.requirements:
            com_time = 0
            for GS, SC, o_s, o_e in candidates:
                if r.SC==SC:
                    t = self.getIntersection(r.tBeg, r.tEnd, o_s, o_e)
                    if t is not None:
                        com_time += t[1]-t[0]
                        GS_usage[GS].append(t)
            if com_time>r.tReq:
                FitTR+=1
            #print(r, com_time)
        FitTR /= len(self.requirements)
        FitTR *= 100

        #print(GS_usage)
        GS_dur = defaultdict(lambda: 0)
        for k, v in GS_usage.items():
            for a, b in self.getMultipleUnion(v):
                GS_dur[k] += b-a

            #print(k, GS_dur[k])

        GS_total = defaultdict(lambda: 0)

        for tw in self.timewindows:
            GS_total[tw.GS]+=tw.tLos-tw.tAos

        FitGU = 100* sum([GS_dur[v] for v in GS_dur.keys()])/sum([GS_total[v] for v in GS_total.keys()])

        ret = {"FitAW": FitAW, "FitCS": FitCS, "FitTR": FitTR, "FitGU": FitGU}
        return ret
