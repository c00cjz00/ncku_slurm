
## 工作派送排程範例
1. 建立檔案工作派送排程範例
> ~/myslurm/slurm_demo01.ipynb

2. 將 SLURM 寫成 FUNCTION
指令文件 https://man.twcc.ai/@Ldk_QYrOR2yo3m8Cb1549A/rkegDKslF
```
# https://man.twcc.ai/@Ldk_QYrOR2yo3m8Cb1549A/rkegDKslF
def SLURM(cmd):
    ## SLURM 內容, 請修改 ---> Email
    SLURM='''#!/work/c00cjz002/binary/bash5.0/bin/bash
#SBATCH -A MST109178              # 計畫代號
#SBATCH -J ngs192g                # 工作代號 (標籤, 可自行定義)
#SBATCH -p ngs192g                # 工作區塊 
#SBATCH -c 56                     # 使用的CPU核心數
##SBATCH --mem=184g               # 使用的記憶體容量 (不設定自動給予ram 10g)
#SBATCH --mail-user=summerhill001@gmail.com    # 請修改為您的信向
#SBATCH --mail-type=BEGIN,END                  # 指定送出email時機 可為NONE, BEGIN, END, FAIL, REQUEUE, ALL
#SBATCH -o log/%j.logi            # 執行記錄檔案儲存於log目錄底下
'''
    myCmd = SLURM + cmd
    
    ## 儲存上述內容 SLURM.sh
    import time
    slurm_shell = 'slurm/'+time.strftime("%Y-%m-%d_%H-%M-%S")+'.sh'
    
    f = open(slurm_shell, "w")
    f.write(myCmd)
    f.close()    

    ## 執行SLURM
    #!sbatch SLURM.sh
    jobID=(subprocess.check_output('sbatch '+slurm_shell+' |awk \'{print $4}\'', shell=True,text=True))
    return jobID

## 建立目錄
import subprocess
!mkdir -p slurm
!mkdir -p log
```

3. 撰寫工作內容 
- 指令集
```
cmd='''
ml libs/singularity/3.7.1
export MAGPURIFYDB=${HOME}/MAGpurify-db-v1.0
singularity exec \
    /work/c00cjz002/nvidia/magpurify_v2.1.2.sif \
    bash -c "magpurify -h && \
    date && \
    pwd && \
    sleep 60"  
'''
```

- 指令集
```
cmd='''
ml libs/singularity/3.7.1
export MAGPURIFYDB=${HOME}/MAGpurify-db-v1.0
singularity exec \
    /work/c00cjz002/nvidia/magpurify_v2.1.2.sif \
    bash -c "magpurify \
    phylo-markers ${HOME}/u3884690/rgi_results/bin_metabat/FS2_CheckM/bins/FS2_bin.1/genes.fna \
    ${HOME}/u3884690/rgi_results/bin_metabat/FS2_bin1_Magpurify \
    --db MAGpurify-db-v1.0 \
    --threads 42"  
'''
```

4. 派送工作到計算節點, 並印出工作ID
```
## 送出工作到計算節點電腦
jobID = SLURM(cmd)
print(jobID.strip())
```

5. 觀看執行狀況
```
## 觀看執行狀況
!squeue -u `whoami` | grep "$jobID\|JOBID" 
```

6.  刪除JOB
```
## 刪除JOB
!scancel $jobID
```

7. 全部JOB刪除
```
## 全部JOB刪除
!squeue -u `whoami` | grep -v JOBID  | awk '{print $1}' | xargs scancel  # 列出 PID 並砍掉 Process
```
