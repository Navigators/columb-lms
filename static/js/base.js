	$.fn.hoverDelay = function(options){
        var defaults = {
            hoverDuring: 200,
            outDuring: 200,
            hoverEvent: function(){
                $.noop();
            },
            outEvent: function(){
                $.noop();    
            }
        };
        var sets = $.extend(defaults,options || {});
        var hoverTimer, outTimer;
        return $(this).each(function(){
            $(this).hover(function(){
                clearTimeout(outTimer);
                hoverTimer = setTimeout(sets.hoverEvent, sets.hoverDuring);
            },function(){
                clearTimeout(hoverTimer);
                outTimer = setTimeout(sets.outEvent, sets.outDuring);
            });    
        });
    }      
	function aside(){
		$('.navigation > li > ul').hide();
		$('.navigation').css('background','#ffffff');
		$('.navigation ul').css('background','#AACEEC');
		$('.navigation > li > a').each(function() {
			var that = $(this);
			$(this).on('click',function() {
				if (that.next().css('display') == "none") {
					that.next().slideDown('slow');
				} else {
					that.next().slideUp('slow');
				}
				
			});
		});
	}
	function choosen(){
		$('tr.choosen').each( function() {
			$(this).on('click', function(){
				if($(this).css('background-color') == 'rgb(196, 196, 226)' || $(this).css('background-color') == '#c4c4e2') {
					$(this).removeClass('tr-choosen-ok');
					$('.updateButton').attr('disabled','disabled');
				} else {
					$(this).parent().find('tr').removeClass('tr-choosen-ok');
					$(this).addClass('tr-choosen-ok');

					$('.updateButton').removeAttr('disabled');
					
				}
				/*$(this).addClass('table-tr-choosen');*/
			});
		});
	}
	function bookUpdate() {
		$('#copy-update').on('click', function() {
			$('#bookModal #bookModalLabel').html('修改复本信息');
			$('#bookModal #saveModal').html('修改');
			$('#bookBarCode').attr('value', $('.tr-choosen-ok').find('td:eq(0)').text());
			$('#searchCode').attr('value', $('.tr-choosen-ok').find('td:eq(1)').text());
			$('#regDate').attr('value', $('.tr-choosen-ok').find('td:eq(3)').text());
			$('#operatorCode').attr('value', $('.tr-choosen-ok').find('td:eq(4)').text());
			$('#operatorName').attr('value', $('.tr-choosen-ok').find('td:eq(5)').text());
			var text = $('.tr-choosen-ok').find('td:eq(2)').text();
			$('#status option[value='+text+']').attr('selected','selected');
		});
		$('#copy-add').on('click', function() {
			$('#bookModal #bookModalLabel').html('添加复本信息');
			$('#bookModal #saveModal').html('添加');
			$('#bookBarCode').attr('value', '');
			$('#searchCode').attr('value', '');
			$('#bookRoom').attr('value', '');
			$('#bookrack').attr('value', '');
			$('#volumeInfo').attr('value', '');
			$('#volumePrice').attr('value', '');
			$('#status option[value='+'可借'+']').attr('selected','selected');
		});
	}
	function permissionUpdate() {
		$('#permission-update').on('click', function() {
			$('#permissionModal #permissionModalLabel').html('修改权限');
			$('#permissionModal #saveModal').html('修改');
			$('#readerCategory').attr('value', $('.tr-choosen-ok').find('td:eq(0)').text());
			$('#borrowBooks').attr('value', $('.tr-choosen-ok').find('td:eq(1)').text());
			$('#borrowDays').attr('value', $('.tr-choosen-ok').find('td:eq(2)').text());
			$('#renewalTimes').attr('value', $('.tr-choosen-ok').find('td:eq(3)').text());
			$('#renewalDays').attr('value', $('.tr-choosen-ok').find('td:eq(4)').text());
			if ($('.tr-choosen-ok').find('td:eq(5)').text() == '是')
			{
				$('#japBooks').get(0).checked = true;
			}
			else
			{
				$('#japBooks').get(0).checked = false;

			}
			$('#idInput').attr('value', $('.tr-choosen-ok').find('td:eq(6)').text());
		});
		$('#permission-add').on('click', function() {
			$('#permissionModal #permissionModalLabel').html('添加权限');
			$('#permissionModal #saveModal').html('添加');
			$('#readerCategory').attr('value', '');
			$('#borrowBooks').attr('value', '');
			$('#borrowDays').attr('value', '');
			$('#renewalTimes').attr('value', '');
			$('#renewalDays').attr('value', '');
			$('#japBooks').get(0).checked = false;
		});
	}
	
	function showTips(cls) {
	    var left = $(cls).offset().left + 100;
	    var top = $(cls).offset().top;
	    $(cls).append('<div class="show-tip"></div>');
	    var str = $(cls).find('span').text();
	    $(cls).find('.show-tip').html(str);
	    $(cls).find('.show-tip').css({
	        'top':top,
	        'left':left,
	        'display':'block'
	    });
	}

	function hideTips(cls) {
	    $(cls).find('.show-tip').remove();
	}

$(function() {

	choosen();
	aside();
	bookUpdate();
	permissionUpdate();
})