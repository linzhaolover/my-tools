# 编写一个工厂模式的实例代码
# 1.定义一个接口类
# 2.定义一个工厂类
# 3.定义一个实现类
# 4.调用工厂类的方法，传入参数，返回实现类的实例
# 5.调用实现类的方法
# 6.调用接口类的方法


class Interface(object):
    def __init__(self):
        pass

    def run(self):
        pass


class Factory(object):
    def __init__(self):
        pass

    def create(self, name):
        if name == 'A':
            return A()
        elif name == 'B':
            return B()
        else:
            return None

    
class A(Interface):
    def __init__(self):
        pass

    def run(self):
        print('A')


class B(Interface):
    def __init__(self):
        pass

    def run(self):
        print('B')


if __name__ == '__main__':
    factory = Factory()
    a = factory.create('A')
    a.run()
    b = factory.create('B')
    b.run()

    
