from flask import Flask, render_template, request, jsonify, redirect, url_for

import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route("/")
def home():
    result = ''
    return render_template("home.html", **locals())

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    Q1 = float(request.form['Q1'])
    Q2 = float(request.form['Q2'])
    Q3 = float(request.form['Q3'])
    Q4 = float(request.form['Q4'])
    Q5 = float(request.form['Q5'])
    Q6 = float(request.form['Q6'])
    Q7 = float(request.form['Q7'])
    Q8 = float(request.form['Q8'])
    Q9 = float(request.form['Q9'])
    Q10 = float(request.form['Q10'])
    Q11 = float(request.form['Q11'])

    result_dict = {
        0: 'Depressed',
        1: 'Not Depressed',
        2: 'Severely Depressed'
    }

    result_num = model.predict([[Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11]])[0]
    result = result_dict[result_num]
    return redirect(url_for('show_result', result=result))

@app.route('/result')
def show_result():
    result = request.args.get('result')
    return render_template('results.html', result=result)


@app.route('/appPredict', methods=['POST'])
def app_predict():
    req_data = request.get_json()
    
    print(req_data["responses"][0])
    # Extracting values from the JSON data
    Q1 = float(req_data["responses"][0])
    Q2 = float(req_data["responses"][1])
    Q3 = float(req_data["responses"][2])
    Q4 = float(req_data["responses"][3])
    Q5 = float(req_data["responses"][4])
    Q6 = float(req_data["responses"][5])
    Q7 = float(req_data["responses"][6])
    Q8 = float(req_data["responses"][7])
    Q9 = float(req_data["responses"][8])
    Q10 = float(req_data["responses"][9])
    Q11 = float(req_data["responses"][10])

    # Getting the prediction
    result_dict = {
        0: 'Depressed',
        1: 'Not Depressed',
        2: 'Severely Depressed'
    }
    result_num = model.predict([[Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11]])[0]
    result = result_dict[result_num]

    # Creating a response JSON object
    res_data = {
        'prediction': result
    }

    return jsonify(res_data)

if __name__ == "__main__":
    app.run(debug=True)