** xxmind  新版本已经出来了
xxmind是将xmind固定格式转为xls的转换工具。


使用说明：
1） 安装：
pip install xxmind
2） 执行
Python -c "from xxmind.main import  Main; Main()" 
3） 按模板xmind格式要求，编写用例
4） 运行工具，把xmind转化为xls、xlsx格式的文件

## 注： 为方便后期操作方便 
# 可以 把上面的 运行命令放到bat或shell文件中，下次直接双击运行 
#######################################################################
Last update time: 2018-11-13 
By： 8034.com

#######################################################################
0.3.5 修改了模板
0.4.0 支持了python3.7

#######################################################################
## 打包 检查
python setup.py check 
## 打包 生成
python setup.py sdist
## 上传
twine upload dist/*
## 使用
pip install xxmind 
## 更新
pip install --upgrade xxmind
## 卸载
pip uninstall -y xxmind 
#######################################################################
## MANIFEST.in 
include pat1 pat2 ...   #include all files matching any of the listed patterns
exclude pat1 pat2 ...   #exclude all files matching any of the listed patterns
recursive-include dir pat1 pat2 ...  #include all files under dir matching any of the listed patterns
recursive-exclude dir pat1 pat2 ... #exclude all files under dir matching any of the listed patterns
global-include pat1 pat2 ...    #include all files anywhere in the source tree matching — & any of the listed patterns
global-exclude pat1 pat2 ...    #exclude all files anywhere in the source tree matching — & any of the listed patterns
prune dir   #exclude all files under dir
graft dir   #include all files under dir
