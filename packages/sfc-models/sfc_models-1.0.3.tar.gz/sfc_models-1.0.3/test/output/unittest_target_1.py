
"""
FNAME

Machine-generated model code
"""



class SFCModel(object):
    """
    Model

    Implements the following system of equations.

    Endogenous variables and parameters
    ===================================
    x = y + 2,
    y = .5 * x,
    where lagged variables are:
    LAG_x(t) = x(t-1)
    
    
    Exogenous Variables
    ===================
    dummy

    """
    def __init__(self):
        self.MaxIterations = 100
        self.MaxTime = 3
        self.T = 0
        self.x = [0.000000,]
        self.y = [0.000000,]
        self.dummy = [1., 1., 1.]


    def Iterator(self, in_vec):
        x, y, LAG_x, dummy = in_vec 
        NEW_x = y + 2
        NEW_y = .5 * x
        NEW_LAG_x = LAG_x
        NEW_dummy = dummy
        return NEW_x, NEW_y, NEW_LAG_x, NEW_dummy


    def main(self):
        for t in range(0, self.MaxTime):
            self.T = t
            self.RunOneStep()

    def RunOneStep(self):
        x = self.x[-1]
        y = self.y[-1]
        LAG_x = self.x[self.T -1]
        dummy = self.dummy[self.T]

        orig_vector = (x, y, LAG_x, dummy)
        err = 1.
        cnt = 0
        while err > .001:
            new_vector = self.Iterator(orig_vector)
            err = self.CalcError(orig_vector, new_vector)
            orig_vector = new_vector
            cnt += 1
            if cnt > self.MaxIterations:
                raise ValueError('No Convergence!')
        x = orig_vector[0]
        self.x.append(x)
        y = orig_vector[1]
        self.y.append(y)


    @staticmethod
    def CalcError(vec1, vec2):
        err = 0.
        for val1, val2 in zip(vec1, vec2):
            err += abs(val1 - val2)
        return err


if __name__ == '__main__':
    obj = SFCModel()
    obj.main()


