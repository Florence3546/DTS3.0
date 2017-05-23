DTS = window.DTS || {};
DTS.lack_good = function ($) {
    $(document).ready(function () {

        $(function () {
            $('[data-toggle="tooltip"]').tooltip();
        });

        //-----------------------------------加入购物车-----------------------------------//
        $('.add_cart').on('click', function () {
            var pk_list = [];
            var url = $(this).attr('api');
            var pk = $(this).data("pk");
            var num = 1;
            pk_list.push({"pk": pk, "num": num});
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

        // 删除
        $('.section').on('click', '.delete', function () {
            var url = $(this).attr('api');
            var this_id = $(this).data("id");
            DTS.confirm("删除后不可恢复，您确定要删除吗？", function () {
                $.ajax({
                    url: url,
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                        'id': this_id
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
            }, "删除提醒");
        });

    })
}($);

