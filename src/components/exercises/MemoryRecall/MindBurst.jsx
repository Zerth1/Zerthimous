import { useState, useEffect } from "react";
const GeneralSettings = () => (
    <div>
      <input type="text" placeholder="Username" className="flex flex-col justify-between p-2 border rounded-md w-full" />
    </div>
);
  
const AppearanceSettings = () => (
    <div>
      <label className="flex flex-col justify-between space-x-2 space-y-8">
        <span>Dark Mode <input type="checkbox" className="toggle-checkbox"/></span>
      </label>
    </div>
);
  
const NotificationSettings = () => (
    <div>
      <select className="flex flex-col justify-between p-2 border rounded-md space-y-8">
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
        <div className="flex flex-col sm:flex-col md:flex-col lg:flex-row-reverse flex-nowrap">
            <div className="w-full sm:w-full md:w-full lg:min-h-screen lg:w-1/6 pt-0 bg-gray-900 text-white p-4 fixed bottom-0">
                <h2 className="text-3xl font-bold pt-4 mb-4">Settings</h2>
                <ul>
                    {["general", "appearance", "notifications"].flatMap((tab) => {
                        const SettingsComponent = settingsComponents[tab];
                        return [
                            <li
                                key={tab}
                                className={`p-2 rounded-lg cursor-pointer text-2xl font-bold ${
                                    activeTab === tab ? "bg-gray-700" : "hover:bg-gray-800"
                                }`}
                                onClick={() => setActiveTab(activeTab === tab ? null : tab)}
                            >
                                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                            </li>,
                            activeTab === tab ? (
                                <div key={`${tab}-settings`} className="p-4 bg-gray-800 rounded-lg">
                                    <SettingsComponent />
                                </div>
                            ) : null,
                        ];
                    })}
                </ul>
            </div>
        </div>
    );
}
function Game() {
    return (
        <div>
            <h1 className="text-3xl font-bold">Press [Space] To Start/Stop</h1>
        </div>
    )
}
export default function MindBurst() {
    const [isGamePlaying, setIsGamePlaying] = useState(true);
    useEffect(() => {
        const handleKeyPress = (event) => {
            if (event.key === " ") {
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
            {isGamePlaying && <Settings/>}
            <Game/>
        </div>
    );
}