$(function(){
     $.ajaxSetup({
          beforeSend: function() {
             $('#ajax-waiting').removeClass('hidden');
          },
          complete: function(){
             $('#ajax-waiting').addClass('hidden');
          },
          success: function() {}
    });

    function show_empty_form(){
        $('#buy-engine-form').removeClass('hidden');
        $("#buy-success-send").addClass('hidden');
    }

    $('[href="#buy-engine"]').click(function(){
      show_empty_form()
    });


    $('#id_buy_phone').inputmask({"mask": "+7 (999) 999-99-99"});



    function isEmail(email) {
      var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
      return regex.test(email);
    }

    function mail_check(){
        var email_input = $("input[name='mail']"),
            email=email_input.val();
        if (isEmail(email)){
            $("#buy-mail-error").addClass('hidden');
            return true;
        } else {
            $("#buy-mail-error").removeClass('hidden');
            return false;
        }
    }
    function isBlank(str) {
        return (!str || /^\s*$/.test(str));
    }

    function phone_check(){
        var phone_input = $("#id_buy_phone"),
            phone=phone_input.val(),
            completed = phone_input.inputmask('isComplete');
        if (isBlank(phone) || completed){
             $("#buy-phone-error").addClass('hidden');
            return true;
        } else {
            $("#buy-phone-error").removeClass('hidden');
            return false;
        }
    }

    function error_send(){
        $('#buy-error-send').removeClass('hidden');
        $("#buy-success-send").addClass('hidden');
    }
    function success_send() {
        $('#buy-error-send').addClass('hidden');
        $("#buy-success-send").removeClass('hidden');
        $('#buy-engine-form').addClass('hidden')[0].reset();
        $.magnificPopup.close();
    }

    $('#buy-engine-form').submit(function(event){
        var mail = mail_check(),
            phone=phone_check();
        event.preventDefault();
        if (mail && phone){
            var data = $(this).serializeArray().reduce(function(obj, item) {
                obj[item.name] = item.value;
                return obj;
            }, {});
            data['csrf'] = $("csrfmiddlewaretoken").val();

            $.post('/json/buy-engine/',data, function(resp){
                if ('success' in resp){
                   success_send()
                } else if ('errors' in resp) {
                    error_send()
                }

            });
        } else {
            event.preventDefault();
        }
    })
});