import React, { useRef, useEffect } from 'react';
import { Terminal, Activity, Wifi } from 'lucide-react';
import { LogEntry } from '../types';

interface InfoPanelProps {
  logs: LogEntry[];
}

export const InfoPanel: React.FC<InfoPanelProps> = ({ logs }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  return (
    <div className="w-full h-full bg-gray-900 flex flex-col min-h-0">
      {/* Header */}
      <div className="h-12 border-b border-gray-800 flex items-center justify-between px-4 bg-gray-950">
        <div className="flex items-center gap-2 text-gray-300">
          <Terminal size={18} />
          <span className="font-semibold text-sm tracking-wide">SYSTEM LOGS</span>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono">
            <div className="flex items-center gap-1.5 text-green-500">
                <Wifi size={14} />
                <span>CONNECTED</span>
            </div>
            <div className="flex items-center gap-1.5 text-blue-400">
                <Activity size={14} />
                <span>ACTIVE</span>
            </div>
        </div>
      </div>

      {/* Log Stream */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-sm space-y-1.5 scroll-smooth">
        {logs.length === 0 && (
            <div className="text-gray-600 italic text-center mt-10">Waiting for system events...</div>
        )}
        {logs.map((log) => (
          <div key={log.id} className="flex gap-3 hover:bg-white/5 p-1 rounded transition-colors">
            <span className="text-gray-500 shrink-0 select-none">[{log.timestamp}]</span>
            <span className={`break-all ${
                log.type === 'error' ? 'text-red-400 font-bold' :
                log.type === 'warning' ? 'text-yellow-400' :
                log.type === 'success' ? 'text-green-400' :
                'text-gray-300'
            }`}>
              {log.type === 'error' && '✖ '}
              {log.type === 'success' && '✔ '}
              {log.type === 'warning' && '⚠ '}
              {log.message}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Status Footer */}
      <div className="h-8 bg-gray-950 border-t border-gray-800 flex items-center px-4 text-xs text-gray-500 gap-4">
        <span>CPU: 12%</span>
        <span>MEM: 434MB</span>
        <span className="ml-auto">v1.0.4-rc</span>
      </div>
    </div>
  );
};