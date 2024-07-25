import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png'; 

const LandingPage = () => {
  const navigate = useNavigate();

  const navigateToMain = () => {
    navigate('/main'); 
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="flex flex-col items-center">
        <img src={logo} alt="Logo" className="w-1/2 " /> 
        <h1 className="text-6xl font-bold text-gray-800 mb-2">Image Insights</h1>
        <p className="text-2xl text-gray-700 mb-4 text-center max-w-2xl">
          Discover the power of visual explanations for image classification models.
          Our tool helps you understand and interpret model predictions through intuitive visualizations.
        </p>
        <button onClick={navigateToMain} className="px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-700 transition duration-300">
          Get Started
        </button>
      </div>
    </div>
  );
};

export default LandingPage;
