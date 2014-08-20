function indexLayout() {
	var navX = $('section nav').offset().left;
	var navY = $('section nav').offset().top;
	$('section nav').css({
		'position':'fixed',
		'left': navX,
		'top': navY
	});
		//改变窗口大小时，现获取section的位置，重新定位
	$(window).resize(function() {
		var sectionX = $('section').offset().left;
		$('section nav').css('left',sectionX);
		if($(window).height() <= 800) {
			$('section nav').css({
				'height':'350px',
				'overflow-y':'auto'
			});
		} else {
			$('section nav').css({
				'height':'650px',
				'overflow-y':'hidden'
			});
		}
	});
}

function baseLayout() {
	$('aside').css({
		'right': '0',
		'top': '60px'
	});

	$('header .message').on('click', function() {
		var width = $('aside').width();
		if (width == 0) {
			$('aside').animate({width:"200px"},500);	
		} else {
			$('aside').animate({width:"0px"},500);	
		}
	});
}

$(function() {
	baseLayout();

	/*function navHidden() {
		$('section nav').remove();
		$('section .recommend').remove();
		$('section article.books').remove();
	}*/

	/*navHidden();*/

	//添加让(section nav)缩进的功能和样式改变，使得右侧向左撑开。
	//同时正好满足其他没有(section nav)的页面。
	
	/*监听网页滚动事件
	$(window).scroll(function() {
		if ($(window).scrollTop() >= 0) {
			
		}
		
	})*/
})