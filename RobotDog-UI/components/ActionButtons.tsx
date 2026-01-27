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
  };

  return (
    <div className="grid grid-cols-2 gap-4 sm:gap-6 p-6 rotate-12">
      <div className="flex justify-end items-end">
        <button 
            className={btnClass('y', 'bg-yellow-600 text-yellow-100')}
            onMouseDown={() => handlePress('y', true)}
            onMouseUp={() => handlePress('y', false)}
            onMouseLeave={() => handlePress('y', false)}
            onTouchStart={() => handlePress('y', true)}
            onTouchEnd={() => handlePress('y', false)}
        >Y</button>
      </div>
      <div className="flex justify-start items-end">
        <button 
            className={btnClass('b', 'bg-red-600 text-red-100')}
            onMouseDown={() => handlePress('b', true)}
            onMouseUp={() => handlePress('b', false)}
            onMouseLeave={() => handlePress('b', false)}
            onTouchStart={() => handlePress('b', true)}
            onTouchEnd={() => handlePress('b', false)}
        >B</button>
      </div>
      <div className="flex justify-end items-start">
        <button 
            className={btnClass('x', 'bg-blue-600 text-blue-100')}
            onMouseDown={() => handlePress('x', true)}
            onMouseUp={() => handlePress('x', false)}
            onMouseLeave={() => handlePress('x', false)}
            onTouchStart={() => handlePress('x', true)}
            onTouchEnd={() => handlePress('x', false)}
        >X</button>
      </div>
      <div className="flex justify-start items-start">
        <button 
            className={btnClass('a', 'bg-green-600 text-green-100')}
            onMouseDown={() => handlePress('a', true)}
            onMouseUp={() => handlePress('a', false)}
            onMouseLeave={() => handlePress('a', false)}
            onTouchStart={() => handlePress('a', true)}
            onTouchEnd={() => handlePress('a', false)}
        >A</button>
      </div>
    </div>
  );
};