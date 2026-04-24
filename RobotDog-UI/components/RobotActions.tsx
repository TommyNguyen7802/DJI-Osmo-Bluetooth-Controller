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

    if (key === "w") fetch("http://localhost:8010/dog/stand", { method: "POST" });
    if (key === "v") fetch("http://localhost:8010/dog/damp", { method: "POST" });
    if (key === "m") fetch("http://localhost:8010/dog/sit", { method: "POST" });
    if (key === "n") fetch("http://localhost:8010/dog/wave", { method: "POST" });
  };

  const handleClickButton = (key: string) => {
    handlePress(key, true);
    setTimeout(() => handlePress(key, false), 120);
  };

  return (
    // comment
    <div className="grid grid-cols-2 gap-4 sm:gap-6 p-6">
      <div className="flex justify-end items-end">
        {/* V - Damp Dog / Lay Down */}
        <button
          className={btnClass('v', 'bg-red-600 text-red-100')}
          onClick={() => handleClickButton('v')}
        >Lay Down</button>
      </div>
      <div className="flex justify-start items-end">
        {/* W - Arm Dog / Stand */}
        <button
          className={btnClass('w', 'bg-green-600 text-green-100')}
          onClick={() => handleClickButton('w')}
        >Stand Up</button>
      </div>
      <div className="flex justify-end items-end">
        {/* M - Sit Dog */}
        <button
          className={btnClass('m', 'bg-yellow-600 text-yellow-100')}
          onClick={() => handleClickButton('m')}
        >Sit</button>
      </div>
      <div className="flex justify-end items-end">
        {/* N - Wave Dog */}
        <button
          className={btnClass('n', 'bg-blue-600 text-blue-100')}
          onClick={() => handleClickButton('n')}
        >Wave</button>
      </div>
    </div>
  );
};