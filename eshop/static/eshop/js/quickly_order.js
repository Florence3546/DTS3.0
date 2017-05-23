var DTS = window.DTS || {};
DTS.quickly_order = function ($) {
    $(document).ready(function () {
        // 排序
        $('.number').each(function (index) {
            $(this).text(index + 1)
        });

        // 全选
        $(".order_item .check-item").on('click', function () {
            if ($(this).is(":checked")) {
                $(this).parents("li").next().find("input").prop("checked", true);
            } else {
                $(this).parents("li").next().find("input").prop("checked", false);
            }
        });

        $(".details .check-item-mun").on('click', function () {
            if ($(this).is(":checked")) {
                $(this).parents(".details").find(".check-item").prop("checked", true);
            } else {
                $(this).parents(".details").find(".check-item").prop("checked", false);
            }
        });

        $('.old_order_item').on('click', function () {
            $(this).parent().parent().next().find('.check-item-mun').click();
        });

        /*-------------------历史购买记录点击订单全选订单下面的商品--------------------------*/


        // $(".details .check-item").on('click', function () {
        //     console.log($(this).parent().parent().find(".check-item"));
        //     var $checks = $(this).parent().parent().find(".check-item");
        //     console.log($checks);
        //     if ($checks.filter(":checked").length == $checks.length) {
        //         $(this).parent().parent().find(".check-item-mun").prop('checked', true);
        //     } else {
        //         $(this).parent().parent().find(".check-item-mun").prop('checked', false);
        //     }
        // });

        DTS.Check(".quick-order-tab .check-all", ".quick-order-tab .check-item");
        DTS.Check("#buyment-record .check-all", "#record-box input");

        // 搜索
        // $(".search-good").on('click', function () {
        //     var topH = $(this).offset().top + 30;
        //     var leftW = $(this).offset().left;
        //     $('#search-result').css({"top": topH});
        //     $('#search-result').css({"left": leftW});
        // });


        // $(".icon-enter").on('click', function () {
        //     var value = $(".search-good").val();
        //     if (value == "板蓝根") {
        //         $("#search-result").removeClass("hide");
        //         $(".mask-white").removeClass("hide");
        //     }
        // });

        $(document).on('click', '.search-closed', function () {
            $("#search-result").addClass("hide");
            $(".mask-white").addClass("hide");
        });
        $(".mask-white").on('click', function () {
            $("#search-result").addClass("hide");
            $(".mask-white").addClass("hide");
        });
        // $(document).keydown(function (event) {
        //     if (event.keyCode == 13) {
        //         $(".icon-enter").click();
        //     }
        // });

        $("#search-result tbody tr").on('click', function () {
            // var html = $(".quick_order_tab tr:eq(1)").html();
            // var str = "<tr>" + html + "</tr>";
            // $(".quick_order_tab tr").eq(1).after(str);
            $("#search-result").addClass("hide");
        });

        // 导入购买记录
        $("#reload-buyment-record").on('click', function () {
            $(".mask-layer").removeClass("hide");
            $("#buyment-record").removeClass("hide");
        });

        $(".cancel").on('click', function () {
            $(".mask-layer").addClass("hide");
            $("#buyment-record").addClass("hide");
        });

        $(".close-box").on('click', function () {
            $(".mask-layer").addClass("hide");
            $("#buyment-record").addClass("hide");
        });

        // 购买记录表格操作
        $("#buyment-record a").on('click', function () {
            var parent_li = $(this).parent().parent();
            if ($(this).hasClass("boult")) {
                if ($(this).hasClass("boult-down")) {
                    $(this).removeClass("boult-down").addClass("boult-up");
                    parent_li.next().removeClass("hide");
                } else {
                    $(this).removeClass("boult-up").addClass("boult-down");
                    parent_li.next().addClass("hide");
                }
            } else {
                if ($(this).siblings().hasClass("boult-down")) {
                    $(this).siblings().removeClass("boult-down").addClass("boult-up");
                    parent_li.next().removeClass("hide");
                } else {
                    $(this).siblings().removeClass("boult-up").addClass("boult-down");
                    parent_li.next().addClass("hide");
                }
            }
        });

        /*-------------------------数值去重------------------------*/
        function uniqueArr(ar) {
            var ret = [];
            ar.forEach(function (e, i, ar) {
                if (ar.indexOf(e) === i) {
                    ret.push(e);
                }
            });
            return ret;
        }

        /*-------------------------历史购买记录添加------------------------*/
        $(document).on('click', '.add_old_order', function () {
            var good_list = [];
            $('.old_good_item[type="checkbox"]:checked').each(function () {
                good_list.push($(this).data('gid'));
            });
            if (good_list.length == 0) {
                alert('请选择历史订单或者商品');
                return false;
            }
            // var $this = $(this);

            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'old_order',
                    'action': 'add',
                    'old_order_list': JSON.stringify(uniqueArr(good_list))
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        if (data.status == 2) {
                            // todo 数量
                            data = JSON.parse(data.data);
                            var select = '.quickly_order_id_';
                            select += data.quickly_order_id;
                            $(select).val(data.count);
                        }
                    }
                    //追加数据
                    $('#search_good_add').parent().parent().before(data);
                    // 处理序号
                    $('.number').each(function (index) {
                        $(this).text(index + 1)
                    });
                    $(".mask-layer").addClass("hide");
                    $("#buyment-record").addClass("hide");
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------删除商品------------------------*/
        $(document).on('click', '.remove', function () {
            var $this = $(this);
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'search_add_good',
                    'action': 'remove',
                    'quickly_order_id': $(this).parent().parent().find('.good_count').data('id')
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        alert(data.msg);
                        $this.parent().parent().remove();
                        $('.number').each(function (index) {
                            $(this).text(index + 1)
                        });
                    } else {
                        alert('删除失败');
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            })
        });

        /*-----------------------回车搜索返回商品列表-----------------------------*/
        $('#search_good_add').on('keydown', function (e) {
            if (event.keyCode == 13) {
                $.ajax({
                    url: $(this).attr('api'),
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'method': 'search_add_good',
                        'action': 'search_keywords',
                        'search_keywords': $('#search_good_add').val()
                    },
                    cache: false,
                    success: function (data) {
                        if (data.status == 0) {
                            alert(data.msg);
                        } else {
                            $('#search-result').replaceWith(data);
                            $("#search-result").removeClass("hide");
                            console.log($('#search_good_add').val());
                        }
                    },
                    error: function () {
                        DTS.alert(DTS.tips_error);
                    }
                });
            }
        });

        /*--------------------------搜索返回商品点击添加----------------------------*/
        $(document).on('click', '.good_item', function () {
            // 序号处理
            // var number = $('.add_good').parent().parent().prev().find('.number').text();
            // if (!number){
            //     number = 0;
            // }
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'search_add_good',
                    'action': 'add_good',
                    'good_id': $(this).data('id'),
                    // 'number': number,
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        if (data.status == 2) {
                            var select = '.quickly_order_id_';
                            select += data.quickly_order_id;
                            $(select).val(data.count);
                        }
                    }

                    $('#search_good_add').parent().parent().before(data);
                    $('.number').each(function (index) {
                        $(this).text(index + 1)
                    });
                    // number = parseInt(number) + 1;
                    // $('.add_good').parent().parent().prev().find('.number').text(number);
                    // $('.add_number').text(number + 1);
                },
                error: function () {
                    alert('网络异常，请刷新重试');
                }
            });
        });

        /*-------------------------数量加减ajax---------------------------------*/
        $(document).on('click', '.good_count_action', function () {
            var action = $(this).data('action');
            var gid = $(this).siblings('.good_count').data('id');
            console.log(gid);
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'good_count',
                    'action': action,
                    'gid': gid
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        alert(data.msg);
                    } else {
                        alert('删除失败');
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /*-------------------------数量加减---------------------------------*/
        // 加减法和计算和
        var index = 0;
        var num = 0;
        $(document).on('click', '.reduce-number', function () {
            index = $(this).index();
            num = $(this).siblings().eq(0).val();
            num = num - 1;
            if (num <= 0) {
                num = 1;
            }
            $(this).siblings().eq(0).val(num);
        });

        // 添加
        $(document).on('click', '.add-number', function () {
            index = $(this).index();
            num = $(this).siblings().eq(1).val();
            num++;
            // if (num >= 10) {
            //     $(".max-number").removeClass('disnone');
            //     num = 10;
            // }
            $(this).siblings().eq(1).val(num);
        });

        /*-------------------------input直接修改数量------------------------*/
        $(document).on('blur', '.good_count', function () {
            var action = $(this).data('action');
            var gid = $(this).data('id');
            var good_count_value = $(this).val();
            console.log(gid);
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'good_count',
                    'action': 'count_value',
                    'gid': gid,
                    'good_count_value': good_count_value
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        console.log(data.good_count);
                    } else {
                        alert('修改失败');
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        /*------------------------------提交结算----------------------------*/
        $('.shopping_balance').on('click', function () {
            var order_list = [];
            $('.order_item[type="checkbox"]:checked').each(function () {
                order_list.push($(this).data('id'));
            });
            if (order_list.length == 0) {
                alert('请选择商品');
                return false;
            }
            console.log(order_list);

            var url = $('#shopping_balance').val();
            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'add_order',
                    'action': 'quickly_add',
                    'quickly_order_ids': JSON.stringify(order_list)
                },
                cache: false,
                success: function (data, status, xhr) {
                    if (xhr.getResponseHeader('Content-Type') == 'application/json') {
                        if (data.status == 2) {
                            window.location.href = data.url;
                        }
                    }
                },
                error: function () {
                    DTS.alert(DTS.tips_error);
                }
            });
        });

        // $('.add_good').on('click', function () {
        //     var num = $(this).parent().parent().prev().find('.number').text();
        //     if (!num) {
        //         num = 0;
        //     }
        //     num = parseInt(num) + 1;
        //     $('.add_number').text(num + 1);
        //
        //     var a = '<tr>';
        //     a += '<td><input type="checkbox" class="check-item"></td>';
        //     a += '			<td class="number">';
        //     a += num;
        //     a += '</td>';
        //     a += '			<td>慢严舒柠 清喉利咽颗粒 5g*18袋</td>';
        //     a += '			<td>';
        //     a += '				<form>';
        //     a += '					<div class="input-group input-group-defined">';
        //     a += '						<div class="input-group-addon btn-addon-defined reduce-number">-</div>';
        //     a += '						<input type="text" class="form-control input-add-subtract" value="5">';
        //     a += '						<div class="input-group-addon btn-addon-defined add-number">+</div>';
        //     a += '					</div>';
        //     a += '				</form>';
        //     a += '			</td>';
        //     a += '			<td>包</td>';
        //     a += '			<td>2016050215478914</td>';
        //     a += '			<td>5g*16袋</td>';
        //     a += '			<td>贵州复方药业有限公司</td>';
        //     a += '			<td>8.00</td>';
        //     a += '			<td>800.00</td>';
        //     a += '			<td>';
        //     a += '				<a class="remove">删除</a>';
        //     a += '</td>';
        //     a += '</tr>';
        //
        //     $(this).parent().parent().before(a);
        // })
    });

}($);

