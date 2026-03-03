# unitree_receiver.py
import cv2
import numpy as np
import zmq
import asyncio
import logging
import threading
import time
from queue import Queue
from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod
from aiortc import MediaStreamTrack

logging.basicConfig(level=logging.FATAL)

def main():
    frame_queue = Queue()

    # ZMQ PUSH setup
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.setsockopt(zmq.SNDHWM, 1)
    socket.setsockopt(zmq.LINGER, 0)
    socket.bind("tcp://127.0.0.1:5555")
    print("ZMQ PUSH bound on tcp://127.0.0.1:5555")

    conn = UnitreeWebRTCConnection(WebRTCConnectionMethod.LocalSTA, ip="192.168.123.161")

    async def recv_camera_stream(track: MediaStreamTrack):
        while True:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            frame_queue.put(img)

            ok, jpg = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ok:
                data = jpg.tobytes()
                try:
                    socket.send(data, zmq.NOBLOCK)
                    print("ZMQ SEND:", len(data), "bytes")
                except zmq.Again:
                    print("ZMQ DROP (no receiver ready)")

    def run_asyncio_loop(loop):
        asyncio.set_event_loop(loop)
        async def setup():
            try:
                await conn.connect()
                conn.video.switchVideoChannel(True)
                conn.video.add_track_callback(recv_camera_stream)
            except Exception as e:
                logging.error(f"Error in WebRTC connection: {e}")

        loop.run_until_complete(setup())
        loop.run_forever()

    loop = asyncio.new_event_loop()
    threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True).start()

    # OpenCV display
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    try:
        while True:
            if not frame_queue.empty():
                img = frame_queue.get()
                cv2.imshow("Video", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.01)
    finally:
        cv2.destroyAllWindows()
        loop.call_soon_threadsafe(loop.stop)

if __name__ == "__main__":
    main()
