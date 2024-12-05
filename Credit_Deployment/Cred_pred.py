# import pickle
# import pandas as pd
# from flask import Flask

# # Create Flask app
# app = Flask(__name__)

# # Load the saved model
# model = pickle.load(open('/workspaces/Credit_Score_Analysis/AutogluonModels/ag-20241205_062650/models/WeightedEnsemble_L2/model.pkl', 'rb'))

# # Define a route
# @app.route('/')
# def home():
#     return "Hello! Your Flask app is running."

# @app.route('/test-model')
# def test_model():
#     # Example test input as a list of values
#     sample_input = [[25,66000,514,0,106827,105,0,95.000000,38,1,7,7,1,13]]  
    
#     # Convert the list to a DataFrame
#     # Replace the columns with the actual feature names used during training
#     columns = ['Age', 'Income', 'Credit History Length', 'Number of Existing Loans',
#        'Loan Amount', 'Loan Tenure', 'Existing Customer', 'LTV Ratio',
#        'Profile Score', 'Gender', 'State', 'City', 'Employment Profile',
#        'Occupation']
#     sample_input_df = pd.DataFrame(sample_input, columns=columns)

#     # Predict using the loaded model
#     sample_output = model.predict(sample_input_df)
#     return f"Prediction: {sample_output.tolist()}"  # Convert output to a list for better readability

# if __name__ == "__main__":
#     app.run(debug=True)


import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify

# Create Flask app
app = Flask(__name__, template_folder='/workspaces/Credit_Score_Analysis/templates')

# Load the saved model
model_path = '/workspaces/Credit_Score_Analysis/AutogluonModels/ag-20241205_062650/models/WeightedEnsemble_L2/model.pkl'
model = pickle.load(open(model_path, 'rb'))

# Define columns used by the model
columns = ['Age', 'Income', 'Credit History Length', 'Number of Existing Loans',
           'Loan Amount', 'Loan Tenure', 'Existing Customer', 'LTV Ratio',
           'Profile Score', 'Gender', 'State', 'City', 'Employment Profile',
           'Occupation']

# Home route with input form
@app.route('/')
def home():
    return render_template('home.html')  

# Handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
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
            'Gender': form_data['Gender'],  # Categorical (raw string)
            'State': form_data['State'],    # Categorical (raw string)
            'City': int(form_data['City']),
            'Employment Profile': int(form_data['Employment Profile']),
            'Occupation': int(form_data['Occupation']),
}

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data], columns=columns)

        # Make prediction
        prediction = model.predict(input_df)

        # Render result page
        return render_template('result.html', prediction=prediction[0])

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
