from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd

app = Flask(__name__)

# Load the model when the app starts
model = xgb.Booster()
model.load_model("xgboost_v0.json")

# Define the feature names expected by the model
FEATURE_NAMES = [
    'score_diff', 'total_unseen_tiles',
    'leave_A', 'leave_B', 'leave_C', 'leave_D', 'leave_E', 'leave_F',
    'leave_G', 'leave_H', 'leave_I', 'leave_J', 'leave_K', 'leave_L',
    'leave_M', 'leave_N', 'leave_O', 'leave_P', 'leave_Q', 'leave_R',
    'leave_S', 'leave_T', 'leave_U', 'leave_V', 'leave_W', 'leave_X',
    'leave_Y', 'leave_Z', 'leave_?', 'unseen_A', 'unseen_B', 'unseen_C',
    'unseen_D', 'unseen_E', 'unseen_F', 'unseen_G', 'unseen_H',
    'unseen_I', 'unseen_J', 'unseen_K', 'unseen_L', 'unseen_M',
    'unseen_N', 'unseen_O', 'unseen_P', 'unseen_Q', 'unseen_R',
    'unseen_S', 'unseen_T', 'unseen_U', 'unseen_V', 'unseen_W',
    'unseen_X', 'unseen_Y', 'unseen_Z', 'unseen_?'
]

@app.route("/", methods=["POST"])
def predict():
    # Parse the incoming JSON request
    data = request.json
    features = data.get("features")
    
    if not features:
        return jsonify({"error": "No features provided"}), 400
    
    # Validate the feature vector length
    if len(features) != len(FEATURE_NAMES):
        return jsonify({"error": f"Expected {len(FEATURE_NAMES)} features, but got {len(features)}"}), 400
    
    # Create a DataFrame for prediction
    try:
        features_df = pd.DataFrame([features], columns=FEATURE_NAMES)
        dmatrix = xgb.DMatrix(features_df)
        prediction = model.predict(dmatrix)
        return jsonify({"score": float(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/batch", methods=["POST"])
def batch_predict():
    # Parse the incoming JSON request
    data = request.json
    batch_features = data.get("batch_features")

    if not batch_features:
        return jsonify({"error": "No batch features provided"}), 400

    if not isinstance(batch_features, list):
        return jsonify({"error": "Batch features should be a list of feature vectors"}), 400

    # Validate feature vectors
    invalid_indices = [
        idx for idx, features in enumerate(batch_features)
        if len(features) != len(FEATURE_NAMES)
    ]

    if invalid_indices:
        return jsonify({
            "error": f"Invalid feature vector lengths at indices: {invalid_indices}. Expected {len(FEATURE_NAMES)} features."
        }), 400

    try:
        # Create a DataFrame for batch prediction
        features_df = pd.DataFrame(batch_features, columns=FEATURE_NAMES)
        dmatrix = xgb.DMatrix(features_df)
        predictions = model.predict(dmatrix)

        # Return predictions as a list
        return jsonify({"scores": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

