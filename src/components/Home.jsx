import { Link } from 'react-router-dom'
import ramImage from '../assets/ram.png';
import calculatorImage from '../assets/calculator.png'
import puzzlePieceImage from '../assets/puzzle-piece.png'
import speakImage from '../assets/speak.png'
export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="w-full text-center mb-8">
        <h1 className="text-4xl font-bold">[Zerthimous]</h1>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 p-4 transform translate-y-[10vh]">
        <Link to="/memory-recall" className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl">
          <img src={ramImage} className="h-full mr-4"/>
          Memory & Recall
        </Link>
        <Link to="/quantitative-reasoning" className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-red-400 to-orange-400 rounded-xl">
          <img src={calculatorImage} className="h-full mr-4"/>
          Quantitative Reasoning
        </Link>
        <Link to="/visuo-spatial-manipulation" className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-green-400 to-teal-500 rounded-xl">
          <img src={puzzlePieceImage} className="h-full mr-4"/>
          Visuo-Spatial Manipulation
        </Link>
        <Link to="/verbal-reasoning" className="p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl">
          <img src={speakImage} className="h-full mr-4"/>
          Verbal Reasoning
        </Link>
      </div>
    </div>
  )
}
