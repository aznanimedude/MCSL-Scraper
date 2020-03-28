var teamNames;
$(function ()
{
  $.ajaxSetup({
    cache: false,
    beforeSend: function ()
    {
      $("#loading").show();
    },
    complete: function ()
    {
      $("#loading").hide();
    }
  });
   teamNames = initTeams();
  $('#header').click(function ()
  {
    window.location = '/default.aspx';
  });
});
function initTeams()
{
  var names = '';
  $.ajax({
    method: 'GET',
    url: '../MCSLData.svc/Teams?year=-1',
    async: false,
    success: function (data)
    {
      var teams = data.d;
      $.each(teams, function (index, team)
      {
        if (names.length > 0) names += ';';
        nm = team.Abbreviation + " - " + team.Name;
        names += team.Abbreviation + ':' + nm;
      });
    }
  });
  return names;
}
function loadDivisions(divId, teamId)
{
  $.get('/MCSLData.svc/Divisions?year=-1', function (data)
  {
    var divCtrl = $('#' + divId).get(0);
    divCtrl.options.length = 0;
    divCtrl.options[0] = new Option('All', '');
    var divs = data.d;
    $.each(divs, function (index, div)
    {
      divCtrl.options[divCtrl.options.length] = new Option(div, div);
    });
    loadTeams(divId, teamId);
  });
}
function loadTeams(divId, teamId)
{
  $.get('/MCSLData.svc/Teams?division=' + $('#' + divId).val() + '&year=-1',
    function (data)
    {
      var teamCtrl = $('#' + teamId).get(0);
      teamCtrl.options.length = 0;
      teamCtrl.options[0] = new Option('<Select Team>', '');
      var teams = data.d;
      $.each(teams, function (index, team)
      {
        teamCtrl.options[$('#lstTeams').get(0).options.length] = new Option(team.Abbreviation + ' - ' + team.Name, team.Abbreviation);
      });
    });
}
