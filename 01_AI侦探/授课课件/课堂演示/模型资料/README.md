# 手写数字识别模型

课堂演示使用已经训练好的MNIST卷积神经网络。输入是一张28×28像素的灰度图片，输出是0～9十个类别的模型分数。

模型与样例已嵌入[手写数字识别页面](../手写数字识别.html)。打开页面即可运行，无需另外加载本目录文件。页面用JavaScript执行原模型的卷积、池化和矩阵运算，没有将样例标签当作预测结果。

| 文件或资料 | 来源与用途 |
|---|---|
| [mnist-8.onnx](mnist-8.onnx) | [ONNX Model Zoo的MNIST模型](https://github.com/onnx/models/tree/main/validated/vision/classification/mnist)。保留原模型，便于核对与替换 |
| 模型说明 | 上游说明列出MNIST数据集、训练框架、输入与输出格式，以及MIT许可。见[上游README](https://github.com/onnx/models/blob/main/validated/vision/classification/mnist/README.md) |
| [上游仓库许可证](上游仓库许可证.txt) | 保留模型仓库根目录提供的Apache-2.0许可证原文；MNIST目录的模型许可按该目录说明 |
| 真实手写样例 | 从[TensorFlow提供的MNIST数据包](https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz)测试集中，按0～9各取第一张图片。页面保留原像素，供课堂快速演示 |

原模型SHA-256：`2f06e72de813a8635c9bc0397ac447a601bdbfa7df4bebc278723b958831c9bf`。

页面只做预测，不更新模型。鼠标手写时会将笔迹缩放、居中，再交给模型；预测不保证正确，可让学生比较不同写法。它不识别笔、橡皮、汉字或整道算式。下一课的文具分类项目仍使用Mind+和学生自己的实拍样本。
