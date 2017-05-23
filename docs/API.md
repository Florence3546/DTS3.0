#### 收藏api

```
api url
{% url 'order:my_favorites' %}



GET
    获取收藏状态
    ?gid=<商品id> 
    返回 =>
    status = 1 已经收藏了 
    status = 0 没有收藏 
    
        result = {
        'status': 1,
        'msg': u'已经收藏了'
        }
POST
    method:
        my_favorites
    action:
        add             添加收藏
        remove          移除收藏
        
    id_list: [1,2]      good列表




```

#### 购物车api  

加入购物车  


```
post 

method: "add_cart"
action: "add"
gid:<good_id>,
count:<good_count>




callback:{
href:"<>"
}

```
