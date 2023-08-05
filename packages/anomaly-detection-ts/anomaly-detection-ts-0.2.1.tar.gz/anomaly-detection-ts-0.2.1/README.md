# Anomaly Detection SDK

## 安装
```bash
git clone http://deployer:SU42HVeK@git.internal/mo/anomaly-detection.git
cd anomaly-detection
python setup.py bdist_egg
python setup.py install
```

## 文档
Linux/macOS 用户通过以下方式生成文档：
```bash
cd docs
make html
```

Windows 用户通过以下方式生成文档：
```powershell
cd docs
meke.bat html
```

## 算法简介
### 异常类型
- 超出固定的波动范围
- 暴涨暴跌
- 均值漂移
- 异常频率

### 算法简介 [^1]
[^1]: 带 * 的算法尚未提供。

检测分为**序列处理**和**异常检测**两个阶段。先对时间序列进行一些处理（分解、预测等），从而得到新的序列，然后检测新序列中的异常。也可以跳过序列处理，直接检测序列中的异常。

![image](./res/algorithms.png)

序列处理算法包括：
- **DIRECT**：不作任何处理，后续直接调用异常检测算法检测原序列中的异常。

- **STL**：适用于周期性序列，使用 STL (Seasonal and Trend decomposition using Loess) 方法将时间序列分解为季节、趋势和残差, 后续调用异常检测算法检测残差中的异常。

- **FFT**：适用于周期性序列，先用快速傅里叶变换将原数据从时域转换到频域, 滤掉低频信号, 再将高频信号转换回时域, 后续调用异常检测算法检测高频信号中的异常。

- **DWT**：适用于周期性序列，先用离散小波变换将原数据从时域转换到频域, 滤掉低频分量, 再将高频分量转换回时域, 后续调用异常检测算法检测高频信号中的异常。

- **Holt-Winters**：适用于周期性序列，使用历史序列训练 Holt-Winters 模型，以之预测新的序列，将预测值与真实值作差，后续调用异常检测算法检测偏差序列中的异常。

异常检测算法包括：

- **固定阈值检测法**：凡是超出设定的阈值（上界或下界）的值均被判定为异常。

- **k-sigma 检测法**：凡是偏离均值超过 $k$ 个 $\sigma$ 的值均被判定为异常。

- **k-IQR 检测法**：凡是偏离上/下四分位数超过 $k$ 倍四分位间隔（interquartile range, IQR）的值均被判定为异常。相比于均值和标准差，分位数受异常值的影响较小，故此方法比 k-sigma 检测法稳定。

- **Grubbs 检测法**：基于 Grubbs 检验，原假设是数据中没有异常值，备择假设是数据中有一个异常值。只能用来检测一组数据中的最大/最小值是否是异常值，应用范围较窄。

- **Tietjen-Moore 检测法**：基于 Tietjen-Moore 检验，原假设是数据中没有异常值，备择假设是数据中有 $k$ 个异常值。必需指定 $k$，若数据中的异常值数量少于 $k$，此方法无法检测出异常，因此应用范围较窄。

- **GESD 检测法**：基于 generalized ESD (extreme Studentized deviate) 检验，原假设是数据中没有异常值，备择假设是数据中有多达 $r$ 个异常值。必需指定 $r$，若数据中的异常值数量少于 $r$，此方法也能够检测出来，因此应用范围较广。

- **CUSUM 检测法**：通过累积和检测序列是否发生均值漂移。