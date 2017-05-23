# coding=UTF-8

from hashids import Hashids
SALT = 'bc4##n_m@6-f_@19(k8#-5f%*'
hashids = Hashids(salt=SALT, min_length=5)

# hashids官网：https://github.com/davidaurelio/hashids-python
