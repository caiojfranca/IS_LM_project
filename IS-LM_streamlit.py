import streamlit as st
from IS_LM import IS_LM

st.set_page_config(layout = 'wide')
st.title('IS-LM Model')


# Central Bank Monetary Policy
central_bank = st.radio('Central Bank Policy', ['Money Supply', 'Interest Rate'])

# Standard Parameters
if 'param_IS' not in st.session_state:
    st.session_state['param_IS'] = [15.0, 0.8, 0.5, 15.0, 20.0, 20.0]
    st.session_state['param_IS_2'] = [15.0, 0.8, 0.5, 15.0, 20.0, 20.0]
    st.session_state['param_LM'] = [25.0, 5.0, 6.0, 0.5, 0.03]
    st.session_state['param_LM_2'] = [25.0, 5.0, 6.0, 0.5, 0.03]
    
# Changing The Policy
if (len(st.session_state['param_LM']) > 1) and (central_bank == 'Interest Rate'):
    st.session_state['param_LM'] = [8.00]
    st.session_state['param_LM_2'] = [8.00]
elif (len(st.session_state['param_LM']) < 2) and (central_bank == 'Money Supply'):
    st.session_state['param_LM'] = [25.0, 5.0, 6.0, 0.5, 0.03]
    st.session_state['param_LM_2'] = [25.0, 5.0, 6.0, 0.5, 0.03]
    
# Functions    
def setting_the_parameters(param):
    st.session_state['param_IS'] = param[0]
    st.session_state['param_LM'] = param[1]
    st.session_state['param_IS_2'] = param[2]
    st.session_state['param_LM_2'] = param[3]

def new_parameters(param):
    st.session_state['param_IS_2'] = param[0]
    st.session_state['param_LM_2'] = param[1]

# Defining The Models
model = IS_LM(param_IS_1 = st.session_state['param_IS'],
                param_LM_1 = st.session_state['param_LM'],
                param_IS_2 = st.session_state['param_IS_2'],
                param_LM_2 = st.session_state['param_LM_2'],
                FED = True if (central_bank == 'Money Supply') else False)

# Number Inputs
col1, col2 = st.columns(2)
with col1:
    # IS Inputs
    st.latex(r'''
    Y = \frac{1}{1-c_1}[(c_0 + c_1T + A + \bar{G}) - ar]
    ''')
    IS_col1, IS_col2 = st.columns(2)
    with IS_col1:
        c_0 = st.number_input(label = '$c_0$', 
                                value = st.session_state['param_IS_2'][0])
        
        c_1 = st.number_input(label = '$c_1$', 
                                value = st.session_state['param_IS_2'][1],
                                min_value = 0.00,
                                max_value = 0.99)
        
        G = st.number_input(label = '$\\bar{G}$', 
                            value = st.session_state['param_IS_2'][4])
        
    with IS_col2:
        a = st.number_input(label = '$a$', 
                            value = st.session_state['param_IS_2'][2])
        
        A = st.number_input(label = '$A$', 
                            value = st.session_state['param_IS_2'][3])
        
        T = st.number_input(label = '$T$', 
                            value = st.session_state['param_IS_2'][5])
        
with col2:
    # LM Inputs
    st.latex(r'''
    \frac{M}{P}=\bar{l} - l_{r}r + l_{Y}Y
    ''')
    LM_col1, LM_col2 = st.columns(2)
    with LM_col1:
        M = st.number_input(label = '$M$', 
                            value = 25.0 if (len(st.session_state['param_LM']) < 2) else st.session_state['param_LM_2'][0], 
                            disabled = False if (len(st.session_state['param_LM']) > 2) else True)
        
        P = st.number_input(label = '$P$', 
                            value = 5.0 if (len(st.session_state['param_LM']) < 2) else st.session_state['param_LM_2'][1], 
                            disabled = False if (len(st.session_state['param_LM']) > 2) else True)
        
        r = st.number_input(label = '$r$', 
                            value = 8.00 if (len(st.session_state['param_LM']) > 2) else st.session_state['param_LM_2'][0], 
                            disabled = True if (len(st.session_state['param_LM']) > 2) else False)
    with LM_col2:
        l_ = st.number_input(label = '$\\bar{l}$', 
                                value = 6.0 if (len(st.session_state['param_LM']) < 2) else st.session_state['param_LM_2'][2], 
                                disabled = False if (len(st.session_state['param_LM']) > 2) else True)
        
        l_r = st.number_input(label = '$l_r$', 
                                value = 0.5 if (len(st.session_state['param_LM']) < 2) else st.session_state['param_LM_2'][3], 
                                disabled = False if (len(st.session_state['param_LM']) > 2) else True)
        
        l_y = st.number_input(label = '$l_y$', 
                                value = 0.03 if (len(st.session_state['param_LM']) < 2) else st.session_state['param_LM_2'][4], 
                                disabled = False if (len(st.session_state['param_LM']) > 2) else True)

# Plot and Metrics  
st.title('Plots and Metrics')            
with st.container():
    
    graph_col, metrics = st.columns([3,1])
    with graph_col:
        
        button_col1, button_col2, button_col3 = st.columns(3)
        with button_col1:
            # Reset Parameters Button
            if central_bank == 'Money Supply':
                st.button(label = 'Reset Parameters', 
                            on_click = setting_the_parameters, 
                            args = [[[15.0, 0.8, 0.5, 15.0, 20.0, 20.0],[25.0, 5.0, 6.0, 0.5, 0.03],
                                    [15.0, 0.8, 0.5, 15.0, 20.0, 20.0],[25.0, 5.0, 6.0, 0.5, 0.03]]])
            else:
                st.button(label = 'Reset Parameters', 
                            on_click = setting_the_parameters, 
                            args = [[[15.0, 0.8, 0.5, 15.0, 20.0, 20.0],[8.00],
                                    [15.0, 0.8, 0.5, 15.0, 20.0, 20.0],[8.00]]])
        with button_col2:
            # Set Parameters Button
            if central_bank == 'Money Supply':
                st.button(label = 'Set Parameters', 
                            on_click = setting_the_parameters, 
                            args = [[[c_0, c_1, a, A, G, T],[M, P, l_, l_r, l_y],
                                    [c_0, c_1, a, A, G, T],[M, P, l_, l_r, l_y]]])
            else:
                st.button(label = 'Set Parameters', 
                            on_click = setting_the_parameters, 
                            args = [[[c_0, c_1, a, A, G, T],[r],
                                    [c_0, c_1, a, A, G, T],[r]]])
        with button_col3:
            # Plot Graph Button
            if central_bank == 'Money Supply':
                st.button(label = 'Plot Graph', 
                            on_click = new_parameters, 
                            args = [[[c_0, c_1, a, A, G, T],[M, P, l_, l_r, l_y]]])
            else:
                st.button(label = 'Plot Graph', 
                            on_click = new_parameters, 
                            args = [[[c_0, c_1, a, A, G, T],[r]]])
        
        st.plotly_chart(model.plot())
        
    with metrics:
        # Metrics     
        st.metric(label = 'Income', 
                    value = f'U$ {round(model.income_2, 2)}', 
                    delta = f'{round(model.income_2 - model.income_1, 2)}')
        
        st.metric(label = 'Rates', 
                    value = f'{round(model.rates_2, 2)}', 
                    delta = f'{round(model.rates_2 - model.rates_1, 2)}')
        
        st.metric(label = 'Consumption  \n $C = c_0 + c_1(Y - T)$', 
                    value = f'U$ {round(model.consumption_2, 2)}', 
                    delta = f'{round(model.consumption_2 - model.consumption_1, 2)}')
        
        st.metric(label = 'Investment  \n $I = A - ar$', 
                    value = f'U$ {round(model.investment_2, 2)}', 
                    delta = f'{round(model.investment_2 - model.investment_1, 2)}')
        