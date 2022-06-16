## 开发环境配置

## 生产环境配置
linux 环境
###1.导出开发环境的配置
        pip install pipreqs
        pipreqs . --encoding=utf8 --force
        生成 requirements.txt
###2.部署到生产环境
        python -m venv env
        source env/bin/activate
        pip install -r requirements.txt
        python MainApplication.py   
