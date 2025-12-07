# dji_handlers.py
import struct

def dispatch_handler(cmd_set, cmd_id, payload):
    if cmd_set == 0x1D and cmd_id == 0x05:
        print("Status subscription command acknowledged (no response expected)")
        return
    if cmd_set == 0x1D and cmd_id == 0x02:
        handle_camera_status_push(payload)
    elif cmd_set == 0x1D and cmd_id == 0x03:
        handle_record_control_response(payload)
    elif cmd_set == 0x1D and cmd_id == 0x06:
        handle_new_camera_status_push(payload)
    elif cmd_set == 0x00 and cmd_id == 0x19:
        handle_connection_response(payload)
    else:
        print(f"Unknown command: cmd_set=0x{cmd_set:02X}, cmd_id=0x{cmd_id:02X}")


def handle_camera_status_push(payload):
    # Parse and print fields from camera_status_push_command_frame
    print("Camera status push received")
    # TODO: unpack fields and log them
    if len(payload) < 48:
        print("Invalid camera status push length")
        return

    fields = struct.unpack("<BBBBBHBBHHHIIBBBBIBH", payload[:48])
    print("Camera Status Push:")
    print(f"  Mode: {fields[0]}")
    print(f"  Status: {fields[1]}")
    print(f"  Resolution: {fields[2]}")
    print(f"  FPS Index: {fields[3]}")
    print(f"  EIS Mode: {fields[4]}")
    print(f"  Record Time: {fields[5]}s")
    print(f"  Photo Ratio: {fields[7]}")
    print(f"  Battery: {fields[-1]}%")

def handle_new_camera_status_push(payload):
    print("New camera status push received")
    # TODO: unpack and print mode name, parameters
    if len(payload) < 44:
        print("Invalid new camera status push length")
        return

    mode_type, name_len = struct.unpack_from("<BB", payload, 0)
    mode_name = payload[2:22].decode("ascii", errors="ignore").strip("\x00")

    param_type, param_len = struct.unpack_from("<BB", payload, 22)
    mode_param = payload[24:44].decode("ascii", errors="ignore").strip("\x00")

    print("New Camera Status Push:")
    print(f"  Mode Name Type: {mode_type}")
    print(f"  Mode Name: {mode_name}")
    print(f"  Param Type: {param_type}")
    print(f"  Mode Param: {mode_param}")

def handle_connection_response(payload):
  # print("")
    return
    # TODO: unpack ret_code and device_id

def handle_record_control_response(payload):
    if len(payload) < 1:
        print("Invalid record control response length")
        return
    ret_code = payload[0]
    if ret_code == 0:
        print("Record command acknowledged: SUCCESS")
    else:
        print(f"Record command failed with ret_code={ret_code}")

