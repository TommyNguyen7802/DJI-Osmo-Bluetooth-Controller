#!/usr/bin/env python3

import asyncio
import logging
from time import sleep

from uhubctl import disable_hub, enable_hub
from transfer_video import transfer_new_videos

from dji_ble import DJIBLE
from dji_commands import build_connection_request
from dji_protocol import build_frame, next_seq
from dji_ble import DJIBLE
from dji_actions import (
    start_recording,
    stop_recording,
    switch_mode_video,
    switch_mode_photo,
)
from unitree_webrtc_connect.webrtc_driver import UnitreeWebRTCConnection, WebRTCConnectionMethod
from unitree_webrtc_connect.constants import RTC_TOPIC, SPORT_CMD
from pydantic import BaseModel


# -------------------------
# FastAPI server
# -------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ble_global = None
device_id_global = None
unitree_conn = None


@app.post("/camera/setup")
async def api_setup():
    if ble_global != None:
        return
    await setup()
    return {"status": "started"}


@app.post("/camera/shutdown")
async def api_shutdown():
    if ble_global == None:
        return
    await shutdown()
    return {"status": "stopped"}


@app.post("/camera/start")
async def api_start():
    if ble_global == None:
        return
    await start_recording(ble_global, device_id_global)
    return {"status": "started"}


@app.post("/camera/stop")
async def api_stop():
    if ble_global == None:
        return
    await stop_recording(ble_global, device_id_global)
    return {"status": "stopped"}


@app.post("/camera/video")
async def api_video():
    if ble_global == None:
        return
    await switch_mode_video(ble_global, device_id_global)
    return {"status": "video_mode"}


@app.post("/camera/photo")
async def api_photo():
    if ble_global == None:
        return
    await switch_mode_photo(ble_global, device_id_global)
    return {"status": "photo_mode"}


@app.post("/camera/transfer")
async def api_transfer():
    # Re-enable USB hubs
    enable_hub()

    transfer_attempts = 4
    transfer_delay_time = 6
    transfer_buffer = 1

    for i in range(transfer_attempts):
        try:
            print("\nAttempting file transfer...")
            await asyncio.sleep(transfer_delay_time)
            transfer_new_videos()
            await asyncio.sleep(transfer_buffer)
            break
        except FileNotFoundError:
            print(f"attempt {i+1} of {transfer_attempts}...")
        except PermissionError:
            print(f"attempt {i+1} of {transfer_attempts}...")
        except Exception as e:
            print(f"Error: {e}. attempt {i+1} of {transfer_attempts}...")

    # Disable hubs again
    disable_hub()

    return {"status": "transfer_complete"}


# -------------------------
# BLE + Camera Setup
# -------------------------
async def setup_ble():
    disable_hub()

    ble = DJIBLE()
    connect_attempts = 3

    for i in range(connect_attempts):
        try:
            await ble.connect()
            break
        except TimeoutError:
            print("Connection attempt timed out.")
            await asyncio.sleep(1)
            if i == connect_attempts - 1:
                print("Exiting...")
                return None
        except Exception as e:
            if str(e) == "Camera not found":
                print("Camera not found, retrying...")
                await asyncio.sleep(1)
                if i == connect_attempts - 1:
                    print("Exiting...")
                    return None
            else:
                raise

    device_id = 0x12345678
    mac = [0x04, 0xA8, 0x5A, 0x67, 0x90, 0x7B]
    fw_version = 0x01020304
    verify_mode = 0
    verify_data = 0x0000

    payload = build_connection_request(
        device_id, mac, fw_version, verify_mode, verify_data
    )
    frame = build_frame(0x00, 0x19, 0x00, payload, next_seq())
    await ble.write(frame)

    await asyncio.sleep(0.5)

    return ble, device_id


async def setup():
    global ble_global, device_id_global

    result = await setup_ble()
    if result is None:
        return

    ble, device_id = result
    ble_global = ble
    device_id_global = device_id

    print("BLE camera connected.")


async def shutdown():
    global ble_global, device_id_global

    try:
        await ble_global.disconnect()
    except (EOFError, AttributeError):
        pass

    ble_global = None
    device_id_global = None

    enable_hub()
    sleep(1)

# -------------------------
# Motion Control Setup
# -------------------------
async def setup_unitree():
    global unitree_conn

    unitree_conn = UnitreeWebRTCConnection(
        WebRTCConnectionMethod.LocalSTA,
        ip="192.168.123.161"
    )

    await unitree_conn.connect()
    await unitree_conn.datachannel.pub_sub.publish_request_new(
            RTC_TOPIC["MOTION_SWITCHER"],
            {"api_id": 1002, "parameter": {"name": "normal"}}
        )

    print("Motion mode enabled.")

    print("Unitree motion channel ready.")

class VelCmd(BaseModel):
    vx: float
    vy: float
    yaw: float

@app.post("/dog/stand")
async def dog_stand():
    await unitree_conn.datachannel.pub_sub.publish_request_new(
    RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["StandUp"]}
)
    await asyncio.sleep(5)

    await unitree_conn.datachannel.pub_sub.publish_request_new(
    RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["BalanceStand"]}
)
    
    return {"status": "standing"}

@app.post("/dog/damp")
async def dog_damp():
    await unitree_conn.datachannel.pub_sub.publish_request_new(
        RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["StopMove"]}
    )

    await unitree_conn.datachannel.pub_sub.publish_request_new(
        RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["StandDown"]}
    )

    await asyncio.sleep(5)

    await unitree_conn.datachannel.pub_sub.publish_request_new(
        RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["Damp"]}
    )

    return {"status": "damped"}


@app.post("/dog/vel")
async def dog_vel(cmd: VelCmd):
    await unitree_conn.datachannel.pub_sub.publish_request_new(
        RTC_TOPIC["SPORT_MOD"],
        {
            "api_id": SPORT_CMD["Move"],
            "parameter": {"x": cmd.vx, "y": cmd.vy, "z": cmd.yaw}
        }
        
    )
    print("VEL:", cmd.vx, cmd.vy, cmd.yaw)

    return {"status": "ok"}

@app.post("/dog/sit")
async def dog_sit():
    await unitree_conn.datachannel.pub_sub.publish_request_new(
        RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["Sit"]}
    )

    await asyncio.sleep(3)

    return {"status": "sitting"}

@app.post("/dog/wave")
async def dog_wave():
    await unitree_conn.datachannel.pub_sub.publish_request_new(
        RTC_TOPIC["SPORT_MOD"],
    {"api_id": SPORT_CMD["Hello"]}
    )

    await asyncio.sleep(1)

    return {"status": "waving"}



# -------------------------
# Main entry point
# -------------------------
async def main():
    print("FastAPI server starting...")

    # Start BLE camera setup (non-blocking)
    asyncio.create_task(setup())

    # Start Unitree WebRTC setup (non-blocking)
    asyncio.create_task(setup_unitree())

    # Start FastAPI server
    config = uvicorn.Config(app, host="0.0.0.0", port=8010, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

    print("goodbye!")
    # Cleanup on exit
    await shutdown()



if __name__ == "__main__":
    asyncio.run(main())
