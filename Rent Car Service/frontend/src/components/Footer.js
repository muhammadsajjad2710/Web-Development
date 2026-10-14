import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  FaCar, 
  FaPhone, 
  FaEnvelope, 
  FaMapMarkerAlt, 
  FaFacebook, 
  FaInstagram, 
  FaWhatsapp,
  FaArrowRight,
  FaShieldAlt,
  FaClock,
  FaUsers,
  FaAward
} from 'react-icons/fa';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const quickLinks = [
    { name: 'Home', path: '/' },
    { name: 'Vehicles', path: '/vehicles' },
    { name: 'Services', path: '/services' },
    { name: 'About Us', path: '/about' },
    { name: 'Contact', path: '/contact' },
    { name: 'Terms & Conditions', path: '/terms' },
    { name: 'Privacy Policy', path: '/privacy' },
  ];

  const services = [
    'Local Car Rental',
    'Intercity Travel',
    'Airport Pickup',
    'Wedding Car Service',
    'Corporate Travel',
    'Tourism Packages',
    'Driver Service',
    'Long-term Rental'
  ];

  const pakistanCities = [
    'Islamabad',
    'Lahore', 
    'Karachi',
    'Peshawar',
    'Faisalabad',
    'Multan',
    'Sargodha',
    'Mianwali'
  ];

  const socialLinks = [
    { 
      name: 'Facebook', 
      icon: <FaFacebook className="w-5 h-5" />, 
      url: 'https://facebook.com/AwanRentACar',
      color: 'hover:bg-blue-600'
    },
    { 
      name: 'Instagram', 
      icon: <FaInstagram className="w-5 h-5" />, 
      url: 'https://instagram.com/AwanRentACar',
      color: 'hover:bg-pink-600'
    },
    { 
      name: 'WhatsApp', 
      icon: <FaWhatsapp className="w-5 h-5" />, 
      url: 'https://wa.me/923000000000',
      color: 'hover:bg-green-600'
    }
  ];

  const features = [
    { icon: <FaShieldAlt />, text: 'Fully Insured Vehicles' },
    { icon: <FaClock />, text: '24/7 Customer Support' },
    { icon: <FaUsers />, text: 'Professional Drivers' },
    { icon: <FaAward />, text: 'Quality Guaranteed' }
  ];

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer Content */}
      <div className="container-responsive py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="lg:col-span-1"
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-green-700 rounded-xl flex items-center justify-center shadow-lg">
                  <FaCar className="text-white text-xl" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h3 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-green-600 bg-clip-text text-transparent">
                  Awan Rent A Car
                </h3>
                <p className="text-sm text-gray-400 -mt-1">Pakistan's Trusted Car Rental</p>
              </div>
            </div>
            
            <p className="text-gray-300 mb-6 leading-relaxed">
              Providing premium car rental services across Pakistan with a focus on safety, 
              reliability, and customer satisfaction. Your trusted partner for local and intercity travel.
            </p>

            {/* Features */}
            <div className="space-y-3">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="flex items-center space-x-3 text-gray-300"
                >
                  <div className="w-5 h-5 text-green-400">{feature.icon}</div>
                  <span className="text-sm">{feature.text}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Quick Links */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1 }}
            viewport={{ once: true }}
          >
            <h4 className="text-lg font-semibold mb-6 text-white">Quick Links</h4>
            <ul className="space-y-3">
              {quickLinks.map((link, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.05 }}
                  viewport={{ once: true }}
                >
                  <Link
                    to={link.path}
                    className="footer-link inline-flex items-center group"
                  >
                    <FaArrowRight className="w-3 h-3 mr-2 group-hover:translate-x-1 transition-transform duration-300" />
                    {link.name}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          {/* Services */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <h4 className="text-lg font-semibold mb-6 text-white">Our Services</h4>
            <ul className="space-y-3">
              {services.map((service, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.05 }}
                  viewport={{ once: true }}
                  className="text-gray-300 hover:text-white transition-colors duration-300 cursor-pointer"
                >
                  • {service}
                </motion.li>
              ))}
            </ul>
          </motion.div>

          {/* Contact & Cities */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            viewport={{ once: true }}
          >
            <h4 className="text-lg font-semibold mb-6 text-white">Contact Info</h4>
            
            {/* Contact Details */}
            <div className="space-y-4 mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                  <FaPhone className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Phone</p>
                  <p className="text-white">+92-300-0000000</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                  <FaEnvelope className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Email</p>
                  <p className="text-white">info@awanrentacar.com</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                  <FaMapMarkerAlt className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Address</p>
                  <p className="text-white">Islamabad, Pakistan</p>
                </div>
              </div>
            </div>

            {/* Cities Covered */}
            <div>
              <h5 className="text-sm font-semibold mb-3 text-gray-300">Cities We Cover</h5>
              <div className="flex flex-wrap gap-2">
                {pakistanCities.map((city, index) => (
                  <motion.span
                    key={index}
                    initial={{ opacity: 0, scale: 0.8 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: index * 0.05 }}
                    viewport={{ once: true }}
                    className="px-3 py-1 bg-gray-800 text-gray-300 rounded-full text-xs hover:bg-green-600 hover:text-white transition-all duration-300 cursor-pointer"
                  >
                    {city}
                  </motion.span>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Social Media & Newsletter */}
      <div className="border-t border-gray-800 py-8">
        <div className="container-responsive">
          <div className="flex flex-col lg:flex-row items-center justify-between space-y-6 lg:space-y-0">
            {/* Social Media */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="flex items-center space-x-4"
            >
              <span className="text-gray-400">Follow us:</span>
              {socialLinks.map((social, index) => (
                <motion.a
                  key={index}
                  href={social.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`social-icon ${social.color}`}
                  initial={{ opacity: 0, scale: 0 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  {social.icon}
                </motion.a>
              ))}
            </motion.div>

            {/* Newsletter */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
              className="flex items-center space-x-4"
            >
              <span className="text-gray-400">Get updates:</span>
              <div className="flex">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-l-lg focus:ring-2 focus:ring-green-500 focus:border-transparent text-white placeholder-gray-400"
                />
                <button className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded-r-lg transition-colors duration-300">
                  Subscribe
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800 py-6">
        <div className="container-responsive">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-gray-400 text-sm"
            >
              © {currentYear} Awan Rent A Car. All rights reserved. | 
              Serving Pakistan with Pride 🇵🇰
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
              className="flex items-center space-x-6 text-sm text-gray-400"
            >
              <span className="flex items-center space-x-2">
                <FaShieldAlt className="w-4 h-4 text-green-400" />
                <span>SSL Secured</span>
              </span>
              <span className="flex items-center space-x-2">
                <FaAward className="w-4 h-4 text-yellow-400" />
                <span>ISO Certified</span>
              </span>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Pakistan Flag Colors Accent */}
      <div className="h-1 bg-gradient-to-r from-green-600 via-white to-green-600"></div>
    </footer>
  );
};

export default Footer;
