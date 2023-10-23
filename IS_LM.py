import numpy as np
import plotly.graph_objects as go


class IS_LM:

    def __init__(self, param_IS_1: list, param_LM_1: list, param_IS_2: list, param_LM_2: list, FED = True):

        # Equation parameters
        self.param_IS_1 = param_IS_1
        self.param_IS_2 = param_IS_2
        self.param_LM_1 = param_LM_1
        self.param_LM_2= param_LM_2
        self.FED = FED

        # Specifying the equation parameters (for the first ones)
        self.C0 = param_IS_1[0]
        self.C1 = param_IS_1[1]
        self.a = param_IS_1[2]
        self.A = param_IS_1[3]
        self.G = param_IS_1[4]
        self.T = param_IS_1[5]

        if (self.FED == True):
            self.M = param_LM_1[0]
            self.P = param_LM_1[1]
            self.L = param_LM_1[2]
            self.Li = param_LM_1[3]
            self.Ly = param_LM_1[4]
        else:
            self.rates_1 = param_LM_1[0]


        # Specifying the equation parameters (for the second ones)
        self.C0_2 = param_IS_2[0]
        self.C1_2 = param_IS_2[1]
        self.a_2 = param_IS_2[2]
        self.A_2 = param_IS_2[3]
        self.G_2 = param_IS_2[4]
        self.T_2 = param_IS_2[5]

        if (self.FED == True):
            self.M_2 = param_LM_2[0]
            self.P_2 = param_LM_2[1]
            self.L_2 = param_LM_2[2]
            self.Li_2 = param_LM_2[3]
            self.Ly_2 = param_LM_2[4]
        else:
            self.rates_2 = param_LM_2[0]


        # Equilibrium (central bank policy -> Money Supply)
        if (self.FED == True):
            ## Fist equilibrium
            self.LM_value_1 = (self.M / self.P) - self.L
            self.IS_value_1 = (1 / (1 - self.C1)) * (self.C0 - (self.C1 * self.T) + self.A + self.G)

            self.LM_Y_variation_1 = self.Ly
            self.LM_i_variation_1 = -self.Li
            self.IS_Y_variation_1 = 1
            self.IS_i_variation_1 = (self.a / (1 - self.C1))

            ### Solving by matrix
            self.Matrix_A = np.matrix([[self.LM_Y_variation_1, self.LM_i_variation_1],
                                       [self.IS_Y_variation_1, self.IS_i_variation_1]])
            self.Matrix_B = np.matrix([[self.LM_value_1],
                                       [self.IS_value_1]])
            self.Matrix_A_1 = self.Matrix_A.I
            self.Matrix_X = np.dot(self.Matrix_A_1, self.Matrix_B)

            #### Results
            self.income_1 = float(self.Matrix_X[0])
            self.rates_1 = float(self.Matrix_X[1])
            self.consumption_1 = self.C0 + self.C1*(self.income_1 - self.T)
            self.investment_1 = self.A - (self.a*self.rates_1)

            ## Second equilibrium
            self.LM_value_2 = (self.M_2 / self.P_2) - self.L_2
            self.IS_value_2 = (1 / (1 - self.C1_2)) * (self.C0_2 - (self.C1_2 * self.T_2) + self.A_2 + self.G_2)

            self.LM_Y_variation_2 = self.Ly_2
            self.LM_i_variation_2 = -self.Li_2
            self.IS_Y_variation_2 = 1
            self.IS_i_variation_2 = (self.a_2 / (1 - self.C1_2))

            ### Solving by matrix
            self.Matrix_A = np.matrix([[self.LM_Y_variation_2, self.LM_i_variation_2],
                                       [self.IS_Y_variation_2, self.IS_i_variation_2]])
            self.Matrix_B = np.matrix([[self.LM_value_2],
                                       [self.IS_value_2]])
            self.Matrix_A_1 = self.Matrix_A.I
            self.Matrix_X = np.dot(self.Matrix_A_1, self.Matrix_B)

            #### Results
            self.income_2 = float(self.Matrix_X[0])
            self.rates_2 = float(self.Matrix_X[1])
            self.consumption_2 = self.C0_2 + self.C1_2*(self.income_2 - self.T_2)
            self.investment_2 = self.A_2 - (self.a_2*self.rates_2)

        else:
            # Equilibrium (central bank policy -> Interest Rate)
            ## Solving the equation for income
            self.IS_value_1 = (1 / (1 - self.C1)) * (self.C0 - (self.C1 * self.T) + self.A + self.G)
            self.IS_value_2 = (1 / (1 - self.C1_2)) * (self.C0_2 - (self.C1_2 * self.T_2) + self.A_2 + self.G_2)

            ### Results
            self.income_1 = (1 / (1 - self.C1)) * (self.C0 - (self.C1 * self.T) + self.A + self.G - (self.a * self.rates_1))
            self.income_2 = (1 / (1 - self.C1_2)) * (self.C0_2 - (self.C1_2 * self.T_2) + self.A_2 + self.G_2 - (self.a_2 * self.rates_2))
            self.consumption_1 = self.C0 + self.C1*(self.income_1 - self.T)
            self.investment_1 = self.A - (self.a*self.rates_1)
            self.consumption_2 = self.C0_2 + self.C1_2*(self.income_2 - self.T_2)
            self.investment_2 = self.A_2 - (self.a_2*self.rates_2)

    
    # Plot function
    def plot(self):
        ## generating income values
        y = np.linspace(round(self.income_1 - (self.income_1 * 0.9)),
                         round(self.income_1 + (self.income_1 * 0.9)),
                           round(self.income_1))

        ## generating values for IS and LM curves (solving the equations for r)
        IS = (((1 - self.C1) / self.a) * self.IS_value_1) - (((1 - self.C1) / self.a) * y)
        LM = (1/self.Li)*((self.LM_Y_variation_1)*y - self.LM_value_1) if (self.FED == True) else self.rates_1 - (y - y)

        ## generating values for IS' and LM' curves
        IS_2 = (((1 - self.C1_2) / self.a_2) * self.IS_value_2) - (((1 - self.C1_2) / self.a_2) * y)
        LM_2 = (1/self.Li_2)*((self.LM_Y_variation_2)*y - self.LM_value_2) if (self.FED == True) else self.rates_2 - (y - y)

        ## defining the figure
        fig = go.Figure()
        ### IS curve
        fig.add_trace(go.Scatter(x=y, y=IS,
                            mode='lines',
                            name='IS',
                            line=dict(color='orange')))
        ### LM curve
        fig.add_trace(go.Scatter(x=y, y=LM,
                            mode='lines',
                            name='LM',
                            line=dict(color='royalblue')))
        ### IS' curve
        if (self.param_IS_1 != self.param_IS_2):
            fig.add_trace(go.Scatter(x=y, y=IS_2,
                                mode='lines',
                                name='IS\'',
                                line=dict(color='red')))
        ### LM' curve
        if (self.param_LM_1 != self.param_LM_2):
            fig.add_trace(go.Scatter(x=y, y=LM_2,
                                mode='lines',
                                name='LM\'',
                                line=dict(color='darkblue')))
        ## updating layout
        fig.update_layout(title=dict(xref='paper', yref='paper', x=0.5, y=1.0,
                        xanchor='left', yanchor='bottom',
                        text='IS-LM'),
                        xaxis_title='Income',
                        yaxis_title='Rates')
        return fig