"use client";

import { motion } from "framer-motion";

export default function FadeIn({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }} // Start position
      animate={{ opacity: 1, y: 0 }} // End position
      exit={{ opacity: 0, y: -50 }} // Exit animation
      transition={{ duration: 0.5, ease: "easeInOut" }} // Animation timing
    >
      {children}
    </motion.div>
  );
}