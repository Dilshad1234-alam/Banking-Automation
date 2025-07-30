import random

captcha=[]
for i in range(3):
    c=chr(random.randint(65,90))
    captcha.append(c)

    n=random.randint(0,9)
    captcha.append(str(n))

random.shuffle(captcha)
captcha=' '.join(captcha)
print(captcha)