import os

SMPL_DATA_PATH = "models/smpl/"

SMPL_KINTREE_PATH = os.path.join(SMPL_DATA_PATH, "kintree_table.pkl")
SMPL_MODEL_PATH = os.path.join(SMPL_DATA_PATH, "SMPL_NEUTRAL.pkl")

JOINT_REGRESSOR_TRAIN_EXTRA = os.path.join(SMPL_DATA_PATH, 'J_regressor_extra.npy')
MAE_MODEL_PATH = os.path.join('/fsx/sernamlim/xiaoliu/models', 'mae_visualize_vit_large_ganloss.pth')

SMPLFACES_PATH = os.path.join(SMPL_DATA_PATH, 'smplfaces.npy')
UESTC_PATH = "/datasets01/UESTC/uestc/"
Pretrained1200_PATH = os.path.join(SMPL_DATA_PATH, "checkpoint_1200.pth.tar")
Pretrained1000_PATH = os.path.join(SMPL_DATA_PATH, "checkpoint_1000.pth.tar")




