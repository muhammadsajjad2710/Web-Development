import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  FaPhone, 
  FaEnvelope, 
  FaMapMarkerAlt, 
  FaClock, 
  FaFacebook, 
  FaInstagram, 
  FaWhatsapp,
  FaCar,
  FaUser,
  FaCalendarAlt,
  FaCheckCircle,
  FaStar,
  FaArrowRight
} from 'react-icons/fa';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      setIsSubmitting(false);
      setSubmitSuccess(true);
      setFormData({
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      });
      
      // Reset success message after 5 seconds
      setTimeout(() => setSubmitSuccess(false), 5000);
    }, 2000);
  };

  const contactInfo = [
    {
      icon: <FaPhone className="w-8 h-8" />,
      title: "Call Us",
      details: ["+92-300-0000000", "24/7 Available"],
      action: "tel:+923000000000",
      color: "from-blue-500 to-blue-600"
    },
    {
      icon: <FaEnvelope className="w-8 h-8" />,
      title: "Email Us",
      details: ["info@awanrentacar.com", "Quick Response"],
      action: "mailto:info@awanrentacar.com",
      color: "from-green-500 to-green-600"
    },
    {
      icon: <FaMapMarkerAlt className="w-8 h-8" />,
      title: "Visit Us",
      details: ["Islamabad, Pakistan", "Main Office"],
      action: "#",
      color: "from-purple-500 to-purple-600"
    }
  ];

  const businessHours = [
    { day: "Monday - Friday", hours: "8:00 AM - 8:00 PM" },
    { day: "Saturday", hours: "9:00 AM - 6:00 PM" },
    { day: "Sunday", hours: "10:00 AM - 4:00 PM" },
    { day: "Emergency", hours: "24/7 Available" }
  ];

  const pakistanCities = [
    { name: "Islamabad", status: "Headquarters", phone: "+92-300-0000000" },
    { name: "Lahore", status: "Branch Office", phone: "+92-300-0000001" },
    { name: "Karachi", status: "Branch Office", phone: "+92-300-0000002" },
    { name: "Peshawar", status: "Branch Office", phone: "+92-300-0000003" }
  ];

  const socialLinks = [
    {
      name: "Facebook",
      icon: <FaFacebook className="w-6 h-6" />,
      url: "https://facebook.com/AwanRentACar",
      color: "hover:bg-blue-600"
    },
    {
      name: "Instagram",
      icon: <FaInstagram className="w-6 h-6" />,
      url: "https://instagram.com/AwanRentACar",
      color: "hover:bg-pink-600"
    },
    {
      name: "WhatsApp",
      icon: <FaWhatsapp className="w-6 h-6" />,
      url: "https://wa.me/923000000000",
      color: "hover:bg-green-600"
    }
  ];

  const quickActions = [
    {
      title: "Book a Vehicle",
      description: "Reserve your preferred vehicle online",
      icon: <FaCar className="w-8 h-8" />,
      action: "/vehicles",
      color: "from-green-500 to-green-600"
    },
    {
      title: "Get a Quote",
      description: "Request pricing for your travel needs",
      icon: <FaUser className="w-8 h-8" />,
      action: "/contact",
      color: "from-blue-500 to-blue-600"
    },
    {
      title: "Check Availability",
      description: "See real-time vehicle availability",
      icon: <FaCalendarAlt className="w-8 h-8" />,
      action: "/vehicles",
      color: "from-purple-500 to-purple-600"
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
            <h1 className="text-5xl font-bold mb-6">Contact Us</h1>
            <p className="text-xl text-green-100 max-w-3xl mx-auto">
              Get in touch with us for all your car rental needs. We're here to help you plan 
              your journey across Pakistan with reliable and comfortable transportation solutions.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Contact Info Cards */}
      <section className="section-padding">
        <div className="container-responsive">
          <div className="grid-responsive">
            {contactInfo.map((info, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-2xl shadow-lg p-8 text-center hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className={`w-20 h-20 bg-gradient-to-br ${info.color} rounded-2xl flex items-center justify-center text-white mx-auto mb-6`}>
                  {info.icon}
                </div>
                <h3 className="text-2xl font-semibold mb-4">{info.title}</h3>
                <div className="space-y-2 mb-6">
                  {info.details.map((detail, idx) => (
                    <p key={idx} className="text-gray-600">{detail}</p>
                  ))}
                </div>
                <a
                  href={info.action}
                  className={`inline-flex items-center px-6 py-3 bg-gradient-to-r ${info.color} text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105`}
                >
                  {info.title} <FaArrowRight className="ml-2" />
                </a>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold mb-6">Send us a Message</h2>
              <p className="text-gray-600 mb-8">
                Have questions about our services or need assistance with your booking? 
                Fill out the form below and we'll get back to you within 24 hours.
              </p>

              {submitSuccess && (
                <motion.div
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="message-success mb-6"
                >
                  <div className="flex items-center">
                    <FaCheckCircle className="w-5 h-5 mr-2" />
                    <span>Thank you! Your message has been sent successfully. We'll get back to you soon.</span>
                  </div>
                </motion.div>
              )}

              <form onSubmit={handleSubmit} className="contact-form">
                <div className="form-group">
                  <label htmlFor="name" className="form-label">Full Name *</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="form-input"
                    placeholder="Enter your full name"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email" className="form-label">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="form-input"
                    placeholder="Enter your email address"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="phone" className="form-label">Phone Number</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    className="form-input"
                    placeholder="Enter your phone number"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="subject" className="form-label">Subject *</label>
                  <select
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleInputChange}
                    required
                    className="form-input"
                  >
                    <option value="">Select a subject</option>
                    <option value="general">General Inquiry</option>
                    <option value="booking">Booking Information</option>
                    <option value="pricing">Pricing & Quotes</option>
                    <option value="support">Customer Support</option>
                    <option value="feedback">Feedback & Suggestions</option>
                    <option value="partnership">Business Partnership</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="message" className="form-label">Message *</label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleInputChange}
                    required
                    rows="5"
                    className="form-textarea"
                    placeholder="Tell us how we can help you..."
                  ></textarea>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn-primary w-full flex items-center justify-center"
                >
                  {isSubmitting ? (
                    <>
                      <div className="spinner w-5 h-5 mr-2"></div>
                      Sending Message...
                    </>
                  ) : (
                    <>
                      Send Message <FaArrowRight className="ml-2" />
                    </>
                  )}
                </button>
              </form>
            </motion.div>

            {/* Contact Details */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              {/* Business Hours */}
              <div className="bg-gray-50 rounded-2xl p-6">
                <div className="flex items-center mb-4">
                  <FaClock className="w-6 h-6 text-green-600 mr-3" />
                  <h3 className="text-xl font-semibold">Business Hours</h3>
                </div>
                <div className="space-y-3">
                  {businessHours.map((schedule, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="font-medium text-gray-700">{schedule.day}</span>
                      <span className="text-gray-600">{schedule.hours}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pakistan Cities */}
              <div className="bg-gray-50 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">Our Locations</h3>
                <div className="space-y-3">
                  {pakistanCities.map((city, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg">
                      <div>
                        <div className="font-medium text-gray-900">{city.name}</div>
                        <div className="text-sm text-gray-500">{city.status}</div>
                      </div>
                      <a
                        href={`tel:${city.phone}`}
                        className="text-green-600 hover:text-green-700 font-medium"
                      >
                        {city.phone}
                      </a>
                    </div>
                  ))}
                </div>
              </div>

              {/* Social Media */}
              <div className="bg-gray-50 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">Follow Us</h3>
                <div className="flex space-x-4">
                  {socialLinks.map((social, index) => (
                    <motion.a
                      key={index}
                      href={social.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`social-icon ${social.color}`}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      {social.icon}
                    </motion.a>
                  ))}
                </div>
                <p className="text-sm text-gray-600 mt-4">
                  Stay updated with our latest offers and news
                </p>
              </div>

              {/* Quick Actions */}
              <div className="bg-gray-50 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  {quickActions.map((action, index) => (
                    <motion.a
                      key={index}
                      href={action.action}
                      className={`block p-4 bg-gradient-to-r ${action.color} text-white rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105`}
                      whileHover={{ y: -2 }}
                    >
                      <div className="flex items-center">
                        <div className="mr-4">{action.icon}</div>
                        <div>
                          <div className="font-semibold">{action.title}</div>
                          <div className="text-sm opacity-90">{action.description}</div>
                        </div>
                      </div>
                    </motion.a>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="section-padding bg-gray-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">What Our Customers Say</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Don't just take our word for it - hear from our satisfied customers across Pakistan
            </p>
          </motion.div>

          <div className="grid-responsive">
            {[
              {
                name: "Ahmed Khan",
                city: "Lahore",
                rating: 5,
                comment: "Excellent customer service! The team was very responsive and helped me find the perfect vehicle for my family trip.",
                avatar: "AK"
              },
              {
                name: "Fatima Ali",
                city: "Islamabad",
                rating: 5,
                comment: "Professional service from start to finish. The booking process was smooth and the vehicle was in perfect condition.",
                avatar: "FA"
              },
              {
                name: "Usman Hassan",
                city: "Karachi",
                rating: 5,
                comment: "Great experience with intercity travel. The staff was helpful and the journey was comfortable and safe.",
                avatar: "UH"
              }
            ].map((testimonial, index) => (
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
                    <p className="text-sm text-gray-500">{testimonial.city}</p>
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
              Contact us today to discuss your car rental needs and get a personalized quote for your journey across Pakistan
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="tel:+923000000000"
                className="btn-secondary text-lg px-8 py-4"
              >
                Call Us Now
              </a>
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
    </div>
  );
};

export default Contact;
