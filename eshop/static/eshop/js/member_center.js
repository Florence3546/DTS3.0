/**
 * Created by Administrator on 2017/5/4 0004.
 */
DTS = window.DTS || {};
DTS.member_center = function ($) {
    $(document).ready(function () {
        $(function () {
            $('[data-toggle="tooltip"]').tooltip();
        });
				//-----------------------------------商品详情图片切换-----------------------------------//
        $(function(){
        	var a = $(".collect-list li").length;
	        var b = a;
	        var l = $(".collect-list ul").width()/a;
	        $(".prev-good").on("click", function () {
	            if (b < a) {
	                b += 1;
	                $(".collect-list ul").css({"left": -l* (a - b) + "px"});
	            }
	        });
	        $(".next-good").on("click", function () {
	            if (b > 4) {
	                b -= 1;
	                $(".collect-list ul").css({"left": -l * (a - b) + "px"});
	            }
	        });
        })

    });
    
    // 接口定义
    return{

    };

}($);