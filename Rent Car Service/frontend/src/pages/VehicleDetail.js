import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaCar, FaMapMarkerAlt, FaCalendarAlt, FaGasPump, FaCog, FaCheck, FaStar } from 'react-icons/fa';
import axios from 'axios';

const VehicleDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchVehicle();
  }, [id]);

  const fetchVehicle = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/vehicles/${id}/`);
      setVehicle(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching vehicle:', error);
      setError('Vehicle not found');
      setLoading(false);
    }
  };

  const handleBookNow = () => {
    navigate(`/booking/${id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading vehicle details...</p>
        </div>
      </div>
    );
  }

  if (error || !vehicle) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <FaCar className="text-6xl text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Vehicle not found</h3>
          <p className="text-gray-600 mb-4">{error || 'The vehicle you are looking for does not exist.'}</p>
          <button
            onClick={() => navigate('/vehicles')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Vehicles
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex mb-8" aria-label="Breadcrumb">
          <ol className="inline-flex items-center space-x-1 md:space-x-3">
            <li className="inline-flex items-center">
              <button
                onClick={() => navigate('/vehicles')}
                className="inline-flex items-center text-sm font-medium text-gray-700 hover:text-blue-600"
              >
                Vehicles
              </button>
            </li>
            <li>
              <div className="flex items-center">
                <span className="mx-2 text-gray-400">/</span>
                <span className="text-sm font-medium text-gray-500">{vehicle.brand} {vehicle.name}</span>
              </div>
            </li>
          </ol>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Vehicle Image */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-4"
          >
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              {vehicle.image ? (
                <img
                  src={vehicle.image}
                  alt={vehicle.name}
                  className="w-full h-96 object-cover"
                />
              ) : (
                <div className="w-full h-96 bg-gray-200 flex items-center justify-center">
                  <FaCar className="text-8xl text-gray-400" />
                </div>
              )}
            </div>
          </motion.div>

          {/* Vehicle Details */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-6"
          >
            {/* Header */}
            <div>
              <div className="flex items-center space-x-2 mb-2">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  {vehicle.category_name}
                </span>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  Available
                </span>
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                {vehicle.brand} {vehicle.name}
              </h1>
              <p className="text-lg text-gray-600">
                {vehicle.year} • {vehicle.fuel_type} • {vehicle.transmission}
              </p>
            </div>

            {/* Key Features */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Features</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center space-x-3">
                  <FaGasPump className="text-blue-600" />
                  <span className="text-gray-700">{vehicle.fuel_type}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <FaCog className="text-blue-600" />
                  <span className="text-gray-700">{vehicle.transmission}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <FaMapMarkerAlt className="text-blue-600" />
                  <span className="text-gray-700">{vehicle.city_name || 'All Cities'}</span>
                </div>
                <div className="flex items-center space-x-3">
                  <FaCalendarAlt className="text-blue-600" />
                  <span className="text-gray-700">{vehicle.year}</span>
                </div>
              </div>
            </div>

            {/* Features List */}
            {vehicle.features && vehicle.features.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Features</h3>
                <div className="grid grid-cols-2 gap-3">
                  {vehicle.features.map((feature, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <FaCheck className="text-green-500 text-sm" />
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Pricing */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Pricing</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Local Rate (per day)</span>
                  <span className="text-xl font-bold text-blue-600">Rs. {vehicle.local_rate_per_day}</span>
                </div>
                {vehicle.intercity_rate_per_day && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Intercity Rate (per day)</span>
                    <span className="text-xl font-bold text-blue-600">Rs. {vehicle.intercity_rate_per_day}</span>
                  </div>
                )}
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Security Deposit</span>
                  <span className="text-lg font-semibold text-gray-900">Rs. {vehicle.security_deposit || 'Contact us'}</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                onClick={handleBookNow}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                Book This Vehicle
              </button>
              <button
                onClick={() => navigate('/vehicles')}
                className="w-full bg-gray-200 text-gray-800 py-3 px-6 rounded-lg text-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                View Other Vehicles
              </button>
            </div>
          </motion.div>
        </div>

        {/* Additional Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-12 bg-white rounded-lg shadow-sm p-6"
        >
          <h3 className="text-xl font-semibold text-gray-900 mb-4">About This Vehicle</h3>
          <p className="text-gray-600 leading-relaxed">
            {vehicle.description || `Experience the perfect blend of comfort, style, and performance with our ${vehicle.brand} ${vehicle.name}. 
            This ${vehicle.year} model comes equipped with modern features and is maintained to the highest standards to ensure your safety and satisfaction. 
            Whether you need it for local travel or intercity journeys, this vehicle is ready to serve your transportation needs.`}
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default VehicleDetail;
