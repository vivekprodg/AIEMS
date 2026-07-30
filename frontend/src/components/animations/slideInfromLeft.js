"use client";

import { motion } from "framer-motion";

const SlideInFromLeft = ({ children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -80 }} // Start off-screen (left)
      animate={{ opacity: 1, x: 0 }} // Slide in to original position
      exit={{ opacity: 0, x: -80 }} // Exit animation
      transition={{ duration: 0.6, ease: "easeOut" }} // Smooth transition
    >
      {children}
    </motion.div>
  );
};

export default SlideInFromLeft;