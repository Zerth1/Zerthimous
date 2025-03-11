import { useState, useEffect } from "react";

const GeneralSettings = () => (
  <div>
    <input type="text" placeholder="Username" className="p-2 border rounded-md w-full" />
  </div>
);

const AppearanceSettings = () => (
  <div>
    <label className="flex flex-col space-y-4">
      <span>Dark Mode <input type="checkbox" className="toggle-checkbox" /></span>
    </label>
  </div>
);

const NotificationSettings = () => (
  <div>
    <select className="p-2 border rounded-md w-full">
      <option>Email</option>
      <option>Push</option>
      <option>SMS</option>
    </select>
  </div>
);

const settingsComponents = {
  general: GeneralSettings,
  appearance: AppearanceSettings,
  notifications: NotificationSettings,
};

function Settings({ onTabChange }) {
  const [activeTab, setActiveTab] = useState(null);
  const handleTabClick = (tab) => {
    setActiveTab(activeTab === tab ? null : tab);
    onTabChange(activeTab === tab ? null : tab);
  };
  
  return (
    <div className="flex flex-col h-auto lg:h-full w-full lg:w-1/5 bg-gray-900 text-white">
      <div className="w-full p-4">
        <h2 className="text-3xl font-bold mb-4">Settings</h2>
        <ul className="space-y-2">
          {["general", "appearance", "notifications"].map((tab) => {
            const SettingsComponent = settingsComponents[tab];
            return (
              <li
                key={tab}
                className={`p-2 rounded-lg cursor-pointer text-1xl font-bold ${activeTab === tab ? "bg-gray-700" : "hover:bg-gray-800"}`}
                onClick={() => handleTabClick(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                {activeTab === tab && (
                  <div className="p-4 bg-gray-800 rounded-lg mt-2">
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
  return (
    <div className="flex-1 relative">
      <h1 className="absolute bottom-4 right-4 text-3xl font-bold">
        Press [Space] To Start/Stop
      </h1>
    </div>
  );
}

export default function MindBurst() {
  const [isGamePlaying, setIsGamePlaying] = useState(true);
  const [windowHeight, setWindowHeight] = useState("min-h-screen lg:h-screen");

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
      // Only change height for large screens when tab is active
      setWindowHeight("min-h-screen h-[calc(100vh+500px)]");
    } else {
      // Reset to default height
      setWindowHeight("min-h-screen h-screen");
    }
  };

  return (
    <div className={`flex flex-col ${windowHeight}`}>
      <div className="flex flex-col lg:flex-row flex-1 overflow-hidden">
        {isGamePlaying && <Settings onTabChange={handleTabChange} />}
        <Game />
      </div>
    </div>
  );
}