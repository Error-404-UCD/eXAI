import React from 'react';

const Modal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full max-h-full overflow-auto">
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
          </p>
          <h3 className="text-lg font-semibold mb-2">Counterfactual Explanations</h3>
          <p className="mb-4">
            Counterfactual explanations show how to change the input to achieve a different prediction. They identify the minimal changes needed to alter the prediction to a desired outcome. These explanations help users understand how close an input is to a decision boundary and what changes could flip the prediction.
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
