while :
do
    gdrive list -q "'1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh' in parents" --no-header --max 0 | cut -d" " -f1 - | xargs -L 1 gdrive delete
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/main/Compositional_Motion_UESTC/slurm_actor_uestc.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_alphauniform/Compositional_Motion_UESTC/slurm_human12_alpha_uniform.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_nomask/Compositional_Motion_UESTC/slurm_uestc_nomask.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_alpha05/Compositional_Motion_UESTC/slurm_uestc_alpha05.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_mae96/Compositional_Motion_UESTC/slurm_uestc_pretrain1000_mae_96_01.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_mae96/Compositional_Motion_UESTC/slurm_uestc_pretrain1000_mae_96_001.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_mae96/Compositional_Motion_UESTC/slurm_uestc_pretrain1200_mae_96_01.out
    gdrive upload --parent 1u_5fuUZ8r1Upffb68Mfmivgw7sWXlSQh /fsx/sernamlim/xiaoliu/Compositional_Motion_UESTC/uestc_mae96/Compositional_Motion_UESTC/slurm_uestc_pretrain1200_mae_96_001.out
    echo "Sleeping for 120"
    sleep "120"
done
