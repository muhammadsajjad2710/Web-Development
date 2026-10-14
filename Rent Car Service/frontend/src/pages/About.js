import React from 'react';
import { motion } from 'framer-motion';
import { 
  FaCar, 
  FaShieldAlt, 
  FaUsers, 
  FaMapMarkerAlt, 
  FaPhone, 
  FaWhatsapp,
  FaGlobe,
  FaHandshake,
  FaHeart,
  FaRocket,
  FaAward
} from 'react-icons/fa';

const About = () => {
  const stats = [
    { number: "500+", label: "Happy Customers", icon: <FaUsers className="w-8 h-8" /> },
    { number: "50+", label: "Vehicle Fleet", icon: <FaCar className="w-8 h-8" /> },
    { number: "7", label: "Cities Covered", icon: <FaMapMarkerAlt className="w-8 h-8" /> },
    { number: "24/7", label: "Support Available", icon: <FaPhone className="w-8 h-8" /> }
  ];

  const values = [
    {
      icon: <FaShieldAlt className="w-12 h-12" />,
      title: "Safety First",
      description: "We prioritize the safety of our customers with well-maintained vehicles and comprehensive insurance coverage."
    },
    {
      icon: <FaHandshake className="w-12 h-12" />,
      title: "Trust & Reliability",
      description: "Building long-term relationships with our customers through consistent, reliable service delivery."
    },
    {
      icon: <FaHeart className="w-12 h-12" />,
      title: "Customer Focus",
      description: "Every decision we make is centered around providing the best possible experience for our customers."
    },
    {
      icon: <FaRocket className="w-12 h-12" />,
      title: "Innovation",
      description: "Continuously improving our services and embracing new technologies to serve our customers better."
    }
  ];

  const team = [
    {
      name: "Ahmed Awan",
      position: "Founder & CEO",
      experience: "15+ years in automotive industry",
      expertise: "Business Strategy, Customer Relations",
      avatar: "AA"
    },
    {
      name: "Fatima Awan",
      position: "Operations Manager",
      experience: "12+ years in operations",
      expertise: "Fleet Management, Quality Control",
      avatar: "FA"
    },
    {
      name: "Usman Awan",
      position: "Head of Customer Service",
      experience: "10+ years in customer service",
      expertise: "Customer Support, Problem Resolution",
      avatar: "UA"
    }
  ];

  const milestones = [
    {
      year: "2010",
      title: "Company Founded",
      description: "Started with 5 vehicles in Islamabad, serving local customers with quality car rental service."
    },
    {
      year: "2015",
      title: "Expansion to Major Cities",
      description: "Extended services to Lahore, Karachi, and Peshawar, becoming a regional player."
    },
    {
      year: "2018",
      title: "Fleet Expansion",
      description: "Grew fleet to 30+ vehicles including luxury cars and SUVs for premium customers."
    },
    {
      year: "2020",
      title: "Digital Transformation",
      description: "Launched online booking platform and mobile app for better customer experience."
    },
    {
      year: "2023",
      title: "Market Leader",
      description: "Became the leading car rental service in Islamabad with 50+ vehicles and 500+ happy customers."
    }
  ];

  const pakistanPresence = [
    {
      city: "Islamabad",
      status: "Headquarters",
      services: ["Local Rental", "Intercity Travel", "Corporate"],
      description: "Capital city operations with full fleet availability"
    },
    {
      city: "Lahore",
      status: "Major Hub",
      services: ["Intercity Travel", "Local Rental"],
      description: "Serving Punjab's largest city and surrounding areas"
    },
    {
      city: "Karachi",
      status: "Coastal Hub",
      services: ["Intercity Travel", "Airport Service"],
      description: "Connecting Pakistan's economic capital"
    },
    {
      city: "Peshawar",
      status: "Frontier Hub",
      services: ["Intercity Travel", "Tourism"],
      description: "Gateway to Khyber Pakhtunkhwa province"
    }
  ];

  const certifications = [
    "ISO 9001:2015 Quality Management",
    "Pakistan Tourism Development Corporation Approved",
    "Federal Board of Revenue Registered",
    "Insurance Regulatory Authority Compliant",
    "Environmental Protection Agency Certified"
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
            <h1 className="text-5xl font-bold mb-6">About Awan Rent A Car</h1>
            <p className="text-xl text-green-100 max-w-3xl mx-auto">
              Pakistan's trusted car rental service, connecting people and places across the country 
              with reliability, safety, and exceptional customer service since 2010.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Company Story */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold mb-6">Our Story</h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                Founded in 2010 by the Awan family in Islamabad, Awan Rent A Car began with a simple mission: 
                to provide reliable, affordable, and safe car rental services to the people of Pakistan.
              </p>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                What started as a small fleet of 5 vehicles has grown into one of Islamabad's most trusted 
                car rental services, serving customers across Pakistan with our commitment to quality and 
                customer satisfaction.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                Today, we're proud to serve customers from all walks of life - from business travelers and 
                tourists to families and individuals seeking reliable transportation solutions.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="bg-gradient-to-br from-green-500 to-green-700 rounded-2xl p-8 text-white">
                <div className="text-center">
                  <FaCar className="w-16 h-16 mx-auto mb-6 text-green-200" />
                  <h3 className="text-2xl font-bold mb-4">Serving Pakistan Since 2010</h3>
                  <p className="text-green-100 mb-6">
                    Over a decade of excellence in car rental services across Pakistan
                  </p>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold">13+</div>
                      <div className="text-sm text-green-200">Years of Service</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold">500+</div>
                      <div className="text-sm text-green-200">Happy Customers</div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="section-padding bg-gray-50">
        <div className="container-responsive">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center text-blue-600 mb-6">
                <FaGlobe className="w-8 h-8" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Our Mission</h3>
              <p className="text-gray-600 leading-relaxed">
                To provide accessible, reliable, and safe car rental services that connect people across Pakistan, 
                contributing to the country's transportation infrastructure and economic development while maintaining 
                the highest standards of customer service and vehicle quality.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mb-6">
                <FaRocket className="w-8 h-8" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Our Vision</h3>
              <p className="text-gray-600 leading-relaxed">
                To become Pakistan's leading car rental service provider, known for innovation, reliability, 
                and exceptional customer experience, while expanding our reach to serve every major city 
                and contributing to the country's tourism and business development.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="section-padding bg-gradient-primary text-white">
        <div className="container-responsive">
          <div className="grid-responsive">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  {stat.icon}
                </div>
                <div className="text-4xl md:text-5xl font-bold mb-2">{stat.number}</div>
                <div className="text-lg opacity-90">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Our Core Values</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The principles that guide our business and shape our relationship with customers
            </p>
          </motion.div>

          <div className="grid-responsive">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-50 rounded-2xl p-8 text-center hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className="w-20 h-20 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mx-auto mb-6">
                  {value.icon}
                </div>
                <h3 className="text-xl font-semibold mb-4">{value.title}</h3>
                <p className="text-gray-600">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pakistan Presence */}
      <section className="section-padding bg-gray-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Our Presence Across Pakistan</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Serving major cities across Pakistan with reliable car rental services
            </p>
          </motion.div>

          <div className="grid-responsive">
            {pakistanPresence.map((city, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-semibold mb-2">{city.city}</h3>
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                    {city.status}
                  </span>
                </div>
                
                <div className="mb-4">
                  <h4 className="font-semibold mb-3 text-gray-900">Services:</h4>
                  <div className="flex flex-wrap gap-2">
                    {city.services.map((service, idx) => (
                      <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                        {service}
                      </span>
                    ))}
                  </div>
                </div>
                
                <p className="text-gray-600 text-sm">{city.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Dedicated professionals committed to providing the best car rental experience in Pakistan
            </p>
          </motion.div>

          <div className="grid-responsive">
            {team.map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-50 rounded-2xl p-8 text-center hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
              >
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center text-green-600 mx-auto mb-6 text-2xl font-bold">
                  {member.avatar}
                </div>
                <h3 className="text-xl font-semibold mb-2">{member.name}</h3>
                <p className="text-green-600 font-medium mb-3">{member.position}</p>
                <p className="text-gray-600 text-sm mb-3">{member.experience}</p>
                <p className="text-gray-600 text-sm">{member.expertise}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Milestones */}
      <section className="section-padding bg-gray-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Our Journey</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Key milestones in our growth and development over the years
            </p>
          </motion.div>

          <div className="space-y-8">
            {milestones.map((milestone, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className={`flex flex-col ${index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-8`}
              >
                <div className="lg:w-1/3 text-center">
                  <div className="w-24 h-24 bg-gradient-to-br from-green-500 to-green-700 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto">
                    {milestone.year}
                  </div>
                </div>
                <div className="lg:w-2/3 text-center lg:text-left">
                  <h3 className="text-2xl font-semibold mb-3">{milestone.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{milestone.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Certifications */}
      <section className="section-padding bg-white">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Certifications & Compliance</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We maintain the highest standards of quality and compliance in all our operations
            </p>
          </motion.div>

          <div className="grid-responsive">
            {certifications.map((cert, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-50 rounded-2xl p-6 text-center hover:shadow-lg transition-all duration-300"
              >
                <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center text-green-600 mx-auto mb-4">
                  <FaAward className="w-8 h-8" />
                </div>
                <p className="text-gray-700 font-medium">{cert}</p>
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
            <h2 className="text-4xl font-bold mb-6">Ready to Experience Our Service?</h2>
            <p className="text-xl text-green-100 mb-8 max-w-3xl mx-auto">
              Join thousands of satisfied customers who trust Awan Rent A Car for their transportation needs
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

export default About;
