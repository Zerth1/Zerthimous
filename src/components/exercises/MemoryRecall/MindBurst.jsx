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

function Settings() {
    const [activeTab, setActiveTab] = useState(null);
    return (
        <div className="flex flex-col sm:flex-col md:flex-col lg:flex-row-reverse lg:flex-col flex-nowrap w-full lg:w-1/5 bg-gray-900 text-white p-4">
            <div className="w-full lg:min-h-screen">
                <h2 className="text-3xl font-bold pt-4 mb-4">Settings</h2>
                <ul className="space-y-2">
                    {["general", "appearance", "notifications"].map((tab) => {
                        const SettingsComponent = settingsComponents[tab];
                        return (
                            <li
                                key={tab}
                                className={`p-2 rounded-lg cursor-pointer text-1xl font-bold ${
                                    activeTab === tab ? "bg-gray-700" : "hover:bg-gray-800"
                                }`}
                                onClick={() => setActiveTab(activeTab === tab ? null : tab)}
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
        <div>
            <h1 className="absolute bottom-4 right-4 text-3xl font-bold">
                Press [Space] To Start/Stop
            </h1>
        </div>
    ); 
}

export default function MindBurst() {
    const [isGamePlaying, setIsGamePlaying] = useState(true);

    useEffect(() => {
        const handleKeyPress = (event) => {
            if (event.key === " ") {
                event.preventDefault()
                setIsGamePlaying((prev) => !prev);
            }
        };
        window.addEventListener("keydown", handleKeyPress);
        return () => {
            window.removeEventListener("keydown", handleKeyPress);
        };
    }, []);

    return (
        <div>
            {isGamePlaying && <Settings />}
            <Game />
        </div>
    );
}
