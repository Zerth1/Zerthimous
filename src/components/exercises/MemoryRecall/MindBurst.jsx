import { useState, useEffect, useRef, createContext, useContext } from "react";
import { useLocalStorage } from "../../../useLocalStorage";

// Create a context for the settings
const SettingsContext = createContext();

const DifficultySettings = () => {
    const { 
      chunkLength, setChunkLength, 
      numberOfDigits, setNumberOfDigits, 
      timer, setTimer 
    } = useContext(SettingsContext);
  
    const handleChunkLengthChange = (e) => {
      const value = e.target.value;
      setChunkLength(value);
    };
  
    const handleNumberOfDigitsChange = (e) => {
      const value = e.target.value;
      setNumberOfDigits(value);
    };
  
    const handleTimerChange = (e) => {
      const value = e.target.value;
      setTimer(value);
    };
  
    const handleChunkLengthBlur = () => {
      if (chunkLength === '' || isNaN(parseInt(chunkLength))) {
        setChunkLength(1);
      } else {
        const numValue = parseInt(chunkLength) || 1;
        const validatedValue = Math.max(1, Math.min(20, numValue));
        setChunkLength(validatedValue);
        if (numberOfDigits !== '' && !isNaN(parseInt(numberOfDigits))) {
          const numDigitsValue = parseInt(numberOfDigits);
          if (numDigitsValue < validatedValue) {
            setNumberOfDigits(Math.max(10, validatedValue));
          }
        }
      }
    };
  
    const handleNumberOfDigitsBlur = () => {
      if (numberOfDigits === '' || isNaN(parseInt(numberOfDigits))) {
        setNumberOfDigits(Math.max(10, chunkLength || 1));
      } else {
        const numValue = parseInt(numberOfDigits) || 10;
        const minValue = Math.max(10, chunkLength || 1);
        const validatedValue = Math.max(minValue, Math.min(100, numValue));
        setNumberOfDigits(validatedValue);
      }
    };
  
    const handleTimerBlur = () => {
      const numValue = parseInt(timer);
      if (timer === '' || isNaN(numValue)) {
        setTimer(30);
      } else {
        const validatedValue = Math.max(1, Math.min(300, numValue));
        setTimer(validatedValue);
      }
    };
  
    return (
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">
            Chunk Length: {chunkLength}
          </label>
          <input
            type="number"
            min="1"
            max="20"
            value={chunkLength}
            onChange={handleChunkLengthChange}
            onBlur={handleChunkLengthBlur}
            className="w-full p-2 bg-gray-700 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Number of Digits: {numberOfDigits}
          </label>
          <input
            type="number"
            min={Math.max(10, chunkLength || 1)}
            max="100"
            value={numberOfDigits}
            onChange={handleNumberOfDigitsChange}
            onBlur={handleNumberOfDigitsBlur}
            className="w-full p-2 bg-gray-700 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">
            Timer (seconds): {timer}
          </label>
          <input
            type="number"
            min="1"
            max="300"
            value={timer ?? ''}
            onChange={handleTimerChange}
            onBlur={handleTimerBlur}
            className="w-full p-2 bg-gray-700 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    );
};

function Settings({ onTabChange }) {
  const [activeTab, setActiveTab] = useState("difficulty");
  const handleTabClick = () => {
    setActiveTab(activeTab === "difficulty" ? null : "difficulty");
    onTabChange(activeTab === "difficulty" ? null : "difficulty");
  };
  const handleSettingsClick = (e) => {
    e.stopPropagation();
  };
  
  return (
    <div className="flex flex-col h-auto lg:h-full w-full lg:w-1/5 bg-gray-900 text-white">
      <div className="w-full p-4">
        <h2 className="text-3xl font-bold mb-4">Settings</h2>
        <div
          className={`p-2 rounded-lg cursor-pointer text-xl font-bold ${
            activeTab === "difficulty" ? "bg-gray-700" : "hover:bg-gray-800"
          }`}
          onClick={handleTabClick}
        >
          Difficulty
          {activeTab === "difficulty" && (
            <div
              className="p-4 bg-gray-800 rounded-lg mt-2"
              onClick={handleSettingsClick}
            >
              <DifficultySettings />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Game() {
    const { 
        isGamePlaying, 
        setIsGamePlaying, 
        chunkLength, 
        numberOfDigits, 
        timer 
    } = useContext(SettingsContext);
    const [generatedNumber, setGeneratedNumber] = useState(null);
    const [chunks, setChunks] = useState([]);
    const [currentChunkIndex, setCurrentChunkIndex] = useState(-1);
    const [time, setTime] = useState(timer);

    const generateNumber = () => {
        const digits = Math.max(1, Math.floor(Number(numberOfDigits) || 1));
        let result = '';
        for (let i = 0; i < digits; i++) {
            const digit = Math.floor(Math.random() * 10);
            result += digit;
        }
        return result;
    };

    const generateNewNumber = () => {
        const newNumber = generateNumber();
        setGeneratedNumber(newNumber);
    };

    const createChunks = (number) => {
        const chunkSize = Math.max(1, Math.floor(Number(chunkLength) || 1));
        const newChunks = [];
        for (let i = 0; i < number.length; i += chunkSize) {
            newChunks.push(number.slice(i, i + chunkSize));
        }
        return newChunks;
    };

    const initializeNumber = (number) => {
        if (!number || !isGamePlaying) return;
        const newChunks = createChunks(number);
        setChunks(newChunks);
        setCurrentChunkIndex(0);
    };

    useEffect(() => {
        let interval;
        if (isGamePlaying && time > 0) {
            interval = setInterval(() => {
                setTime((prev) => prev - 1);
            }, 1000);
        } else if (isGamePlaying && time <= 0) {
            const concatenatedChunks = chunks.join('');
            const userInput = prompt('Enter The Full Number (All Chunks Concatenated In order):');
            if (userInput !== null) {
                if (userInput === concatenatedChunks) {
                    alert('Correct! Well Done!');
                } else {
                    alert(`Incorrect. Your Input: ${userInput}. Correct Number: ${concatenatedChunks}`);
                }
            }
            setIsGamePlaying(false);
        }
        return () => clearInterval(interval);
    }, [isGamePlaying, time, setIsGamePlaying, chunks]);

    useEffect(() => {
        if (isGamePlaying) {
            setTime(timer);
        }
    }, [isGamePlaying, timer]);

    useEffect(() => {
        const handleKeyPress = (event) => {
            if (event.key === 'a' && chunks.length > 0) {
                setCurrentChunkIndex(prev => 
                    prev > 0 ? prev - 1 : prev
                );
            } else if (event.key === 'l' && chunks.length > 0) {
                setCurrentChunkIndex(prev => 
                    prev < chunks.length - 1 ? prev + 1 : prev
                );
            }
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [chunks, currentChunkIndex]);

    useEffect(() => {
        if (isGamePlaying) {
            if (!generatedNumber) {
                generateNewNumber();
            }
        } else {
            setGeneratedNumber(null);
            setChunks([]);
            setCurrentChunkIndex(-1);
        }
    }, [isGamePlaying]);

    useEffect(() => {
        if (isGamePlaying && generatedNumber) {
            initializeNumber(generatedNumber);
        }
    }, [generatedNumber, chunkLength, isGamePlaying]);

    return (
        <div className="flex-1 flex items-center justify-center min-h-screen text-white relative">
            <div className="text-center">
                <p className="text-3xl font-bold">
                    {currentChunkIndex >= 0 && currentChunkIndex < chunks.length 
                        ? chunks[currentChunkIndex] 
                        : ' '}
                </p>
            </div>
            {isGamePlaying && (
                <>
                    <div className="absolute top-4 right-4 text-right">
                        <p className="text-xl font-bold">[A] Previous Chunk</p>
                        <p className="text-xl font-bold">[L] Next Chunk</p>
                    </div>
                    <div 
                        className="absolute w-full text-center text-2xl font-bold"
                        style={{ top: '25%' }}
                    >
                        Timer: {time}
                    </div>
                </>
            )}
        </div>
    );
}

export default function MindBurst() {
    const [isGamePlaying, setIsGamePlaying] = useState(false);
    const [windowHeight, setWindowHeight] = useState("min-h-screen lg:h-screen");
  
    const [chunkLength, setChunkLength] = useLocalStorage('mind_burst_chunk_length', 5);
    const [numberOfDigits, setNumberOfDigits] = useLocalStorage('mind_burst_number_of_digits', 10);
    const [timer, setTimer] = useLocalStorage('mind_burst_timer', 30)
  
    const handleTabChange = (activeTab) => {
      if (activeTab) {
        setWindowHeight("min-h-screen h-[calc(100vh+500px)]");
      } else {
        setWindowHeight("min-h-screen lg:h-screen");
      }
    };
  
    const toggleGame = () => {
      if (!isGamePlaying) {
        handleTabChange(false);
      }
      setIsGamePlaying((prev) => !prev);
    };
  
    useEffect(() => {
      const handleKeyPress = (event) => {
        if (event.key === " ") {
          event.preventDefault();
          toggleGame();
        }
      };
      
      window.addEventListener("keydown", handleKeyPress);
      return () => window.removeEventListener("keydown", handleKeyPress);
    }, [isGamePlaying]);
  
    const settingsContextValue = {
      isGamePlaying,
      setIsGamePlaying,
      chunkLength,
      setChunkLength,
      numberOfDigits,
      setNumberOfDigits,
      timer, 
      setTimer
    };
  
    return (
      <SettingsContext.Provider value={settingsContextValue}>
        <div className={`flex flex-col ${windowHeight} relative`}>
          <div className="flex flex-col lg:flex-row flex-1 overflow-hidden">
            {isGamePlaying ? (
              <Game />
            ) : (
              <Settings onTabChange={handleTabChange} />
            )}
          </div>
          <div className="absolute bottom-4 right-4 flex items-center space-x-4">
            <button
              onClick={toggleGame}
              className="px-4 py-2 bg-blue-500 text-white font-bold rounded hover:bg-blue-600 focus:outline-none"
            >
              {isGamePlaying ? 'Stop' : 'Start'}
            </button>
            <h1 className="text-3xl font-bold text-white">
              Press [Space] To Start/Stop
            </h1>
          </div>
        </div>
      </SettingsContext.Provider>
    );
}