var n = 0;
    $(document).ready(function(){
        count=$(".iga_lb_cont a").length;//显示区域的内容长度
        $(".iga_lb_item a").click(function(){
            $(this).addClass("iga_lb_seld").siblings().removeClass("iga_lb_seld");
            var _index=$(this).index();//分屏的数字索引
            $(".iga_lb_cont>a").eq(_index).fadeIn(260).siblings().fadeOut(260);
        });
        t = setInterval("iga_lb_showAuto()", 2000);//执行定义好的函数
        $(".iga_lb_box").hover(function(){clearInterval(t)}, function(){t = setInterval("iga_lb_showAuto()", 2000);});/*当鼠标划向图片时终止定时器，离开时再调用定时器*/
    })
    function iga_lb_showAuto()
    {
        n = n >=(count - 1)?0: ++n;
        $(".iga_lb_item a").eq(n).trigger('click');
    }