import React, { useState, useCallback } from 'react';
import { VideoPanel } from './components/VideoPanel';
import { InfoPanel } from './components/InfoPanel';
import { ControlPanel } from './components/ControlPanel';
import { Direction, LogEntry } from './types';
import { Activity, Battery, Signal } from 'lucide-react';

const App: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([
    { id: '1', timestamp: new Date().toLocaleTimeString(), message: 'System initialized', type: 'info' },
    { id: '2', timestamp: new Date().toLocaleTimeString(), message: 'Waiting for video stream...', type: 'warning' }
  ]);
  
  const [activeDirection, setActiveDirection] = useState<Direction>(Direction.NONE);
  const [activeButtons, setActiveButtons] = useState({
    a: false, b: false, x: false, y: false
  });

  const addLog = useCallback((message: string, type: 'info' | 'warning' | 'error' | 'success' = 'info') => {
    const newLog: LogEntry = {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toLocaleTimeString(),
      message,
      type
    };
    setLogs(prev => [...prev.slice(-49), newLog]); // Keep last 50 logs
  }, []);

  const handleDirectionChange = (dir: Direction) => {
    if (dir !== activeDirection) {
      setActiveDirection(dir);
      if (dir !== Direction.NONE) {
        addLog(`Input Direction: ${dir}`, 'info');
      }
    }
  };

  const handleButtonPress = (btn: string, active: boolean) => {
    setActiveButtons(prev => {
        if (prev[btn as keyof typeof prev] !== active) {
             if (active) addLog(`Button ${btn.toUpperCase()} Pressed`, 'success');
             return { ...prev, [btn]: active };
        }
        return prev;
    });
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-black text-gray-200 font-sans overflow-hidden">
      {/* Top Half: Video & Logs */}
      <div className="flex-1 flex flex-col md:flex-row min-h-0">
        {/* Top Left: Video */}
        <div className="w-full md:w-1/2 h-1/2 md:h-full">
            <VideoPanel onLog={addLog} />
        </div>
        
        {/* Top Right: UI Text / Logs */}
        <div className="w-full md:w-1/2 h-1/2 md:h-full border-l border-gray-800">
            <InfoPanel logs={logs} />
        </div>
      </div>

      {/* Middle Status Bar (Thin) */}
      <div className="h-6 bg-blue-900/20 border-y border-blue-900/30 flex items-center justify-between px-4 text-[10px] sm:text-xs text-blue-200 font-mono tracking-wider">
        <div className="flex gap-4">
            <span className="flex items-center gap-1"><Signal size={12}/> RSSI: -42dBm</span>
            <span className="flex items-center gap-1"><Battery size={12}/> BAT: 98%</span>
        </div>
        <div className="flex gap-4">
            <span className="flex items-center gap-1"><Activity size={12}/> LATENCY: 24ms</span>
            <span>MODE: REMOTE</span>
        </div>
      </div>

      {/* Bottom Half: Controls */}
      <div className="h-1/2 min-h-[300px] border-t border-gray-800">
        <ControlPanel 
            activeDirection={activeDirection} 
            onDirectionChange={handleDirectionChange}
            activeButtons={activeButtons}
            onButtonPress={handleButtonPress}
        />
      </div>
    </div>
  );
};

export default App;