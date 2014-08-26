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
		$('.navigation > li > a').each(function() {
			var that = $(this);
			$(this).on('click',function() {
				if (that.next().css('display') == "none") {
					that.next().slideDown('slow');
					that.parent().addClass('nav-active');
				} else {
					that.next().slideUp('slow');
					that.parent().removeClass('nav-active');
				}
				
			});
		});
	}
	function choosen(){
		$('tr.choosen').each( function() {
			$(this).on('click', function(){
				if($(this).css('background-color') == 'rgb(209, 227, 241)' || $(this).css('background-color') == '#D1E3F1') {
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
	
	function customizeTable() {
		$('#customize').on('click', function() {
			if ($('#tableItems').css('display') == 'none') {
				$('#tableItems').slideDown('slow');
				$(this).html('收起定制');
			} else {
				$('#tableItems').slideUp('slow');
				$(this).html('定制列表');
			}
		});
		$('#tableItems input').attr('checked','checked');
		$('#tableItems input').each(function(index) {
			$(this).click(function(){
				if ($(this).attr('checked') == 'checked') {
					$(this).removeAttr('checked');
					console.log('这是第'+index+'个');
					$(this).parent().next().find('tr th:eq('+index+')').hide();
				} else {
					$(this).attr('checked','checked');
					$(this).parent().next().find('tr th:eq('+index+')').show();
				}
			});
		});
		$('#resultTable').hoverDelay({
			hoverEvent: function() {
				$('#resultTable').css('overflow','auto');
			},
			outEvent: function() {
				$('#resultTable').css('overflow','hidden');
			}
		});
	}
	
	function newTableTd() {
		$('#tableItems').html('');
		$('#tableItems').html('<input type="checkbox"><label>借出时间</label><input type="checkbox"><label>书刊名称</label><input type="checkbox"><label>书刊条号</label><input type="checkbox"><label>读者姓名</label><input type="checkbox"><label>读者工号</label><input type="checkbox"><label>读者类别</label><input type="checkbox"><label>续借次数</label><input type="checkbox"><label>应还日期</label><input type="checkbox"><label>借书操作员</label>');
		$('#tableItems input').attr('checked','checked');
		$('#tableItems input').each(function(index) {
			$(this).click(function(){
				if ($(this).attr('checked') == 'checked') {
					$(this).removeAttr('checked');
					console.log('这是第'+index+'个');
					var length = $(this).parent().next().find('tr').length;
					for (var i=0; i<length; i++) {
						$(this).parent().next().find('tr:eq('+i+')').find('td:eq('+index+')').hide();
					}
				} else {
					$(this).attr('checked','checked');
					var length = $(this).parent().next().find('tr').length;
					for (var i=0; i<length; i++) {
						$(this).parent().next().find('tr:eq('+i+')').find('td:eq('+index+')').show();
					}
				}
			});
		});
	}
	

function showTdContent(){
	$('.table tr').addClass('cursor-pointer');
	$('.table td').each(function() {
		var title = $(this).text();
		$(this).attr('title',title);
	})
}

$(function() {
	showTdContent();
	choosen();
	aside();
	customizeTable();
})