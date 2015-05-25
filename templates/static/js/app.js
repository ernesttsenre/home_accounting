$(document).ready(function(){
   $('body').on('click', 'button[type="submit"]', function(e) {
       $(this).button('loading');
   })
});