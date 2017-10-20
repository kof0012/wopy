
def wai(fun):
    def nei(*canshu):
        if len(canshu) == 0:
            return '没有传至'
        for i in canshu:
            if not isinstance(i, int):

                return '不是数字'
        return fun(*canshu)
    return nei


@wai
def my_sun(*canshu):
    return sum(canshu)

print(my_sun(1, 2, 3, 'zi'))
# he=wai(my_sun)
# print(he(1,2,3))


class jago():
    def dongzuo(self):
        print("这里是jago的dongzuo")


class Car():
    def __init__(self, make, mode, year, odometer_reading=0):
        self.make = make
        self.year = year
        self.model = mode
        self.odometer_reading = odometer_reading

    def get_descriptive_name(self):
        """ 返回整洁的描述性信息 """
        long_name = str(self.year) + ' ' + self.make + ' ' + \
            self.model + ' ' + str(self.odometer_reading)
        return long_name.title()

    def update_odometer(self, mileage):
        if mileage > self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print('你不能这么干')


class ElectricCar(Car):
    '''电动汽车'''

    def __init__(self, make, mode, year, what):
        super().__init__(make, mode, year)
        self.what = what
        self.jj = jago()

    def get_Elect_descriptive_name(self):
        """ 返回整洁的描述性信息 """
        long_name = 'wakawaka'
        return long_name.title()


class HunHeDongLi(ElectricCar):
    def __init__(self, make, mode, year, what):
        super().__init__(make, mode, year, what)

    def gandiansha(self, sha):
        return '你要干点啥' + sha + self.year

    def change_year(self, value):
        self.year = value

    @property
    def wucan(self):
        return self.make
diandong = ElectricCar('93号油', '5度电', '10', 'whatfuck')
print(diandong.what)
leiling = HunHeDongLi('93号油', '5度电', '10', 'whatfuck')
print(leiling.gandiansha('不知道'))
leiling.change_year(20)
print(leiling.year)
print(leiling.wucan)

def exceptTest():
    try:
        print( 'doing some work, and maybe exception will be raised')
        #raise IndexError('index error')
        print( 'after exception raise')
        return 0
        
    except KeyError:
        print( 'in KeyError except')
        
        return 1
    except IndexError:
        print( 'in IndexError except')
        return 2
    except ZeroDivisionError:
        print( 'in ZeroDivisionError')
        return 3
    else:
        print( 'no exception')
        return 4
    # finally:
    #     print( 'in finally')
    #     return 5

resultCode = exceptTest()
print (resultCode)