conda config --add channels https://mirrors.sjtug.sjtu.edu.cn/anaconda/pkgs/free/;
conda config --add channels https://mirrors.sjtug.sjtu.edu.cn/anaconda/pkgs/main/;
conda config --set show_channel_urls yes;
conda create -n stock python=3
