import React from 'react';
import shapCorrect from '../assets/shap_correct.png';
import shap_wrong from '../assets/shap_wrong.png';

const Modal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-3xl w-full max-h-full overflow-auto">
        <div className="overflow-y-auto max-h-96">
          <h2 className="text-xl font-bold mb-4">Understanding Model Explanations</h2>
          
          <h3 className="text-lg font-semibold mb-2">LIME (Local Interpretable Model-agnostic Explanations)</h3>
          <p className="mb-4">
            LIME is an algorithm designed to explain the predictions of any machine learning model by approximating it locally with an interpretable model. It highlights the important features in the input data by perturbing the data and observing the model's response. In image analysis:
            <ul className="list-disc ml-6">
              <li>Red superpixels indicate areas that significantly contributed to the model's prediction.</li>
              <li>Blue superpixels indicate areas that were less important.</li>
            </ul>
          </p>
          
          <h3 className="text-lg font-semibold mb-2">SHAP (SHapley Additive exPlanations)</h3>
          <p className="mb-4">
            SHAP assigns each feature an importance value for a particular prediction, based on Shapley values from cooperative game theory. It provides a consistent and fair explanation of feature contributions. In image analysis:
            <ul className="list-disc ml-6">
              <li>Green areas represent pixels that had a positive impact on the prediction.</li>
              <li>Purple areas represent pixels that had a negative impact.</li>
              <li>The more intense the color, the stronger the influence of those pixels.</li>
            </ul>
            SHAP values typically range from -0.1 to 0.1, indicating the degree of influence each pixel has on the model's decision.
          </p>
          
          <h3 className="text-lg font-semibold mb-2">Counterfactual Explanations</h3>
          <p className="mb-4">
            Counterfactual explanations show how to change the input to achieve a different prediction. They identify the minimal changes needed to alter the prediction to a desired outcome. These explanations help users understand how close an input is to a decision boundary and what changes could flip the prediction.
          </p>
          
          <h3 className="text-lg font-semibold mb-2">Model Training Suggestions</h3>
          <p className="mb-4">
            In the context of model training:
            <ul className="list-disc ml-6">
              <li><strong>Fully Trained Model:</strong> A model that has been trained on the entire dataset until the performance metrics have stabilized.</li>
              <li><strong>Half-Trained Model:</strong> A model that has only been trained partially and may not have learned all the nuances of the data.</li>
            </ul>
          </p>
          
          <h3 className="text-lg font-semibold mb-2">Handling Misclassifications</h3>
          <p className="mb-4">
            If the model misclassifies an input, consider the following suggestions:
            <ul className="list-disc ml-6">
              <li><strong>Use a Larger Model:</strong> Increasing the complexity of the model may help it capture more intricate patterns in the data.</li>
              <li><strong>Redo Training Data Preprocessing:</strong> Ensure that the data is clean and properly preprocessed. This includes handling missing values, normalization, and augmentation.</li>
              <li><strong>Collect More Data:</strong> More training data can help the model generalize better.</li>
              <li><strong>Use Advanced Techniques:</strong> Techniques like transfer learning, ensemble methods, or hyperparameter tuning can enhance model performance.</li>
            </ul>
            These actions can help improve model accuracy and robustness, leading to better performance in real-world scenarios.
          </p>

          <h3 className="text-lg font-semibold mb-2">Example of Correct SHAP Values</h3>
          <div className="mb-4">
            <p className="mb-2">Below is an example of SHAP values for a correctly classified digit. The first image shows the SHAP values highlighted, and the second image shows the original digit without SHAP values.</p>
            <div className="mb-4">
              <img src={shapCorrect} alt="SHAP Highlighted" className="mb-2 w-3/5 h-auto" />
              <p className="text-sm">Figure 1: SHAP values highlighted. Green areas represent positive contributions to the prediction, while purple areas represent negative contributions.</p>
            </div>
            <div className="mb-4">
              <img src={shap_wrong} alt="Shap not highlighted. " className="mb-2 w-3/5 h-auto" />
              <p className="text-sm">Figure 2: Predicted class without SHAP values.</p>
            </div>
          </div>

          <h3 className="text-lg font-semibold mb-2">Reasons for Incorrect SHAP Values</h3>
          <p className="mb-4">
            When SHAP values do not clearly show for the correct class, it can be due to several factors: the model might be uncertain or not confident in its prediction, often indicating insufficient training data or an imbalanced dataset. If the model has not seen enough examples of the particular class during training, it may not learn the distinctive features well. Additionally, a too simple or overly complex model can lead to poor performance. Data preprocessing issues, high noise levels, or underfitting can also obscure important features. To address these, consider increasing and balancing the training data, enhancing model complexity, improving preprocessing steps, applying regularization techniques, using cross-validation, and calibrating the model to ensure accurate predictions and meaningful SHAP values.
          </p>
        </div>
        <button onClick={onClose} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700">
          Close
        </button>
      </div>
    </div>
  );
};

export default Modal;
