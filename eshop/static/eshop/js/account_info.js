var DTS = window.DTS || {};
DTS.account_info = function ($) {

    $(document).ready(function () {

        /*-------------------------个人会员注册确认提交------------------------*/

        function is_change() {
            var is_change = false;
            $('.is_change').each(function () {
                if(!($(this).attr('value') == $(this).val())){
                    is_change = true;
                }
                if(!($('input:radio:checked').val() == $('#is_gender_change').val())){
                    is_change = true;
                }
            });
            console.log(is_change);
            return is_change;
        }

        $(document).on('click', '.save', function () {
            if ($('#first_name').val() == '') {
                DTS.alert('姓名不能为空');
                return false
            }
            if ($('#phone').val() == '') {
                DTS.alert('手机号不能为空');
                return false
            }
            if ($('#email').val() == '') {
                DTS.alert('邮箱不能为空');
                return false
            }

            if (!is_change()) {
                DTS.alert('没有做任何修改');
                return false;
            }
            console.log('submit');
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: $('#account_form').serialize(),
                dataType: 'json',
                cache: false,
                success: function (data) {
                    DTS.alert(data.msg, function () {
                        window.location.reload();
                    });
                },
                error: function () {
                    alert('网络异常，请稍后刷新重试');
                }
            });
        });
    })


        // /*-------------------------提交时判断账户信息是否做过更改------------------------*/
        //
        //
        // $(".is_change").on('change',function () {
        //     console.log('fas');
        //     $(this).attr("changed", true);
        //     var value1 = $('#value1').val();
        //
        // });
        //     $.ajax({
        //         url: $(this).attr('api'),
        //         type: 'POST',
        //         data: $('#account_form').data("changed",true),
        //         dataType: 'json',
        //         cache: false,
        //         success: function (data) {
        //             DTS.alert(data.msg, function () {
        //                 window.location.reload();
        //             });
        //         },
        //         error: function () {
        //             alert('没有做任何修改');
        //         }
        //     });
}($);

