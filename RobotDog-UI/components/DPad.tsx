import React from 'react';
import { ChevronUp, ChevronDown, ChevronLeft, ChevronRight } from 'lucide-react';
import { Direction } from '../types';

interface DPadProps {
  activeDirection: Direction;
  onDirectionChange: (dir: Direction) => void;
}

export const DPad: React.FC<DPadProps> = ({ activeDirection, onDirectionChange }) => {
  const btnClass = (isActive: boolean) => `
    w-16 h-16 sm:w-20 sm:h-20 rounded-xl flex items-center justify-center 
    transition-all duration-100 shadow-[0_4px_0_0_rgba(0,0,0,0.3)] 
    active:shadow-none active:translate-y-[4px]
    border border-white/10
    ${isActive 
      ? 'bg-blue-600 text-white shadow-none translate-y-[4px] ring-2 ring-blue-400 ring-offset-2 ring-offset-gray-900' 
      : 'bg-gray-800 text-gray-400 hover:bg-gray-750 hover:text-white'}
  `;

  return (
    <div className="grid grid-cols-3 gap-2 sm:gap-3 p-4 bg-gray-950/50 rounded-3xl border border-gray-800">
      {/* Top Row */}
      <div />
      <button 
        className={btnClass(activeDirection === Direction.UP)}
        onMouseDown={() => onDirectionChange(Direction.UP)}
        onMouseUp={() => onDirectionChange(Direction.NONE)}
        onMouseLeave={() => onDirectionChange(Direction.NONE)}
        onTouchStart={() => onDirectionChange(Direction.UP)}
        onTouchEnd={() => onDirectionChange(Direction.NONE)}
      >
        <ChevronUp size={32} strokeWidth={3} />
      </button>
      <div />

      {/* Middle Row */}
      <button 
        className={btnClass(activeDirection === Direction.LEFT)}
        onMouseDown={() => onDirectionChange(Direction.LEFT)}
        onMouseUp={() => onDirectionChange(Direction.NONE)}
        onMouseLeave={() => onDirectionChange(Direction.NONE)}
        onTouchStart={() => onDirectionChange(Direction.LEFT)}
        onTouchEnd={() => onDirectionChange(Direction.NONE)}
      >
        <ChevronLeft size={32} strokeWidth={3} />
      </button>
      <div className="flex items-center justify-center">
        <div className="w-4 h-4 rounded-full bg-gray-700 shadow-inner" />
      </div>
      <button 
        className={btnClass(activeDirection === Direction.RIGHT)}
        onMouseDown={() => onDirectionChange(Direction.RIGHT)}
        onMouseUp={() => onDirectionChange(Direction.NONE)}
        onMouseLeave={() => onDirectionChange(Direction.NONE)}
        onTouchStart={() => onDirectionChange(Direction.RIGHT)}
        onTouchEnd={() => onDirectionChange(Direction.NONE)}
      >
        <ChevronRight size={32} strokeWidth={3} />
      </button>

      {/* Bottom Row */}
      <div />
      <button 
        className={btnClass(activeDirection === Direction.DOWN)}
        onMouseDown={() => onDirectionChange(Direction.DOWN)}
        onMouseUp={() => onDirectionChange(Direction.NONE)}
        onMouseLeave={() => onDirectionChange(Direction.NONE)}
        onTouchStart={() => onDirectionChange(Direction.DOWN)}
        onTouchEnd={() => onDirectionChange(Direction.NONE)}
      >
        <ChevronDown size={32} strokeWidth={3} />
      </button>
      <div />
    </div>
  );
};