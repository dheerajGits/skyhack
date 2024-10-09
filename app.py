from flask import Flask, request, jsonify
import pandas as pd
import pickle
import joblib  # For loading the model
import os


app = Flask(__name__)

# Load your pre-trained model
model_pipeline = joblib.load('dataset/model_pipeline.pkl')  
agent_data = pickle.load(open('dataset/agent_data.pkl', 'rb'))  # Load agent data
customer_data = joblib.load('dataset/customer_data.pkl')

# File path for HDF5
hdf5_file = 'dataset/customer_data.h5'

# Save it in chunks to avoid MemoryError
chunk_size = 1000  # Adjust the chunk size as needed

# Check if the file already exists
if not os.path.exists(hdf5_file):
    # If the file does not exist, create it and write the first chunk
    customer_data_chunk = customer_data[0:chunk_size]
    customer_data_chunk.to_hdf(hdf5_file, key='df', mode='w', format='table')
    
    start_index = chunk_size
else:
    start_index = 0

# Append remaining chunks to the existing HDF5 file
for i in range(start_index, len(customer_data), chunk_size):
    customer_data_chunk = customer_data[i:i + chunk_size]
    customer_data_chunk.to_hdf(hdf5_file, key='df', mode='a', format='table', append=True)


customer_data = pd.read_hdf('dataset/customer_data.h5', where='customer_id == customer_id_value')


agent_data["is_available"]= True 

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get JSON data from the request
    customer_id = data.get('customer_id')
    primary_call_reason = data.get('primary_call_reason')
    customer_specific_data= customer_data.loc[customer_data['customer_id'] == customer_id]
    customer_tone_score = 3 # intial value
    if(customer_specific_data):
        customer_tone_score= customer_specific_data.customer_tone_score
    # Extract current hour (example)
    from datetime import datetime
    hour = datetime.now().hour

    least_handle_time_agent = None
    least_handle_time = float('inf')

    # Loop through agent_data to check availability
    for agent, details in agent_data.items():
        if details['is_available']:  # Check if the agent is available
            # Prepare input for the agent
            agent_input = pd.DataFrame({
                'agent_tone_score': [details['tone']],
                'customer_tone_score': [customer_tone_score],  # Add any required customer tone data
                'avg_call_sentiment_score_of_agent': [details['sentiment_score']],
                'silence_average_by_call_reason': [details['silence_percentage']],
                'primary_call_reason': [primary_call_reason],
                'hour': [hour]
            })

            # Predict handle time for the available agent
            agent_handle_time = model_pipeline.predict(agent_input)[0]

            # Check if this agent has the least handle time
            if agent_handle_time < least_handle_time:
                least_handle_time = agent_handle_time
                least_handle_time_agent = agent

    if least_handle_time_agent is None:
        return jsonify({'error': 'No available agents.'}), 404
    agent_data.loc[agent_data['agent_id_x'] == least_handle_time_agent, 'is_available'] = False # to change the status to false
    return jsonify({
        'transferred_to_agent': least_handle_time_agent,
        'least_handle_time': least_handle_time
    })

@app.route('/call_complete', methods=['POST'])
def call_complete():
    data = request.json  # Get JSON data from the request
    agent_id = data.get('agent_id')
    
    # Update the agent's availability
    if agent_id in agent_data['agent_id_x'].values:  # Check if agent exists
        agent_data.loc[agent_data['agent_id_x'] == agent_id, 'is_available'] = True
        return jsonify({'message': 'Agent status updated to available.'}), 200
    else:
        return jsonify({'error': 'Agent not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
