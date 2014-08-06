$(function() {
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
					$('#copy-update').attr('disabled','disabled');
				} else {
					$(this).parent().find('tr').removeClass('tr-choosen-ok');
					$(this).addClass('tr-choosen-ok');

					$('#copy-update').removeAttr('disabled');
					
				}
				/*$(this).addClass('table-tr-choosen');*/
			});
		});
	}
	function update() {
		//$('tr.choosen').each( function() {
			//var that = $(this);
			$('#copy-update').on('click', function() {
				$('#bookModal #bookModalLabel').html('修改复本信息');
				$('#bookModal #saveModal').html('修改');
				$('#bookBarCode').attr('value', $('.tr-choosen-ok').find('td:eq(0)').text());
				$('#searchCode').attr('value', $('.tr-choosen-ok').find('td:eq(1)').text());
				$('#bookRoom').attr('value', $('.tr-choosen-ok').find('td:eq(2)').text());
				$('#bookrack').attr('value', $('.tr-choosen-ok').find('td:eq(4)').text());
				$('#volumeInfo').attr('value', $('.tr-choosen-ok').find('td:eq(5)').text());
				$('#volumePrice').attr('value', $('.tr-choosen-ok').find('td:eq(6)').text());
				var text = $('.tr-choosen-ok').find('td:eq(3)').text();
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
		//});
	}
	choosen();
	aside();
	update();
})