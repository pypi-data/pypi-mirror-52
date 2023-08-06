import cv2


__all__ = ["Drawer"]


class Drawer:
    def __init__(self):
        self.colors = {
            "red": (0, 0, 255),
            "green": (0, 255, 0),
            "blue": (255, 0, 0),
            "white": (255, 255, 255),
            "black": (0, 0, 0)
        }

    def draw_rectangle(self, image, tlbr, color="green"):
        tlbr = [int(x) for x in tlbr]
        cv2.rectangle(image, (tlbr[1], tlbr[0]), (tlbr[3], tlbr[2]), self.colors[color], -1)
        return image

    def draw_landmarks(self, image, landmarks, radius=1, color="green"):
        for p in landmarks:
            p1, p2 = int(p[0]), int(p[1])
            cv2.circle(image, (p1, p2), radius, self.colors[color], -1)
        return image
