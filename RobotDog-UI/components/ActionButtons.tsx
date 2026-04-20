import React from 'react';

interface ActionButtonsProps {
  activeButtons: { [key: string]: boolean };
  onButtonPress: (btn: string, active: boolean) => void;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({ activeButtons, onButtonPress }) => {
  const btnClass = (key: string, color: string) => `
    w-14 h-14 sm:w-16 sm:h-16 rounded-full flex items-center justify-center 
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
    <div className="grid grid-cols-3 gap-4 sm:gap-6 p-6 rotate-12">
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
      <div className="flex justify-start items-end">
        {/* Y - Photo Mode */}
        <button
          className={btnClass('y', 'bg-yellow-600 text-yellow-100')}
          onClick={() => handleClickButton('y')}
        >Photo Mode</button>
      </div>
      <div className="flex justify-start items-end">
        {/* B - Stop Recording */}
        <button
          className={btnClass('b', 'bg-red-600 text-red-100')}
          onClick={() => handleClickButton('b')}
        >Stop Recording</button>
      </div>
      <div className="flex justify-end items-start">
        {/* X - Video Mode */}
        <button
          className={btnClass('x', 'bg-blue-600 text-blue-100')}
          onClick={() => handleClickButton('x')}
        >Video Mode</button>
      </div>
      <div className="flex justify-start items-start">
        {/* A - Capture Photo/Video */}
        <button
          className={btnClass('a', 'bg-green-600 text-green-100')}
          onClick={() => handleClickButton('a')}
        >Capture</button>
      </div>
      <div className="flex justify-start items-start">
        {/* C - File Upload */}
        <button
          className={btnClass('c', 'bg-purple-600 text-purple-100')}
          onClick={() => handleClickButton('c')}
        >File Upload</button>
      </div>
      <div className="flex justify-start items-start">
        {/* D - Connect Camera */}
        <button
          className={btnClass('d', 'bg-pink-600 text-pink-100')}
          onClick={() => handleClickButton('d')}
        >Connect Camera</button>
      </div>
      <div className="flex justify-start items-start">
        {/* E - Disconnect Camera */}
        <button
          className={btnClass('e', 'bg-orange-600 text-orange-100')}
          // onMouseDown={() => handlePress('d', true)}
          // onMouseUp={() => handlePress('d', false)}
          // onMouseLeave={() => handlePress('d', false)}
          // onTouchStart={() => handlePress('d', true)}
          // onTouchEnd={() => handlePress('d', false)}
          onClick={() => handleClickButton('e')}
        >Disconnect Camera</button>
      </div>
    </div>
  );
};