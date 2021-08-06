# 在 GPAW 中进行 GW/BSE 计算的简单教程

## dft

`Si_gs.py`: 硅的基态计算

`Si_bs.py`: 利用基态计算结果 (电子密度) 计算硅的能带结构

## gw

`C_gw.py`: 金刚石的 G0W0 计算. 4 进程计算大约 30 min.

`C_qpbs.py`: 基于上一步的 G0W0 计算作 KS (PBE) 和 QP 能带图.
由于能带由插值得到, 当 GW 计算的 k 点过于稀疏时, 插值很可能得到错误的结果.

## bse

`Si_bse.py`: 硅的 BSE 计算.
为了减少计算量, 平面波和响应函数截断能都取了比较小的值.
为获得更好的光谱计算结果, 除了需要增大基组截断能以外,
还需要增加 `kx` 以更好地采样 BZ 内的垂直激发.

