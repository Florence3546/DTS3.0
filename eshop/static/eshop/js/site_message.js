var DTS = window.DTS || {};
DTS.site_message = function ($) {
    $(document).ready(function () {
        /**************************全部标记已读****************************/
        $(".sign_all_read").on("click", function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'mark_read_all',
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

        /**************************清除已读****************************/
        $(".clear_read").on("click", function () {
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'action': 'delete_read',
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

        /**************************点击标记为已读****************************/
        $(".unread").on("click", function () {
            var pk = $(this).data("pk");
            $.ajax({
                url: $(this).attr('api'),
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
                    'pk': pk,
                    'action': 'mark_read_single'
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

        /**************************分页跳转****************************/
        $(".skip").on("click", function () {
            var page = $(".page_no").val();
            $(".page_num").val(page);
            $(".page_skip").click();
        });

        /**************************tip提示****************************/
        $(function () {
            $("[data-toggle='tooltip']").tooltip();
        });

    });

    return {
        // 接口定义
    };


}($);