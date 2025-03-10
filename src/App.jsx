import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import './App.css'
import Home from './components/Home';
import MemoryRecall from './components/MemoryRecall';
import QuantitativeReasoning from './components/QuantitativeReasoning';
import VisuoSpatialManipulation from './components/VisuoSpatialManipulation'
import VerbalReasoning from './components/VerbalReasoning';

import MindBurst from './components/exercises/MemoryRecall/MindBurst'
const TRANSITION_SPRING = {
  type: "spring",
  stiffness: 300,
  damping: 65,
}
const pageTransitionVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -50 },
}
function PageTransition({ children }) {
  const location = useLocation()
  return (
    <motion.div
      key={location.pathname}
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageTransitionVariants}
      transition={TRANSITION_SPRING}
      className="min-h-screen w-full"
    >
      {children}
    </motion.div>
  )
}
function App() {
  const location = useLocation()
  return (
    <>
      <AnimatePresence mode='wait'>
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<PageTransition><Home/></PageTransition>}/>
          <Route path="/memory-recall" element={<PageTransition><MemoryRecall/></PageTransition>}/>
          <Route path="/quantitative-reasoning" element={<PageTransition><QuantitativeReasoning/></PageTransition>}/>
          <Route path="/visuo-spatial-manipulation" element={<PageTransition><VisuoSpatialManipulation/></PageTransition>}/>
          <Route path="/verbal-reasoning" element={<PageTransition><VerbalReasoning/></PageTransition>}/>

          <Route path="/mind-burst" element={<PageTransition><MindBurst/></PageTransition>}/>
        </Routes>
      </AnimatePresence>
    </>
  )
}
export default App
