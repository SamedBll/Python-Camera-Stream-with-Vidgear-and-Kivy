import cv2
from vidgear.gears import CamGear
from vidgear.gears import NetGear
from datetime import datetime

options_1 = {
    "CAP_PROP_FRAME_WIDTH": 1920, # resolution 320x240
    "CAP_PROP_FRAME_HEIGHT": 1080,
}

stream = CamGear(source=0, logging=False, **options_1).start() #loggingi kapatacaz


options = {"bidirectional_mode": True}

server = NetGear(
    address="192.168.0.14", 
    port="5454",
    protocol="tcp",
    pattern=1,
    logging=False,
    **options
)

while True:

    # read frames from stream
    frame = stream.read()
    now = datetime.now()
    zaman = now.strftime("%H%M%S%f")
    
    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # Show output window
    server.send(frame, message=zaman)


# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()
server.close()