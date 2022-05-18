#!/bin/bash


#SBATCH --gres=gpu:a100:8
#SBATCH --output=slurm_uestc_alpha05.out


srun python -m torch.distributed.launch --nproc_per_node=8 --nnodes=1 --master_addr=127.0.3.5 --master_port=29535 -m src.train.train_cvae --modelname cvae_transformer_rc_rcxyz_kl --pose_rep rot6d --lambda_kl 1e-5 --jointstype vertices --batch_size 800 --num_frames 60 --num_layers 8 --lr 0.0001 --glob --no-vertstrans --dataset uestc --num_epochs 2000 --snapshot 100 --folder exps_uestc_alpha05/uestc


