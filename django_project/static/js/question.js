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

    $('#id_question_phone').inputmask({"mask": "+7 (999) 999-99-99"});

    function isEmail(email) {
      var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
      return regex.test(email);
    }

    function mail_check(){
        var email_input = $("input[name='mail']"),
            email=email_input.val();
        if (isEmail(email)){
            $("#question-mail-error").addClass('hidden');
            return true;
        } else {
            $("#question-mail-error").removeClass('hidden');
            return false;
        }
    }
    function isBlank(str) {
        return (!str || /^\s*$/.test(str));
    }

    function phone_check(){
        var phone_input = $("#id_question_phone"),
            phone=phone_input.val(),
            completed = phone_input.inputmask('isComplete');
        if (isBlank(phone) || completed){
             $("#question-phone-error").addClass('hidden');
            return true;
        } else {
            $("#question-phone-error").removeClass('hidden');
            return false;
        }
    }
    function create_checker(input_selector, error_selector){
            checker = function(){
              var input = $(input_selector),
                value=input.val();
                if (!isBlank(value)){
                     $(error_selector).addClass('hidden');
                    return true;
                } else {
                    $(error_selector).removeClass('hidden');
                    return false;
                }
            };
            return checker
        }

    question_check = create_checker("textarea[name='question']","#question-comment-error");
    function error_send(){
        $('#question-error-send').removeClass('hidden');
    }
    function success_send() {
        $('#question-error-send').addClass('hidden');
        $("#question-success-send").removeClass('hidden');
        $("#ajax-waiting").addClass('hidden');
        $('#engine-question-form')[0].reset();
        $.magnificPopup.close();

    }

    $('#engine-question-form').submit(function(event){
        var mail = mail_check(),
            phone=phone_check();
            question=question_check();
        event.preventDefault();
        if (mail && phone && question){
            var data = $(this).serializeArray().reduce(function(obj, item) {
                obj[item.name] = item.value;
                return obj;
            }, {});
            data['csrf'] = $("csrfmiddlewaretoken").val();

            console.log(data);
            $.post('/json/question/',data,function(resp){
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