import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { 
  FaCar, 
  FaShieldAlt, 
  FaClock, 
  FaMapMarkerAlt, 
  FaStar, 
  FaPhone, 
  FaArrowRight,
  FaEnvelope
} from 'react-icons/fa';

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -50]);

  // Auto-advance hero slides
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % 3);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const heroSlides = [
    {
      title: "Premium Car Rental in Pakistan",
      subtitle: "Experience luxury and comfort with our premium fleet",
      image: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80",
      cta: "Explore Fleet"
    },
    {
      title: "Intercity Travel Made Easy",
      subtitle: "Connect major cities across Pakistan with comfort",
      image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80",
      cta: "Book Now"
    },
    {
      title: "24/7 Customer Support",
      subtitle: "We're here for you anytime, anywhere in Pakistan",
      image: "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80",
      cta: "Contact Us"
    }
  ];

  const features = [
    {
      icon: <FaShieldAlt className="w-8 h-8" />,
      title: "Fully Insured",
      description: "All vehicles come with comprehensive insurance coverage"
    },
    {
      icon: <FaClock className="w-8 h-8" />,
      title: "24/7 Service",
      description: "Round-the-clock support for all your rental needs"
    },
    {
      icon: <FaMapMarkerAlt className="w-8 h-8" />,
      title: "Nationwide Coverage",
      description: "Available in major cities across Pakistan"
    },
    {
      icon: <FaCar className="w-8 h-8" />,
      title: "Well-Maintained Fleet",
      description: "Regularly serviced vehicles for your safety"
    }
  ];

  const pakistanCities = [
    { name: "Lahore", distance: "280 km", time: "3.5 hours", image: "🏛️" },
    { name: "Karachi", distance: "1,200 km", time: "16 hours", image: "🌊" },
    { name: "Peshawar", distance: "180 km", time: "2.5 hours", image: "🏔️" },
    { name: "Faisalabad", distance: "320 km", time: "4 hours", image: "🏭" },
    { name: "Multan", distance: "400 km", time: "5 hours", image: "🕌" },
    { name: "Sargodha", distance: "200 km", time: "2.5 hours", image: "🍊" }
  ];

  const testimonials = [
    {
      name: "Ahmed Khan",
      city: "Lahore",
      rating: 5,
      comment: "Excellent service! The car was in perfect condition and the staff was very professional.",
      avatar: "AK"
    },
    {
      name: "Fatima Ali",
      city: "Islamabad",
      rating: 5,
      comment: "Best car rental service in Pakistan. Highly recommended for family trips.",
      avatar: "FA"
    },
    {
      name: "Usman Hassan",
      city: "Karachi",
      rating: 5,
      comment: "Great experience with intercity travel. The vehicle was comfortable and reliable.",
      avatar: "UH"
    }
  ];

  const stats = [
    { number: "500+", label: "Happy Customers" },
    { number: "50+", label: "Vehicle Fleet" },
    { number: "7", label: "Cities Covered" },
    { number: "24/7", label: "Support Available" }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen overflow-hidden">
        {/* Background Slides */}
        {heroSlides.map((slide, index) => (
          <motion.div
            key={index}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentSlide ? 'opacity-100' : 'opacity-0'
            }`}
            style={{ y: index === currentSlide ? y : 0 }}
          >
            <div 
              className="absolute inset-0 bg-cover bg-center bg-no-repeat"
              style={{ backgroundImage: `url(${slide.image})` }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-900/40 to-purple-900/40"></div>
            </div>
          </motion.div>
        ))}

        {/* Hero Content */}
        <div className="relative z-10 flex items-center justify-center h-full">
          <div className="text-center text-white px-4">
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-5xl md:text-7xl font-bold mb-6"
            >
              {heroSlides[currentSlide].title}
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl md:text-2xl mb-8 text-gray-200"
            >
              {heroSlides[currentSlide].subtitle}
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link
                to="/vehicles"
                className="btn-primary text-lg px-8 py-4 inline-flex items-center"
              >
                {heroSlides[currentSlide].cta}
                <FaArrowRight className="ml-2" />
              </Link>
              <Link
                to="/contact"
                className="btn-secondary text-lg px-8 py-4"
              >
                Get Quote
              </Link>
            </motion.div>
          </div>
        </div>

        {/* Slide Indicators */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-3">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`w-3 h-3 rounded-full transition-all duration-300 ${
                index === currentSlide ? 'bg-white scale-125' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="section-padding bg-gradient-to-br from-blue-50 to-indigo-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4 text-gradient-primary">Why Choose Awan Rent A Car?</h2>
            <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
              We provide the best car rental experience in Pakistan with premium vehicles, 
              professional service, and nationwide coverage.
            </p>
          </motion.div>

          <div className="grid-responsive">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card-hover p-8 text-center group bg-white/80 backdrop-blur-sm"
              >
                <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl flex items-center justify-center text-blue-600 mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-4 text-neutral-800">{feature.title}</h3>
                <p className="text-neutral-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pakistan Cities Section */}
      <section className="section-padding bg-gradient-to-br from-emerald-50 to-teal-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4 text-gradient-accent">Intercity Travel Routes</h2>
            <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
              Connect major cities across Pakistan with our reliable intercity car rental service
            </p>
          </motion.div>

          <div className="grid-responsive">
            {pakistanCities.map((city, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card-hover p-6 text-center bg-white/80 backdrop-blur-sm"
              >
                <div className="text-4xl mb-4">{city.image}</div>
                <h3 className="text-xl font-semibold mb-2 text-neutral-800">{city.name}</h3>
                <div className="space-y-2 text-neutral-600">
                  <p>Distance: {city.distance}</p>
                  <p>Travel Time: {city.time}</p>
                </div>
                <Link
                  to="/vehicles"
                  className="inline-flex items-center mt-4 text-emerald-600 hover:text-emerald-700 font-medium transition-colors duration-300"
                >
                  Book Vehicle <FaArrowRight className="ml-2 w-4 h-4" />
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section-padding bg-gradient-to-br from-blue-500 via-purple-500 to-indigo-600 text-white">
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
                <div className="text-4xl md:text-5xl font-bold mb-2">{stat.number}</div>
                <div className="text-lg opacity-90">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="section-padding bg-gradient-to-br from-amber-50 to-orange-50">
        <div className="container-responsive">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4 text-gradient-accent">What Our Customers Say</h2>
            <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
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
                className="card-hover p-6 bg-white/80 backdrop-blur-sm"
              >
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-amber-100 to-orange-100 rounded-full flex items-center justify-center text-amber-600 font-bold mr-4">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <h4 className="font-semibold text-neutral-800">{testimonial.name}</h4>
                    <p className="text-sm text-neutral-500">{testimonial.city}</p>
                  </div>
                </div>
                <div className="flex mb-3">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <FaStar key={i} className="text-amber-400 w-4 h-4" />
                  ))}
                </div>
                <p className="text-neutral-600 italic">"{testimonial.comment}"</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-gradient-to-br from-slate-800 via-purple-900 to-slate-900 text-white">
        <div className="container-responsive text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-6">Ready to Start Your Journey?</h2>
            <p className="text-xl text-slate-200 mb-8 max-w-3xl mx-auto">
              Join thousands of satisfied customers who trust Awan Rent A Car for your transportation needs across Pakistan
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/vehicles"
                className="btn-primary text-lg px-8 py-4 inline-flex items-center"
              >
                Browse Vehicles <FaArrowRight className="ml-2" />
              </Link>
              <Link
                to="/contact"
                className="btn-outline text-lg px-8 py-4 border-white text-white hover:bg-white hover:text-slate-900"
              >
                Contact Us
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Contact Info Section */}
      <section className="section-padding bg-gradient-to-br from-rose-50 to-pink-50">
        <div className="container-responsive">
          <div className="grid-responsive">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-2xl flex items-center justify-center text-blue-600 mx-auto mb-6">
                <FaPhone className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-neutral-800">Call Us</h3>
              <p className="text-neutral-600">+92-300-0000000</p>
              <p className="text-neutral-600">24/7 Available</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-2xl flex items-center justify-center text-emerald-600 mx-auto mb-6">
                <FaEnvelope className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-neutral-800">Email Us</h3>
              <p className="text-neutral-600">info@awanrentacar.com</p>
              <p className="text-neutral-600">Quick Response</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-gradient-to-br from-amber-100 to-orange-100 rounded-2xl flex items-center justify-center text-amber-600 mx-auto mb-6">
                <FaMapMarkerAlt className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-neutral-800">Visit Us</h3>
              <p className="text-neutral-600">Islamabad, Pakistan</p>
              <p className="text-neutral-600">Main Office</p>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
