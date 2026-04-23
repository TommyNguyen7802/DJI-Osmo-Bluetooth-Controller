import React from 'react';

interface RobotActionsProps {
  activeButtons: { [key: string]: boolean };
  onButtonPress: (btn: string, active: boolean) => void;
}

export const RobotActions: React.FC<RobotActionsProps> = ({ activeButtons, onButtonPress }) => {
  const btnClass = (key: string, color: string) => `
    w-36 h-14 sm:w-38 sm:h-16 rounded-full px-4 flex items-center justify-center 
    text-xl font-bold font-mono transition-all duration-100 
    shadow-[0_4px_0_0_rgba(0,0,0,0.3)] active:shadow-none active:translate-y-[4px]
    border-2 border-white/5
    ${activeButtons[key]
      ? `shadow-none translate-y-[4px] brightness-125 scale-95 ring-2 ring-white/50 ring-offset-2 ring-offset-gray-900 ${color.replace('bg-', 'bg-')}`
      : `${color} opacity-80 hover:opacity-100`}
  `;

  const handlePress = (key: string, active: boolean) => {
    onButtonPress(key, active);
    if (!active) return;

    if (key === "a") fetch("http://localhost:8010/camera/start", { method: "POST" });
    if (key === "b") fetch("http://localhost:8010/camera/stop", { method: "POST" });
    if (key === "x") fetch("http://localhost:8010/camera/video", { method: "POST" });
    if (key === "y") fetch("http://localhost:8010/camera/photo", { method: "POST" });
    if (key === "c") fetch("http://localhost:8010/camera/transfer", { method: "POST" });
    if (key === "d") fetch("http://localhost:8010/camera/setup", { method: "POST" });
    if (key === "e") fetch("http://localhost:8010/camera/shutdown", { method: "POST" });
    if (key === "w") fetch("http://localhost:8010/dog/stand", { method: "POST" });
    if (key === "v") fetch("http://localhost:8010/dog/damp", { method: "POST" });
  };

  const handleClickButton = (key: string) => {
    handlePress(key, true);
    setTimeout(() => handlePress(key, false), 120);
  };

  return (
    // comment
    <div className="grid grid-cols-1 gap-4 sm:gap-6 p-6">
      <div className="flex justify-end items-end">
        {/* V - Damp Dog */}
        <button
          className={btnClass('v', 'bg-amber-800 text-amber-100')}
          onClick={() => handleClickButton('v')}
        >Damp Dog</button>
      </div>
      <div className="flex justify-start items-end">
        {/* W - Arm Dog / Stand */}
        <button
          className={btnClass('w', 'bg-gray-400 text-gray-900')}
          onClick={() => handleClickButton('w')}
        >Arm Dog</button>
      </div>
    </div>
  );
};