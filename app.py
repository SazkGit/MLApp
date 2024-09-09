from flask import Flask, render_template, request
import pybamm
import numpy as np
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def simulate_and_get_solution(t_eval):
    model = pybamm.lithium_ion.DFN()
    sim = pybamm.Simulation(model)
    sim.solve(t_eval)
    return sim

def generate_plot(decimal):
    t_start = 0
    t_end = 3600
    t_eval = [t_start, t_end]
    sim = simulate_and_get_solution(t_eval)
    plt.close('all')
    plt.switch_backend('Agg')
   
    quick_plot = pybamm.QuickPlot(sim)
    fig = quick_plot.plot(decimal)  


    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
      
    img_buffer.seek(0)
    
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')

    return img_str


@app.route('/')
def index():
    model = pybamm.lithium_ion.DFN()
    sim = pybamm.Simulation(model)
    t_eval = [0, 3600]
    sim.solve(t_eval)
    solution = sim.solution

    
    variable_names = model.variable_names()

    solution_dict = {}
    for var_name in variable_names:
        if(isinstance(solution[var_name].entries[-1],np.float64)) :
            solution_dict[var_name] = solution[var_name].entries[-1]

    return render_template('index.html', solution=solution_dict)

@app.route('/plot', methods=['GET'])
def plot_data():
    decimal = float(request.args.get('decimal', 0))
    img_data = generate_plot(decimal)
    return render_template('index2.html', plot_data=img_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port =5001)