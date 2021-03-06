import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.utils import shuffle



# -------------------------------------步骤1：数据准备----------------------------------------------------------
# 用pandas读取数据文件,并显示统计概述信息
df = pd.read_csv("boston-HousePrice-predict.csv", header=0)
# print(df.describe())
# plt.plot(df)
# plt.show()

df = df.values
df = np.array(df)
# print(df)

# 数据归一化：对特征值(0-11列）归一化（特征值/(最大值-最小值)）
for i in range(12):
    df[:, i] = (df[:, i]-df[:, i].min())/(df[:, i].max() - df[:, i].min())

x_data = df[:, :12]
y_data = df[:, -1]
# print(x_data)
# print(y_data)

# -------------------------------------步骤2：构建模型----------------------------------------------------------
# 定义训练数据占位符
x = tf.placeholder(tf.float32, shape=(None, 12), name="X")
y = tf.placeholder(tf.float32, shape=(None, 1), name="Y")

# 定义一个命名空间:把下面的语句打包，在计算图里面显示为一个子图
with tf.name_scope("Model"):
    # w初始化为shape=(12,1)的随机数
    w = tf.Variable(tf.random_normal([12, 1], stddev=0.01), name="W")
    # b初始化为固定值1
    b = tf.Variable(1.0, name="b")

    def model(x, w, b):
        return tf.matmul(x, w) + b

    pred = model(x, w, b)

# -------------------------------------步骤3：训练模型----------------------------------------------------------
# 设置超参数
train_epochs = 50
learning_rate = 0.01

# 定义均方差损失函数MSE
with tf.name_scope("LossFunction"):
    loss_func = tf.reduce_mean(tf.pow(y-pred, 2))

# 选择和定义优化器
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss_func)

# 开启会话
sess = tf.Session()
init = tf.global_variables_initializer()

# 启动sess
sess.run(init)

# 迭代训练
for epoch in range(train_epochs):
    loss_sum = 0.0
    for xs, ys in zip(x_data, y_data):
        # 后面feed的数据必须要与前面定义的placeholder的shape一致
        xs = xs.reshape(1, 12)
        ys = ys.reshape(1, 1)

        _, loss = sess.run([optimizer, loss_func], feed_dict={x: xs, y: ys})
        loss_sum += loss

    # 打乱数据顺序
    x_values, y_values = shuffle(x_data, y_data)

    b0temp = b.eval(session=sess)
    w0temp = w.eval(session=sess)
    loss_average = loss_sum / len(y_data)    # len(y_data)=506

    print("epoch=", (epoch+1), "loss=", loss_average, "b=", b0temp, "w=", w0temp)

# -----------------------------------步骤4：用训练好的模型进行预测----------------------------------------------
n = np.random.randint(506)
x_test = x_data[n]
print('n=', n)

x_test = x_test.reshape(1, 12)
predict = sess.run(pred, feed_dict={x: x_test})
print("预测值=", predict)

target = y_data[n]
print("目标值=", target)