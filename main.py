# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import requests
import json


# -- Initialization section --
app = Flask(__name__)

# -- Routes section --
@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/quiz', methods=['POST'])
def quiz():
  villagers= []
  response = requests.get("http://acnhapi.com/v1/villagers/")
  data = response.json()
  with open("data.json", "w") as f:
    json.dump(data, f)
  birthday = request.form['bday']
  animal = request.form['animal']
  personality = request.form['personality']
  similarity=0
  image=""
  for key, value in data.items():
    if birthday.strip().lower() == value["birthday"].strip().lower():
      similarity= similarity +1
    if animal.strip().lower() == value["species"].strip().lower():
      similarity= similarity +1
    if personality.strip().lower() == value["personality"].strip().lower():
      similarity= similarity +1
    if similarity >= 3:
      villagers.append({"id":value["id"],'name': value["name"]["name-USen"], 'similarity': similarity})
      image=value["image_uri"]
  if villagers:
    villagers.sort(reverse=True, key=lambda e: e["similarity"])
    villager = villagers[0]["name"]
  else:
    villager = "No match found"
  return render_template('result.html', villager=villager, image=image)

    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)