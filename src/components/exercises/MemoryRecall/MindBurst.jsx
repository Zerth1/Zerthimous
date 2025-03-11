import { useState } from "react"
const GeneralSettings = () => (
    <div>
      <input type="text" placeholder="Username" className="p-2 border rounded-md w-full" />
    </div>
);
  
const AppearanceSettings = () => (
    <div>
      <label className="flex items-center space-x-2">
        <span>Dark Mode</span>
        <input type="checkbox" className="toggle-checkbox" />
      </label>
    </div>
);
  
const NotificationSettings = () => (
    <div>
      <select className="p-2 border rounded-md">
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
        <div className="flex flex-row-reverse h-fit">
            <div className="w-1/6 h-screen bg-gray-900 text-white p-4">
                <h2 className="text-3xl font-bold mb-4">Settings</h2>
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
                                <div key={`${tab}-settings`} className="p-4 bg-gray-800 rounded-lg mt-2">
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
export default function MindBurst() {
    return (
        <div>
            <Settings/>
        </div>
    );
}