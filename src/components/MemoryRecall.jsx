import { Link } from 'react-router-dom'
import { motion } from 'framer-motion';
import { useState } from "react";
const exercises = [
  {
    name: "Mind Burst"
  }
]
export default function MemoryRecall() {
  return (
    <div className="flex flex-col items-center justify-center h-fit">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
        <Link to="/mind-burst" className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl">
          Mind Burst
        </Link>
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl">
          Coming Soon...
        </div>
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl">
          Coming Soon...
        </div>
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl">
          Coming Soon...
        </div>
      </div>
    </div>
  );
}