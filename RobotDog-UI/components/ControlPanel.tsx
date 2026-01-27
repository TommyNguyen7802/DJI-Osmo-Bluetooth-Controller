import React, { useEffect } from 'react';
import { DPad } from './DPad';
import { ActionButtons } from './ActionButtons';
import { Direction } from '../types';
import { Gamepad2 } from 'lucide-react';

interface ControlPanelProps {
  onDirectionChange: (dir: Direction) => void;
  onButtonPress: (btn: string, active: boolean) => void;
  activeDirection: Direction;
  activeButtons: { [key: string]: boolean };
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  onDirectionChange,
  onButtonPress,
  activeDirection,
  activeButtons
}) => {
  
  // Keyboard mapping
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.repeat) return; // Ignore hold-down repeat for initial logic if needed, but here we want sustained state
      
      switch(e.key.toLowerCase()) {
        case 'w':
        case 'arrowup':
          onDirectionChange(Direction.UP);
          break;
        case 's':
        case 'arrowdown':
          onDirectionChange(Direction.DOWN);
          break;
        case 'a':
        case 'arrowleft':
          onDirectionChange(Direction.LEFT);
          break;
        case 'd':
        case 'arrowright':
          onDirectionChange(Direction.RIGHT);
          break;
        case 'enter': // Button A
          onButtonPress('a', true);
          break;
        case 'escape': // Button B
          onButtonPress('b', true);
          break;
        case 'shift': // Button X
          onButtonPress('x', true);
          break;
        case ' ': // Button Y
          onButtonPress('y', true);
          break;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      switch(e.key.toLowerCase()) {
        case 'w':
        case 'arrowup':
        case 's':
        case 'arrowdown':
        case 'a':
        case 'arrowleft':
        case 'd':
        case 'arrowright':
          onDirectionChange(Direction.NONE);
          break;
        case 'enter':
          onButtonPress('a', false);
          break;
        case 'escape':
          onButtonPress('b', false);
          break;
        case 'shift':
          onButtonPress('x', false);
          break;
        case ' ':
          onButtonPress('y', false);
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [onDirectionChange, onButtonPress]);

  return (
    <div className="w-full h-full bg-gray-800 flex flex-col relative overflow-hidden">
        {/* Background Decorative Grid */}
        <div className="absolute inset-0 opacity-5 pointer-events-none" 
             style={{ 
                 backgroundImage: 'radial-gradient(circle, #ffffff 1px, transparent 1px)', 
                 backgroundSize: '20px 20px' 
             }}>
        </div>

        {/* Header Label */}
        <div className="absolute top-4 left-0 w-full text-center pointer-events-none">
            <div className="inline-flex items-center gap-2 bg-gray-900/80 px-4 py-1.5 rounded-full border border-gray-700 text-xs font-mono text-gray-400">
                <Gamepad2 size={14} />
                <span>MANUAL OVERRIDE ENABLED</span>
            </div>
        </div>

        <div className="flex-1 flex flex-col md:flex-row items-center justify-around gap-8 p-8 relative z-10">
            {/* Left Zone: D-Pad */}
            <div className="flex flex-col items-center gap-4">
                <span className="text-xs font-bold text-gray-500 tracking-widest">DIRECTIONAL</span>
                <DPad activeDirection={activeDirection} onDirectionChange={onDirectionChange} />
                <div className="text-[10px] text-gray-600 font-mono">WASD / ARROW KEYS</div>
            </div>

            {/* Divider (Desktop Only) */}
            <div className="hidden md:block w-px h-32 bg-gradient-to-b from-transparent via-gray-600 to-transparent"></div>

            {/* Right Zone: Actions */}
            <div className="flex flex-col items-center gap-4">
                <span className="text-xs font-bold text-gray-500 tracking-widest">MODULES</span>
                <ActionButtons activeButtons={activeButtons} onButtonPress={onButtonPress} />
                <div className="text-[10px] text-gray-600 font-mono">SPACE - SHIFT - ENT - ESC</div>
            </div>
        </div>
    </div>
  );
};