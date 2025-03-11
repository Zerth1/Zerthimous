import { Link } from 'react-router-dom'
import ramImage from '../assets/ram.png';
import calculatorImage from '../assets/calculator.png'
import puzzlePieceImage from '../assets/puzzle-piece.png'
import speakImage from '../assets/speak.png'
export default function Home() {
  return (
    <div className="overflow-hidden">
      <div className="text-center mb-0 sm:mb-1 md:mb-2 lg:mb-3">
        <h1 className="text-5xl sm:text-5xl md:text-5xl lg:text-6xl font-bold whitespace-nowrap pt-24">[Zerthimous]</h1>
      </div>
      <div className="flex flex-col items-center max-h-dvh">
        <div className="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 p-4">
          <Link to="/memory-recall" className="sm:p-6 md:p-12 lg:p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl">
            <img src={ramImage} className="h-12 mr-4"/>
            Memory & Recall
          </Link>
          <Link to="/quantitative-reasoning" className="sm:p-6 md:p-12 lg:p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-red-400 to-orange-400 rounded-xl">
            <img src={calculatorImage} className="h-12 mr-4"/>
            Quantitative Reasoning
          </Link>
          <Link to="/visuo-spatial-manipulation" className="sm:p-6 md:p-12 lg:p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-green-400 to-teal-500 rounded-xl">
            <img src={puzzlePieceImage} className="h-12 mr-4"/>
            Visuo-Spatial Manipulation
          </Link>
          <Link to="/verbal-reasoning" className="sm:p-6 md:p-12 lg:p-25 flex items-center justify-center text-center text-3xl font-bold neon-effect bg-gradient-to-r from-purple-400 to-pink-400 rounded-xl">
            <img src={speakImage} className="h-12 mr-4"/>
            Verbal Reasoning
          </Link>
        </div>
      </div>
    </div>
  )
}
