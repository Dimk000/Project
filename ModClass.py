import numpy as np
import pprint

class SDModulator:
    def __init__(self, PulseTime, timeStep, modelTime, Uref, Uin):
        self.modelTime = modelTime
        self.timeStep = timeStep
        self.Uref = Uref
        self.Uin = Uin
        self.pulseTime = PulseTime
        self.R = np.zeros(int(self.modelTime/self.timeStep)+1)
        self.dout = np.zeros(int(self.modelTime)+1)

    def sdModulatorHardPrecision(self,forRound):
        Compare, i, j = 1, 1, 1
        currentTime = self.timeStep
        self.R[0] = 0
        self.dout[0] = Compare
        if type(self.Uin) is not float:
            self.Uin[0] = 0
        currentT0 = self.pulseTime
        if type(self.Uin) is float:
            while currentTime <= self.modelTime:
                if Compare == 1:
                    self.R[i] = self.R[i-1] + (self.Uin + self.Uref)*self.timeStep
                else:
                    self.R[i] = self.R[i-1] + (self.Uin - self.Uref)*self.timeStep
                if currentTime >= currentT0:
                    if self.R[i] > 0:
                        Compare = 0
                    else:
                        Compare = 1
                    currentT0 += self.pulseTime
                    self.dout[j] = Compare
                    j += 1
                i += 1
                currentTime += self.timeStep
                try: currentTime = round(currentTime, forRound)
                except: pass
        else:
            while currentTime <= self.modelTime:
                if Compare == 1:
                    self.R[i] = self.R[i-1] + (self.Uin[i-1] + self.Uref)*self.timeStep
                else:
                    self.R[i] = self.R[i-1] + (self.Uin[i-1] - self.Uref)*self.timeStep
                if currentTime >= currentT0:
                    if self.R[i] > 0:
                        Compare = 0
                    else:
                        Compare = 1
                    currentT0 += self.pulseTime
                    self.dout[j] = Compare
                    j += 1
                i += 1
                currentTime += self.timeStep
                try: currentTime = round(currentTime, forRound)
                except: pass
        time = np.linspace(0, self.modelTime, len(self.R))
        pprint.pprint(self.R)
        pprint.pprint(self.dout)
        return self.R, self.dout, time

class SDModulatorVer2:
    def __init__(self, Uin, Uref, PulseTime, PulseNumbers, timeStep, dCoeff, Precision):
        self.Uin = Uin
        self.Uref = Uref
        self.PulseTime = PulseTime
        self.PulseNumbers = PulseNumbers
        self.timeStep = timeStep
        self.dCoeff = dCoeff
        self.Precision = Precision
        self.ArraySizeTest = int(self.PulseNumbers*self.PulseTime/self.timeStep)
        self.R = np.zeros(int(self.PulseNumbers / self.timeStep) + 1)
        self.dout = np.zeros((int(self.PulseNumbers + 1) * self.dCoeff))

    def sdModificationHardPrecision(self):
        if len(self.Uin)>self.ArraySizeTest:
            self.Uin[0] = 0
            delta_t = self.timeStep
            self.R[0] = 0
            T0_Active = self.PulseTime
            time_Active = self.timeStep
            t0 = self.PulseTime/self.dCoeff
            LogicNum = 1
            Compare = 1
            for j in range(0, self.dCoeff+1, 1):
                self.dout[j] = Compare
            j = self.dCoeff
            for i in range(1,self.ArraySizeTest, 1):
                if Compare == 1: self.R[i] = self.R[i-1] + delta_t*(self.Uin[i]+self.Uin[i-1])/2 + self.Uref*delta_t
                else: self.R[i] = self.R[i - 1] + delta_t * (self.Uin[i] + self.Uin[i - 1]) / 2 - self.Uref * delta_t
                if time_Active >= T0_Active+self.Precision or time_Active >= T0_Active-self.Precision:
                    if (self.R[i] >= 0+self.Precision): Compare = 0
                    else: Compare, LogicNum = 1,1
                    if LogicNum == 1:
                        T0_Active += self.PulseTime
                        LogicNum = 0
                        for j1 in range(j,j+self.dCoeff, 1): self.dout[j1] = Compare
                        j += self.dCoeff
                    else:
                        T0_Active += t0
                        self.dout[j] = Compare
                        j += 1
                time_Active+=self.timeStep
        time = np.linspace(0, self.PulseNumbers, len(self.R))
        pprint.pprint(self.Uin)
        return self.R, self.dout, time