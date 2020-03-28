$(function () {
  displayResults();
  $('.clsYr').on('change', function () {
    displayResults();
  });
  $('#resultText').delegate('a', 'click', function () {
    var tokens = [];
    tokens = $(this).attr('href').split('/');
    var params = {};
    params.file = tokens[tokens.length - 1];
    params.week = tokens[tokens.length - 2];
    params.year = $('.clsYr').val(); //tokens[tokens.length - 3];
    var path = './Results/' + params.year + '/' + params.week + '/' + params.file;
    $('#resultFrame').attr('src', path);
    $('#resultDetails').show();
    $('#resultText').hide();
    return false;
  });
  $('#detailBack').on('click', function () { $('#resultDetails').hide(); $('#resultText').show(); });
  $('#posts').delegate('.result', 'click', function () {
    $('#resultDetails').hide();
    $('#resultText').show();
    var params = {};
    params.year = $('.clsYr').val();
    params.meet = $(this).attr('id');
    $.get('/MCSLData.svc/ResultText',
    params,
    function (data, textStatus) {
      if (textStatus == "success") {
        if (data.d.Format == "pdf" || data.d.Format == "txt") {
          $('#resultFrame').attr('src', data.d.Text);
          $('#resultDetails').show();
          $('#resultText').hide();
        }
        else {
          $('#resultText').show();
          $('#resultDetails').hide();
          $('#resultText').html(data.d.Text);
        }
        return false;
      }
    });
  });
});
function displayResults() {
  var params = {};
  $('#resultLinks').html('');
  $('#resultText').html('');
  $('#resultDetails').hide();
  $('#resultText').show();
  params.year = $('.clsYr').val();
  $.get('/MCSLData.svc/AvailableResults',
    params,
    function (data, status) {
      if (status == "success")
        $('#resultLinks').html(data.d);
    });
}