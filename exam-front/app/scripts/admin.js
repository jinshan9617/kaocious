require.config({
    paths: {
        jquery: '../bower_components/jquery/jquery',
        underscore: '../bower_components/underscore/underscore',
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
        },
        underscore: {
            exports: '_'
        }
    }
});

require(['underscore', 'jquery', 'bootstrap', 'cookie'], function (_, $) {
    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (true) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var new_q_btn = document.getElementById("new_question_link");
    new_q_btn.onclick = function(e){
        //clearContainer();
        renderNewQuestion();
    };

    document.getElementById("logout_link").onclick = function(e){
        $.post('/logout',{},function(data){
            window.location.href = 'index.html'
        });
    };

    function renderNewQuestion(){
        var newQuestionTemplate = document.getElementById("new_question").innerHTML;
        var template = _.template(newQuestionTemplate);
        document.getElementById("main").innerHTML = template({});
        var selQuestionBtn = document.getElementById('selq_btn');
        var proQuestionBtn = document.getElementById('proq_btn');
        selQuestionBtn.onchange = function(e){
            if(this.value !== 'on'){
                return false;
            }
            renderChoiceQuestion();
        };

        proQuestionBtn.onchange = function(e){
            if(this.checked !== true){
                return false;
            }
            renderProgramQuestion();
        };
    }

    function renderChoiceQuestion(){
        var choiceQuestionTemplate = document.getElementById("choice_question").innerHTML;
        var template = _.template(choiceQuestionTemplate);
        document.getElementById('question_content').innerHTML = template({});
        var addOptionBtn = document.getElementById("add_option_btn");
        addOptionBtn.onclick = function(e){
            renderOption();
        };
        var submitBtn = document.getElementById("submit_btn");
        submitBtn.onclick = function(e){
            var optioncan = document.getElementById("options");
            var options = optioncan.getElementsByClassName("option");
            var optionsdata = [];
            var correctoptions = [];
            for(var i=0, l=options.length; i<l; i++){
                optionsdata.push({
                    id: options[i].getElementsByClassName("option_id")[0].innerText,
                    txt: options[i].getElementsByClassName("option_txt")[0].value
                });
                if(options[i].getElementsByClassName("correct")[0].checked){
                    correctoptions.push(options[i].getElementsByClassName("option_id")[0].innerText);
                }
            }
            var senddata = {
                type: "select_qustion",
                description: document.getElementById("description").value,
                options: optionsdata,
                correct_answer: correctoptions
            };
            $.post(
                '/question/' + document.getElementById('question_id').value,
                {
                    "data": JSON.stringify(senddata)
                },
                function(data){
                    console(data);
                }
            );
        };
    }

    function renderProgramQuestion(){
        var newProgramQuestionTemplate = document.getElementById("program_question").innerHTML;
        var template = _.template(newProgramQuestionTemplate);
        document.getElementById('question_content').innerHTML = template({});
        document.getElementById('submit_btn').onclick = upload;
        function upload(){
            var file = document.getElementById('tester_file').files[0];
            var xhr = new XMLHttpRequest();
            var reader = new FileReader();
            reader.onload = function(e){
                data = reader.result;
                var formdata = new FormData();
                var senddata = {
                    type: "program_question",
                    description: document.getElementById("description").value
                };
                formdata.append('file', file);
                formdata.append('data', JSON.stringify(senddata));
                xhr.onreadystatechange = function(){
                    if(xhr.readyState==4 && xhr.status==200){
                        console.log(xhr.responseText);
                    }
                };
                xhr.open('POST', '/question/' + document.getElementById('question_id').value);
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                xhr.send(formdata);
            };
            reader.readAsDataURL(file);
        }
    }

    function renderOption(){
        var newOptionTemplate = document.getElementById('option').innerHTML;
        var template = _.template(newOptionTemplate);
        var options = document.getElementById("options");
        options.innerHTML += (template({"optionId": options.children.length+1}));
    }

});
