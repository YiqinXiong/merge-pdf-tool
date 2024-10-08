# merge-pdf-tool
> A simple script to merge pdf and add filename page automatically.

## 动机
- 每张发票背面需要备注姓名、日期等信息
- 打印后发票乱作一团，还需要逐张核对再手写信息
- 手写的信息已经包含在提交到SVN的文件名了，再抄一遍=浪费生命

## 最佳实践

### 1. 准备工作
1. 根据系统不同，在[Release](https://github.com/YiqinXiong/merge-pdf-tool/releases) 或 [Gitee发行库](https://gitee.com/yiqin0411/merge-pdf-tool/releases)中下载对应的可执行文件
2. 各张发票已按照SVN中要求的格式命名

### 2. 合并PDF
1. 双击1.1中下载的可执行文件
2. 在弹出的资源管理器窗口中选择**需要合并的PDF文件**（可框选、多选）
3. 在新弹出的资源管理器窗口中选择**合并后输出的PDF文件路径和文件名**
4. 去输出路径查看合并后的PDF文件

### 3. 打印
1. 把合并后的PDF文件安渡到**办公内网**用于打印
2. 办公机上：
   1. 安渡下载合并后的PDF文件
   2. 右键-打开方式-数科OFD3.0
   3. 选择左上角打印（或快捷键Ctrl+P）
   4. 选择双面打印-长边装订，取消自动旋转
3. enjoy your life~

## 作者
熊逸钦
