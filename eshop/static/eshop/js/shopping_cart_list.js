var DTS = window.DTS || {};
DTS.shopping_cart_list = function ($) {
    $(document).ready(function () {

        // 缺货登记
        DTS.lack_register($(".lack_register"));
				if($(".stockout").length){
					$(".remove_failed_goods").removeClass("hide");
				}
        // 全选按钮 click
        $('.check-all').click(function () {
            if ($(this).is(":checked")) { //全选
                $('ul input[type=checkbox]').each(function () {
                    if ($(this).attr("disabled") == undefined) {
                        $(this).prop('checked', true);
                    }
                });
            } else {
                $('ul input[type=checkbox]').prop('checked', false);
            }
            var selected_len = $(".shopping_car_list li input[type=checkbox]:checked").length;
            update_total_prices('.total_prices')
        });

        // 多选单个选中操作
        $("ul.shopping_car_list input[type=checkbox]").on('click', function () {
            var selected_len = $(".shopping_car_list li input.check-box[type=checkbox]:checked").length;
            var all_len = $(".shopping_car_list li input.check-box[type=checkbox]").length;
            var dis_len = $(".shopping_car_list li input.check-box[type=checkbox]:disabled").length;
            if (selected_len == (all_len - dis_len)) {
                $('.check-all').prop('checked', true);
            } else {
                $('.check-all').prop('checked', false);
            }
            update_total_prices('.total_prices')
        });

        /*---------------------更新商品数量ajax----------------------*/
        function update_good_count(obj) {
            var url = $('#shopping_cart_list').val();
            var good_count = $(obj).parent().find('.good_count').val();
            var id = $(obj).parent().find('.good_count').data('id');
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'good_count',
                    'good_count': good_count,
                    'id': id
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data.status == 0) {
                        DTS.alert(data.msg, function () {
                            $(".good_count").val(data.good_count);
                        });
                        console.log(data.msg);
                    } else if (data.status == 1) {
                        console.log(data.msg);
                    }
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        }

        // 加减法和计算和
        var index = 0,
            num = 0;
        $(".reduce-number").on('click', function () {
            var $this = $(this);
            index = $(this).index();
            num = $(this).siblings().eq(0).val();
            num = num - 1;
            if (num <= 0) {
                num = 1;
            }
            $(this).siblings().eq(0).val(num);
            $(this).parent().siblings().addClass('hide');
            var price = $(this).parents('.good').find('.price').text();
            var subtotal = parseFloat(price) * num;
            $(this).parents('.good').find('.subtotal').text(subtotal.toFixed(2));
            // 更新价钱
            update_total_prices('.total_prices');
            // 更新数量ajax
            update_good_count($this);
        });

        $(".add-number").on('click', function () {
            var $this = $(this);
            index = $(this).index();
            num = $(this).siblings().eq(1).val();
            num++;
            if (num >= 999) {
                num = 999;
                $(this).parent().siblings().removeClass('hide');
                // $(".max-number").removeClass('hide');
            }
            $(this).siblings().eq(1).val(num);
            var price = $(this).parents('.good').find('.price').text();
            var subtotal = parseFloat(price) * num;
            $(this).parents('.good').find('.subtotal').text(subtotal.toFixed(2));
            // 更新价钱
            update_total_prices('.total_prices');
            // 更新数量ajax
            update_good_count($this);
        });
        $(".input-add-subtract").change(function () {
            var $this = $(this);
            num = $(this).val();
            if (isNaN(num) || num == 0) {
                $(this).val("1");
                num = $(this).val();
            } else if (num >= 999) {
                num = 999;
                $(this).val(num);
                $(this).parent().siblings().removeClass('hide');
            }
            var price = $(this).parents('.good').find('.price').text();
            var subtotal = price * num;
            $(this).parents('.good').find('.subtotal').text(subtotal.toFixed(2));
            // 更新价钱
            update_total_prices('.total_prices');
            // 更新数量ajax
            update_good_count($this);
        });

        /*-------------------------单个删除购物车商品------------------------*/
        $('#content').on('click', '.delete_good', function () {
            var pk_list = [];
            var $this = $(this);
            pk_list.push($(this).data('pk'));
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'delete_good',
                    'pk': JSON.stringify(pk_list)
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    $this.closest("li").remove();
                    $(".shopping_cart_count").text($("input.check-box").length);
                    update_total_prices('.total_prices');
                    refresh();
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------批量删除购物车商品------------------------*/
        $('#content').on('click', '.delete_goods', function () {
            var pk_list = [];

            $('.check-box').each(function () {
            	if($(this).is(":checked")){
                pk_list.push($(this).data('pk'));
            	}
            });
						if(pk_list.length){
							$.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'delete_good',
                    'pk': JSON.stringify(pk_list)
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    for(var i in pk_list){
                    	$("input[data-pk="+pk_list[i]+"]").closest("li").remove();
                    }
                    $(".shopping_cart_count").text($("input.check-box").length);
                    update_total_prices('.total_prices');
                    refresh();
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            	});
						}else{
							alert("请至少选中一件商品");
						}
            
        });
				
        /*-------------------------单个移动到收藏夹------------------------*/
        $('#content').on('click', '.move_to_favorites', function () {
            var pk_list = [];
            var $this = $(this);
            pk_list.push($(this).data('pk'));
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'move_to_favorites',
                    'pk': JSON.stringify(pk_list)
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    $this.closest("li").remove();
                    $(".shopping_cart_count").text($("input.check-box").length);
                    update_total_prices('.total_prices');
                    refresh();
                },
                error: function () {
                    DTS.affirm(DTS.tips_error);
                }
            });
        });

        /*-------------------------批量移动到收藏夹------------------------*/
        $('#content').on('click', '.batch_move_to_favorites', function () {
            var pk_list = [];
            $('.check-box').each(function () {
                if ($(this).is(":checked")) {
                    var pk = $(this).closest("li").find(".move_to_favorites").data("pk")
                    pk_list.push(pk);
                }
            });
            if (pk_list.length) {
                $.ajax({
                    url: $(this).attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'action': 'move_to_favorites',
                        'pk': JSON.stringify(pk_list)
                    },
                    dataType: 'json',
                    cache: false,
                    success: function (data) {
                        DTS.affirm(data.msg);
                        for(var i in pk_list){
		                    	$(".move_to_favorites[data-pk="+pk_list[i]+"]").closest("li").remove();
		                    }
		                    $(".shopping_cart_count").text($("input.check-box").length);
		                    update_total_prices('.total_prices');
		                    refresh();
                    },
                    error: function () {
                        DTS.affirm(DTS.tips_error);
                    }
                });
            } else {
                alert("请至少选中一件商品")
            }
        });

        /*-------------------------移除失效商品------------------------*/
        $('#content').on('click', '.remove_failed_goods', function () {
            var pk_list = [];
            $('.stockout input').each(function () {
                pk_list.push($(this).data('pk'));
            });
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'remove_failed_goods',
                    'pk': JSON.stringify(pk_list)
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.affirm(data.msg);
                    $(".stockout").remove();
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------总价------------------------*/
        //修改总价
        function update_total_prices(select) {
            var total_prices = 0;
            $('.good input.check-box[type=checkbox]:checked').each(function () {
                var price = $(this).parent().siblings('.sub-total').find('.subtotal').text();
                if (price) {
                    return total_prices += parseFloat(price);
                }
            });
            $(".selected").text($('.good input.check-box[type=checkbox]:checked').length);
            $(select).text(total_prices.toFixed(2));
        }

        /*-------------------------去结算 ------------------------*/

        $('#content').on('click', '.shopping_balance', function () {
            var pk_list = [];
            $('.check-box').each(function () {
                if ($(this).is(":checked")&&!$(this).closest('li').hasClass("stockout")) {
                    pk_list.push($(this).data('pk'));
                }
            });
            if (pk_list.length == 0) {
                DTS.affirm("请至少选中一件商品！失效商品不能结算");
                return false;
            }
            $.ajax({
                url: $('#shopping_balance').val(),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'add_order',
                    'action': 'cart_add',
                    'pk': JSON.stringify(pk_list)
                    // 购物车id
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data.status == 2) {
                        window.location.href = data.url;
                    }
                },
                error: function () {
                    DTS.affirm('发生错误');
                }
            });
        });
        /*-------------------------无数据时刷新页面------------------------*/
	      function refresh(){
	        if(!$("input.check-box").length){
	        	$(".list-footer").remove();
	        	window.location.reload();
	        }
	      }
    });


}($);



