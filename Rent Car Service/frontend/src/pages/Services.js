import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  FaCar, 
  FaRoute, 
  FaPlane, 
  FaHeart, 
  FaBuilding, 
  FaGlobe, 
  FaUserTie, 
  FaShieldAlt,
  FaClock,
  FaMapMarkerAlt,
  FaPhone,
  FaWhatsapp,
  FaCheckCircle,
  FaStar,
  FaArrowRight
} from 'react-icons/fa';

const Services = () => {
  const services = [
    {
      icon: <FaCar className="w-12 h-12" />,
      title: "Local Car Rental",
      description: "Daily and weekly car rentals in Islamabad for business, shopping, and local travel needs.",
      features: [
        "Flexible rental periods",
        "Multiple pickup locations",
        "24/7 customer support",
        "No hidden charges"
      ],
      price: "Starting from Rs. 2,500/day",
      color: "from-blue-500 to-blue-600",
      bgColor: "bg-blue-50",
      iconColor: "text-blue-600"
    },
    {
      icon: <FaRoute className="w-12 h-12" />,
      title: "Intercity Travel",
      description: "Reliable intercity car rental service connecting major cities across Pakistan.",
      features: [
        "Islamabad to all major cities",
        "Professional drivers available",
        "Comfortable long-distance travel",
        "Fixed pricing structure"
      ],
      price: "Starting from Rs. 3,000/day",
      color: "from-green-500 to-green-600",
      bgColor: "bg-green-50",
      iconColor: "text-green-600"
    },
    {
      icon: <FaPlane className="w-12 h-12" />,
      title: "Airport Pickup & Drop",
      description: "Convenient airport transfer service to and from Islamabad International Airport.",
      features: [
        "Flight tracking service",
        "Meet & greet service",
        "Luggage assistance",
        "Fixed airport rates"
      ],
      price: "Starting from Rs. 1,500",
      color: "from-purple-500 to-purple-600",
      bgColor: "bg-purple-50",
      iconColor: "text-purple-600"
    },
    {
      icon: <FaHeart className="w-12 h-12" />,
      title: "Wedding Car Service",
      description: "Luxury vehicles for your special day with professional chauffeur service.",
      features: [
        "Luxury vehicle fleet",
        "Professional drivers",
        "Decoration included",
        "Flexible timing"
      ],
      price: "Starting from Rs. 15,000",
      color: "from-pink-500 to-pink-600",
      bgColor: "bg-pink-50",
      iconColor: "text-pink-600"
    },
    {
      icon: <FaBuilding className="w-12 h-12" />,
      title: "Corporate Travel",
      description: "Business car rental solutions for corporate clients and business travelers.",
      features: [
        "Corporate accounts",
        "Monthly billing",
        "Priority booking",
        "Dedicated support"
      ],
      price: "Corporate rates available",
      color: "from-indigo-500 to-indigo-600",
      bgColor: "bg-indigo-50",
      iconColor: "text-indigo-600"
    },
    {
      icon: <FaGlobe className="w-12 h-12" />,
      title: "Tourism Packages",
      description: "Complete travel packages for tourists visiting Pakistan's beautiful destinations.",
      features: [
        "Guided tours available",
        "Hotel bookings",
        "Multi-day packages",
        "Local expertise"
      ],
      price: "Custom packages",
      color: "from-orange-500 to-orange-600",
      bgColor: "bg-orange-50",
      iconColor: "text-orange-600"
    }
  ];

  const pakistanRoutes = [
    {
      from: "Islamabad",
      to: "Lahore",
      distance: "280 km",
      time: "3.5 hours",
      price: "Rs. 3,500",
      highlights: ["Historical sites", "Food capital", "Shopping"]
    },
    {
      from: "Islamabad",
      to: "Karachi",
      distance: "1,200 km",
      time: "16 hours",
      price: "Rs. 12,000",
      highlights: ["Beach city", "Business hub", "Port city"]
    },
    {
      from: "Islamabad",
      to: "Peshawar",
      distance: "180 km",
      time: "2.5 hours",
      price: "Rs. 2,800",
      highlights: ["Frontier city", "Historical", "Cultural"]
    },
    {
      from: "Islamabad",
      to: "Faisalabad",
      distance: "320 km",
      time: "4 hours",
      price: "Rs. 4,000",
      highlights: ["Industrial city", "Textile hub", "Modern"]
    }
  ];

  const whyChooseUs = [
    {
      icon: <FaShieldAlt className="w-8 h-8" />,
      title: "Fully Insured",
      description: "All vehicles come with comprehensive insurance coverage for your peace of mind."
    },
    {
      icon: <FaClock className="w-8 h-8" />,
      title: "24/7 Support",
      description: "Round-the-clock customer support available for all your rental needs."
    },
    {
      icon: <FaUserTie className="w-8 h-8" />,
      title: "Professional Service",
      description: "Experienced staff and professional drivers ensure a smooth experience."
    },
    {
      icon: <FaCheckCircle className="w-8 h-8" />,
      title: "Quality Guaranteed",
      description: "Well-maintained vehicles and regular service checks for reliability."
    }
  ];

  const testimonials = [
    {
      name: "Ahmed Khan",
      company: "Business Owner, Lahore",
      rating: 5,
      comment: "Excellent corporate travel service. Reliable vehicles and professional drivers.",
      avatar: "AK"
    },
    {
      name: "Fatima Ali",
      company: "Tourist, Karachi",
      rating: 5,
      comment: "Amazing experience with intercity travel. Comfortable journey and great service.",
      avatar: "FA"
    },
    {
      name: "Usman Hassan",
      company: "Wedding Client, Islamabad",
      rating: 5,
      comment: "Perfect wedding car service. Beautiful vehicle and professional chauffeur.",
      avatar: "UH"
    }
  ];

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
            <h1 className="text-5xl font-bold mb-6">Our Services</h1>
            <p className="text-xl text-green-100 max-w-3xl mx-auto">
              Comprehensive car rental solutions tailored for Pakistan's diverse transportation needs. 
              From local rentals to intercity travel, we've got you covered.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="section-padding">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">What We Offer</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Choose from our wide range of services designed to meet all your transportation needs across Pakistan
            </p>
          </motion.div>

          <div className="grid-responsive">
            {services.map((service, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className={`${service.bgColor} rounded-2xl p-8 hover:shadow-xl transition-all duration-500 hover:-translate-y-2`}
              >
                <div className={`w-20 h-20 bg-gradient-to-br ${service.color} rounded-2xl flex items-center justify-center text-white mb-6 mx-auto`}>
                  {service.icon}
                </div>
                
                <h3 className="text-2xl font-semibold mb-4 text-gray-900">{service.title}</h3>
                <p className="text-gray-600 mb-6 leading-relaxed">{service.description}</p>
                
                <div className="space-y-3 mb-6">
                  {service.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center space-x-3">
                      <FaCheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>
                
                <div className="text-center">
                  <div className="text-lg font-semibold text-gray-900 mb-4">{service.price}</div>
                  <Link
                    to="/contact"
                    className={`inline-flex items-center px-6 py-3 bg-gradient-to-r ${service.color} text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105`}
                  >
                    Get Quote <FaArrowRight className="ml-2" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Intercity Routes */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Popular Intercity Routes</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Connect major cities across Pakistan with our reliable intercity car rental service
            </p>
          </motion.div>

          <div className="grid-responsive">
            {pakistanRoutes.map((route, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all duration-300"
              >
                <div className="text-center mb-6">
                  <h3 className="text-xl font-semibold mb-2">
                    {route.from} → {route.to}
                  </h3>
                  <div className="w-16 h-1 bg-green-500 mx-auto"></div>
                </div>
                
                <div className="space-y-4 mb-6">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Distance:</span>
                    <span className="font-semibold">{route.distance}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Travel Time:</span>
                    <span className="font-semibold">{route.time}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Price:</span>
                    <span className="font-semibold text-green-600">{route.price}</span>
                  </div>
                </div>
                
                <div className="mb-6">
                  <h4 className="font-semibold mb-3 text-gray-900">Highlights:</h4>
                  <div className="flex flex-wrap gap-2">
                    {route.highlights.map((highlight, idx) => (
                      <span key={idx} className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                        {highlight}
                      </span>
                    ))}
                  </div>
                </div>
                
                <Link
                  to="/vehicles"
                  className="w-full btn-primary text-center"
                >
                  Book Vehicle
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="section-padding bg-gray-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Why Choose Awan Rent A Car?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We're committed to providing the best car rental experience in Pakistan
            </p>
          </motion.div>

          <div className="grid-responsive">
            {whyChooseUs.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-2xl p-8 text-center hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mx-auto mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-4">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">What Our Clients Say</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Don't just take our word for it - hear from our satisfied customers across Pakistan
            </p>
          </motion.div>

          <div className="grid-responsive">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="testimonial-card"
              >
                <div className="flex items-center mb-4">
                  <div className="testimonial-avatar mr-4">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <h4 className="font-semibold">{testimonial.name}</h4>
                    <p className="text-sm text-gray-500">{testimonial.company}</p>
                  </div>
                </div>
                <div className="flex mb-3">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <FaStar key={i} className="text-yellow-400 w-4 h-4" />
                  ))}
                </div>
                <p className="text-gray-600 italic">"{testimonial.comment}"</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-gradient-primary text-white">
        <div className="container-responsive text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-green-100 mb-8 max-w-3xl mx-auto">
              Contact us today to discuss your car rental needs and get a personalized quote for your journey
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/contact"
                className="btn-secondary text-lg px-8 py-4"
              >
                Contact Us
              </Link>
              <a
                href="https://wa.me/923000000000"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-green-500 hover:bg-green-600 text-white font-semibold py-4 px-8 rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg inline-flex items-center"
              >
                <FaWhatsapp className="mr-2" />
                WhatsApp Us
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Contact Info */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <div className="grid-responsive">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mx-auto mb-6">
                <FaPhone className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Call Us</h3>
              <p className="text-gray-600">+92-300-0000000</p>
              <p className="text-gray-600">24/7 Available</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mx-auto mb-6">
                <FaMapMarkerAlt className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Visit Us</h3>
              <p className="text-gray-600">Islamabad, Pakistan</p>
              <p className="text-gray-600">Main Office</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mx-auto mb-6">
                <FaWhatsapp className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2">WhatsApp</h3>
              <p className="text-gray-600">+92-300-0000000</p>
              <p className="text-gray-600">Quick Response</p>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;
