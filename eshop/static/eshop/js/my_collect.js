DTS = window.DTS || {};
DTS.my_collect = function ($) {
    $(document).ready(function () {
//---------------------------商品筛选---------------------------//
        $(".choose").on("click","a",function(){
            $(this).addClass("active").siblings().removeClass("active");
        });
//---------------------------批量操作---------------------------//
        $(".cancel a").on("click",function(){
        	if($(this).data("search")){
        		if($(".collect-list").hasClass("batch")){
                $(this).find("a").html("批量管理");
                $(".collect-list").removeClass("batch");
                $(".cancel-box").removeClass("active");
            }else{
                $(this).find("a").html("取消管理");
                $(".collect-list").addClass("batch");
                $(".single_good").removeClass("active");
                $(".cancel-box").addClass("active");
            }
            $(".check-all").removeClass("active");
        	}
        });
//---------------------------是否全选---------------------------//
        $(".check-all").on("click",function(){
            if($(this).hasClass("active")){
                $(this).removeClass("active");
                $(".single_good").removeClass("active");
            }else{
                $(this).addClass("active");
                $(".single_good").addClass("active");
            }
        })
//---------------------------是否选中单个商品---------------------------//
        $(".search-goods").on("click",".single_good",function(){
            if($(this).hasClass("active")){
                $(this).removeClass("active");
                $(".check-all").removeClass("active");
            }else{
                $(this).addClass("active");
                var flag=true;
                $(this).siblings().each(function(){
                    if(!$(this).hasClass("active")){
                        flag=false;
                    }
                });
                if(flag){
                    $(".check-all").addClass("active");
                }
            }
        })
//--------------------------加减---------------------------//
        $(".search-goods").on("click",".reduce",function(){
            var num=$(this).next().val()-1;
            if(num>0){
                $(this).next().val(num);
            }
        })
        $(".search-goods").on("click",".add",function(){
            var num=$(this).prev().val()*1+1;
            if(num<=999){
                $(this).prev().val(num);
            }
        })
        /*************************分页事件绑定************************/
        DTS.bind_page( DTS.my_collect.load_collect_data);

        /*************************搜索页码************************/
        // $(".skip").on("click",function(){
        //     // 查询时默认加载第一页
        //     DTS.my_collect.load_collect_data(1);
        // })
        /*************************单个删除************************/
        $('.search-goods').on('click', '.collect', function () {
            var pk_list = [];
            var url = $(this).attr('api');
            pk_list.push($(this).data('pk'));
            DTS.confirm('确定要删除此商品吗?',function(){
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'pk': JSON.stringify(pk_list)
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        alert(data.msg);
                        window.location.reload();
                    },
                    error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            },'删除商品');
        });
        /*************************批量删除************************/
        $('.batch_delete').on('click', function () {
            var pk_list = [];
            var url = $(this).attr('api');
            $('.single_good').each(function(){
                if($(this).hasClass("active")){
                    var str=$(this).find(".collect").data("pk");
                    pk_list.push(str);
                }
            })
            if(pk_list.length>0){
                DTS.confirm('确定要删除此商品吗?',function(){
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: {
                            'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                            "pk": JSON.stringify(pk_list)
                        },
                        dataType: 'json',
                        cache: false,
                        success: function (data) {
                            alert(data.msg);
                            window.location.reload();
                        },
                        error: function () {
                            DTS.alert(DTS.tips_error);
                        }
                    });
                },'删除商品');
            }
        });
        /*************************单个添加购物车************************/
        $('.search-goods').on('click', '.add_shopping_cart', function () {
            var pk_list = [];
            var url = $(this).attr('api');
            var pk=$(this).data("pk");
            var num=$(this).parent().find("input").val();
            pk_list.push({"pk":pk, "num":num});
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'pk': JSON.stringify(pk_list)
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    alert(data.msg);
                    window.location.reload();
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });
        /*************************批量加入购物车************************/
        $('.batch_add_shopping_cart').on('click', function () {
            var pk_list = [];
            var url = $(this).attr('api');
            $('.single_good').each(function(){
                if($(this).hasClass("active")&!$(this).hasClass("disabled")&!$(this).find(".stockout").length){
                    var pk=$(this).find('.add_shopping_cart').data("pk");
                    var num=$(this).find("input").val();
                    pk_list.push({"pk":pk, "num":num});
                }
            });
            if(pk_list.length>0){
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        "pk": JSON.stringify(pk_list)
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        alert(data.msg);
                        window.location.reload();
                    },
                    error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            }
        });
        DTS.lack_register($(".lack_register"));

    });

    return{
        // 多条件加载我的收藏数据
        load_collect_data:function(num){
            $(".page_num").val(num);
            $("#collect_form").submit();
        }
    }
}($);