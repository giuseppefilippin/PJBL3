from flask import Blueprint, render_template, request
from models.IoT.actuators import Actuator

actuator = Blueprint('actuator', __name__, template_folder='views')

@actuator.route('/actuators')
def actuators():
    actuators = Actuator.get_actuators()
    return render_template('actuator.html', actuators=actuators)

@actuator.route('/add_actuator', methods=['POST'])
def add_actuator():
    name = request.form.get('name')
    brand = request.form.get('brand')
    model = request.form.get('model')
    topic = request.form.get('topic')
    unit = request.form.get('unit')
    is_active = True if request.form.get('is_active') == 'on' else False

    Actuator.save_actuator(name, brand, model, topic, unit, is_active)

    actuators = Actuator.get_actuators()
    return render_template('actuator.html', actuators=actuators)

@actuator.route('/update_actuator', methods=['POST'])
def update_sensor():
    id = request.form.get('id')
    name = request.form.get('name')
    brand = request.form.get('brand')
    model = request.form.get('model')
    topic = request.form.get('topic')
    unit = request.form.get('unit')
    is_active = True if request.form.get('is_active') == 'on' else False

    actuators = Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)
    return render_template('actuator.html', actuators=actuators)

@actuator.route('/del_actuator', methods=['GET'])
def del_actuator():
    id = request.args.get('id', None)
    actuators = Actuator.delete_actuator(id)
    
    return render_template('actuator.html', actuators=actuators)