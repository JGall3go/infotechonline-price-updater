var swiper=new Swiper(".swiper",{effect:"coverflow",grabCursor:!0,centeredSlides:!0,slidesPerView:"auto",coverflowEffect:{rotate:0,stretch:0,depth:100,modifier:2,slideShadows:!0},spaceBetween:0,pagination:{el:".swiper-pagination",clickable:!0},on:{init:function(){this.slideTo(2,0)}}});let clickCount=0;function handleClick(e){var i=document.querySelectorAll(".swiper-slide")[e];if(i){var l=Array.from(i.parentNode.children).indexOf(i);if(clickCount++,console.log(clickCount),l===swiper.activeIndex||2===clickCount){if(l===swiper.activeIndex){var o=i.dataset.url;window.open(o,"_blank")}}else console.log("Primer clic ignorado");clickCount>=2&&(clickCount=0)}}function goToSlide(e){handleClick(e),swiper.slideTo(e)}