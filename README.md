# Graduation-Project
毕业设计项目-基于Python和JoinQuant平台的选股模型构建与设计

# 项目说明：
## 各部分链接：
论文：[链接]()；数据集：[链接]()；源代码：[链接]()；相关资料（开题报告等）：[链接]()

## 写在前面：
	由于疏忽，做成了太偏金融的设计了，之后会加入tensorflow等。
	在写说明文档的时候发现还有一些业务可以优化。
	可查看个人github仓库：https://github.com/jklf5
	个人博客：https://jklf5.xyz/（陆续完善中）
	建议使用Anaconda环境，及Spyder代码编辑器或者VSCODE编辑器
	金融预备知识：
		基本面分析
		对数收益率
		资本资产投资模型（CAPM）
		正态性检验（偏度和峰度）
		直方图的作用
		现代投资组合理论（MPT）
			夏普比率
			最小方差
		JoinQuant平台
## 代码结构：
	1_CAPM.py:使用资本资产定价模型（CAPM）筛选股票
	2_skews_kurts.py:使用正态性检验历史交易数据并筛选股票
	3_all_safe_hist.py:统计所有筛选后股票（安全的股票）的对数收益率的直方图和收益总和条形图
	4_all_safe_log_rets.py:统计所有筛选后股票（安全的股票）和000001.ss（上证指数）的对比图
	5_protfolio_sharpe_ratio.py:使用夏普比率作为指标构建等权重双资产投资组合，找最大夏普比率
	6_protfolio_std.py:使用方差作为指标构建等权重双资产投资组合，找最小方差
	functionClass.py:一些常用的函数
		函数如下：
		log_rets:求差分
		merge_SHci:合并股票数据
		plot_polyfit:绘制拟合线
		plot_text:绘制给定坐标的文本标签
		find_not_safe:找出不安全的股票
		count_save_not_safe:计数并保存不安全的股票
		find_not_safe_skews_kurts:找出偏度和峰度过于离群的股票
		open_not_safe_txt:读取不安全股票文件
		write_not_safe_txt:向不安全股票文件写入
		delete_not_safe:删除股票列表中不安全的股票
		mimic_seaborn:模仿seaborn风格
	fundamental_analysis.py:公司基本面分析筛选股票
	infoClass.py:保存公司基本面分析筛选后剩余的股票于STOCKS变量中
	not_safe.txt:保存金融技术分析筛选出的不安全股票，也会统计出现的次数（但不会自动清空）
	stocks_fundamental.xlsx:公司基本面数据集（详情见数据集文件夹下“数据集说明.txt”）
	JoinQuant平台回测代码.txt:JoinQuant平台回测代码，将代码放入JoinQuant平台的策略中使用
## 使用说明：
	按照序号使用
	infoClass运行的时候会自动调用fundamental_analysis中的基本面分析函数
	1-6文件中均import了infoClass，因此运行1-6，都会分析一次基本面
	使用1_CAPM.py可以得到经过资本资产定价模型运用后的散点图，并在IDE的输出框中显示需要筛序掉的股票，要筛选掉的股票也会保存到not_safe.txt中
	使用2_skews_kurts.py可以得到经过正态性检验后的散点图，并在IDE的输出框中显示需要筛选掉的股票，要筛选掉的股票也会保存到not_safe.txt中
	使用3_all_safe_hist.py可以得到经过基本面筛选和金融技术筛选后剩下的各股票的对数收益率的直方图以及股票收益总和的条形图
	使用4_all_safe_log_rets.py可以得到经过筛选后的股票和000001.ss（上证指数）对比的折线图
	使用5_protfolio_sharpe_ratio.py可以得到使用夏普比率构建的等权重双资产投资组合的热图及tensorflow运行后选出的最大夏普比率组合
	使用6_protfolio_std.py可以得到使用方差构建的等权重双资产投资组合的热图及tensorflow运行后选出的最小方差组合
	代码中出现的start及end可以调整历史交易数据获取的时间区间
## 注意：
	functionClass中某些函数可能对于既定情况有用，不一定普遍适用。
	代码中多处已注释。
## 参考书目：
	量化投资 以Python为工具 蔡立耑 电子工业出版社
	Python数据分析实战 伊凡·伊德里斯(Ivan Idris) 机械工业出版社
	Python金融衍生品大数据分析 伊夫·希尔皮斯科(Yves Hilpisch) 电子工业出版社
	Python金融大数据分析 伊夫·希尔皮斯科(Yves Hilpisch) 人民邮电出版社