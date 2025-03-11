import { Link } from 'react-router-dom'
import { motion } from 'framer-motion';
import { useState } from "react";
const exercises = [
  {

  }
]
export default function VerbalReasoning() {
  return (
    <div className="flex flex-col items-center justify-center dvh">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl">
          Coming Soon...
        </div>
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl">
          Coming Soon...
        </div>
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl">
          Coming Soon...
        </div>
        <div className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl">
          Coming Soon...
        </div>
      </div>
    </div>
  )
}