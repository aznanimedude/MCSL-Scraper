function getNearbyPools(addr, dist, parent, busyImg)
{
  busyImg.show();
  parent.empty();
  $.ajax({
    url: '/MCSLData.svc/Teams?division=&year=-1',
    type: 'GET',
    success: function (data)
    {
      $.each(data.d, function (idx, team)
      {
        $('#findMap').gmap3({
          getdistance: {
            options: {
              origins: [addr],
              destinations: [team.Address + ',' + team.City || "" + ',' + 'MD' + ' ' + team.ZipCode || ""],
              travelMode: google.maps.TravelMode.DRIVING
            },
            callback: function (results, status)
            {
              if (results)
              {
                for (var i = 0; i < results.rows.length; i++)
                {
                  var elements = results.rows[i].elements;
                  for (var j = 0; j < elements.length; j++)
                  {
                    switch (elements[j].status)
                    {
                      case "OK":
                        var miles = (0.621371 * elements[j].distance.value) / 1000;
                        if (miles <= dist)
                        {
                          if (team.Url != null)
                            parent.append('<li><a href="' + team.Url + '" target="_blank">' + team.Name + '</a> (' + miles.toFixed(2) + ' miles)</li>');
                          else
                            parent.append('<li>' + team.Name + ' (' + miles.toFixed(2) + ' miles)</li>');
                        }
                        break;
                      case "NOT_FOUND":
                        break;
                      case "ZERO_RESULTS":
                        break;
                    }
                  }
                }
              }
            }
          }
        });
      });
    }
  });
  busyImg.hide();
}