import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder='/workspaces/Credit_Score_Analysis/templates')


model_path = '/workspaces/Credit_Score_Analysis/model PKL/model.pkl'
model = pickle.load(open(model_path, 'rb'))


columns = ['Age', 'Income', 'Credit History Length', 'Number of Existing Loans',
           'Loan Amount', 'Loan Tenure', 'Existing Customer', 'LTV Ratio',
           'Profile Score', 'Gender', 'State', 'City', 'Employment Profile',
           'Occupation']


@app.route('/')
def home():
    return render_template('home.html')  


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Extract input from form
            form_data = request.form
            input_data = {
                'Age': int(form_data['Age']),
                'Income': float(form_data['Income']),
                'Credit History Length': int(form_data['Credit History Length']),
                'Number of Existing Loans': int(form_data['Number of Existing Loans']),
                'Loan Amount': float(form_data['Loan Amount']),
                'Loan Tenure': int(form_data['Loan Tenure']),
                'Existing Customer': int(form_data['Existing Customer']),
                'LTV Ratio': float(form_data['LTV Ratio']),
                'Profile Score': int(form_data['Profile Score']),
                'Gender': form_data['Gender'], 
                'State': form_data['State'], 
                'City': form_data['City'],
                'Employment Profile': int(form_data['Employment Profile']),
                'Occupation': int(form_data['Occupation']),
            }

            # Convert to DataFrame
            input_df = pd.DataFrame([input_data], columns=columns)

            # Make prediction
            prediction = model.predict(input_df)

            # Render the result page
            return render_template('result.html', prediction=prediction[0])

        except Exception as e:
            return jsonify({'error': f"An error occurred: {str(e)}"}), 400

    # Render the input form if GET request
    return render_template('form.html')  # Prediction form (template should be created)

# Error handling route for invalid endpoints
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
