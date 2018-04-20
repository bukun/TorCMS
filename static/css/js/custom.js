jQuery(document).ready(function ($) {
    /* BX slider 1*/
	var bannerslider = $('#banner_slider');
    if (bannerslider.length) {
        bannerslider.bxSlider({ auto: true, minSlides: 1, maxSlides: 1, slideMargin: 18, speed: 500 });
    }
	var newslider = $('#news_slider');
    if (newslider.length) {
        newslider.bxSlider({ minSlides: 1, maxSlides: 1, slideMargin: 18, speed: 500 });
    }
	var videoslider = $('.video_slider');
    if (videoslider.length) {
        videoslider.bxSlider({ minSlides: 1, maxSlides: 1, slideMargin: 25, speed: 500, });
    }
	var blogslider = $('#blog_slider');
    if (blogslider.length) {
        blogslider.bxSlider({ minSlides: 1, maxSlides: 1 });
    }
	var shopslider = $('#shop_slider');
    if (shopslider.length) {
        shopslider.bxSlider({ slideWidth: 140,minSlides: 1, maxSlides: 3, slideMargin: 28 });
    }
	var officeslider = $('#office_slider');
    if (officeslider.length) {
        officeslider.bxSlider({ slideWidth: 270, minSlides: 1, maxSlides: 4, slideMargin: 28 });
    }
	var productslider = $('#slider_products');
    if (productslider.length) {
       productslider.bxSlider({ slideWidth: 270, minSlides: 1, maxSlides: 1, slideMargin: 10 });
    }

    /* bootstrap Add class to accordion **/
    var sidebar = $('.accordion-heading'); /* cache sidebar to a variable for performance */
    sidebar.delegate('.accordion-toggle', 'click', function () {
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).addClass('inactive');
            $("#icon_toggle i", this).removeClass('icon-minus').addClass('icon-plus');
        } else {
            sidebar.find('.active').addClass('inactive');
            sidebar.find('.active').removeClass('active');
            $(this).removeClass('inactive');
            $(this).addClass('active');
            $("#icon_toggle i", this).removeClass('icon-plus').addClass('icon-minus');
        }
    });
    /* End of bootstrap Add class to accordion **/

    /* Footer Gallery Pretty Photo Widget **/
    $(".gallery-list:first a[rel^='prettyPhoto']").prettyPhoto({ animation_speed: 'normal', theme: 'light_square', slideshow: 3000, autoplay_slideshow: true });
    /* End of Footer Gallery Pretty Photo Widget **/
	
	/* Start of Photo Gallery Pretty Photo **/
	$(".gallery-page:first a[rel^='prettyPhoto']").prettyPhoto({animation_speed: 'normal',theme: 'light_square', slideshow: 3000, autoplay_slideshow: true });
	/* End of Photo Gallery Pretty Photo **/
	
    /* Social Icons **/
    $('.social_active').hoverdir({});
    /* End of Social Icons Animation **/

    /* Start of Counter */
    var austDay = new Date();
    austDay = new Date(2013, 8 - 1, 5, 11, 00)
    $('#countdown162').countdown({
        until: austDay
    });
    $('#year').text(austDay.getFullYear());	    
	/* End of Counter */
	
	 /* Bootstrap Tooltip */
	 $("[rel='tooltip']").tooltip();
	 /* Bootstrap Tooltip */
});
/* End of Counter */