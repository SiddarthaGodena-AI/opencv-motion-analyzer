import numpy as np
from motion import analyze_frames
def test_static():
    frames=[np.zeros((100,100,3),np.uint8) for _ in range(4)]
    assert analyze_frames(frames)=={"frames":4,"moving_frames":0,"motion_events":0}
def test_motion_event():
    blank=np.zeros((100,100,3),np.uint8)
    box=blank.copy()
    box[20:70,20:70]=255
    result=analyze_frames([blank,box,box,box],min_area=100)
    assert result["motion_events"]==1 and result["moving_frames"]==1
def test_empty():
    assert analyze_frames([])["frames"]==0

