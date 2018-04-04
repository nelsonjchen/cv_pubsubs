import unittest as ut
import cv_pubsubs.webcam_pub as w
from cv_pubsubs.window_sub import frame_dict, sub_win_loop

def subscribe_to_key_command(cam_id,  # type: Union[int, str]
                         frame_handler,  # type: Callable[[int, np.ndarray], Any]
                         request_size=(1280, 720),  # type: Tuple[int, int]
                         high_speed=False,  # type: bool
                         fps_limit=240  # type: float
                         ):  # type: (...) -> threading.Thread
    t = threading.Thread(target=frame_handler_loop, args=(cam_id, frame_handler, request_size, high_speed, fps_limit))
    t.start()
    return t

class TestSubWin(ut.TestCase):

    def test_sub(self):
        def cam_handler(frame, cam_id):
            frame_dict[str(cam_id) + "Frame"] = (frame, frame)

        t = w.frame_handler_thread(0, cam_handler,
                                   request_size=(1280, 720),
                                   high_speed=True,
                                   fps_limit=240
                                   )

        sub_win_loop(names=['cammy', 'cammy2'],
                     input_vid_global_names=[str(0) + "Frame"])

        w.CamCtrl.stop_cam(0)

        t.join()
