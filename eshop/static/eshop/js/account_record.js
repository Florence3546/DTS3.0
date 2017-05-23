DTS = window.DTS || {};
DTS.account_record = function ($) {
    $(document).ready(function () {

        // 更多查询条件
        $(".select").on("click", function () {
            if ($(".more-choices").hasClass("hide")) {
                $(".more-choices").removeClass("hide");
                $(this).addClass("active");
            } else {
                $(".more-choices").addClass("hide");
                $(this).removeClass("active");
            }
        });

        var href = URI(document.location.href);
        var local_href = URI.parseQuery(href.query());

        // 记录时间选择
        $("#time_state").on('click', 'a', function () {
            var data_name = $(this).attr("data-name");
            var data_value = $(this).attr("data-value");
            var href = URI(document.location.href);
            href.removeSearch("time_state");
            href.addQuery(data_name.toString(), data_value.toString());
            local_href = URI.parseQuery(href.query());
            $(this).prop('href', href.toString());
        });

        $(".date").on('change', function () {
            var timer1 = $(".date").eq(0).val();
            var timer2 = $(".date").eq(1).val();
            var starttime1 = timer1.replace(new RegExp("-", "gm"), "/");
            var starttime2 = timer2.replace(new RegExp("-", "gm"), "/");
            var starttimeHaoMiao1 = (new Date(starttime1)).getTime(); //得到毫秒数
            var starttimeHaoMiao2 = (new Date(starttime2)).getTime(); //得到毫秒数
            if (starttimeHaoMiao1 > starttimeHaoMiao2) {
                $(".time-region").removeClass("hide");
                $("#btn-query").attr("disabled", true);
            } else {
                $(".time-region").addClass("hide");
                $("#btn-query").attr("disabled", false);
            }
        });

        // 交易类型选择
        $("#type_state").on('click', 'a', function () {
            var data_name = $(this).attr("data-name");
            var data_value = $(this).attr("data-value");
            var href = URI(document.location.href);
            href.removeSearch("type_state");
            href.addQuery(data_name.toString(), data_value.toString());
            local_href = URI.parseQuery(href.query());
            $(this).prop('href', href.toString());
        });

        // 支付方式选择
        $("#method_state").on('click', 'a', function () {
            var data_name = $(this).attr("data-name");
            var data_value = $(this).attr("data-value");
            var href = URI(document.location.href);
            href.removeSearch("method_state");
            href.addQuery(data_name.toString(), data_value.toString());
            local_href = URI.parseQuery(href.query());
            $(this).prop('href', href.toString());
        });

        // $(document).change("#money_from", function () {
        //     var min = $("#money_from").val();
        //     var max = $("#money_to").val();
        //     console.log(min);
        //     console.log(max);
        // });
        //
        // $(document).change("#money_to", function () {
        //     var min = $("#money_from").val();
        //     var max = $("#money_to").val();
        //     console.log(min);
        //     console.log(max);
        // });

        // 跳转到某一页
        $("#page_confirm").on('click', function () {
            var val = $("#page_num").val();
            $("#account_record_tab_paginate span a").eq(val - 1).click();
        });

        // 更多查询条件显示与否控制
        var form_val = $('#tread_node').val() ||
            $("#money_from").val() ||
            $('#money_to').val() ||
            $('#record_created_from').val() ||
            $('#record_created_to').val();
        if (form_val) {
            $(".more-choices").removeClass("hide");
        }
    });


    if ($(".dataTables_empty").is(":visible")) {
        // dataTable功能
        $('#account_record_tab').DataTable({
            "bPaginate": false, //翻页功能
            "bLengthChange": false, //改变每页显示数据数量
            "bFilter": false, //过滤功能
            "bSort": false, //排序功能
            "bInfo": false, //页脚信息
            "bAutoWidth": false,
            // "bStateSave": true,
            "oLanguage": {
                "sZeroRecords": "<img src='../../static/eshop/images/record.png' /> 暂无账户记录",
            }
        });
        $("#page_no").addClass("hide");
    } else {
        // dataTable功能
        $('#account_record_tab').DataTable({
            "bPaginate": true, //翻页功能
            "bLengthChange": false, //改变每页显示数据数量
            "bFilter": false, //过滤功能
            // "bSort": true, //排序功能
            "bInfo": false, //页脚信息
            "bAutoWidth": false,
            // "bStateSave": true,
            "order": [
                [0, "desc"]
            ],
            "aoColumnDefs": [{
                "bSortable": false,
                "aTargets": [1, 2, 3, 4]
            }],
            "aLengthMenu": [25],
            "oLanguage": {
                "sLengthMenu": "每页显示 _MENU_ 条记录",
                "sZeroRecords": "<img src='../../static/eshop/images/record.png' /> 暂无账户记录",
                "sInfo": "从 _START_ 条到 _END_ 条/共 _TOTAL_ 条数据",
                "sInfoEmpty": "",
                "sInfoFiltered": "(从 _MAX_ 条数据中检索)",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "< 上一页",
                    "sNext": "下一页 >",
                    "sLast": "尾页"
                }
            }
        });
    }


}($);
