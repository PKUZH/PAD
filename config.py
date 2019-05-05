"""
configure file for Traditional Catalog Making.

"""
class Config(object):
  def __init__(self):
    # 1. picker params
    self.pick_win    = [10., 1.]  # pick win for STA/LTA
    self.trig_thres  = 15.        # threshold to trig picker (by energy)
    self.pick_thres  = 0.96       # threshold for picking
    self.p_win       = 2.         # win len for P picking
    self.s_win       = 15.        # win len for S picking
    self.pca_win     = 1.         # win len for PCA filter
    self.s_stride    = 0.05       # time stride for picking S
    self.amp_win     = 5.         # time win to get S amplitude
    self.det_gap     = 5.         # time gap between detections
    # 2. assoc params
    self.ot_dev      = 3.         # win len for assoc picks
    self.assoc_num   = 4          # num of stations to assoc
    # 3. loc params
    self.side_width  = 0.2        # ratio of sides relative to sta range
    self.xy_grid     = 0.05       # lateral grid width, in degree
    self.resp_dict   = {'ZSY': 3.02e8,
                         'YN': 1.67785e9,
                        'XLS': 1/1.6e-9}     # instrumental response (cnt/m/s)

