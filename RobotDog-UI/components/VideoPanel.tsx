import React, { useRef, useEffect, useState } from "react";

export const VideoPanel = ({ onLog }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!videoRef.current) return;

    const pc = new RTCPeerConnection();

    pc.addTransceiver("video", { direction: "recvonly" });

    pc.ontrack = (event) => {
      onLog("Received WebRTC track", "info");
      videoRef.current!.srcObject = event.streams[0];

      videoRef.current!.play().catch((e) => {
        onLog(`Autoplay failed: ${e.message}`, "warning");
      });

      event.track.onmute = () => onLog("Track muted", "warning");
      event.track.onunmute = () => onLog("Track unmuted", "info");
    };

    async function start() {
      try {
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        const res = await fetch("http://localhost:8080/offer", {
          method: "POST",
          body: JSON.stringify(offer),
          headers: { "Content-Type": "application/json" },
        });

        const answer = await res.json();
        await pc.setRemoteDescription(answer);

        onLog("WebRTC negotiation complete", "success");
      } catch (err: any) {
        onLog(`WebRTC error: ${err.message}`, "error");
      }
    }

    start();

    return () => {
      pc.close();
    };
  }, []);

  return (
    <div className="relative w-full h-full bg-black flex items-center justify-center">
      <video
        ref={videoRef}
        className="w-full h-full object-contain"
        playsInline
        muted
        autoPlay
      />

      <div className="absolute bottom-4 left-4 bg-black/50 px-2 py-1 rounded text-xs font-mono text-green-400 border border-green-900/50">
        LIVE FEED ●
      </div>
    </div>
  );
};
