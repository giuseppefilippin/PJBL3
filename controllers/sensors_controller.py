from flask import Blueprint, render_template, request
from models.IoT.sensors import Sensor

sensor = Blueprint('sensor', __name__, template_folder='views')

@sensor.route('/sensors')
def sensors():
    sensors = Sensor.get_sensors()
    return render_template('sensor.html', sensors=sensors)

@sensor.route('/add_sensor', methods=['POST'])
def add_sensor():
    name = request.form.get('name')
    brand = request.form.get('brand')
    model = request.form.get('model')
    topic = request.form.get('topic')
    unit = request.form.get('unit')    
    is_active = True if request.form.get('is_active') == 'on' else False

    Sensor.save_sensor(name, brand, model, topic, unit, is_active)

    sensors = Sensor.get_sensors()
    return render_template('sensor.html', sensors=sensors)

@sensor.route('edit_sensor')
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)

    return render_template('edit_sensor.html', sensor=sensor)

@sensor.route('/update_sensor', methods=['POST'])
def update_sensor():
    id = request.form.get('id')
    name = request.form.get('name')
    brand = request.form.get('brand')
    model = request.form.get('model')
    topic = request.form.get('topic')
    unit = request.form.get('unit')
    is_active = True if request.form.get('is_active') == 'on' else False

    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active)
    return render_template('sensor.html', sensors=sensors)

@sensor.route('/del_sensor', methods=['GET'])
def del_sensor():
    id = request.args.get('id', None)
    sensors = Sensor.delete_sensor(id)

    return render_template('sensor.html', sensors=sensors)
