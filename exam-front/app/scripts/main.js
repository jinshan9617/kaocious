require.config({
    paths: {
        jquery: '../bower_components/jquery/jquery',
        bootstrap: '../bower_components/bootstrap/dist/js/bootstrap',
        cookie: '../bower_components/jquery.cookie/jquery.cookie'
    },
    shim: {
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        },
        cookie: {
            deps: ['jquery']
        }
    }
});

require(['jquery', 'bootstrap', 'cookie'], function ($) {
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    document.getElementById("login_btn").onclick = function(e){
        var user_id = document.getElementById('user_id').value;
        
        if(!user_id.replace(" ","")){
            alert('userID can not be empty!');
            return false;
        }
        $.post("/login",
            {"user_id":user_id},
            function(data){
                alert(data);
            });
        
    };

    document.getElementById("start_btn").onclick = function(e){
        $.get('/questions',
            function(data){
                document.getElementById("questions").innerText = JSON.stringify(data);
            });
    };

    document.getElementById("answer_btn").onclick = function(e){
        var option = document.getElementById("option").value;
        $.post('/answer/q0001',
            {
                "type":"select_question",
                "options":[option]
            },
            function(data){
                alert(data);
            });
    };

    document.getElementById('submit_paper_btn').onclick = function(e){
        $.get('/report',
        function(data){
            document.getElementById("report").innerText = JSON.stringify(data);
        });
    };

});
