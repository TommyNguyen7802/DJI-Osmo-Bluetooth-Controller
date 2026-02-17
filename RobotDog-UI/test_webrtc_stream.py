import asyncio
import json
import numpy as np
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame

import cv2
import threading
import time
from queue import Queue
import aiohttp_cors

# Global queue for frames
frame_queue = Queue()

pcs = set()

class TestVideoTrack(VideoStreamTrack):
    """
    A synthetic video track that generates moving color bars.
    """
    def __init__(self):
        super().__init__()
        self.counter = 0

    async def recv(self):
        print("recv called")
        pts, time_base = await self.next_timestamp()

        # Create a simple moving pattern
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        img[:, :, 0] = (self.counter % 255)
        img[:, :, 1] = ((self.counter * 2) % 255)
        img[:, :, 2] = ((self.counter * 3) % 255)
        self.counter += 1

        # Push frame to OpenCV thread
        frame_queue.put(img)

        # Convert to WebRTC frame
        frame = VideoFrame.from_ndarray(img, format="bgr24")
        frame.pts = pts
        frame.time_base = time_base
        return frame

# OpenCV preview thread
def opencv_thread():
    while True:
        if not frame_queue.empty():
            img = frame_queue.get()
            cv2.imshow("WebRTC Test Output", img)
            cv2.waitKey(1)
        else:
            time.sleep(0.01)

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # 1. Apply remote description first
    await pc.setRemoteDescription(offer)

    # 2. For each transceiver the browser offered, attach our track
    for t in pc.getTransceivers():
        if t.kind == "video":
            pc.addTrack(TestVideoTrack())

    # 3. Create and set answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
    )


app = web.Application()

# Enable CORS
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods=["POST", "GET", "OPTIONS"],
    )
})

# Register route ONCE, wrapped with CORS
resource = app.router.add_resource("/offer")
route = resource.add_route("POST", offer)
cors.add(route)



# Start OpenCV thread BEFORE running the server
threading.Thread(target=opencv_thread, daemon=True).start()

web.run_app(app, port=8080)

