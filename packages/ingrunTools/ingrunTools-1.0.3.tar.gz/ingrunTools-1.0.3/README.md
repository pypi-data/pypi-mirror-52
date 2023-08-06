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

