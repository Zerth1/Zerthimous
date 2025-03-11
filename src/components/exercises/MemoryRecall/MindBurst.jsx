import { useState, useEffect, createContext, useContext } from "react";
import { useLocalStorage } from "../../../useLocalStorage";
// Create a context for the settings
const SettingsContext = createContext();

const DifficultySettings = () => {
  const { chunkLength, setChunkLength, numberOfDigits, setNumberOfDigits } = useContext(SettingsContext);

  const handleChunkLengthChange = (e) => {
    const value = e.target.value;
    if (value === '') {
      setChunkLength('');
    } else {
      const numValue = parseInt(value) || 1;
      setChunkLength(Math.max(1, Math.min(20, numValue)));
    }
  };

  const handleNumberOfDigitsChange = (e) => {
    const value = e.target.value;
    if (value === '') {
      setNumberOfDigits('');
    } else {
      const numValue = parseInt(value) || 10; // Default to 10 instead of 1
      // Ensure minimum is 10 and at least chunkLength
      const minValue = Math.max(10, chunkLength || 1);
      setNumberOfDigits(Math.max(minValue, Math.min(100, numValue)));
    }
  };

  const handleChunkLengthBlur = () => {
    if (chunkLength === '' || isNaN(parseInt(chunkLength))) {
      setChunkLength(1);
    } else {
      const numValue = parseInt(chunkLength) || 1;
      setChunkLength(Math.max(1, Math.min(20, numValue)));
      // Adjust numberOfDigits if it's less than the new chunkLength
      if (numberOfDigits < numValue) {
        setNumberOfDigits(Math.max(10, numValue));
      }
    }
  };

  const handleNumberOfDigitsBlur = () => {
    if (numberOfDigits === '' || isNaN(parseInt(numberOfDigits))) {
      // Default to 10 or chunkLength, whichever is greater
      setNumberOfDigits(Math.max(10, chunkLength || 1));
    } else {
      const numValue = parseInt(numberOfDigits) || 10;
      // Ensure minimum is 10 and at least chunkLength
      const minValue = Math.max(10, chunkLength || 1);
      setNumberOfDigits(Math.max(minValue, Math.min(100, numValue)));
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
          min={Math.max(10, chunkLength || 1)} // Reflect dynamic min in UI
          max="100"
          value={numberOfDigits}
          onChange={handleNumberOfDigitsChange}
          onBlur={handleNumberOfDigitsBlur}
          className="w-full p-2 bg-gray-700 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>
  );
};

// Single declaration of settingsComponents
const settingsComponents = {
  difficulty: DifficultySettings,
};

function Settings({ onTabChange }) {
  const [activeTab, setActiveTab] = useState(null);
  const handleTabClick = (tab) => {
    setActiveTab(activeTab === tab ? null : tab);
    onTabChange(activeTab === tab ? null : tab);
  };
  const handleSettingsClick = (e) => {
    e.stopPropagation();
  };
  return (
    <div className="flex flex-col h-auto lg:h-full w-full lg:w-1/5 bg-gray-900 text-white">
      <div className="w-full p-4">
        <h2 className="text-3xl font-bold mb-4">Settings</h2>
        <ul className="space-y-2">
          {["difficulty"].map((tab) => {
            const SettingsComponent = settingsComponents[tab];
            return (
              <li
                key={tab}
                className={`p-2 rounded-lg cursor-pointer text-1xl font-bold ${
                  activeTab === tab ? "bg-gray-700" : "hover:bg-gray-800"
                }`}
                onClick={() => handleTabClick(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                {activeTab === tab && (
                  <div 
                    className="p-4 bg-gray-800 rounded-lg mt-2"
                    onClick={handleSettingsClick}
                  >
                    <SettingsComponent />
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}

function Game() {
  const { chunkLength, numberOfDigits } = useContext(SettingsContext);
  
  return (
    <div className="flex-1 relative">
      <h1 className="absolute bottom-4 right-4 text-3xl font-bold">
        Press [Space] To Start/Stop
      </h1>
      {/* You can use the settings here */}
      {/* <p>Chunk Length: {chunkLength}, Number of Digits: {numberOfDigits}</p> */}
    </div>
  );
}

export default function MindBurst() {
  const [isGamePlaying, setIsGamePlaying] = useState(true);
  const [windowHeight, setWindowHeight] = useState("min-h-screen lg:h-screen");
  
  const [chunkLength, setChunkLength] = useLocalStorage('mind_burst_chunk_length', 5);
  const [numberOfDigits, setNumberOfDigits] = useLocalStorage('mind_burst_number_of_digits', 10);

  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === " ") {
        event.preventDefault();
        setIsGamePlaying((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyPress);
    return () => {
      window.removeEventListener("keydown", handleKeyPress);
    };
  }, []);

  const handleTabChange = (activeTab) => {
    if (activeTab) {
      setWindowHeight("min-h-screen h-[calc(100vh+500px)]");
    } else {
      setWindowHeight("min-h-screen h-screen");
    }
  };

  const settingsContextValue = {
    chunkLength,
    setChunkLength,
    numberOfDigits,
    setNumberOfDigits
  };

  return (
    <SettingsContext.Provider value={settingsContextValue}>
      <div className={`flex flex-col ${windowHeight}`}>
        <div className="flex flex-col lg:flex-row flex-1 overflow-hidden">
          {isGamePlaying && <Settings onTabChange={handleTabChange} />}
          <Game />
        </div>
      </div>
    </SettingsContext.Provider>
  );
}