# ingrunTools

### JsonToolsDjango

适配 django 的 http 返回  json 数据    



```python        
from ingrunTools.JsonToolsDjango import get_user_info, get_user_info

# get_json_models(ser, data, code, msg)    
# 栗子:        
class get_user_info(APIView):            
	user = User.object.get(pk=1)            
	return get_json_models(UserSerializer, user, 1, '查询用户信息成功') 

# {'code':1, msg: '查询用户信息成功', data: {'id':1, 'username': 'ingrun'} }

# get_json_success(msg)
# 栗子:        
class get_user_info(APIView):            
	user = User.object.get(pk=1)            
	return get_json_success('查询用户信息成功') 

# {'code':1, msg: '查询用户信息成功', data: '' }
```

### RandomTools

生成随机数的工具

```python
# get_random_list(max, length, min)  返回一个包含随机不重复整数的列表
# get_random_data_list(li, length) 随机返回一个列表的一部分 不重复

# 栗子:

a = get_random_list(10, 5, -10)
print(a)

print(get_random_data_list(a, 3))

# [10, -1, 9, 0, -5]
# [-1, 10, 9]


```

