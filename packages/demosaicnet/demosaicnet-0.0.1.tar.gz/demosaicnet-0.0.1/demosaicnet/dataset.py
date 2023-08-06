"""Dataset loader for demosaicnet."""
import numpy as np
from skimage.io import imread
import torch as th

from .mosaic import bayer, xtrans


class DemosaicnetDataset(th.utils.data.Dataset):

    BAYER = "bayer"
    XTRANS = "xtrans"

    def __init__(self, listfile, download=False, mode=DemosaicnetDataset.BAYER):
        super(self, DemosaicnetDataset).__init__(self)

        self.root = os.path.dirname(listfile)
        if mode not in [DemosaicnetDataset.BAYER, DemosaicnetDataset.XTRANS]:
           raise ValueError("Dataset mode should be 'xtrans' or 'bayer', got %s"
                            % mode)
        self.mode = mode

        self.files = []
        with open(listfile, "r") as fid:
            for fname in fid.readlines():
                self.files.append(fname.strip())

    def __len__(self):
        pass

    def __getitem__(self, idx):
        fname = self.files[idx]
        im = imread(fname).astype(np.float32) / (2**8-1)

        if self.mode == DemosaicnetDataset.BAYER:
            mosaic = bayer(im)
        else:
            mosaic = bayer(im)
