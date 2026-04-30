# webrtc_server.py
import asyncio
import json
from aiohttp import web
import aiohttp_cors
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
import time
import zmq
import numpy as np
import cv2
import threading
from collections import deque

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect("tcp://192.168.0.2:5555")
print("ZMQ PULL connected to tcp://192.168.0.2:5555")

# simple frame buffer
frame_buffer = deque(maxlen=1)

def zmq_reader():
    while True:
        jpg_bytes = socket.recv()
        img = cv2.imdecode(np.frombuffer(jpg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            frame_buffer.append(img)

threading.Thread(target=zmq_reader, daemon=True).start()

pcs = set()

class Go2VideoTrack(VideoStreamTrack):
    async def recv(self):
        # wait until we have at least one frame
        while not frame_buffer:
            await asyncio.sleep(0.01)

        frame = frame_buffer[-1]  # latest frame

        ts, tb = await self.next_timestamp()
        vf = VideoFrame.from_ndarray(frame, format="bgr24")
        vf.pts, vf.time_base = ts, tb
        return vf

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        print("Data channel opened:", channel.label)

        @channel.on("message")
        def on_message(message):
            print("Received:", message)
            channel.send("pong")

    await pc.setRemoteDescription(offer)

    pc.addTrack(Go2VideoTrack())

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

web.run_app(app, port=8080)
