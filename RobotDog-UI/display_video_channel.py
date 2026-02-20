import cv2
import numpy as np
import asyncio
import logging
import threading
import time
import json
from queue import Queue

from aiohttp import web
import aiohttp_cors

from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, MediaStreamTrack
from av import VideoFrame

from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod

logging.basicConfig(level=logging.INFO)

# Shared frame queue
frame_queue = Queue()
pcs = set()

# -------------------------------
# Video track for WebRTC
# -------------------------------
class Go2VideoTrack(VideoStreamTrack):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    async def recv(self):
        # Pull frame from queue (blocking in thread executor)
        frame = await asyncio.get_event_loop().run_in_executor(None, self.queue.get)
        vf = VideoFrame.from_ndarray(frame, format="bgr24")
        vf.pts, vf.time_base = self.next_timestamp()
        return vf

# -------------------------------
# Unitree WebRTC receiver thread
# -------------------------------
def start_unitree_receiver():
    conn = UnitreeWebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.123.161")

    async def recv_camera_stream(track: MediaStreamTrack):
        print("recv_camera_stream: started")
        while True:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            print("recv_camera_stream: got frame", img.shape)
            frame_queue.put(img)

    async def setup():
        await conn.connect()
        conn.video.switchVideoChannel(True)
        print("setup: connected, adding video callback")
        conn.video.add_track_callback(recv_camera_stream)

    loop = asyncio.new_event_loop()

    def run():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(setup())
        loop.run_forever()

    threading.Thread(target=run, daemon=True).start()

# -------------------------------
# OpenCV display thread
# -------------------------------
def opencv_thread():
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    while True:
        if not frame_queue.empty():
            img = frame_queue.get()
            print("opencv_thread: displaying frame", img.shape)
            cv2.imshow("Video", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.01)

    cv2.destroyAllWindows()

# -------------------------------
# WebRTC /offer endpoint
# -------------------------------
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # Handle data channel
    @pc.on("datachannel")
    def on_datachannel(channel):
        print("Data channel opened:", channel.label)

        @channel.on("message")
        def on_message(message):
            print("Received:", message)
            channel.send("pong")

    # Apply remote description
    await pc.setRemoteDescription(offer)

    # Add our robot video track
    pc.addTrack(Go2VideoTrack(frame_queue))

    # Create and send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
    )

# -------------------------------
# Main server setup
# -------------------------------
app = web.Application()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods=["POST", "GET", "OPTIONS"],
    )
})

resource = app.router.add_resource("/offer")
route = resource.add_route("POST", offer)
cors.add(route)

# -------------------------------
# Start everything
# -------------------------------
if __name__ == "__main__":
    start_unitree_receiver()
    threading.Thread(target=opencv_thread, daemon=True).start()
    web.run_app(app, port=8080)
