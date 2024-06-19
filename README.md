# Compiler-theory
基于Python、Jupyter和Tkinter的编译原理技术的实现。包括词法分析（Token序列的识别），消除左递归的First集、Follow集、Select集求解、LL(1)文法判断等。进行了可视化图形界面操作。
发现代码有问题的话，欢迎联系我。邮箱：2106397770@qq.com

# 词法分析
实验使用Jupyter Notebook实现

in.txt和out.txt分别为输入文件和输出文件
in.txt存放待识别的token序列
out.txt存放识别结果

其中in.txt前半部分为堆排序代码
后半部分为一些特殊的合法的和非法的测试用例

# First集合计算
实验使用Python3实现，并应用tkinter实现了可视化操作。

通过设计一个FIRST集合计算器，帮助理解FIRST集合的计算方法。FIRST集合是语法分析中的重要概念，掌握其计算对后续的语法分析有重要意义。
FIRST集合的求解解决了左递归问题。

# LL(1)文法判断
实验使用Python3实现，并应用tkinter实现了可视化操作。

通过设计一个FOLLOW集合、SELECT集合计算器、LL(1)文法判断和冲突求解，帮助理解FOLLOW集合、SELECT集合计算、LL(1)文法判断和冲突求解计算方法。FOLLOW集合、SELECT集、LL(1)文法判断和冲突求解是语法分析中的重要概念，掌握其计算对后续的语法分析有重要意义。
