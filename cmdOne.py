# EXAMPLE: python cmdOne.py ${HOME}/freesurfer/demo/ /work/c00cjz002/data/Powei20211109/02322379.img

def SLURM(cmd):
    ## SLURM 內容, 請修改 ---> Email
    SLURM='''#!/work/c00cjz002/binary/bash5.0/bin/bash
#SBATCH -A GOV110079        # 計畫代號
#SBATCH -J CPU_T3_C2        # 工作代號 (標籤, 可自行定義)
#SBATCH -p ct56             # 工作區塊 
#SBATCH -c 3                # 使用的CPU核心數
##SBATCH --mem=12g           # 使用的記憶體容量 (不設定自動給予ram 10g)
#SBATCH --mail-user=summerhill001@gmail.com    # 請修改為您的信向
#SBATCH --mail-type=BEGIN,END                  # 指定送出email時機 可為NONE, BEGIN, END, FAIL, REQUEUE, ALL
#SBATCH -o log/%j.logi      # 執行記錄檔案儲存於log目錄底下
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

def createCMD(SUBJECTS_DIR, inputFile, saveFolder):
    cmd='''
# -> 啟動 jupyter
##~/.nchc_jupyter/startifdown_jupyterlab.sh >> ~/jupyter.log 

# -> 環境變數 1
export FREESURFER_HOME=/work/c00cjz002/package/freesurfer711
source $FREESURFER_HOME/SetUpFreeSurfer.sh

# -> 環境變數 2 (請自行修改)
SUBJECTS_DIR='''+ SUBJECTS_DIR +''' 
inputFile='''+ inputFile +''' 
saveFolder='''+ saveFolder +''' 

# -> 切換目錄
export SUBJECTS_DIR='''+ SUBJECTS_DIR +''' 
mkdir -p $SUBJECTS_DIR
cd $SUBJECTS_DIR

# -> 執行程式 1 (recon-all )
echo "STEP01"
recon-all -s $saveFolder -i $inputFile -all -qcache -parallel -openmp 3
'''
    return cmd

## 建立目錄
import subprocess
subprocess.run(["mkdir", "-p", "slurm"])
subprocess.run(["mkdir", "-p", "log"])

## 指令集
import os
import sys
SUBJECTS_DIR=sys.argv[1]
inputFile=sys.argv[2]
saveFolder=os.path.splitext(os.path.basename(inputFile))[0]
cmd=createCMD(SUBJECTS_DIR, inputFile, saveFolder)
#print(cmd)

## 送出工作到計算節點電腦
jobID = SLURM(cmd)
print(jobID.strip())