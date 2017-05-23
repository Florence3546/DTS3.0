DTS = window.DTS || {};
DTS.log_manage = function ($) {
    $(document).ready(function () {
        // 分页事件绑定
        if ($("#total_count").val() > 0) {
            DTS.bind_page(DTS.log_manage.load_log_data);
            DTS.data_table('#table_log');
        }
    });

    return {
        load_log_data: function (load_page) {
            //查询加载数据列表
            $("#page").val(load_page);
            $("#id_operator_name").val($.trim($("#id_operator_name").val()));
            $("#log_detail").val($.trim($("#log_detail").val()));
            DTS.loading_dialog(true);
            $("#form_log_manage").submit();
        }
    };
}($);