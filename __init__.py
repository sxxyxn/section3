from flask import Flask, render_template, request
import pickle


def create_app():
  app = Flask(__name__)
  model = pickle.load(open('model.pkl', 'rb'))

  @app.route('/')
  def index():
    return render_template('index.html')

  @app.route('/predict', methods=['POST'])
  def home():
      data1 = request.form['chk_info']
      data2 = request.form['time']

      pred = model.predict([[data1,data2]])
      return render_template('result.html', data=pred)
  return app
