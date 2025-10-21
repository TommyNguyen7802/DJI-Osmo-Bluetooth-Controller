# dji_handlers.py

def dispatch_handler(cmd_set, cmd_id, payload):
    if cmd_set == 0x1D and cmd_id == 0x02:
        handle_camera_status_push(payload)
    elif cmd_set == 0x1D and cmd_id == 0x03:
        handle_record_control_response(payload)
    elif cmd_set == 0x1D and cmd_id == 0x06:
        handle_new_camera_status_push(payload)
    elif cmd_set == 0x00 and cmd_id == 0x19:
        handle_connection_response(payload)
    else:
        print(f"⚠️ Unknown command: cmd_set=0x{cmd_set:02X}, cmd_id=0x{cmd_id:02X}")


def handle_camera_status_push(payload):
    # Parse and print fields from camera_status_push_command_frame
    print("📡 Camera status push received")
    # TODO: unpack fields and log them

def handle_new_camera_status_push(payload):
    print("📡 New camera status push received")
    # TODO: unpack and print mode name, parameters

def handle_connection_response(payload):
    print("🔐 Connection response received")
    # TODO: unpack ret_code and device_id

def handle_record_control_response(payload):
    if len(payload) < 1:
        print("❌ Invalid record control response length")
        return
    ret_code = payload[0]
    if ret_code == 0:
        print("🎥 Record command acknowledged: SUCCESS")
    else:
        print(f"⚠️ Record command failed with ret_code={ret_code}")

