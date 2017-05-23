var DTS = window.DTS || {};
DTS.shopping_balance = function ($) {
    $(document).ready(function () {
        /*-------------------------支付方式------------------------*/
        $('.payment-img div').on('click', function () {
            $(this).addClass('active');
            $(this).siblings().removeClass('active');
            $('#payment_method').val($(this).data('id'));
        });

        $("#set-permission").validate();

        /*---------------------预付款支付--------------------*/
        $('.submit_pay').on('click', function () {
            if ($('#entry_password').val() == '') {
                DTS.alert('请输入支付密码');
                return false;
            }
            $.ajax({
                url: '',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'method': 'pre_pay',
                    // 'oid': $('#oid').val(),
                    'opk': $('#opk').val(),
                    // todo liu 2017-5-4 加密提交
                    'pay_passwd': $('#entry_password').val(),
                },
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.alert(data.msg);
                    if (data.status == 1) {
                        DTS.alert(data.msg, function () {
                            window.location.href = data.url + '?action=action_4&step=pay_password';
                        });
                    }
                },
                error: function () {
                    alert(DTS.tips_error);
                }
            });
        });

        $("#entry_password").on('input propertychange', function () {
            var value = $(this).val();
            if (value.length == 6) {
                $(this).blur();
            }
        })
    });



}($);
