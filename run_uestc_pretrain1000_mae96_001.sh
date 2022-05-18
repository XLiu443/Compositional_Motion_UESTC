#!/bin/bash


#SBATCH --gres=gpu:a100:8
#SBATCH --output=slurm_uestc_pretrain1000_mae_96_001.out

module load anaconda
conda activate myactor

srun python -m torch.distributed.launch --nproc_per_node=8 --nnodes=1 --master_addr=127.0.3.2 --master_port=29532 -m src.train.train_cvae --modelname cvae_transformer_rc_rcxyz_kl_mae --pose_rep rot6d --lambda_kl 1e-5 --lambda_mae 0.01 --jointstype vertices --batch_size 160 --num_frames 60 --num_layers 8 --lr 0.0001 --glob --no-vertstrans --dataset uestc --num_epochs 500 --snapshot 100 --folder exps_uestc_pretrain1000_mae_96_001/uestc --resume2


