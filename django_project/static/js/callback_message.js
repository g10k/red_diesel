$(document).ready(function() {
    $.ajaxSetup({
      beforeSend: function() {
         $('#ajax-waiting').removeClass('hidden');
      },
      complete: function(){
         $('#ajax-waiting').addClass('hidden');
      },
      success: function() {

      }
    });


    function show_empty_form(){
        $('#callback-form').removeClass('hidden');
        $("#success-send").addClass('hidden');
    }

    function success_submit_form(){
        $('#error-send').addClass('hidden');
        $("#success-send").removeClass('hidden');
        $('#callback-form').addClass('hidden')[0].reset();
    }

    $('#id_phone').inputmask({"mask": "+7 (999) 999-99-99"});
    function isBlank(str) {
            return (!str || /^\s*$/.test(str));
        }
    function phone_check(){
        var phone_input = $("#id_phone"),
            phone=phone_input.val(),
            completed = phone_input.inputmask('isComplete');
        if (!isBlank(phone) && completed){
             $("#phone-error").addClass('hidden');
            return true;
        } else {
            $("#phone-error").removeClass('hidden');
            return false;
        }
    }
        //function call_message_check(){
        //	var call_message =  $('#id_call-message').val();
        //
        //	if (!isBlank(call_message)){
        //		 $("#call-message-error").addClass('hidden');
        //		return true;
        //	} else {
        //		$("#call-message-error").removeClass('hidden');
        //		return false;
        //	}
        //};
    $('[href="#callback"]').click(function(){
      show_empty_form()
    });
    $('#callback-form').submit(function(event){
        var phone=phone_check();
        console.log(phone);
        event.preventDefault();
        if (phone){
            var phone_text=$("#id_phone").val(),
                call_message =  $('#id_call-message').val(),
                csrf = $("csrfmiddlewaretoken").val();
            data = {
                'phone':phone_text,
                'call_message':call_message,
                'csrfmiddlewaretoken':csrf
            };
            $.post('/call-message/', data, function(resp){
                if ('success' in resp){
                    success_submit_form();
                } else if ('errors' in resp) {
                    $('#error-send').removeClass('hidden');
                }

            });
        } else {
            event.preventDefault();
        }
    });
});