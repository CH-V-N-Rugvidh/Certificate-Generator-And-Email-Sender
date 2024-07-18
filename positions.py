import cv2


class Positions:
    def __init__(self):
        self.x = 0
        self.y = 0

    def mouse_callback(self, event, x, y, _, __):  # flags, param
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y

    def position(self, image_path):
        # Load an image
        image = cv2.imread(image_path)

        # Create a window and set the mouse callback
        cv2.namedWindow("Select Position")
        cv2.setMouseCallback("Select Position", self.mouse_callback)  # NOQA

        # Display the image
        cv2.imshow("Select Position", image)

        # Wait for a key event
        cv2.waitKey(0)

        # Close the window
        cv2.destroyAllWindows()

        return self.x, self.y

    def get_certificate_id_pos(self, image_path):
        return self.position(image_path)

    def get_name_pos(self, image_path):
        return self.position(image_path)
