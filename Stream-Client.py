from vidgear.gears import NetGear
import cv2

# activate Bidirectional mode
options = {"bidirectional_mode": True}

# Define NetGear Client at given IP address and define parameters 
# !!! change following IP address '192.168.x.xxx' with yours !!!
client = NetGear(
    address="192.168.0.14",
    port="5454",
    protocol="tcp",
    pattern=1,
    receive_mode=True,
    logging=True,
    **options
)

# loop over
while True:

    # receive data from server and also send our data
    data = client.recv()

    # extract server_data & frame from data
    server_data, frame = data

    # again check for frame if None
    if frame is None:
        break

    # {do something with the extracted frame and data here}

    # lets print received server data
    if not (server_data is None):
        print(server_data)

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close client
client.close()
