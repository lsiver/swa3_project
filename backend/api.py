from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import config
from chem.DA.bindist import BinDist, kcalculation
from chem.DA import kcalc
from chem.DC.antoine_data_scraper import build_antoine_list, build_antoine_list_oneshot
from tasks import scrape_antoine_data, celery
import os

app = Flask(__name__)
allowed_origins = [
    'http://localhost:3000',
    'https://swa3-project-1.onrender.com'
]
CORS(app, origins=['*'])

def convert_numpy_to_python(obj):
    if hasattr(obj, 'item'):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

@app.route('/api/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json

        component_a = data.get('component_a', 'Toluene')
        component_b = data.get('component_b', 'Benzene')
        feed_composition = data.get('feed_composition', 0.8)
        distillate_purity = data.get('distillate_purity', 0.95)
        bottoms_purity = data.get('bottoms_purity', 0.05)
        pressure = data.get('pressure', 1)
        reflux_ratio = data.get('reflux_ratio', 2.0)

        tower = BinDist(component_a, component_b, feed_composition,
                        distillate_purity, bottoms_purity, 1.0, reflux_ratio,pressure)

        tower.Nmin_calc()
        tower.binary_distillation_calc()

        # clean up stage data
        clean_stages = []
        for stage in tower.stages:
            x, y, section = stage
            clean_stages.append([
                convert_numpy_to_python(x),
                convert_numpy_to_python(y),
                section
            ])

        plot_data = tower.get_plotting_data()

        return jsonify({
            'success': True,
            'results': {
                'Nmin': convert_numpy_to_python(tower.Nmin),
                'Rmin': convert_numpy_to_python(tower.Rmin),
                'stages': clean_stages,
                'stage_count': tower.stage_count,
                'alpha_1_2': convert_numpy_to_python(tower.alpha_1_2),
                'plot_data': plot_data
            },
            'parameters': data
        })

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/rescrapeAntoine', methods=['POST'])
def rescrapeAntoine():
    try:
        task = scrape_antoine_data.delay()
        return jsonify({
            'success':True,
            'message':'Antoine scraping started',
            'task_id':task.id
        })
    except Exception as e:
        return jsonify({'success':False, 'error':str(e)}), 400
    #     old way of doing it without a message queue. might need this again.
    #     data = request.json
    #     flag = data.get('flag',0)
    #     build_antoine_list_oneshot()
    #     return jsonify({'success':True, 'message':'Antoine constants scraped from NIST'})
    #
    # except Exception as e:
    #     print(f"Error: {e}")
    #     import traceback
    #     traceback.print_exc()
    #     return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/task-status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': 'PENDING', 'status':'Processing request'}
    elif task.state == 'SUCCESS':
        response = {'state': 'SUCCESS', 'result':task.result}
    else:
        response = {'state':'FAILURE','error':str(task.info)}
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port,debug=False)
    #app.run(debug=True, port=5000)