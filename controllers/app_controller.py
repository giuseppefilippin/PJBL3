#app_controller.py
from flask import Flask, render_template, request
import flask_login
from flask_login import LoginManager, logout_user
from flask_mqtt import Mqtt
from models.db import db, instance
from controllers.sensors_controller import sensor
from controllers.actuators_controller import actuator
from controllers.users_controller import user
from controllers.login_controller import login
from models.Users.users import User

def create_app():
    app = Flask(__name__, 
                template_folder="./views/", 
                static_folder="./static/",
                root_path="./")
    
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    app.config['MQTT_BROKER_URL'] = 'broker.mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    topic_subscribe = "flask-web-app-send"
    messages = []

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_disconnect()
    def handle_disconnect(client, userdata, rc):
        print("Disconnected from broker")


    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        if(message.topic==topic_subscribe):
            messages.append(message.payload.decode())

    app.register_blueprint(sensor, url_prefix='/')
    app.register_blueprint(actuator, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(login, url_prefix='/')

    @app.route('/')
    def index():
        return render_template("login.html")

    @login_manager.user_loader  
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/home', methods=["GET", "POST"])
    @flask_login.login_required
    def home():
        temperature = None
        for message in reversed(messages):
            if "Temperature" in message:
                temperature = message
                break

        humidity = None
        for message in reversed(messages):
            if "Humidity" in message:
                humidity = message
                break
        
        distance = None
        for message in reversed(messages):
            if "Distance" in message:
                distance = message
                break
        return render_template("home.html", messages=messages, temperature=temperature, humidity=humidity, distance=distance)
    
    @app.route('/about_us')
    @flask_login.login_required
    def about_us():
        return render_template("about_us.html")
    
    @app.route('/comand', methods=['GET', 'POST'])
    def comand():
        if request.method == 'POST':
            mqtt_client.publish("flask-web-app-receive", str(request.form['command']))
            return render_template("comand.html")
        
        return render_template("comand.html")
            
    return app
