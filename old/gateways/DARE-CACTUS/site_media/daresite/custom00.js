jQuery.noConflict();

/* if IE run unitpngfix for sociable fade
if(jQuery.browser.msie){
	var $shared_path = jQuery("meta[name=shared_path]").attr('content');
	var clear=$shared_path+"/clear.gif"; //path to clear.gif
	document.write('<script type="text/javascript" id="ct" defer="defer" src="javascript:void(0)"><\/script>');var ct=document.getElementById("ct");ct.onreadystatechange=function(){pngfix()};pngfix=function(){var els=document.getElementsByTagName('*'),ip=/\.png/i,al="progid:DXImageTransform.Microsoft.AlphaImageLoader(src='",i=els.length,uels=new Array(),c=0;while(i-->0){if(els[i].className.match(/unitPng/)){uels[c]=els[i];c++;}}if(uels.length==0)pfx(els);else pfx(uels);function pfx(els){i=els.length;while(i-->0){var el=els[i],es=el.style,elc=el.currentStyle,elb=elc.backgroundImage;if(el.src&&el.src.match(ip)&&!es.filter){es.height=el.height;es.width=el.width;es.filter=al+el.src+"',sizingMethod='crop')";el.src=clear;}else{if(elb.match(ip)){var path=elb.split('"'),rep=(elc.backgroundRepeat=='no-repeat')?'crop':'scale',elkids=el.getElementsByTagName('*'),j=elkids.length;es.filter=al+path[1]+"',sizingMethod='"+rep+"')";es.height=el.clientHeight+'px';es.backgroundImage='none';if(j!=0){if(elc.position!="absolute")es.position='static';while(j-->0)if(!elkids[j].style.position)elkids[j].style.position="relative";}}}}};};

}
*/

/* delay function */
jQuery.fn.delay = function(time,func) {
	this.each(function() {
		setTimeout(func,time);
	})
	return this;
};

/* hover fade functions */
function fade_hover() {
	jQuery('.fade_hover').hover(
		function() {
				jQuery(this).stop().animate({opacity:0.4},400);
			},
			function() {
				jQuery(this).stop().animate({opacity:1},400);
		});

}

function portfolio_img_hover() {
	jQuery(".load_img").hover(
		function() {
				jQuery(this).find('.portfolio_hover').stop().animate({opacity:0.4},400);
			},
			function() {
				jQuery(this).find('.portfolio_hover').stop().animate({opacity:1},400);
			});
}

function sociable_hover() {
	jQuery('.sociable_hover').hover(
		function() {
				jQuery(this).stop().animate({opacity:0.5},400);
			},
			function() {
				jQuery(this).stop().animate({opacity:1},400);
		});
}

function button_hover(){
	jQuery('.button_link,button[type=submit],button,input[type=submit],input[type=button],input[type=reset]').hover(
		function() {
				jQuery(this).stop().animate({opacity:0.8},400);
			},
			function() {
				jQuery(this).stop().animate({opacity:1},400);
		});
}


function expandIt(getIt){getIt.style.display=(getIt.style.display=="none")?"":"none";}

/* 
 * No Spam (1.3)
 * by Mike Branski (www.leftrightdesigns.com)
 * mikebranski@gmail.com
 *
 * Copyright (c) 2008 Mike Branski (www.leftrightdesigns.com)
 * Licensed under GPL (www.leftrightdesigns.com/library/jquery/nospam/gpl.txt)
 *
 * NOTE: This script requires jQuery to work.  Download jQuery at www.jquery.com
 *
 * Thanks to Bill on the jQuery mailing list for the double slash idea!
 *
 * CHANGELOG:
 * v 1.3   - Added support for e-mail addresses with multiple dots (.) both before and after the at (@) sign
 * v 1.2.1 - Included GPL license
 * v 1.2   - Finalized name as No Spam (was Protect Email)
 * v 1.1   - Changed switch() to if() statement
 * v 1.0   - Initial release
 *
 */

jQuery.fn.nospam = function(settings) {
	settings = jQuery.extend({
		replaceText: false, 	// optional, accepts true or false
		filterLevel: 'normal' 	// optional, accepts 'low' or 'normal'
	}, settings);
	
	return this.each(function(){
		e = null;
		if(settings.filterLevel == 'low') { // Can be a switch() if more levels added
			if(jQuery(this).is('a[rel]')) {
				e = jQuery(this).attr('rel').replace('//', '@').replace(/\//g, '.');
			} else {
				e = jQuery(this).text().replace('//', '@').replace(/\//g, '.');
			}
		} else { // 'normal'
			if(jQuery(this).is('a[rel]')) {
				e = jQuery(this).attr('rel').split('').reverse().join('').replace('//', '@').replace(/\//g, '.');
			} else {
				e = jQuery(this).text().split('').reverse().join('').replace('//', '@').replace(/\//g, '.');
			}
		}
		if(e) {
			if(jQuery(this).is('a[rel]')) {
				jQuery(this).attr('href', 'mailto:' + e);
				if(settings.replaceText) {
					jQuery(this).text(e);
				}
			} else {
				jQuery(this).text(e);
			}
		}
	});
};

/*********************
//* jQuery Multi Level CSS Menu #2- By Dynamic Drive: http://www.dynamicdrive.com/
//* Last update: Nov 7th, 08': Limit # of queued animations to minmize animation stuttering
//* Menu avaiable at DD CSS Library: http://www.dynamicdrive.com/style/
*********************/

//Update: April 12th, 10: Fixed compat issue with jquery 1.4x

//Specify full URL to down and right arrow images (23 is padding-right to add to top level LIs with drop downs):
var arrowimages={down:['', ''], right:['', '']}

var jqueryslidemenu={

animateduration: {over: 200, out: 25}, //duration of slide in/ out animation, in milliseconds

buildmenu:function(menuid, arrowsvar){
	jQuery(document).ready(function($){
		$(" #main_navigation a").removeAttr("title");

		var $mainmenu=$("#"+menuid+">ul")
		var $headers=$mainmenu.find("ul").parent()
		$headers.each(function(i){
			var $curobj=$(this)
			var $subul=$(this).find('ul:eq(0)')
			this._dimensions={w:this.offsetWidth, h:this.offsetHeight, subulw:$subul.outerWidth(), subulh:$subul.outerHeight()}
			this.istopheader=$curobj.parents("ul").length==1? true : false
			$subul.css({top:this.istopheader? this._dimensions.h+"px" : 0})
			/*
			$curobj.children("a:eq(0)").css(this.istopheader? {paddingRight: arrowsvar.down[2]} : {}).append(
				'<img src="'+ (this.istopheader? arrowsvar.down[1] : arrowsvar.right[1])
				+'" class="' + (this.istopheader? arrowsvar.down[0] : arrowsvar.right[0])
				+ '" style="border:0;" />'
			)*/
			
			$curobj.hover(
				function(e){
					var $targetul=$(this).children("ul:eq(0)")
					this._offsets={left:$(this).offset().left, top:$(this).offset().top}
					
					if(jQuery.browser.msie){
						var menuleft=this.istopheader? 0 : this._dimensions.w +2
						menuleft=(this._offsets.left+menuleft+this._dimensions.subulw>$(window).width())? (this.istopheader? -this._dimensions.subulw+this._dimensions.w : -this._dimensions.w) -4 : menuleft
					}
					if(!jQuery.browser.msie){
						var menuleft=this.istopheader? 0 : this._dimensions.w
						menuleft=(this._offsets.left+menuleft+this._dimensions.subulw>$(window).width())? (this.istopheader? -this._dimensions.subulw+this._dimensions.w : -this._dimensions.w) : menuleft
					}
					if ($targetul.queue().length<=1) //if 1 or less queued animations
						$targetul.css({left:menuleft+"px", width:this._dimensions.subulw+'px'}).slideDown(jqueryslidemenu.animateduration.over)
				},
				function(e){
					var $targetul=$(this).children("ul:eq(0)")
					$targetul.slideUp(jqueryslidemenu.animateduration.out)
				}
			) //end hover
			$curobj.click(function(){
				$(this).children("ul:eq(0)").hide()
			})
		}) //end $headers.each()
		$mainmenu.find("ul").css({display:'none', visibility:'visible'})
	}) //end document.ready
}
}
//build menu with ID="main_navigation" on page:
jqueryslidemenu.buildmenu("main_navigation", arrowimages)


jQuery(document).ready(function() {
	if(!jQuery.browser.msie){
			button_hover()
			sociable_hover();
			fade_hover();
		}

	/* 
	 * Cufon 
	 */
	var $disable_cufon = jQuery("meta[name=disable_cufon]").attr('content');
	
	if($disable_cufon !='true') {
		
			Cufon.replace('h4,h5,#site_name,.dropcap1,.dropcap4,.teaser_large', { });
			Cufon.replace('#blurb,#footer_teaser_text', { textShadow: '#f9f9f9 1px 1px' });
			Cufon.replace('th,.light_gradient', {
				color: '-linear-gradient(#bbb, #888)',
				hover: 'true'
			});
			Cufon.replace('h3', {
				color: '-linear-gradient(#bbb, #888)'});
			Cufon.replace('h1,.staged_slide h2, .partial_staged_slide h2, .floating_slide h2, .full_slide h2, #body_block_background h2,.widgettitle,.dropcap2,.dark_gradient', {
				color: '-linear-gradient(#999, #4d4d4d)',
				hover: 'true',
				textShadow: '#fff 1px 1px'
			});
			Cufon.replace('.partial_gradient_slide h2', { });
			Cufon.replace('.large_button', { textShadow: '0 -1px 0 #888888' });
			
			Cufon.replace('.toggle_frame h4.toggle', {color: '-linear-gradient(#bbb, #888)',hover: 'false' });
			
			//fix flash of unstyled content with cufon
			jQuery('h1,h2,h3,h4,h5,#blurb,#site_name,.toggle,.light_gradient.dropcap1,.widgettitle,.dropcap2,.dropcap4,.teaser_large,.dark_gradient,th').each(function(){
				jQuery(this).css("text-indent", "0px");
				});

			var userAgent = navigator.userAgent.toLowerCase();
		    if(jQuery.browser.msie){
				var $ieVersion = jQuery.browser.version.substring(0,1);
				if($ieVersion == 7){
					jQuery(".dropcap1").css({paddingTop:"2px"});
				}
		    }
			
	}
	
	
	/*
	 * prettyPhoto 
	 */
	jQuery("a[rel^='prettyPhoto'], a[rel^='lightbox']").prettyPhoto({
		overlay_gallery: false, "theme": 'light_rounded' /* light_square / dark_rounded / light_square / dark_square */															
	});
	
	
	/* 
	 * toggle functions 
	 */
	//Hide (Collapse) the toggle containers on load
	jQuery(".toggle_content").hide(); 

	//Switch the "Open" and "Close" state per click
	jQuery("h4.toggle").toggle(function(){
		jQuery(this).addClass("active");
		}, function () {
		jQuery(this).removeClass("active");
	});

	//Slide up and down on click
	jQuery("h4.toggle").click(function(){
		jQuery(this).next(".toggle_content").slideToggle();
	});
	
	
	/* 
	 * tooltip functions 
	 */
	//sociable tooltip
	jQuery(".share_this_post").tooltip({ effect: 'slide', relative: false, tip: '.share_this_post_tooltip', offset: [20, 67] });

	//site search tooltip
	jQuery("#menu_search").tooltip({ effect: 'slide' , relative: true, offset: [70, -45]});

	//tooltip shortcode
	jQuery(".tooltip_btn_sc").tooltip({ effect: "slide", relative: true, offset: [20, -6], tipClass: "tool_tip" });
	jQuery(".tooltip_sc").tooltip({ effect: "slide", relative: true, offset: [20, 0], tipClass: "tool_tip" });
	jQuery(".tooltip_text").tooltip({ effect: "slide", offset: [0, 0] });


	/* 
	 * tab functions
	 */
	jQuery(function() {
		jQuery("ul.tabs").tabs("> .tab_content");
	});
	
	jQuery(function() {
		jQuery(".minimal_tab_set ul.tabs").tabs("> .tab_content");
		jQuery(".framed_tab_set ul.tabs").tabs("> .tab_content");	
	});
	

	/* 
	 * "target_blank" links
	 */
	jQuery(".flickr_badge_image a").attr("target", "_blank");
	jQuery(".target_blank").attr("target", "_blank");


	/* 
	 * spam protction on mailto: links
	 */
	jQuery('a.email').nospam({
      replaceText: false,    
      filterLevel: 'normal'
    });

	jQuery('a.email_widget').nospam({
      replaceText: true,
      filterLevel: 'normal'
    });


	/* 
	 * contact form widget
	 */
	jQuery('form#contactFormWidget').submit(function() {
		
		// assign dynamic div height to footer
		var $h = jQuery(".footer_background").height();
		jQuery(".footer_background").css({height: $h});
		
		// assign dynamic div height to secondary
		var $sb_h = jQuery("#secondary").height();
		jQuery("#secondary").css({height: $sb_h});
		
		jQuery('form#contactFormWidget .error').remove();
		var hasError = false;
		jQuery('.requiredField').each(function() {
			if(jQuery.trim(jQuery(this).val()) == '') {
				var labelText = jQuery(this).prev('label').text();
				//jQuery(this).parent().append('<span class="error">You forgot to enter your '+labelText+'.</span>');
				jQuery(this).addClass('inputError');
				hasError = true;
			} else if(jQuery(this).hasClass('email')) {
				var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
				if(!emailReg.test(jQuery.trim(jQuery(this).val()))) {
					var labelText = jQuery(this).prev('label').text();
					//jQuery(this).parent().append('<span class="error">You entered an invalid '+labelText+'.</span>');
					jQuery(this).addClass('inputError');
					hasError = true;
				}
			}
		});
	
		if(!hasError) {
			
			jQuery("#submittedWidget").css('display','none'); 
			jQuery(".loadingImgWidget").fadeTo("slow", 0.5);
			
			var formInput = jQuery(this).serialize();
			jQuery.post(jQuery('#submitUrlWidget').val(),formInput, function(data){
				jQuery('form#contactFormWidget').fadeOut('fast', function() {		   
					jQuery(this).before('<p class="thanks"><strong>Thanks!</strong> Your email was successfully sent.</p>');
					});
			});
		}
	
		return false;
	
	});

	/* 
	 * contact form
	 */
	jQuery('form#contact_form').submit(function() {
		
		// assign dynamic div height to body_block
		var $h = jQuery("#main").height();
		jQuery("#main").css({height: $h});
		
		jQuery('form#contact_form .error').remove();
		var hasError = false;
		jQuery('.requiredFieldContact').each(function() {
			if(jQuery.trim(jQuery(this).val()) == '') {
				var labelText = jQuery(this).prev('label').text();
				//jQuery(this).parent().append('<span class="error">You forgot to enter your '+labelText+'.</span>');
				jQuery(this).addClass('inputError');
				hasError = true;
			} else if(jQuery(this).hasClass('email')) {
				var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
				if(!emailReg.test(jQuery.trim(jQuery(this).val()))) {
					var labelText = jQuery(this).prev('label').text();
					//jQuery(this).parent().append('<span class="error">You entered an invalid '+labelText+'.</span>');
					jQuery(this).addClass('inputError');
					hasError = true;
				}
			}
		});
	
		if(!hasError) {
			
			jQuery("#submittedContact").css('display','none'); 
			jQuery(".loadingImg").css('display','block');
		
			var formInput = jQuery(this).serialize();
			jQuery.post(jQuery('#submitUrl').val(),formInput, function(data){
				jQuery('form#contact_form').fadeOut('fast', function() {		   
					jQuery(this).before('<p class="thanks"><strong>Thanks!</strong> Your email was successfully sent.</p>');
				});
			});
		}
	
		return false;
	
	});
	

/* image preloader  */
	jQuery(function () {

		// class of the div containers
		var $imgContainerClass = ".img_loader";

		// grab the images
		var $images = jQuery($imgContainerClass+' span img');
		
		// image length
		var $max = $images.length;

		// remove them from DOM to prevent normal load
		jQuery('.rm_img').remove();

		// start loading
		if($max>0) {
			LoadImage(0,$max);
		}

	// loading function handler
	function LoadImage(index,$max) {

		if(index<$max) {

			// add list to div
			jQuery('<span id="img'+(index+1)+'"></span>').each(function() {
			   jQuery(this).appendTo(jQuery('.img_loader .load_img').eq(index));
			});

			// new image object
			var $img = new Image();
	
			// current image
			var $curr = jQuery("#img"+(index+1));
	
			// load current image
			jQuery($img).load(function () {
		
				// hide it first + .hide() failed in safari
				jQuery(this).css('display','none');
		
				//add alt attr
				//jQuery(this).attr({alt: ""});
	 
				// remove loading class from div and insert the image into it
				jQuery($curr).append(this);
		
				// fade it in
				jQuery(this).fadeIn('slow',function() {
					jQuery(this).parent().parent().css("background-image", "none");
			
					if(index == ($max-1)) {
							jQuery('div, li').removeClass('bg_hover');
							portfolio_img_hover();
							fade_hover();
							
						}else{
						  // we are loading next item
						  LoadImage(index+1,$max);
						}
				});
		
			}).error(function () {
				// if loading error remove div
				jQuery($curr).remove();
				// try to load next item
				LoadImage(index+1,$max);
			}).attr('src', jQuery($images[index]).attr('src')).attr('class', jQuery($images[index]).attr('class')).attr('title', jQuery($images[index]).attr('title')).attr('alt', jQuery($images[index]).attr('alt'));
	   	  }
		}
	});

});