var today = new Date();
var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
var curYear = today.getFullYear();
var dateTime = date+' '+time;

$(function () {
    $('#datetimepicker').datetimepicker({
        inline: true,
        sideBySide: true
    });
});

function getByType(value) {
    var jsonObject = {
        'type':value
    }
    
    $.ajax({
        url:'/show_by_type',
        data: JSON.stringify(jsonObject),
        type:'POST',
        success:function(response) {
            $('#container').empty()
            $('#new_container').html(response.data)
        },
        error:function(response){
            $(alert('it doesnt work'))
        },
        datatype:'json',
        contentType:'application/json; charset = utf-8'
    });
}

function getByAll() {
    
    
    $.ajax({
        url:'/show_by_all',
        type:'POST',
        success:function(response) {
            
            $('#container').empty()
            $('#new_container').html(response.data)
        },
        error:function(response){
            $(alert('it doesnt work'))
        },
        datatype:'json',
        contentType:'application/json; charset = utf-8'
    });
}

var widths = [700];

function resizeFn() {
    if (window.innerWidth>=widths[0]) {
        changeStatusFullScreen();
    } else {
        changeStatusSmallScreen();
    }
}


function changeStatusFullScreen(){
    $('ul.dropdown-content li').click(function() {
        $(document.getElementById('status_hidden').value = $(this).text())
        $('#search_button_hide').click();
    });
    
    $('form').on('submit', function(event) {
        event.preventDefault();
    });
}

function changeStatusSmallScreen() {
    $('ul.dropdown-content li').click(function() {
        $(document.getElementById('status_hidden').value = $(this).text())
        $('#search_button_hide').click();
    });

    $('form').on('submit', function(event) {
        event.preventDefault();
    });
}

var geocoder;
var map;
function codeAddress() {
    geocoder = new google.maps.Geocoder();
    var lat='';
    var lng=''
    var address = document.getElementById('address').innerHTML;
    geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
       lat = results[0].geometry.location.lat(); //getting the lat
       lng = results[0].geometry.location.lng(); //getting the lng
    map.setCenter(results[0].geometry.location);
    var marker = new google.maps.Marker({
        map: map,
    position: results[0].geometry.location
    });
    } else {
            alert("Geocode was not successful for the following reason: " + status);
            }
    });
    var latlng = new google.maps.LatLng(lat, lng);
    var myOptions = {
        zoom: 15,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    }


window.onload = function(){
    codeAddress();
    window.addEventListener('resize', resizeFn);
    resizeFn();
}

function addAttendingStatus(){
    $.ajax({
        data : {
            attending_status:$('#status_hidden').val(),
            event_id:$("#event_id").val(),
            user_id:$("#user_id").val()
        },
        url:'/add_attending_status',
        type:'POST',
        success:function(response) {
            $('#old_container').html(response.data)
        },
    })
    .done(function(){
        $('#status_id_new').html("Your Status: " + $('#status_hidden').val());
        resizeFn();
    })
};

function updateAttendingStatus(){
    $.ajax({
        data : {
            attending_status:$('#status_hidden').val(),
            event_id:$("#event_id").val(),
            user_id:$("#user_id").val()
        },
        url:'/change_attending_status',
        type:'POST',
        success:function(response) {
            $('#attending_status_container').empty('')
            $('#new_attending_status').html(response.data)
        }
    })
    .done(function(){
        $('#status_id').remove()
        $('#status_id_new').text("Your Status: " + $('#status_hidden').val());
    });
};