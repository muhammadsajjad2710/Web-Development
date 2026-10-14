import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaSearch, FaFilter, FaCar, FaMapMarkerAlt, FaCalendarAlt, FaStar, FaEye, FaHeart } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Vehicles = () => {
  const [vehicles, setVehicles] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedFuelType, setSelectedFuelType] = useState('');
  const [selectedTransmission, setSelectedTransmission] = useState('');
  const [priceRange, setPriceRange] = useState([0, 50000]);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [sortBy, setSortBy] = useState('name'); // 'name', 'price', 'year'

  useEffect(() => {
    fetchVehicles();
    fetchCategories();
  }, []);

  const fetchVehicles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/vehicles/');
      setVehicles(response.data.results || response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching vehicles:', error);
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/vehicles/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const filteredVehicles = vehicles
    .filter(vehicle => {
      const matchesSearch = vehicle.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           vehicle.brand.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = !selectedCategory || vehicle.category === selectedCategory;
      const matchesFuel = !selectedFuelType || vehicle.fuel_type === selectedFuelType;
      const matchesTransmission = !selectedTransmission || vehicle.transmission === selectedTransmission;
      const matchesPrice = vehicle.daily_rate >= priceRange[0] && vehicle.daily_rate <= priceRange[1];
      
      return matchesSearch && matchesCategory && matchesFuel && matchesTransmission && matchesPrice;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'price':
          return a.daily_rate - b.daily_rate;
        case 'year':
          return b.model_year - a.model_year;
        default:
          return a.name.localeCompare(b.name);
      }
    });

  const fuelTypes = ['petrol', 'diesel', 'hybrid', 'electric'];
  const transmissionTypes = ['manual', 'automatic'];

  const clearFilters = () => {
    setSearchTerm('');
    setSelectedCategory('');
    setSelectedFuelType('');
    setSelectedTransmission('');
    setPriceRange([0, 50000]);
    setSortBy('name');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available':
        return 'bg-green-100 text-green-800';
      case 'booked':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="spinner w-32 h-32 mx-auto"></div>
          <p className="mt-4 text-gray-600 text-lg">Loading vehicles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-green-600 to-green-800 text-white py-20">
        <div className="container-responsive text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl font-bold mb-6">Our Vehicle Fleet</h1>
            <p className="text-xl text-green-100 max-w-3xl mx-auto">
              Choose from our wide selection of well-maintained vehicles for your local and intercity travel needs across Pakistan
            </p>
          </motion.div>
        </div>
      </section>

      {/* Filters and Search */}
      <section className="py-8 bg-white shadow-sm">
        <div className="container-responsive">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            {/* Search Bar */}
            <div className="mb-6">
              <div className="search-container">
                <FaSearch className="search-icon" />
                <input
                  type="text"
                  placeholder="Search vehicles by name or brand..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="search-input"
                />
              </div>
            </div>

            {/* Filters Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
              {/* Category Filter */}
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="input-field"
              >
                <option value="">All Categories</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>

              {/* Fuel Type Filter */}
              <select
                value={selectedFuelType}
                onChange={(e) => setSelectedFuelType(e.target.value)}
                className="input-field"
              >
                <option value="">All Fuel Types</option>
                {fuelTypes.map((type) => (
                  <option key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>

              {/* Transmission Filter */}
              <select
                value={selectedTransmission}
                onChange={(e) => setSelectedTransmission(e.target.value)}
                className="input-field"
              >
                <option value="">All Transmissions</option>
                {transmissionTypes.map((type) => (
                  <option key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>

              {/* Sort By */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="input-field"
              >
                <option value="name">Sort by Name</option>
                <option value="price">Sort by Price</option>
                <option value="year">Sort by Year</option>
              </select>

              {/* View Mode */}
              <div className="flex border border-gray-300 rounded-lg overflow-hidden">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-4 py-3 transition-colors ${
                    viewMode === 'grid' 
                      ? 'bg-green-600 text-white' 
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <FaCar className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-4 py-3 transition-colors ${
                    viewMode === 'list' 
                      ? 'bg-green-600 text-white' 
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <FaFilter className="w-4 h-4" />
                </button>
              </div>

              {/* Clear Filters */}
              <button
                onClick={clearFilters}
                className="btn-outline"
              >
                Clear Filters
              </button>
            </div>

            {/* Price Range */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Price Range: Rs. {priceRange[0].toLocaleString()} - Rs. {priceRange[1].toLocaleString()}
              </label>
              <div className="flex items-center space-x-4">
                <input
                  type="range"
                  min="0"
                  max="50000"
                  value={priceRange[0]}
                  onChange={(e) => setPriceRange([parseInt(e.target.value), priceRange[1]])}
                  className="flex-1"
                />
                <input
                  type="range"
                  min="0"
                  max="50000"
                  value={priceRange[1]}
                  onChange={(e) => setPriceRange([priceRange[0], parseInt(e.target.value)])}
                  className="flex-1"
                />
              </div>
            </div>

            {/* Results Count */}
            <div className="flex items-center justify-between">
              <p className="text-gray-600">
                Showing {filteredVehicles.length} of {vehicles.length} vehicles
              </p>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-500">Active filters:</span>
                {selectedCategory && (
                  <span className="filter-tag active">
                    {categories.find(c => c.id === selectedCategory)?.name}
                  </span>
                )}
                {selectedFuelType && (
                  <span className="filter-tag active">
                    {selectedFuelType.charAt(0).toUpperCase() + selectedFuelType.slice(1)}
                  </span>
                )}
                {selectedTransmission && (
                  <span className="filter-tag active">
                    {selectedTransmission.charAt(0).toUpperCase() + selectedTransmission.slice(1)}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Vehicle Grid/List */}
      <section className="py-12">
        <div className="container-responsive">
          <AnimatePresence mode="wait">
            {filteredVehicles.length === 0 ? (
              <motion.div
                key="no-results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="text-center py-16"
              >
                <FaCar className="text-8xl text-gray-300 mx-auto mb-6" />
                <h3 className="text-2xl font-semibold text-gray-900 mb-4">No vehicles found</h3>
                <p className="text-gray-600 mb-6 max-w-md mx-auto">
                  Try adjusting your search criteria or filters to find the perfect vehicle for your needs.
                </p>
                <button
                  onClick={clearFilters}
                  className="btn-primary"
                >
                  Clear All Filters
                </button>
              </motion.div>
            ) : (
              <motion.div
                key="vehicle-grid"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className={viewMode === 'grid' ? 'grid-responsive' : 'space-y-6'}
              >
                {filteredVehicles.map((vehicle, index) => (
                  <motion.div
                    key={vehicle.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: index * 0.1 }}
                    className={viewMode === 'grid' ? 'vehicle-card' : 'bg-white rounded-2xl shadow-lg overflow-hidden'}
                  >
                    {viewMode === 'grid' ? (
                      /* Grid View */
                      <div className="group">
                        {/* Vehicle Image */}
                        <div className="relative overflow-hidden">
                          {vehicle.image ? (
                            <img
                              src={vehicle.image}
                              alt={vehicle.name}
                              className="vehicle-image"
                            />
                          ) : (
                            <div className="w-full h-48 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                              <FaCar className="text-6xl text-gray-400" />
                            </div>
                          )}
                          
                          {/* Overlay Actions */}
                          <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center space-x-4">
                            <Link
                              to={`/vehicles/${vehicle.id}`}
                              className="w-12 h-12 bg-white rounded-full flex items-center justify-center text-gray-800 hover:bg-green-600 hover:text-white transition-all duration-300"
                            >
                              <FaEye className="w-5 h-5" />
                            </Link>
                            <button className="w-12 h-12 bg-white rounded-full flex items-center justify-center text-gray-800 hover:bg-red-600 hover:text-white transition-all duration-300">
                              <FaHeart className="w-5 h-5" />
                            </button>
                          </div>

                          {/* Status Badge */}
                          <div className="absolute top-4 left-4">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(vehicle.is_available ? 'available' : 'booked')}`}>
                              {vehicle.is_available ? 'Available' : 'Booked'}
                            </span>
                          </div>

                          {/* Category Badge */}
                          <div className="absolute top-4 right-4">
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              {vehicle.category_name}
                            </span>
                          </div>
                        </div>

                        {/* Vehicle Info */}
                        <div className="p-6">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="text-xl font-semibold text-gray-900 group-hover:text-green-600 transition-colors">
                              {vehicle.brand} {vehicle.name}
                            </h3>
                            <div className="flex items-center space-x-1">
                              <FaStar className="w-4 h-4 text-yellow-400" />
                              <span className="text-sm text-gray-600">4.8</span>
                            </div>
                          </div>

                          <div className="space-y-3 mb-4">
                            <div className="flex items-center text-sm text-gray-600">
                              <FaCalendarAlt className="mr-2 text-gray-400" />
                              <span>{vehicle.model_year}</span>
                            </div>
                            <div className="flex items-center text-sm text-gray-600">
                              <FaMapMarkerAlt className="mr-2 text-gray-400" />
                              <span>Available in {vehicle.city_name || 'All Cities'}</span>
                            </div>
                            <div className="flex items-center justify-between text-sm">
                              <span className="text-gray-600">{vehicle.fuel_type} • {vehicle.transmission}</span>
                              <span className="text-gray-600">{vehicle.seats} Seats</span>
                            </div>
                          </div>

                          {/* Features */}
                          {vehicle.features && vehicle.features.length > 0 && (
                            <div className="mb-4">
                              <div className="flex flex-wrap gap-2">
                                {vehicle.features.slice(0, 3).map((feature, idx) => (
                                  <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                                    {feature}
                                  </span>
                                ))}
                                {vehicle.features.length > 3 && (
                                  <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                                    +{vehicle.features.length - 3} more
                                  </span>
                                )}
                              </div>
                            </div>
                          )}

                          {/* Price and Action */}
                          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                            <div>
                              <div className="price-display">
                                Rs. {vehicle.daily_rate.toLocaleString()}
                              </div>
                              <div className="price-unit">/day</div>
                            </div>
                            <Link
                              to={`/vehicles/${vehicle.id}`}
                              className="btn-primary"
                            >
                              View Details
                            </Link>
                          </div>
                        </div>
                      </div>
                    ) : (
                      /* List View */
                      <div className="flex flex-col lg:flex-row">
                        <div className="lg:w-1/3">
                          {vehicle.image ? (
                            <img
                              src={vehicle.image}
                              alt={vehicle.name}
                              className="w-full h-48 lg:h-full object-cover"
                            />
                          ) : (
                            <div className="w-full h-48 lg:h-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
                              <FaCar className="text-6xl text-gray-400" />
                            </div>
                          )}
                        </div>
                        
                        <div className="lg:w-2/3 p-6">
                          <div className="flex items-start justify-between mb-4">
                            <div>
                              <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                                {vehicle.brand} {vehicle.name}
                              </h3>
                              <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                                <span>{vehicle.model_year}</span>
                                <span>•</span>
                                <span>{vehicle.fuel_type}</span>
                                <span>•</span>
                                <span>{vehicle.transmission}</span>
                                <span>•</span>
                                <span>{vehicle.seats} Seats</span>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="price-display">
                                Rs. {vehicle.daily_rate.toLocaleString()}
                              </div>
                              <div className="price-unit">/day</div>
                            </div>
                          </div>

                          <p className="text-gray-600 mb-4">
                            {vehicle.description || `Experience the perfect blend of comfort, style, and performance with our ${vehicle.brand} ${vehicle.name}.`}
                          </p>

                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(vehicle.is_available ? 'available' : 'booked')}`}>
                                {vehicle.is_available ? 'Available' : 'Booked'}
                              </span>
                              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                                {vehicle.category_name}
                              </span>
                            </div>
                            <Link
                              to={`/vehicles/${vehicle.id}`}
                              className="btn-primary"
                            >
                              View Details
                            </Link>
                          </div>
                        </div>
                      </div>
                    )}
                  </motion.div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </section>
    </div>
  );
};

export default Vehicles;
