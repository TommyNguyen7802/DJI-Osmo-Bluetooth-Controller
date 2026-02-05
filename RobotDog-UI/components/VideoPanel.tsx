import React, { useState, useRef, useEffect } from 'react';
import { Settings, Play, Pause, RefreshCw, VideoOff } from 'lucide-react';

interface VideoPanelProps {
  onLog: (msg: string, type?: 'info' | 'warning' | 'error' | 'success') => void;
}

export const VideoPanel: React.FC<VideoPanelProps> = ({ onLog }) => {
  const [videoSrc, setVideoSrc] = useState<string>('https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4');
  const [inputSrc, setInputSrc] = useState<string>('https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4');
  const [isPlaying, setIsPlaying] = useState(true);
  const [showControls, setShowControls] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleUpdateSource = () => {
    if (inputSrc) {
      setVideoSrc(inputSrc);
      onLog(`Video source updated: ${inputSrc}`, 'info');
    }
  };

  const togglePlay = () => {
    if (videoRef.current) {
      if (videoRef.current.paused) {
        videoRef.current.play().catch(e => {
            onLog(`Error playing video: ${e.message}`, 'error');
        });
      } else {
        videoRef.current.pause();
      }
    }
  };

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);
    const onError = () => {
        setIsPlaying(false);
        onLog('Video playback error occurred', 'error');
    };

    video.addEventListener('play', onPlay);
    video.addEventListener('pause', onPause);
    video.addEventListener('error', onError);

    return () => {
      video.removeEventListener('play', onPlay);
      video.removeEventListener('pause', onPause);
      video.removeEventListener('error', onError);
    };
  }, [onLog]);

  useEffect(() => {
  if (videoRef.current && videoSrc) {
    videoRef.current.play().catch(e => {
      onLog(`Autoplay failed: ${e.message}`, 'warning');
    });
  }
}, [videoSrc, onLog]);


  return (
    <div 
      className="relative w-full h-full bg-black flex items-center justify-center overflow-hidden group border-b md:border-b-0 md:border-r border-gray-700"
      onMouseEnter={() => setShowControls(true)}
      onMouseLeave={() => setShowControls(false)}
    >
      {videoSrc ? (
        <video 
          ref={videoRef}
          src={videoSrc} 
          className="w-full h-full object-contain"
          playsInline
          Autoplay
          muted
          loop
          crossOrigin="anonymous"
        />
      ) : (
        <div className="flex flex-col items-center text-gray-500 space-y-2">
            <VideoOff size={48} />
            <span className="font-mono text-sm">No Signal Source</span>
        </div>
      )}

      {/* Overlay Controls */}
      <div className={`absolute top-0 left-0 w-full p-4 transition-opacity duration-300 ${showControls || !videoSrc ? 'opacity-100' : 'opacity-0'}`}>
        <div className="bg-black/70 backdrop-blur-md p-3 rounded-lg border border-gray-700 shadow-xl max-w-lg mx-auto flex items-center gap-2">
            <div className="p-2 bg-gray-800 rounded-md">
                <Settings size={18} className="text-gray-400" />
            </div>
            <input 
                type="text" 
                value={inputSrc}
                onChange={(e) => setInputSrc(e.target.value)}
                placeholder="Enter stream URL / file path..."
                className="flex-1 bg-transparent border-none text-xs sm:text-sm text-white focus:ring-0 placeholder-gray-500 font-mono outline-none"
            />
            <button 
                onClick={handleUpdateSource}
                className="p-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md transition-colors"
                title="Load Source"
            >
                <RefreshCw size={16} />
            </button>
             {videoSrc && (
                <button 
                    onClick={togglePlay}
                    className="p-2 bg-gray-700 hover:bg-gray-600 text-white rounded-md transition-colors"
                >
                    {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                </button>
            )}
        </div>
      </div>

      <div className="absolute bottom-4 left-4 bg-black/50 px-2 py-1 rounded text-xs font-mono text-green-400 border border-green-900/50">
        LIVE FEED ●
      </div>
    </div>
  );
};