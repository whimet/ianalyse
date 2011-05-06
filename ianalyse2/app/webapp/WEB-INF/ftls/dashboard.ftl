<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <script type="text/javascript" src="/ianalyse2/javascripts/jquery-1.5.2.min.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/highcharts.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/exporting.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/compare-projects.js"></script>
    <script type="text/javascript" src="/ianalyse2/javascripts/commitors.js"></script>
</head>
<body>
<h1>Passed/Failed builds between projects hah<h1>
<div id="container"></div>

<#list projects as x>
  <div id="projects-${x}">
  </div>
  <script>
  jQuery(document).ready(function() {
  $.ajax({
    url: "/ianalyse2/project/${x}/commitors.json",
    success: function(data, textStatus, jqXHR){
          var obj = jQuery.parseJSON(jqXHR.responseText);
          render_commitors(obj, "projects-${x}")
    }
  });
  })
  </script>
</#list>
</body>
</html>
